# TeraAustralis Incognita – Comprehensive Licensing Strategy

**Protecting innovation while enabling community access across seven distinct products.**

> **Superseded — not adopted.** This strategy's differentiated per-package
> licensing (AGPL v3 / Proprietary / Dual / CC BY-NC-ND) was implemented in
> `packages/*/LICENSE.md` and `packages/*/pyproject.toml`, then reverted:
> the maintainer decided the whole repository stays uniformly CC BY-NC-ND
> 4.0 instead, weighing operational simplicity for a pre-revenue project
> over per-product legal nuance. See [`ADR-0010`](../adr/ADR-0010.md). Kept
> for provenance and as the reasoning to revisit if the calculus changes
> later (e.g. an actual paying customer for one specific package).

---

## Executive Summary

The repository currently mixes seven products under Apache-2.0, creating IP exposure if any become commercially valuable. This strategy recommends **splitting into separate packages with differentiated licensing**:

- **3 products** → AGPL v3 (open protocol + copyleft protection)
- **2 products** → Dual license (free open source + paid commercial)
- **1 product** → Proprietary (keep closed-source)
- **1 product** → CC BY-NC-ND (story/art, unchanged)

**Result**: Clear IP boundaries, sustainable commercial model, community accessibility.

---

## Product Analysis & Recommendations

### 1. 📱 **Clementine** (The Sovereign Companion)
**Location**: `vision/apps/clementine/`  
**What it is**: Local-first AI companion with persona, memory, Flask API, web UI

**Strategic Value**: ⭐⭐⭐⭐⭐ **VERY HIGH**
- User-facing product with differentiation
- Could become SaaS offering
- Companion persona is core IP
- Local-first UX is competitive advantage

**Current license**: Apache-2.0 (❌ Too permissive)

**Recommended license**: **AGPL v3**
```
Why AGPL v3:
✅ Anyone can use it free (open source)
✅ Anyone modifying it must contribute improvements back
✅ SaaS providers must open-source their version
✅ Prevents direct cloning and rebranding
✅ Community benefits from improvements
```

**Alternative**: Dual license (AGPL v3 + Commercial for proprietary use)
- If you want to sell closed-source variants
- Gives you revenue stream while keeping open version free

**Support tier**: Community (AGPL) or Commercial (premium SaaS)

---

### 2. 🔌 **Starline Weaver** (Multi-AI Message Bus)
**Location**: `src/crystal-core/bus/`  
**What it is**: Wire protocol, envelope schema, Belt-Three conduct rules enforced in code

**Strategic Value**: ⭐⭐⭐⭐ **HIGH**
- Protocol layer (network effect)
- Could become industry standard
- Interoperability is key value
- Hub agent (Clementine) is novel

**Current license**: Apache-2.0 (❌ Too permissive)

**Recommended license**: **AGPL v3**
```
Why AGPL v3:
✅ Protocol needs to remain open (network effects)
✅ But implementations using it must stay compatible
✅ Prevents proprietary forks that break the protocol
✅ Server/service using it must open-source customizations
```

**Specifications to open**: `STARLINE-WEAVE-PROTOCOL.md` (already exists)  
**Reference implementation**: AGPL v3

**Support tier**: Community (open protocol) + Consulting (enterprise deployment)

---

### 3. 🤝 **Consent Transport** (P2P Sovereign Memory)
**Location**: `src/crystal-core/consent_transport/`  
**What it is**: Peer-to-peer data exchange with Noise Protocol handshake, consent model

**Strategic Value**: ⭐⭐⭐⭐ **HIGH**
- Cryptographic primitive (difficult to reverse-engineer)
- Could become privacy standard
- Novel consent architecture
- Differentiator for sovereign computing

**Current license**: Apache-2.0 (❌ Too permissive)

**Recommended license**: **AGPL v3**
```
Why AGPL v3:
✅ Cryptographic protocols need open review
✅ Prevent proprietary "backdoor" variants
✅ Encourage peer implementations (more eyes on security)
✅ SaaS using it must open their code
```

**Specification**: Publicly available (enable security audits)  
**Implementation**: AGPL v3

**Support tier**: Community + Academic security research

---

### 4. 📖 **RDP** (Record Kernel & Explainable Decision Engine)
**Location**: `src/crystal-core/rdp/`  
**What it is**: Tamper-evident record journal, precedence tiers, explainable decisions

**Strategic Value**: ⭐⭐⭐ **MEDIUM-HIGH**
- Could be audit/compliance product
- Valuable for regulated industries
- Technical moat (decision hierarchy design)

