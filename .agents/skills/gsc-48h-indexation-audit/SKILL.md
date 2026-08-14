---
name: gsc-48h-indexation-audit
description: Autonomous 48-hour audit workflow for Google Search Console (sitemap transition validation, discovered URL count, page indexing growth, and AdSense approval status check).
---

# Google Search Console 48-Hour Indexation & AdSense Audit Workflow

Follow this procedure 48 hours after a sitemap submission or major site restructuring to verify that Googlebot has processed `sitemap.xml`, discovered all canonical URLs, accelerated page indexing, and advanced Google AdSense review status.

---

## Pre-flight Checklist (Terminal Execution)

Run the pre-flight verification script to ensure all production endpoints and sitemap XML structures are 100% operational:

```bash
# In WSL:
cd /home/merolhack/fl/mach-playbook
python3 scripts/audit-gsc-indexation.py
```

This verifies:
1. `https://mach-playbook.github.io/sitemap.xml` returns `HTTP 200 OK` with valid XML and ~117 URLs.
2. `https://mach-playbook.github.io/robots.txt` explicitly allows and links to `sitemap.xml`.
3. All core trust tabs (`/about/`, `/contact/`, `/terms/`, `/privacy/`) respond with `HTTP 200 OK`.

---

## Step 1: GSC Sitemap Status Verification (Browser Subagent)

Dispatch the `browser_subagent` to inspect the Sitemaps report in Google Search Console:

**Target URL:** `https://search.google.com/search-console/sitemaps?resource_id=https%3A%2F%2Fmach-playbook.github.io%2F&hl=en`

### Verification Protocol:
1. Locate the `/sitemap.xml` entry in the **Submitted sitemaps** table.
2. **Status Column**: Confirm the status has transitioned from `Couldn't fetch` to **`Success`** (green).
3. **Type Column**: Confirm it is identified as **`Sitemap`** (formerly `Unknown`).
4. **Last Read Column**: Verify a recent timestamp is recorded (confirming Googlebot successfully read the file).
5. **Discovered Pages**: Verify that discovered pages count reflects the canonical sitemap size (**~117 pages**).

> [!NOTE]
> If the sitemap still shows `Couldn't fetch` but `Last read` is blank, Google's queue is still pending. If `Last read` is populated with an error, click the row to inspect the error drilldown.

---

## Step 2: Page Indexing Report Audit (Browser Subagent)

Navigate to the Page Indexing report:

**Target URL:** `https://search.google.com/search-console/index?resource_id=https%3A%2F%2Fmach-playbook.github.io%2F&hl=en`

### Verification Protocol:
1. Record the number of **Indexed pages** (target: increasing from 1 towards 62+).
2. Record the number of **Not indexed pages**.
3. In the **"Why pages aren't indexed"** table, audit the breakdown:
   * **`Discovered - currently not indexed`**: Normal for newly submitted URLs waiting for crawler allocation.
   * **`Crawled - currently not indexed`**: Indicates Google evaluated the page; check if any thin content or duplicate tags remain.
   * **`Page with redirect`**: Normal for trailing slash normalizations or old tag redirects.
   * **`Not found (404)`**: Must be 0 (if any 404s exist, fix internal broken links immediately).

---

## Step 3: Priority URL Inspection & Live Test (Top 5 Unindexed Articles)

For any high-priority pillar articles that remain unindexed:
1. Open the top URL inspection bar (`Inspect any URL in "https://mach-playbook.github.io/"`).
2. Paste the article URL and press Enter.
3. Click **"Test Live URL"** to confirm Googlebot smartphone accessibility.
4. Click **"Request Indexing"** (respecting daily quota limits).

---

## Step 4: Google AdSense Review Status Check (Browser Subagent)

Navigate to the Google AdSense Console:

**Target URL:** `https://adsense.google.com/` &rarr; **Sites**

### Verification Protocol:
1. Check the status badge for `mach-playbook.github.io`:
   * **`Ready` (Green)**: Site approved! Ads are active.
   * **`Getting ready` / `Review requested`**: Review in progress.
   * **`Needs attention`**: Click to read specific feedback. If all 11 compliance vectors pass (`python3 scripts/test-adsense-compliance.py`), check the resolution box and click **"Request review"**.

---

## Step 5: Document Audit Findings

Append a structured audit entry to `HISTORY.txt` and update `llm-wiki.md`:
* Date & Time of Audit
* GSC Sitemap status (`Success` vs `Pending`) & Discovered count
* Indexed pages count vs Not indexed count
* AdSense review status
