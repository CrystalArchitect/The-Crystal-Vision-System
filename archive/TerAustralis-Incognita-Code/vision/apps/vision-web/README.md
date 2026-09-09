# Crystal Vision · Citizen Shell

User-facing demo surface for the Crystal stack.

| Surface | Audience |
|---------|----------|
| **This app** (`vision/apps/vision-web`) | Citizens / end users |
| `vision/apps/crystal-interface` | Operators / builders |
| TerAustralis + Starline | Investor / pilot narrative |

**Not production.** Credits, capabilities, and receipts are client-side demo only. Authority **HOLD**. Cultural metaphors (Seven Sisters / Songline) are collaborative framing only — not ownership claims.

**Honest scope of the simulation.** So the words match the code: "credits" is a
single in-memory balance — the **dual-currency (AUD-C / EUR-C) framing is
illustrative**, not implemented. Receipts are marked `confirmed` locally; there
is **no real dual-attestation**. Capability grants and GDPR export/erase are
client-side stubs. Nothing here calls a server.

**Not a copy of `crystal-interface`.** This is a *separate, slimmer* citizen
surface. The operator shell (`crystal-interface`) is a different codebase.

## Open

```powershell
cd vision/apps/vision-web
# from vision/apps/ so cross-links work:
cd ..
python -m http.server 8090
# → http://127.0.0.1:8090/vision-web/
# → http://127.0.0.1:8090/crystal-interface/
```

## Panels

- **Home** — product map + citizen journey
- **My twin** — personal layer canvas (water / energy / mobility)
- **Consume** — capability grant + spend → receipt
- **Receipts** — local demo table
- **Privacy** — export / erase request stubs (GDPR path)

## Related

- Operator UI: `vision/apps/crystal-interface/`
- Mesh stub: `core/node/mesh/`
- Roadmap: [`Full-Stack-v0.5.md`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/architecture/Full-Stack-v0.5.md)
  (lives in the umbrella repo's `docs/`, not here)

*(Earlier drafts linked `docs/journeys/README.md` and `compliance/GDPR_ROPA.md`;
those don't exist in the repo, so they've been removed rather than left dead.)*
