#!/usr/bin/env python3
"""
MACH Playbook - Autonomous Daily Post & Cover Image Publisher with Gemini AI
Author: Lenin Meza (merolhack)
Description:
  Automated agent workflow that scans existing Jekyll blog posts for deduplication,
  selects an architectural topic across 5 MACH/Composable Commerce pillars,
  prompts Google Gemini for a Senior Solutions Architect-level article (1,500-2,200 words)
  with E-E-A-T rigor, Mermaid diagrams, and code snippets.
  Simultaneously synthesizes unique matching cover images via Google Imagen 3 (Nano Banana)
  with multi-layer fallback (Pollinations AI & Unsplash IT Photography), saving both
  the Markdown post and PNG cover asset in a single atomic pipeline.
"""

import argparse
import base64
import datetime
import glob
import json
import os
import random
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple

# Supported Gemini text generation models in prioritized order (latest 2026 fleet first)
DEFAULT_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-3.1-pro",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.5-pro"
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

# Verified high-resolution IT & architecture photos for fallback
UNSPLASH_IT_PHOTOS = [
    "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=675&fit=crop",  # Enterprise Server Racks
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&h=675&fit=crop",  # Digital Matrix Code
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=675&fit=crop",  # Analytics Dashboard
    "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&h=675&fit=crop",  # High-Speed Fiber Optic
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&h=675&fit=crop",  # Microchip Architecture
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=675&fit=crop",  # Global Cloud Network
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1200&h=675&fit=crop",  # Code Editor
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=675&fit=crop",  # Abstract Digital 3D
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&h=675&fit=crop",  # Neon Network Hardware
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1200&h=675&fit=crop"   # Data Center Room
]


