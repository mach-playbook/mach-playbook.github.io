# Codebase Knowledge Graph & Agent Guidelines (codebase-memory-mcp)

This workspace uses `codebase-memory-mcp` to build and maintain a structural knowledge graph of the repository.

## MANDATORY AGENT INSTRUCTIONS FOR CODEBASE MEMORY

1. **ALWAYS Query the Knowledge Graph First**:
   - Before performing broad searches, reading large files, or running grep across the repository, ALWAYS use `codebase-memory` MCP tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) to query the knowledge graph.

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
