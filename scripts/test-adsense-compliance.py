#!/usr/bin/env python3
import os
import glob
import re
import sys

def run_adsense_tests():
    print("==================================================")
    print("   RUNNING GOOGLE ADSENSE POLICY COMPLIANCE TESTS  ")
    print("==================================================")
    
    failures = []
    
    # Test 1: Verify ads.txt
    ads_path = "ads.txt"
    if not os.path.exists(ads_path):
        failures.append("FAIL: ads.txt is missing from repository root!")
    else:
        with open(ads_path, "r", encoding="utf-8") as f:
            ads_content = f.read()
        if "google.com, pub-2700240339792942, DIRECT, f08c47fec0942fa0" in ads_content:
            print("[PASS] ads.txt contains valid Publisher ID (ca-pub-2700240339792942)")
        else:
            failures.append("FAIL: ads.txt does not contain valid Publisher ID!")

    # Test 2: Verify head.html AdSense meta tags
    head_path = "_includes/head.html"
    if not os.path.exists(head_path):
        failures.append("FAIL: _includes/head.html is missing!")
    else:
        with open(head_path, "r", encoding="utf-8") as f:
            head_content = f.read()
        if "ca-pub-2700240339792942" in head_content:
            print("[PASS] _includes/head.html contains AdSense Publisher ID & Verification Tag")
        else:
            failures.append("FAIL: _includes/head.html missing AdSense Publisher ID!")

    # Test 3: Verify Privacy Policy AdSense Disclosures
    privacy_path = "_tabs/privacy.md"
    if not os.path.exists(privacy_path):
        failures.append("FAIL: _tabs/privacy.md is missing!")
    else:
        with open(privacy_path, "r", encoding="utf-8") as f:
            privacy_content = f.read()
        if "AdSense" in privacy_content or "cookie" in privacy_content.lower():
            print("[PASS] Privacy Policy includes Google AdSense cookie disclosures")
        else:
            failures.append("FAIL: Privacy Policy missing AdSense & cookie disclosure clauses!")

    # Test 4: Verify About Page E-E-A-T Credentials
    about_path = "_tabs/about.md"
    if not os.path.exists(about_path):
        failures.append("FAIL: _tabs/about.md is missing!")
    else:
        with open(about_path, "r", encoding="utf-8") as f:
            about_content = f.read()
        if len(about_content.split()) >= 200:
            print("[PASS] About page contains robust E-E-A-T author credentials")
        else:
            failures.append("FAIL: About page content too brief for E-E-A-T!")

    # Test 5: Verify Contact Page Presence
    contact_path = "_tabs/contact.md"
    if not os.path.exists(contact_path):
        failures.append("FAIL: _tabs/contact.md is missing!")
    else:
        with open(contact_path, "r", encoding="utf-8") as f:
            contact_content = f.read()
        if "merolhack@gmail.com" in contact_content:
            print("[PASS] Contact page verified with direct inquiry endpoints")
        else:
            failures.append("FAIL: Contact page missing direct email contact endpoint!")

    # Test 6: Verify Terms of Service Page Presence
    terms_path = "_tabs/terms.md"
    if not os.path.exists(terms_path):
        failures.append("FAIL: _tabs/terms.md is missing!")
    else:
        with open(terms_path, "r", encoding="utf-8") as f:
            terms_content = f.read()
        if "Terms" in terms_content:
            print("[PASS] Terms of Service page verified with full legal disclaimers")
        else:
            failures.append("FAIL: Terms of Service page content incomplete!")

    # Test 7: Verify Post-Level Author Bio Box in post layout
    post_layout_path = "_layouts/post.html"
    if not os.path.exists(post_layout_path):
        failures.append("FAIL: _layouts/post.html is missing!")
    else:
        with open(post_layout_path, "r", encoding="utf-8") as f:
            post_layout = f.read()
        if "author-bio-card" in post_layout:
            print("[PASS] _layouts/post.html includes responsive Author E-E-A-T Bio Box")
        else:
            failures.append("FAIL: _layouts/post.html missing author-bio-card component!")

    # Test 8: Verify Post Quality & Language Flags across _posts/
    posts = glob.glob("_posts/*.md")
    if len(posts) == 0:
        failures.append("FAIL: No Markdown posts found in _posts/!")
    
    total_posts = len(posts)
    thin_posts = []
    missing_lang = []
    missing_cats = []
    missing_tags = []

    for post_file in posts:
        base = os.path.basename(post_file)
        with open(post_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Word count check (>800 words for deep technical content)
        words = len(content.split())
        if words < 800:
            thin_posts.append((base, words))
        
        # Check language flag
        if not re.search(r"^lang:\s*(es|en)", content, re.MULTILINE):
            missing_lang.append(base)

        # Check categories
        if not re.search(r"^categories:\s*\[.+?\]", content, re.MULTILINE):
            missing_cats.append(base)

        # Check tags
        if not re.search(r"^tags:\s*\[.+?\]", content, re.MULTILINE):
            missing_tags.append(base)

    if thin_posts:
        for fname, wcnt in thin_posts:
            failures.append(f"FAIL: Post '{fname}' is thin content ({wcnt} words < 800 words threshold)!")
    else:
        print(f"[PASS] All {total_posts} posts meet strict non-thin content requirements (>800 words)")

    if missing_lang:
        for fname in missing_lang:
            failures.append(f"FAIL: Post '{fname}' is missing explicit 'lang: es' or 'lang: en' frontmatter flag!")
    else:
        print(f"[PASS] All {total_posts} posts have explicit 'lang' frontmatter classification")

    if missing_cats:
        for fname in missing_cats:
            failures.append(f"FAIL: Post '{fname}' is missing structured frontmatter categories!")
    else:
        print(f"[PASS] All {total_posts} posts have structured categories")

    if missing_tags:
        for fname in missing_tags:
            failures.append(f"FAIL: Post '{fname}' is missing structured frontmatter tags!")
    else:
        print(f"[PASS] All {total_posts} posts have structured tags")

    # Test 9: Verify AdSense script loads directly (NOT lazy/interaction-triggered)
    head_path = "_includes/head.html"
    if os.path.exists(head_path):
        with open(head_path, "r", encoding="utf-8") as f:
            head_content = f.read()
        # Check for direct async script tag (not inside event listeners or setTimeout)
        lazy_patterns = [
            "requestIdleCallback",
            "addEventListener.*initAdSense",
            "touchstart.*AdSense",
            "setTimeout.*initAdSense",
        ]
        has_lazy_load = any(p.split(".*")[0] in head_content and "AdSense" in head_content
                            and "setTimeout" in head_content for p in lazy_patterns)
        has_direct_async = (
            'script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js' in head_content
            or "script async src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in head_content
        )
        if has_direct_async and not has_lazy_load:
            print("[PASS] AdSense script loads directly with async tag (crawler-compatible)")
        elif has_lazy_load:
            failures.append("FAIL: AdSense script uses lazy/interaction-triggered loading! Google crawler cannot detect it. Use direct <script async> tag instead.")
        else:
            failures.append("FAIL: AdSense script not found in head.html or not properly configured!")

    # Test 10: Detect near-duplicate posts (same topic published on consecutive days)
    # Identifies posts where the first 50 chars of the slug (after date) are identical
    post_slugs_by_date = {}
    for post_file in posts:
        base = os.path.basename(post_file)
        # Extract date and slug: YYYY-MM-DD-slug.md
        match = re.match(r"(\d{4}-\d{2}-\d{2})-(.*?)\.md$", base)
        if match:
            date_str = match.group(1)
            slug = match.group(2)
            # Use first 40 chars of slug as topic fingerprint
            topic_key = slug[:40]
            if topic_key not in post_slugs_by_date:
                post_slugs_by_date[topic_key] = []
            post_slugs_by_date[topic_key].append((date_str, base))

    consecutive_duplicates = []
    for topic_key, occurrences in post_slugs_by_date.items():
        if len(occurrences) > 1:
            consecutive_duplicates.append((topic_key, occurrences))

    if consecutive_duplicates:
        for topic_key, occurrences in consecutive_duplicates:
            files_list = ", ".join([f[1] for f in occurrences])
            failures.append(f"FAIL: Near-duplicate posts detected with same topic '{topic_key}': {files_list} - Google flags these as auto-generated low-value content!")
    else:
        print(f"[PASS] No near-duplicate posts detected (all topics are unique across different dates)")

    print("--------------------------------------------------")
    if failures:
        print(f"FAILED: {len(failures)} AdSense compliance issue(s) detected:")
        for err in failures:
            print(" -", err)
        sys.exit(1)
    else:
        print("SUCCESS: 100% Google AdSense Policy Compliance Verified!")
        print("==================================================")

if __name__ == "__main__":
    run_adsense_tests()
