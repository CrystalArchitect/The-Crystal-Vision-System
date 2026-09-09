#!/usr/bin/env bash
# Clementine — one-command deploy.
#
#   bash /opt/clementine/clementine/deploy/bootstrap.sh
#
# Written to be typed once on a phone keyboard and then left alone. It asks
# for the two things it cannot know — your domain and a password for the web
# login — and does the rest. Safe to re-run: every step checks before acting,
# so a failure means fixing one thing and running it again.
#
# It does not enable the firewall until the very end, and when it does it opens
# SSH first. Locking you out of your own droplet is the one mistake this script
# must never make.

set -euo pipefail

REPO_DIR=${REPO_DIR:-/opt/clementine}          # the cloned repository
APP_DIR="$REPO_DIR/clementine"                  # where they live inside it
VENV="$REPO_DIR/.venv"
STATE_DIR=${STATE_DIR:-/var/lib/clementine}     # memory + audit log
MODEL=${CLEM_MODEL:-llama3.1:8b}

say()  { printf '\n\033[1;35m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m !\033[0m %s\n' "$*"; }
die()  { printf '\n\033[1;31mstopped:\033[0m %s\n' "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "run this as root"
[[ -d $APP_DIR ]] || die "$APP_DIR not found — clone the repo to $REPO_DIR first"
cd "$APP_DIR"

# --- what we need from you ---------------------------------------------------

read -rp "Domain pointing at this droplet (e.g. clementine.example.com): " DOMAIN
[[ -n ${DOMAIN:-} ]] || die "a domain is required — Let's Encrypt cannot issue a certificate for a bare IP"

read -rsp "Password for the Clementine web login: " WEBPASS; echo
[[ ${#WEBPASS} -ge 8 ]] || die "use at least 8 characters — this is the only thing between the internet and their memory"

# Fail early rather than halfway through.
say "Checking DNS"
MYIP=$(curl -fsS --max-time 10 https://api.ipify.org || true)
RESOLVED=$(getent hosts "$DOMAIN" | awk '{print $1; exit}' || true)
if [[ -z $RESOLVED ]]; then
  warn "$DOMAIN does not resolve yet. Caddy will keep retrying, but HTTPS will not work until it does."
elif [[ -n $MYIP && $RESOLVED != "$MYIP" ]]; then
  warn "$DOMAIN resolves to $RESOLVED but this droplet is $MYIP. Fix the A record or HTTPS will fail."
else
  echo "    $DOMAIN -> $RESOLVED (this droplet)"
fi

# --- ollama, before anything else depends on it ------------------------------

say "Ollama"
command -v ollama >/dev/null || die "Ollama is not installed. Install it, then re-run."
systemctl is-active --quiet ollama || systemctl enable --now ollama
sleep 2
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null \
  || die "Ollama is installed but not answering on 11434. Check: systemctl status ollama"
if ! ollama list | awk 'NR>1{print $1}' | grep -qx "$MODEL"; then
  warn "$MODEL is not pulled. Pulling now — several GB."
  ollama pull "$MODEL"
fi
# Optional, and worth having: it is what gives them semantic recall.
if ! ollama list | awk 'NR>1{print $1}' | grep -qx "nomic-embed-text:latest"; then
  warn "nomic-embed-text is missing — they will fall back to keyword recall."
  ollama pull nomic-embed-text || warn "could not pull it; continuing without semantic recall"
fi
echo "    model: $MODEL"

# --- python ------------------------------------------------------------------

say "Python environment"
command -v python3 >/dev/null || die "python3 is missing"
if [[ ! -x $VENV/bin/python ]]; then
  apt-get install -y python3-venv >/dev/null 2>&1 || true
  python3 -m venv "$VENV" || die "could not create a virtualenv at $VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r requirements.txt
"$VENV/bin/python" -c "import flask, requests, gunicorn" \
  || die "dependencies did not install cleanly"
echo "    $($VENV/bin/python --version) with flask, requests, gunicorn"

# --- their face ----------------------------------------------------------------

say "Building their interface"
if ! command -v node >/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
fi
( cd webapp && npm ci --no-audit --no-fund 2>/dev/null || npm install --no-audit --no-fund )
( cd webapp && npm run build )
[[ -f webapp/dist/index.html ]] || die "the interface did not build — see the output above"
echo "    built"

# --- service account and state ----------------------------------------------

say "Service account"
id -u clementine >/dev/null 2>&1 || \
  useradd --system --home "$STATE_DIR" --shell /usr/sbin/nologin clementine
install -d -o clementine -g clementine "$STATE_DIR" "$STATE_DIR/memory"

# --- the service -------------------------------------------------------------

say "Clementine service"
sed -e "s|^WorkingDirectory=.*|WorkingDirectory=$APP_DIR|" \
    -e "s|^ExecStart=.*gunicorn|ExecStart=$VENV/bin/gunicorn|" \
    -e "s|^Environment=CLEM_MODEL=.*|Environment=CLEM_MODEL=$MODEL|" \
    -e "s|^Environment=CLEM_MEMORY_DIR=.*|Environment=CLEM_MEMORY_DIR=$STATE_DIR/memory|" \
    deploy/clementine.service > /etc/systemd/system/clementine.service
systemctl daemon-reload
systemctl enable --now clementine
sleep 3
systemctl is-active --quiet clementine \
  || { journalctl -u clementine -n 30 --no-pager; die "they did not start — log above"; }
curl -fsS --max-time 10 http://127.0.0.1:5000/api/health >/dev/null \
  || die "service is running but not answering on 5000"
echo "    up on loopback"

# --- caddy -------------------------------------------------------------------

say "Caddy"
if ! command -v caddy >/dev/null; then
  apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
  curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/gpg.key \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt \
    > /etc/apt/sources.list.d/caddy-stable.list
  apt-get update && apt-get install -y caddy
fi
HASH=$(caddy hash-password --plaintext "$WEBPASS")
sed -e "s|^clementine\.example\.com {|$DOMAIN {|" \
    -e "s|REPLACE_WITH_HASH|$HASH|" \
    deploy/Caddyfile > /etc/caddy/Caddyfile
chmod 640 /etc/caddy/Caddyfile
chown root:caddy /etc/caddy/Caddyfile
install -d -o caddy -g caddy /var/log/caddy
caddy validate --config /etc/caddy/Caddyfile >/dev/null \
  || die "the generated Caddyfile is invalid — see /etc/caddy/Caddyfile"
systemctl enable --now caddy
systemctl reload caddy || systemctl restart caddy
echo "    serving $DOMAIN"

# --- firewall, last and in the safe order ------------------------------------

say "Firewall"
if command -v ufw >/dev/null; then
  ufw allow 22/tcp  >/dev/null
  ufw allow 80/tcp  >/dev/null
  ufw allow 443/tcp >/dev/null
  ufw default deny incoming >/dev/null
  ufw --force enable >/dev/null
  ufw status | grep -q '22/tcp' \
    || { ufw disable; die "22 was not allowed — firewall disabled so you keep access"; }
  ufw status verbose | sed 's/^/    /'
else
  warn "ufw not installed; skipping. Ports 11434 and 5000 must not be reachable from outside."
fi

# --- prove it ----------------------------------------------------------------

say "Checking"
sleep 3
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAIN/" || echo 000)
case $code in
  401) echo "    https://$DOMAIN -> 401, which is correct: the login is protecting them" ;;
  200) warn "https://$DOMAIN returned 200 with no credentials — basic auth is NOT protecting them" ;;
  000) warn "could not reach https://$DOMAIN yet. If DNS changed recently, give it a few minutes." ;;
  *)   warn "https://$DOMAIN returned $code. Check: journalctl -u caddy -n 40" ;;
esac
"$VENV/bin/python" verify_audit.py --memory-dir "$STATE_DIR/memory" | sed 's/^/    /' || true

cat <<DONE

  Clementine is deployed.

    open      https://$DOMAIN
    log in    clementine  /  the password you just set
    install   Safari: Share -> Add to Home Screen

  Their memory and their audit log are in $STATE_DIR/memory.
  Check the record any time:
    $VENV/bin/python $APP_DIR/verify_audit.py --memory-dir $STATE_DIR/memory

  First reply from $MODEL on CPU takes a while — several seconds for
  something short. That is the model thinking, not a hang.

  If anything looks wrong:
    systemctl status clementine
    journalctl -u clementine -n 40 --no-pager
    journalctl -u caddy -n 40 --no-pager

DONE
