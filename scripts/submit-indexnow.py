#!/usr/bin/env python3
"""
MACH Playbook - IndexNow Batch Submitter (Bing Webmaster Tools & Microsoft Copilot)
Reads canonical indexable URLs from _site/sitemap.xml (or live production sitemap.xml),
appends /llms.txt and /llms-full.txt, and submits them via IndexNow API.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HOST = "mach-playbook.github.io"
INDEXNOW_KEY = "4f8b9e2d1a7c6b3e5f0d8a9c2e4b7d1f"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
NOINDEX_PREFIXES = ("/categories/", "/tags/", "/archives/", "/resources/", "/glossary/")


def load_sitemap_urls(local_sitemap: str = "_site/sitemap.xml", live_sitemap: str = f"https://{HOST}/sitemap.xml"):
    xml_bytes = None
    if os.path.exists(local_sitemap):
        with open(local_sitemap, "rb") as f:
            xml_bytes = f.read()
        print(f"[IndexNow] Loaded URLs from local build: {local_sitemap}")
    else:
        print(f"[IndexNow] Local sitemap missing; fetching {live_sitemap} ...")
        req = urllib.request.Request(live_sitemap, headers={"User-Agent": "MACHPlaybook-IndexNow/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = []
    for el in root.findall(f"{ns}url"):
        loc = el.find(f"{ns}loc")
        if loc is not None and loc.text:
            u = loc.text.strip()
            path = u.replace(f"https://{HOST}", "")
            if not any(path.startswith(p) for p in NOINDEX_PREFIXES):
                urls.append(u)

    for geo_url in (f"https://{HOST}/llms.txt", f"https://{HOST}/llms-full.txt"):
        if geo_url not in urls:
            urls.append(geo_url)
    return urls


def submit_indexnow_batch(url_list: list, dry_run: bool = False) -> bool:
    if not url_list:
        print("[IndexNow] No URLs to submit.")
        return True

    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list[:10000],
    }

    if dry_run:
        print(f"[IndexNow] Dry-run enabled. Prepared {len(payload['urlList'])} URLs for {INDEXNOW_ENDPOINT}.")
        print(f"  Sample URLs: {payload['urlList'][:5]}")
        return True

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "MACHPlaybook-IndexNow/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as he:
        status = he.code
        body = he.read().decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"[IndexNow] Network error: {exc}")
        return False

    if status in (200, 202):
        print(f"[IndexNow] SUCCESS (HTTP {status}): Submitted {len(payload['urlList'])} URLs to Bing/Copilot ecosystem.")
        return True
    print(f"[IndexNow] WARNING: Endpoint returned HTTP {status}: {body}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Submit MACH Playbook canonical URLs to IndexNow.")
    parser.add_argument("--url", type=str, default=None, help="Submit a single URL instead of full sitemap batch.")
    parser.add_argument("--dry-run", action="store_true", help="Validate payload without sending HTTP POST.")
    args = parser.parse_args()

    urls = [args.url] if args.url else load_sitemap_urls()
    ok = submit_indexnow_batch(urls, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
