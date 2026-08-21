import json

with open('/mnt/c/Users/lenin/.gemini/antigravity-ide/brain/d2f7dd85-7a98-4472-91dc-8f7f0c4f276c/.system_generated/tasks/task-1417.log', 'r') as f:
    text = f.read()

start = text.find('{')
end = text.rfind('}')
if start != -1 and end != -1:
    data = json.loads(text[start:end+1])
    net = data['audits']['network-requests']['details']['items']
    print(f"Total network requests: {len(net)}")
    for item in net:
        print(f"[{item.get('resourceType')}] {item.get('transferSize', 0)/1024:.1f} KB | {item.get('url')[:100]} | Time: {item.get('networkRequestTime', 0):.0f}ms - {item.get('networkEndTime', 0):.0f}ms")
