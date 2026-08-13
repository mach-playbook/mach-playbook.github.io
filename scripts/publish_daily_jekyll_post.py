#!/usr/bin/env python3
"""
MACH Playbook - Autonomous Daily Post Publisher with Gemini AI
Author: Lenin Meza (merolhack)
Description:
  Automated agent workflow that scans existing Jekyll blog posts for deduplication,
  selects an architectural topic across 5 MACH/Composable Commerce pillars,
  prompts Google Gemini for a Senior Solutions Architect-level article (1,500-2,200 words)
  with E-E-A-T rigor, Mermaid diagrams, and code snippets, and creates the formatted
  Jekyll markdown file ready for GitHub Pages CI/CD.
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys
import unicodedata
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error

# Supported Gemini models in priority fallback order
DEFAULT_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest"
]

# 5 Core Pillars of MACH Playbook Topic Matrix
TOPIC_MATRIX = {
    "Microservicios & Cloud Native": [
        "Patrón Outbox Transaccional y Debezium en Arquitecturas de Microservicios Distribuidas",
        "Resiliencia y Circuit Breaking Avanzado con Envoy Proxy e Istio Service Mesh",
        "Estrategias de Sharding y Escalabilidad Horizontal en Bases de Datos SQL Distribuidas",
        "Orquestación de Sagas Asíncronas con Temporal.io y Apache Kafka",
        "Gobernanza de Seguridad Zero Trust y mTLS en Clústeres Kubernetes Multi-Tenant",
        "Observabilidad Cardinal con OpenTelemetry, Jaeger y Métricas RED en Microservicios",
        "Optimización de Cold Starts y Conexiones Pooling en Serverless con Google Cloud Run y AWS Lambda",
        "Estrategias de Despliegue Canary y Blue/Green con ArgoCD y Flagger en Kubernetes",
        "Aislamiento de Cargas y Bulkhead Pattern en Microservicios de Alta Concurrencia",
        "Patrones de Caché Distribuida con Redis Cluster y Consistencia Eventual"
    ],
    "API-First & Integraciones": [
        "Federación de GraphQL (Apollo Federation) vs REST Gateway en Ecosistemas Composable",
        "Diseño de Contratos API con OpenAPI v3.1 y Validación de Schemas en CI/CD",
        "Idempotencia de Pagos y Webhooks Distribuidos con Colas Dead-Letter (DLQ)",
        "Estrategias de Rate Limiting Adaptativo y Algoritmos Token Bucket en API Gateways",
        "Migración y Versionado No Destructivo de APIs RESTful en Entornos Empresariales",
        "AsyncAPI para la Gobernanza de Event Streams y Webhooks en Tiempo Real",
        "Diseño de APIs de Alto Rendimiento con gRPC y Protocol Buffers para Comunicación Interna",
        "Seguridad de APIs: Prevención de OWASP API Top 10 y Manejo Seguro de Tokens JWT",
        "Traducción y Mediación de Protocolos en Edge Gateways (HTTP/3, WebSockets, SSE)",
        "Gobernanza de APIs: Pruebas de Contrato Automatizadas con Pact en Pipelines CI/CD"
    ],
    "Headless & Frontend Moderno": [
        "Optimización de Core Web Vitals (INP, LCP) en Frontends Composable con Next.js e ISR",
        "Estrategias de Caché Edge y Purgado Granular con Cloudflare Workers y Fastly Compute",
        "Integración de CMS Headless Multi-Tenant (Contentful, Strapi, Sanity) en E-Commerce Global",
        "Micro-Frontends con Module Federation: Modularización sin Pérdida de Rendimiento",
        "Estrategias de Hidratación Parcial y Server Components en Arquitecturas Headless",
        "Búsqueda Composable Instantánea: Integración de Algolia / Meilisearch con Catálogos Dinámicos",
        "Diseño de Sistemas de Diseño (Design Systems) Headless Desacoplados de la Lógica de Negocio",
        "State Management y Offline-First en Progressive Web Apps (PWA) de Alto Tráfico",
        "Monitoreo de Rendimiento Real (RUM) y Telemetría de Usuario en Tiendas Headless",
        "Internacionalización Dinámica y Localización Geo-Distribuida en Frontends Composable"
    ],
    "Composable Commerce & Transición": [
        "Patrón Strangler Fig: Cómo Desmantelar un Monolito SAP Commerce o Magento Paso a Paso",
        "Modelado y Delimitación de Packaged Business Capabilities (PBCs) en Comercio Digital",
        "Orquestación de Checkout Composable y Pasarelas de Pago Multi-Adquirente",
        "Gestión de Inventario en Tiempo Real y Consistencia Distribuida en Composable Commerce",
        "Transición de Catálogos Monolíticos a Motores Composable PIM (Akeneo, Pimcore)",
        "Estrategias de Pricing Dinámico y Motores de Promociones Desacoplados",
        "Gestión de Devoluciones y Logística Inversa en Arquitecturas de Comercio Desacoplado",
        "Composable B2B Commerce: Reglas Complejas de Precios y Cuentas Corporativas",
        "Migración de Salesforce Commerce Cloud a Stack MACH: Lecciones Aprendidas y Trade-offs",
        "Orquestación de Carritos de Compra Distribuidos y Manejo de Concurrencia Masiva"
    ],
    "Estrategia Enterprise, FinOps & ROI": [
        "Cómo Justificar el ROI de una Arquitectura MACH ante el C-Level y Comité de Dirección",
        "FinOps para MACH: Control de Costos y Optimización de Facturación Multi-Vendor",
        "Cómo Evitar la Trampa del 'Monolito Distribuido': Señales de Alerta y Remediación",
        "Matriz de Decisión: Construir vs Comprar (Build vs Buy) en Ecosistemas Composable",
        "Gestión de Proveedores (Vendor Lock-in Mitigation) en Contratos SaaS de Arquitectura MACH",
        "Estructura Organizacional: Equipos Stream-Aligned e Inversión Conway en Equipos MACH",
        "Acuerdos de Nivel de Servicio (SLA) Agregados en Cadenas de Dependencias Multi-SaaS",
        "Auditoría y Cumplimiento Normativo (PCI-DSS, GDPR, SOC2) en Plataformas Composable",
        "Métricas Clave de Éxito Técnico y de Negocio Post-Migración Composable (DORA + KPIs)",
        "Gestión del Cambio Cultural y Capacitación de Equipos de Ingeniería Tradicionales a MACH"
    ]
}


def slugify(text: str) -> str:
    """Generate a clean, SEO-friendly ASCII slug from a title string."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[-\s]+', '-', text)


