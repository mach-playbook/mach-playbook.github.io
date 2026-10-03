# UI/UX Design System, Responsive Layouts & Multi-Tier Testing Architecture

> **MANDATORY SPECIFICATION**:  
> Governs all layout modifications, responsive grid behaviors, typography standards, Zero-CLS constraints, and the automated 3-tier testing framework (Unit, BDD, E2E) across the MACH Playbook platform.

---

## 1. Executive Summary & Design System Principles

The MACH Playbook frontend combines the static performance of [Jekyll Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) with enterprise-grade responsive layouts, high-contrast dark mode aesthetics, and zero layout shift.

### Core Visual & Functional Directives
1. **Zero Cumulative Layout Shift (0.000 CLS)**: All visual assets (hero images, card previews, diagrams) must possess explicit dimensional aspect ratios or container reservations before paint.
2. **Space Utilization without Dead White Space**: Category and index listings utilize multi-column masonry arrangements on desktop screens (&ge;768px) and collapse gracefully on mobile viewports (<768px).
3. **Synchronized Dual Table of Contents**: In-article navigation widgets work harmoniously with desktop floating sidebar TOCs without heading ID duplication or navigation jump clipping.
4. **Automated Zero-Regression Testing**: No manual layout checks are required; all UI components, responsive breakpoints, and DOM geometries are validated through automated Unit, BDD, and E2E browser tests in CI/CD.

---

## 2. Post Hero Image Architecture & The 41.6% Postmortem

### A. Problem Diagnosis & Root Cause
In early revisions, post hero images on individual article pages (`/posts/:slug/`) were rendering at less than 50% width inside their parent `.post-meta` container on screens larger than 768px. Furthermore, home page card previews appeared excessively shrunk to ~17% of total card width.

**Root Cause**:  
In Bootstrap's grid system, `.col-md-5` corresponds to `41.66666667%` width ($5 / 12$). In Chirpy's home page card layout, the card structure is divided into:
- `.col-md-7` (text / excerpt, 58.33%)
- `.col-md-5` (preview image wrapper, 41.67%)

A global CSS override had been previously injected into `<head>`:
```css
/* ROGUE RULE (DEPRECATED & BANNED) */
@media (min-width: 768px) {
  #post-list .preview-img, .post-preview .preview-img, .card-wrapper .preview-img {
    width: 41.66666667% !important;
  }
}
```
**Why this failed**:
1. On home page cards, applying `width: 41.66666667%` to `.preview-img` inside a container that was *already* `.col-md-5` (41.66666667%) resulted in a compounding shrink: $0.4166 \times 0.4166 = 0.1736$ (17.36% of the card width).
2. On individual post pages, `.preview-img` was scoped under `.card-wrapper` or generic classes, forcibly constricting the hero banner to 41.66% instead of filling its 100% full-width container.

### B. The Solution: Independent Container Scoping & Aspect Ratio Locks
1. **Removal of the Global 41.6% Constraint**: The rule was eradicated from `_includes/head.html`.
2. **Full-Width Hero Container (`_layouts/post.html`)**:
   ```html
   <div class="post-hero-image-wrapper w-100 my-4">
     <div class="preview-img">
       <img src="{{ post_img_path }}" alt="{{ page.title }}" width="1200" height="630" loading="eager" fetchpriority="high">
     </div>
   </div>
   ```
3. **Dedicated Post Hero & Preview Image CSS Rules (`_includes/head.html`)**:
   ```css
   /* Dedicated post hero image rules: 100% width of parent */
   .post-hero-image-wrapper {
     width: 100% !important;
     max-width: 100% !important;
     margin-left: 0 !important;
     margin-right: 0 !important;
     aspect-ratio: 1200 / 630;
     overflow: hidden;
     border-radius: 0.5rem;
   }

   .post-hero-image-wrapper .preview-img {
     width: 100% !important;
     max-width: 100% !important;
     height: 100% !important;
     aspect-ratio: 1200 / 630;
   }

   /* Ensure preview images expand to 100% of their intended container */
   #post-list .preview-img,
   .post-preview .preview-img,
   .card-wrapper .preview-img {
     width: 100% !important;
     height: 100% !important;
     object-fit: cover;
   }
   ```