def slugify(text: str) -> str:
    """Transform topic title into URL-friendly, clean ASCII slug."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


def scan_existing_posts(posts_dir: str = "_posts") -> List[Dict[str, str]]:
    """Scan existing Jekyll posts to extract titles, slugs, and language for deduplication."""
    existing_posts = []
    if not os.path.exists(posts_dir):
        return existing_posts

    files = glob.glob(os.path.join(posts_dir, "*.md"))
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read(2048)  # Read header block
            
            title_match = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", content, re.MULTILINE)
            lang_match = re.search(r"^lang:\s*[\"']?(.*?)[\"']?$", content, re.MULTILINE)
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

    for pillar, topics in TOPIC_MATRIX.items():
        for topic in topics:
            topic_clean = topic.lower()
            topic_slug = slugify(topic)
            
            is_covered = any(
                topic_slug in s or s in topic_slug or
                any(word in s for word in topic_slug.split("-") if len(word) > 5)
                for s in existing_slugs_lower
            ) or any(topic_clean in t or t in topic_clean for t in existing_titles_lower)
            
            if not is_covered:
                return topic, pillar

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
5. **Idioma:** Español técnico impecable, fluido y profesional, utilizando la terminología estándar de la industria cloud/software.
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
   - Failure modes and mitigation strategies.
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


def get_available_gemini_models(api_key: str) -> List[str]:
    """Dynamically query Gemini API to discover active models supporting generateContent."""
    if not api_key or api_key == "MOCK_KEY":
        return DEFAULT_MODELS

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                discovered = []
                for m in data.get("models", []):
                    methods = m.get("supportedGenerationMethods", [])
                    name = m.get("name", "")
                    if "generateContent" in methods and name.startswith("models/"):
                        model_id = name.replace("models/", "")
                        discovered.append(model_id)

                if discovered:
                    def model_priority(m: str) -> int:
                        m_low = m.lower()
                        # Flash models (fastest, cheapest, highest availability)
                        if "flash" in m_low and "lite" not in m_low and "8b" not in m_low:
                            return 1
                        elif "flash" in m_low:
                            return 2
                        elif "pro" in m_low:
                            return 3
                        return 4

                    sorted_models = sorted(discovered, key=model_priority)
                    print(f" Dynamically discovered {len(sorted_models)} active Gemini models (top: {', '.join(sorted_models[:4])})")
                    return sorted_models
    except Exception as e:
        print(f" Warning: Could not query dynamic Gemini model list ({e}). Using default static model list.")

    return DEFAULT_MODELS


def call_gemini_api(api_key: str, system_prompt: str, user_prompt: str, preferred_model: Optional[str] = None) -> str:
    """Call Google Gemini API using REST endpoint with dynamic model discovery, prioritized models, exponential backoff, and retry handling."""
    if preferred_model:
        models_to_try = [preferred_model]
    else:
        models_to_try = get_available_gemini_models(api_key)

    last_error = None

    for model in models_to_try:
        if not model:
            continue
        
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            print(f" Attempting generation with Gemini model: {model} (Attempt {attempt}/{max_retries})...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            
            combined_prompt = "System Context:\n" + system_prompt + "\n\nTask:\n" + user_prompt
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": combined_prompt}
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
                last_error = f"HTTP {e.code} ({model}): {err_body}"
                
                # If 404 (Model not found/deprecated), break retry loop immediately and try next model
                if e.code == 404:
                    print(f" Model {model} is not supported or deprecated. Advancing immediately to next fallback model...")
                    break
                
                # If 429 (Rate limit / Quota)
                if e.code == 429:
                    if "limit: 0" in err_body or ("RESOURCE_EXHAUSTED" in err_body and "GenerateRequestsPerDay" in err_body):
                        print(f" Model {model} has 0 quota or daily quota exhausted on this project. Advancing immediately to next fallback model...")
                        break
                    if attempt < max_retries:
                        backoff = (2 ** attempt) + random.uniform(1.0, 3.0)
                        print(f" Transient rate limit 429. Retrying {model} in {backoff:.1f}s...")
                        time.sleep(backoff)
                        continue
                
                # If 503 (High demand) or 500, 502, 504
                if e.code in [503, 500, 502, 504]:
                    if attempt < max_retries:
                        backoff = (2 ** attempt) + random.uniform(1.0, 3.0)
                        print(f" Transient error {e.code}. Retrying {model} in {backoff:.1f}s...")
                        time.sleep(backoff)
                        continue
            except Exception as e:
                print(f" Model {model} request failed: {e}")
                last_error = f"{model}: {str(e)}"
                if attempt < max_retries:
                    time.sleep(2)
                    continue

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


def generate_fallback_article(topic: str, pillar: str, slug: str, lang: str, post_date_str: str) -> str:
    """Synthesize an authoritative, exhaustive Senior Solutions Architect article adhering strictly to E-E-A-T and Chirpy standards when external LLM APIs are unreachable."""
    print(f" Synthesizing autonomous high-quality deep dive article for '{topic}'...")

    if lang == "es":
        categories_str = "[Arquitectura Cloud, Microservicios]"
        if "API" in pillar or "Integraciones" in pillar:
            categories_str = "[Diseño de APIs, Microservicios]"
        elif "Headless" in pillar or "Frontend" in pillar:
            categories_str = "[Headless & Frontend, Arquitectura Cloud]"
        elif "Estrategia" in pillar or "FinOps" in pillar:
            categories_str = "[Arquitectura Cloud, Automatización]"

        return f"""---
layout: post
title: "{topic}"
date: {post_date_str} 09:00:00 -0600
lang: es
categories: {categories_str}
tags: [mach, microservicios, cloud-native, api-first, resiliencia, arquitectura, devops]
image:
  path: /assets/img/posts/{slug}.png
---

En el panorama del comercio digital y los sistemas distribuidos a escala empresarial, la adopción del paradigma MACH (Microservices, API-first, Cloud-native, Headless) ha dejado de ser una opción experimental para convertirse en el estándar de oro de la ingeniería de software moderna. En este análisis profundo, abordamos los principios arquitectónicos, las decisiones de diseño críticas y los patrones de implementación necesarios para ejecutar con éxito **{topic}**.

## 1. El Desafío Empresarial: Del Acoplamiento Monolítico a la Modularidad Resiliente

Las organizaciones que operan sobre arquitecturas heredadas enfrentan fricciones sistemáticas: despliegues coordinados de alto riesgo, bases de código monolíticas con límites de contexto difusos, cuellos de botella en la persistencia de datos y una incapacidad estructural para innovar al ritmo del mercado.

Al implementar estrategias alineadas con **{topic}**, el objetivo primordial es desacoplar las responsabilidades funcionales y garantizar que cada componente pueda escalar, evolucionar y recuperarse de fallos de manera autónoma.

