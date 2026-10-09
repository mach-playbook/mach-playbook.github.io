# MACH Playbook Wiki Chronological Audit Log

> Append-only changelog and knowledge ingestion ledger following the [Karpathy LLM Wiki Architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).  
> Parseable via standard Unix commands: `grep "^## \[" wiki/log.md`

---

## [2026-10-09] feat | Multi-Platform Content Syndication & Social Amplification (DEV.to, Medium, LinkedIn, X & Buffer)

- **Impacted Files**: `scripts/publish_to_devto.py`, `.devto_synced.json`, `.github/workflows/daily-blog-post.yml`, `wiki/content-syndication-and-distribution.md`, `wiki/publishing-pipeline-and-deduplication.md`, `wiki/index.md`, `wiki/log.md`
- **Summary**:
  - Implemented automated syndication engine (`scripts/publish_to_devto.py`) interfacing with DEV.to REST API:
    - 100% SEO Canonical Protection (`canonical_url` targeting `https://mach-playbook.github.io/posts/{slug}/`).
    - DEV.to frontmatter tag sanitization (maximum 4 alphanumeric tags).
    - Rate limit resilience handling HTTP 429 backoff (sleep 32s) and 3.0s interval throttling.
  - Executed 100% complete historical backfill: all 117 articles in `_posts/` published and recorded in `.devto_synced.json`.
  - Integrated automated syndication into GitHub Actions daily publisher (`.github/workflows/daily-blog-post.yml`) conditioned on repository secret `DEVTO_API_KEY`.
  - Evaluated community Squad on daily.dev (`https://daily.dev/squads/machplaybook`), resolving RSS reputation gate by enabling direct Squad content distribution.
  - Investigated Hashnode API and bulk import: discovered GraphQL deprecation and Pro paywall restriction; made architectural decision to avoid paid tiers ($0 budget rule).
  - Executed Medium web import (`medium.com/p/import`), verified canonical attribution, assigned 5 architectural tags, and published live post.
  - Executed and validated cross-platform social amplification on LinkedIn (offsite share intent with card metadata) and X (Twitter intent with character budget optimization) on `@merolhack`.
  - Documented Buffer middleware architecture (`publish.buffer.com`) connecting blog RSS feed (`feed.xml`) to LinkedIn and X channels with anti-spam rate governance.
  - Authored comprehensive modular wiki topic `wiki/content-syndication-and-distribution.md` and updated `wiki/index.md`.


---

## [2026-10-08] audit+feat | AdSense Policy Remediation: Rate-Limit Postmortem, E-E-A-T Transparency & Interactive Architecture Tools Hub


- **Impacted Files**: `_tabs/tools.md`, `_tabs/about.md`, `_tabs/glossary.md`, `_tabs/contact.md`, `_tabs/privacy.md`, `_tabs/terms.md`, `_data/locales/es.yml`, `_data/locales/en.yml`, `_data/locales/es-ES.yml`, `scripts/test-adsense-compliance.py`, `wiki/adsense-policy-and-compliance.md`
- **Summary**:
  - Investigated official Google AdSense review attempt status for `mach-playbook.github.io` (`ca-pub-2700240339792942`): identified attempt limit rate-lock with cooldown until **October 14, 2026**.
  - Conducted root cause postmortem on recurring "Low value content" violation: lack of organic traffic signals, static-only nature vs need for interactive tools/services, scaled publishing patterns, and `.github.io` subdomain scrutiny.
  - Built and deployed interactive engineering tools hub (`_tabs/tools.md`):
    1. **MACH Architecture Maturity Evaluator**: Quantitative 7-dimension audit (0-100 Pts), animated progress metrics, per-pillar scoring (M, A, C, H), customized technical roadmaps, and 1-click clipboard export.
    2. **TCO, Latency & Scale Simulator**: Real-time slider calculations for RPS, domain counts, and release velocity comparing Monolith vs Enterprise MACH vs Serverless Headless.
  - Reinforced E-E-A-T in `_tabs/about.md`: explicit testing lab methodology, peer review declarations, and empirical benchmark validation.
  - Upgraded AdSense test suite (`scripts/test-adsense-compliance.py`) with Test 11 for interactive utility assertions (100% PASS).
  - Validated full Docker build and HTML-Proofer across 365 files and 1,542 internal links with 0 errors.