4. **Result**:
   - On the Home page: `.preview-img` fills 100% of its `.col-md-5` container (exactly 41.67% of the card).
   - On Post pages: `.preview-img` fills 100% of `.post-hero-image-wrapper` (100% of the article reading column).
   - Core Web Vitals CLS remains locked at `0.000` because the container reserves an exact `1200 / 630` aspect ratio prior to asset loading.

---

## 3. Categories 2-Column Masonry Architecture

### A. The White Space Challenge
In the default Chirpy category archive (`/categories/`), category cards rendered as a single vertical column. On desktop displays (&ge;1200px or 1707px), category lists occupied only 35-45% of available horizontal canvas, creating vast empty white areas on the right side of the screen.

### B. Pure CSS Multi-Column Masonry Solution
Rather than introducing heavy JavaScript masonry libraries (e.g. Masonry.js or Isotope) that incur runtime overhead and cause CLS, the layout uses native CSS Multi-Column properties (`_layouts/categories.html` & `_includes/head.html`):

```css
/* 2-Column masonry layout for categories on desktop screens */
@media (min-width: 768px) {
  .categories-masonry-wrapper {
    column-count: 2;
    column-gap: 1.5rem;
  }
  .categories-masonry-wrapper .card-wrapper {
    break-inside: avoid;
    margin-bottom: 1.5rem;
    display: inline-block;
    width: 100%;
  }
}

/* Single column fallback for mobile */
@media (max-width: 767.98px) {
  .categories-masonry-wrapper {
    column-count: 1;
  }
}
```

### C. Benefits
- **Zero CLS**: Browsers calculate column breaks natively during box-model layout.
- **Zero JavaScript Overhead**: 0 KB runtime footprint.
- **Graceful Collapse**: Fluidly collapses to a single column on tablets and smartphones (<768px).

---

## 4. Hybrid Table of Contents (TOC) Architecture

### A. The Challenge
Technical guides on MACH Playbook often exceed 2,000 words with 6-10 deep architectural sections. The default Chirpy theme relies on a floating sidebar TOC (`#toc-wrapper`) that:
- Is hidden entirely on mobile viewports (<1200px / 850px).
- Can be visually detached on wide ultra-high-resolution monitors.

### B. Dual Hybrid Synchronized Architecture
The platform introduces a **Hybrid In-Article + Sidebar TOC**:
1. **In-Article Structured TOC Card (`_includes/post-bottom-widgets.html` / `_layouts/post.html`)**:
   - Rendered at the beginning of the article content directly below the hero banner.
   - Styled as a sleek, high-contrast navigation card with clear H2/H3 indentation.
   - Enables readers on mobile and desktop to survey the architecture before diving into deep code.
2. **Floating Sidebar TOC (`#toc-wrapper`)**:
   - Active on desktop screens &ge;1200px.
   - Highlights the current section in real-time as the reader scrolls.
3. **Scroll Offset Optimization**:
   ```css
   /* Prevent sticky topbar from obscuring target headings on jump */
   h2[id], h3[id], h4[id] {
     scroll-margin-top: 5rem;
   }
   ```
4. **Duplicate ID Prevention**: The in-article TOC links to existing heading IDs without cloning header tags, ensuring valid HTML5 and passing all `html-proofer` anchor validations.

---

## 5. Dark Mode Mermaid Diagram Rendering Engine

Mermaid.js architecture diagrams are rendered dynamically in technical posts (`mermaid: true`). By default, Mermaid SVGs can display dark text on dark backgrounds or render with opaque white rectangles in dark themes.