def scan_existing_posts(posts_dir: str = "_posts") -> List[Dict[str, str]]:
    """Scan existing Markdown posts to extract titles, filenames, languages, and slugs for deduplication."""
    post_files = sorted(glob.glob(os.path.join(posts_dir, "*.md")))
    existing_posts = []

    for fpath in post_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract YAML front matter
            title_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?\s*$", content, re.MULTILINE)
            lang_match = re.search(r"^lang:\s*['\"]?(.*?)['\"]?\s*$", content, re.MULTILINE)
            categories_match = re.search(r"^categories:\s*\[(.*?)\]", content, re.MULTILINE)
            
            title = title_match.group(1).strip() if title_match else ""
            lang = lang_match.group(1).strip() if lang_match else "es"
            categories = [c.strip(" '\"") for c in categories_match.group(1).split(",")] if categories_match else []
            
            existing_posts.append({
                "file": os.path.basename(fpath),
                "title": title,
                "lang": lang,
                "categories": categories,
                "slug": os.path.basename(fpath).replace(".md", "")
            })
        except Exception as e:
            print(f"Warning: Failed to parse {fpath}: {e}")

    return existing_posts


def select_next_topic(existing_posts: List[Dict[str, str]], manual_topic: Optional[str] = None) -> Tuple[str, str]:
    """Select a fresh, untackled topic balancing the 5 pillars, or use manual topic if provided."""
    if manual_topic:
        return manual_topic, "Arquitectura Cloud & Microservicios"

    existing_titles_lower = [p["title"].lower() for p in existing_posts if p["title"]]
    existing_slugs_lower = [p["slug"].lower() for p in existing_posts]

    # Find the first untackled topic in the matrix
    for pillar, topics in TOPIC_MATRIX.items():
        for topic in topics:
            topic_clean = topic.lower()
            topic_slug = slugify(topic)
            
            # Check if title or slug overlaps significantly
            is_covered = any(
                topic_slug in s or s in topic_slug or
                any(word in s for word in topic_slug.split("-") if len(word) > 5)
                for s in existing_slugs_lower
            ) or any(topic_clean in t or t in topic_clean for t in existing_titles_lower)
            
            if not is_covered:
                return topic, pillar

    # Fallback to an advanced dynamic variation if all standard topics are covered
    timestamp_seed = datetime.datetime.now().strftime("%Y%m%d")
    fallback_topic = f"Patrones Avanzados de Resiliencia y Consistencia en Arquitecturas MACH - Edición {timestamp_seed}"
    return fallback_topic, "Arquitectura Cloud & Microservicios"


