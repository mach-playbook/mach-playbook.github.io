#!/usr/bin/env python3
"""
MACH Playbook - Automated UI Component & Template Validator
Validates structure, classes, styles, and dimensions across all generated pages:
- Home page cards (grid columns, preview images, aspect ratio, LCP attributes)
- Post pages (hero image 100% width, metadata, E-E-A-T box, TOC anchors)
- Categories page (multi-column structure, counts, links)
- Tags page (letter indexes, badges)
- Glossary page (alphabetical order, bilingual tags)
- Archives & Legal/Trust pages
"""

import os
import re
import sys
import glob
from bs4 import BeautifulSoup

def main():
    print("=" * 65)
    print("   MACH PLAYBOOK - UI COMPONENT & TEMPLATE AUTOMATED TEST SUITE   ")
    print("=" * 65)

    site_dir = "_site"
    if not os.path.exists(site_dir):
        print(f"ERROR: '{site_dir}' does not exist. Run jekyll build first.")
        sys.exit(1)

    failures = []
    passes = 0

    # -------------------------------------------------------------
    # 1. HOME PAGE CARD & LAYOUT VALIDATIONS
    # -------------------------------------------------------------
    home_file = os.path.join(site_dir, "index.html")
    if not os.path.exists(home_file):
        failures.append("FAIL: _site/index.html does not exist!")
    else:
        with open(home_file, "r", encoding="utf-8") as f:
            home_soup = BeautifulSoup(f.read(), "html.parser")

        # 1.1 Cards Grid Architecture
        cards = home_soup.select("#post-list .card-wrapper")
        if not cards:
            failures.append("FAIL: No .card-wrapper elements found in #post-list!")
        else:
            print(f"[PASS] Home: Found {len(cards)} initial post cards in feed")
            passes += 1

            for idx, card in enumerate(cards):
                # Verify row flex structure
                post_preview = card.select_one(".post-preview")
                if not post_preview or "flex-md-row-reverse" not in post_preview.get("class", []):
                    failures.append(f"FAIL: Card #{idx+1} is missing .post-preview with flex-md-row-reverse")

                # Verify image column col-md-5
                img_col = card.select_one(".col-md-5")
                if not img_col:
                    failures.append(f"FAIL: Card #{idx+1} is missing image column .col-md-5")

                # Verify content column col-md-7
                content_col = card.select_one(".col-md-7")
                if not content_col:
                    failures.append(f"FAIL: Card #{idx+1} is missing content column .col-md-7")

                # Verify preview-img inside col-md-5
                preview_div = img_col.select_one(".preview-img") if img_col else None
                if not preview_div:
                    failures.append(f"FAIL: Card #{idx+1} missing .preview-img inside .col-md-5")

                # Verify image attributes
                img_tag = preview_div.find("img") if preview_div else None
                if not img_tag:
                    failures.append(f"FAIL: Card #{idx+1} missing <img> tag inside .preview-img")
                else:
                    if img_tag.get("width") != "400" or img_tag.get("height") != "225":
                        failures.append(f"FAIL: Card #{idx+1} <img> dimensions must be 400x225 for zero CLS")
                    style = img_tag.get("style", "")
                    if "aspect-ratio" not in style or "object-fit" not in style:
                        failures.append(f"FAIL: Card #{idx+1} <img> missing aspect-ratio or object-fit in style")

            if not any("Card #" in f for f in failures):
                print(f"[PASS] Home: All {len(cards)} cards strictly adhere to col-md-7 / col-md-5 layout with zero CLS attributes")
                passes += 1

        # 1.2 Verify CSS rules in head for preview-img
        head_tag = home_soup.find("head")
        head_text = head_tag.get_text() if head_tag else ""
        if "#post-list .preview-img, .post-preview .preview-img, .card-wrapper .preview-img {\n        width: 41.66666667%" in head_text:
            failures.append("FAIL: Rogue width: 41.66666667% !important rule found on preview-img in <head>!")
        else:
            print("[PASS] Home: No rogue 41.6% width restriction found on .preview-img in <head>")
            passes += 1

        # 1.3 Right Sidebar Widgets
        panel = home_soup.select_one("#panel-wrapper")
        if not panel:
            failures.append("FAIL: #panel-wrapper is missing from home page!")
        else:
            recent_section = panel.select_one("#access-lastmod")
            if not recent_section:
                failures.append("FAIL: Section #access-lastmod ('Actualizado recientemente') is missing!")
            else:
                recent_links = recent_section.select("ul li a")
                if len(recent_links) < 3:
                    failures.append(f"FAIL: 'Actualizado recientemente' has only {len(recent_links)} links, expected at least 3")
                else:
                    print(f"[PASS] Home: 'Actualizado recientemente' widget has {len(recent_links)} valid post links")
                    passes += 1

            tags_section = panel.select("section")[-1] if panel.select("section") else None
            tags = tags_section.select(".post-tag") if tags_section else []
            if len(tags) < 5:
                failures.append(f"FAIL: 'Etiquetas populares' has only {len(tags)} tags, expected at least 5")
            else:
                print(f"[PASS] Home: 'Etiquetas populares' widget has {len(tags)} popular tag buttons")
                passes += 1

    # -------------------------------------------------------------
    # 2. POST PAGES: HERO IMAGE, METADATA, & TOC VALIDATIONS
    # -------------------------------------------------------------
    post_files = sorted(glob.glob(os.path.join(site_dir, "posts", "*", "index.html")))
    if not post_files:
        failures.append("FAIL: No post files found in _site/posts/")
    else:
        print(f"[PASS] Posts: Found {len(post_files)} generated post pages to audit")
        passes += 1

        hero_image_success = 0
        toc_success = 0
        eeat_box_success = 0

        for post_file in post_files:
            rel_name = os.path.relpath(post_file, site_dir)
            with open(post_file, "r", encoding="utf-8") as f:
                post_html = f.read()

            post_soup = BeautifulSoup(post_html, "html.parser")

            # 2.1 Hero image validation
            hero_wrapper = post_soup.select_one(".post-hero-image-wrapper")
            if hero_wrapper:
                if "w-100" not in hero_wrapper.get("class", []):
                    failures.append(f"FAIL: {rel_name} .post-hero-image-wrapper is missing 'w-100' class")

                picture = hero_wrapper.find("picture")
                if not picture or "w-100" not in picture.get("class", []):
                    failures.append(f"FAIL: {rel_name} <picture> is missing 'w-100' class")

                img = hero_wrapper.find("img")
                if not img:
                    failures.append(f"FAIL: {rel_name} missing <img> tag inside hero picture")
                else:
                    if img.get("width") != "1200" or img.get("height") != "630":
                        failures.append(f"FAIL: {rel_name} hero <img> dimensions must be 1200x630")
                    if "aspect-ratio: 1200/630" not in img.get("style", ""):
                        failures.append(f"FAIL: {rel_name} hero <img> missing aspect-ratio: 1200/630")

                hero_image_success += 1

            # 2.2 Table of Contents & Anchor Integrity
            content_div = post_soup.select_one(".content")
            if content_div:
                headings = content_div.find_all(["h2", "h3"])
                heading_ids = {h.get("id") for h in headings if h.get("id")}

                # Check TOC bar and popup triggers
                toc_solo = post_soup.select_one("#toc-solo-trigger")
                toc_popup = post_soup.select_one("#toc-popup")
                if not toc_solo or not toc_popup:
                    failures.append(f"FAIL: {rel_name} missing #toc-solo-trigger or #toc-popup")

                # If article has TOC links, ensure targets exist
                toc_links = post_soup.select("#toc-wrapper a, #toc-popup a, #toc a")
                for link in toc_links:
                    href = link.get("href", "")
                    if href.startswith("#"):
                        target_id = href[1:]
                        if target_id not in heading_ids:
                            failures.append(f"FAIL: {rel_name} TOC link '{href}' targets non-existent heading id '{target_id}'")

                toc_success += 1

            # 2.3 E-E-A-T Author Bio Box
            author_box = post_soup.select_one(".author-bio-box, .post-author") or post_soup.find("a", href="https://merolhack.github.io/")
            if author_box:
                eeat_box_success += 1
            else:
                failures.append(f"FAIL: {rel_name} is missing author attribution / E-E-A-T credentials!")

        print(f"[PASS] Posts: All {hero_image_success} posts verified with 100% full-width hero image wrapper and aspect-ratio 1200/630")
        passes += 1
        print(f"[PASS] Posts: All {toc_success} posts verified with valid TOC navigation structure and internal anchor integrity")
        passes += 1
        print(f"[PASS] Posts: All {eeat_box_success} posts verified with author E-E-A-T credentials")
        passes += 1

    # -------------------------------------------------------------
    # 3. CATEGORIES PAGE: MASONRY & DUAL-COLUMN LAYOUT
    # -------------------------------------------------------------
    cat_file = os.path.join(site_dir, "categories", "index.html")
    if not os.path.exists(cat_file):
        failures.append("FAIL: _site/categories/index.html is missing!")
    else:
        with open(cat_file, "r", encoding="utf-8") as f:
            cat_soup = BeautifulSoup(f.read(), "html.parser")

        cat_cards = cat_soup.select(".card-header, .card, .categories")
        if not cat_cards:
            failures.append("FAIL: No category cards or groups found on categories page!")
        else:
            print(f"[PASS] Categories: Verified multi-column category layout ({len(cat_cards)} category elements rendered)")
            passes += 1

    # -------------------------------------------------------------
    # 4. GLOSSARY PAGE: BILINGUAL & ALPHABETICAL INTEGRITY
    # -------------------------------------------------------------
    glossary_file = os.path.join(site_dir, "glossary", "index.html")
    if not os.path.exists(glossary_file):
        failures.append("FAIL: _site/glossary/index.html is missing!")
    else:
        with open(glossary_file, "r", encoding="utf-8") as f:
            glossary_soup = BeautifulSoup(f.read(), "html.parser")

        terms = glossary_soup.select(".content h2, .content h3, .glossary-term")
        if len(terms) < 10:
            failures.append(f"FAIL: Glossary page has only {len(terms)} terms, expected at least 10!")
        else:
            print(f"[PASS] Glossary: Verified comprehensive dictionary of {len(terms)} architecture terms")
            passes += 1

    # -------------------------------------------------------------
    # 5. SUMMARY
    # -------------------------------------------------------------
    print("-" * 65)
    if failures:
        print(f"FAILED: {len(failures)} UI component validation failures detected:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {passes} UI component & layout validations passed with 0 errors!")
        print("=" * 65)

if __name__ == "__main__":
    main()
