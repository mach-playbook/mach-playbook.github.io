import urllib.request
import json
import sys

def check_pagespeed(url="https://mach-playbook.github.io/"):
    strategies = ["mobile", "desktop"]
    for strategy in strategies:
        print(f"\n========================================================")
        print(f"   PAGE SPEED INSIGHTS REPORT: {strategy.upper()} ")
        print(f"   Target: {url}")
        print(f"========================================================")
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}&category=performance&category=accessibility&category=best-practices&category=seo"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                lh = data.get("lighthouseResult", {})
                cats = lh.get("categories", {})
                perf = cats.get("performance", {}).get("score", 0) * 100
                accessibility = cats.get("accessibility", {}).get("score", 0) * 100
                best_practices = cats.get("best-practices", {}).get("score", 0) * 100
                seo = cats.get("seo", {}).get("score", 0) * 100
                
                audits = lh.get("audits", {})
                fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")
                lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
                tbt = audits.get("total-blocking-time", {}).get("displayValue", "N/A")
                cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
                si = audits.get("speed-index", {}).get("displayValue", "N/A")
                
                print(f"SCORES:")
                print(f"  ⚡ Performance:    {perf:.0f}/100")
                print(f"  ♿ Accessibility:  {accessibility:.0f}/100")
                print(f"  🛡️ Best Practices: {best_practices:.0f}/100")
                print(f"  🔍 SEO:            {seo:.0f}/100")
                print(f"\nCORE WEB VITALS & TIMINGS:")
                print(f"  * First Contentful Paint (FCP): {fcp}")
                print(f"  * Largest Contentful Paint (LCP): {lcp}")
                print(f"  * Total Blocking Time (TBT):     {tbt}")
                print(f"  * Cumulative Layout Shift (CLS): {cls}")
                print(f"  * Speed Index (SI):              {si}")
                
                print(f"\nOPPORTUNITIES & DIAGNOSTICS:")
                for audit_id, audit in audits.items():
                    score = audit.get("score")
                    mode = audit.get("scoreDisplayMode")
                    if score is not None and score < 0.9 and mode not in ["notApplicable", "informative", "manual"]:
                        title = audit.get("title", audit_id)
                        disp = audit.get("displayValue", "")
                        print(f"  ❌ [{score:.2f}] {title} {('- ' + disp) if disp else ''}")
                        if "details" in audit and "items" in audit["details"]:
                            items = audit["details"]["items"]
                            for item in items[:5]:
                                if isinstance(item, dict):
                                    u = item.get("url") or item.get("source") or item.get("node", {}).get("snippet") or item.get("label")
                                    wasted = item.get("wastedBytes") or item.get("wastedMs")
                                    extra = f" (wasted: {wasted})" if wasted else ""
                                    if u:
                                        print(f"       -> {str(u)[:90]}{extra}")
        except Exception as e:
            print(f"Error fetching PSI for {strategy}: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://mach-playbook.github.io/"
    check_pagespeed(target)
