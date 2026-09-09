# GitHub — Development Platform

Not an AI: the ground every flow ends on. GitHub is where work stops being
conversation and becomes canon.

## Responsibilities

- Version control — the repository is the primary surface of truth
  ([Constitution §7](../governance/Constitution.md))
- Branching and pull requests — the only path to `main`
  ([`Review-Process.md`](../governance/Review-Process.md))
- Issues and Discussions — durable, linkable problem statements (templates
  in `.github/`)
- Actions — CI (`ci.yml`: syntax + self-tests + suites) and the Pages
  deploy (`deploy.yml`: builds `src/site/` on merge to `main`)
- CODEOWNERS — review routes to the maintainer by default

## Platform configuration

The intended setup for this repository: Issues, Discussions, and Actions
enabled; security scanning and Dependabot on; branch protection on `main`
(PRs required, CI required). Repository *settings* live outside the tree —
what's listed here is the target configuration; only the maintainer can
read or change the live values.

## Why it sits at the end of every flow

Every AI in [`AI-Workflow.md`](AI-Workflow.md) hands off through GitHub
because that's where the honesty mechanisms live: CI that runs the code
instead of admiring it, review that checks labels, history that keeps every
claim dated and attributable. Disk is canon — and this is the disk.
