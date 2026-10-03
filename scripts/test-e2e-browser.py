#!/usr/bin/env python3
"""
MACH Playbook - E2E (End-to-End) Headless Browser Automation Test Suite
Validates real browser rendering across viewports (Desktop & Mobile):
1. Zero horizontal overflow (no horizontal scrollbar / overflow-x bugs)
2. Card preview image fills 100% of .col-md-5 container on home page
3. Post hero image occupies 100% of .post-meta container with 1200/630 aspect ratio
4. Mobile layout adaptation (TOC button, fluid hero scaling)
"""

import os
import sys
import time
import json
import tempfile
import urllib.request
import subprocess
import http.server
import socketserver
import threading
import asyncio
import websockets

def run_server(port, directory):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def log_message(self, format, *args):
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        httpd.serve_forever()

async def cdp_eval(ws_url, expr):
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": expr, "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        data = json.loads(resp)
        return data.get("result", {}).get("result", {}).get("value")

async def cdp_navigate(ws_url, url, wait_seconds=3):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
        await ws.recv()
        await asyncio.sleep(wait_seconds)

def main():
    print("=" * 65)
    print("   MACH PLAYBOOK - E2E HEADLESS BROWSER AUTOMATION TEST SUITE   ")
    print("=" * 65)

    site_dir = "_site"
    if not os.path.exists(site_dir):
        print(f"ERROR: '{site_dir}' does not exist. Run jekyll build first.")
        sys.exit(1)

    port = 8895
    server_thread = threading.Thread(target=run_server, args=(port, site_dir), daemon=True)
    server_thread.start()
    time.sleep(1)

    base_url = f"http://127.0.0.1:{port}"
    failures = []
    passes = 0

    # -------------------------------------------------------------
    # 1. DESKTOP VIEWPORT E2E TESTS (1707x932)
    # -------------------------------------------------------------
    print("\n[E2E Scenario 1: Desktop Viewport 1707x932]")
    user_data_dir = tempfile.mkdtemp()
    chrome_desktop = subprocess.Popen([
        "google-chrome",
        "--headless",
        "--remote-debugging-port=9455",
        "--disable-gpu",
        "--disable-extensions",
        f"--user-data-dir={user_data_dir}",
        "--no-sandbox",
        "--window-size=1707,932",
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        tabs = json.loads(urllib.request.urlopen("http://localhost:9455/json").read().decode())
        page_tabs = [t for t in tabs if t.get("type") == "page"]
        ws_desktop = page_tabs[0]["webSocketDebuggerUrl"]

        # 1.1 Test Home Page
        asyncio.run(cdp_navigate(ws_desktop, f"{base_url}/"))
        expr_home = """(() => {
            const hasOverflow = document.documentElement.scrollWidth > window.innerWidth;
            const card = document.querySelector('.card-wrapper');
            const imgCol = card ? card.querySelector('.col-md-5') : null;
            const previewImg = imgCol ? imgCol.querySelector('.preview-img') : null;
            const rCol = imgCol ? imgCol.getBoundingClientRect() : null;
            const rImg = previewImg ? previewImg.getBoundingClientRect() : null;
            return {
                hasOverflow,
                colWidth: rCol ? Math.round(rCol.width) : 0,
                imgWidth: rImg ? Math.round(rImg.width) : 0,
                fillsCol: (rCol && rImg) ? Math.abs(rCol.width - rImg.width) <= 2 : false
            };
        })()"""
        home_res = asyncio.run(cdp_eval(ws_desktop, expr_home))
        if home_res:
            if home_res.get("hasOverflow"):
                failures.append("E2E Home Desktop: Detected horizontal overflow (scrollWidth > innerWidth)")
            else:
                print("  ✓ Home Desktop: Zero horizontal overflow verified")
                passes += 1

            if home_res.get("fillsCol"):
                print(f"  ✓ Home Desktop: Card image fills 100% of .col-md-5 ({home_res.get('imgWidth')}px / {home_res.get('colWidth')}px)")
                passes += 1
            else:
                failures.append(f"E2E Home Desktop: Image ({home_res.get('imgWidth')}px) does not fill .col-md-5 ({home_res.get('colWidth')}px)")

        # 1.2 Test Post Page
        post_url = f"{base_url}/posts/estrategias-de-pricing-dinamico-y-motores-de-promociones-desacoplados/"
        asyncio.run(cdp_navigate(ws_desktop, post_url))
        expr_post = """(() => {
            const hasOverflow = document.documentElement.scrollWidth > window.innerWidth;
            const meta = document.querySelector('.post-meta');
            const heroWrap = document.querySelector('.post-hero-image-wrapper');
            const heroImg = document.querySelector('.post-hero-image-wrapper img');
            const rMeta = meta ? meta.getBoundingClientRect() : null;
            const rWrap = heroWrap ? heroWrap.getBoundingClientRect() : null;
            const rImg = heroImg ? heroImg.getBoundingClientRect() : null;
            const ratio = (rImg && rImg.height > 0) ? (rImg.width / rImg.height).toFixed(2) : "0";
            return {
                hasOverflow,
                metaWidth: rMeta ? Math.round(rMeta.width) : 0,
                wrapWidth: rWrap ? Math.round(rWrap.width) : 0,
                imgWidth: rImg ? Math.round(rImg.width) : 0,
                ratio,
                fillsMeta: (rMeta && rWrap) ? Math.abs(rMeta.width - rWrap.width) <= 2 : false
            };
        })()"""
        post_res = asyncio.run(cdp_eval(ws_desktop, expr_post))
        if post_res:
            if post_res.get("hasOverflow"):
                failures.append("E2E Post Desktop: Detected horizontal overflow (scrollWidth > innerWidth)")
            else:
                print("  ✓ Post Desktop: Zero horizontal overflow verified")
                passes += 1

            if post_res.get("fillsMeta"):
                print(f"  ✓ Post Desktop: Hero image fills 100% of .post-meta container ({post_res.get('wrapWidth')}px / {post_res.get('metaWidth')}px)")
                passes += 1
            else:
                failures.append(f"E2E Post Desktop: Hero wrapper ({post_res.get('wrapWidth')}px) does not fill .post-meta ({post_res.get('metaWidth')}px)")

            if post_res.get("ratio") in ["1.90", "1.91", "1.92"]:
                print(f"  ✓ Post Desktop: Hero image strictly preserves 1200/630 ratio ({post_res.get('ratio')})")
                passes += 1
            else:
                failures.append(f"E2E Post Desktop: Unexpected hero image aspect ratio: {post_res.get('ratio')}")

    finally:
        chrome_desktop.kill()

    # -------------------------------------------------------------
    # 2. MOBILE VIEWPORT E2E TESTS (390x844)
    # -------------------------------------------------------------
    print("\n[E2E Scenario 2: Mobile Viewport 390x844 (iPhone / Modern Android)]")
    user_data_mobile = tempfile.mkdtemp()
    chrome_mobile = subprocess.Popen([
        "google-chrome",
        "--headless",
        "--remote-debugging-port=9456",
        "--disable-gpu",
        "--disable-extensions",
        f"--user-data-dir={user_data_mobile}",
        "--no-sandbox",
        "--window-size=390,844",
        "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    try:
        tabs_m = json.loads(urllib.request.urlopen("http://localhost:9456/json").read().decode())
        page_tabs_m = [t for t in tabs_m if t.get("type") == "page"]
        ws_mobile = page_tabs_m[0]["webSocketDebuggerUrl"]

        asyncio.run(cdp_navigate(ws_mobile, post_url))
        expr_mobile = """(() => {
            const hasOverflow = document.documentElement.scrollWidth > window.innerWidth;
            const heroImg = document.querySelector('.post-hero-image-wrapper img');
            const tocBtn = document.querySelector('#toc-solo-trigger');
            const rImg = heroImg ? heroImg.getBoundingClientRect() : null;
            return {
                hasOverflow,
                imgWidth: rImg ? Math.round(rImg.width) : 0,
                hasTocBtn: tocBtn !== null
            };
        })()"""
        mob_res = asyncio.run(cdp_eval(ws_mobile, expr_mobile))
        if mob_res:
            if mob_res.get("hasOverflow"):
                failures.append("E2E Mobile: Detected horizontal overflow on mobile viewport")
            else:
                print("  ✓ Post Mobile: Zero horizontal overflow on 390px viewport")
                passes += 1

            if mob_res.get("imgWidth") > 300:
                print(f"  ✓ Post Mobile: Hero image fluidly adapts to mobile width ({mob_res.get('imgWidth')}px)")
                passes += 1
            else:
                failures.append(f"E2E Mobile: Hero image unexpectedly small: {mob_res.get('imgWidth')}px")

            if mob_res.get("hasTocBtn"):
                print("  ✓ Post Mobile: Touch-optimized TOC trigger (#toc-solo-trigger) present for mobile users")
                passes += 1
            else:
                failures.append("E2E Mobile: Missing #toc-solo-trigger on mobile view")

    finally:
        chrome_mobile.kill()

    # -------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    if failures:
        print(f"FAILED: {len(failures)} E2E browser automation failures detected:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {passes} E2E browser automation scenarios passed with 0 errors!")
        print("=" * 65)

if __name__ == "__main__":
    main()