### CSS High-Contrast Dark Mode Overrides (`_includes/head.html`)
```css
/* High-contrast dark mode overrides for Mermaid architecture diagrams */
[data-mode="dark"] .mermaid svg,
html[data-mode="dark"] .mermaid {
  background: transparent !important;
}

[data-mode="dark"] .mermaid .node rect,
[data-mode="dark"] .mermaid .node circle,
[data-mode="dark"] .mermaid .node polygon {
  fill: #1e293b !important;
  stroke: #38bdf8 !important;
  stroke-width: 1.5px !important;
}

[data-mode="dark"] .mermaid .node .label {
  color: #f8fafc !important;
  fill: #f8fafc !important;
}

[data-mode="dark"] .mermaid .edgePath .path {
  stroke: #94a3b8 !important;
  stroke-width: 1.5px !important;
}
```

---

## 6. Automated Multi-Tier Testing Infrastructure

To guarantee zero visual or behavioral regressions across all pages and viewports, the project employs a 3-tier automated test pyramid:

```
┌───────────────────────────────────────────────────────┐
│     Tier 3: E2E Headless Browser Testing              │
│     (Chrome DevTools Protocol - CDP WebSocket)        │
│     scripts/test-e2e-browser.py                       │
├───────────────────────────────────────────────────────┤
│     Tier 2: BDD Behavioral Specifications             │
│     (19 Given-When-Then Scenarios)                    │
│     scripts/test-bdd-specs.py                         │
├───────────────────────────────────────────────────────┤
│     Tier 1: Unit & Component DOM Testing              │
│     (Static Templates, Includes & CSS Assertions)     │
│     scripts/test-ui-components.py                     │
└───────────────────────────────────────────────────────┘
```

### Tier 1: Unit & Component Testing (`scripts/test-ui-components.py`)
- **Scope**: Parses Jekyll layout templates (`_layouts/`), includes (`_includes/`), and CSS stylesheets.
- **Assertions**:
  - Confirms `.post-hero-image-wrapper` exists with `width: 100% !important` and `aspect-ratio: 1200 / 630`.
  - Confirms complete eradication of deprecated `width: 41.66666667% !important` rule on preview images.
  - Validates `scroll-margin-top: 5rem` on heading anchors.
  - Confirms `.categories-masonry-wrapper` declares `column-count: 2`.
  - Validates Formspree endpoint integration and honeypot field presence.

### Tier 2: BDD Behavioral Specifications (`scripts/test-bdd-specs.py`)
- **Scope**: Implements 19 Given-When-Then specifications across 6 distinct feature suites:
  1. `Feature: Home Page Post Grid and Preview Images`
  2. `Feature: Post Page Hero Image and Reading Layout`
  3. `Feature: Categories Page Multi-Column Masonry Layout`
  4. `Feature: Technical Glossary Navigation and Anchor Links`
  5. `Feature: Serverless Contact Form and Honeypot Protection`
  6. `Feature: Mobile Responsive Layout and Drawer Mechanics`
- **Execution**: Evaluates compiled production HTML (`_site/`) to verify DOM relationships, attributes, and structural invariants.

### Tier 3: E2E Headless Browser Testing (`scripts/test-e2e-browser.py`)
- **Scope**: Controls Google Chrome in headless mode via raw WebSocket connection to the Chrome DevTools Protocol (CDP). Eliminates heavy npm dependencies (Cypress, Playwright) and runs natively in standard Python environments.
- **Key Viewports Tested**:
  - Desktop Ultra-Wide / Laptop: `1707 x 932`
  - Desktop Standard HD: `1440 x 900`
  - Mobile Smartphone: `390 x 844` (iPhone 12/13/14 profile)
- **Geometry & Layout Assertions**:
  - Executes JavaScript expressions in page context to measure exact bounding box dimensions via `getBoundingClientRect()`.
  - Asserts that post hero image width matches container width with &le; 2px tolerance.
  - Asserts that home card images maintain balanced aspect ratios without distortion.
  - Confirms category columns arrange into 2 horizontal columns on desktop and cleanly collapse to 1 column on mobile.

### CI/CD Gating Integration
All three suites are executed during automated verification:
1. **Local Test Script**: `tools/test.sh` executes all suites in sequence.
2. **Docker Container**: `docker build --target test -t mach-playbook:test .` gates production image generation on 100% test passage.
3. **GitHub Actions**: `.github/workflows/pages-deploy.yml` enforces test passage before deploying artifacts to GitHub Pages.
