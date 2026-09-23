# MACH Playbook LLM Wiki & Knowledge Base

> **MANDATORY DIRECTIVE FOR ALL AI AGENTS & SKILLS**:
> Always consult this Karpathy-style LLM Wiki ([`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md)) and the **codebase-memory-mcp** knowledge graph tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) as the primary, single source of truth for project architecture, coding standards, environment gotchas, deployment workflows, Core Web Vitals performance benchmarks, and E-E-A-T / AdSense compliance rules before executing tasks.

---

## 1. Wiki Navigation & Core Modules

This LLM Wiki is structured according to the [Karpathy LLM Wiki Architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) to provide structured, interconnected modular knowledge for both autonomous AI agents and human engineers.

| Document | Purpose & Key Topics |
| :--- | :--- |
| [**architecture.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/architecture.md) | High-level system architecture, Jekyll Chirpy static generator, GitHub Pages CI/CD, local multi-stage Docker environment, mobile Core Web Vitals optimizations (0.000 CLS, >90 Performance), and Spanish primary i18n architecture. |
| [**adsense-policy-and-compliance.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/adsense-policy-and-compliance.md) | Complete Google AdSense integration guide, Publisher ID `ca-pub-2700240339792942`, mandatory direct `<script async>` loading requirement, postmortem of "Low-value content" rejections, and automated compliance test suite. |
| [**publishing-pipeline-and-deduplication.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/publishing-pipeline-and-deduplication.md) | Architecture of the Autonomous Daily Blog Post Agent (`scripts/publish_daily_jekyll_post.py`), 5-pillar MACH matrix (100+ topics), smart Jaccard deduplication engine, dynamic Gemini AI topic discovery, Pillow companion WebP generation, and continuous pages deployment. |
| [**content-and-editorial-standards.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/content-and-editorial-standards.md) | E-E-A-T editorial standards, mandatory word count (>1,000 words), YAML frontmatter schema, 7 core MACH pillars, 21 technical tags, and the Content Validation Trinity (Depth, Physical Assets, Mermaid Diagrams). |
| [**tools-and-operations.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/tools-and-operations.md) | Operational playbooks, Docker testing commands (`mach-playbook:test`), compliance test scripts (`test-adsense-compliance.py`, `check-duplicates.py`), Google Search Console submissions log, secondary model delegation (`consultar_modelo_local` via `gemma4:cloud` &rarr; `qwen3:8b-8k`), known environment gotchas & solutions, and agent workflows. |
| [**sources/**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/sources/) | Directory containing raw diagnostic evidence, official AdSense notification emails (`.eml`), and compliance audit artifacts. |


---

## 2. Quick Repository Metadata

- **Repository**: `mach-playbook/mach-playbook.github.io`
- **Live Production URL**: [https://mach-playbook.github.io](https://mach-playbook.github.io)
- **Local Testing URL**: `http://localhost:8080` (via Docker `mach-playbook:prod`)
- **Primary Language**: Spanish (`lang: es`) with native English support (`lang: en`)
- **AdSense Publisher ID**: `ca-pub-2700240339792942`
- **Content Inventory**: **96 deep technical guides** (34 English, 62 Spanish)
- **AdSense Status**: **Getting ready** (Review requested on 2026-09-17 11:16 AM; ownership verified, review active)
- **Author**: Lenin Meza (`author: leninmeza`), Senior Solutions Architect & Enterprise Software Engineer
- **Codebase Memory Graph**: `home-merolhack-fl-mach-playbook` (maintained via `codebase-memory-mcp`)
