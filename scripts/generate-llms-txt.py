#!/usr/bin/env python3
"""
MACH Playbook - GEO (Generative Engine Optimization) Generator
Generates /llms.txt and /llms-full.txt following the llmstxt.org standard
so AI search engines (Microsoft Copilot, ChatGPT Search, Perplexity, Google AI)
accurately index all 150 deep-dive guides and interactive architecture tools.
"""

import glob
import os
import re
import yaml
from collections import defaultdict

BASE_URL = "https://mach-playbook.github.io"
PILLAR_ORDER = [
    "Arquitectura Cloud",
    "Microservicios",
    "API Design",
    "DevOps & CI/CD",
    "Headless & Frontend",
    "Security & Observability",
    "Data Engineering",
]


def extract_excerpt(body: str, max_len: int = 220) -> str:
    lines = []
    in_code = False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not s or s.startswith("#") or s.startswith("---") or s.startswith("|") or s.startswith("<") or s.startswith("!"):
            continue
        clean = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", s)
        clean = re.sub(r"[*_`>]", "", clean).strip()
        if len(clean) >= 40:
            lines.append(clean)
            break
    text = " ".join(lines)
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0].rstrip(".,;:") + "..."
    return text


def parse_posts():
    grouped = defaultdict(list)
    all_posts = []
    for path in sorted(glob.glob("_posts/*.md"), reverse=True):
        fname = os.path.basename(path)
        m_slug = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)\.md$", fname)
        if not m_slug:
            continue
        slug = m_slug.group(1)
        url = f"{BASE_URL}/posts/{slug}/"

        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        m_fm = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
        if not m_fm:
            continue

        data = yaml.safe_load(m_fm.group(1)) or {}
        body = m_fm.group(2)
        title = str(data.get("title", slug)).strip()
        lang = str(data.get("lang", "es")).strip()
        cats = data.get("categories") or ["Arquitectura Cloud"]
        pillar = cats[0] if isinstance(cats, list) and cats else str(cats)
        tags = data.get("tags") or []
        desc = str(data.get("description") or extract_excerpt(body)).strip()
        words = len(body.split())

        entry = {
            "title": title,
            "url": url,
            "lang": lang,
            "pillar": pillar,
            "tags": tags,
            "description": desc,
            "words": words,
            "date": str(data.get("date", ""))[:10],
        }
        grouped[pillar].append(entry)
        all_posts.append(entry)
    return grouped, all_posts


def generate():
    grouped, all_posts = parse_posts()

    llms_lines = [
        "# MACH Playbook",
        "",
        "> Bilingual (Spanish & English) enterprise software architecture knowledge base authored by Lenin Meza (Senior Solutions Architect), covering Microservices, API-First contracts, Cloud-Native Kubernetes, Headless Composable Commerce, Zero-Trust Security, Distributed SQL, and FinOps.",
        "",
        "## Interactive Engineering Tools & Reference Hubs",
        "",
        f"- [MACH Architecture Tools Hub]({BASE_URL}/tools/): Interactive MACH Maturity Evaluator, Infrastructure TCO & P99 Latency Simulator, and OpenAPI 3.1 + Token Bucket Rate-Limiting Policy Generator.",
        f"- [Author & Editorial Standards (E-E-A-T)]({BASE_URL}/about/): Credentials, laboratory validation methodology, and architectural review criteria.",
        f"- [MACH Technical Glossary]({BASE_URL}/glossary/): Bilingual A-Z dictionary of composable commerce and distributed systems terminology.",
        f"- [Ecosystem Resources]({BASE_URL}/resources/): Links to CNCF, MACH Alliance, OpenAPI 3.1, and AsyncAPI specifications.",
        f"- [Contact & Enterprise Advisory]({BASE_URL}/contact/): Direct engineering inquiry channel.",
        "",
    ]

    for pillar in PILLAR_ORDER:
        posts = grouped.get(pillar, [])
        if not posts:
            continue
        llms_lines.append(f"## {pillar} ({len(posts)} guides)")
        llms_lines.append("")
        for p in posts:
            llms_lines.append(f"- [{p['title']}]({p['url']}): {p['description']}")
        llms_lines.append("")

    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(llms_lines).strip() + "\n")

    full_lines = [
        "# MACH Playbook — Complete Grounding Corpus Index",
        "",
        f"Canonical Site: {BASE_URL}/",
        f"Total Technical Guides Indexed: {len(all_posts)}",
        "Languages: Spanish (es), English (en)",
        "Author: Lenin Meza (https://merolhack.github.io/)",
        "",
        "## Core Tools & Interactive Simulators",
        f"- URL: {BASE_URL}/tools/",
        "- Tools: (1) MACH Architecture Maturity Evaluator (0-100 score across 7 dimensions), (2) Monolith vs MACH vs Serverless TCO & P99 Latency Simulator, (3) OpenAPI 3.1 & Token Bucket Rate-Limiting Policy Generator.",
        "",
        "## Complete Article Catalog",
        "",
    ]
    for p in all_posts:
        full_lines.extend([
            f"### {p['title']}",
            f"- URL: {p['url']}",
            f"- Pillar: {p['pillar']} | Language: {p['lang']} | Date: {p['date']} | Length: ~{p['words']} words",
            f"- Tags: {', '.join(str(t) for t in p['tags'])}",
            f"- Summary: {p['description']}",
            "",
        ])

    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(full_lines).strip() + "\n")

    print(f"Generated llms.txt ({len(llms_lines)} lines) and llms-full.txt ({len(full_lines)} lines) covering {len(all_posts)} posts.")


if __name__ == "__main__":
    generate()