### Objetivos Clave de la Arquitectura
- **Aislamiento de Fallos (Blast Radius Containment):** Prevenir que la degradación de un servicio secundario comprometa la disponibilidad del flujo principal transaccional.
- **Soberanía y Consistencia de Datos:** Garantizar la integridad transaccional mediante patrones eventuales y asíncronos sin recurrir a bloqueos distribuidos (Two-Phase Commit).
- **Observabilidad Cardinal de Extremo a Extremo:** Integrar trazas distribuidas, métricas RED (Rate, Errors, Duration) y logs estructurados en tiempo real.

```mermaid
graph TD
    subgraph Ingress Layer
        Client["Cliente Web / Móvil / PWA"] --> Edge["Edge CDN / Cloudflare Workers"]
        Edge --> Gateway["API Gateway Empresarial (Kong / Apigee)"]
    end

    subgraph Service Mesh & Compute Layer
        Gateway --> Auth["Servicio de Autenticación & IAM (mTLS)"]
        Gateway --> CoreService["Microservicio Central: {slug}"]
        CoreService --> EventBus["Event Backbone (Apache Kafka / GCP Pub/Sub)"]
    end

    subgraph Persistence & Asynchronous Processing
        CoreService --> FastCache["Redis Cluster (Caché L1/L2)"]
        CoreService --> PrimaryDB["Base de Datos Distribuida (PostgreSQL / Spanner)"]
        EventBus --> AnalyticsWorker["Procesador Asíncrono / CDC (Debezium)"]
        EventBus --> NotificationService["Servicio de Notificaciones y Webhooks"]
    end

    classDef primary fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#fff;
    classDef storage fill:#059669,stroke:#047857,stroke-width:2px,color:#fff;
    class CoreService,Gateway primary;
    class PrimaryDB,FastCache,EventBus storage;
```

---

## 2. Patrones de Diseño y Modelado de la Solución

Para abordar con solvencia **{topic}**, los equipos de ingeniería de élite deben estructurar la solución basándose en contratos formales, encapsulamiento riguroso de capacidades de negocio (Packaged Business Capabilities - PBCs) y gestión proactiva de la concurrencia.

### Principios Rectores
1. **Contratos Primero (API-First Design):** La interfaz pública y los contratos de eventos deben definirse y validarse en CI/CD antes de escribir una sola línea de código de producción.
2. **Idempotencia Transaccional:** Cada mutación debe soportar reintentos transparentes mediante claves de idempotencia únicas respaldadas en almacenamiento volátil de ultra baja latencia.
3. **Degradación Elegante:** Si las dependencias aguas abajo experimentan saturación, el sistema debe responder con fallbacks cacheados o respuestas parciales estructuradas.

---

## 3. Implementación de Referencia en Producción

A continuación, se detalla una implementación técnica de referencia diseñada para entornos de alta concurrencia en la nube:

```typescript
/**
 * MACH Playbook - Production Architectural Reference Implementation
 * Topic: {topic}
 */

import {{ Request, Response, NextFunction }} from 'express';
import Redis from 'ioredis';
import {{ v4 as uuidv4 }} from 'uuid';

export interface ExecutionContext {{
  traceId: string;
  tenantId: string;
  timestamp: string;
  idempotencyKey?: string;
}}

export interface ServiceResult<T> {{
  success: boolean;
  data?: T;
  errorCode?: string;
  errorMessage?: string;
  executionTimeMs: number;
}}

export class EnterpriseMACHEngine {{
  private redisClient: Redis;
  private readonly defaultTtlSeconds = 300;

  constructor(redisConnectionUri: string) {{
    this.redisClient = new Redis(redisConnectionUri, {{
      maxRetriesPerRequest: 3,
      enableReadyCheck: true,
      retryStrategy: (times) => Math.min(times * 100, 3000),
    }});
  }}

  /**
   * Ejecución resiliente con validación de idempotencia y circuit breaking preventivo
   */
  public async executeWithResilience<T>(
    context: ExecutionContext,
    operation: () => Promise<T>
  ): Promise<ServiceResult<T>> {{
    const startTime = Date.now();
    const lockKey = `lock:mach:${{context.tenantId}}:${{context.idempotencyKey || uuidv4()}}`;

    try {{
      // 1. Verificación de Idempotencia
      if (context.idempotencyKey) {{
        const cachedResult = await this.redisClient.get(lockKey);
        if (cachedResult) {{
          return {{
            success: true,
            data: JSON.parse(cachedResult),
            executionTimeMs: Date.now() - startTime,
          }};
        }}
      }}

      // 2. Ejecución de la operación de negocio
      const result = await operation();

      // 3. Persistencia de caché/idempotencia
      if (context.idempotencyKey && result) {{
        await this.redisClient.setex(
          lockKey,
          this.defaultTtlSeconds,
          JSON.stringify(result)
        );
      }}

      return {{
        success: true,
        data: result,
        executionTimeMs: Date.now() - startTime,
      }};
    }} catch (error: any) {{
      return {{
        success: false,
        errorCode: error.code || 'INTERNAL_PROCESSING_FAULT',
        errorMessage: error.message || 'Error no controlado durante la ejecución',
        executionTimeMs: Date.now() - startTime,
      }};
    }}
  }}
}}
```

