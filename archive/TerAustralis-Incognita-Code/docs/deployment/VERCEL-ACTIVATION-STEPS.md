# Vercel Activation Steps — Concrete Deployment Procedure

**Status**: EXECUTABLE CHECKLIST  
**Date**: 2026-07-27  
**Target**: Activate criterion 1 (live at teraustralis.com.au via Vercel)  
**Dependency**: Vercel team "TerAustralis Incognita" exists (verified: team_f1hq365mhrEb4hQmYBOABHWD)

---

## Phase 1: Create Vercel Project (5 minutes)

### Step 1.1: Log into Vercel Dashboard
- URL: https://vercel.com/dashboard
- Team selector: Select "TerAustralis Incognita" (not Personal account)

### Step 1.2: Create New Project
- Click "Add New → Project"
- Search for repository: `TerAustralis-Incognita-Code`
- Select it (private repo; GitHub auth required)

### Step 1.3: Configure Project
**Framework**: SvelteKit (auto-detected)  
**Root Directory**: `vision/site`  
**Build Command**: `npm run build` (pre-filled)  
**Output Directory**: `.svelte-kit/output` (auto-filled)  

**Environment Variables** (add these):
```
PUBLIC_SITE_NAME = TerAustralis Incognita
PUBLIC_SITE_DOMAIN = teraustralis.com.au
```

**Click**: "Deploy"

**Result**: Vercel begins first build. You'll receive a deployment URL (e.g., `ter-australis-incognita.vercel.app`).

---

## Phase 2: Verify Staging Deployment (10 minutes)

### Step 2.1: Wait for Build
- Vercel dashboard shows build progress
- Expected time: 2–4 minutes
- Status should change to "Ready"

### Step 2.2: Test Staging URL
- Open `ter-australis-incognita.vercel.app` in browser
- Verify:
  - [ ] Homepage loads
  - [ ] Navigation works (all links clickable)
  - [ ] Dark theme applied
  - [ ] No 404 errors in console
  - [ ] Images/assets load
  - [ ] Constellation component renders
  - [ ] Mobile responsive (test at 375px width)

### Step 2.3: Run Lighthouse Audit
- In Chrome DevTools → Lighthouse
- Run "Performance" audit on staging
- Verify:
  - [ ] FCP (First Contentful Paint): <1.8s
  - [ ] LCP (Largest Contentful Paint): <2.5s
  - [ ] CLS (Cumulative Layout Shift): <0.1
  - [ ] Accessibility score: >90

### Step 2.4: Test Reduced Motion
- DevTools → Rendering → Emulate CSS media feature `prefers-reduced-motion: reduce`
- Verify:
  - [ ] All animations stop (no orbit-drift, no ui-breathe)
  - [ ] Page still renders correctly
  - [ ] Content is readable

**If any failures**: Vercel provides detailed logs. Check "Deployments → [latest] → Logs" for errors.

---

## Phase 3: Integrate Monitoring (Optional, but Recommended)

### Step 3.1: Set Up Plausible Analytics

**Create account**:
1. Go to https://plausible.io
2. Sign up (free tier sufficient)
3. Create new site: `teraustralis.com.au`
4. Copy the tracking script (provided by Plausible)

**Add to codebase**:
- File: `vision/site/src/routes/+layout.svelte`
- Locate the `<script>` block at the top
- Add this after the existing imports:

```javascript
import { dev } from '$app/environment';

// Analytics (only in production)
if (!dev && typeof window !== 'undefined') {
  const script = document.createElement('script');
  script.defer = true;
  script.setAttribute('data-domain', 'teraustralis.com.au');
  script.src = 'https://plausible.io/js/script.js';
  document.head.appendChild(script);
}
```

**Commit**:
```bash
git add vision/site/src/routes/+layout.svelte
git commit -m "Add Plausible analytics tracking"
git push origin main
```

**Vercel redeploys automatically**. Wait 2 minutes, then verify Plausible dashboard shows traffic.

### Step 3.2: Set Up Sentry Error Tracking

**Create account**:
1. Go to https://sentry.io
2. Sign up (free tier)
3. Create new project: "SvelteKit"
4. Get DSN (looks like `https://...@sentry.io/...`)

**Add environment variable to Vercel**:
- Vercel dashboard → Project → Settings → Environment Variables
- Add: `PUBLIC_SENTRY_DSN = [your-dsn-here]`
- Save

**Add to codebase**:
- Install Sentry: `npm install @sentry/sveltekit @sentry/tracing`
- File: `vision/site/src/routes/+layout.svelte`
- Add after Plausible block:

```javascript
// Error tracking (only in production)
if (!dev && import.meta.env.PUBLIC_SENTRY_DSN) {
  import('@sentry/sveltekit').then(({ init }) => {
    init({
      dsn: import.meta.env.PUBLIC_SENTRY_DSN,
      tracesSampleRate: 0.1,
      environment: 'production',
    });
  });
}
```

**Commit and push**:
```bash
git add vision/site/src/routes/+layout.svelte package.json package-lock.json
git commit -m "Add Sentry error tracking"
git push origin main
```

**Vercel redeploys**. Test by intentionally triggering a JS error in staging; verify it appears in Sentry dashboard within 1 minute.

---

## Phase 4: Assign Domain (DNS Cutover)

### Step 4.1: Add Domain to Vercel

**In Vercel dashboard**:
- Project → Settings → Domains
- Click "Add Domain"
- Enter: `teraustralis.com.au`
- Vercel displays configuration options

**Two paths**:

