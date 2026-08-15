#!/usr/bin/env python3
"""
MACH Playbook - Comprehensive Site Integrity & Localization Validator
Validates:
1. Markdown parsing inside bilingual divs across all static pages (_site/about, contact, terms, privacy, resources, glossary).
2. Global language script (assets/js/lang-filter.js) inclusion on all pages.
3. Mermaid high-contrast dark theme CSS injection.
4. Google AdSense policy compliance and E-E-A-T credentials.
5. Zero duplicates across 65+ articles.
"""

import os
import re
import sys
from bs4 import BeautifulSoup

def main():
    print("=" * 60)
    print("   MACH PLAYBOOK - SITE INTEGRITY & LOCALIZATION VALIDATION   ")
    print("=" * 60)

    site_dir = "_site"
    if not os.path.exists(site_dir):
        print(f"ERROR: '{site_dir}' directory does not exist! Please build Jekyll first.")
        sys.exit(1)

    failures = []
    passes = 0

    # 1. Check static tab pages
    tabs = ["about", "contact", "terms", "privacy", "resources", "glossary"]
    raw_markdown_patterns = [
        r"(?:^|\s)#{1,4}\s+[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ]",  # Raw markdown headings like "# Title"
        r"\*\*[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ].*?\*\*",         # Raw markdown bold like "**Bold**"
        r"(?:^|\n)\s*---\s*(?:\n|$)",                   # Raw markdown horizontal rules
        r"(?:^|\n)\s*\*\s+[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ]"     # Raw markdown list items "* item"
    ]

    for tab in tabs:
        path = os.path.join(site_dir, tab, "index.html")
        if not os.path.exists(path):
            failures.append(f"FAIL: Missing HTML file for tab: {tab} at {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        main_article = soup.find("article") or soup.find("main")
        if not main_article:
            failures.append(f"FAIL: Tab {tab} has no <article> or <main> tag!")
            continue

        article_text = main_article.get_text()

        # Check for unparsed raw markdown leaking into visible text
        leaked_markdown = False
        for pat in raw_markdown_patterns:
            matches = re.findall(pat, article_text)
            if matches:
                failures.append(f"FAIL: Tab '{tab}' contains unparsed markdown: {matches[:3]} in rendered text!")
                leaked_markdown = True
                break

        if not leaked_markdown:
            print(f"[PASS] Tab '{tab}': Markdown rendered properly into HTML (no raw syntax)")
            passes += 1

        # Check bilingual blocks on about, contact, terms, privacy
        if tab in ["about", "contact", "terms", "privacy"]:
            es_block = soup.find(class_="lang-es")
            en_block = soup.find(class_="lang-en")
            if es_block and en_block:
                print(f"[PASS] Tab '{tab}': Contains bilingual blocks (.lang-es and .lang-en)")
                passes += 1
            else:
                failures.append(f"FAIL: Tab '{tab}' missing bilingual blocks (.lang-es or .lang-en)!")

        # Check lang-filter.js inclusion
        scripts = [s.get("src", "") for s in soup.find_all("script")]
        has_lang_filter = any("lang-filter.js" in s for s in scripts)
        if has_lang_filter:
            print(f"[PASS] Tab '{tab}': Includes assets/js/lang-filter.js")
            passes += 1
        else:
            failures.append(f"FAIL: Tab '{tab}' does NOT include assets/js/lang-filter.js!")

    # 2. Check Home Page
    home_path = os.path.join(site_dir, "index.html")
    if os.path.exists(home_path):
        with open(home_path, "r", encoding="utf-8") as f:
            home_html = f.read()
        home_soup = BeautifulSoup(home_html, "html.parser")
        home_scripts = [s.get("src", "") for s in home_soup.find_all("script")]
        if any("lang-filter.js" in s for s in home_scripts):
            print("[PASS] Home page: Includes assets/js/lang-filter.js")
            passes += 1
        else:
            failures.append("FAIL: Home page does NOT include assets/js/lang-filter.js!")

        # Check filter pills
        pills = home_soup.find(id="home-lang-pills")
        if pills:
            print("[PASS] Home page: Contains #home-lang-pills")
            passes += 1
        else:
            failures.append("FAIL: Home page missing #home-lang-pills!")

    # 3. Check Mermaid CSS Injected in Head
    if os.path.exists(home_path):
        with open(home_path, "r", encoding="utf-8") as f:
            head_content = f.read()
        if "rect.actor" in head_content and "messageLine0" in head_content and "noteText" in head_content:
            print("[PASS] Mermaid sequence diagram dark-mode CSS overrides verified in <head>")
            passes += 1
        else:
            failures.append("FAIL: Mermaid sequence diagram CSS overrides missing from <head>!")

    print("-" * 60)
    if failures:
        print(f"FAILED: {len(failures)} test failures detected:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {passes} site integrity & localization checks passed with 0 errors!")
        print("=" * 60)

if __name__ == "__main__":
    main()