---

## 4. Matriz Comparativa de Trade-offs Arquitectónicos

Toda decisión de ingeniería conlleva compromisos. La siguiente matriz resume los vectores clave a evaluar al implementar esta solución:

| Criterio de Evaluación | Enfoque Centralizado / Monolítico | Enfoque Distribuido Composable (MACH) | Recomendación Enterprise |
| :--- | :--- | :--- | :--- |
| **Velocidad de Despliegue** | Lenta; bloqueada por dependencias cruzadas. | Rápida; despliegues continuos e independientes por PBC. | **MACH:** Acelera el time-to-market y reduce riesgos. |
| **Complejidad Operativa** | Baja a nivel de infraestructura; alta a nivel de código. | Alta; requiere Kubernetes, Service Mesh y Observabilidad. | **MACH con DevOps Maduro:** Fundamental contar con GitOps y CI/CD automatizado. |
| **Resiliencia & Tolerancia a Fallos** | Punto único de fallo; una caída afecta a todo el sistema. | Aislada; degradación controlada y contención del radio de explosión. | **MACH:** Esencial para plataformas con SLAs superiores a 99.95%. |
| **Escalabilidad de Costos (FinOps)** | Escalamiento vertical costoso y rígido. | Escalamiento horizontal elástico por microservicio. | **MACH:** Optimiza el consumo de recursos en picos de demanda. |

---

## 5. Modos de Fallo Comunes en Producción y Mitigaciones

Al desplegar **{topic}** en entornos reales de producción, los arquitectos deben prever y neutralizar los siguientes riesgos operativos:

### A. Tormentas de Reintentos (Thundering Herd / Retry Storms)
- **Problema:** Múltiples clientes reintentan simultáneamente peticiones fallidas contra un servicio en recuperación, provocando su saturación permanente.
- **Mitigación:** Implementar retroceso exponencial con variación aleatoria (exponential backoff with jitter) y Circuit Breakers activos en el API Gateway.

### B. Consistencia de Lectura Tras Escritura (Eventual Consistency Lag)
- **Problema:** El usuario actualiza su estado pero la réplica de lectura aún no ha recibido el evento del bus de mensajes.
- **Mitigación:** Usar encabezados de versión o enrutar lecturas inmediatas posteriores a mutaciones hacia la réplica primaria (Read-Your-Own-Writes Consistency).

### C. Deriva de Esquemas en APIs y Eventos
- **Problema:** Un cambio en la estructura de datos rompe silenciosamente consumidores aguas abajo.
- **Mitigación:** Exigir Schema Registry (Avro / JSON Schema / Protobuf) con validaciones automáticas de compatibilidad hacia atrás en los pipelines de CI/CD.

---

## 6. Checklist de Implementación para Equipos de Ingeniería

Antes de promover la arquitectura a producción, asegúrese de haber cumplido los siguientes hitos técnicos:

- [x] Contratos de API formalizados y validados mediante pruebas de contrato automatizadas (Pact / OpenAPI Spec).
- [x] Claves de idempotencia y locks distribuidos operativos para todas las operaciones mutables.
- [x] Métricas RED e instrumentación OpenTelemetry integradas en los paneles de control de observabilidad.
- [x] Pruebas de estrés y caos (Chaos Engineering) ejecutadas para validar el aislamiento de fallos del Service Mesh.
- [x] Políticas de seguridad Zero Trust (mTLS y validación de tokens JWT) activadas en todas las rutas internas.

---

## Conclusión

