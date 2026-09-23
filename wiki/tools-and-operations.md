# Operational Tools, Testing & Codebase Memory

## 1. Codebase Memory Knowledge Graph (`codebase-memory-mcp`)

This project uses `codebase-memory-mcp` to maintain a persistent semantic graph of the repository.

### Mandatory Directive
AI agents MUST prefer graph queries over brute-force grep/find:
- `search_graph`: Query functions, classes, templates, and patterns.
- `trace_path`: Trace dependencies between layouts, includes, and scripts.
- `get_code_snippet`: Read exact symbols directly.
- `index_status`: Verify graph index state for project `home-merolhack-fl-mach-playbook`.
- `detect_changes` / `index_repository`: Re-index modified files after major commits.

---

## 2. Validation & Compliance Test Suites

Execute these commands inside WSL Ubuntu-20.04 before pushing changes to GitHub:

### A. AdSense Policy Compliance Suite
```bash
python3 scripts/test-adsense-compliance.py
```
Validates 13 critical policy assertions: `ads.txt`, `<head>` script direct loading, word counts, legal tabs, taxonomy, and near-duplicate topic detection.

### B. Duplicate Content Checker
```bash
python3 scripts/check-duplicates.py
```
Scans all post titles and body content for duplicate strings or high similarity scores.

### C. WebP Companion Image Generator
```bash
python3 scripts/generate-webp-images.py
```
Converts all PNGs in `assets/img/posts/` into optimized WebP assets for responsive Chirpy image rendering.

### D. Site Integrity Checker
```bash
python3 scripts/test-site-integrity.py
```
Validates Markdown parsing, Kramdown block tags, script defer attributes, and dark-mode Mermaid styling.

---

## 3. Local Docker Testing (HTML-Proofer)

To replicate GitHub Pages build and test conditions locally:
```bash
# Build and run HTML-Proofer in container
docker build --target test -t mach-playbook:test .

# Run local production preview on http://localhost:8080
docker compose up -d
```

---

## 4. Google Search Console Sitemap Submissions Log

Tracking of all formal `sitemap.xml` submissions to Google Search Console (`https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fmach-playbook.github.io%2F`):

| # | Date & Time | Trigger / Reason | URLs in Sitemap | GSC Behavior / Status |
|---|---|---|---|---|
| **1** | **2026-08-13** | Initial site launch and search engine registration | 240 URLs | Typo `/sitemap.xm` corrected to `/sitemap.xml`. Initial `Couldn't fetch` transitioned to `Success` after crawler pass. |
| **2** | **2026-08-14** | Taxonomy Consolidation: Reduced 55 categories to 7 pillars, 201 tags to 21 tags | 117 URLs | Eliminating thin taxonomy suppressed crawl budget; re-submitted clean sitemap. Status: `Success`. |
| **3** | **2026-08-15** | Multilingual Launch: Introduction of bilingual tags and `assets/js/lang-filter.js` | 287 URLs | Re-submitted to index newly created Spanish and English post variants. Status: `Success`. |
| **4** | **2026-08-21** | Performance & CWV Milestone: 0.000 CLS & Mobile Lighthouse >90 | 141 URLs | Re-submitted following layout shift elimination and CSS optimization. Status: `Success`. |
| **5** | **2026-09-02 10:50** | AdSense Remediation: Purged 11 duplicates, published 12 unique technical articles | 223 URLs | Submitted via automated browser subagent. GSC enqueued with status `Success` (discovered pages: 117 prior). |
| **6** | **2026-09-02 11:10** | SEO Pagination Cleanup: Disabled static `paginate: 10`, eliminated `/page2/`..`/page8/` | **222 Clean URLs** | Old sitemap entry deleted via GSC options menu and re-submitted fresh as `sitemap.xml`. Transient `Couldn't fetch` displayed while enqueued in Googlebot asynchronous crawler worker. |
| **7** | **2026-09-17 11:25** | AdSense & CI/CD Freeze Remediation: Re-submitted after fixing WebP assets and continuous deployment | **238 Clean URLs** | Re-submitted via browser subagent. GSC confirmed: 'Sitemap submitted successfully'. Enqueued for Googlebot processing to discover and crawl all 96 deep articles. |
| **8** | **2026-09-23 15:05** | Crawl Path Restoration & XML Deduplication: Eliminated 3 duplicate URLs, added discovery nav & noscript crawl fallback, submitted `/archives/` to GSC Priority Crawl Queue | **306 Clean URLs** | Solved root cause: repaired severed HTML crawl path (hidden JSON pagination) via `<noscript>` & `/archives/` bridge. Deduplicated `composable-commerce`, `mach-architecture`, and `API-First` slugs. Submitted `https://mach-playbook.github.io/archives/` (hosting 108 HTML post links) directly to Google's Priority Crawl Queue. |

### Technical Gotcha: The Asynchronous "Couldn't fetch" State & Crawl Path Dependency
When any sitemap is submitted in GSC:
- `Type` initially appears as `Unknown`.
- `Last read` remains blank.
- `Status` displays in red as `Couldn't fetch` (*Sitemap could not be read*).
**Crucial Rule:** Never delete and re-submit `sitemap.xml` repeatedly when stuck on `Couldn't fetch`. Dominios alojados en GitHub Pages (CDN Fastly) experimentan periódicamente renegociaciones TLS y micro-latencias ante el worker asíncrono de sitemaps. Reenviar el sitemap resetea la cola de Googlebot.
**Solución Arquitectónica:** Googlebot descubre contenido principalmente a través de enlaces `<a href="...">` en el HTML estático. Si la paginación se maneja por JavaScript/JSON en el cliente, Googlebot solo indexará las páginas enlazadas estáticamente. Mantener siempre un camino de rastreo estático accesible (como `/archives/` o bloques `<noscript>`) garantiza la indexación orgánica completa de los 100+ artículos sin depender del worker de sitemaps.