def build_system_prompt(lang: str = "es") -> str:
    """Build the comprehensive Senior Solutions Architect system prompt with E-E-A-T guidelines."""
    if lang == "es":
        return """Eres un Principal Enterprise Solutions Architect y especialista certificado en Arquitectura MACH (Microservices, API-first, Cloud-native, Headless) y Composable Commerce.
Escribes artículos técnicos de altísimo nivel para 'MACH Playbook' (mach-playbook.github.io).

DIRECTRICES EDITORIALES Y DE CALIDAD (E-E-A-T):
1. **Profundidad Técnica y Experiencia Real:** No te limites a explicaciones teóricas superficiales. Proporciona ejemplos prácticos de arquitectura, patrones de diseño de producción, trade-offs reales y métricas de desempeño.
2. **Extensión:** Entre 1,500 y 2,200 palabras. El contenido debe ser exhaustivo, estructurado y sin texto de relleno.
3. **Estructura Requerida:**
   - Título impactante y profesional.
   - Front Matter YAML compatible con Jekyll tema Chirpy al inicio del archivo.
   - Introducción con planteamiento del problema en el mundo real (dolores de empresas enterprise).
   - Diagrama de arquitectura o secuencia en sintaxis Mermaid (```mermaid).
   - Bloques de código reales, ejecutables y documentados (TypeScript, Python, YAML, Go o SQL).
   - Tablas comparativas de trade-offs arquitectónicos (pros, contras, cuándo usarlo, cuándo evitarlo).
   - Modos de fallo comunes y estrategias de mitigación/recuperación en producción.
   - Conclusión accionable con checklist de implementación para equipos de ingeniería.
4. **Formato Front Matter de Jekyll:**
---
layout: post
title: "Título Exacto Entre Comillas"
date: YYYY-MM-DD HH:MM:SS -0600
lang: es
categories: [Categoría Principal, Subcategoría]
tags: [tag1, tag2, tag3, tag4, tag5, tag6]
image:
  path: /assets/img/posts/YYYY-MM-DD-slug.png
---
5. **Idioma:** Español técnico impecable, fluido y profesional, utilizando la terminología estándar de la industria cloud/software (ej: 'throughput', 'bounded context', 'event-driven', 'failover', 'dead-letter queue').
"""
    else:
        return """You are a Principal Enterprise Solutions Architect and MACH Alliance Certified Specialist (Microservices, API-first, Cloud-native, Headless) and Composable Commerce expert.
You write authoritative technical deep-dives for 'MACH Playbook' (mach-playbook.github.io).

EDITORIAL GUIDELINES (E-E-A-T):
1. **Technical Depth & Real-World Experience:** Provide concrete production architecture patterns, design tradeoffs, performance metrics, and actionable blueprints.
2. **Length:** Between 1,500 and 2,200 words. Exhaustive, well-structured, zero fluff.
3. **Required Elements:**
   - Jekyll Chirpy-compliant YAML Front Matter at the very beginning.
   - Real-world problem statement and enterprise challenges.
   - Architecture or sequence diagram in Mermaid syntax (```mermaid).
   - Production-grade, documented code snippets (TypeScript, Python, YAML, Go, or SQL).
   - Comparative tradeoff table (Pros, Cons, When to use, When to avoid).
   - Failure modes and production mitigation strategies.
   - Actionable conclusion with engineering implementation checklist.
4. **Language:** Professional, highly technical English.
"""


