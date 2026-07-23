2026-04-04 18:58: Phase 4 configuration completed
- Edited _config.yml with site details, dark mode, github repo/username and giscus comments.
- Added _tabs/about.md with customized description.
- Created _tabs/privacy.md for future AdSense application logic.

2026-04-04 19:12: Phase 5 progression
- Programmatically extracted dates and copied 34 Markdown posts to _posts/.
- Formatted post names with date-prefix to follow Jekyll's naming convention.
- Created _includes/head.html template with AdSense placeholder script.
- Waiting for user to configure Giscus repo_id and category_id.

2026-04-05 13:00: Phase 6 Automation Complete
- Modified Auto-Generate Image script to use unmetered Pollinations AI instead of Gemini Free due to Google account block.
- Pushed workflow to dynamically synthesize frontmatter images for all 34 posts natively.
- Scaffolded scalable vector mapping (`avatar.svg`).
- Un-commented and activated Google AdSense ID linking via custom headers and injected `ads.txt`.

2026-07-13 21:39: Sidebar Layout & GitHub Link Fix
- Fixed sidebar navigation menu overlap caused by multiline site subtitle (`height: 3rem` overridden to `height: auto !important` in `_includes/head.html`).
- Updated GitHub logo/profile links to `https://github.com/merolhack` in `_config.yml` and `_data/contact.yml`.

2026-07-22 19:00: AdSense E-E-A-T & Thin Content Resolution
- Identified Google AdSense "Low value content" violation.
- Developed `scripts/deep-expand-posts.py` to programmatically rewrite 34 thin Markdown posts.
- Expanded all posts to >1,100 words using advanced architectural insights (GCP, AWS, MuleSoft, Apigee, Event-driven architectures) ensuring Senior Solutions Architect tone, while preserving YAML frontmatter and AI image automation.
- Deepened E-E-A-T trust signals by updating `_tabs/about.md` with explicit professional credentials.
- Updated `_tabs/privacy.md` to explicitly comply with Google AdSense cookie tracking and opt-out policies.
- Verified `_data/contact.yml` accurately points to the `merolhack` GitHub profile.
- Encountered a GitHub CLI authentication gotcha: Windows `gh` fails due to an invalid `GITHUB_TOKEN` environment variable in PowerShell overriding valid keyring credentials. Executing `wsl gh` bypasses this environment variable and successfully utilizes the `hosts.yml` valid token.

2026-07-23 03:30: Author Attribution & Sidebar LinkedIn Integration
- Configured `_data/authors.yml` and `_config.yml` social metadata for author **Lenin Meza** (`author: leninmeza`), linking post author titles to `https://merolhack.github.io/`.
- Updated `_data/contact.yml` with LinkedIn profile (`https://www.linkedin.com/in/leninmezazarco`) rendering FontAwesome `fab fa-linkedin` in the sidebar footer.
- Overhauled image generator (`scripts/generate-images.js`) to strictly produce IT, server, microchip, data center, and code editor graphics, eliminating landscape fallbacks.

2026-07-23 06:12: E-E-A-T Spanish Articles & Sitemap Fix
- Published 4 comprehensive Spanish-language technical posts: `orquestacion-mach-multi-nube.md`, `infraestructura-voip-cloud-native.md`, `arquitectura-api-first-erpnext.md`, and `finops-desmantelamiento-gcp.md`.
- Solved Jekyll future post exclusion gotcha where posts were omitted from build/sitemap due to UTC timezone offsets by adding `future: true` in `_config.yml` and adjusting date timestamps.
- Verified all 39 posts are indexed in the live `sitemap.xml`.

2026-07-23 21:51: Docker Desktop Testing Environment & AI QA Articles
- Published 2 additional Spanish-language technical posts: `automatizacion-inteligente-playwright-ollama.md` and `flujos-hibridos-wsl-powershell-windows.md`. Total posts: **41**.
- Created multi-stage `Dockerfile`, `docker-compose.yml`, `.dockerignore`, and npm scripts to replicate GitHub Pages CI/CD locally (Ruby 3.4, Jekyll Chirpy, HTMLProofer, Nginx).
- Verified HTMLProofer unit tests in Docker on 101 files / 193 links with 0 errors (`HTML-Proofer finished successfully`).
- Started background production replica container `mach-playbook-site` listening on `http://localhost:8080` (HTTP 200 OK).
- Verified GitHub Actions `Build and Deploy` and `Auto Generate Missing Post Images` pipelines completed with `completed | success`.
