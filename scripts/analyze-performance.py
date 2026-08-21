import urllib.request
from html.parser import HTMLParser

class TagAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

def audit_url(url, label):
    print(f"\n========================================================")
    print(f"   AUDIT: {label} ({url})")
    print(f"========================================================")
    html = urllib.request.urlopen(url).read().decode('utf-8')
    auditor = TagAuditor()
    auditor.feed(html)

    print(f"HTML Size: {len(html) / 1024:.1f} KB")

    # Check scripts
    scripts = [attrs for tag, attrs in auditor.tags if tag == 'script']
    print(f"\nScripts ({len(scripts)}):")
    for s in scripts:
        src = s.get('src', '[inline]')
        is_defer = 'defer' in s
        is_async = 'async' in s
        print(f"  - {src[:70]} | defer: {is_defer} | async: {is_async}")

    # Check images
    images = [attrs for tag, attrs in auditor.tags if tag == 'img']
    print(f"\nImages ({len(images)}):")
    for i, img in enumerate(images[:6]):
        print(f"  [{i+1}] src: {img.get('src', '')[:65]} | loading: {img.get('loading')} | fetchpriority: {img.get('fetchpriority')} | dims: {img.get('width')}x{img.get('height')} | style: {img.get('style')}")

    # Check preconnects
    preconnects = [attrs for tag, attrs in auditor.tags if tag == 'link' and attrs.get('rel') == 'preconnect']
    print(f"\nPreconnect Hints ({len(preconnects)}):")
    for p in preconnects:
        print(f"  - href: {p.get('href')} | crossorigin: {p.get('crossorigin', 'None')}")

if __name__ == '__main__':
    audit_url('http://localhost:8080/', 'HOME PAGE')
    audit_url('http://localhost:8080/posts/welcome-to-mach/', 'POST ARTICLE PAGE')