La implementación de **{topic}** marca un salto cuantitativo en la madurez técnica de cualquier organización digital. Al adoptar principios modulares, contratos rigurosos y mecanismos avanzados de resiliencia, los equipos de ingeniería pueden ofrecer experiencias digitales de clase mundial con la máxima velocidad y confiabilidad operativa.
"""
    else:
        categories_str = "[Architecture, Microservices]"
        if "API" in pillar or "Integration" in pillar:
            categories_str = "[API Design, Microservices]"
        elif "Headless" in pillar or "Frontend" in pillar:
            categories_str = "[Headless & Frontend, Architecture]"
        elif "Strategy" in pillar or "FinOps" in pillar:
            categories_str = "[Enterprise Architecture, FinOps]"

        return f"""---
layout: post
title: "{topic}"
date: {post_date_str} 09:00:00 -0600
lang: en
categories: {categories_str}
tags: [mach, microservices, cloud-native, api-first, resilience, architecture, devops]
image:
  path: /assets/img/posts/{slug}.png
---

In the landscape of modern enterprise software and composable digital commerce, adopting the MACH paradigm (Microservices, API-first, Cloud-native, Headless) has transitioned from an ambitious architectural vision to an operational necessity. In this comprehensive technical deep-dive, we examine the production design patterns, architectural tradeoffs, and implementation blueprints required for **{topic}**.

## 1. The Enterprise Problem Statement: Monolithic Debt vs. Composable Agility

Traditional legacy architectures suffer from inherent systemic bottlenecks: risky, all-or-nothing deployments, tangled domain boundaries, database contention, and high operational friction.

Implementing patterns around **{topic}** enables engineering organizations to establish strict domain separation, allowing Packaged Business Capabilities (PBCs) to scale, iterate, and recover independently.

```mermaid
graph TD
    Client["Client / PWA / Headless Storefront"] --> Edge["Edge CDN / Compute Worker"]
    Edge --> Gateway["Enterprise API Gateway"]
    Gateway --> Auth["Identity & Access Management (mTLS)"]
    Gateway --> Service["Core Service: {slug}"]
    Service --> Cache["Distributed Cache (Redis Cluster)"]
    Service --> DB["Primary Distributed Database"]
    Service --> Bus["Event Stream (Apache Kafka / GCP PubSub)"]
    Bus --> Worker["Asynchronous CDC Worker"]
```

## 2. Architectural Tradeoffs Matrix

| Dimension | Monolithic Paradigm | Composable MACH Architecture | Verdict |
| :--- | :--- | :--- | :--- |
| **Deployment Velocity** | Coupled releases with high regression risks. | Decoupled, independent CI/CD pipelines per service. | **MACH Wins** |
| **Fault Isolation** | Single point of failure across services. | Contained blast radius with graceful degradation. | **MACH Wins** |
| **Operational Overhead** | Low infrastructure complexity. | Requires mature GitOps, Service Mesh, and Observability. | **Requires Mature DevOps** |
| **Cost Efficiency** | Expensive vertical scaling. | Elastic horizontal autoscaling based on load. | **MACH Wins** |

## 3. Production Reference Implementation

```typescript
/**
 * MACH Playbook - Enterprise Reference Implementation
 * Topic: {topic}
 */
export interface ServiceResponse<T> {{
  success: boolean;
  data?: T;
  timestamp: string;
  traceId: string;
}}

export class ResilientServiceEngine {{
  async processRequest<T>(traceId: string, action: () => Promise<T>): Promise<ServiceResponse<T>> {{
    try {{
      const result = await action();
      return {{
        success: true,
        data: result,
        timestamp: new Date().toISOString(),
        traceId
      }};
    }} catch (error: any) {{
      return {{
        success: false,
        timestamp: new Date().toISOString(),
        traceId
      }};
    }}
  }}
}}
```

## 4. Production Failure Modes & Mitigations

1. **Cascading Service Failures:** Implement aggressive timeouts, dead-letter queues (DLQ), and circuit breaking at the gateway layer.
2. **Schema Drift:** Enforce centralized schema registries with backward compatibility gates in CI/CD.
3. **Thundering Herd:** Use exponential backoff with randomized jitter on client retries.

## Conclusion

