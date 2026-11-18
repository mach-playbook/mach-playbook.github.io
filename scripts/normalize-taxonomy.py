#!/usr/bin/env python3
"""
MACH Playbook - Canonical Taxonomy Normalizer & SEO Title Enforcer
Normalizes all posts in _posts/*.md to:
  - Exactly 1 primary category from the 7 Canonical MACH Pillars
  - 4 to 6 high-density tags strictly from the 21 Canonical Tags
  - Clean inline YAML format ([item1, item2]) compatible with compliance tests
  - Concise seo_title (<= 66 chars) whenever title length > 68 chars
"""

import glob
import os
import re
import yaml

CANONICAL_CATEGORIES = [
    "Arquitectura Cloud",
    "Microservicios",
    "API Design",
    "DevOps & CI/CD",
    "Headless & Frontend",
    "Security & Observability",
    "Data Engineering",
]

CANONICAL_TAGS = [
    "cloud-native",
    "microservices",
    "architecture",
    "headless",
    "api-first",
    "devops",
    "gcp",
    "data-engineering",
    "qa-automation",
    "distributed-systems",
    "postgresql",
    "observability",
    "ci-cd",
    "finops",
    "security",
    "ai-engineering",
    "aws",
    "event-driven",
    "telecom",
    "kubernetes",
    "nextjs",
]

# Curated SEO titles (<= 65 chars) for Bing-flagged & top-priority posts
CURATED_SEO_TITLES = {
    "2026-08-03-ci-cd-microservicios-multi-repositorio.md": "CI/CD para Microservicios en Entornos Multi-Repositorio",
    "2026-04-04-clean-rest-api-design-practical-rules-for-modern-backend-engineers.md": "Clean REST API Design: Practical Rules for Backend Engineers",
    "2026-08-16-modelado-y-delimitacion-de-packaged-business-capabilities-pbcs-en-comercio-digital.md": "Modelado de Packaged Business Capabilities (PBCs) en MACH",
    "2026-07-28-seguridad-zero-trust-microservicios-mach.md": "Seguridad Zero Trust y mTLS en Microservicios MACH Cloud",
    "2026-04-04-the-strangler-fig-pattern-migrating-a-monolith-without-a-big-bang-rewrite.md": "Strangler Fig Pattern: Migrating Monoliths Without Rewrites",
    "2026-04-04-video-review-martin-fowler-on-microservices-key-takeaways.md": "Video Review: Martin Fowler on Microservices Key Takeaways",
    "2026-08-23-platform-engineering-backstage-idp-interno.md": "Microservicios con Backstage: Guía IDP, YAML y QA Testing",
    "2026-09-13-estrategias-de-rate-limiting-adaptativo-y-algoritmos-token-bucket-en-api-gateways.md": "Algoritmo Token Bucket y Rate Limiting Adaptativo en APIs",
    "2026-09-15-migracion-y-versionado-no-destructivo-de-apis-restful-en-entornos-empresariales.md": "Versionado y Migración No Destructiva de APIs RESTful",
}

