# MACH Playbook (`mach-playbook.github.io`)

[![Build and Deploy](https://github.com/mach-playbook/mach-playbook.github.io/actions/workflows/pages-deploy.yml/badge.svg)](https://github.com/mach-playbook/mach-playbook.github.io/actions/workflows/pages-deploy.yml)
[![Docker Test](https://img.shields.io/badge/Docker-HTMLProofer%20Passing-brightgreen)](https://github.com/mach-playbook/mach-playbook.github.io)
[![AdSense Verified](https://img.shields.io/badge/Google%20AdSense-Verified%20ca--pub--2700240339792942-blue)](https://mach-playbook.github.io)

An enterprise-grade architectural engineering blog and technical playbook dedicated to **MACH** (**M**icroservices, **A**PI-First, **C**loud-Native, **H**eadless) architectures, cloud multi-cloud strategies (GCP, AWS), API management (Apigee, MuleSoft), ERP integrations, and VoIP/SIP infrastructure.

Created and authored by **[Lenin Meza](https://merolhack.github.io/)** ([LinkedIn](https://www.linkedin.com/in/leninmezazarco) | [GitHub](https://github.com/merolhack)).

---

## 🚀 Key Features

- **43 Deep Technical Guides**: 35 English and 8 Spanish long-form articles (>1,000 words each) covering microservices, domain-driven design, API gateways, headless CMS, Salesforce Data Cloud, AI system skills, FinOps, and Kubernetes.
- **100% Unique Content**: Verified with `scripts/check-duplicates.py` (**0% title duplication, 0% body duplication**).
- **🌐 Interactive Language Selector**: Global Topbar dropdown (`🌐 All | 🇲🇽/🇪🇸 Español | 🇺🇸 English`) and Home Feed Filter Pills with instant Vanilla JS client-side filtering and `localStorage` preference persistence.
- **🎨 Topic-Aware IT Image Generation**: Automated image pipeline (`scripts/generate-images.js`) backed by Pollinations AI and a curated pool of 46+ high-resolution Unsplash IT graphics mapped by post index.
- **🐳 Multi-Stage Docker CI/CD**: Local Docker Desktop environment matching GitHub Actions CI/CD for unit testing (`HTMLProofer`) and production serving via Nginx.
- **💰 Google AdSense & E-E-A-T Compliant**: Includes `ca-pub-2700240339792942` integration, `ads.txt`, GDPR/CCPA cookie disclosures, and explicit author attribution.

---

## 🛠️ Repository & Tooling Structure

```text
.
├── _posts/                    # 43 Technical Markdown articles (35 EN, 8 ES)
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
│   ├── generate-images.js     # Unsplash & Pollinations AI image generator
│   ├── check-duplicates.py    # Automated similarity & duplicate checker
│   └── make-remaining-english-unique.py # Bulk unique content writer
├── Dockerfile                 # Multi-stage Dockerfile (builder, test, dev, prod)
├── docker-compose.yml         # Container orchestration configuration
├── _config.yml                # Jekyll site configuration
├── sitemap.xml                # Automated site map index (240 URLs)
├── robots.txt                 # Search engine crawler instructions
├── llms.txt                   # LLM Wiki knowledge base (GitHub Markdown)
├── AGENTS.md                  # Comprehensive AI Agent operational log
└── HISTORY.txt                # Chronological development history
```

---

## 🐳 Running Locally with Docker Desktop

### 1. Execute Unit Tests (`HTMLProofer`)
Run the test stage to validate all 241 HTML files and 555 internal links:

```bash
docker build --target test -t mach-playbook:test .
```

### 2. Launch Local Production Replica
Run the Nginx production container listening on `http://localhost:8080`:

```bash
docker rm -f mach-playbook-site
docker build -t mach-playbook:prod .
docker run -d --name mach-playbook-site -p 8080:80 mach-playbook:prod
```

Access the site locally at **`http://localhost:8080`**.

---

## 🌐 Language Filtering System

The site supports bilingual post classification (`lang: es` and `lang: en`):

- **Topbar Dropdown**: Access `🌐 Language` next to the search bar on any page.
- **Home Filter Pills**: Select `All (43)`, `🇲🇽/🇪🇸 Español (8)`, or `🇺🇸 English (35)` directly above the post list.
- **Persistence**: User selection is saved to `localStorage.setItem('mach_playbook_lang', lang)` and applied automatically across page navigation.

---

## 📜 License & Copyright

© 2026 **Lenin Meza**. Built with the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme for [Jekyll](https://jekyllrb.com/).
