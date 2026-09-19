# Freeze checklist — cut tag `crystalcore-os-0.3-freeze-2026-09-11`

Run on a machine that can see CrystalArchitect private repos. Tick in order. Do not skip 3 or 7.

## 0. Identity

- [ ] Company name on the tag README: **TerAustralis Incognita**
- [ ] Product name: **CrystalCore.OS**
- [ ] Version on the web shell README remains **v0.3** until a real 1.0 ships
- [ ] No `v∞`, no “Year 3000 Build” on the product README

## 1. Single tree

- [ ] Create or restore public repo `CrystalArchitect/CrystalCore.OS` **or** a `product/` folder with a signed export zip
- [ ] Copy into it only the bill of materials in `02-WHAT-RUNS.md` section D
- [ ] Add this freeze pack under `freeze/2026-09-11/`
- [ ] Do not squash-delete the 20 source repos. Monorepo memory already forbids that without per-repo Crystal confirmation

## 2. License

- [ ] Crystal stamps `03-LICENSE-SPLIT.md`
- [ ] `LICENSE-CODE` and `LICENSE-MYTHOS` added
- [ ] SPDX headers on new/changed files
- [ ] NOTICE updated

## 3. WHAT-RUNS matches the files

- [ ] Every path in section A exists in the tag
- [ ] Every path in section C is absent from feature lists
- [ ] `README.md` top paragraph equals the one-sentence definition in WHAT-RUNS §E

## 4. Secrets

- [ ] No `.env`, no API keys, no personal Drive drawer 09
- [ ] `backend/.env.example` only
- [ ] `git log -p` scanned for keys before the tag

## 5. Tests (author pass — required)

From product backend:

```bash
cd backend
python -m pytest tests/ -q
```

From July snapshot if included as provenance:

```bash
python run_tests.py
```

From protocol tree if linked:

```bash
# historical commands from the umbrella guide
python -m bus.selftest
python -m services.selftest
python -m consent_transport.selftest
python -m rdp.selftest
```

- [ ] Raw stdout saved as `freeze/2026-09-11/test-log-author.txt`
- [ ] Counts written into `05-TEST-LOG-TEMPLATE.md`

## 6. Third-party or second-machine pass (required for the high end of the valuation)

- [ ] Same commands on a clean clone, different machine
- [ ] Output attached as `test-log-independent.txt`
- [ ] If this box is empty, the artifact stays at the low-mid of the range

## 7. Hash and tag

```bash
git add -A
git commit -m "CrystalCore.OS v0.3 paper freeze 2026-09-11"
git tag -a crystalcore-os-0.3-freeze-2026-09-11 -m "Product freeze. Company: TerAustralis Incognita."
git rev-parse HEAD > freeze/2026-09-11/HEAD.sha
sha256sum $(git ls-files) > freeze/2026-09-11/TREE.sha256
git push origin main --tags
```

- [ ] Annotated tag exists
- [ ] SHA256 list filed
- [ ] GitHub Release attached with WHAT-RUNS.md as the release body

## 8. Demos

- [ ] Local `index.html` confirmed
- [ ] Vercel/Pages restored **or** the README stops advertising dead URLs
- [ ] Canonical hostname either reclaimed or struck from README

## 9. Stop conditions (do not tag if true)

- Tree still 404 and no private export zip
- License still ND on runnable code **and** the asking price assumes a commercial buyer
- README still calls it a kernel
- Test log is a screenshot of a chat, not raw runner output
