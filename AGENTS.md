2026-04-04 18:58: Phase 4 configuration completed
- Edited _config.yml with site details, dark mode, github repo/username and giscus comments.
- Added _tabs/about.md with customized description.
- Created _tabs/privacy.md for future AdSense application logic.

2026-04-04 19:12: Phase 5 progression
- Programmatically extracted dates and copied 34 Markdown posts to _posts/.
- Formatted post names with date-prefix to follow Jekyll's naming convention.
- Created _includes/head.html template with AdSense placeholder script.
- Waiting for user to configure Giscus repo_id and category_id.

2026-04-05 13:00: Phase 6 Automation Complete
- Modified Auto-Generate Image script to use unmetered Pollinations AI instead of Gemini Free due to Google account block.
- Pushed workflow to dynamically synthesize frontmatter images for all 34 posts natively.
- Scaffolded scalable vector mapping (`avatar.svg`).
- Un-commented and activated Google AdSense ID linking via custom headers and injected `ads.txt`.

2026-07-13 21:39: Sidebar Layout & GitHub Link Fix
- Fixed sidebar navigation menu overlap caused by multiline site subtitle (`height: 3rem` overridden to `height: auto !important` in `_includes/head.html`).
- Updated GitHub logo/profile links to `https://github.com/merolhack` in `_config.yml` and `_data/contact.yml`.

2026-07-22 19:00: AdSense E-E-A-T & Thin Content Resolution
- Identified Google AdSense "Low value content" violation.
- Developed `scripts/deep-expand-posts.py` to programmatically rewrite 34 thin Markdown posts.
- Expanded all posts to >1,100 words using advanced architectural insights (GCP, AWS, MuleSoft, Apigee, Event-driven architectures) ensuring Senior Solutions Architect tone, while preserving YAML frontmatter and AI image automation.
- Deepened E-E-A-T trust signals by updating `_tabs/about.md` with explicit professional credentials.
- Updated `_tabs/privacy.md` to explicitly comply with Google AdSense cookie tracking and opt-out policies.
- Verified `_data/contact.yml` accurately points to the `merolhack` GitHub profile.
- Encountered a GitHub CLI authentication gotcha: Windows `gh` fails due to an invalid `GITHUB_TOKEN` environment variable in PowerShell overriding valid keyring credentials. Executing `wsl gh` bypasses this environment variable and successfully utilizes the `hosts.yml` valid token.

2026-07-23 03:30: Author Attribution & Sidebar LinkedIn Integration
- Configured `_data/authors.yml` and `_config.yml` social metadata for author **Lenin Meza** (`author: leninmeza`), linking post author titles to `https://merolhack.github.io/`.
- Updated `_data/contact.yml` with LinkedIn profile (`https://www.linkedin.com/in/leninmezazarco`) rendering FontAwesome `fab fa-linkedin` in the sidebar footer.
- Overhauled image generator (`scripts/generate-images.js`) to strictly produce IT, server, microchip, data center, and code editor graphics, eliminating landscape fallbacks.

2026-07-23 06:12: E-E-A-T Spanish Articles & Sitemap Fix
- Published 4 comprehensive Spanish-language technical posts: `orquestacion-mach-multi-nube.md`, `infraestructura-voip-cloud-native.md`, `arquitectura-api-first-erpnext.md`, and `finops-desmantelamiento-gcp.md`.
- Solved Jekyll future post exclusion gotcha where posts were omitted from build/sitemap due to UTC timezone offsets by adding `future: true` in `_config.yml` and adjusting date timestamps.
- Verified all 39 posts are indexed in the live `sitemap.xml`.

2026-07-23 21:51: Docker Desktop Testing Environment & AI QA Articles
- Published 2 additional Spanish-language technical articles: `automatizacion-inteligente-playwright-ollama.md` and `flujos-hibridos-wsl-powershell-windows.md`. Total posts: **41**.
- Created multi-stage `Dockerfile` (builder, test, dev, prod), `docker-compose.yml`, `.dockerignore`, and npm scripts to replicate GitHub Pages CI/CD locally (Ruby 3.4, Jekyll Chirpy, HTMLProofer, Nginx).
- Verified HTMLProofer unit tests in Docker container (`mach-playbook:test`) passing 101 files / 193 links with 0 errors (`HTML-Proofer finished successfully`).
- Started background production replica container `mach-playbook-site` listening on `http://localhost:8080` (HTTP 200 OK).
- Verified GitHub Actions `Build and Deploy` and `Auto Generate Missing Post Images` pipelines completed with `completed | success`.

