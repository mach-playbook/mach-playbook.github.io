# MACH Playbook
## Modern Engineering & Architecture Knowledge Base

This repository hosts the **MACH Playbook** (`https://mach-playbook.github.io`), a professional engineering blog and reference playbook covering modern software architecture:
- **M**icroservices
- **A**PI-First
- **C**loud-Native
- **H**eadless Architecture

Built on [Jekyll](https://jekyllrb.com) using the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy/) theme, this platform is deployed automatically via GitHub Pages.

---

## 🚀 Local Development & Docker Testing

### 1. Run Unit Tests & Link Audit (HTMLProofer)
To test internal links, images, and HTML syntax inside the production-replica Docker container:

```bash
docker build --target test -t mach-playbook:test .
# OR
docker-compose run --rm test
# OR
npm test
```

### 2. Preview Production Build (Nginx Container)
To run a local web server serving the compiled static site on port `8080`:

```bash
docker-compose up site
```
Open **`http://localhost:8080`** in your browser.

### 3. Live Development Server (Hot Reload)
To run the live Jekyll dev server on port `4000`:

```bash
docker-compose up dev
```
Open **`http://localhost:4000`** in your browser.

---

## 🛠 Features & Architecture

1. **Automated IT System Header Imagery**:
   - `scripts/generate-images.js` generates topic-aware IT/System graphics (server racks, data centers, microchips, code editors) for new posts and updates frontmatter automatically via GitHub Actions.
2. **Google AdSense Compliant & E-E-A-T Optimized**:
   - 41+ deep technical posts (>1,000 words each).
   - Author profile **Lenin Meza** (`https://merolhack.github.io/`) linked in post headers.
   - Authoritative E-E-A-T credentials in `_tabs/about.md` and complete AdSense disclosures in `_tabs/privacy.md`.
3. **Automated CI/CD Deployment**:
   - Deployments managed via `.github/workflows/pages-deploy.yml`.

---

## 👤 Author
- **Lenin Meza**: [GitHub Page](https://merolhack.github.io/) | [GitHub Profile](https://github.com/merolhack) | [LinkedIn](https://www.linkedin.com/in/leninmezazarco)
