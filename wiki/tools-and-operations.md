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