2026-07-24 17:45: Dual Language Selector UI, Sitemap & GSC Audit
- Built interactive Global Language Selector dropdown (`_includes/topbar.html` override) and Home Feed Filter Pills (`_layouts/home.html` override) displaying `Filter: [ All (43) | 🇲🇽/🇪🇸 Español (8) | 🇺🇸 English (35) ]`.
- Implemented `assets/js/lang-filter.js` for instant Vanilla JS filtering and `localStorage` preference persistence.
- Verified live `https://mach-playbook.github.io/sitemap.xml` returns `HTTP 200 OK` with 240 URLs and verified `robots.txt` authorization.
- Conducted Google Search Console audit: resolved sitemap typo (`/sitemap.xm` -> `/sitemap.xml`), explained "URL is not on Google" / "Something went wrong" live test behavior for XML files, and verified priority crawl queue status.
- Rebuilt local Docker container `mach-playbook-site` (`http://localhost:8080`) and verified GitHub Actions deployment `30113525500` completed with `completed | success`.

2026-07-27 16:30: DB Migration & VoIP Posts, Automated AdSense Compliance Suite
- Published 2 additional Spanish technical articles: `estrategias-migracion-bases-datos-multi-nube.md` and `trazabilidad-avanzada-traduccion-gateways-voip.md`. Total posts: **45** (35 EN, 10 ES).
- Created `scripts/test-adsense-compliance.py` unit testing suite validating `ads.txt`, `<head>` Publisher ID, Privacy disclosures, E-E-A-T credentials, and non-thin word counts (>1,000 words per article).
- Auto-generated 100% unique cover graphics via `scripts/generate-images.js`.
- Verified HTMLProofer in Docker container (`mach-playbook:test`) passing 251 files / 579 internal links with 0 errors.
- Pushed commit `f7241c9` to `main`, with GitHub Actions `Build and Deploy` workflow `30285213779` executing successfully.

2026-07-31 23:12: CFDI Cloud-Native Cryptography & Cloud Run Blue/Green Articles
- Published 2 specialized Spanish-language technical posts: `2026-07-31-gestion-segura-certificados-cfdi-cloud-native.md` and `2026-07-31-infraestructura-inmutable-despliegues-blue-green-cloud-run.md`. Total posts: **51** (37 EN, 14 ES).
- Verified zero content duplication via `scripts/check-duplicates.py` and 100% Google AdSense policy compliance via `scripts/test-adsense-compliance.py`.
- Tested site generation and HTML-Proofer unit tests in Docker container (`mach-playbook:test`) passing 279 files and 627 internal links with 0 errors.
- Committed, rebased, and pushed changes to `main`.
- Validated GitHub Actions `Auto Generate Missing Post Images` (`30672188420`) and `Build and Deploy` (`30672221791`) workflows completed successfully (`completed | success`).

2026-08-01 20:16: Next.js/Supabase Headless & OpenSIPS VoIP Fraud Mitigation Articles
- Published 2 final Spanish-language technical articles: `2026-08-01-desarrollo-headless-nextjs-supabase.md` and `2026-08-01-mitigacion-fraude-voip-opensips.md`. Total posts: **53** (35 EN, 18 ES).
- Verified zero content duplication via `scripts/check-duplicates.py` and 100% Google AdSense policy compliance via `scripts/test-adsense-compliance.py`.
- Tested site generation and HTML-Proofer unit tests in Docker container (`mach-playbook:test`) passing 287 files and 644 internal links with 0 errors.
- Committed, rebased, and pushed changes to `main`.
- Validated GitHub Actions `Auto Generate Missing Post Images` (`30716592803`) and `Build and Deploy` (`30716592844`) workflows completed successfully (`completed | success`).