def build_user_prompt(topic: str, pillar: str, existing_posts: List[Dict[str, str]], post_date_str: str, slug: str, lang: str = "es") -> str:
    """Build the user prompt instructing Gemini on the exact post to generate."""
    existing_titles_summary = "\n".join([f"- {p['title']} ({p['lang']})" for p in existing_posts[-25:]])
    
    if lang == "es":
        return f"""Por favor genera un artículo técnico completo y exhaustivo sobre el siguiente tema:

TEMA SELECCIONADO: {topic}
PILAR DE ARQUITECTURA: {pillar}
FECHA DE PUBLICACIÓN: {post_date_str} 09:00:00 -0600
SLUG ASIGNADO: {slug}
IMAGEN ASIGNADA: /assets/img/posts/{slug}.png

CONTEXTO DE DEDUPLICACIÓN (ÚLTIMOS ARTÍCULOS YA PUBLICADOS EN EL BLOG):
{existing_titles_summary}

REQUISITOS ESTRICTOS:
1. El artículo DEBE comenzar exactamente con el bloque Front Matter de YAML delimitado por '---'.
2. El Front Matter debe contener:
   - layout: post
   - title: "{topic}" (o un título refinado de nivel Senior Architect para este tema)
   - date: {post_date_str} 09:00:00 -0600
   - lang: es
   - categories: [Dos categorías pertinentes, ej: Arquitectura Cloud, Microservicios / Compras Composable, etc.]
   - tags: [5 a 7 etiquetas relevantes en minúsculas separadas por comas]
   - image:
       path: /assets/img/posts/{slug}.png
3. El cuerpo debe tener entre 1,500 y 2,200 palabras organizadas con encabezados H2 (##) y H3 (###).
4. Incluye al menos UN diagrama de arquitectura o flujo en formato Mermaid (```mermaid ... ```).
5. Incluye ejemplos de código de producción detallados y bien comentados.
6. Incluye una tabla comparativa Markdown con trade-offs de arquitectura.
7. NO incluyas introducciones meta como 'Aquí tienes el artículo...' ni bloques de markdown envolventes adicionales. Devuelve directamente el documento listo para guardar en Jekyll.
"""
    else:
        return f"""Please generate a complete, exhaustive technical deep-dive article on the following topic:

TOPIC: {topic}
PILLAR: {pillar}
PUBLICATION DATE: {post_date_str} 09:00:00 -0600
SLUG: {slug}
IMAGE PATH: /assets/img/posts/{slug}.png

DEDUPLICATION CONTEXT (RECENT POSTS ALREADY PUBLISHED):
{existing_titles_summary}

STRICT REQUIREMENTS:
1. Must start directly with the YAML Front Matter enclosed in '---'.
2. Front matter must include: layout: post, title, date, lang: en, categories, tags, image.path.
3. 1,500 to 2,200 words of technical content.
4. Include at least one Mermaid diagram (```mermaid).
5. Include concrete production code blocks.
6. Include an architectural comparison table.
7. Return ONLY the raw Jekyll markdown document with no conversational wrapper.
"""


def call_gemini_api(api_key: str, system_prompt: str, user_prompt: str, preferred_model: Optional[str] = None) -> str:
    """Call Google Gemini API using REST endpoint with automatic fallback across supported models."""
    models_to_try = [preferred_model] if preferred_model else DEFAULT_MODELS

    last_error = None

    for model in models_to_try:
        if not model:
            continue
        print(f" Attempting generation with Gemini model: {model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"System Context:\n{system_prompt}\n\nTask:\n{user_prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 8192,
                "topP": 0.95
            }
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                if response.status == 200:
                    resp_data = json.loads(response.read().decode("utf-8"))
                    candidates = resp_data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text_content = "".join([p.get("text", "") for p in parts])
                        if text_content.strip():
                            print(f" Successfully generated article using {model} ({len(text_content.split())} words)!")
                            return text_content.strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f" Model {model} returned HTTP {e.code}: {err_body}")
            last_error = f"HTTP {e.code}: {err_body}"
        except Exception as e:
            print(f" Model {model} request failed: {e}")
            last_error = str(e)

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


def sanitize_markdown_post(raw_markdown: str, post_date_str: str, slug: str, lang: str = "es") -> str:
    """Ensure raw LLM output has valid Jekyll Front Matter and clean Markdown formatting."""
    content = raw_markdown.strip()

    # Remove enclosing markdown backticks if returned (e.g. ```markdown ... ```)
    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
    elif content.startswith("```md"):
        content = content[len("```md"):].strip()
    elif content.startswith("```"):
        content = content[3:].strip()
    
    if content.endswith("```"):
        content = content[:-3].strip()

    # Ensure it starts with front matter delimiter
    if not content.startswith("---"):
        # Synthesize front matter
        title = "Arquitectura Composable y Patrones MACH en Producción"
        front_matter = f"""---
layout: post
title: "{title}"
date: {post_date_str} 09:00:00 -0600
lang: {lang}
categories: [Arquitectura Cloud, Microservicios]
tags: [mach, microservicios, api-first, cloud-native, headless, enterprise]
image:
  path: /assets/img/posts/{slug}.png
---

"""
        content = front_matter + content
    else:
        # Verify image path is populated correctly inside front matter
        if "image:" not in content and "path:" not in content:
            content = content.replace("---", f"""---
image:
  path: /assets/img/posts/{slug}.png""", 1)

    return content


