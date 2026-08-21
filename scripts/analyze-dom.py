import re
from html.parser import HTMLParser
from collections import Counter

class TagCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.stack = []
        self.parents = Counter()

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        parent = self.stack[-1] if self.stack else 'root'
        self.parents[parent] += 1
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

with open('/home/merolhack/fl/mach-playbook/_site/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

parser = TagCounter()
parser.feed(content)

print(f"Total HTML Tags: {len(parser.tags)}")
print("\nTop 15 most frequent tags:")
for tag, count in Counter(parser.tags).most_common(15):
    print(f"  <{tag}>: {count}")

print("\nTop 10 parents with most direct child tags:")
for parent, count in parser.parents.most_common(10):
    print(f"  <{parent}>: {count} children")
