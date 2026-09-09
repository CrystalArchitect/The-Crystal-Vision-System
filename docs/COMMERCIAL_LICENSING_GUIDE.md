# Commercial Licensing Guide

> **Scope note.** This guide describes the `packages/` layout and its
> per-package licensing (AGPL v3 / Proprietary / dual). That model was
> **not adopted** — [`ADR-0010`](adr/ADR-0010.md) chose uniform
> CC BY-NC-ND 4.0 for the whole repository, and
> [`ADR-0013`](adr/ADR-0013.md) extended it across the portfolio. The
> `packages/` tree it refers to does not exist here. Kept for provenance;
> read it as history, not as instructions.

> **Status note (2026-07-23):** the per-package licensing tiers this guide
> describes were reverted by [`ADR-0010`](adr/ADR-0010.md) — the whole
> repository is uniformly CC BY-NC-ND 4.0. Kept for provenance. See
> [SystemMap: where the code actually lives](architecture/SystemMap.md#where-the-code-actually-lives).

This document outlines the commercial licensing strategies for TeraAustralis products and how to implement license verification in deployed systems.

## Product Licensing Summary

### Open Source (AGPL v3)

**Products:** Clementine, Starline Weaver, Consent Transport, RDP

- **Model:** Free for open-source / non-commercial use
- **Commercial SaaS:** License required ($2.5K–$10K+/year)
- **CLA:** Contributor License Agreement required for contributions
- **Revenue:** Support contracts, commercial SaaS licensing

**Licensing Contacts:**
- Clementine: clementine-commercial@teraaustralis.dev
- Starline: starline-support@teraaustralis.dev
- Consent: consent-commercial@teraaustralis.dev
- RDP: rdp-commercial@teraaustralis.dev

### Proprietary (CrystalBridge)

**Model:** Enterprise licensing only

- **SaaS Deployment:** $1,000–$50,000/month
  - Small deployments (< 10M tokens/month): $1K/month
  - Mid-market (10M–100M tokens/month): $5K–$15K/month
  - Enterprise (100M+ tokens/month): Custom pricing

- **On-Premises:** $100,000–$1,000,000+ one-time
  - Perpetual license
  - Source access (read-only)
  - Annual support contract

**Licensing Contacts:**
- Sales: crystalbridge-sales@teraaustralis.dev
- Evaluation: crystalbridge-eval@teraaustralis.dev
- Support: support.teraaustralis.dev

### Dual Licensing (CrystalCore-EI)

**Model:** MIT (non-commercial) + Commercial licensing

**Non-Commercial (MIT):**
- Free for research, personal, educational use
- Open-source modifications allowed
- No SaaS re-hosting

**Commercial Tiers:**

| Tier | Price | Calls/Month | Deployments | Use Case |
|------|-------|------------|-------------|----------|
| Startup | $5K/year | 50K | 1 | Early-stage companies |
| Professional | $25K/year | 1M | 3 | Growing SaaS products |
| Enterprise | Custom | Unlimited | Unlimited | Large-scale deployments |

**Commercial License Contacts:**
- Sales: ei-commercial@teraaustralis.dev
- Technical: ei-support@teraaustralis.dev

### Creative Commons (Mythos)

**Model:** CC-BY-NC-ND-4.0

- **Non-Commercial Use:** Free (with attribution)
- **Fan Works:** Encouraged and celebrated
- **Commercial Adaptations:** License required
- **Community:** Submissions to community@teraaustralis.dev

## Implementation: License Verification

### For AGPL v3 Products

**Approach:** Honor system + contact on commercial use

1. **Add License Check (Optional):**

```python
# In your deployment
import os
from datetime import datetime

def check_license_requirement():
    """Warn if using in production without commercial license."""
    if os.getenv("ENVIRONMENT") == "production":
        print(
            "⚠️  AGPL v3 Commercial Notice:\n"
            "If you are using this in a commercial SaaS product,\n"
            "you are required to have a commercial license.\n"
            "Contact: clementine-commercial@teraaustralis.dev"
        )
```

2. **Add License Reminder to README:**

```markdown
## Commercial Use

If you are using Clementine in a commercial SaaS product or service,
you are required to obtain a commercial license. The AGPL v3 license
permits commercial services but requires source code disclosure.

For commercial licensing: clementine-commercial@teraaustralis.dev
```

### For Proprietary (CrystalBridge)

**Approach:** License key + deployment verification

1. **License Key Format:**

```python
# License key structure: org-tier-expiry-hash
# Example: ACME-PROFESSIONAL-2026-08-15-abc123def456

import hashlib
from datetime import datetime

def verify_license(license_key: str) -> bool:
    """Verify CrystalBridge license key."""
    try:
        parts = license_key.split("-")
        if len(parts) != 5:
            return False
        
        org, tier, year, month, day, signature = (
            parts[0], parts[1], parts[2], parts[3], parts[4]
        )
        
        # Verify expiration date
        expiry = datetime(int(year), int(month), int(day))
        if datetime.now() > expiry:
            return False
        
        # Verify signature (simplified)
        # In production, use cryptographic verification
        expected_sig = hashlib.sha256(
            f"{org}-{tier}-{year}-{month}-{day}".encode()
        ).hexdigest()[:6]
        
        return signature == expected_sig
    except:
        return False
```

2. **Deployment Check:**

```python
# At startup
license_key = os.getenv("CRYSTALBRIDGE_LICENSE")
if not license_key or not verify_license(license_key):
    raise RuntimeError(
        "Invalid or missing CrystalBridge license. "
        "Contact crystalbridge-sales@teraaustralis.dev"
    )
```

### For Dual Licensing (CrystalCore-EI)

**Approach:** License tier detection + API quota enforcement

```python
from enum import Enum

class LicenseTier(Enum):
    FREE = "free"  # MIT non-commercial
    STARTUP = "startup"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class LicenseManager:
    def __init__(self, license_key: str = None):
        self.license_key = license_key
        self.tier = self._detect_tier(license_key)
        self.monthly_calls = self._get_monthly_quota()
        self.calls_used = 0
    
    def _detect_tier(self, license_key: str) -> LicenseTier:
        if not license_key:
            return LicenseTier.FREE
        
        # Parse license key to determine tier
        if "STARTUP" in license_key:
            return LicenseTier.STARTUP
        elif "PROFESSIONAL" in license_key:
            return LicenseTier.PROFESSIONAL
        elif "ENTERPRISE" in license_key:
            return LicenseTier.ENTERPRISE
        else:
            return LicenseTier.FREE
    
    def _get_monthly_quota(self) -> int:
        """Get monthly API call quota based on tier."""
        quotas = {
            LicenseTier.FREE: 0,  # Non-commercial only
            LicenseTier.STARTUP: 50_000,
            LicenseTier.PROFESSIONAL: 1_000_000,
            LicenseTier.ENTERPRISE: float('inf'),
        }
        return quotas[self.tier]
    
    def check_quota(self, num_calls: int = 1) -> bool:
        """Check if API calls are within quota."""
        if self.tier == LicenseTier.FREE:
            raise RuntimeError(
                "Commercial license required. "
                "Contact ei-commercial@teraaustralis.dev"
            )
        
        if self.calls_used + num_calls > self.monthly_calls:
            raise RuntimeError(
                f"API quota exceeded. "
                f"Used: {self.calls_used}/{self.monthly_calls}. "
                f"Upgrade at: ei-commercial@teraaustralis.dev"
            )
        
        self.calls_used += num_calls
        return True
```

## Revenue Model & Projections

### Year 1 Conservative Scenario

| Product | Licenses | Annual | Notes |
|---------|----------|--------|-------|
| Clementine | 5 × $5K | $25K | Early adoption |
| Starline | 3 × $7.5K | $22.5K | Technical teams |
| CrystalCore-EI | 1 × $25K + 2 × $5K | $35K | Dual licensing working |
| CrystalBridge | 1 × $50K/yr | $50K | Enterprise early access |
| **Total** | | **$132.5K** | Conservative |

### Year 3 Growth Scenario

| Product | Licenses | Annual | Notes |
|---------|----------|--------|-------|
| Clementine | 50 × $7.5K | $375K | Widespread adoption |
| Starline | 20 × $10K | $200K | Protocol standard |
| CrystalCore-EI | 5 × $25K + 15 × $5K | $200K | Scaling startups |
| CrystalBridge | 2 × $500K + 5 × $100K | $1.5M | Enterprise deployments |
| **Total** | | **$2.275M** | Growth achieved |

## Setting Up Payment Processing

### Stripe Integration

1. **Create products:**

```bash
stripe products create --name="Clementine Commercial License" --type=service
stripe price create --product=prod_xyz --currency=usd --unit_amount=500000 --recurring=[interval=month]
```

2. **Generate invoice templates:**

See `docs/governance/LICENSING-STRATEGY.md` for invoice templates and commercial terms.

## Compliance & Legal

### Required Notices

Every commercial deployment must include:

1. **License Attribution:**
   - Product name and version
   - License tier
   - Expiration date (if applicable)

2. **Commercial Terms:**
   - Link to commercial license agreement
   - Support SLA (if applicable)
   - Data processing terms (GDPR/CCPA)

3. **Open Source Compliance (AGPL v3):**
   - Source code availability link
   - License text in documentation
   - Contributor attribution

### Annual Audit Checklist

- [ ] Review all commercial licenses and expiration dates
- [ ] Reconcile revenue against license inventory
- [ ] Check AGPL compliance (source code disclosure)
- [ ] Audit deployments for unauthorized commercial use
- [ ] Update pricing based on market conditions
- [ ] Renew legal reviews

## Further Resources

- [The licence that actually governs this repository](../LICENSE) — CC BY-NC-ND 4.0
- [Commercial licensing terms](../COMMERCIAL_LICENSE.md)
- [Licensing Strategy](../docs/governance/LICENSING-STRATEGY.md)
- [Publishing Guide](./PUBLISHING.md)
