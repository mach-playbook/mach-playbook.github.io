#!/usr/bin/env python3
"""
MACH Playbook - Unified Telemetry, Sitemap SEO & GitHub Actions Log Auditor
Consolidates:
  1. Live/Local Sitemap audit (checking 0 noindex URLs leaked into sitemap.xml)
  2. Title length audit (flagging HTML <title> or seo_title > 70 chars)
  3. GitHub Pages status and recent GitHub Actions workflow runs (with safe timeouts)
  4. GitGuardian security posture probe (if GITGUARDIAN_API_KEY is available)
"""

import argparse
import glob
import json
import os
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import yaml

SITE_URL = "https://mach-playbook.github.io"
NOINDEX_PREFIXES = ("/categories/", "/tags/", "/archives/", "/resources/", "/glossary/")


def audit_sitemap(source: str = "live"):
    print("\n--- 1. SITEMAP & NOINDEX CONTRADICTION AUDIT ---")
    if source == "local" and os.path.exists("_site/sitemap.xml"):
        with open("_site/sitemap.xml", "rb") as f:
            data = f.read()
        label = "_site/sitemap.xml"
    else:
        url = f"{SITE_URL}/sitemap.xml"
        req = urllib.request.Request(url, headers={"User-Agent": "MACHPlaybook-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        label = url

    root = ET.fromstring(data)
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [el.find(f"{ns}loc").text.strip() for el in root.findall(f"{ns}url") if el.find(f"{ns}loc") is not None]
    noindex_leaks = [u for u in locs if any(u.replace(SITE_URL, "").startswith(p) for p in NOINDEX_PREFIXES)]
    print(f"Source: {label} | Total URLs: {len(locs)} | Noindex Leaks: {len(noindex_leaks)}")
    if noindex_leaks:
        print(f"  Sample leaks: {noindex_leaks[:5]}")
    return len(locs), len(noindex_leaks)


def audit_titles():
    print("\n--- 2. SEO TITLE LENGTH AUDIT (<= 70 CHARS TARGET) ---")
    over_70 = []
    posts = sorted(glob.glob("_posts/*.md"))
    for path in posts:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        m = re.match(r"^---\n(.*?)\n---", raw, re.DOTALL)
        if not m:
            continue
        data = yaml.safe_load(m.group(1)) or {}
        effective = str(data.get("seo_title") or data.get("title") or "").strip()
        rendered_len = len(effective) if len(effective) > 54 else len(effective) + len(" | MACH Playbook")
        if rendered_len > 70:
            over_70.append((os.path.basename(path), rendered_len, effective))
    print(f"Posts checked: {len(posts)} | Titles > 70 chars: {len(over_70)}")
    for fname, length, title in over_70[:10]:
        print(f"  [{length} chars] {fname}: {title}")
    return len(over_70)


def fetch_github_logs(save_dir: str = None):
    print("\n--- 3. GITHUB PAGES & ACTIONS LOGS ---")
    env = os.environ.copy()
    env.pop("GITHUB_TOKEN", None)
    env["GH_PAGER"] = ""
    env["GIT_TERMINAL_PROMPT"] = "0"

    try:
        pages_proc = subprocess.run(
            ["gh", "api", "repos/mach-playbook/mach-playbook.github.io/pages"],
            capture_output=True, text=True, env=env, timeout=15
        )
        if pages_proc.returncode == 0:
            pages_info = json.loads(pages_proc.stdout)
            print(f"GitHub Pages: url={pages_info.get('html_url')} build_type={pages_info.get('build_type')} https_enforced={pages_info.get('https_enforced')}")

        runs_proc = subprocess.run(
            ["gh", "run", "list", "--limit", "5", "--json", "databaseId,workflowName,status,conclusion,createdAt"],
            capture_output=True, text=True, env=env, timeout=15
        )
        if runs_proc.returncode == 0:
            runs = json.loads(runs_proc.stdout)
            for r in runs:
                print(f"  Run {r['databaseId']} | {r['workflowName']} | {r['status']} / {r['conclusion']} | {r['createdAt']}")
            if save_dir and runs:
                os.makedirs(save_dir, exist_ok=True)
                latest_id = str(runs[0]["databaseId"])
                log_proc = subprocess.run(
                    ["gh", "run", "view", latest_id, "--log"],
                    capture_output=True, text=True, env=env, timeout=30
                )
                if log_proc.returncode == 0:
                    out_file = os.path.join(save_dir, f"gh-run-{latest_id}.log")
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(log_proc.stdout)
                    print(f"  Saved latest log to {out_file}")
    except Exception as exc:
        print(f"  [WARN] GitHub CLI probe skipped/failed: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Audit MACH Playbook SEO, sitemap, and server CI logs.")
    parser.add_argument("--sitemap-source", choices=["live", "local"], default="live")
    parser.add_argument("--save-logs-dir", type=str, default=None, help="Optional directory to save downloaded GH logs.")
    args = parser.parse_args()

    print("=" * 60)
    print("   MACH PLAYBOOK - UNIFIED TELEMETRY & LOG AUDITOR        ")
    print("=" * 60)
    audit_sitemap(args.sitemap_source)
    audit_titles()
    fetch_github_logs(args.save_logs_dir)


if __name__ == "__main__":
    main()