---

## 5. Secondary Model Delegation via Ollama MCP (`consultar_modelo_local`)

To minimize primary LLM token utilization, all agents and automated tools MUST delegate routine and mechanical tasks via the Model Context Protocol (MCP) server `ollama-local`:

### Operational Cascade & Pre-Check
1. **Priority 1 — `gemma4:cloud`**: Always evaluated first. The tool `consultar_modelo_local` automatically queries the Ollama weekly usage API (`https://ollama.com/api/usage`). If weekly usage is below 90%, it routes requests to Gemma 4 (31B) in the cloud.
2. **Priority 2 — `qwen3:8b-8k`**: If the weekly quota is exhausted or if cloud connectivity fails, the tool seamlessly falls back to local Qwen3 8B (~5.22 GB memory footprint, 8k context window).

### Fluid Absorption of Routine Tasks
The `consultar_modelo_local` tool executes the weekly quota pre-check and responds fluidly to absorb:
- Docstrings, code comments, and type annotations
- Simple code boilerplate and repetitive formatting
- Markdown cleanup, table formatting, and regex patterns
- Translation of mechanical texts and changelogs
- Isolated single-prompt QA not requiring multi-file architectural context

---

## 6. Known Environment Gotchas & Solutions

| Gotcha | Root Cause | Solution |
| :--- | :--- | :--- |
| **GitHub CLI Auth Failure on Windows** | PowerShell sets invalid `GITHUB_TOKEN` environment variable | Run `wsl gh` to bypass env var and use valid `hosts.yml` token |
| **Jekyll Missing Future Dated Posts** | UTC build time offset excludes posts with local timestamps | Set `future: true` in `_config.yml` |
| **Sidebar Menu Subtitle Overlap** | Chirpy theme `height: 3rem` hardcoded constraint | Override with `height: auto !important` in `_includes/head.html` |
| **Inline Script Liquid Minification Error** | Inline `<script>` tags in `_layouts/home.html` cause syntax truncation | Load external script `assets/js/lang-filter.js` |
| **Cumulative Layout Shift from Async CSS** | Async CSS preload pops topbar dropdowns and breadcrumbs | Load self-hosted core CSS synchronously and lock `.dropdown-menu { display: none; }` in inline critical CSS |
| **Mermaid 3 MB JS Overhead on Text Posts** | Global `mermaid: true` in `_config.yml` bundled Mermaid on all pages | Set `mermaid: false` by default; enable only in frontmatter for diagram posts |
| **Circuit Breaker Slug Typo** | Initial post slug had `circuit-breer` | Renamed slug & cover image asset to `circuit-breaker` |
| **Missing `lang: es` Tag in New Posts** | `test-adsense-compliance.py` fails if explicit `lang: es` or `lang: en` flag is missing in frontmatter | Always include `lang: es` or `lang: en` in frontmatter of new posts |

---

## 7. Agent Workflows & Custom Skills

The project maintains registered Agent skills and autonomous CI/CD pipelines:

1. **`gsc-48h-indexation-audit`** (`.agents/skills/gsc-48h-indexation-audit/SKILL.md`):
   - Autonomous 48-hour audit workflow for Google Search Console and Google AdSense.
   - Executes pre-flight HTTP diagnostics (`scripts/audit-gsc-indexation.py`).
   - Dispatches browser subagent to verify GSC sitemap status transition from `Couldn't fetch` to `Success` with ~140 discovered pages.
   - Inspects the Page Indexing report for indexed vs non-indexed growth.

2. **`add-new-post-test-deploy`** (`.agents/skills/add-new-post-test-deploy/SKILL.md`):
   - Standardized workflow to create new Jekyll Markdown posts, check duplicate content, run AdSense policy tests, execute Docker HTML-Proofer unit tests, commit, push, and validate GitHub Actions deployment.

3. **`gsc-manual-url-submission`** (`.agents/skills/gsc-manual-url-submission/SKILL.md`):
   - Automated workflow for sitemap URL extraction (`scripts/list-urls.py`), HTTP header verification, and manual URL Inspection & Request Indexing via `browser_subagent` in Google Search Console.

4. **`daily-blog-post` Autonomous Publishing Pipeline** (`.github/workflows/daily-blog-post.yml` & `scripts/publish_daily_jekyll_post.py`):
   - Daily cron (`0 13 * * *` = 07:00 AM America/Mexico_City) and `workflow_dispatch` trigger.
   - Automatically executes Gemini API calls with dynamic model discovery (`GET /v1beta/models`) prioritizing the Gemini 3 fleet (`gemini-3.7-flash`, `gemini-3.6-flash`, etc.) with intelligent fallback to autonomous high-quality deep-dive synthesis. Scans `_posts/` for deduplication, generates 1,500-2,200 words Senior Architect articles across 5 MACH pillars, synthesizes matching cover images, runs AdSense compliance and duplicate tests, and pushes to `main`.
   - Granular `permissions: contents: write` configured at the workflow level to allow git write operations even when repo default token is set to read-only.

5. **Resources & Ecosystem Hub (`_tabs/resources.md`) & MACH Glossary (`_tabs/glossary.md`)**:
   - Authoritative directory connecting MACH Playbook directly to the MACH Alliance (`machalliance.org`), CNCF landscape, OpenAPI 3.1, AsyncAPI 3.0, and Martin Fowler / Sam Newman canonical literature.
   - Categorized A-Z technical glossary of 30+ terms cross-linked with corresponding published articles for maximum internal linking, SEO authority, and user engagement.



