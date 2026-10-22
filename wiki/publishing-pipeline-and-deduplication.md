# Autonomous Daily Publishing Pipeline & Deduplication Engine

## 1. Pipeline Overview

- **Script**: `scripts/publish_daily_jekyll_post.py`
- **Workflow**: `.github/workflows/daily-blog-post.yml`
- **Schedule**: Daily at `13:00 UTC` (07:00 AM CDMX).
- **Core AI Model Fleet**: Google Gemini 3 fleet (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemini-flash-latest`) with autonomous local synthesis fallback when APIs are unavailable.

---

## 2. Topic Deduplication Engine & 200+ Enterprise Matrix

To avoid Google AdSense "Low-value content" violations and ensure fresh, diverse architectural coverage, `publish_daily_jekyll_post.py` employs an expanded **8-Pillar Enterprise Matrix (200 Topics)** and a 3-tier selection engine:

```mermaid
flowchart TD
    Start["Trigger Daily Workflow"] --> Scan["Scan all existing articles in _posts/"]
    Scan --> CheckMatrix{"Search 8-Pillar Enterprise Matrix (200 Topics)"}
    
    CheckMatrix -->|"Found Untackled Topic (Jaccard < 0.40)"| PickTopic["Select Topic & Pillar"]
    CheckMatrix -->|"Matrix Exhausted"| TryAI{"Gemini API Key Available?"}
    
    TryAI -->|"Yes"| AIGen["Prompt Gemini for 100% Novel 2026 Topic (Staff/Principal Persona)"]
    AIGen --> CheckAICovered{"Is AI Topic Covered? (Threshold 0.35)"}
    CheckAICovered -->|"No"| PickTopic
    CheckAICovered -->|"Yes"| AlgoFallback["Tridimensional Algorithmic Generator"]
    
    TryAI -->|"No / Quota Exhausted"| AlgoFallback
    AlgoFallback --> PickTopic
    
    PickTopic --> Generate["Generate Deep Article (>1,500 words, Zero Clichés)"]
    Generate --> AntiThinGate["Anti-Thin-Content Gate (wc -w >= 700 words)"]
    AntiThinGate --> CoverImage["Synthesize Matching Cover Image & WebP (Pillow)"]
    CoverImage --> Verify["Validate Duplicates & AdSense Compliance"]
    Verify --> Deploy["Commit & Push to main via GITHUB_TOKEN"]
    Deploy --> Summary["Emit GitHub Actions Job Summary"]
    Deploy -.->|workflow_run trigger| PagesDeploy["Trigger pages-deploy.yml (Build & Deploy to GitHub Pages)"]
```

### The 8 Enterprise Architecture Pillars (25 Topics Each = 200 Total)
1. **Microservicios & Cloud Native**: Cell-based architecture, eBPF/Cilium, Dapr, KEDA, LitmusChaos, reactive streams, multi-region active-active.
2. **API-First & Integraciones Distribuidas**: Apollo Federation v2, OpenAPI 3.1 schema validation, HMAC webhooks, gRPC/Protobuf, Event Mesh.
3. **Headless & Frontend Moderno**: Edge caching/purging, React Server Components, hybrid SSG/ISR, offline-first PWAs, WCAG 2.2 AA.
4. **Composable Commerce & Transición**: Strangler Fig on legacy ERP/monoliths, multi-acquirer checkout, distributed OMS, reverse logistics PBCs.
5. **Consistencia de Datos & Transaccionalidad Multi-SaaS**: Outbox pattern, CDC with Debezium, Vector Clocks, Read-Your-Own-Writes, dual-write prevention.
6. **Operaciones Día 2, Observabilidad & Resiliencia**: W3C TraceContext propagation, high-cardinality metrics, blameless post-mortems, error budgets.
7. **FinOps, Unit Economics & Gestión Multi-Vendor**: Cost per API call, network egress optimization, multi-vendor billing sprawl, build vs buy vs compose.
8. **Seguridad Zero Trust & AI Composable**: SPIFFE/SPIRE mTLS, OWASP API Top 10 mitigation, autonomous AI agents consuming OpenAPI/GraphQL, Turnstile bot defense.

### Jaccard Keyword Similarity & Anti-Repetition Rules
Instead of naive word matching, the engine strips common stop words and computes set similarity:

$$\text{Similarity}(A, B) = \frac{|\text{Keywords}(A) \cap \text{Keywords}(B)|}{|\text{Keywords}(A) \cup \text{Keywords}(B)|}$$

A candidate topic is rejected if:
1. Its sanitized slug matches an existing slug exactly.
2. Its keyword similarity with any existing title or slug exceeds `0.40`.
3. Banned introductory clichés are strictly forbidden (e.g., glossary definitions of MACH or repetitive title formulas like *"Estrategias de..."*).

### Tridimensional Algorithmic Fallback
When Gemini AI is offline and the static matrix is exhausted, the generator dynamically intersects:
$$\mathbf{\text{Padrón / Capacidad Core}} \times \mathbf{\text{Problema Técnico en Producción}} \times \mathbf{\text{Contexto Enterprise / Industria}}$$
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

# Standalone submission of any existing URL directly to Bing Webmaster Tools API
python3 scripts/publish_daily_jekyll_post.py --submit-url "https://mach-playbook.github.io/posts/welcome-to-mach/"
```

---

## 4. Post-Publishing Multi-Platform Syndication

Immediately following git commit and deployment, the workflow executes automated syndication via `scripts/publish_to_devto.py`.
- **Target Platform**: DEV.to REST API
- **Secret Required**: `DEVTO_API_KEY` (stored in GitHub Repository Secrets)
- **Tracking Ledger**: `.devto_synced.json`
- **Canonical Preservation**: Injects `https://mach-playbook.github.io/posts/{slug}/` ensuring 100% SEO attribution.
- **Reference**: See full specifications in [content-syndication-and-distribution.md](content-syndication-and-distribution.md).

---

## 5. Instant Indexation Engine (Bing Webmaster Tools & Microsoft Copilot)

Whenever a new technical guide is generated and saved to `_posts/`, `scripts/publish_daily_jekyll_post.py` immediately notifies the Bing Webmaster Tools REST API via `submit_post_to_bing()` for priority indexation by Bingbot and immediate grounding into Microsoft Copilot:

```mermaid
flowchart LR
    Publisher["publish_daily_jekyll_post.py"] -->|Write File| PostDisk["_posts/YYYY-MM-DD-slug.md"]
    Publisher -->|submit_post_to_bing| BingAPI["Bing Webmaster SubmitUrlBatch API"]
    BingAPI --> Bingbot["Bingbot Priority Crawler"]
    BingAPI --> Copilot["Microsoft Copilot Grounding Index"]
```

### 5.1 Endpoint & Authentication
- **Endpoint**: `POST https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey={BING_WEBMASTER_API_KEY}`
- **Authentication**: Query parameter `apikey` resolved from environment variable `BING_WEBMASTER_API_KEY` (or local `.env` fallback, or `--bing-api-key` CLI override).
- **Headers**:
  ```json
  {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 MACHPlaybookBot/1.0",
    "Content-Type": "application/json; charset=utf-8"
  }
  ```

### 5.2 Payload Structure
```json
{
  "siteUrl": "https://mach-playbook.github.io/",
  "urlList": [
    "https://mach-playbook.github.io/posts/change-data-capture-cdc-con-debezium-y-kafka-para-sincronizar-erps-legados-con-almacenes-de-lectura/"
  ]
}
```

### 5.3 Resilience & Fault Isolation
1. **Non-Blocking Operation**: Network timeouts, quota limits, or API outages emit explicit warnings (`⚠️ Warning: Bing API returned HTTP {status_code}`) without terminating or failing the publication pipeline.
2. **Missing Key Gracefulness**: If `BING_WEBMASTER_API_KEY` is not configured, the script logs an informational notice (`ℹ️ BING_WEBMASTER_API_KEY is not configured; skipping instant indexing on Bing`) and exits cleanly.
3. **Dry-Run Mode Safety**: In `--dry-run` executions, actual network submission is bypassed and logged as preview.
4. **CI/CD Secret Injection**: The repository secret `BING_WEBMASTER_API_KEY` is injected directly into `.github/workflows/daily-blog-post.yml` under the `Run Autonomous Daily Post Agent` step.


