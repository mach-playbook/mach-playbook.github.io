# MACH Playbook LLM Wiki & Knowledge Base

> **MANDATORY DIRECTIVE FOR ALL AI AGENTS & SKILLS**:
> Always consult this Karpathy-style LLM Wiki ([`wiki/index.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/index.md)) and the **codebase-memory-mcp** knowledge graph tools (`search_graph`, `trace_path`, `get_code_snippet`, `get_architecture`, `query_graph`) as the primary, single source of truth for project architecture, coding standards, environment gotchas, deployment workflows, Core Web Vitals performance benchmarks, and E-E-A-T / AdSense compliance rules before executing tasks.

---

## 1. Wiki Navigation & Core Modules

This LLM Wiki is structured according to the [Karpathy LLM Wiki Architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) to provide structured, interconnected modular knowledge for both autonomous AI agents and human engineers.

| Document | Purpose & Key Topics |
| :--- | :--- |
| [**SCHEMA.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/SCHEMA.md) | Canonical structural specification, 3-tier architectural layering (`sources/`, topic pages, registry), markdown formatting standards, and ingestion protocol. |
| [**log.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/log.md) | Chronological append-only ledger tracking all knowledge ingestions, technical fixes, and architectural decisions. Parseable via `grep "^## \[" wiki/log.md`. |
| [**architecture.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/architecture.md) | High-level system architecture, Jekyll Chirpy static generator, GitHub Pages CI/CD, local multi-stage Docker environment, mobile Core Web Vitals optimizations (0.000 CLS, >90 Performance), Spanish primary i18n architecture, and Google Analytics 4 (GA4) telemetry. |
| [**ui-ux-design-system-and-testing.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/ui-ux-design-system-and-testing.md) | Complete design system and testing specification: post hero 100% width layout, postmortem of the rogue 41.6% Bootstrap collision, 2-column pure CSS categories masonry, hybrid in-article TOC, dark-mode Mermaid overrides, and 3-tier automated testing pyramid (Unit, BDD, E2E). |
| [**contact-and-formspree-architecture.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/contact-and-formspree-architecture.md) | Serverless Jamstack contact architecture, Formspree endpoint `https://formspree.io/f/xoevgrqq`, silent honeypot anti-spam defense (`_gotcha`), async AJAX JSON feedback loop, and graceful degradation. |
| [**adsense-policy-and-compliance.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/adsense-policy-and-compliance.md) | Complete Google AdSense integration guide, Publisher ID `ca-pub-2700240339792942`, mandatory direct `<script async>` loading requirement, postmortem of "Low-value content" rejections, and automated compliance test suite. |
| [**publishing-pipeline-and-deduplication.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/publishing-pipeline-and-deduplication.md) | Architecture of the Autonomous Daily Blog Post Agent (`scripts/publish_daily_jekyll_post.py`), 5-pillar MACH matrix (100+ topics), smart Jaccard deduplication engine, dynamic Gemini AI topic discovery, Pillow companion WebP generation, and continuous pages deployment. |
| [**content-and-editorial-standards.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/content-and-editorial-standards.md) | E-E-A-T editorial standards, mandatory word count (>1,000 words), YAML frontmatter schema, 7 core MACH pillars, 21 technical tags, and the Content Validation Trinity (Depth, Physical Assets, Mermaid Diagrams). |
| [**content-syndication-and-distribution.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/content-syndication-and-distribution.md) | Multi-platform developer distribution architecture: DEV.to REST API engine (`scripts/publish_to_devto.py`), 100% canonical SEO protection, adaptive rate limit backoff (HTTP 429), 117-post historical backfill ledger (`.devto_synced.json`), daily.dev Squad (`machplaybook`) curation, Hashnode paywall postmortem, and CI/CD secret scoping. |
| [**tools-and-operations.md**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/tools-and-operations.md) | Operational playbooks, Docker testing commands (`mach-playbook:test`), compliance test scripts (`test-adsense-compliance.py`, `check-duplicates.py`, `test-ui-components.py`, `test-bdd-specs.py`, `test-e2e-browser.py`), Google Search Console submissions log, Google Analytics 4 (GA4) setup assistant protocol, secondary model delegation (`consultar_modelo_local` via `gemma4:cloud` -> `qwen3:8b-8k`), known environment gotchas & solutions, and agent workflows. |
| [**sources/**](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/wiki/sources/) | Directory containing raw diagnostic evidence, official AdSense notification emails (`.eml`), and compliance audit artifacts. |

---

## 2. Quick Repository Metadata

- **Repository**: `mach-playbook/mach-playbook.github.io`
- **Live Production URL**: [https://mach-playbook.github.io](https://mach-playbook.github.io)
- **Local Testing URL**: `http://localhost:8080` (via Docker `mach-playbook:prod`)
- **Primary Language**: Spanish (`lang: es`) with native English support (`lang: en`)
- **AdSense Publisher ID**: `ca-pub-2700240339792942`
- **Google Analytics 4 (GA4)**: Property ID `531281877` | Measurement ID `G-98D95S3VXX` | Stream ID `14312315619`
- **Content Inventory**: **117 deep technical guides** (34 English, 83 Spanish)
- **Multi-Platform Distribution**:
  - **DEV.to**: 117 / 117 articles live with `<link rel="canonical">` protection (`@merolhack`)
  - **daily.dev Squad**: Live at [https://daily.dev/squads/machplaybook](https://daily.dev/squads/machplaybook)
- **Interactive Tools**: MACH Architecture Maturity Evaluator & TCO Simulator live at [`/tools/`](https://mach-playbook.github.io/tools/)
- **Automated Test Pyramid**: 8 Automated Test Suites (HTML-Proofer, AdSense Policy, Duplicate Detector, Site Integrity, Topic Generator, UI Components, BDD Specs, E2E Browser)
- **AdSense Status**: Review limit cooldown active until **October 14, 2026** (Remediated: interactive utility hub added + external distribution live)
- **Author**: Lenin Meza (`author: leninmeza`), Senior Solutions Architect & Enterprise Software Engineer
- **Codebase Memory Graph**: `home-merolhack-fl-mach-playbook` (maintained via `codebase-memory-mcp`)

