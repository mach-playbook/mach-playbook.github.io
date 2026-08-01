---
name: add-new-post-test-deploy
description: Standardized workflow to create new Jekyll Markdown blog posts, perform duplicate and AdSense policy checks, execute Docker HTML-Proofer unit testing, commit, push, and validate GitHub Pages deployment.
---

# Add New Posts, Test, and Deploy Workflow

Follow this procedure whenever creating, updating, or publishing new blog posts to the **MACH Playbook** codebase (`mach-playbook.github.io`).

## Step 1: Create Post Markdown File

Create a new file under `_posts/YYYY-MM-DD-title.md` following Jekyll date-prefix naming conventions.

### YAML Frontmatter Requirements
Every post MUST include explicit frontmatter parameters:
```yaml
---
layout: post
title: "Descriptive Post Title"
date: YYYY-MM-DD HH:MM:SS -0600
lang: es # Or 'en' depending on article language
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
image:
  path: /assets/img/posts/YYYY-MM-DD-title.png # Optional, cover image synthesized automatically if omitted
---
```

> **E-E-A-T & Word Count Requirement**: All technical posts must exceed 1,000 words with concrete architectural analysis, code snippets, or sequence diagrams to prevent "thin content" flags.

## Step 2: Validate Content Quality & AdSense Compliance

Run pre-deployment compliance scripts in WSL:

```bash
# 1. Check for duplicate post titles and body content similarity
wsl --cd /home/merolhack/fl/mach-playbook python3 scripts/check-duplicates.py

# 2. Check AdSense Policy Compliance (ads.txt, Publisher ID, privacy, non-thin content, lang flags)
wsl --cd /home/merolhack/fl/mach-playbook python3 scripts/test-adsense-compliance.py
```

Ensure both scripts output `SUCCESS` with 0 issues detected.

## Step 3: Run Docker Unit Tests (HTML-Proofer)

Run the multi-stage Docker build matching GitHub Pages CI/CD to validate HTML syntax, internal links, and image paths:

```bash
wsl --cd /home/merolhack/fl/mach-playbook docker build --target test -t mach-playbook:test .
```

Verify output ends with: `HTML-Proofer finished successfully.`

## Step 4: Git Stage, Commit, and Push

1. Stage new or modified post files:
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook git add _posts/
   ```
2. Commit with descriptive semantic message:
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook git commit -m "feat: add <Post Title> technical article for AdSense compliance"
   ```
3. Rebase onto origin main (in case image generation CI pushed commits):
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook git pull --rebase origin main
   ```
4. Push to remote:
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook git push origin main
   ```

## Step 5: Validate GitHub Actions Deployment

1. Check active workflow runs:
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook gh run list --limit 5
   ```
2. Monitor `Build and Deploy` and `Auto Generate Missing Post Images` workflows:
   ```bash
   wsl --cd /home/merolhack/fl/mach-playbook gh run watch <RUN_ID>
   ```
3. Confirm both workflows finish with status `completed | success`.
