---
name: gsc-manual-url-submission
description: Automated workflow for extracting sitemap URLs, verifying sitemap/robots headers, and executing manual URL Inspection & Request Indexing in Google Search Console via browser subagent.
---

# Google Search Console Manual URL Submission Workflow

Follow this procedure when inspecting sitemap status or requesting priority indexing for new or modified URLs in **Google Search Console** for `https://mach-playbook.github.io/`.

## Step 1: Verify Sitemap and Robots.txt Health

Run network header checks to ensure `sitemap.xml` and `robots.txt` are publicly accessible:

```bash
# 1. Verify sitemap.xml returns HTTP 200 OK
wsl curl -I -L https://mach-playbook.github.io/sitemap.xml

# 2. Verify robots.txt authorizes sitemap.xml
wsl curl -L https://mach-playbook.github.io/robots.txt
```

Extract all URLs from `sitemap.xml`:
```bash
wsl --cd /home/merolhack/fl/mach-playbook python3 scripts/list-urls.py
```

## Step 2: Understand GSC Sitemap Behavior ("Couldn't fetch")

- **"Couldn't fetch" Status**: When `sitemap.xml` is newly submitted or updated in GSC, GSC displays **"Couldn't fetch"** until Google's background crawler completes its initial queue run. This is normal UI behavior and resolves automatically to **Success** within 24–48 hours.

## Step 3: Launch Browser Subagent for Manual URL Inspection

Invoke `browser_subagent` targeting Google Search Console (`https://search.google.com/search-console/inspect?resource_id=https%3A%2F%2Fmach-playbook.github.io%2F`).

### Task Automation Protocol
1. Navigate to the property inspection page.
2. For each high-priority URL (homepage, new blog posts, main tabs):
   - Type/paste full URL into the top search bar (`Inspect any URL in "https://mach-playbook.github.io/"`).
   - Wait for URL Inspection result card to render.
   - Click **"REQUEST INDEXING"**.
   - Wait for the modal dialog ("Testing if live URL can be indexed" -> "Indexing requested").
   - Click **"Dismiss"** on the confirmation dialog.
3. **Daily Quota Handling**: Google limits manual URL indexing requests (~10–12 requests per 24 hours per account). If GSC displays a "Quota exceeded" modal, gracefully log the submitted URLs and stop manual submission.

## Step 4: Record Results

Document submitted URLs, their status in Search Console, and verify that `sitemap.xml` remains active in GSC for background crawling of all remaining pages.
