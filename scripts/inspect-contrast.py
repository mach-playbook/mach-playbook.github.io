import json

with open('/mnt/c/Users/lenin/.gemini/antigravity-ide/brain/d2f7dd85-7a98-4472-91dc-8f7f0c4f276c/.system_generated/tasks/task-1417.log', 'r') as f:
    text = f.read()

start = text.find('{')
end = text.rfind('}')
if start != -1 and end != -1:
    data = json.loads(text[start:end+1])
    contrast = data['audits']['color-contrast']
    print("Color contrast details:")
    print(json.dumps(contrast.get('details', {}), indent=2))
