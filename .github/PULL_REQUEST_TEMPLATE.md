# What changed

<!-- Plain description of the change and why. -->

## Belt-Three label

<!-- Which layer does this change live on? Keep the labels honest
     (the umbrella's CONTRIBUTING.md / docs/governance/The-Incognita-Rule.md). -->

- [ ] **Science / Built** — running code, tests, checkable facts
- [ ] **Story / Vision** — speculative framing (labeled as such)
- [ ] **Docs / process**

## AI tools used

<!-- Canon law: every PR names the AI tools that helped produce it
     (umbrella's docs/governance/AI-Governance.md). "None" is a fine answer. -->

## Checks run

<!-- Paste what you ran and the results — claims come with evidence.
     CI (.github/workflows/ci.yml) runs the same checks. -->

- [ ] `python -m compileall -q core vision`
- [ ] Crystal Core self-tests (`bus` / `services` / `starline` / `rdp`, in `core/crystal-core/`)
- [ ] Mesh stub tests (`cd core && PYTHONPATH=. pytest tests -q`)
- [ ] `pytest vision/apps/clementine-discord/tests`
- [ ] Site builds (`cd vision/site && npm run build`) — if the site changed
- [ ] No generated files, secrets, or personal data staged

## For the reviewer

<!-- Anything that needs a second pair of eyes: judgment calls, deviations
     from a spec, an ADR if the change is structural. Cross-repo context
     (boundary charter, migration plan) lives in the umbrella repo,
     TerAustralis-Incognita. -->
