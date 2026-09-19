# Configuring GitHub Pages with a Custom Domain on GoDaddy

A step-by-step guide for pointing a GoDaddy-managed domain at a GitHub Pages site, written for `teraustralis.com.au` → the **TerAustralis-Incognita-Code** Pages deployment, but applicable to any domain. It covers both the `www` subdomain and the bare apex domain, plus HTTPS provisioning and verification.

---

## How the pieces fit together

GitHub Pages serves your site from GitHub's edge network. Your job at GoDaddy is purely DNS: tell the internet that requests for your domain should be routed to GitHub's servers. GitHub then matches the incoming hostname against the **custom domain** configured in your repository and serves the right site with an automatically provisioned Let's Encrypt certificate.

Two hostnames need to resolve correctly:

| Hostname | Record type | Points to | Why |
|----------|-------------|-----------|-----|
| `www.teraustralis.com.au` | CNAME | `crystalarchitect.github.io` | Subdomains use a CNAME to your GitHub Pages hostname |
| `teraustralis.com.au` (apex) | A ×4 | GitHub Pages anycast IPs | Apex domains cannot use CNAME; they need A records |

With both in place, GitHub automatically 301-redirects the apex to `www` (or vice versa, depending on which one is set as the custom domain in the repo).

---

## Part 1 — Configure DNS at GoDaddy

### Step 1: Open the DNS manager

