# Autonomous Daily Publishing Pipeline & Deduplication Engine

## 1. Pipeline Overview

- **Script**: `scripts/publish_daily_jekyll_post.py`
- **Workflow**: `.github/workflows/daily-blog-post.yml`
- **Schedule**: Daily at `13:00 UTC` (07:00 AM CDMX).
- **Core AI Model Fleet**: Google Gemini 3 fleet (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemini-flash-latest`) with autonomous local synthesis fallback when APIs are unavailable.

---

## 2. Topic Deduplication Engine

To avoid Google AdSense "Low-value content" violations and ensure fresh, diverse architectural coverage, `publish_daily_jekyll_post.py` employs a 3-tier topic selection architecture:

```mermaid
flowchart TD
    Start["Trigger Daily Workflow"] --> Scan["Scan all existing articles in _posts/"]
    Scan --> CheckMatrix{"Search 100+ Static Topic Matrix"}
    
    CheckMatrix -->|"Found Untackled Topic (Jaccard < 0.45)"| PickTopic["Select Topic & Pillar"]
    CheckMatrix -->|"Matrix Exhausted"| TryAI{"Gemini API Key Available?"}
    
    TryAI -->|"Yes"| AIGen["Prompt Gemini for 100% Novel 2026 Topic"]
    AIGen --> CheckAICovered{"Is AI Topic Covered?"}
    CheckAICovered -->|"No"| PickTopic
    CheckAICovered -->|"Yes"| AlgoFallback["Combinatorial Algorithmic Generator"]
    
    TryAI -->|"No / Quota Exhausted"| AlgoFallback
    AlgoFallback --> PickTopic
    
    PickTopic --> Generate["Generate Deep Article (>1,200 words)"]
    Generate --> AntiThinGate["Anti-Thin-Content Gate (wc -w >= 700 words)"]
    AntiThinGate --> CoverImage["Synthesize Matching Cover Image & WebP (Pillow)"]
    CoverImage --> Verify["Validate Duplicates & AdSense Compliance"]
    Verify --> Deploy["Commit & Push to main via GITHUB_TOKEN"]
    Deploy --> Summary["Emit GitHub Actions Job Summary"]
    Deploy -.->|workflow_run trigger| PagesDeploy["Trigger pages-deploy.yml (Build & Deploy to GitHub Pages)"]
```

### Jaccard Keyword Similarity Algorithm
Instead of naive word matching (which falsely rejected topics sharing common engineering terms like "microservicios" or "arquitecturas"), the engine strips common stop words and computes set similarity:

$$\text{Similarity}(A, B) = \frac{|\text{Keywords}(A) \cap \text{Keywords}(B)|}{|\text{Keywords}(A) \cup \text{Keywords}(B)|}$$

A candidate topic is rejected if:
1. Its sanitized slug matches an existing slug exactly.
2. Its keyword similarity with any existing title or slug exceeds `0.45`.

### Combinatorial Algorithmic Fallback
When Gemini AI is offline and the static matrix is exhausted, the generator combines:
- **Patterns**: Cell-Based Architecture, Dapr Runtime, eBPF, Event Sourcing, CQRS, GraphQL Federation v2, AsyncAPI, OAuth 2.1 Passkeys, Edge Middleware, Platform Engineering.
- **Contexts**: Sistemas de Alta Concurrencia, Transacciones Transfronterizas, Plataformas E-Commerce Global, Prevención de Fraude, Reducción de Latencia p99.
- **Rule**: Every combination is dynamically checked against all historical posts. The hardcoded repetitive string `Edición YYYYMMDD` is **strictly prohibited**.

---



### CI/CD Deployment Automation & Continuous Pages Delivery
To prevent production freeze and ensure every article is immediately available to search engine and AdSense crawlers:
1. **Pillow Dependency**: Declared in `requirements.txt` (`Pillow>=10.0.0`) so CI runners never fail during WebP companion generation.
2. **Anti-Thin-Content Quality Gate**: The publishing workflow checks `wc -w < 700` before git commit; thin articles are blocked with `exit 1`.
3. **Automated `workflow_run` Trigger**: `.github/workflows/pages-deploy.yml` listens for `completed` events from `Autonomous Daily Blog Post Agent`. This bypasses GitHub's default recursive trigger block on `GITHUB_TOKEN` pushes, ensuring that Jekyll automatically compiles and deploys each daily post to GitHub Pages.
4. **Job Summary Observability**: Each execution logs a Markdown report into the GitHub Actions run summary displaying the published post slug, date, and URL.

---

## 3. Workflow CLI Usage

Run dry-run tests locally without modifying git:
```bash
# Dry run with automatic topic selection
python3 scripts/publish_daily_jekyll_post.py --dry-run

# Force a specific manual topic
python3 scripts/publish_daily_jekyll_post.py --topic "eBPF y Cilium en Arquitecturas Cloud-Native" --dry-run

# Run with custom language
python3 scripts/publish_daily_jekyll_post.py --lang en --dry-run
```
