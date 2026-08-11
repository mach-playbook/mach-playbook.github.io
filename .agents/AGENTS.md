# Project Knowledge, LLM Wiki & Agent Guidelines (`.agents/AGENTS.md`)

This workspace uses `llm-wiki.md` as its primary Karpathy-style knowledge base and `codebase-memory-mcp` for structural graph discovery.

---

## 1. MANDATORY LLM WIKI INSTRUCTION FOR ALL AGENTS & SKILLS

- **ALWAYS CONSULT `llm-wiki.md` FIRST**:
  Before starting any task, architectural research, content creation, or debugging in this repository, ALL AGENTS and SKILLS MUST consult [`llm-wiki.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/llm-wiki.md) as the authoritative single source of truth for:
  - Repository architecture & Jekyll Chirpy theme specs
  - Bilingual post classification (`lang: es` and `lang: en`) & frontmatter rules
  - Google AdSense policy compliance requirements & automated testing (`scripts/test-adsense-compliance.py`)
  - Automated image pipeline (`scripts/generate-images.js`)
  - Multi-stage Docker test environment & CI/CD deployment rules
  - Environment gotchas & resolutions

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

## Fallback Rules
- Only fall back to ripgrep (`grep_search`) or file list tools when searching for literal raw strings, config values, or non-code asset files where graph resolution is insufficient.