1. Sign in at [godaddy.com](https://www.godaddy.com) and go to **My Products**.
2. Find `teraustralis.com.au` in your domain list and click **DNS** (or **Manage DNS** from the three-dot menu). You land on the **DNS Records** page for the domain.

> **Important:** If the domain's nameservers were changed away from GoDaddy's defaults (e.g. to AWS Route 53 — plausible given the current parking IPs are AWS addresses), GoDaddy's DNS records page will have no effect. Check the **Nameservers** section on the same page first: it should say "GoDaddy nameservers" or show entries like `ns**.domaincontrol.com`. If it shows other nameservers, either switch back to GoDaddy nameservers or make these same record changes at the provider those nameservers belong to.

### Step 2: Remove conflicting records

On the DNS Records page, delete anything that would collide with the new records:

- Any existing **A** records with Name `@` (the apex) — including the current parking records pointing at `15.197.225.128` and `3.33.251.168`.
- Any **AAAA** records with Name `@` (unless you re-add GitHub's IPv6 records in Step 4).
- Any **CNAME** record with Name `www` that points somewhere other than your GitHub Pages hostname.
- Any GoDaddy **Forwarding** rule on the domain (bottom of the DNS page) — domain forwarding and A records fight each other; use one, not both. For this setup, remove forwarding.

Leave **MX**, **TXT**, **SRV**, and other record types alone — they handle email and verification and are unaffected by where the website points.

### Step 3: Add the `www` CNAME record

Click **Add New Record** and enter:

| Field | Value |
|-------|-------|
| Type | CNAME |
| Name | `www` |
| Value | `crystalarchitect.github.io` |
| TTL | 1 Hour (default) |

Note the CNAME target is your **GitHub Pages hostname** (`<username-or-org>.github.io`), never the repository name and never `github.com`. Do not include `https://` or a trailing path.

### Step 4: Add the four apex A records

Add four separate A records, all with the same Name:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | `@` | `185.199.108.153` | 1 Hour |
| A | `@` | `185.199.109.153` | 1 Hour |
| A | `@` | `185.199.110.153` | 1 Hour |
| A | `@` | `185.199.111.153` | 1 Hour |

In GoDaddy, `@` means the bare domain. All four IPs are required — GitHub serves from all of them and uses the full set for load distribution and failover.

*Optional (IPv6):* add four AAAA records with Name `@` and values `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

### Step 5: Save and note the propagation window

GoDaddy applies changes within minutes, but resolvers elsewhere may cache the old records until the previous TTL expires — typically under an hour. Don't troubleshoot until at least an hour has passed.

---

## Part 2 — Configure the repository on GitHub

### Step 6: Set the custom domain

1. In the repository (**TerAustralis-Incognita-Code**), go to **Settings → Pages**.
2. Under **Custom domain**, the field should contain `www.teraustralis.com.au`. If it's empty, enter it and click **Save**.
3. GitHub runs a DNS check. Once the GoDaddy records propagate, it shows a green check: *"DNS check successful."*

Two notes specific to this repo:

- **Use the `www` form, not the apex.** GitHub recommends the `www` subdomain as the canonical custom domain; with the A records from Step 4 in place, the apex automatically 301-redirects to `www`. This is already how the repo is configured — don't change it.
- **The CNAME file is managed in the repo.** Saving a custom domain normally commits a `CNAME` file; this repo already ships one through its deploy workflow (`deploy.yml` builds from `vision/site/` and publishes via GitHub Actions). Avoid editing the domain in the Pages UI in a way that creates a competing CNAME commit — the workflow's copy is the source of truth.

### Step 7: Enforce HTTPS

Still in **Settings → Pages**:

1. Wait for the certificate. After the DNS check passes, GitHub requests a Let's Encrypt certificate covering both `www.teraustralis.com.au` and `teraustralis.com.au`. This usually takes a few minutes but can take up to 24 hours. The UI shows *"TLS certificate is being provisioned"* in the interim.
2. Once available, tick **Enforce HTTPS**. This makes GitHub 301-redirect all `http://` requests to `https://`.

If the checkbox stays greyed out for more than a day, remove the custom domain, save, re-add it, and save again — this re-triggers certificate provisioning.

---

## Part 3 — Verify end-to-end

Run these from any machine once propagation has had time to complete:

```bash
# 1. Apex resolves to GitHub's IPs (not the old parking IPs)
dig +short teraustralis.com.au
# expect: 185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153

# 2. www resolves via the CNAME chain
dig +short www.teraustralis.com.au
# expect: crystalarchitect.github.io. followed by GitHub IPs

# 3. Apex redirects to www with a valid certificate
curl -sI https://teraustralis.com.au
# expect: HTTP/2 301  +  location: https://www.teraustralis.com.au/

# 4. www serves the real site
curl -sI https://www.teraustralis.com.au
# expect: HTTP/2 200  +  server: GitHub.com

# 5. Strongest check — a route only the real build produces
curl -s -o /dev/null -w "%{http_code}\n" https://www.teraustralis.com.au/crystalcore-os
# expect: 200
```

Check 5 matters because GitHub's fallback failure mode (Jekyll rendering a README) also returns 200 at the root — only the genuine SvelteKit build serves `/crystalcore-os`.

---

## Troubleshooting quick reference

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| GoDaddy record changes have no effect | Nameservers point elsewhere (e.g. Route 53) | Change records at the actual DNS host, or repoint nameservers to GoDaddy |
| Apex still shows old parking page / 405 | DNS cache | Wait out the TTL; test with `dig @8.8.8.8 teraustralis.com.au` to bypass local cache |
| "Domain's DNS record could not be retrieved" in Pages settings | Records not yet propagated, or wrong Name/Value | Re-check Steps 3–4; retry the DNS check after 30–60 min |
| Certificate error on apex or www | Cert still provisioning | Wait up to 24 h; if stuck, remove and re-add the custom domain |
| `www` shows a GoDaddy parking page | Leftover forwarding rule or parked CNAME | Delete forwarding and re-check the `www` CNAME target |
| Site shows a rendered README instead of the real site | Pages source flipped to "Deploy from a branch" | Settings → Pages → Source: **GitHub Actions**; re-run the deploy workflow |
| Random other subdomain shows your site | Wildcard DNS record | Avoid `*` records; GitHub recommends domain verification (Settings → Pages → verified domains) to prevent takeovers |

---

## Summary checklist

- [ ] Confirm nameservers actually point at GoDaddy
- [ ] Delete apex parking A records and any forwarding rules
- [ ] Add CNAME: `www` → `crystalarchitect.github.io`
- [ ] Add four A records: `@` → `185.199.108.153` / `.109.153` / `.110.153` / `.111.153`
- [ ] Confirm custom domain `www.teraustralis.com.au` in Settings → Pages with green DNS check
- [ ] Enable **Enforce HTTPS** once the certificate is issued
- [ ] Run the five verification probes above
