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

- **Static demo only** — plain HTML/CSS/JS, no backend, no accounts, no cookies,
  no analytics, no data collection.
- **Simulated data** — wallet, credits, burn/mint, and receipts are illustrative
  client-side numbers. **Authority: HOLD** — not production, not mainnet, no token.
- **No secrets committed** — `.gitignore` blocks `.env`, keys, and credentials;
  the site needs none.

## Scope

Reports about the deployed demo site (XSS, dependency issues, misleading content)
or leaked credentials are in scope.
