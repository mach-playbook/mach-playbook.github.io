import xml.etree.ElementTree as ET
import urllib.request

url = 'https://mach-playbook.github.io/sitemap.xml'
req = urllib.request.urlopen(url)
xml_data = req.read()

root = ET.fromstring(xml_data)
urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

with open('urls_list.txt', 'w') as f:
    for u in urls:
        f.write(u + '\n')

print(f"Total extracted URLs: {len(urls)}")
print("Sample URLs:")
for u in urls[:15]:
    print(" -", u)