TAG_ALIASES = {
    "mach": "architecture",
    "mach-architecture": "architecture",
    "arquitectura": "architecture",
    "arquitectura-cloud": "cloud-native",
    "microservicios": "microservices",
    "composable-commerce": "headless",
    "ecommerce": "headless",
    "pbcs": "architecture",
    "frontend": "headless",
    "core-web-vitals": "headless",
    "performance": "cloud-native",
    "edge-computing": "cloud-native",
    "edge": "cloud-native",
    "cdn": "cloud-native",
    "zero-trust": "security",
    "seguridad": "security",
    "mtls": "security",
    "oauth2": "security",
    "jwt": "security",
    "owasp": "security",
    "spiffe": "security",
    "vault": "security",
    "cfdi": "security",
    "pci-dss": "security",
    "api-gateway": "api-first",
    "openapi": "api-first",
    "graphql": "api-first",
    "rest": "api-first",
    "restful": "api-first",
    "grpc": "api-first",
    "rate-limiting": "api-first",
    "token-bucket": "api-first",
    "versionado-api": "api-first",
    "apigee": "api-first",
    "mulesoft": "api-first",
    "contract-testing": "qa-automation",
    "pact": "qa-automation",
    "playwright": "qa-automation",
    "testing": "qa-automation",
    "e2e": "qa-automation",
    "kafka": "event-driven",
    "debezium": "event-driven",
    "cdc": "event-driven",
    "outbox": "event-driven",
    "saga": "event-driven",
    "cqrs": "event-driven",
    "webhooks": "event-driven",
    "asyncapi": "event-driven",
    "rabbitmq": "event-driven",
    "event-streams": "event-driven",
    "resiliencia": "distributed-systems",
    "resilience": "distributed-systems",
    "consistencia": "distributed-systems",
    "consistency": "distributed-systems",
    "circuit-breaker": "distributed-systems",
    "bulkhead": "distributed-systems",
    "sistemas-distribuidos": "distributed-systems",
    "sharding": "postgresql",
    "database": "postgresql",
    "yugabytedb": "postgresql",
    "sql": "postgresql",
    "redis": "distributed-systems",
    "etl": "data-engineering",
    "bigquery": "data-engineering",
    "databricks": "data-engineering",
    "analytics": "data-engineering",
    "opentelemetry": "observability",
    "telemetry": "observability",
    "logging": "observability",
    "tracing": "observability",
    "prometheus": "observability",
    "grafana": "observability",
    "gitops": "ci-cd",
    "argocd": "ci-cd",
    "github-actions": "ci-cd",
    "blue-green": "ci-cd",
    "canary": "ci-cd",
    "feature-flags": "ci-cd",
    "docker": "kubernetes",
    "istio": "kubernetes",
    "service-mesh": "kubernetes",
    "keda": "kubernetes",
    "cloud-run": "gcp",
    "google-cloud": "gcp",
    "ollama": "ai-engineering",
    "llm": "ai-engineering",
    "ia": "ai-engineering",
    "rag": "ai-engineering",
    "voip": "telecom",
    "sip": "telecom",
    "opensips": "telecom",
    "webrtc": "telecom",
    "roi": "finops",
    "cost-optimization": "finops",
    "costo": "finops",
    "enterprise": "architecture",
    "strategy": "architecture",
    "estrategia": "architecture",
    "backstage": "devops",
    "idp": "devops",
    "platform-engineering": "devops",
    "developer-experience": "devops",
    "terraform": "devops",
    "supabase": "nextjs",
    "react": "nextjs",
    "pwa": "nextjs",
}

PILLAR_DEFAULT_TAGS = {
    "Security & Observability": ["security", "observability", "cloud-native", "microservices", "architecture"],
    "DevOps & CI/CD": ["devops", "ci-cd", "kubernetes", "cloud-native", "architecture"],
    "API Design": ["api-first", "microservices", "architecture", "cloud-native", "security"],
    "Data Engineering": ["data-engineering", "postgresql", "distributed-systems", "cloud-native", "architecture"],
    "Headless & Frontend": ["headless", "nextjs", "api-first", "cloud-native", "architecture"],
    "Microservicios": ["microservices", "distributed-systems", "event-driven", "cloud-native", "architecture"],
    "Arquitectura Cloud": ["cloud-native", "architecture", "microservices", "distributed-systems", "devops"],
}