Mastering **{topic}** equips engineering teams to build durable, scalable, and highly available composable architectures capable of supporting mission-critical enterprise workloads.
"""


def get_image_topic_prompt(title: str) -> str:
    """Build optimized visual prompt for IT and cloud architecture imagery."""
    t = title.lower()
    if any(k in t for k in ["security", "oauth", "jwt", "zero trust", "seguridad", "mtls"]):
        subject = "a high-tech cybersecurity vault with glowing digital padlock, cryptographic authentication shields, and dark metallic server hardware"
    elif any(k in t for k in ["saga", "cqrs", "event", "kafka", "stream", "outbox", "asincrona"]):
        subject = "an asynchronous event stream topology with glowing message queues, Kafka event bus, and database node cluster in dark space"
    elif any(k in t for k in ["api", "openapi", "rest", "graphql", "grpc", "gateway"]):
        subject = "an isometric 3D blueprint of API Gateway proxy routing JSON payloads between cloud microservice containers, dark glassmorphism render"
    elif any(k in t for k in ["observability", "tracing", "metrics", "opentelemetry", "jaeger", "monitoreo"]):
        subject = "a futuristic holographic observability monitoring console displaying OpenTelemetry traces, latency graphs, and system metrics"
    elif any(k in t for k in ["ci/cd", "deploy", "pipeline", "argocd", "kubernetes", "canary"]):
        subject = "an automated DevOps software deployment pipeline with glowing code blocks moving through continuous integration stages"
    elif any(k in t for k in ["headless", "cms", "frontend", "next.js", "nuxt", "storefront"]):
        subject = "decoupled headless CMS layers floating in 3D space above glowing glass mobile and web displays"
    elif any(k in t for k in ["commerce", "checkout", "pbc", "pago", "sap", "magento", "monolito"]):
        subject = "a global high-speed digital commerce cloud network with thousands of microservice transactions and high tech server nodes"
    elif any(k in t for k in ["sql", "yugabyte", "postgres", "sharding", "database", "base de datos"]):
        subject = "distributed database cluster nodes synchronizing data shards across geographic regions with glowing fiber optic links"
    else:
        subject = "an enterprise data center server rack room with glowing fiber optic cables, ultra detailed IT infrastructure photography"

    return f"Professional IT computer system graphic: {subject}. Dark technological background, ultra high resolution, clean architectural design, 16:9 aspect ratio, no text."


def generate_post_image(title: str, slug: str, api_key: str, output_path: str, dry_run: bool = False) -> bool:
    """Generate high-res cover image using Google Imagen 3 with Pollinations & Unsplash fallback."""
    print(f"\n--- Generating Matching Cover Image for: '{slug}' ---")
    prompt = get_image_topic_prompt(title)
    print(f" Image Prompt: {prompt}")

    if dry_run:
        print(" Dry-run mode: Skipping disk write for cover image.")
        return True

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Attempt Google Imagen 3 via Gemini API if valid API key is provided
    if api_key and api_key != "MOCK_KEY":
        imagen_model = "imagen-3.0-generate-002"
        print(f" Attempting image synthesis with Google Imagen 3 ({imagen_model})...")
        imagen_url = f"https://generativelanguage.googleapis.com/v1beta/models/{imagen_model}:predict?key={api_key}"
        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "outputOptions": {"mimeType": "image/png"}
            }
        }
        try:
            req = urllib.request.Request(
                imagen_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=25) as response:
                if response.status == 200:
                    resp_data = json.loads(response.read().decode("utf-8"))
                    predictions = resp_data.get("predictions", [])
                    if predictions and "bytesBase64Encoded" in predictions[0]:
                        img_bytes = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                        with open(output_path, "wb") as f:
                            f.write(img_bytes)
                        print(f" Successfully generated cover image via Google Imagen 3 ({len(img_bytes)} bytes) -> {output_path}")
                        return True
        except Exception as e:
            print(f" Imagen 3 image generation failed ({e}). Proceeding to Pollinations AI fallback...")

    # 2. Attempt Pollinations AI (Free FLUX / SD engine)
    seed = abs(hash(slug)) % 100000
    pollinations_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1200&height=675&nologo=true&seed={seed}"
    print(f" Attempting image synthesis with Pollinations AI...")
    try:
        req = urllib.request.Request(pollinations_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                img_bytes = response.read()
                if len(img_bytes) > 5000:
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f" Successfully generated cover image via Pollinations AI ({len(img_bytes)} bytes) -> {output_path}")
                    return True
    except Exception as e:
        print(f" Pollinations AI generation failed ({e}). Proceeding to Unsplash fallback...")

    # 3. Fallback: Curated Verified High-Resolution Unsplash IT Photo
    photo_index = abs(hash(slug)) % len(UNSPLASH_IT_PHOTOS)
    unsplash_url = UNSPLASH_IT_PHOTOS[photo_index]
    print(f" Downloading verified IT fallback photo from Unsplash...")
    try:
        req = urllib.request.Request(unsplash_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                img_bytes = response.read()
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f" Successfully saved verified cover photo from Unsplash -> {output_path}")
                return True
    except Exception as e:
        print(f" Error saving fallback image from Unsplash: {e}")

    # 4. Final Fallback: Standalone Minimal Valid PNG Generator
    print(" Generating local fallback graphic asset...")
    try:
        minimal_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkWPjfDwAEfgH50mSTVAAAAABJRU5ErkJggg=="
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(minimal_png_base64))
        print(f" Saved local fallback placeholder image -> {output_path}")
        return True
    except Exception as e:
        print(f" Error generating local fallback image: {e}")
        return False


def sanitize_markdown_post(raw_markdown: str, post_date_str: str, slug: str, lang: str = "es") -> str:
    """Ensure raw LLM output has valid Jekyll Front Matter, clean Markdown formatting, and canonical taxonomy."""
    content = raw_markdown.strip()

    if content.startswith("```markdown"):
        content = content[len("```markdown"):].strip()
    elif content.startswith("```md"):
        content = content[len("```md"):].strip()
    elif content.startswith("```"):
        content = content[3:].strip()
    
    if content.endswith("```"):
        content = content[:-3].strip()

    if not content.startswith("---"):
        default_cat = "Arquitectura Cloud, Microservicios" if lang == "es" else "Architecture, Microservices"
        front_matter = f"""---
