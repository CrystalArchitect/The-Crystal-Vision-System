# Security Policy

## Supported versions

Rolling: the latest `main` is the supported version.

## Reporting a vulnerability

Please report privately via GitHub → **Security** tab → **Report a vulnerability**
(private vulnerability reporting). If that is unavailable, open an issue titled
"security contact request" **without details** and a private channel will be arranged.
You can expect an acknowledgement within 7 days. Please do not disclose publicly
until a fix has shipped.

## Safety measures in this repo

- **CrystalBridge is fail-closed** (`src/crystalcore/gate.py`): every guest-AI call
  passes four checks — approval, permission, scope, provenance — and refusal is
  the default on any failure.
- **Append-only audit** (`src/crystalcore/audit.py`): every guest interaction is
  logged; the log is not rewritten.
- **Scoped guests** (`src/profiles/*/bridge_config.json`): each guest AI gets an
  explicit tool list; nothing is granted implicitly.
- **No secrets committed** — `.gitignore` blocks `.env`, keys, and credentials.

## Scope

Reports about the CrystalBridge MCP server, its consent gate and audit trail, or
leaked credentials are all in scope.
