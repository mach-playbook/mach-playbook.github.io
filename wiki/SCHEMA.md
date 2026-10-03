# MACH Playbook Wiki Schema Specification

> This document defines the structural rules, editorial conventions, and ingestion protocol for the MACH Playbook knowledge base, strictly adhering to the [Karpathy LLM Wiki Architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## 1. The Three Architectural Layers

The wiki maintains a strict three-tier information hierarchy:

```
wiki/
├── sources/                           <-- Tier 1: Raw, immutable evidence & external documents
│   ├── You need to fix some issues...eml
│   └── karpathy-llm-wiki-gist.md
├── [topic-name].md                    <-- Tier 2: Interlinked, compounding knowledge topics
│   ├── architecture.md
│   ├── ui-ux-design-system-and-testing.md
│   ├── contact-and-formspree-architecture.md
│   ├── adsense-policy-and-compliance.md
│   ├── publishing-pipeline-and-deduplication.md
│   ├── content-and-editorial-standards.md
│   └── tools-and-operations.md
├── SCHEMA.md                          <-- Tier 3: Structural contracts & editorial guidelines
├── index.md                           <-- Tier 3: Thematic catalog of all topics with 1-line summaries
└── log.md                             <-- Tier 3: Chronological, append-only changelog / ledger
```

### Layer 1: Raw Sources (`wiki/sources/`)
- Contains immutable artifacts: email records (`.eml`), vendor guidelines, API schemas, external specs, and raw audit exports.
- **Rule**: Never edit raw source files once placed in `sources/`. They serve as immutable primary evidence.

### Layer 2: The Wiki Core (`wiki/*.md`)
- Modular markdown documents focused on a single architectural domain or operational discipline.
- Synthesized and maintained by AI agents and engineers as a **compounding artifact**.
- **Rule**: Every page must be cross-referenced with related pages and indexed in `wiki/index.md`.

### Layer 3: System Registry (`SCHEMA.md`, `index.md`, `log.md`)
- `SCHEMA.md` (this file): Canonical structural specification.
- `index.md`: Fast, thematic catalog for human and LLM navigation.
- `log.md`: Append-only chronological ledger tracking all ingestions, updates, and architectural decisions.

---

## 2. Formatting & Editorial Conventions

1. **File Naming**:
   - Lowercase kebab-case only (e.g., `ui-ux-design-system-and-testing.md`).
   - Suffix must always be `.md`.

2. **Heading Hierarchy**:
   - Exactly one `# Level 1 Heading` per file at the top.
   - Logical sequential nesting: `## Level 2` for major modules, `### Level 3` for subsections. Never skip heading levels.

3. **Hyperlinking Standards**:
   - All internal references must use valid markdown links with either relative paths (`[architecture](architecture.md)`) or standard workspace URIs.
   - External URLs must point to canonical upstream documentation.

4. **Code & Configuration Blocks**:
   - All code snippets must declare their language explicitly (e.g., ````html````, ````css````, ````python````, ````bash````).
   - Shell commands must be executable as presented without hidden environment assumptions.

5. **Tables & Benchmarks**:
   - Tables must include clear header columns and aligned delimiters for rapid scanning.
   - Metrics and scores must include baseline vs. optimized numbers and verification timestamps.

---

## 3. Ingestion Protocol

When an agent or engineer finishes a technical session, resolves an issue, or adds capabilities:

1. **Synthesize, Don't Dump**:
   - Extract lessons, root causes, bug fixes, benchmarks, and architectural designs.
   - Update existing domain pages if the topic already has a home.
   - Create a new topic page if the concept represents a substantial new domain (e.g., automated testing, contact subsystem).

2. **Append to `wiki/log.md`**:
   - Must use the machine-parseable entry format:
     ```markdown
     ## [YYYY-MM-DD] <action> | <Title>

     - **Impacted Files**: `file1`, `file2`
     - **Summary**: Concise bullet points explaining the problem, root cause, and technical solution.
     ```
   - Standard actions: `feat`, `fix`, `perf`, `test`, `audit`, `ingest`, `refactor`.

3. **Synchronize `wiki/index.md`**:
   - If a new page was created, add a row to the master catalog table with a concise 1-line purpose summary.
   - Update repository statistics and inventory metrics.

4. **Unix Verification**:
   - Ensure `grep "^## \[" wiki/log.md` produces a clean, parseable audit trail.