**Current license**: Apache-2.0 (❌ Too permissive)

**Recommended license**: **AGPL v3**
```
Why AGPL v3:
✅ Audit trail integrity needs transparency
✅ Prevent proprietary "tamper" implementations
✅ Regulated industries need open specs
✅ Encourages adoption while protecting code
```

**Potential commercial use**: Licensing to financial/healthcare (audit compliance)

**Support tier**: Commercial (audit certification, compliance support)

---

### 5. 🔐 **CrystalBridge** (MCP Consent Gate)
**Location**: `src/crystalcore/`  
**What it is**: MCP server with fail-closed consent architecture, AI safety guard

**Strategic Value**: ⭐⭐⭐⭐⭐ **VERY HIGH**
- Novel AI safety mechanism
- Could prevent harmful outputs
- Unique consent model for AI
- Valuable IP for safety-conscious companies

**Current license**: Apache-2.0 (❌ Too permissive)

**Recommended license**: **PROPRIETARY** (with limited open-source components)
```
Why Proprietary:
✅ Consent gate logic is core safety IP
✅ Open-sourcing enables adversarial bypass
✅ Safety mechanism value is in trade-secret aspects
✅ Auditable but not modifiable (like security hardware)
```

**Model**: 
- Core consent gate: **Proprietary (closed-source)**
- MCP protocol adapter: **AGPL v3 (reference implementation)**
- Let customers audit, but not modify

**Licensing model**: Per-deployment or SaaS only

**Support tier**: Commercial only (premium pricing, direct support)

---

### 6. 🧠 **CrystalCore.OS EI** (Emotional Intelligence & Affective Computing)
**Location**: `src/crystalcore-os/`  
**What it is**: Emotion detection, active learning, Bayesian uncertainty, dbt warehouse

**Strategic Value**: ⭐⭐⭐⭐ **HIGH**
- Novel EI framework
- Multimodal emotion detection
- Active learning loop
- Commercial appeal (HR tech, customer service, healthcare)

**Current license**: Apache-2.0 (❌ Already being fixed with dual-license)

**Recommended license**: **DUAL LICENSE** ✅ (Already implemented)
- **Non-commercial**: MIT (free for research, education, open-source)
- **Commercial**: Paid license ($5K–$25K+/year)

**This is already done!** See `LICENSE.md` + `COMMERCIAL_LICENSE.md`

**Support tier**: Community (MIT) + Commercial (SaaS tiers)

---

### 7. 🎨 **Mythos** (Story, Art, Lore)
**Location**: `mythos/`  
**What it is**: Codex, Apocryphon, visual art, narrative canon

**Strategic Value**: ⭐⭐⭐ **BRAND/CULTURAL**
- Narrative differentiation
- Visual identity
- Fan engagement potential

**Current license**: CC BY-NC-ND 4.0 (✅ Good choice)
- Share with attribution
- No commercial use
- No derivatives

**Recommendation**: **Keep unchanged** (CC BY-NC-ND 4.0)

**Support tier**: Community + Fan ecosystem

---

## Summary Table

| Product | Package | Location | License | Commercial | Support |
|---------|---------|----------|---------|-----------|---------|
| **Clementine** | `@teraaustralis/clementine` | `packages/clementine/` | AGPL v3 | Optional (commercial variant) | Community + Commercial |
| **Starline Weaver** | `@teraaustralis/starline` | `packages/starline/` | AGPL v3 | Consulting/integration | Community + Consulting |
| **Consent Transport** | `@teraaustralis/consent` | `packages/consent-transport/` | AGPL v3 | Research licensing | Academic + Support |
| **RDP** | `@teraaustralis/rdp` | `packages/rdp/` | AGPL v3 | Audit/compliance licensing | Commercial (regulated industries) |
| **CrystalBridge** | `@teraaustralis/bridge` | `packages/crystalbridge/` | **PROPRIETARY** | SaaS/licensing | Commercial only |
| **CrystalCore.OS EI** | `@teraaustralis/ei` | `packages/crystalcore-ei/` | **Dual** (MIT + Commercial) | Paid tiers | Community + Commercial ✅ |
| **Mythos** | `@teraaustralis/mythos` | `mythos/` | CC BY-NC-ND | None | Community |

---

## Licensing Tiers & Pricing

### AGPL v3 Products (Clementine, Starline, Consent, RDP)
**Open source, free to use. Optional commercial support:**