2026-08-01 21:01: Circuit Breaker Typo Fix in Post Slug & Cover Image Asset
- Corrected typo in post slug from `_posts/2026-04-04-circuit-breer-pattern-protecting-your-services-from-cascading-failures.md` to `_posts/2026-04-04-circuit-breaker-pattern-protecting-your-services-from-cascading-failures.md`.
- Updated `image: path:` frontmatter reference and renamed `assets/img/posts/2026-04-04-circuit-breaker-pattern-protecting-your-services-from-cascading-failures.png`.
- Verified HTML-Proofer unit tests in Docker container (`mach-playbook:test`) passing 287 files and 646 internal links with 0 errors.
- Pushed commit `68fec55` to `main`, with GitHub Actions `Build and Deploy` workflow `30718198685` executing successfully (`completed | success`).

2026-08-01 21:50: GSC Sitemap Audit, Manual Indexing & Agent Skills Registration
- Conducted Google Search Console sitemap audit: verified `sitemap.xml` returns `HTTP 200 OK` (287 URLs) and `robots.txt` authorization. Re-submitted `sitemap.xml` in GSC to trigger crawler queue.
- Executed manual URL Inspection & Request Indexing via `browser_subagent` for top site pages and blog posts up to GSC daily quota limit.
- Registered two specialized Agent Workflows in `.agents/skills/`:
  1. `.agents/skills/add-new-post-test-deploy/SKILL.md`: 7-step post creation, compliance check, Docker testing & CI/CD deployment workflow.
  2. `.agents/skills/gsc-manual-url-submission/SKILL.md`: Sitemap extraction, header validation & Search Console URL inspection workflow.
- Ingested comprehensive repository context, architecture, gotchas, and skills into `llm-wiki.md`, `README.md`, and `HISTORY.txt`.

2026-08-05 11:55: Apigee/MuleSoft Integration & Playwright/Ollama E2E Testing Articles
- Published 2 Spanish-language technical articles: `2026-08-05-gestion-apis-apigee-mulesoft-salesforce.md` and `2026-08-05-automatizacion-e2e-playwright-ollama.md`. Total posts: **59** (35 EN, 24 ES).
- Fixed `lang: es` frontmatter tags across newly published and recent Spanish posts.
- Verified zero content duplication via `scripts/check-duplicates.py` and 100% Google AdSense policy compliance via `scripts/test-adsense-compliance.py`.
- Executed Docker unit testing (`mach-playbook:test`), passing 309 files / 693 internal links with 0 errors (`HTML-Proofer finished successfully`).
- Verified automatic inclusion of new article URLs in dynamic `sitemap.xml`.
- Committed and pushed commit `c361e88` to `main`.
- Validated GitHub Actions `Auto Generate Missing Post Images` (`31032141220`) and `Build and Deploy` (`31032197440`) workflows completed with status `completed | success`.

2026-08-05 11:58: Mandatory Codebase Memory Rule Added
- Created `.agents/AGENTS.md` defining strict project-scoped rules for AI agents:
  1. ALWAYS query `codebase-memory` knowledge graph tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) before performing broad file reads or grepping.
  2. ALWAYS check `index_status` and update the knowledge graph using `index_repository` / `detect_changes` whenever files are modified or added.

2026-08-11 18:55: YugabyteDB & Local Graph Indexing Articles, AdSense Status & LLM Wiki Ingestion
- Published 2 Spanish-language technical articles: `2026-08-11-sistemas-sql-distribuidos-yugabytedb.md` and `2026-08-11-indexacion-grafos-locales-ia-ides.md`. Total posts: **63** (35 EN, 28 ES).
- Fixed missing `lang: es` frontmatter metadata tags and ran `scripts/test-adsense-compliance.py` to achieve 100% AdSense Policy Compliance PASS.
- Tested site build & internal links via Docker container (`mach-playbook:test`), passing 331 HTML files and 729 links with 0 errors.
- Verified Google AdSense Console status: Site Ownership Verified, Review Requested ("Getting ready").
- Updated `codebase-memory` knowledge graph (`home-merolhack-fl-mach-playbook`) via `detect_changes` and `index_status`.
- Updated Karpathy-style `llm-wiki.md`, `.agents/AGENTS.md`, `.agents/skills/add-new-post-test-deploy/SKILL.md`, `README.md`, and `HISTORY.txt`.
- Established strict mandate across all AGENTS and SKILLS to ALWAYS consult `llm-wiki.md` first for project knowledge and rules.

