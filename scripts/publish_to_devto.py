#!/usr/bin/env python3
"""
DEV.to Automated Syndication & Historical Backfill Engine
Publishes Jekyll Markdown posts to DEV.to with 100% SEO canonical protection.
"""

import os
import sys
import glob
import re
import time
import json
import argparse
import requests
import yaml

DEVTO_API_URL = "https://dev.to/api/articles"
SYNC_LOG_FILE = ".devto_synced.json"

def load_synced_log():
    if os.path.exists(SYNC_LOG_FILE):
        try:
            with open(SYNC_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_synced_log(log):
    with open(SYNC_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def parse_jekyll_post(post_path):
    with open(post_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Split YAML frontmatter
    parts = re.split(r"^---\s*$", raw_text, flags=re.MULTILINE)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except Exception:
        return None

    body_markdown = "---".join(parts[2:]).strip()
    title = frontmatter.get("title", "")
    
    # Calculate canonical URL
    base_name = os.path.basename(post_path)
    match = re.match(r"\d{4}-\d{2}-\d{2}-(.*?)\.md$", base_name)
    slug = match.group(1) if match else os.path.splitext(base_name)[0]
    canonical_url = f"https://mach-playbook.github.io/posts/{slug}/"

    # Sanitize tags (DEV.to allows max 4 tags, alphanumeric only)
    raw_tags = frontmatter.get("tags", [])
    if isinstance(raw_tags, str):
        raw_tags = [t.strip() for t in raw_tags.split(",")]
    
    clean_tags = []
    for t in raw_tags:
        sanitized = re.sub(r"[^a-zA-Z0-9]", "", str(t)).lower()
        if sanitized and sanitized not in clean_tags:
            clean_tags.append(sanitized)
        if len(clean_tags) >= 4:
            break
    if not clean_tags:
        clean_tags = ["architecture", "cloud", "devops"]

    return {
        "title": title,
        "body_markdown": body_markdown,
        "tags": clean_tags,
        "canonical_url": canonical_url,
        "slug": slug,
        "file": base_name
    }

def publish_to_devto(api_key, post_data, published=True):
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "MACH-Playbook-Syndicator/1.0"
    }

    payload = {
        "article": {
            "title": post_data["title"],
            "body_markdown": post_data["body_markdown"],
            "published": published,
            "tags": post_data["tags"],
            "canonical_url": post_data["canonical_url"]
        }
    }

    response = requests.post(DEVTO_API_URL, json=payload, headers=headers)
    return response

def main():
    parser = argparse.ArgumentParser(description="Publish posts to DEV.to")
    parser.add_argument("--api-key", default=os.environ.get("DEVTO_API_KEY"), help="DEV.to API Key")
    parser.add_argument("--all", action="store_true", help="Backfill all historical posts")
    parser.add_argument("--post", help="Path to single Markdown post to publish")
    parser.add_argument("--draft", action="store_true", help="Publish as draft instead of live")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of posts to publish")
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        print("ERROR: DEV.to API Key is required. Pass --api-key <key> or set DEVTO_API_KEY environment variable.")
        print("Get your free key at: https://dev.to/settings/extensions (Section: DEV Community API Keys)")
        sys.exit(1)

    published = not args.draft
    synced_log = load_synced_log()

    if args.post:
        files = [args.post]
    elif args.all:
        files = sorted(glob.glob("_posts/*.md"))
    else:
        # Default: publish the most recent post
        files = sorted(glob.glob("_posts/*.md"))[-1:]

    print(f"[*] Found {len(files)} post(s) to process...")
    count = 0

    for post_file in files:
        base_name = os.path.basename(post_file)
        if base_name in synced_log:
            print(f"[-] Already synced: {base_name} -> {synced_log[base_name]['url']}")
            continue

        post_data = parse_jekyll_post(post_file)
        if not post_data or not post_data["title"]:
            print(f"[!] Skipped invalid post: {base_name}")
            continue

        print(f"[+] Publishing: '{post_data['title']}'...")
        try:
            resp = publish_to_devto(api_key, post_data, published=published)
            if resp.status_code in [200, 201]:
                res_json = resp.json()
                devto_url = res_json.get("url", "")
                print(f"    SUCCESS: Published at {devto_url}")
                print(f"    Canonical preserved: {post_data['canonical_url']}")
                synced_log[base_name] = {
                    "id": res_json.get("id"),
                    "url": devto_url,
                    "canonical_url": post_data["canonical_url"],
                    "synced_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                save_synced_log(synced_log)
                count += 1
            else:
                print(f"    FAIL ({resp.status_code}): {resp.text[:200]}")
        except Exception as e:
            print(f"    ERROR: {e}")

        if args.limit and count >= args.limit:
            print(f"[*] Reached limit of {args.limit} posts.")
            break

        # Respect DEV.to rate limit (30 req / 30s)
        time.sleep(1.5)

    print(f"[*] Completed. Synced {count} post(s) to DEV.to.")

if __name__ == "__main__":
    main()
