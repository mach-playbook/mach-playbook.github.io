# Google AdSense Integration & Policy Compliance

## 1. Publisher Credentials & Core Configuration

- **AdSense Publisher ID**: `ca-pub-2700240339792942`
- **Customer ID**: `2700240339792942`
- **ads.txt Location**: Root directory (`/ads.txt`), served live at `https://mach-playbook.github.io/ads.txt`
  ```text
  google.com, pub-2700240339792942, DIRECT, f08c47fec0942fa0
  ```
- **AdSense Verification Meta Tag** (in `_includes/head.html`):
  ```html
  <meta name="google-adsense-account" content="ca-pub-2700240339792942">
  ```

---

## 2. Critical Script Loading Rule (Direct Async vs Lazy Loading)

> ⚠️ **CRITICAL ARCHITECTURAL DIRECTIVE**:
> **NEVER** wrap the Google AdSense script in a user interaction event listener (`scroll`, `touchstart`, `click`, `keydown`) or in a `setTimeout` / `requestIdleCallback`.

### The Crawler Gotcha & Postmortem
- **Issue**: Previously, to maximize mobile Lighthouse scores, an IIFE delayed loading `adsbygoogle.js` until user interaction or an 8-second timer elapsed.
- **Consequence**: Google AdSense verification bots and crawlers do not trigger user interactions and do not wait 8 seconds. Consequently, the automated crawler could not detect the script on the page and repeatedly flagged the site as **"Site not ready"** / **"Code missing"**.
- **Remediation**: The script MUST load immediately and asynchronously via the official tag in `_includes/head.html`:
  ```html
  <!-- Google AdSense - Activated (Direct async load for crawler compatibility) -->
  <meta name="google-adsense-account" content="ca-pub-2700240339792942">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2700240339792942" crossorigin="anonymous"></script>
  ```

---

## 3. Postmortem: Resolving the "Low-Value Content" Rejection

### Root Cause
1. The autonomous daily publishing workflow had a defective deduplication filter (`len(word) > 5`), causing all topics in the static matrix to be mistakenly marked as "covered".
2. The script fell back to a hardcoded string `Patrones Avanzados de Resiliencia y Consistencia en Arquitecturas MACH - Edición YYYYMMDD`.
3. Over 11 near-identical articles were generated on consecutive days with the same topic.
4. Google AdSense policy algorithms classify identical/repetitive automated topics as **"Thin / Low-value content"**.

### Remediation Executed on 2026-09-02
1. **Deletions**: Purged all 11 repetitive articles and their corresponding PNG/WebP assets.
2. **Additions**: Authored and published **12 completely unique, high-quality technical deep-dives** (>1,000 words each) spanning FinOps, Backstage Platform Engineering, GraphQL Federation, Multi-tenancy SaaS, Contract Testing with Pact, Istio Service Mesh, Database Sharding, API Rate Limiting, Feature Flags, OpenTelemetry, and Domain-Driven Design.
3. **Asset Generation**: Synthesized 100% unique PNG headers and WebP companion images for every new post.
4. **Script Hardening**: Rewrote `scripts/publish_daily_jekyll_post.py` with Jaccard similarity deduplication, a 100+ topic matrix, dynamic AI topic generation, and an algorithmic combinatorial fallback.
5. **Review Submitted**: Review successfully requested via the AdSense Console; status transitioned to **"Getting ready"**.

---

## 4. Automated Compliance Test Suite (`scripts/test-adsense-compliance.py`)

Run the automated test suite locally to verify 100% policy compliance before pushing changes:

```bash
python3 scripts/test-adsense-compliance.py
```

The script asserts 13 strict checks:
1. `ads.txt` present and contains valid Publisher ID.
2. `_includes/head.html` contains meta tag and Publisher ID.
3. Privacy policy (`_tabs/privacy.md`) contains explicit cookie/AdSense disclosures.
4. About page (`_tabs/about.md`) contains author E-E-A-T credentials.
5. Contact page (`_tabs/contact.md`) contains verified contact endpoints.
6. Terms of Service (`_tabs/terms.md`) contains legal disclaimers.
7. Post layout (`_layouts/post.html`) includes author bio box.
8. Non-thin content (>800 words on every post).
9. Explicit `lang` frontmatter on every post.
10. Explicit `categories` frontmatter on every post.
11. Explicit `tags` frontmatter on every post.
12. AdSense script loads with direct `<script async>` (failing if lazy loading or timeouts are detected).
13. No near-duplicate posts across different dates (failing if slug similarity indicates repetitive editions).
