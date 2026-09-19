# Deploying Clementine to a droplet

Written for the `Clementine` droplet, which already has Ollama installed and
`llama3.1:8b` pulled. Everything below runs as root over SSH unless noted.

There is **no `pip install`** step and **no `npm install` step**. The bridge is
plain Node with zero dependencies; the UI is plain Web Components with no build.
If you find yourself installing packages for Clementine itself, something has
gone wrong.

## What you need before starting

- A domain or subdomain you control (e.g. `clementine.yourdomain.com`).
- An **A record** for it pointing at the droplet's public IPv4 address.
  Let's Encrypt validates over HTTP, so this must resolve before step 4.
- Node 20 or newer on the droplet.

## 1. Node

```sh
node --version || {
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
}

# The service unit hardcodes /usr/bin/node. Confirm that is where yours is:
command -v node
```

If `node` is somewhere else (a `nvm` install, for instance), edit the
`ExecStart=` line in `deploy/clementine.service` to match, or the service will
fail to start with *"Command /usr/bin/node is not executable"*.

## 2. The code

```sh
git clone https://github.com/CrystalArchitect/clementine.git /opt/clementine
cd /opt/clementine
git checkout claude/full-review-6qas8j     # until this merges to main

# Service account that owns only its own audit log
useradd --system --home /opt/clementine --shell /usr/sbin/nologin clementine
mkdir -p backend/data
chown -R clementine:clementine backend/data
```

## 3. Confirm Ollama is actually serving

```sh
systemctl enable --now ollama          # if not already running
curl -s http://127.0.0.1:11434/api/tags | head -c 200
```

You should see JSON listing `llama3.1:8b`. If this fails, nothing downstream
will work — fix it here.

## 4. The bridge

```sh
cp deploy/clementine.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now clementine
systemctl status clementine --no-pager

# Proves the whole local path, model included. Takes a while on CPU.
curl -s -X POST http://127.0.0.1:8787/api/chat \
  -H 'content-type: application/json' \
  -d '{"message":"In one sentence: what is wise mind?"}'
```

If that returns a real sentence, Clementine is thinking on your droplet.

A 503 saying *"Local model unavailable"* means Ollama isn't reachable — that is
Clementine refusing rather than faking an answer, which is the intended
behaviour. Go back to step 3.

## 5. Caddy — HTTPS and authentication

```sh
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/gpg.key \
  | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt \
  | tee /etc/apt/sources.list.d/caddy-stable.list
apt-get update && apt-get install -y caddy

caddy hash-password        # type a strong password; copy the $2a$... output
```

Edit `deploy/Caddyfile`: replace `clementine.example.com` with your hostname
and `REPLACE_WITH_HASH` with that hash. Then:

```sh
cp deploy/Caddyfile /etc/caddy/Caddyfile
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

## 6. Firewall

Allow **only** 22, 80, and 443 inbound. Ports **11434** (Ollama) and **8787**
(the bridge) must never be reachable from outside — they have no
authentication of their own.

DigitalOcean → Networking → Firewalls, or on the droplet:

```sh
ufw default deny incoming
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp
ufw enable
ufw status verbose
```

**Do not pin the rules to your home IP address.** Mobile networks reassign
addresses constantly, and you will lock yourself out from your phone within a
day. Leave 443 open to the world and let basic auth do the gatekeeping — that
is what it is for.

## 7. Use it

Open `https://clementine.yourdomain.com` on your iPhone, enter the basic-auth
credentials, and in Safari choose **Share → Add to Home Screen**. You get an
icon that opens without browser chrome — not a native app, but close enough to
live with while the SwiftUI wrapper is built.

Voice input needs the padlock: it will not work over plain HTTP, which is why
step 5 is not optional.

## Verifying it end to end

```sh
# From your laptop, not the droplet:
curl -sI https://clementine.yourdomain.com | head -3          # expect 401
curl -sI -u clementine:YOURPASS https://clementine.yourdomain.com | head -3   # expect 200

# Ports that must be closed from outside:
nc -zv -w3 <droplet-ip> 11434    # expect refused/timeout
nc -zv -w3 <droplet-ip> 8787     # expect refused/timeout
```

On the droplet, confirm the continuity record is intact and growing:

```sh
node /opt/clementine/backend/verify-chain.mjs
```

## What to expect from llama3.1:8b on CPU

A quantised 8B model needs roughly 6 GB of RAM and, on a CPU-only droplet,
produces a few tokens per second. A short reply lands in several seconds; a long
one takes the better part of a minute. That is workable for turn-based
conversation and noticeably slower than a hosted API — the trade you are making
for the model being yours.

If it feels too slow, `ollama pull llama3.2:3b` and change `CLEM_MODEL` in the
service file. Smaller model, faster answers, less depth.

## Updating

```sh
cd /opt/clementine && git pull && systemctl restart clementine
```

The audit log lives in `backend/data/` and is gitignored, so updates never
touch your history.
