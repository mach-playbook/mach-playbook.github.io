#!/usr/bin/env python3
"""
MACH Playbook - 48-Hour GSC & Indexation Audit Pre-Flight Script
Author: Lenin Meza (merolhack)
Description:
  Automates the HTTP pre-flight validation of sitemap.xml, robots.txt,
  trust pages, and article URLs before dispatching the GSC browser subagent.
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import sys
import os

SITE_URL = "https://mach-playbook.github.io"
SITEMAP_URL = f"{SITE_URL}/sitemap.xml"
ROBOTS_URL = f"{SITE_URL}/robots.txt"

CORE_PAGES = [
    f"{SITE_URL}/",
    f"{SITE_URL}/about/",
    f"{SITE_URL}/contact/",
    f"{SITE_URL}/terms/",
    f"{SITE_URL}/privacy/",
    f"{SITE_URL}/categories/",
    f"{SITE_URL}/tags/"
]

def check_url(url: str, user_agent: str = "Googlebot/2.1") -> tuple:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, str(e)

def run_preflight_audit():
    print("==================================================")
    print("   GSC 48-HOUR AUDIT PRE-FLIGHT DIAGNOSTICS       ")
    print("==================================================")
    
    failures = []
    
    # 1. Sitemap Verification
    print(f" Checking Sitemap: {SITEMAP_URL} ...")
    status, sitemap_data = check_url(SITEMAP_URL)
    if status != 200:
        failures.append(f"Sitemap {SITEMAP_URL} returned HTTP {status}")
        print(f"  [FAIL] Sitemap returned HTTP {status}")
    else:
        try:
            root = ET.fromstring(sitemap_data)
            urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            print(f"  [PASS] Sitemap XML is valid (HTTP 200 OK, {len(urls)} URLs discovered)")
        except Exception as e:
            failures.append(f"Sitemap XML parsing error: {e}")
            print(f"  [FAIL] Sitemap XML parsing error: {e}")

    # 2. Robots.txt Verification
    print(f"\n Checking Robots.txt: {ROBOTS_URL} ...")
    status, robots_data = check_url(ROBOTS_URL)
    if status != 200:
        failures.append(f"robots.txt returned HTTP {status}")
        print(f"  [FAIL] robots.txt returned HTTP {status}")
    else:
        robots_text = robots_data.decode("utf-8", errors="ignore")
        if "sitemap.xml" in robots_text:
            print("  [PASS] robots.txt is live and points to sitemap.xml")
        else:
            failures.append("robots.txt missing sitemap.xml declaration")
            print("  [FAIL] robots.txt missing sitemap.xml directive")

    # 3. Core Pages Verification
    print("\n Checking Core Trust Pages...")
    for page_url in CORE_PAGES:
        status, _ = check_url(page_url)
        if status == 200:
            print(f"  [PASS] {page_url} (HTTP 200 OK)")
        else:
            failures.append(f"Page {page_url} returned HTTP {status}")
            print(f"  [FAIL] {page_url} (HTTP {status})")

    print("\n--------------------------------------------------")
    if failures:
        print(f"FAILED: {len(failures)} pre-flight issue(s) detected.")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    else:
        print("PRE-FLIGHT PASSED: All production endpoints ready for GSC audit!")
        print("==================================================")

if __name__ == "__main__":
    run_preflight_audit()
