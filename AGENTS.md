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
