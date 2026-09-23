# Project Knowledge, LLM Wiki & Agent Guidelines (`.agents/AGENTS.md`)

This workspace uses the modular Karpathy-style `wiki/` directory ([`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md)) as its primary knowledge base and `codebase-memory-mcp` for structural graph discovery.

---

## 1. MANDATORY LLM WIKI INSTRUCTION FOR ALL AGENTS & SKILLS

- **ALWAYS CONSULT THE LLM WIKI FIRST**:
  Before starting any task, architectural research, content creation, or debugging in this repository, ALL AGENTS and SKILLS MUST consult the **LLM Wiki** ([`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md)) as the authoritative single source of truth for:
  - Repository architecture & Jekyll Chirpy theme specs ([`wiki/architecture.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/architecture.md))
  - Google AdSense policy compliance & direct async script loading rules ([`wiki/adsense-policy-and-compliance.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/adsense-policy-and-compliance.md))
  - Autonomous daily publishing pipeline, topic matrix & smart Jaccard deduplication ([`wiki/publishing-pipeline-and-deduplication.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/publishing-pipeline-and-deduplication.md))
  - Content standards & E-E-A-T editorial requirements ([`wiki/content-and-editorial-standards.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/content-and-editorial-standards.md))
  - Operational testing suites, Docker HTML-Proofer, gotchas & `codebase-memory-mcp` tools ([`wiki/tools-and-operations.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/tools-and-operations.md))

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

---

## 4. MANDATORY SECONDARY MODEL DELEGATION VIA OLLAMA MCP (`gemma4:cloud` &rarr; `qwen3:8b-8k`)

> ⚠️ **MANDATORY DIRECTIVE FOR ALL AGENTS & SESSIONS**:
> Whenever a task is routine, mechanical, or low-risk, ALL AGENTS **MUST** delegate its execution using the MCP tool `consultar_modelo_local` (`ServerName="ollama-local"`).
>
> **Model Hierarchy & Execution Logic:**
> 1. **ALWAYS use `gemma4:cloud` first** whenever there is sufficient weekly usage quota available (< 90%).
> 2. **SUBSEQUENTLY use `qwen3:8b-8k`** (local model, ~5.22 GB memory footprint, 8k context) as automatic fallback if weekly cloud quota is exhausted or if the cloud connection fails.
>
> **MCP Tool Behavior (`consultar_modelo_local`):**
> The `consultar_modelo_local` tool natively executes an automated pre-check of the weekly quota against the usage API and responds fluidly to absorb routine and mechanical tasks, eliminating primary agent token consumption and executing with minimal latency.

### Delegation Matrix:

| Task Type | Action | Execution Tool |
| :--- | :---: | :--- |
| **Docstrings, Comments & Type Annotations** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **Simple Code Boilerplate & Repetitive Formatting** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **Basic Markdown Formatting, Clean-up & Regex** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **Quick Mechanical Text/Summary Translations** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **Isolated Question Answering (No Multi-file Context)** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **Routine Data Transformations & Dictionaries/Mappings** | **MUST DELEGATE** | `ollama-local` &rarr; `consultar_modelo_local` (`gemma4:cloud` &rarr; `qwen3:8b-8k`) |
| **High-level System Architecture & Technical Design** | **DO NOT DELEGATE** | Primary Reasoning Agent (Antigravity) |
| **Multi-file Refactoring & Dependency Management** | **DO NOT DELEGATE** | Primary Reasoning Agent (Antigravity) |
| **Git Operations, CI/CD Pipeline & Deployment Workflows** | **DO NOT DELEGATE** | Primary Reasoning Agent (Antigravity) |
| **Critical Security, AdSense Policy & Data Integrity Tasks**| **DO NOT DELEGATE** | Primary Reasoning Agent (Antigravity) |

### Technical Specifications: Secondary Models
- **Priority 1 (Cloud)**: `gemma4:cloud` (Google DeepMind Gemma 4 31B via Ollama Cloud API; active when weekly quota < 90%)
- **Priority 2 (Local Fallback)**: `qwen3:8b-8k` (Alibaba Cloud Qwen3 8.2B dense decoder, `Q4_K_M` GGUF, ~5.22 GB memory footprint, 8,192 active context window)
- **Pre-check Quota Check**: Evaluated automatically by `consultar_modelo_local` prior to routing to cloud
- **Ollama API Endpoint**: `http://localhost:11434/v1/chat/completions`
- **MCP Bridge**: `C:\Users\lenin\Documents\AIDevelopment\ollama\ollama_mcp_server.py`

