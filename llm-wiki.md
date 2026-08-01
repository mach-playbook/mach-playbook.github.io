# LLM Wiki & Knowledge Base (`llm-wiki.md`)

> Authoritative repository context, architectural patterns, workflow automation rules, environment gotchas, technical specifications, and AI Agent skills operating within the **MACH Playbook** codebase.
> 
> *Format: Karpathy-style LLM Wiki (Markdown formatted for GitHub UI navigation).*

---

## 1. Project Overview & Architecture

- **Repository Name**: `mach-playbook` (`mach-playbook.github.io`)
- **Live Production URL**: [https://mach-playbook.github.io](https://mach-playbook.github.io)
- **Local Replica URL**: `http://localhost:8080` (Nginx Docker container)
- **Framework**: Static Site Generator built on **Jekyll** with the [Chirpy Theme](https://github.com/cotes2020/jekyll-theme-chirpy) (v7.5+).
- **Core Domain & Purpose**: Enterprise architecture playbook providing deep technical insights into **MACH** (**M**icroservices, **A**PI-First, **C**loud-Native, **H**eadless) architectures, cloud multi-cloud strategies (GCP, AWS), API management (Apigee, MuleSoft), ERP integrations (CFDI security), Next.js/Supabase serverless edge architectures, OpenSIPS VoIP security routing, and database administration.
- **Content Inventory**: **53 deep technical guides** (>1,000 words each):
  - **35 English Articles** (`lang: en`)
  - **18 Spanish Articles** (`lang: es`)
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
   - Displays real-time post count badges (`All: 53`, `Español: 18`, `English: 35`).
2. **Home Feed Filter Pills (`_layouts/home.html`)**:
   - Filter pill group positioned directly above `#post-list`.
   - Renders `Filter: [ All (53) | 🇲🇽/🇪🇸 Español (18) | 🇺🇸 English (35) ]`.
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
  - Non-thin content word counts (>1,000 words per article across all 53 posts).
  - Explicit language classification (`lang: es` or `lang: en`).

### B. Zero-Duplication & High E-E-A-T Content
- **Zero-Duplication Guarantee**: Verified with `scripts/check-duplicates.py` (**0% title duplication, 0% body duplication** across all 53 posts).
- **Article Depth**: All articles exceed 1,000 words, featuring concrete architectural diagrams, code snippets, and Senior Solutions Architect insights.

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

# 2. Run HTMLProofer Unit Tests (287 HTML files, 646 internal links)
docker build --target test -t mach-playbook:test .

# 3. Rebuild and Launch Local Production Container on http://localhost:8080
docker rm -f mach-playbook-site
docker build -t mach-playbook:prod .
docker run -d --name mach-playbook-site -p 8080:80 mach-playbook:prod
```

---

## 6. Technical SEO & Google Search Console Guide

- **Sitemap Location**: `https://mach-playbook.github.io/sitemap.xml` (HTTP 200 OK, 287 URLs).
- **Robots.txt Location**: `https://mach-playbook.github.io/robots.txt` (authorizes `sitemap.xml`).
- **Sitemap Extraction Utility**: `scripts/list-urls.py` parses all 287 sitemap links.
- **Google Search Console (GSC) Behavior**:
  - **Sitemap Status**: `"Couldn't fetch"` occurs on initial GSC submission before background worker executes. Resolves automatically to **Success (287 discovered pages)** within 24–48 hours.
  - **Live URL Inspection for XML**: Inspecting `.xml` files in GSC displays `"URL is not on Google"` because GSC inspects HTML DOM pages, not raw XML data feeds.
  - **Manual Request Indexing**: Executed via `browser_subagent` for high-priority pages up to Google's daily quota limit (~10–12 URLs / 24 hrs).

---

## 7. Known Environment Gotchas & Solutions

| Gotcha | Root Cause | Solution |
| :--- | :--- | :--- |
| **GitHub CLI Auth Failure on Windows** | PowerShell sets invalid `GITHUB_TOKEN` environment variable | Run `wsl gh` to bypass env var and use valid `hosts.yml` token |
| **Jekyll Missing Future Dated Posts** | UTC build time offset excludes posts with local timestamps | Set `future: true` in `_config.yml` |
| **Sidebar Menu Subtitle Overlap** | Chirpy theme `height: 3rem` hardcoded constraint | Override with `height: auto !important` in `_includes/head.html` |
| **Inline Script Liquid Minification Error** | Inline `<script>` tags in `_layouts/home.html` cause syntax truncation | Load external script `assets/js/lang-filter.js` |
| **Circuit Breaker Slug Typo** | Initial post slug had `circuit-breer` | Renamed slug & cover image asset to `circuit-breaker` |

---

## 8. Agent Workflows & Custom Skills

The project maintains two registered Agent skills located in `.agents/skills/`:

1. **`add-new-post-test-deploy`** (`.agents/skills/add-new-post-test-deploy/SKILL.md`):
   - Standardized workflow to create new Jekyll Markdown posts, check duplicate content, run AdSense policy tests, execute Docker HTML-Proofer unit tests, commit, push, and validate GitHub Actions deployment.

2. **`gsc-manual-url-submission`** (`.agents/skills/gsc-manual-url-submission/SKILL.md`):
   - Automated workflow for sitemap URL extraction (`scripts/list-urls.py`), HTTP header verification, and manual URL Inspection & Request Indexing via `browser_subagent` in Google Search Console.