---

## [2026-09-02] audit | Initial Google AdSense Compliance Analysis

- **Impacted Files**: `wiki/sources/You need to fix some issues before your site is ready for AdSense.eml`
- **Summary**:
  - Received official AdSense notification regarding "Low-value content" / site readiness requirements.
  - Preserved raw `.eml` email file in `wiki/sources/` as immutable diagnostic baseline.
  - Initiated audit of thin content, missing taxonomy, and template script delivery.

---

## [2026-09-17] audit | Google AdSense Review Submission & Head Script Async Integration

- **Impacted Files**: `_includes/head.html`, `ads.txt`, `wiki/adsense-policy-and-compliance.md`
- **Summary**:
  - Verified site ownership and requested official review on Publisher ID `ca-pub-2700240339792942`.
  - Discovered root cause of initial rejection: AdSense crawler failed to detect the script tag because it was injected via deferred/lazy wrappers.
  - Implemented direct, asynchronous `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2700240339792942" crossorigin="anonymous"></script>` directly inside `<head>`.
  - Authored automated compliance validation test suite (`scripts/test-adsense-compliance.py`).

---

## [2026-09-23] feat | Autonomous Daily Content Publishing Pipeline Engine

- **Impacted Files**: `scripts/publish_daily_jekyll_post.py`, `wiki/publishing-pipeline-and-deduplication.md`, `wiki/content-and-editorial-standards.md`
- **Summary**:
  - Engineered autonomous daily content publisher driven by Google Gemini API.
  - Implemented 5-pillar MACH matrix (100+ topics) with dynamic fallback algorithmic generator.
  - Integrated Jaccard similarity deduplication engine preventing overlapping content.
  - Integrated Pillow automated companion WebP banner generator for responsive Chirpy themes.

---

## [2026-09-28] perf | Core Web Vitals Optimization & Mobile Zero-CLS Lockdown

- **Impacted Files**: `_includes/head.html`, `_config.yml`, `wiki/architecture.md`
- **Summary**:
  - Achieved Mobile Lighthouse score of 91/100 Performance, 100/100 Accessibility, 100/100 Best Practices, and 100/100 SEO.
  - Eliminated layout reflows, dropping Cumulative Layout Shift (CLS) from 0.275 to 0.000.
  - Inlined critical layout locks in `<head>` for sidebar, dropdowns, and search modals.
  - Converted Mermaid.js to on-demand loading driven by post frontmatter `mermaid: true`.

---

## [2026-10-02] feat | UX: Hybrid In-Article TOC, 2-Column Category Masonry, and Expanded Glossary

- **Impacted Files**: `_includes/head.html`, `_includes/post-bottom-widgets.html`, `_layouts/categories.html`, `_layouts/default.html`, `_layouts/post.html`, `_tabs/glossary.md`
- **Summary**:
  - Implemented dual Hybrid Table of Contents (TOC): in-article navigation widget synchronized with desktop floating sidebar TOC (`#toc-wrapper`), with smooth scroll offset `scroll-margin-top: 5rem`.
  - Engineered 2-column masonry layout for Categories (`/categories/`) using CSS columns (`column-count: 2`, `break-inside: avoid`), eliminating dead white space while cleanly collapsing to 1 column on mobile.
  - Expanded technical glossary (`/glossary/`) with 30+ bilingual MACH, composable commerce, and microservices definitions with letter navigation jump links.
  - Applied dark-mode CSS overrides for Mermaid diagrams, forcing transparent background and `#f8fafc` text contrast.

---

## [2026-10-02] fix | UI: Post Hero Image 100% Width Expansion & 41.6% Constraint Postmortem

