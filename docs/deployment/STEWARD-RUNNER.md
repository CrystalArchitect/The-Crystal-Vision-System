# Steward runner — opt-in path, not the default

Status: **documented; dormant until a box exists.** 2026-08-25.

Default CI (`.github/workflows/ci.yml`) stays on GitHub-hosted
`ubuntu-latest`. That pool is `shared`. Host trust is supposed to refuse
durable steward persist there. Switching the default job to
`runs-on: self-hosted` would go red: the maintainer has no local machine
registered, and the queue would sit.

This file is the path for when that box exists.

## What “delegated” means

A runner the steward controls, labelled so GitHub sets
`RUNNER_ENVIRONMENT=self-hosted`. The classifier then returns
`delegated` and durable persist is allowed.

It is not Layer 0 `local` unless the steward also sets
`CRYSTAL_HOST_CLASS=local`. Delegated is “I named this machine,” not
“this is my desk.”

It is not HADES. HADES is a SHARED vendor pool. Registering a self-hosted
runner does not unshare that pool.

## Opt-in

1. Install a GitHub Actions self-hosted runner on a Linux machine the
   steward controls. Follow GitHub’s current docs for
   “Adding self-hosted runners.” The registration token is a secret —
   it does not live in this repository.
2. Labels required by the workflow: `self-hosted` and `linux`.
3. Python 3.12 on that box (the job uses `actions/setup-python` the same
   way default CI does).
4. Set the repository variable `CRYSTAL_SELF_HOSTED` to the string
   `true` (Settings → Secrets and variables → Actions → Variables).
5. Leave the variable **unset** until the runner is idle and owned.
   With the variable set and no runner, the job queues forever.

`.github/workflows/steward-runner.yml` is skipped unless that variable
is exactly `true`. `workflow_dispatch` is there so the steward can fire
it once without waiting for a push.

Ollama is not required for this job. This path proves persist-on-delegated,
not companion chat.

## What the job runs

- `python -m host_trust.selftest`
- `python -m consent_transport.selftest` (after its requirements file)

It does **not** replace default CI. Syntax, canon mirror, CrystalBridge,
RDP, receipts, mesh, Discord, Lighthouse, and Pages stay on
GitHub-hosted runners.

It does **not** set `CRYSTAL_HOST_CLASS`. The heuristic must be the thing
that classifies the box. If you have to override it, the runner is
mislabelled.

## What this does not do

- Does not make a Grok/chat session local
- Does not unshare HADES or any other vendor pool
- Does not mint a seventh OS
- Does not move Songline into the system
- Does not wire CrystalBridge