def main():
    parser = argparse.ArgumentParser(description="Publish daily autonomous technical blog post to Jekyll with Gemini AI.")
    parser.add_argument("--dry-run", action="store_true", help="Generate post in memory and validate without writing to disk.")
    parser.add_argument("--topic", type=str, default=None, help="Custom topic to override automatic matrix selection.")
    parser.add_argument("--lang", type=str, default="es", choices=["es", "en"], help="Article language (default: es).")
    parser.add_argument("--model", type=str, default=None, help="Specific Gemini model to prioritize.")
    parser.add_argument("--date", type=str, default=None, help="Custom publication date (YYYY-MM-DD).")
    parser.add_argument("--api-key", type=str, default=None, help="Gemini API Key override.")
    args = parser.parse_args()

    print("==================================================")
    print("   MACH PLAYBOOK - AUTONOMOUS DAILY POST AGENT   ")
    print("==================================================")

    # 1. Resolve API Key
    api_key = args.api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(" Error: GEMINI_API_KEY is not set in environment or arguments.")
        if args.dry_run:
            print(" Running in Mock/Dry-Run mode without API Key...")
            api_key = "MOCK_KEY"
        else:
            sys.exit(1)

    # 2. Resolve Post Date
    now = datetime.datetime.now()
    post_date_str = args.date if args.date else now.strftime("%Y-%m-%d")

    # 3. Deduplication Check
    posts_dir = "_posts"
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir, exist_ok=True)

    existing_posts = scan_existing_posts(posts_dir)
    print(f" Scanned {len(existing_posts)} existing articles in '{posts_dir}/' for deduplication.")

    # 4. Topic Selection
    selected_topic, pillar = select_next_topic(existing_posts, args.topic)
    print(f" Selected Topic: '{selected_topic}'")
    print(f" Pillar: [{pillar}] | Target Language: [{args.lang.upper()}]")

    # 5. Generate Slug and Filename
    clean_slug = slugify(selected_topic)
    filename = f"{post_date_str}-{clean_slug}.md"
    filepath = os.path.join(posts_dir, filename)
    slug_with_date = f"{post_date_str}-{clean_slug}"

    print(f" Target Filename: {filepath}")

    # 6. Build Prompts
    system_prompt = build_system_prompt(args.lang)
    user_prompt = build_user_prompt(selected_topic, pillar, existing_posts, post_date_str, slug_with_date, args.lang)

    # 7. Generate Article
    if api_key == "MOCK_KEY":
        print(" Synthesizing mock post for dry-run testing...")
        post_content = f"""---
layout: post
title: "{selected_topic}"
date: {post_date_str} 09:00:00 -0600
lang: {args.lang}
categories: [Arquitectura Cloud, Microservicios]
tags: [mach, microservicios, cloud-native, api-first, resiliencia, patrones]
image:
  path: /assets/img/posts/{slug_with_date}.png
---

En los ecosistemas empresariales modernos, la transición hacia arquitecturas composables requiere patrones robustos y desacoplados.

## Contexto de Negocio y Desafíos Arquitectónicos

Las suites monolíticas tradicionales crean dependencias rígidas y cuellos de botella en el ciclo de vida del software.

```mermaid
graph TD
    A[Client Request] --> B[API Gateway]
    B --> C[Service Mesh]
    C --> D[Microservice A]
    C --> E[Microservice B]
```

## Implementación Técnica

A continuación se presenta una implementación de referencia en TypeScript:

```typescript
export interface ServiceResponse<T> {{
  status: 'SUCCESS' | 'ERROR';
  data?: T;
  timestamp: string;
}}

export class ResilientGateway {{
  async routeRequest(serviceName: string): Promise<void> {{
    console.log("Routing request securely to " + serviceName);
  }}
}}
```

## Conclusión

La adopción de {selected_topic} permite una mayor agilidad y escalabilidad sin comprometer la estabilidad del sistema.
"""
    else:
        raw_article = call_gemini_api(api_key, system_prompt, user_prompt, args.model)
        post_content = sanitize_markdown_post(raw_article, post_date_str, slug_with_date, args.lang)

    # Word count check
    words = len(post_content.split())
    print(f" Generated article word count: {words} words.")

    # 8. Dry Run vs Save
    if args.dry_run:
        print("\n--- [DRY RUN PREVIEW - FIRST 35 LINES] ---")
        preview_lines = post_content.splitlines()[:35]
        print("\n".join(preview_lines))
        print("--- [END DRY RUN PREVIEW] ---\n")
        print("✔ Dry-run completed successfully. No files written to disk.")
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_content)
        print(f" Successfully written post to: {filepath}")

    print("==================================================")
    print("   WORKFLOW EXECUTION FINISHED SUCCESSFULLY      ")
    print("==================================================")


if __name__ == "__main__":
    main()
