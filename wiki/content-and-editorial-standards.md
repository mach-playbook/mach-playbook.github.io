# Content & Editorial Standards (E-E-A-T)

## 1. Editorial Quality Guidelines (E-E-A-T)

All articles published on **MACH Playbook** represent Senior Solutions Architect-level technical deep-dives. Every article must embody:

- **Experience & Expertise**: Real-world architectural trade-offs, performance benchmarks, and concrete failure scenarios (not textbook overviews).
- **Authoritativeness**: Production-grade code snippets (Go, TypeScript, Python, SQL, YAML), sequence diagrams, and architecture blueprints.
- **Trustworthiness**: Explicit author attribution, transparent disclaimers, cookie tracking notices, and reproducible examples.

---

## 2. Article Structural Requirements

Every post in `_posts/YYYY-MM-DD-slug.md` MUST comply with:

1. **Word Count**: Strictly **>1,000 words** (recommended 1,200–2,000 words) to avoid "thin content" flags.
2. **Jekyll Front Matter**:
   ```yaml
   ---
   layout: post
   title: "Descriptive, Professional Title"
   date: YYYY-MM-DD 09:00:00 -0600
   lang: es # or 'en'
   categories: [Primary Category, Subcategory]
   tags: [tag1, tag2, tag3, tag4, tag5, tag6]
   image:
     path: /assets/img/posts/YYYY-MM-DD-slug.png
   ---
   ```
3. **Mermaid Diagrams**: Include at least one vector architecture or sequence diagram in Mermaid syntax:
   ```mermaid
   graph TD
       Client --> Gateway
       Gateway --> Service
   ```
   > *Note*: When diagrams are included, set `mermaid: true` in the post frontmatter to enable dynamic client-side rendering.
4. **Companion WebP Assets**:
   For every PNG in `assets/img/posts/<slug>.png`, a corresponding `<slug>.webp` file must exist to satisfy Jekyll Chirpy's responsive image template and `HTML-Proofer`. Run `python3 scripts/generate-webp-images.py` after creating new images.
5. **Code Snippets**: Documented, production-grade code illustrating patterns like Outbox, Circuit Breaker, Token Bucket, or JWT validation.
6. **Trade-Off Table**: Comparative table analyzing Pros, Cons, When to Use, and When to Avoid.

---

## 3. Taxonomy & Category Architecture

Following the August 14 taxonomy consolidation to eliminate crawl bloat (preventing "low value navigation" algorithms in Googlebot):

### A. The 7 Core MACH Pillars
1. `Architecture` / `Arquitectura Cloud` (Microservices, DDD, System Boundaries)
2. `Microservices` / `Microservicios` (Sagas, CQRS, Circuit Breaking, Service Mesh)
3. `API Design` / `Diseño de APIs` (OpenAPI, GraphQL, REST, gRPC, Rate Limiting, Versioning)
4. `DevOps & CI/CD` / `Automatización` (Docker, Kubernetes, GitHub Actions, Blue/Green)
5. `Headless & Frontend` / `Desarrollo Web` (Next.js, Supabase, Edge CDN, Core Web Vitals)
6. `Security & Observability` / `Seguridad & Observabilidad` (OAuth2, JWT, Zero-Trust, OpenTelemetry)
7. `Data Engineering & Distributed SQL` / `Bases de Datos` (PostgreSQL, Distributed SQL, Databricks, AI)

### B. The 21 High-Density Technical Tags
`cloud-native`, `microservices`, `architecture`, `headless`, `api-first`, `devops`, `gcp`, `data-engineering`, `qa-automation`, `distributed-systems`, `postgresql`, `observability`, `ci-cd`, `finops`, `security`, `ai-engineering`, `aws`, `event-driven`, `telecom`, `kubernetes`, `nextjs`.

---

## 4. Mandatory Content Validation Trinity (Antigravity IDE & GitHub Actions)

Whenever new content is generated—whether in **Antigravity IDE pair-programming sessions** or via the **autonomous GitHub Actions workflow (`daily-blog-post.yml`)**—the agent/system MUST always execute and verify the **Three Pillars of Content Integrity**:

1. **Content Depth & E-E-A-T Quality Gate**:
   - Article word count must exceed **>800–1,500 words** with actionable architectural analysis, trade-off matrices, and failure modes.
   - Front matter must have valid taxonomy (`layout: post`, `title`, `date`, `lang: es` or `lang: en`, approved `categories`, structured `tags`, `image`).
   - Zero duplicates in title or body content (`scripts/check-duplicates.py`).
   - 100% PASS on `scripts/test-adsense-compliance.py`.

2. **Cover Image Physical Asset Verification**:
   - Every post must resolve an explicit cover image in `image.path` pointing to `/assets/img/posts/<date-slug>.webp` or `.png`.
   - The image file must physically exist in `assets/img/posts/`, match IT/cloud architectural themes, and load with HTTP 200 without 404s.

3. **Mermaid Diagram Syntax & On-Demand Rendering**:
   - Posts containing diagrams must use valid Mermaid syntax (```` ```mermaid ````).
   - Node labels containing special characters (parentheses, brackets, `<br/>`) MUST be double-quoted (e.g. `A["Microservices<br/>(Bounded Context)"]`).
   - `mermaid: true` must be enabled in frontmatter so Mermaid.js loads and renders interactive vector SVG diagrams.

