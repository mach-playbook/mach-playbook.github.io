import urllib.request
import re

url = 'https://mach-playbook.github.io/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("PRELOADS IN PRODUCTION:")
for p in re.findall(r'<link[^>]*preload[^>]*>', html):
    print(" ", p)

print("\nFIRST 4 IMGS IN PRODUCTION:")
for i in re.findall(r'<img[^>]*>', html)[:4]:
    print(" ", i)
