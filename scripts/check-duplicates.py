import glob
import os
from difflib import SequenceMatcher

files = sorted(glob.glob('_posts/*.md'))
posts = []

for f in files:
    content = open(f, encoding='utf-8').read()
    lines = content.splitlines()
    title = ''
    lang = ''
    body_lines = []
    in_meta = False
    for l in lines:
        if l.strip() == '---':
            in_meta = not in_meta
            continue
        if in_meta:
            if l.startswith('title:'):
                title = l.split('title:', 1)[1].strip(" \"'")
            elif l.startswith('lang:'):
                lang = l.split('lang:', 1)[1].strip(" \"'")
        else:
            body_lines.append(l)
    body = ' '.join(body_lines)
    posts.append({
        'file': os.path.basename(f),
        'title': title,
        'lang': lang,
        'body': body
    })

print(f"Total posts analyzed: {len(posts)}")
spanish_posts = [p for p in posts if p['lang'] == 'es']
english_posts = [p for p in posts if p['lang'] == 'en' or not p['lang']]
print(f"English posts: {len(english_posts)}")
print(f"Spanish posts: {len(spanish_posts)}\n")

# 1. Exact / Near-Duplicate Titles
title_map = {}
duplicate_titles_found = False
for p in posts:
    t_lower = p['title'].lower()
    if t_lower in title_map:
        duplicate_titles_found = True
        print(f"[DUPLICATE TITLE DETECTED]")
        print(f"  1: {title_map[t_lower]}")
        print(f"  2: {p['file']}")
        print(f"  Title: '{p['title']}'\n")
    else:
        title_map[t_lower] = p['file']

if not duplicate_titles_found:
    print("✔ No duplicate titles found.\n")

# 2. Content Similarity Check (> 70% match)
duplicates_found = False
print("Scanning body content for high similarity matches...\n")
for i in range(len(posts)):
    for j in range(i + 1, len(posts)):
        p1 = posts[i]
        p2 = posts[j]
        
        words1 = set(p1['body'].lower().split())
        words2 = set(p2['body'].lower().split())
        
        if not words1 or not words2:
            continue
            
        jaccard = len(words1 & words2) / float(len(words1 | words2))
        
        if jaccard > 0.50:
            ratio = SequenceMatcher(None, p1['body'][:2000], p2['body'][:2000]).ratio()
            if ratio > 0.65:
                duplicates_found = True
                print(f"[HIGH SIMILARITY MATCH - {ratio*100:.1f}% Match]")
                print(f"  File A: {p1['file']} [{p1['lang'].upper()}] -> '{p1['title']}'")
                print(f"  File B: {p2['file']} [{p2['lang'].upper()}] -> '{p2['title']}'")
                print(f"  Word Overlap (Jaccard): {jaccard*100:.1f}%\n")

if not duplicates_found:
    print("✔ No duplicate body content found across all posts.")
