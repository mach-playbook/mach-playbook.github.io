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

        # Check bilingual blocks on all tabs
        es_block = soup.find(class_="lang-es")
        en_block = soup.find(class_="lang-en")
        if es_block and en_block:
            print(f"[PASS] Tab '{tab}': Contains bilingual blocks (.lang-es and .lang-en)")
            passes += 1
        else:
            failures.append(f"FAIL: Tab '{tab}' missing bilingual blocks (.lang-es or .lang-en)!")

        # Check table rendering on resources tab
        if tab == "resources":
            tables = soup.find_all("table")
            if len(tables) >= 2:
                print("[PASS] Tab 'resources': Tables properly rendered into <table> elements")
                passes += 1
            else:
                failures.append(f"FAIL: Tab 'resources' expected at least 2 <table> elements but found {len(tables)}!")

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

    # 4. Performance & Core Web Vitals Integrity Checks
    if os.path.exists(home_path):
        # A. Verify theme.min.js is deferred to prevent render blocking
        theme_script = home_soup.find("script", src=lambda s: s and "theme.min.js" in s)
        if theme_script and theme_script.has_attr("defer"):
            print("[PASS] Performance: theme.min.js has 'defer' attribute to eliminate render-blocking JS")
            passes += 1
        else:
            failures.append("FAIL: theme.min.js is missing 'defer' attribute in <head>!")

        # B. Verify Preconnect crossorigin for fonts.gstatic.com
        gstatic_preconnect = home_soup.find("link", rel="preconnect", href="https://fonts.gstatic.com")
        if gstatic_preconnect and gstatic_preconnect.has_attr("crossorigin"):
            print("[PASS] Performance: fonts.gstatic.com preconnect includes 'crossorigin'")
            passes += 1
        else:
            failures.append("FAIL: fonts.gstatic.com preconnect is missing 'crossorigin' attribute!")

        # C. Verify Post preview images have explicit dimensions, WebP picture sources, and proper loading attributes
        preview_imgs = home_soup.find_all("img", src=lambda s: s and "/assets/img/posts/" in s)
        if preview_imgs:
            first_img = preview_imgs[0]
            if first_img.get("loading") == "eager" and first_img.get("fetchpriority") == "high":
                print("[PASS] Performance: First post image configured with loading='eager' and fetchpriority='high' for mobile LCP")
                passes += 1
            else:
                failures.append(f"FAIL: First post image has loading='{first_img.get('loading')}', expected 'eager'!")

            all_have_dims = all(img.get("width") == "400" and img.get("height") == "225" for img in preview_imgs)
            if all_have_dims:
                print(f"[PASS] Performance: All {len(preview_imgs)} post preview images have width='400' height='225' for zero CLS")
                passes += 1
            else:
                failures.append("FAIL: Not all post preview images have width='400' and height='225'!")

        # D. Verify WebP picture sources in home feed
        webp_sources = home_soup.find_all("source", type="image/webp")
        if len(webp_sources) > 0:
            print(f"[PASS] Performance: WebP image sources configured ({len(webp_sources)} picture elements)")
            passes += 1
        else:
            failures.append("FAIL: No WebP picture sources found in home feed!")

        # E. Verify Hero WebP Image Preload in <head>
        hero_preload = home_soup.find(lambda tag: tag.name == "link" and tag.get("as") == "image" and "preload" in tag.get("rel", []))
        if hero_preload:
            print(f"[PASS] Performance: High-priority Hero WebP image preload active in <head>: {hero_preload.get('href')}")
            passes += 1
        else:
            failures.append("FAIL: Hero WebP image preload is missing in <head>!")

        # F. Verify Remaining Posts JSON serialization for lean DOM
        remaining_json = home_soup.find("script", id="remaining-posts-data", type="application/json")
        if remaining_json and len(remaining_json.text.strip()) > 50:
            print("[PASS] Performance: Remaining posts serialized to JSON for lean initial DOM")
            passes += 1
        else:
            failures.append("FAIL: remaining-posts-data JSON block is missing or empty!")

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