- **Impacted Files**: `_includes/head.html`, `_layouts/post.html`
- **Summary**:
  - Identified layout issue where post hero images rendered at less than 50% width inside their container.
  - Root cause postmortem: Bootstrap's `.col-md-5` (41.66666667%) rule on home post cards was mistakenly applied as a global rule `@media (min-width: 768px) { #post-list .preview-img, .post-preview .preview-img, .card-wrapper .preview-img { width: 41.66666667% !important; } }`. On home cards, this caused double-shrinking (41.6% of 41.6% = 17%), while on post pages it constrained `.preview-img` to 41.6%.
  - Removed rogue 41.6% rule from `_includes/head.html`.
  - Added `.post-hero-image-wrapper` with `width: 100% !important; max-width: 100% !important;` and fixed `aspect-ratio: 1200 / 630` for Zero-CLS stability.
  - Configured `.preview-img { width: 100% !important; height: 100% !important; object-fit: cover; }` so images properly occupy 100% of their intended card or hero container.

---

## [2026-10-03] test | CI: Automated Testing Architecture (Unit, BDD, Headless E2E Browser Testing)

- **Impacted Files**: `scripts/test-ui-components.py`, `scripts/test-bdd-specs.py`, `scripts/test-e2e-browser.py`, `tools/test.sh`, `Dockerfile`, `.github/workflows/pages-deploy.yml`
- **Summary**:
  - Built comprehensive 3-tier automated testing framework to prevent regressions and eliminate manual verification:
    1. **Tier 1 (Unit & Component)**: `test-ui-components.py` parses Jekyll layouts, includes, and CSS to assert DOM structure, aspect ratios, and absence of deprecated constraints.
    2. **Tier 2 (BDD Specifications)**: `test-bdd-specs.py` executes 19 Given-When-Then behavioral specifications across Home, Post Hero, Categories, Glossary, Contact, and Mobile viewports.
    3. **Tier 3 (Headless E2E Browser Testing)**: `test-e2e-browser.py` drives Headless Chrome via raw Chrome DevTools Protocol (CDP) WebSocket, evaluating real rendered DOM geometry (`getBoundingClientRect()`) across 1707x932, 1440x900, and 390x844 viewports.
  - Integrated all test suites into Docker multi-stage build (`mach-playbook:test`), `tools/test.sh`, and GitHub Actions deployment workflow.

---

## [2026-10-03] feat | Contact: Formspree Serverless Architecture & Async UI Feedback Loop

- **Impacted Files**: `_tabs/contact.md`
- **Summary**:
  - Upgraded contact system to Jamstack serverless architecture using Formspree endpoint `https://formspree.io/f/xoevgrqq`.
  - Added hidden anti-spam honeypot field `<input type="text" name="_gotcha" style="display:none !important">` to trap automated bots silently without CAPTCHA friction.
  - Implemented modern asynchronous client-side `fetch()` with `Accept: application/json` header.
  - Displays inline Bootstrap success and error feedback banners (`#form-success`, `#form-error`) with smooth auto-reset, keeping the user on `/contact/` without disrupting navigation.
  - Preserved standard HTML POST action and graceful degradation fallback for clients with JavaScript disabled.

---

## [2026-10-03] ingest | Knowledge Base Ingestion per Karpathy LLM Wiki Architecture

- **Impacted Files**: `wiki/SCHEMA.md`, `wiki/log.md`, `wiki/index.md`, `wiki/ui-ux-design-system-and-testing.md`, `wiki/contact-and-formspree-architecture.md`, `wiki/architecture.md`, `wiki/tools-and-operations.md`, `wiki/sources/karpathy-llm-wiki-gist.md`
- **Summary**:
  - Fully ingested all architectural decisions, layout postmortems, test suite frameworks, and serverless patterns from the interactive session into the persistent wiki.
  - Established formal `wiki/SCHEMA.md` and chronological `wiki/log.md`.
  - Cross-linked new domain modules in `wiki/index.md` and updated operational procedures.