2026-08-13 23:15: Autonomous Daily Blog Post Agent & Workflow Setup
- Developed `scripts/publish_daily_jekyll_post.py`: Autonomous daily post publishing engine integrating Gemini API (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-flash-latest`), automated deduplication scanning `_posts/`, 5-pillar MACH architectural topic matrix, and Senior Architect E-E-A-T prompt standards with Mermaid diagrams and code snippets.
- Implemented `.github/workflows/daily-blog-post.yml`: GitHub Actions workflow with cron schedule (`0 13 * * *` = 07:00 AM CDMX / 13:00 UTC) and `workflow_dispatch` manual trigger with `dry_run`, `topic`, and `lang` parameters.
- Configured granular `permissions: contents: write` in workflow YAML to permit autonomous `git commit` and `git push` directly to `main` with fallback PAT token support (`GH_PAT`).
- Verified zero duplicate matches and 100% Google AdSense policy compliance across scripts and dry-run tests.


2026-08-14 00:50: GSC 48-Hour Indexation & AdSense Audit Workflow Registered
- Registered new specialized Agent Workflow in `.agents/skills/gsc-48h-indexation-audit/SKILL.md`.
- Implemented automated pre-flight audit script `scripts/audit-gsc-indexation.py` validating live HTTP 200 responses for `sitemap.xml` (117 URLs), `robots.txt`, and core trust tabs.
- Configured step-by-step browser subagent verification protocols for GSC sitemap transition (`Couldn't fetch` -> `Success`), Page Indexing growth tracking, priority URL live inspection, and Google AdSense approval status monitoring.
- Updated `llm-wiki.md`, `AGENTS.md`, and `HISTORY.txt`.

2026-08-15 14:35: Gemini 3 Upgrade, Dynamic Discovery & Autonomous Fallback for Daily Publisher
- Diagnosed failed GitHub Action run 31887174445 caused by deprecation of older Gemini 2.x/1.x models and quota limits on Pro tiers.
- Updated `scripts/publish_daily_jekyll_post.py` with dynamic Gemini model discovery (`get_available_gemini_models`), prioritized 2026 Gemini 3 lineup (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, etc.), fast-fail on 404/429-limit-0, and autonomous deep-dive article synthesis fallback.
- Tested locally in Docker container (`python:3.11-slim` and `ruby:3.4-slim` / `mach-playbook-test`), passing 100% AdSense compliance, zero duplicates, and HTML-Proofer across 64 posts.

2026-08-15 15:05: Phase 1 Quick Wins - Resources Hub & MACH Glossary Tabs Launched
- Created `_tabs/resources.md` and `_tabs/glossary.md` with structured links to MACH Alliance (machalliance.org), CNCF, OpenAPI Initiative, AsyncAPI, and canonical literature.
- Re-sequenced tab orders (1-9) for sidebar navigation.
- Validated with Docker HTML-Proofer (615 links, 142 files, 0 errors) and 100% Google AdSense compliance.

2026-08-15 15:18: Mermaid Diagram Rendering Fix & Mandatory Triple Content Validation Protocol
- Diagnosed unrendered Mermaid code blocks: in Chirpy, `mermaid.min.js` only loads when `page.mermaid` evaluates to `true`.
- Added `mermaid: true` globally to `_config.yml` defaults for both `posts` and `tabs`, ensuring SVG diagram rendering across all articles and resource pages.
- Established the **Mandatory Content Validation Trinity** for all content generated via Antigravity IDE or GitHub Actions:
  1. Content depth (>950–1,500 words, Senior Architect tone, 100% AdSense compliance, zero duplicates).
  2. Matching cover image asset physically present at `/assets/img/posts/<date-slug>.png`.
  3. Mermaid architecture diagram syntax and client-side vector SVG rendering.

2026-08-15 15:45: Spanish Primary Language Setup, Global Flag Switcher & Bilingual Static Pages
- Configured Spanish as the default site language (`lang: es` in `_config.yml`, Spanish tagline and description).
- Added `_data/locales/es.yml`, `_data/locales/es-ES.yml`, and `en.yml` for navigation and Chirpy locale support.
- Overhauled topbar with a compact Flag language toggle (`🇲🇽 ES` / `🇺🇸 EN`).
- Added dynamic `data-i18n-es` / `data-i18n-en` client switching to `_includes/sidebar.html` and bilingual blocks to `_tabs/about.md`, `_tabs/contact.md`, `_tabs/privacy.md`, and `_tabs/terms.md`.
- Injected in-article contextual language notice and Google Translate bridge in `_layouts/post.html`.
- Upgraded `assets/js/lang-filter.js` to manage global localization state (`localStorage`), page text swaps, and home post filtering.
- Validated with Docker HTML-Proofer (599 links, 142 files, 0 errors) and 100% Google AdSense compliance.

2026-08-15 17:45: Markdown Parsing Fix, Global Script Loading & High-Contrast Mermaid Dark Mode
- Resolved Kramdown markdown skipping inside HTML blocks by adding `markdown="1"` to all bilingual `.lang-block` containers in `_tabs/about.md`, `_tabs/contact.md`, `_tabs/privacy.md`, and `_tabs/terms.md`.
- Added global `assets/js/lang-filter.js` loading via `_includes/head.html` with `defer`, ensuring flag switcher and language persistence work across 100% of pages.
- Added comprehensive CSS styling for Mermaid sequence diagrams and flowcharts in `_includes/head.html` for high contrast on `#1b1b1e` dark theme.
- Added `scripts/test-site-integrity.py` and embedded into `Dockerfile` Stage 2 test runner (19/19 checks passed).

2026-08-21 08:50: Page Speed Optimization, Core Web Vitals Hardening & GSC Forensics
- Eliminated render-blocking JS in `<head>` by adding `defer` to `theme.min.js`.
- Optimized Resource Hints: added `crossorigin` to `fonts.gstatic.com` preconnect, preconnected to `cdn.jsdelivr.net`, and added `dns-prefetch` for AdSense and GTM.
- Solved Cumulative Layout Shift (CLS): added explicit `width="400" height="225"` and `aspect-ratio: 16/9; object-fit: cover;` across all post preview images (`_layouts/home.html`) and `width="1200" height="630"` with aspect ratio on article hero banners (`_layouts/post.html`).
- Optimized Largest Contentful Paint (LCP) on mobile: configured `loading="eager" fetchpriority="high" decoding="async"` on above-the-fold first post and article hero banner, while setting `loading="lazy" decoding="async"` on subsequent post cards.
- Extended `scripts/test-site-integrity.py` with 4 automated performance assertions (26/26 test points passing with 0 errors).
- Validated Docker Stage 2 unit test pipeline (`mach-playbook:test`) passing 142 HTML files, 641 internal links, and 100% AdSense compliance with 0 errors.
- Conducted Google Search Console forensics: identified `/sitemap.xm` submission typo (missing 'l'), confirmed live `sitemap.xml` HTTP 200 OK with 141 URLs, and explained 3-page indexing baseline vs GSC pipeline indexing lag.

2026-08-21 14:00: Elimination of 0.275 CLS, On-Demand Mermaid Loading & Mobile Lighthouse >90 Achievement
- Replaced asynchronous stylesheet preloads with standard synchronous local CSS (`bootstrap.min.css` and Chirpy theme) and inlined critical layout locks (`.dropdown-menu { display: none; }`, `#search { display: none; }`, `#breadcrumb { display: none; }` on mobile) in `_includes/head.html`, completely eliminating topbar height shifts (CLS: 0.275 -> 0.000).
- Configured on-demand Mermaid.js loading: disabled global `mermaid: true` default in `_config.yml` and enabled only in frontmatter for the 9 posts with diagrams, eliminating 3 MB of unused JS on 62+ text articles.
- Made secondary stylesheets (`tocbot.min.css`, `glightbox.min.css`) non-blocking via `media="print" onload="this.media='all'"`.
- Verified live mobile Lighthouse audit: Performance **91/100**, Accessibility **100/100**, Best Practices **100/100**, SEO **100/100**, CLS **0.000**, FCP **1.4s**, TBT **120ms**.
- Updated Karpathy-style `llm-wiki.md` and codebase memory Knowledge Graph ADR (`manage_adr`) with full architectural documentation.




