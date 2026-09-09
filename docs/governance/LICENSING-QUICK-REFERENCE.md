# Licensing Quick Reference – Visual Guide

> **Superseded — not adopted.** Companion doc to
> [`LICENSING-STRATEGY.md`](LICENSING-STRATEGY.md); the differentiated
> per-package model it visualizes was reverted in favor of uniform
> CC BY-NC-ND 4.0 — see [`ADR-0010`](../adr/ADR-0010.md). Kept for
> provenance, not in effect.

---

## 🎯 Decision Tree: Which License for Each Product?

```
┌─────────────────────────────────────────┐
│  Is this a core safety/protection      │
│  mechanism (hard to audit)?            │
└────────────────┬────────────────────────┘
        YES │                    │ NO
            │                    └─────────────────────┐
            │                                          │
            ▼                                          │
        ┌─────────────────┐              ┌────────────▼─────────────┐
        │ PROPRIETARY     │              │ Will we monetize this?   │
        │ (CrystalBridge) │              └────────────┬─────────────┘
        │                 │                     YES │  │ NO
        │ - Closed source │                        │  │
        │ - SaaS/deploy   │                        │  │
        │ - Premium price │                        │  │
        └─────────────────┘                        │  │
                                      ┌────────────▼─┐ │
                                      │ DUAL LICENSE │ │
                                      │ (CrystalCore │ │
                                      │ OS EI)       │ │
                                      │              │ │
                                      │ - MIT (free) │ │
                                      │ - Commercial │ │
                                      │ - $5K–$25K+  │ │
                                      └──────────────┘ │
                                                       │
                                      ┌────────────────▼─┐
                                      │ AGPL v3          │
                                      │ (Clementine, etc)    │
                                      │                  │
                                      │ - Open source    │
                                      │ - Free to use    │
                                      │ - Copyleft       │
                                      │ - Services $$    │
                                      └──────────────────┘
```

---

## 📊 License Comparison Matrix

```
┌──────────────────┬──────────┬──────────┬───────────┬──────────────┐
│ Aspect           │ AGPL v3  │ Dual     │ Propriet. │ CC BY-NC-ND  │
├──────────────────┼──────────┼──────────┼───────────┼──────────────┤
│ Cost             │ Free     │ Free+Paid│ Paid only │ Free (attr)  │
│ Commercial use   │ ✅ (open)│ ✅ (paid)│ ✅ (lic.) │ ❌ No        │
│ Modifications    │ ✅ share │ ✅ own   │ ❌ No     │ ❌ No        │
│ Sublicense       │ Inherit  │ Limited  │ Yes       │ No           │
│ Open source      │ ✅ Yes   │ ✅ Yes   │ ❌ No     │ ✅ Yes (art) │
│ Revenue model    │ Services │ Licenses │ Licensing │ NA           │
│ Adoption         │ High     │ High     │ Medium    │ Medium       │
│ Community        │ Large    │ Large    │ Small     │ Fans         │
└──────────────────┴──────────┴──────────┴───────────┴──────────────┘
```

---

## 🏷️ Product License Map

```
╔════════════════════════════════════════════════════════════════════╗
║ TeraAustralis Products & Licenses                                 ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  📱 CLEMENTINE (Companion)                                            ║
║  ├─ License: AGPL v3                                             ║
║  ├─ Strategy: Open source + support services                     ║
║  ├─ Revenue: Consulting, support contracts, SaaS variant         ║
║  └─ Contact: clementine@teraaustralis.dev                            ║
║                                                                    ║
║  🔌 STARLINE WEAVER (Message Bus)                                ║
║  ├─ License: AGPL v3                                             ║
║  ├─ Strategy: Open protocol + reference implementation           ║
║  ├─ Revenue: Integration consulting, enterprise support          ║
║  └─ Contact: starline@teraaustralis.dev                          ║
║                                                                    ║
║  🤝 CONSENT TRANSPORT (P2P Memory)                               ║
║  ├─ License: AGPL v3                                             ║
║  ├─ Strategy: Open cryptographic protocol                        ║
║  ├─ Revenue: Academic research support, security audits          ║
║  └─ Contact: consent@teraaustralis.dev                           ║
║                                                                    ║
║  📖 RDP (Record Kernel)                                          ║
║  ├─ License: AGPL v3                                             ║
║  ├─ Strategy: Open audit framework                               ║
║  ├─ Revenue: Compliance licensing, regulatory support            ║
║  └─ Contact: rdp@teraaustralis.dev                               ║
║                                                                    ║
║  🔐 CRYSTALBRIDGE (AI Safety Gate)                               ║
║  ├─ License: PROPRIETARY                                         ║
║  ├─ Strategy: Closed-source safety mechanism                     ║
║  ├─ Revenue: Per-deployment or SaaS licensing ($100K–$1M+)       ║
║  └─ Contact: bridge@teraaustralis.dev                            ║
║                                                                    ║
║  🧠 CRYSTALCORE.OS EI (Emotion Intelligence)                     ║
║  ├─ License: DUAL (MIT + Commercial)                             ║
║  ├─ Strategy: Free for research, paid for commercial             ║
║  ├─ Revenue: Commercial licenses ($5K–$25K+/year)                ║
║  └─ Contact: ei-licensing@teraaustralis.dev                      ║
║                                                                    ║
║  🎨 MYTHOS (Story/Art/Canon)                                     ║
║  ├─ License: CC BY-NC-ND 4.0                                     ║
║  ├─ Strategy: Creative commons, fan ecosystem                    ║
║  ├─ Revenue: Merchandise, fan support, Patreon                   ║
║  └─ Contact: mythos@teraaustralis.dev                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 💰 Revenue Model by License Type

### AGPL v3 (Clementine, Starline, Consent, RDP)
```
Free/Open Source → + Services = Revenue
                    
   ├─ Consulting integration
   ├─ Support contracts (SLA)
   ├─ Training workshops
   ├─ Certifications
   ├─ Premium hosting
   └─ Custom development

