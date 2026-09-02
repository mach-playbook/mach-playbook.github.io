# Project Knowledge, LLM Wiki & Agent Guidelines (`.agents/AGENTS.md`)

This workspace uses `llm-wiki.md` as its primary Karpathy-style knowledge base and `codebase-memory-mcp` for structural graph discovery.

---

## 1. MANDATORY LLM WIKI INSTRUCTION FOR ALL AGENTS & SKILLS

- **ALWAYS CONSULT THE LLM WIKI FIRST**:
  Before starting any task, architectural research, content creation, or debugging in this repository, ALL AGENTS and SKILLS MUST consult the **LLM Wiki** ([`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md) and [`llm-wiki.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/llm-wiki.md)) as the authoritative single source of truth for:
  - Repository architecture & Jekyll Chirpy theme specs ([`wiki/architecture.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/architecture.md))
  - Google AdSense policy compliance & direct async script loading rules ([`wiki/adsense-policy-and-compliance.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/adsense-policy-and-compliance.md))
  - Autonomous daily publishing pipeline, topic matrix & smart Jaccard deduplication ([`wiki/publishing-pipeline-and-deduplication.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/publishing-pipeline-and-deduplication.md))
  - Content standards & E-E-A-T editorial requirements ([`wiki/content-and-editorial-standards.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/content-and-editorial-standards.md))
  - Operational testing suites, Docker HTML-Proofer & `codebase-memory-mcp` tools ([`wiki/tools-and-operations.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/tools-and-operations.md))

---

## 2. MANDATORY CODEBASE MEMORY GRAPH INSTRUCTIONS

1. **ALWAYS Query the Knowledge Graph First**:
   - Before performing broad searches, reading large files, or running grep across the repository, ALWAYS use `codebase-memory` MCP tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) to query the knowledge graph (`home-merolhack-fl-mach-playbook`).

2. **Verify and Update Index Status**:
   - Always check `index_status` to verify that the graph is up to date for the target project (`home-merolhack-fl-mach-playbook`).
   - After creating, modifying, or deleting files, run `index_repository` or `detect_changes` to re-index the repository and ensure the knowledge graph stays perfectly synchronized with the workspace.

3. **Priority Tool Execution Order**:
   - `index_status`: Verify project indexing status and graph freshness.
   - `search_graph`: Find functions, classes, routes, variables, and markdown symbols by pattern.
   - `trace_path`: Trace incoming/outgoing dependencies or call graphs.
   - `get_code_snippet`: Retrieve target code snippets directly from graph nodes.
   - `index_repository`: Re-index modified files into the graph after changes.

## 3. MANDATORY CONTENT VALIDATION TRINITY (ALL SESSIONS & WORKFLOWS)

Whenever new content (posts, pages, tabs) is generated—whether in **Antigravity IDE pair-programming sessions** or via the **autonomous GitHub Actions workflow (`daily-blog-post.yml`)**—ALL AGENTS and AUTOMATIONS MUST ALWAYS perform and verify the **Three Pillar Content Validations**:

1. **Content Depth & E-E-A-T Quality Gate**:
   - Article word count must exceed **>950–1,500 words** of actionable, senior-level architectural analysis.
   - Front matter must have valid taxonomy (`layout: post`, `title`, `date`, `lang: es` or `lang: en`, approved `categories`, structured `tags`, `image`, `mermaid: true`).
   - Must pass deduplication (`scripts/check-duplicates.py`) with 0 duplicate titles/bodies.
   - Must achieve **100% PASS** on `scripts/test-adsense-compliance.py`.

2. **Cover Image Asset Verification**:
   - Every post must resolve an explicit cover image in `image.path` pointing to `/assets/img/posts/<date-slug>.png`.
   - The image file must physically exist on disk, match IT/cloud architectural themes, and load without 404s.

3. **Mermaid Architecture Diagram Rendering**:
   - Every post must include at least one valid Mermaid architecture/flow/sequence diagram (```` ```mermaid ````).
   - Ensure `mermaid: true` is active (configured globally in `_config.yml` defaults and frontmatter) so `npm/mermaid@11/dist/mermaid.min.js` loads properly.
   - Node labels containing special characters (parentheses, brackets, `<br/>`) MUST be double-quoted (e.g. `A["Microservices<br/>(Bounded Context)"]`) to prevent client-side parsing failures and ensure the diagram renders as a clean interactive SVG rather than raw code.

---

## Fallback Rules
- Only fall back to ripgrep (`grep_search`) or file list tools when searching for literal raw strings, config values, or non-code asset files where graph resolution is insufficient.