def classify_pillar(cats, tags, title, slug):
    text = " ".join([str(c) for c in cats] + [str(t) for t in tags] + [title, slug]).lower()
    if any(k in text for k in ["zero trust", "zero-trust", "mtls", "spiffe", "owasp", "oauth", "jwt", "vault", "cfdi", "pci-dss", "observabilidad", "observability", "opentelemetry", "trazabilidad", "seguridad", "security", "fraude", "fraud", "opensips", "voip"]):
        return "Security & Observability"
    if any(k in text for k in ["ci/cd", "ci-cd", "devops", "gitops", "argocd", "canary", "blue-green", "bluegreen", "kubernetes", "docker", "backstage", "idp", "platform engineering", "playwright", "qa", "contract testing", "pact", "feature flag", "chaos", "toxiproxy"]):
        return "DevOps & CI/CD"
    if any(k in text for k in ["api ", "apis", "api-", "openapi", "asyncapi", "graphql", "grpc", "rest", "rate limiting", "token bucket", "apigee", "mulesoft", "versionado", "gateway", "webhook"]):
        return "API Design"
    if any(k in text for k in ["database", "base de datos", "bases de datos", "sharding", "postgres", "yugabytedb", "sql", "cqrs", "outbox", "debezium", "cdc", "data ", "datos", "etl", "rag", "búsqueda semántica", "busquedas semanticas"]):
        return "Data Engineering"
    if any(k in text for k in ["headless", "frontend", "nextjs", "next.js", "supabase", "cms", "composable commerce", "comercio", "checkout", "sephora", "nike", "edge", "cdn", "pwa", "offline-first", "dxp", "retail"]):
        return "Headless & Frontend"
    if any(k in text for k in ["microservicio", "microservice", "saga", "circuit breaker", "bulkhead", "strangler", "monolito", "monolith", "bounded context", "ddd", "event-driven", "kafka", "idempotenc", "fallback", "pbc", "fowler", "netflix"]):
        return "Microservicios"
    return "Arquitectura Cloud"


def map_tags(raw_tags, title, slug, pillar):
    mapped = []
    # 1. Map raw tags via exact match or alias
    for t in raw_tags:
        clean = str(t).strip().lower().replace("_", "-")
        if clean in CANONICAL_TAGS and clean not in mapped:
            mapped.append(clean)
        elif clean in TAG_ALIASES:
            alias = TAG_ALIASES[clean]
            if alias not in mapped:
                mapped.append(alias)

    # 2. Enrich from title/slug keywords
    text = f"{title} {slug}".lower()
    keyword_map = [
        ("kubernetes", ["kubernetes", "k8s", "argocd", "istio", "helm", "keda"]),
        ("gcp", ["gcp", "cloud run", "bigquery", "spanner", "google cloud"]),
        ("aws", ["aws", "lambda", "dynamodb", "s3"]),
        ("finops", ["finops", "costo", "cost", "roi", "factura", "presupuesto", "saas"]),
        ("ai-engineering", ["ia", "ai ", "ollama", "llm", "gemini", "rag", "semántic", "semantic", "grafo", "mcp"]),
        ("telecom", ["voip", "sip", "opensips", "asterisk", "telecom", "gateway voip"]),
        ("postgresql", ["postgres", "sql", "yugabyte", "sharding", "bbdd"]),
        ("event-driven", ["kafka", "event", "evento", "outbox", "debezium", "cdc", "saga", "async"]),
        ("security", ["seguridad", "security", "zero trust", "mtls", "jwt", "oauth", "owasp", "cfdi", "pci"]),
        ("observability", ["observabilidad", "observability", "opentelemetry", "traza", "rum", "telemetr"]),
        ("qa-automation", ["playwright", "qa", "testing", "pact", "e2e", "chaos"]),
        ("nextjs", ["next.js", "nextjs", "react", "supabase"]),
        ("ci-cd", ["ci/cd", "ci-cd", "canary", "blue-green", "bluegreen", "gitops", "feature flag"]),
        ("api-first", ["api", "openapi", "graphql", "grpc", "rest", "token bucket", "rate limit", "apigee", "mulesoft"]),
        ("headless", ["headless", "composable", "checkout", "cms", "dxp", "frontend"]),
        ("data-engineering", ["data", "datos", "etl", "analytics", "cqrs"]),
    ]
    for tag, keywords in keyword_map:
        if len(mapped) >= 6:
            break
        if any(kw in text for kw in keywords) and tag not in mapped:
            mapped.append(tag)

    # 3. Ensure at least 4 tags using pillar defaults
    for default_tag in PILLAR_DEFAULT_TAGS[pillar]:
        if len(mapped) >= 5:
            break
        if default_tag not in mapped:
            mapped.append(default_tag)

    return mapped[:6]


