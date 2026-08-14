# LLM Wiki & Knowledge Base (`llm-wiki.md`)

> **MANDATORY DIRECTIVE FOR ALL AI AGENTS & SKILLS**:
> Always consult this Karpathy-style LLM Wiki (`llm-wiki.md`) first as the primary, single source of truth for project architecture, coding standards, environment gotchas, deployment workflows, and E-E-A-T / AdSense compliance rules before executing tasks.

---

## 1. Project Overview & Architecture

- **Repository Name**: `mach-playbook` (`mach-playbook.github.io`)
- **Live Production URL**: [https://mach-playbook.github.io](https://mach-playbook.github.io)
- **Local Replica URL**: `http://localhost:8080` (Nginx Docker container)
- **Framework**: Static Site Generator built on **Jekyll** with the [Chirpy Theme](https://github.com/cotes2020/jekyll-theme-chirpy) (v7.5+).
- **Core Domain & Purpose**: Enterprise architecture playbook providing deep technical insights into **MACH** (**M**icroservices, **A**PI-First, **C**loud-Native, **H**eadless) architectures, cloud multi-cloud strategies (GCP, AWS), API management (Apigee, MuleSoft), ERP integrations (CFDI security), Next.js/Supabase serverless edge architectures, OpenSIPS VoIP security routing, YugabyteDB distributed SQL, local graph database indexing for AI IDEs in WSL, and database administration.
- **Content Inventory**: **62 deep technical guides** (>1,000 words each):
  - **34 English Articles** (`lang: en`)
  - **28 Spanish Articles** (`lang: es`)
- **Author Identity & E-E-A-T**:
  - **Author Name**: **Lenin Meza** (`author: leninmeza` / `lenin`)
  - **Personal Portfolio**: [https://merolhack.github.io/](https://merolhack.github.io/)
  - **LinkedIn Profile**: [https://www.linkedin.com/in/leninmezazarco](https://www.linkedin.com/in/leninmezazarco)
  - **GitHub Profile**: [https://github.com/merolhack](https://github.com/merolhack)

---

## 2. Global Language Selector & Filtering System

The site implements dynamic bilingual post classification (`lang: es` and `lang: en`) backed by a client-side filtering engine:

### A. UI Placement Architecture
1. **Global Topbar Selector (`_includes/topbar.html`)**:
   - Globe icon dropdown button (`🌐 All | 🇲🇽/🇪🇸 Español | 🇺🇸 English`) positioned next to `#search`.
   - Displays real-time post count badges (`All: 62`, `Español: 28`, `English: 35`).
2. **Home Feed Filter Pills (`_layouts/home.html`)**:
   - Filter pill group positioned directly above `#post-list`.
   - Renders `Filter: [ All (62) | 🇲🇽/🇪🇸 Español (28) | 🇺🇸 English (34) ]`.
3. **Card & Header Badges**:
   - Each post card and article header renders explicit language badges (`🇲🇽/🇪🇸 Español` vs `🇺🇸 English`).

### B. Client-Side Script Engine (`assets/js/lang-filter.js`)
- **Function**: `setLanguageFilter(lang)`
- **Behavior**: Real-time card visibility toggle (`data-post-lang="es"` vs `data-post-lang="en"`).
- **State Persistence**: Saves selection to `localStorage.setItem('mach_playbook_lang', lang)` to maintain user language preference across page navigation and page reloads.

---

## 3. Monetization & E-E-A-T Adherence

### A. Automated AdSense Policy Compliance Suite (`scripts/test-adsense-compliance.py`)
- Programmatically executes pre-deployment checks validating:
  - `ads.txt` publisher verification (`google.com, pub-2700240339792942, DIRECT, f08c47fec0942fa0`).
  - `<head>` Publisher ID & Verification Meta Tag insertion (`ca-pub-2700240339792942`).
  - Privacy policy disclosures in `_tabs/privacy.md`.
  - Author credentials in `_tabs/about.md`.
  - Non-thin content word counts (>1,000 words per article across all 63 posts).
  - Explicit language classification (`lang: es` or `lang: en`).

### B. Zero-Duplication & High E-E-A-T Content
- **Zero-Duplication Guarantee**: Verified with `scripts/check-duplicates.py` (**0% title duplication, 0% body duplication** across all 63 posts).
- **Article Depth**: All articles exceed 1,000 words, featuring concrete architectural diagrams, code snippets, and Senior Solutions Architect insights.

### C. Google AdSense Approval Status
- **Domain**: `mach-playbook.github.io`
- **Status**: `Getting ready` / Review Requested (Site Ownership Verified).

---

## 4. Automated Image Generation Pipeline

### Script: `scripts/generate-images.js`
- **CI/CD Workflow**: `.github/workflows/auto-generate-images.yml`
- **Primary Generator**: Pollinations AI API with topic-aware prompts (`server room`, `datacenter`, `microchip`, `code editor`).
- **Fallback Pool**: Expanded to **46+ verified high-resolution Unsplash IT graphics**.
- **Mapping Logic**: `index % unsplashITPhotos.length`, guaranteeing **100% unique cover graphics** across all posts.

---

## 5. Local Docker Testing & CI/CD Workflow

The repository includes a multi-stage `Dockerfile` and `docker-compose.yml` mirroring GitHub Actions CI/CD (Ruby 3.4, Jekyll Chirpy, HTMLProofer, Nginx):

```bash
# 1. Run AdSense Policy Compliance Test Suite
python3 scripts/test-adsense-compliance.py

# 2. Run HTMLProofer Unit Tests (328 HTML files, 747 internal links)
docker build --target test -t mach-playbook:test .

# 3. Rebuild and Launch Local Production Container on http://localhost:8080
docker rm -f mach-playbook-site
docker build -t mach-playbook:prod .
docker run -d --name mach-playbook-site -p 8080:80 mach-playbook:prod
```

---

## 6. Technical SEO & Google Search Console Guide

- **Sitemap Location**: `https://mach-playbook.github.io/sitemap.xml` (HTTP 200 OK, 331 URLs).
- **Robots.txt Location**: `https://mach-playbook.github.io/robots.txt` (authorizes `sitemap.xml`).
- **Sitemap Extraction Utility**: `scripts/list-urls.py` parses all sitemap links.
- **Google Search Console (GSC) Behavior**:
  - **Sitemap Status**: `"Couldn't fetch"` occurs on initial GSC submission before background worker executes. Resolves automatically to **Success (331 discovered pages)** within 24–48 hours.
  - **Live URL Inspection for XML**: Inspecting `.xml` files in GSC displays `"URL is not on Google"` because GSC inspects HTML DOM pages, not raw XML data feeds.
  - **Manual Request Indexing**: Executed via `browser_subagent` for high-priority pages up to Google's daily quota limit (~10–12 URLs / 24 hrs).

---

## 7. Codebase Memory Knowledge Graph (`codebase-memory`)

- **Project ID**: `home-merolhack-fl-mach-playbook`
- **Graph Status**: Active & Updated (`index_status` ready, `detect_changes` tracked).
- **Mandatory Usage Rule**: Agents MUST query graph tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) to explore symbols and relationships before making code modifications.

---

## 8. Known Environment Gotchas & Solutions

| Gotcha | Root Cause | Solution |
| :--- | :--- | :--- |
| **GitHub CLI Auth Failure on Windows** | PowerShell sets invalid `GITHUB_TOKEN` environment variable | Run `wsl gh` to bypass env var and use valid `hosts.yml` token |
| **Jekyll Missing Future Dated Posts** | UTC build time offset excludes posts with local timestamps | Set `future: true` in `_config.yml` |
| **Sidebar Menu Subtitle Overlap** | Chirpy theme `height: 3rem` hardcoded constraint | Override with `height: auto !important` in `_includes/head.html` |
| **Inline Script Liquid Minification Error** | Inline `<script>` tags in `_layouts/home.html` cause syntax truncation | Load external script `assets/js/lang-filter.js` |
| **Circuit Breaker Slug Typo** | Initial post slug had `circuit-breer` | Renamed slug & cover image asset to `circuit-breaker` |
| **Missing `lang: es` Tag in New Posts** | `test-adsense-compliance.py` fails if explicit `lang: es` or `lang: en` flag is missing in frontmatter | Always include `lang: es` or `lang: en` in frontmatter of new posts |

---

## 9. Agent Workflows & Custom Skills

The project maintains registered Agent skills and autonomous CI/CD pipelines:

1. **`add-new-post-test-deploy`** (`.agents/skills/add-new-post-test-deploy/SKILL.md`):
   - Standardized workflow to create new Jekyll Markdown posts, check duplicate content, run AdSense policy tests, execute Docker HTML-Proofer unit tests, commit, push, and validate GitHub Actions deployment.

2. **`gsc-manual-url-submission`** (`.agents/skills/gsc-manual-url-submission/SKILL.md`):
   - Automated workflow for sitemap URL extraction (`scripts/list-urls.py`), HTTP header verification, and manual URL Inspection & Request Indexing via `browser_subagent` in Google Search Console.

3. **`daily-blog-post` Autonomous Publishing Pipeline** (`.github/workflows/daily-blog-post.yml` & `scripts/publish_daily_jekyll_post.py`):
   - Daily cron (`0 13 * * *` = 07:00 AM America/Mexico_City) and `workflow_dispatch` trigger.
   - Automatically executes Gemini API calls (`gemini-2.5-flash` / `gemini-2.0-flash` / `gemini-1.5-flash`), scans `_posts/` for deduplication, generates 1,500-2,200 words Senior Architect articles across 5 MACH pillars, runs AdSense compliance tests, and pushes to `main`.
   - Granular `permissions: contents: write` configured at the workflow level to allow git write operations even when repo default token is set to read-only.
