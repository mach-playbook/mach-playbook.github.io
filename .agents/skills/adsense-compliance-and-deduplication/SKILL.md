---
name: adsense-compliance-and-deduplication
description: Comprehensive workflow to verify, audit, and maintain Google AdSense policy compliance, crawler compatibility, and topic deduplication for mach-playbook.github.io.
---

# Google AdSense Compliance and Deduplication Workflow

Follow this procedure whenever auditing AdSense health, investigating rejection notices, or publishing new content to **MACH Playbook** (`mach-playbook.github.io`).

## Step 0: Mandatory Knowledge Directives

Before taking action, ALWAYS:
1. Consult the **LLM Wiki**: [`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md) and [`wiki/adsense-policy-and-compliance.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/adsense-policy-and-compliance.md).
2. Query the **codebase-memory-mcp** knowledge graph (`home-merolhack-fl-mach-playbook`) to inspect relationships between templates and scripts.

---

## Step 1: Script Loading Verification (No Lazy-Loading)

Verify that `_includes/head.html` includes the direct asynchronous tag:
```html
<!-- Google AdSense - Activated (Direct async load for crawler compatibility) -->
<meta name="google-adsense-account" content="ca-pub-2700240339792942">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2700240339792942" crossorigin="anonymous"></script>
```
> ⚠️ **STRICT PROHIBITION**: NEVER wrap `adsbygoogle.js` in user-interaction events (`scroll`, `click`, `touchstart`) or `setTimeout` delays. Google crawlers do not trigger these events and will flag the site as "Code missing".

---

## Step 2: Content Deduplication & Thin Content Check

1. Run the duplicate content validator:
   ```bash
   python3 scripts/check-duplicates.py
   ```
2. Verify that no posts share more than 45% keyword similarity or have repetitive slugs across consecutive days.
3. Confirm all articles exceed **1,000 words** with Senior Architect E-E-A-T depth.

---

## Step 3: Run Full AdSense Policy Test Suite

Execute the 13-point compliance suite:
```bash
python3 scripts/test-adsense-compliance.py
```
Ensure all 13 checks output `[PASS]`, including:
- `ads.txt` publisher ID verification.
- Direct async script loading test.
- No near-duplicate posts across dates test.

---

## Step 4: Generate WebP Companion Assets

Ensure all post images have both PNG and WebP formats:
```bash
python3 scripts/generate-webp-images.py
```

---

## Step 5: Test Build & Deploy

Validate HTML syntax with Docker HTML-Proofer:
```bash
docker build --target test -t mach-playbook:test .
```
After committing and pushing to `main`, check GitHub Actions (`gh run list`) to ensure `Build and Deploy` completes with `completed | success`.