#### Option A: Nameserver Transfer (Recommended)
1. Vercel shows 4 nameservers (e.g., `ns1.vercel.com`, etc.)
2. Go to your domain registrar (wherever you registered teraustralis.com.au)
3. Update nameservers to Vercel's (replaces current nameservers entirely)
4. Wait 24–48 hours for DNS propagation
5. Vercel auto-provisions SSL certificate (via Let's Encrypt)

#### Option B: CNAME Record (If registrar won't allow full nameserver swap)
1. Vercel shows CNAME target (e.g., `cname.vercel-dns.com`)
2. In registrar, add CNAME record:
   - Host: `www`
   - Target: `cname.vercel-dns.com`
3. Wait 24 hours for propagation
4. SSL certificate auto-provisions

### Step 4.2: Verify DNS Propagation

**Check DNS**:
```bash
# In terminal, run:
nslookup teraustralis.com.au
# or
dig teraustralis.com.au

# Should resolve to Vercel IPs (e.g., 76.76.19.89)
```

**Or use online tool**:
- https://mxtoolbox.com/nslookup.aspx
- Enter: `teraustralis.com.au`
- Verify it resolves to Vercel

### Step 4.3: Verify HTTPS Certificate

- Visit https://teraustralis.com.au (note: HTTPS, not HTTP)
- Browser shows green lock 🔒
- Click lock → Certificate → Verify "Let's Encrypt" is issuer
- Expiration should be ~90 days out

---

## Phase 5: Final Verification (Post-Cutover)

### Step 5.1: Test Production Domain

**In browser**:
- [ ] Open https://www.teraustralis.com.au
- [ ] Verify homepage loads (same as staging)
- [ ] Test all navigation links
- [ ] Verify analytics fires (check Plausible dashboard for new session)
- [ ] Run Lighthouse again (should match staging scores)

### Step 5.2: Verify SSL/Security Headers

**In browser DevTools → Network tab**:
- Reload page
- Click any request
- Headers → Response Headers
- Verify:
  - [ ] `Strict-Transport-Security` present (HSTS)
  - [ ] `X-Content-Type-Options: nosniff` present
  - [ ] `X-Frame-Options: DENY` present

### Step 5.3: Confirm Monitoring

**Plausible**:
- Visit Plausible dashboard
- Verify "teraustralis.com.au" is listed
- Check "Visitors" graph shows traffic from production domain

**Sentry**:
- Visit Sentry dashboard
- Check "Releases" shows deployment from main branch
- (No errors expected yet unless there are bugs)

---

## Phase 6: Update Success Criteria Verification

| Criterion | Before | After | Status |
|-----------|--------|-------|--------|
| 1. Live at teraustralis.com.au via Vercel | ✗ | ✓ | **PASS** |
| 2. PR #11 merged | ✓ | ✓ | **PASS** |
| 3. Version/Migration Key locked | ✓ | ✓ | **PASS** |
| 4. Monitoring active (Plausible + Sentry) | ✗ | ✓ | **PASS** |
| 5. Governance boundaries preserved | ✓ | ✓ | **PASS** |
| **Overall** | **2/5** | **5/5** | **RELEASE GATE: OPEN ✓** |

---

## Rollback Procedure (If Needed)

If something breaks after DNS cutover:

### Quick Rollback (within 24 hours)
1. **Option A**: Revert DNS to previous host (if known)
   - Go to registrar
   - Change nameservers back to GitHub Pages or previous host
   - Wait 1-2 hours for propagation
   
2. **Option B**: Revert Vercel deployment
   - Vercel dashboard → Deployments
   - Find last known-good deployment
   - Click "Redeploy"
   - Vercel reinstates that version instantly

### Persistent Rollback
```bash
git revert <commit-hash>
git push origin main
# Vercel auto-deploys the revert within 2 minutes
```

---

## Troubleshooting

### Build fails on Vercel
- Check Vercel dashboard → Logs
- Common causes: Missing environment variables, Node version mismatch
- Solution: Ensure `PUBLIC_*` variables are set, Node 18+ is selected

### Domain not resolving after 48 hours
- Check registrar's DNS settings (often propagation takes full 48h)
- Use `dig` or online tool to verify Vercel nameservers are active
- If stuck: Contact Vercel support (vercel.com/support)

### HTTPS certificate not auto-provisioning
- Wait 30 minutes (Let's Encrypt takes time)
- If still no certificate: Check domain is correctly configured in Vercel
- Restart: Remove domain, re-add, wait 30 min

### Analytics not firing
- Check Plausible dashboard → Domains → teraustralis.com.au
- Verify script is in +layout.svelte (View Page Source in browser)
- Clear browser cache, hard refresh (Ctrl+Shift+R)
- Check for CSP violations in browser console

---

## Governance Checkpoint

After deployment, verify:
- ✓ No hard-coded colors in CSS (all via var())
- ✓ All animations respect prefers-reduced-motion
- ✓ Analytics is observation-only (Plausible tracks no personal data)
- ✓ Sentry is configured to exclude PII
- ✓ No control-plane features on observation surfaces

All checks should pass given the design-locked implementation.

---

## Timeline Estimate

| Phase | Duration | Cumulative |
|-------|----------|-----------|
| Create Vercel project | 5 min | 5 min |
| Verify staging | 10 min | 15 min |
| Integrate monitoring | 15 min | 30 min |
| DNS cutover | 5 min (+ 24-48h propagation) | 35 min + wait |
| Final verification | 10 min | 45 min + wait |

**Total active work**: ~45 minutes  
**Total time to live**: 45 minutes + 24-48 hours (DNS propagation)

---

**Ready to execute. All steps are concrete and testable.**