| Tier | Cost | Support | Use Case |
|------|------|---------|----------|
| **Community** | Free | GitHub issues, community forum | Personal projects, research |
| **Startup** | $2,500/yr | Email support, bug reports | Early-stage companies |
| **Professional** | $10,000/yr | Slack + phone, SLA (24h response) | Production deployments |
| **Enterprise** | Custom | Direct engineering, custom integrations | Fortune 500, mission-critical |

### Dual License Products (CrystalCore.OS EI)
**MIT for non-commercial, Commercial licenses for paid use:**

| Tier | Cost | Users | Deployment | Support |
|------|------|-------|-----------|---------|
| **Open (MIT)** | Free | Unlimited | Any (non-commercial) | Community |
| **Startup** | $5,000/yr | 50K API calls/month | 1 | Email |
| **Professional** | $25,000/yr | 1M API calls/month | 3 | Slack + Phone |
| **Enterprise** | Custom | Unlimited | Unlimited | 24/7 SLA |

### Proprietary Products (CrystalBridge)
**Closed-source, commercial licensing only:**

| Model | Cost | Support |
|-------|------|---------|
| **SaaS (usage-based)** | $1,000–$50,000/mo | Included, direct support |
| **Per-deployment license** | $100,000–$1,000,000/yr | Included, direct support |
| **Enterprise agreement** | Custom | Custom SLA |

---

## Migration Path

### Phase 1: Prepare (Week 1)
- [ ] Create `packages/` directory structure
- [ ] Create individual LICENSE files per package
- [ ] Create `pyproject.toml` and `setup.py` for each package

### Phase 2: Restructure (Week 2-3)
- [ ] Move code into package directories
- [ ] Update internal imports (from `src.crystalcore` → `from teraaustralis.crystalcore`)
- [ ] Create `__init__.py` files with clean APIs
- [ ] Update main `README.md` to point to individual packages

### Phase 3: Package (Week 3-4)
- [ ] Publish to PyPI under `@teraaustralis` namespace
- [ ] Create GitHub organization repos (optional but recommended)
- [ ] Set up individual CI/CD per package

### Phase 4: Documentation (Ongoing)
- [ ] Create `LICENSING.md` per package
- [ ] Add license headers to source files
- [ ] Update contribution guidelines

---

## Revenue Model

### Open Source (AGPL v3)
- Free to use, modify, contribute
- Revenue from **services**:
  - Consulting (protocol integration, security review)
  - Support contracts (SLA, direct engineering)
  - Certifications (auditor training for RDP/audit)
  - Training (workshops, online courses)

### Dual License (EI)
- Free for non-commercial
- Revenue from **commercial licenses**:
  - SaaS platforms using EI
  - Enterprise deployments
  - Custom integrations

### Proprietary (CrystalBridge)
- Revenue from **usage** or **deployment licenses**
- High-value customers only
- Direct sales model

### Combined Strategy
**Est. Annual Revenue (realistic projections):**
- AGPL consulting: $100K–$500K
- Dual license (EI): $50K–$200K
- Proprietary (Bridge): $500K–$2M+
- **Total**: $650K–$2.7M/year at scale

---

## FAQ

**Q: Will AGPL v3 prevent commercial use?**  
A: No. Companies can use it commercially in-house. They must open-source **modifications** and **SaaS deployments**. Services (consulting, support) can be charged.

**Q: Can we change licenses later?**  
A: For AGPL/dual-license products: yes, but only for new versions (contributors own past code).  
For proprietary: you own it outright, can change anytime.

**Q: Won't AGPL scare away users?**  
A: Open-source projects using AGPL (WordPress, GitLab) have millions of users. Enterprise support makes it palatable for companies.

**Q: Should CrystalBridge really be proprietary?**  
A: If it's AI safety critical, yes. Adversaries will try to bypass it. Security-through-obscurity is inappropriate for crypto/protocols, but appropriate for safety gates.

**Q: What about contributor agreements?**  
A: For AGPL: Contributor License Agreement (CLA) needed to ensure you can relicense if needed.  
For proprietary: Assign copyright to your company.

---

## Next Steps

1. **Decide** on this strategy (or modify it)
2. **Commit** licensing decisions in writing
3. **Restructure** repo according to Phase 1-4
4. **Update** all LICENSE headers in source files
5. **Publish** to PyPI with separate package pages
6. **Set up** commercial licensing infrastructure (if needed)

---

*CrystalArchitect – Licensing Strategy for Sustainable Innovation*
