import json

with open('/mnt/c/Users/lenin/.gemini/antigravity-ide/brain/d2f7dd85-7a98-4472-91dc-8f7f0c4f276c/.system_generated/tasks/task-1179.log', 'r') as f:
    text = f.read()

start = text.find('{')
end = text.rfind('}')
if start != -1 and end != -1:
    data = json.loads(text[start:end+1])
    lcp = data['audits']['largest-contentful-paint-element']
    print("LCP Element details:")
    print(json.dumps(lcp.get('details', {}), indent=2))
