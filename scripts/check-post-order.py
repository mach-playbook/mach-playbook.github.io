from html.parser import HTMLParser

class PostOrderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_h1 = False
        self.titles = []
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'h1' and 'card-title' in attrs_dict.get('class', ''):
            self.in_h1 = True
        if tag == 'img' and 'assets/img/posts/' in attrs_dict.get('src', ''):
            self.imgs.append(attrs_dict.get('src'))

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.titles.append(data.strip())

parser = PostOrderParser()
with open('/home/merolhack/fl/mach-playbook/_site/index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())

print("First 5 posts in HTML:")
for i, title in enumerate(parser.titles[:5]):
    img = parser.imgs[i] if i < len(parser.imgs) else 'no img'
    print(f"  {i+1}. {title} -> {img}")
