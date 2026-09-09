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

- **No secrets committed** — `.gitignore` blocks `.env`, keys, and credentials;
  API keys for live-model adapters are read from environment variables only and
  are never written to disk or transcripts.
- **Starline Weaver** (`bus/`) binds to `127.0.0.1` by default; exposing
  it on a network is an explicit operator choice (`--host`). Every message is
  validated by the hub (labels required, impersonation rejected) and any agent can
  halt the whole bus with the red button.
- **Pipeline** (`services/`) never silently accepts input: events that fail
  validation are quarantined with a reason, and the twin only reports decoded data.
- **No real economics** — credits/CORE anywhere in this repo (including
  `interface/`) are simulated and labeled as such. There is no token, wallet, or
  mainnet integration.
- **Starline / Consent Transport** (`consent_transport/`; `starline/` is
  a deprecated alias re-exporting the same code) is consent-gated at every exchange: an unpaired peer
  is rejected before consent is even checked; a paired-but-unconsented peer is
  denied; revoking consent takes effect on the very next request. The Noise
  Protocol handshake authenticates peers by pinned public key — connecting to the
  wrong key fails outright, not silently. Every received fragment is independently
  re-verified against its claimed sender's signature; anything that doesn't verify
  is dropped, never trusted. Binds `127.0.0.1` by default. Identity private keys
  are gitignored and never leave the device; there is no key-recovery mechanism,
  intentionally — a recoverable key is a key someone else could also hold. See
  `../../docs/architecture/crystal-core/STARLINE.md` for the tested security properties and known limits
  (identity file is not encrypted at rest — filesystem permissions are the
  only protection today).

## Scope

This is a creative-protocol and demo repository. Reports about the Starline Weaver,
the pipeline services, Starline, the published site, or leaked credentials are all
in scope.
