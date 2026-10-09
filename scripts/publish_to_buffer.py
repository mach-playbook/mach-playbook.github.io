#!/usr/bin/env python3
"""
Buffer GraphQL Automated Syndication Engine for MACH Playbook
Schedules/Publishes posts to connected Twitter (X) and LinkedIn channels via Buffer GraphQL API.
"""

import os
import sys
import glob
import re
import json
import argparse
import requests
import yaml

BUFFER_GRAPHQL_URL = "https://api.buffer.com/graphql"
BUFFER_SYNC_LOG = ".buffer_synced.json"

def load_buffer_log():
    if os.path.exists(BUFFER_SYNC_LOG):
        try:
            with open(BUFFER_SYNC_LOG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_buffer_log(log):
    with open(BUFFER_SYNC_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def parse_jekyll_post(post_path):
    with open(post_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    parts = re.split(r"^---\s*$", raw_text, flags=re.MULTILINE)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except Exception:
        return None

    title = frontmatter.get("title", "")
    description = frontmatter.get("description", "")
    
    base_name = os.path.basename(post_path)
    match = re.match(r"\d{4}-\d{2}-\d{2}-(.*?)\.md$", base_name)
    slug = match.group(1) if match else os.path.splitext(base_name)[0]
    canonical_url = f"https://mach-playbook.github.io/posts/{slug}/"

    raw_tags = frontmatter.get("tags", [])
    if isinstance(raw_tags, str):
        raw_tags = [t.strip() for t in raw_tags.split(",")]
    
    clean_tags = []
    for t in raw_tags:
        sanitized = re.sub(r"[^a-zA-Z0-9]", "", str(t))
        if sanitized and sanitized not in clean_tags:
            clean_tags.append(f"#{sanitized}")
        if len(clean_tags) >= 4:
            break
    if not clean_tags:
        clean_tags = ["#MACH", "#CloudNative", "#SoftwareArchitecture", "#DevOps"]

    return {
        "title": title,
        "description": description,
        "canonical_url": canonical_url,
        "tags": clean_tags,
        "file": base_name
    }

def get_buffer_channels(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 1. Get Organization ID
    org_query = """
    query GetOrg {
      account {
        organizations {
          id
          name
        }
      }
    }
    """
    resp = requests.post(BUFFER_GRAPHQL_URL, headers=headers, json={"query": org_query}, timeout=10)
    if resp.status_code != 200:
        print(f"[!] Error fetching Buffer account: HTTP {resp.status_code} - {resp.text}")
        return []

    data = resp.json().get("data", {})
    orgs = data.get("account", {}).get("organizations", [])
    if not orgs:
        print("[!] No Buffer organizations found.")
        return []

    org_id = orgs[0]["id"]

    # 2. Get Channels for Organization
    channels_query = """
    query GetChannels($input: ChannelsInput!) {
      channels(input: $input) {
        id
        name
        service
        displayName
      }
    }
    """
    c_resp = requests.post(BUFFER_GRAPHQL_URL, headers=headers, json={
        "query": channels_query,
        "variables": {"input": {"organizationId": org_id}}
    }, timeout=10)

    if c_resp.status_code != 200:
        print(f"[!] Error fetching channels: HTTP {c_resp.status_code} - {c_resp.text}")
        return []

    return c_resp.json().get("data", {}).get("channels", [])

def schedule_post_to_buffer(api_key, channel_id, text, mode="addToQueue"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        __typename
        ... on PostActionSuccess {
          post {
            id
            status
            dueAt
          }
        }
        ... on InvalidInputError {
          message
        }
        ... on LimitReachedError {
          message
        }
        ... on UnexpectedError {
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "channelId": channel_id,
            "text": text,
            "mode": mode,
            "schedulingType": "automatic",
            "assets": [],
            "saveToDraft": False
        }
    }

    resp = requests.post(BUFFER_GRAPHQL_URL, headers=headers, json={
        "query": mutation,
        "variables": variables
    }, timeout=10)

    return resp

def main():
    parser = argparse.ArgumentParser(description="Schedule/Publish posts to Buffer (X & LinkedIn)")
    parser.add_argument("--api-key", default=os.environ.get("BUFFER_API_KEY"), help="Buffer API Key")
    parser.add_argument("--post", help="Path to single Markdown post")
    parser.add_argument("--now", action="store_true", help="Publish immediately (shareNow) instead of addToQueue")
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        print("ERROR: Buffer API Key required. Set BUFFER_API_KEY environment variable or pass --api-key.")
        sys.exit(1)

    channels = get_buffer_channels(api_key)
    if not channels:
        print("[-] No channels connected in Buffer.")
        sys.exit(1)

    print(f"[*] Found {len(channels)} connected Buffer channel(s):")
    for c in channels:
        print(f"    - [{c['service'].upper()}] {c['displayName']} (ID: {c['id']})")

    if args.post:
        post_file = args.post
    else:
        # Default: latest post
        files = sorted(glob.glob("_posts/*.md"))
        if not files:
            print("[!] No posts found in _posts/")
            sys.exit(1)
        post_file = files[-1]

    post_data = parse_jekyll_post(post_file)
    if not post_data or not post_data["title"]:
        print(f"[!] Could not parse valid post from {post_file}")
        sys.exit(1)

    base_name = post_data["file"]
    sync_log = load_buffer_log()
    if base_name in sync_log:
        print(f"[-] Already scheduled/published in Buffer: {base_name}")
        for s in sync_log[base_name].get("channels", []):
            print(f"    - [{s.get('service')}] Post ID: {s.get('post_id')} (Status: {s.get('status')})")
        return

    mode = "shareNow" if args.now else "addToQueue"
    tags_str = " ".join(post_data["tags"])

    # Compose platform-optimized text
    text_content = f"{post_data['title']}\n\n{post_data['canonical_url']}\n\n{tags_str}"

    print(f"\n[+] Scheduling post: '{post_data['title']}'...")
    scheduled_channels = []

    for c in channels:
        ch_id = c["id"]
        ch_service = c["service"]
        resp = schedule_post_to_buffer(api_key, ch_id, text_content, mode=mode)
        if resp.status_code == 200:
            res_data = resp.json().get("data", {}).get("createPost", {})
            if res_data.get("__typename") == "PostActionSuccess":
                p_info = res_data.get("post", {})
                print(f"    SUCCESS [{ch_service.upper()}]: Post ID {p_info.get('id')} scheduled for {p_info.get('dueAt')}")
                scheduled_channels.append({
                    "channel_id": ch_id,
                    "service": ch_service,
                    "post_id": p_info.get("id"),
                    "dueAt": p_info.get("dueAt"),
                    "status": p_info.get("status")
                })
            else:
                print(f"    FAILED [{ch_service.upper()}]: {res_data}")
        else:
            print(f"    HTTP ERROR [{ch_service.upper()}]: {resp.status_code} - {resp.text}")

    if scheduled_channels:
        sync_log[base_name] = {
            "title": post_data["title"],
            "url": post_data["canonical_url"],
            "scheduled_at": str(os.popen("date -u '+%Y-%m-%d %H:%M:%S UTC'").read().strip()),
            "channels": scheduled_channels
        }
        save_buffer_log(sync_log)
        print(f"[✓] Recorded in {BUFFER_SYNC_LOG}")

if __name__ == "__main__":
    main()
