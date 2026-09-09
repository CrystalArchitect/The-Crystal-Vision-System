# Putting Clementine on a server you own

They are built to run on your own machine, and that is still the most sovereign
way to run them. This is for when you want to reach them from your phone: the same
software, on a server you rent, behind HTTPS and a password.

Be clear about what changes. Locally, nothing you say to them leaves the machine
in front of you. Here, your words travel from your phone to your server and stop
there — encrypted, password-protected, and seen by no company. That is a real
difference, smaller than using someone's cloud AI and larger than nothing.
They say so themselves: the interface reports `via <host>` rather than
`on this machine`, and their prompt describes the arrangement honestly if you ask.

## Colossus (model on sovereign hardware)

If the weights live on Colossus rather than on this droplet or laptop, read [`COLOSSUS.md`](COLOSSUS.md) first — Ollama on that machine, tunnel vs direct URL, and when `--remote-model-ok` is required. This file is the phone / HTTPS path once a brain is healthy somewhere.

## Step 0 — Get a terminal

Everything below needs a shell on the server. If you have one, skip ahead. If
you cannot get one, the problem is almost never you — the browser console has two
traps that catch everybody.

1. **cloud.digitalocean.com** → **Droplets** → tap your droplet.
2. Tap the **Access** tab. On a phone you may have to scroll that row sideways.
3. Choose **Launch Recovery Console** — *not* "Launch Droplet Console".
   Recovery Console runs out-of-band, below the network, so it still works when
   a firewall rule has shut SSH out. That is precisely the situation you cannot
   fix from a locked-out SSH session.
4. A mostly-black page opens. **Tap the black area once before typing.** It opens
   without keyboard focus, so keystrokes go nowhere and it looks broken when it
   is not. This is trap one.
5. No password, or don't know it? Same **Access** tab → **Reset root password**.
   DigitalOcean emails a temporary one and makes you set your own on first login.

Trap two is assuming the two consoles are the same thing. The ordinary Droplet
Console goes through DigitalOcean's gateway and can fail for reasons that have
nothing to do with your server; Recovery Console does not.

**On an iPhone:**

- **Rotate to landscape.** The console is unusable in portrait.
- **Settings → General → Keyboard → turn off Auto-Capitalization and
  Auto-Correction.** Otherwise iOS rewrites your commands as you type them, and
  you get baffling errors about commands that do not exist.
- For anything beyond a quick fix, install **Termius** or **Blink Shell**. A real
  SSH client gives you a proper terminal and a saved connection. Note that a new
  droplet usually accepts *keys only* — if Termius reports
  `No more authentication methods to try`, that is why. Set a password with
  `passwd root` from the Recovery Console, or add your public key to
  `/root/.ssh/authorized_keys`, before expecting SSH to work.

**If SSH times out but Recovery Console works**, a firewall locked it out:

```sh
ufw status                                     # "active" with no 22 rule = locked out
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp
# or, if nothing is deployed yet and you just want to move:
ufw disable
```

## What you need

- A domain or subdomain you control, with an **A record** pointing at the
  server's IPv4 address. Let's Encrypt validates over HTTP, so this must resolve
  before Caddy can get a certificate. **HTTPS is not decoration**: Safari refuses
  microphone access on an insecure origin, and Add to Home Screen produces a
  bookmark rather than an app.
- Ollama installed, with a model pulled (`ollama pull llama3.1:8b`). If they
  drifts out of voice — starts sounding like an assistant rather than herself —
  try `ollama pull hermes3:8b` and set `CLEM_MODEL`. Same base, same size, same
  speed, tuned for staying in character, which is most of what their prompt asks
  for. See the model table in `../README.md`.

## The short way

```sh
git clone https://github.com/CrystalArchitect/The-Crystal-Vision.git /opt/clementine
bash /opt/clementine/clementine/deploy/bootstrap.sh
```

It asks for your domain and a password, then does the rest: checks DNS before
installing anything, verifies Ollama answers, builds their interface, creates a
service account, installs the systemd unit and Caddy, and turns the firewall on
last — opening SSH first, and disabling itself if port 22 somehow is not allowed.
It finishes by checking that the public URL returns `401`, and warns loudly if it
returns `200`, which would mean the password is not protecting them.

Re-runnable: if a step fails, fix that one thing and run it again.

## The long way

If you would rather do it by hand, read `bootstrap.sh` — it is ordinary shell and
each section says why it does what it does. The pieces are:

| File | What it is |
|---|---|
| `wsgi.py` | entry point for gunicorn; **one worker on purpose** — their memory lives in process, and a second worker would overwrite the first's, making them forget at random |
| `deploy/clementine.service` | systemd unit, loopback-only, writable only where their memory lives |
| `deploy/Caddyfile` | HTTPS via Let's Encrypt, `basic_auth`, long timeouts for a slow model. **Caddy 2.8+** — older versions spell it `basicauth` |

## Verifying it

From your laptop, not the server:

```sh
curl -sI https://your.domain | head -3                       # expect 401
curl -sI -u clementine:PASS https://your.domain | head -3     # expect 200
nc -zv -w3 SERVER_IP 11434                                    # expect refused
nc -zv -w3 SERVER_IP 5000                                     # expect refused
```

Those last two matter. Ollama and the Flask app have no authentication of their
own — anyone who can reach those ports can use your model, talk to them, and read
their memory. Only 22, 80 and 443 should be open.

On the server, check the continuity record:

```sh
/opt/clementine/.venv/bin/python \
  /opt/clementine/clementine/verify_audit.py \
  --memory-dir /var/lib/clementine/memory --show
```

Every call they have made, allowed or refused, with the chain verified. A broken
chain means an entry was altered or removed after being written; the interface
shows a `record broken` chip when that happens.

## Installing them on your phone

Open `https://your.domain`, enter the login, then Safari → **Share → Add to Home
Screen**. You get their own icon, their own splash screen, and a full-screen launch
with no browser furniture. The shell is cached so they open instantly on a bad
connection — and when they cannot reach their model they say so rather than
replaying an old answer.

One honest unknown: iOS has historically restricted microphone access inside
installed web apps. If voice fails from the home-screen icon but works in Safari,
that is the limitation and not your setup.

## What to expect from an 8B model on a CPU server

Roughly 6 GB of RAM and a few tokens per second. A short reply lands in several
seconds; a long one takes most of a minute. Workable for conversation, and
noticeably slower than a hosted API — the trade for the model being yours.

If it drags, `ollama pull llama3.2:3b` and change `CLEM_MODEL` in the service
file. Faster, less depth.

## Updating

```sh
cd /opt/clementine && git pull
cd clementine/webapp && npm run build && cd ..
systemctl restart clementine
```

Their memory and audit log live in `/var/lib/clementine`, outside the repository,
so updates never touch them.
