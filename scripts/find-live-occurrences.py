import urllib.request

url = 'https://mach-playbook.github.io/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

for line in html.splitlines():
    if '2026-08-14-asyncapi' in line:
        print(line.strip())
