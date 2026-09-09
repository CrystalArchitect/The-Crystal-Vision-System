# CrystalCore.OS Dual-Licensing Model

**Protecting Innovation While Enabling Community**

> **Superseded — not the project's license.** This document proposed a
> dual-license model for one package (CrystalCore-EI). The maintainer
> decided against differentiated per-package licensing entirely: the whole
> repository, `packages/` included, is uniformly CC BY-NC-ND 4.0 — see
> [`ADR-0010`](docs/adr/ADR-0010.md). Kept for provenance, not in effect.

---

## Overview

CrystalCore.OS uses a **dual-licensing** model:

1. **MIT License** – Non-commercial use (free, open source)
2. **Commercial License** – Commercial use (paid subscription)

This allows academics, researchers, and hobbyists to use CrystalCore.OS freely, while commercial users support ongoing development.

---

## Choosing Your License

### 🎓 Use the MIT License If You:

- Building personal projects or prototypes
- Conducting academic research or education
- Contributing to open source (non-profit)
- Working at a non-profit organization
- Learning and experimenting
- Publishing research papers
- Creating educational content

✅ **MIT License is free** – No payment required  
📝 **Simple compliance** – Just include copyright notice  

**Example**: University researchers using CrystalCore.OS to study emotion recognition.

---

### 💼 Use the Commercial License If You:

- Building products that generate revenue
- Offering SaaS or cloud services
- Providing consulting or professional services using the code
- Integrating into enterprise software
- Reselling or sublicensing capabilities
- Using in any commercial context

💰 **Commercial License is paid** – Annual subscription  
🤝 **Includes support** – Priority support and updates  

**Example**: AI startup embedding CrystalCore.OS in emotion detection SaaS.

---

## Quick Decision Tree

```
Does your use generate revenue or profit?
├─ YES → Use COMMERCIAL_LICENSE.md
│        (Contact licensing for pricing)
└─ NO → Does your use involve:
        ├─ Academic research? → MIT License ✅
        ├─ Personal project? → MIT License ✅
        ├─ Open source contribution (non-commercial)? → MIT License ✅
        ├─ Educational use? → MIT License ✅
        └─ Non-profit work? → MIT License ✅
```

---

## License Comparison

| Aspect | MIT License | Commercial License |
|--------|------------|-------------------|
| **Cost** | Free | $5K–$25K+/year |
| **Commercial Use** | ❌ Not allowed | ✅ Allowed |
| **Modifications** | ✅ Allowed | ✅ Allowed |
| **Distribution** | Open source only | Proprietary + open |
| **Sublicensing** | ❌ No | ✅ Yes (restricted) |
| **Support** | Community | Priority SLA |
| **Attribution** | ✅ Required | ✅ Required |
| **Warranty** | None | Limited |
| **IP Ownership** | You own derivatives | CrystalArchitect retains core |

---

## Common Scenarios

### Scenario 1: University Researcher
**Use case**: Using CrystalCore.OS to publish a paper on emotion detection

→ **Use MIT License**
- Non-commercial academic use
- Cite CrystalCore.OS in publications
- Can share code with other researchers
- ✅ Free, no license required

---

### Scenario 2: AI Startup
**Use case**: Building a commercial emotion detection API service

→ **Use Commercial License**
- SaaS product = commercial use
- Need paid commercial license
- Can customize and extend
- Includes support and updates
- 💰 Contact licensing for pricing

---

### Scenario 3: Student Project
**Use case**: Building a chatbot with emotion awareness for class

→ **Use MIT License**
- Educational, non-commercial
- Can share code on GitHub (with MIT license)
- Can submit as coursework
- ✅ Free

---

### Scenario 4: Consulting Firm
**Use case**: Using CrystalCore.OS in consulting deliverables for paying clients

→ **Use Commercial License**
- Consulting services = commercial context
- Need commercial license for each client engagement
- Can bill clients for CrystalCore.OS integration
- 💰 Requires paid license

---

### Scenario 5: Corporate Internal Tool
**Use case**: Large company building internal HR analytics with emotion insights

→ **Use Commercial License**
- Commercial entity using commercial software
- Internal corporate use = commercial license
- No revenue generated from the tool itself, but company is commercial
- 💰 Requires commercial license (enterprise tier)

---

## Getting a Commercial License

### Steps:

1. **Review** `COMMERCIAL_LICENSE.md` for terms
2. **Determine** your volume tier:
   - Startup: 50K API calls/month ($5K/year)
   - Professional: 1M API calls/month ($25K/year)
   - Enterprise: Unlimited (custom pricing)
3. **Contact**:
   - 📧 licensing@crystalarchitect.dev
   - 🌐 www.crystalarchitect.dev/licensing
4. **Sign** license agreement
5. **Integrate** with payment processing (if SaaS)
6. **Receive** commercial license key + support access

### Pricing Includes:

✅ Full use of CrystalCore.OS  
✅ Source code access  
✅ Priority support (email/Slack/phone)  
✅ Bug fixes and security patches  
✅ Quarterly updates  
✅ SLA guarantees (Professional+)  

---

## Compliance Checklist

### If Using MIT License:

- [ ] Include full MIT license text in your project
- [ ] Keep copyright notice: `(c) 2026 CrystalArchitect`
- [ ] Do not use in commercial context
- [ ] Share modifications (recommended)
- [ ] Attribute CrystalCore.OS in documentation

### If Using Commercial License:

- [ ] Sign commercial license agreement
- [ ] Pay annual license fee
- [ ] Include attribution in product docs/UI
- [ ] Comply with sublicensing restrictions
- [ ] Notify end customers they cannot use independently
- [ ] Maintain records of deployment locations
- [ ] Pay for additional deployments if needed

---

## Gray Areas & Clarifications

**Q: I'm a student using this for a capstone project. Can I use MIT?**  
A: Yes, educational use is non-commercial. Use MIT license.

**Q: My company will evaluate this internally. Do I need a commercial license?**  
A: Not for evaluation. Commercial license required only when deploying to production or using in revenue-generating products.

**Q: I'm using CrystalCore.OS in a free open source project, but my company is commercial.**  
A: Use MIT license if the project itself is non-commercial. Company status doesn't matter—the *use* determines the license.

**Q: Can I use MIT license and charge for support/consulting around it?**  
A: The code must be MIT (free), but you can charge for services. However, if you're embedding it in a commercial product, use commercial license.

**Q: I want to publish modified CrystalCore.OS on PyPI. Which license?**  
A: If free/open source (non-commercial) → MIT. If paid package/service → Commercial.

**Q: What if I don't want to buy a commercial license but also don't want to open-source?**  
A: We may offer custom agreements. Contact licensing@crystalarchitect.dev.

---

## Contributing & Improvements

We welcome contributions! 

- **MIT users**: Submit pull requests to improve CrystalCore.OS
- **Commercial licensees**: Priority review for contributions
- **CLA required**: Sign contributor license agreement
- **Attribution**: Your contributions will be credited

---

## Support & Questions

- **Licensing questions**: licensing@crystalarchitect.dev
- **Technical support (MIT)**: GitHub issues, community forums
- **Technical support (Commercial)**: Priority Slack/email/phone
- **Custom arrangements**: Contact licensing team

---

## TL;DR

| Your Use | License | Cost |
|----------|---------|------|
| Personal, research, learning, open source | MIT | Free |
| Revenue-generating, SaaS, consulting, enterprise | Commercial | $5K–$25K+/year |

**When in doubt, ask**: licensing@crystalarchitect.dev

---

*CrystalCore.OS – Emotional Intelligence & Affective Computing System*  
*Supporting innovation, research, and sustainable business models*