Annual: $100K–$500K per product (at scale)
```

### Dual License (CrystalCore.OS EI)
```
Non-Commercial (MIT)  →  Free
         +
Commercial License    →  Revenue ($5K–$25K+/year)

Annual: $50K–$200K (at scale)
```

### Proprietary (CrystalBridge)
```
Closed Source  →  High-value customers only
                  
   ├─ Per-deployment licenses ($100K–$1M)
   ├─ SaaS usage-based billing ($1K–$50K/mo)
   └─ Enterprise agreements (custom)

Annual: $500K–$2M+ (high-value customers)
```

---

## 🔄 Product Dependencies

```
Clementine (End-user facing)
    ↓ imports
    ├→ Starline (message bus)
    ├→ Consent (P2P secure)
    ├→ CrystalCore.OS EI (emotion detection)
    └→ CrystalBridge (safety gate)
    
Starline (Protocol)
    ↓ implements
    Clementine (hub agent)
    
Consent (Cryptography)
    ↓ (independent)
    (no deps)
    
RDP (Audit system)
    ↓ (independent)
    (used by systems needing audit trail)
    
CrystalBridge (Safety)
    ↓ (independent)
    (integrates via MCP)
    
CrystalCore.OS EI
    ↓ (independent)
    (emotion detection library)
    
Mythos (Canon)
    ↓ (artistic)
    (no code deps)
```

---

## ✅ Compliance Checklist

### For AGPL v3 Products

- [ ] Include LICENSE.md in repo root
- [ ] Add GPL header to all source files
  ```python
  """
  [Module name]
  
  Licensed under GNU Affero General Public License v3.0
  See LICENSE.md for details
  """
  ```
- [ ] Update README with AGPL v3 badge
- [ ] Create CONTRIBUTING.md with CLA statement
- [ ] Document how services differ from free software
- [ ] Provide dual-license option for proprietary users

### For Dual License Products

- [ ] Include LICENSE.md (MIT)
- [ ] Include COMMERCIAL_LICENSE.md
- [ ] Add LICENSING.md with decision tree
- [ ] Add license headers to source files (MIT style)
  ```python
  """
  [Module name]
  
  Licensed under MIT License (non-commercial)
  or Commercial License (commercial use)
  See LICENSE.md and COMMERCIAL_LICENSE.md
  """
  ```
- [ ] Set up licensing infrastructure (LicenseHub, Stripe)
- [ ] Create license key validation system

### For Proprietary Products

- [ ] Copyright notice in every file
  ```python
  """
  [Module name]
  
  Copyright (c) 2026 CrystalArchitect. All Rights Reserved.
  Proprietary and Confidential
  """
  ```
- [ ] Include LICENSE.md with proprietary terms
- [ ] Add access controls (if applicable)
- [ ] Set up licensing/deployment tracking
- [ ] Create commercial only support channels

### For All Products

- [ ] CHANGELOG.md with version history
- [ ] AUTHORS.md with contributor list
- [ ] SECURITY.md if applicable
- [ ] README.md with clear license statement
- [ ] Copyright year in main files

---

## 📋 License Text Locations

```
licenses/
├── AGPL-v3.0.txt              (Full text)
├── MIT.txt                    (Full text)
├── CC-BY-NC-ND-4.0.txt        (Full text)
│
packages/clementine/
├── LICENSE.md                 (AGPL v3 - copy from above)
│
packages/starline/
├── LICENSE.md                 (AGPL v3)
│
packages/consent-transport/
├── LICENSE.md                 (AGPL v3)
│
packages/rdp/
├── LICENSE.md                 (AGPL v3)
│
packages/crystalbridge/
├── LICENSE.md                 (Proprietary)
│
packages/crystalcore-ei/
├── LICENSE.md                 (MIT)
├── COMMERCIAL_LICENSE.md      (Custom commercial)
│
packages/mythos/
├── LICENSE.md                 (CC BY-NC-ND 4.0)
```

---

## 🚀 Next Steps

### Immediate (This week)
1. ✅ Review LICENSING-STRATEGY.md
2. ✅ Review REPO-RESTRUCTURING-PLAN.md
3. ⬜ Decide: Approve strategy? Modify? Other approach?
4. ⬜ Commit decisions in writing

### Week 2-3
5. ⬜ Create package directory structure
6. ⬜ Create pyproject.toml for each package
7. ⬜ Add LICENSE files to each package

### Week 3-4
8. ⬜ Move code into packages
9. ⬜ Update imports
10. ⬜ Test each package independently
11. ⬜ Set up CI/CD per package

### Week 5+
12. ⬜ Publish to PyPI
13. ⬜ Set up commercial licensing (if needed)
14. ⬜ Create separate GitHub repos (optional)

---

## 📞 Questions?

- **Licensing strategy**: See LICENSING-STRATEGY.md
- **Repo restructuring**: See REPO-RESTRUCTURING-PLAN.md
- **License texts**: See individual LICENSE.md files
- **Commercial licensing**: licensing@teraaustralis.dev
- **Contributing**: See CONTRIBUTING.md (per-package)

---

*TeraAustralis – Licensing Made Clear*
