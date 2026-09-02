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

### Technical Gotcha: The Asynchronous "Couldn't fetch" State
When any sitemap is newly submitted in GSC:
- `Type` initially appears as `Unknown`.
- `Last read` remains blank.
- `Status` displays in red as `Couldn't fetch`.
This is normal Google Search Console asynchronous queueing behavior: Googlebot has not yet sent the HTTP request. Once the Googlebot worker pulls the queue item, it executes `GET https://mach-playbook.github.io/sitemap.xml` (which responds `HTTP/2 200 OK` with 222 URLs), sets `Type: Sitemap`, logs the timestamp in `Last read`, and updates status to `Success`.

