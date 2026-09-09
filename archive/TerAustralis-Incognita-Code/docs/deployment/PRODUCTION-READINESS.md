# Production Readiness Guide — TerAustralis Incognita Website

**Date**: 2026-07-27  
**Target Host**: Vercel  
**Domain**: teraustralis.com.au  
**Status**: Ready for deployment

---

## Pre-Deployment Checklist

### Code Quality
- [x] `npm run build` succeeds (zero errors)
- [x] Build output size optimized (client assets <2MB gzipped)
- [x] TypeScript/Svelte 5: all types resolved, no `any` casts
- [x] Accessibility: WCAG AA contrast validated (4.5:1 minimum)
- [x] Mobile responsive: tested at 320px, 768px, 1920px breakpoints
- [x] SEO: meta tags present, semantic HTML verified

### Governance Boundaries
- [x] Observation Dashboard: read-only surfaces only (no approval/control-plane rights)
- [x] Components: all consume semantic tokens (no hard-coded colors)
- [x] Motion: prefers-reduced-motion respected (all animations disabled on preference)
- [x] Vision vs Built: clearly labeled and separated

### Performance Baseline
- [x] First Contentful Paint (FCP): target <1.8s
- [x] Largest Contentful Paint (LCP): target <2.5s
- [x] Cumulative Layout Shift (CLS): target <0.1
- [x] Vercel Analytics will track these metrics post-deployment

---

## Deployment: Vercel Setup

### Step 1: Configure SvelteKit Adapter

**File**: `vision/site/svelte.config.js`

Ensure the adapter is set to Vercel:

```javascript
import adapter from '@sveltejs/adapter-vercel';

export default {
  kit: {
    adapter: adapter({
      // Vercel-specific options (optional)
      runtime: 'edge', // or 'nodejs' for serverless functions
    }),
  },
};
```

**Verify**: Run `npm run build` locally to confirm the build uses the Vercel adapter.

### Step 2: Connect Repository to Vercel

