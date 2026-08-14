# MACH Playbook (`mach-playbook.github.io`)

[![Build and Deploy](https://github.com/mach-playbook/mach-playbook.github.io/actions/workflows/pages-deploy.yml/badge.svg)](https://github.com/mach-playbook/mach-playbook.github.io/actions/workflows/pages-deploy.yml)
[![Docker Test](https://img.shields.io/badge/Docker-HTMLProofer%20Passing-brightgreen)](https://github.com/mach-playbook/mach-playbook.github.io)
[![AdSense Test Suite](https://img.shields.io/badge/AdSense-100%25%20Verified-blue)](https://mach-playbook.github.io)
[![AdSense Approval Status](https://img.shields.io/badge/AdSense%20Status-Getting%20Ready-yellow)](https://adsense.google.com/)

An enterprise-grade architectural engineering blog and technical playbook dedicated to **MACH** (**M**icroservices, **A**PI-First, **C**loud-Native, **H**eadless) architectures, cloud multi-cloud strategies (GCP, AWS), API management (Apigee, MuleSoft), ERP integrations, Next.js/Supabase serverless edge architectures, OpenSIPS VoIP security routing, YugabyteDB distributed SQL, local graph database indexing for AI IDEs in WSL, and database administration (RDS to Cloud SQL).

Created and authored by **[Lenin Meza](https://merolhack.github.io/)** ([LinkedIn](https://www.linkedin.com/in/leninmezazarco) | [GitHub](https://github.com/merolhack)).

---

## 📖 Primary Source of Knowledge (`llm-wiki.md`)

> **IMPORTANT**: All AI Agents and Developers MUST consult [`llm-wiki.md`](file:///ubuntu-20.04/home/merolhack/fl/mach-playbook/llm-wiki.md) as the authoritative Karpathy-style knowledge base for project architecture, coding standards, environment gotchas, deployment workflows, and E-E-A-T / AdSense compliance rules.

---

## 🚀 Key Features

- **62 Deep Technical Guides**: 34 English and 28 Spanish long-form articles (>1,000 words each) covering microservices, domain-driven design, API gateways, YugabyteDB distributed SQL, local graph database indexing in WSL, Playwright + Ollama QA, headless CMS, Next.js/Supabase, OpenSIPS VoIP security, CFDI digital signatures, Cloud Run Blue/Green deployments, Event-Driven architectures, Zero Trust Apigee/mTLS, AWS RDS to GCP Cloud SQL migrations, VoIP call tracing, FinOps, and Kubernetes.
- **100% Unique Content**: Verified with `scripts/check-duplicates.py` (**0% title duplication, 0% body duplication**).
- **🌐 Interactive Language Selector**: Global Topbar dropdown (`🌐 All | 🇲🇽/🇪🇸 Español | 🇺🇸 English`) and Home Feed Filter Pills with instant Vanilla JS client-side filtering and `localStorage` preference persistence.
- **🎨 Topic-Aware IT Image Generation**: Automated image pipeline (`scripts/generate-images.js`) backed by Pollinations AI and a curated pool of 46+ high-resolution Unsplash IT graphics mapped by post index.
- **🛡️ Automated AdSense Compliance Suite**: `scripts/test-adsense-compliance.py` verifies Publisher ID (`ca-pub-2700240339792942`), `ads.txt`, `<head>` verification, E-E-A-T credentials, word counts, and language metadata.
- **🤖 Registered Agent Workflows**: Custom AI Agent skills in `.agents/skills/` for automated post creation, testing, deployment (`add-new-post-test-deploy`) and Search Console URL Inspection & Indexing (`gsc-manual-url-submission`).
- **🐳 Multi-Stage Docker CI/CD**: Local Docker Desktop environment matching GitHub Actions CI/CD for unit testing (`HTMLProofer`) and production serving via Nginx.

---

## 🛠️ Repository & Tooling Structure

```text
.
├── _posts/                    # 62 Technical Markdown articles (35 EN, 28 ES)
├── .agents/
│   ├── AGENTS.md              # AI Agent operational guidelines & LLM Wiki mandate
│   └── skills/                # Registered AI Agent Skill Workflows
│       ├── add-new-post-test-deploy/  # Post creation, compliance & deployment skill
│       └── gsc-manual-url-submission/ # GSC URL extraction & indexing submission skill
├── _includes/
│   ├── head.html              # Custom head override with AdSense & SEO tags
│   └── topbar.html            # Topbar override with Global Language Selector
├── _layouts/
│   ├── home.html              # Home layout override with Language Filter Pills
│   └── post.html              # Post layout override with flag badges
├── assets/
│   ├── js/lang-filter.js      # Client-side language filtering engine
│   └── img/posts/             # Generated post cover graphics
├── scripts/
│   ├── test-adsense-compliance.py # Automated AdSense E-E-A-T policy compliance suite
│   ├── generate-images.js     # Unsplash & Pollinations AI image generator
│   ├── check-duplicates.py    # Automated similarity & duplicate checker
│   └── list-urls.py           # Sitemap XML URL extractor utility
├── Dockerfile                 # Multi-stage Dockerfile (builder, test, dev, prod)
├── docker-compose.yml         # Container orchestration configuration
├── _config.yml                # Jekyll site configuration
├── sitemap.xml                # Automated site map index (331 URLs)
├── robots.txt                 # Search engine crawler instructions
├── llm-wiki.md                 # Karpathy-style LLM Wiki knowledge base (Primary Single Source of Truth)
├── AGENTS.md                  # Comprehensive AI Agent operational log
└── HISTORY.txt                # Chronological development history
```

---

## 🧪 Testing & Verification Commands

### 1. Execute AdSense Policy Compliance Suite
```bash
python3 scripts/test-adsense-compliance.py
```

### 2. Execute Docker HTMLProofer Unit Tests
Run the test stage to validate all 331 HTML files and 729 internal links:

```bash
docker build --target test -t mach-playbook:test .
```

### 3. Launch Local Production Replica
Run the Nginx production container listening on `http://localhost:8080`:

```bash
docker rm -f mach-playbook-site
docker build -t mach-playbook:prod .
docker run -d --name mach-playbook-site -p 8080:80 mach-playbook:prod
```

Access the site locally at **`http://localhost:8080`**.

---

## 📜 License & Copyright

© 2026 **Lenin Meza**. Built with the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme for [Jekyll](https://jekyllrb.com/).