def make_seo_title(filename, title):
    if filename in CURATED_SEO_TITLES:
        return CURATED_SEO_TITLES[filename]
    if len(title) <= 68:
        return None

    # Prefer cutting cleanly before ':' or '—' or '-' if that yields a strong 32-66 char title
    for sep in [": ", " — ", " - "]:
        if sep in title:
            parts = title.split(sep, 1)
            candidate = parts[0].strip()
            if 28 <= len(candidate) <= 66:
                return candidate
            # Or try adding shortened second half up to 66 chars
            combined = f"{parts[0].strip()}: {parts[1].strip()}" if sep == ": " else title
            if len(combined) <= 66:
                return combined

    # Clean word-boundary cut <= 66 chars
    words = title.split()
    out = []
    for w in words:
        candidate = " ".join(out + [w])
        if len(candidate) > 66:
            break
        out.append(w)
    res = " ".join(out).rstrip(" :-–—,;(")
    if res.count("(") > res.count(")"):
        res = res.rsplit("(", 1)[0].rstrip(" :-–—,;(")
    return res[:66]


def main():
    post_files = sorted(glob.glob("_posts/*.md"))
    updated = 0
    seo_added = 0
    all_cats = set()
    all_tags = set()

    for path in post_files:
        fname = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()

        match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
        if not match:
            print(f"[WARN] Could not parse frontmatter in {fname}")
            continue

        fm_text = match.group(1)
        body = match.group(2)
        data = yaml.safe_load(fm_text) or {}

        title = str(data.get("title", "")).strip()
        raw_cats = data.get("categories") or []
        raw_tags = data.get("tags") or []
        if isinstance(raw_cats, str):
            raw_cats = [raw_cats]
        if isinstance(raw_tags, str):
            raw_tags = [raw_tags]

        pillar = classify_pillar(raw_cats, raw_tags, title, fname)
        new_tags = map_tags(raw_tags, title, fname, pillar)
        all_cats.add(pillar)
        all_tags.update(new_tags)

        new_fm = fm_text
        cats_line = f"categories: [{pillar}]"
        tags_line = f"tags: [{', '.join(new_tags)}]"

        if re.search(r"^categories:\s*.*$", new_fm, re.MULTILINE):
            new_fm = re.sub(r"^categories:\s*.*$", cats_line, new_fm, count=1, flags=re.MULTILINE)
        else:
            new_fm += f"\n{cats_line}"

        if re.search(r"^tags:\s*.*$", new_fm, re.MULTILINE):
            new_fm = re.sub(r"^tags:\s*.*$", tags_line, new_fm, count=1, flags=re.MULTILINE)
        else:
            new_fm += f"\n{tags_line}"

        seo_title = make_seo_title(fname, title)
        if seo_title:
            safe_seo = seo_title.replace('"', "'")
            seo_line = f'seo_title: "{safe_seo}"'
            if re.search(r"^seo_title:\s*.*$", new_fm, re.MULTILINE):
                new_fm = re.sub(r"^seo_title:\s*.*$", seo_line, new_fm, count=1, flags=re.MULTILINE)
            else:
                new_fm = re.sub(r"^(title:\s*.*)$", r"\1\n" + seo_line, new_fm, count=1, flags=re.MULTILINE)
            seo_added += 1

        new_raw = f"---\n{new_fm}\n---\n{body}"
        if new_raw != raw:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_raw)
            updated += 1

    print(f"Processed {len(post_files)} posts | Updated: {updated} | With seo_title: {seo_added}")
    print(f"Canonical Categories Used ({len(all_cats)}): {sorted(all_cats)}")
    print(f"Canonical Tags Used ({len(all_tags)}): {sorted(all_tags)}")


if __name__ == "__main__":
    main()
