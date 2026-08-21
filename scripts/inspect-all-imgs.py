import urllib.request
import re

url = 'https://mach-playbook.github.io/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("ALL IMGS IN PRODUCTION HTML:")
for idx, i in enumerate(re.findall(r'<img[^>]*>', html)):
    print(f"  {idx+1}: {i}")