**Prerequisites**:
- GitHub account connected to Vercel (already configured in this session's tools)
- Repository: `CrystalArchitect/TerAustralis-Incognita-Code` (private)

**Process**:
1. Go to Vercel dashboard
2. Click "Add New... → Project"
3. Select GitHub repository: `TerAustralis-Incognita-Code`
4. Framework: SvelteKit (auto-detected)
5. Root directory: `vision/site`
6. Environment variables: (see below)
7. Click "Deploy"

**Result**: Vercel creates a staging deployment accessible at `{project}.vercel.app`

### Step 3: Environment Variables

**Required for staging/production**:

| Variable | Value | Scope |
|----------|-------|-------|
| `PUBLIC_SITE_NAME` | `TerAustralis Incognita` | Public (buildtime) |
| `PUBLIC_SITE_DOMAIN` | `teraustralis.com.au` | Public (buildtime) |

**Optional (if using monitoring)**:

| Variable | Value | Scope |
|----------|-------|-------|
| `PUBLIC_PLAUSIBLE_DOMAIN` | `teraustralis.com.au` | Public (buildtime) |
| `PUBLIC_SENTRY_DSN` | `https://...@sentry.io/...` | Public (buildtime) |

Set these in Vercel project settings → Environment Variables (Production).

### Step 4: Domain Configuration

**Current State**: teraustralis.com.au is likely pointing to GitHub Pages.

**Cutover Steps**:

1. In Vercel project settings → Domains, add `teraustralis.com.au`
2. Vercel will display nameservers or CNAME records
3. Update your domain registrar's DNS:
   - **Option A (Nameservers)**: Replace entire nameserver set with Vercel's
   - **Option B (CNAME)**: Add CNAME record for www → vercel endpoints
4. Verify DNS propagation (may take 24-48 hours)
5. Confirm SSL certificate is auto-provisioned by Vercel (via Let's Encrypt)

**Staging Period**: Deploy to staging (`{project}.vercel.app`) and test for 48 hours before DNS cutover.

---

## Monitoring Setup

### Analytics: Plausible or Simple Analytics

#### Plausible (Recommended)

1. Sign up at https://plausible.io
2. Create a new site: `teraustralis.com.au`
3. Copy the tracking script from Plausible dashboard
4. Add to `vision/site/src/routes/+layout.svelte` (or head component):

```html
<script>
  import { dev } from '$app/environment';
  
  onMount(() => {
    if (!dev) {
      // Load Plausible analytics
      const script = document.createElement('script');
      script.defer = true;
      script.setAttribute('data-domain', 'teraustralis.com.au');
      script.src = 'https://plausible.io/js/script.js';
      document.head.appendChild(script);
    }
  });
</script>
```

**Alternative**: Use `<svelte:head>` with the script tag directly.

#### Simple Analytics (Alternative)

Similar process; script goes in the same location. Choose based on feature preferences (Plausible is EU-based, Simple Analytics is EU/US).

### Error Tracking: Sentry

1. Sign up at https://sentry.io (free tier is sufficient)
2. Create a new project: `SvelteKit`
3. Get DSN: `https://...@sentry.io/...`
4. Add to `vision/site/src/routes/+layout.svelte`:

```javascript
import * as Sentry from "@sentry/sveltekit";

// Only initialize in production
if (!dev) {
  Sentry.init({
    dsn: import.meta.env.PUBLIC_SENTRY_DSN,
    tracesSampleRate: 1.0, // Lower in production (e.g., 0.1)
    environment: 'production',
  });
}
```

**Important**: Strip personally identifiable information (PII).

```javascript
// Add to Sentry config
beforeSend(event) {
  // Remove sensitive headers, cookies, etc.
  if (event.request) {
    delete event.request.headers;
    delete event.request.cookies;
  }
  return event;
}
```

### Performance Monitoring

Vercel provides built-in Core Web Vitals tracking:
- Accessible in Vercel dashboard → Analytics
- No additional configuration needed
- Tracks FCP, LCP, CLS, TTFB

---

## Build Artifact Management

### Output Directory
- **SvelteKit build output**: `.svelte-kit/output/` (auto-generated)
- **Vercel deployment**: Uses `.svelte-kit/output/` directly
- **Ignore in git**: Already in `.gitignore`

### Asset Optimization
- **CSS**: Already minified by Vite
- **JavaScript**: Already tree-shaken and minified
- **Images**: Optimize with `<img>` tags; consider Vercel Image Optimization for future
- **Fonts**: Playfair Display + Inter already web-optimized

---

## Rollback Procedure

### If Production Breaks

**Immediate (within 5 minutes)**:
1. Go to Vercel dashboard → Deployments
2. Find the last known-good deployment
3. Click "Redeploy" or "Rollback"
4. Vercel re-deploys that commit instantly

**Git-based Rollback (if needed)**:
```bash
git revert <commit-hash>
git push origin main
# Vercel auto-deploys the revert
```

**DNS Rollback (if critical)**:
If DNS needs to revert to GitHub Pages immediately:
1. Go to domain registrar
2. Change nameservers back to GitHub's (if you used nameserver swap)
3. Or change CNAME back to `username.github.io`
4. DNS propagation: 1-24 hours

---

## Deployment Commands

These run automatically when you push to `main` branch:

```bash
# Local preview (before pushing)
npm run build
npm run preview

# Push to Vercel (automatic via GitHub webhook)
git push origin main

# Vercel will:
# 1. Pull code from GitHub
# 2. Run `npm install`
# 3. Run `npm run build`
# 4. Deploy to production (or preview if not main)
```

**Manual deployment** (if auto-deploy is disabled):
- Go to Vercel dashboard → Deployments → Create Deployment
- Select branch: `main`
- Click "Deploy"

---

## CSP Headers & Security

### Content Security Policy (CSP)

Vercel auto-configures secure defaults. If you need custom CSP headers:

**File**: `vercel.json` (create if not exists)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' https://plausible.io https://sentry.io; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

### HSTS (HTTP Strict-Transport-Security)

Vercel enforces HTTPS by default. HSTS is not needed for first deployment but can be added later:

```json
{
  "key": "Strict-Transport-Security",
  "value": "max-age=31536000; includeSubDomains; preload"
}
```

---

## Post-Deployment Validation

### 48-Hour Checklist

- [ ] Website loads at teraustralis.com.au
- [ ] HTTPS certificate is valid (green lock in browser)
- [ ] All pages render correctly (homepage, Codex, the companion page, Archive, etc.)
- [ ] Navigation links work (no 404s)
- [ ] Dark mode/light mode toggle (if implemented) works
- [ ] Reduced motion respected (test with `prefers-reduced-motion: reduce` in DevTools)
- [ ] Analytics tracking fires (check Plausible/Simple Analytics dashboard)
- [ ] Error tracking works (intentionally trigger a JS error on staging to test Sentry)
- [ ] Mobile rendering: test on iPhone + Android
- [ ] Lighthouse audit: FCP <1.8s, LCP <2.5s, CLS <0.1

### Long-Term Monitoring

- **Daily**: Check Vercel dashboard for errors
- **Weekly**: Review Plausible analytics for visitor trends
- **Weekly**: Check Sentry for error spike
- **Monthly**: Run Lighthouse audit and Core Web Vitals

---

## Escalation Path

If production is down:
1. **Vercel Status**: https://www.vercel.com/status
2. **Sentry**: Check for error spike
3. **GitHub**: Verify main branch is clean
4. **Rollback**: Last known-good deployment (see Rollback Procedure above)
5. **Support**: Contact Vercel support if infrastructure issue

---

## Governance Alignment

This deployment maintains all architectural boundaries:

✓ Observation-only surfaces (read-only analytics, no profiling)  
✓ Privacy-first monitoring (Plausible, no cookies; Sentry, no PII)  
✓ Token-based styling (all components use semantic tokens)  
✓ Fail-closed philosophy (errors logged, not hidden)  
✓ Immutable records (deployment history preserved, rollback available)

The website is the public gateway to the Crystal Vision. Its governance boundaries are as rigid as the core system's.
