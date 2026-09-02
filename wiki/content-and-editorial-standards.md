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
