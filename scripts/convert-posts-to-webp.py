import glob
import os
import re

posts = glob.glob('/home/merolhack/fl/mach-playbook/_posts/*.md')
updated = 0

for p in posts:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'path:\s*(/assets/img/posts/[^ \n\r\t]+)\.png', r'path: \1.webp', content)
    if new_content != content:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1

print(f"Updated {updated} posts to use .webp images natively!")