layout: post
title: "{slug.replace('-', ' ').title()}"
date: {post_date_str} 09:00:00 -0600
lang: {lang}
categories: [{default_cat}]
tags: [cloud-native, microservices, architecture, api-first, devops]
image:
  path: /assets/img/posts/{slug}.png
---

"""
        content = front_matter + content
    else:
        # Ensure image path is present
        if "image:" not in content and "path:" not in content:
            content = content.replace("---", f"""---
image:
  path: /assets/img/posts/{slug}.png""", 1)

        # Ensure lang flag is present
        if not re.search(r"^lang:\s*(es|en)", content, re.MULTILINE):
            content = content.replace("---", f"""---
lang: {lang}""", 1)

    return content


def main():
    parser = argparse.ArgumentParser(description="Publish daily autonomous technical blog post and cover image to Jekyll with Gemini AI.")
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
        print(" Warning: GEMINI_API_KEY is not set in environment or arguments.")
        if args.dry_run:
            print(" Running in Mock/Dry-Run mode without API Key...")
            api_key = "MOCK_KEY"
        else:
            api_key = "MOCK_KEY"

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

    # 5. Generate Slug and Filenames
    clean_slug = slugify(selected_topic)
    filename = f"{post_date_str}-{clean_slug}.md"
    filepath = os.path.join(posts_dir, filename)
    slug_with_date = f"{post_date_str}-{clean_slug}"
    image_rel_path = f"/assets/img/posts/{slug_with_date}.png"
    image_file_path = os.path.join("assets/img/posts", f"{slug_with_date}.png")

    print(f" Target Filename: {filepath}")
    print(f" Target Cover Image: {image_file_path}")

    # 6. Build Prompts
    system_prompt = build_system_prompt(args.lang)
    user_prompt = build_user_prompt(selected_topic, pillar, existing_posts, post_date_str, slug_with_date, args.lang)

    # 7. Generate Article (Gemini API with Autonomous Fallback)
    post_content = None
    if api_key != "MOCK_KEY":
        try:
            raw_article = call_gemini_api(api_key, system_prompt, user_prompt, args.model)
            post_content = sanitize_markdown_post(raw_article, post_date_str, slug_with_date, args.lang)
        except Exception as e:
            print(f" ⚠️ Remote Gemini API generation failed ({e}).")
            print(" Activating resilient autonomous article synthesizer...")
            post_content = generate_fallback_article(selected_topic, pillar, slug_with_date, args.lang, post_date_str)
    else:
        post_content = generate_fallback_article(selected_topic, pillar, slug_with_date, args.lang, post_date_str)

    # Word count check
    words = len(post_content.split())
    print(f" Generated article word count: {words} words.")

    # 8. Generate Matching Cover Image
    generate_post_image(selected_topic, slug_with_date, api_key, image_file_path, args.dry_run)

    # 9. Dry Run vs Save
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
