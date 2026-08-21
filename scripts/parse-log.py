import json
import sys

def parse(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        text = f.read()

    start = text.find('{')
    if start != -1:
        data = json.loads(text[start:])
        cats = data.get('categories', {})
        print("==================================================")
        print("   LIGHTHOUSE SCORES (MOBILE)")
        print("==================================================")
        for k, v in cats.items():
            print(f"  * {k.upper()}: {v.get('score', 0) * 100:.0f}/100")

        audits = data.get('audits', {})
        print("\nCORE WEB VITALS:")
        for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
            print(f"  * {m}: {audits.get(m, {}).get('displayValue')} (score: {audits.get(m, {}).get('score')})")

        print("\nOPPORTUNITIES & DIAGNOSTICS (< 0.9):")
        for k, a in audits.items():
            score = a.get('score')
            if score is not None and score < 0.9 and a.get('scoreDisplayMode') not in ['notApplicable', 'informative', 'manual']:
                print(f"* [{score:.2f}] {a.get('title')}: {a.get('displayValue', '')}")
                details = a.get('details', {})
                if 'items' in details:
                    for item in details['items'][:4]:
                        if isinstance(item, dict):
                            u = item.get('url') or item.get('source') or item.get('label') or str(item)[:60]
                            w = item.get('wastedBytes') or item.get('wastedMs')
                            extra = f" (wasted: {w})" if w else ""
                            print(f"    - {str(u)[:85]}{extra}")

if __name__ == '__main__':
    log = sys.argv[1] if len(sys.argv) > 1 else '/mnt/c/Users/lenin/.gemini/antigravity-ide/brain/d2f7dd85-7a98-4472-91dc-8f7f0c4f276c/.system_generated/tasks/task-392.log'
    parse(log)
