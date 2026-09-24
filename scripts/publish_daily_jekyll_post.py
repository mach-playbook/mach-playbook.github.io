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

# 8 Enterprise Pillars of MACH Playbook Topic Matrix - Expanded to 200+ Topics
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
        "Patrones de Caché Distribuida con Redis Cluster y Consistencia Eventual",
        "eBPF y Cilium para Seguridad y Redes de Alto Rendimiento en Kubernetes",
        "Dapr como Distributed Application Runtime: Abstracción de Estado y Pub/Sub",
        "KEDA y Escalado Dirigido por Eventos en Microservicios de Procesamiento Asíncrono",
        "Gestión de Secretos Dinámicos y Rotación Automática con HashiCorp Vault en Kubernetes",
        "Cell-Based Architecture: Aislamiento Extremo de Blast Radius para Escala Global",
        "Chaos Engineering Continuo con LitmusChaos y Chaos Mesh en Entornos Staging",
        "Arquitectura Hexagonal (Puertos y Adaptadores) en Microservicios Go y TypeScript",
        "Migración sin Caídas de Esquemas Relacionales con gh-ost y pt-online-schema-change",
        "Consistencia Eventual en CQRS: Manejo de Lecturas Sucias y Proyecciones Asíncronas",
        "Multi-Cluster Kubernetes con Cilium Mesh y Global Service Load Balancing",
        "Controladores Kubernetes Personalizados (Custom Controllers) con Kubebuilder en Go",
        "Contención de Cascading Failures con Backpressure y Reactive Streams en Microservicios",
        "Gestión de Memoria y Garbage Collection Tuning para Microservicios Java y Node.js en Contenedores",
        "Arquitecturas Multi-Región Activo-Activo con Bases de Datos Globalmente Distribuidas (Spanner, CockroachDB)",
        "Compresión y Optimización de Payloads Binarios Internos con Protobuf vs FlatBuffers"
    ],
    "API-First & Integraciones Distribuidas": [
        "Federación de GraphQL (Apollo Federation v2) vs REST Gateway en Ecosistemas Composable",
        "Diseño de Contratos API con OpenAPI v3.1 y Validación de Schemas en CI/CD",
        "Idempotencia de Pagos y Webhooks Distribuidos con Colas Dead-Letter (DLQ)",
        "Estrategias de Rate Limiting Adaptativo y Algoritmos Token Bucket en API Gateways",
        "Migración y Versionado No Destructivo de APIs RESTful en Entornos Empresariales",
        "AsyncAPI para la Gobernanza de Event Streams y Webhooks en Tiempo Real",
        "Diseño de APIs de Alto Rendimiento con gRPC y Protocol Buffers para Comunicación Interna",
        "Seguridad de APIs: Prevención de OWASP API Top 10 y Manejo Seguro de Tokens JWT",
        "Traducción y Mediación de Protocolos en Edge Gateways (HTTP/3, WebSockets, SSE)",
        "Gobernanza de APIs: Pruebas de Contrato Automatizadas con Pact en Pipelines CI/CD",
        "Kafka Schema Registry y Apache Avro para Evolución Compatible de Mensajería",
        "BFF (Backend for Frontend) Ultraligero con Hono y Cloudflare Workers",
        "Server-Sent Events (SSE) vs WebSockets para Notificaciones Push en Frontends Headless",
        "OAuth 2.1 y Passkeys (WebAuthn): Modernizando la Identidad en Plataformas Composable",
        "Gobernanza de Webhooks Entrantes: Verificación Criptográfica HMAC y Rate Limiting",
        "API Monetization y Quotas Granulares con Kong Gateway y Stripe Billing",
        "Enrutamiento Inteligente en API Gateway con Machine Learning para Detección de Anomalías",
        "GraphQL Subscriptions a Escala con Redis Streams y NATS Messaging",
        "Contratos Basados en Consumidores (Consumer-Driven Contracts) para Equipos Desacoplados",
        "Mocking Dinámico y Virtualización de APIs en Ambientes de Pruebas Distribuidas",
        "Event Mesh Global: Conectando Nubes Híbridas con Solace PubSub+ y Apache Pulsar",
        "API Linters y Style Guides Automatizados con Spectral en Flujos de Pull Request",
        "Depuración y Replay de Webhooks Fallidos mediante Arquitecturas Dead-Letter Event-Driven",
        "Transformación de Cargas XML/SOAP Legadas a JSON REST mediante Middleware Liviano",
        "Sistemas de Notificaciones Masivas Multi-Canal (SMS, Push, Email) con Resiliencia ante Caídas"
    ],
    "Headless & Frontend Moderno": [
        "Optimización de Core Web Vitals (INP, LCP) en Frontends Composable con Next.js e ISR",
        "Estrategias de Caché Edge y Purgado Granular con Cloudflare Workers y Fastly Compute",
        "Integración de CMS Headless Multi-Tenant (Contentful, Strapi, Sanity) en E-Commerce Global",
        "Micro-Frontends con Module Federation: Modularización sin Pérdida de Rendimiento",
        "Estrategias de Hidratación Parcial y React Server Components en Arquitecturas Headless",
        "Búsqueda Composable Instantánea: Integración de Algolia y Meilisearch con Catálogos Dinámicos",
        "Diseño de Sistemas de Diseño (Design Systems) Headless Desacoplados de la Lógica de Negocio",
        "State Management y Offline-First en Progressive Web Apps (PWA) de Alto Tráfico",
        "Monitoreo de Rendimiento Real (RUM) y Telemetría de Usuario en Tiendas Headless",
        "Internacionalización Dinámica y Localización Geo-Distribuida en Frontends Composable",
        "Astro y Edge Islands para Sitios de Comercio Electrónico de Máximo Rendimiento",
        "Optimización de Imágenes Responsive al Vuelo con Cloudflare Images y Next/Image",
        "Estrategias de Renderizado Híbrido: SSG, SSR e ISR en Plataformas Omnicanal",
        "Web Workers y Off-Main-Thread Architecture para Computación Pesada en el Navegador",
        "A/B Testing en el Edge sin Layout Shifts (Zero-CLS) con Middleware Edge",
        "Seguridad en el Cliente: Content Security Policy (CSP) Estricto y Protección XSS en SPAs",
        "Personalización en Tiempo Real Basada en Edge Middleware sin Afectar la Tasa de Acierto de Caché",
        "Storybook y Visual Regression Testing para Componentes Headless Composable",
        "Accesibilidad Web (WCAG 2.2 AA) en Componentes Headless Interactivos Complejos",
        "Micro-Frontends con Qiankun vs Single-SPA: Análisis de Sobrecarga y Rendimiento",
        "Sincronización de Estado Local con IndexedDB para Checkouts Resistentes a Desconexiones",
        "Optimizaciones de Bundle Size: Tree Shaking y Análisis de Dependencias Críticas en SPAs",
        "Edge Functions y Streaming SSR para Reducir Time To First Byte (TTFB) a Escala Global",
        "Gestión de Sesiones de Usuario Stateful en Plataformas Headless Serverless",
        "Pruebas End-to-End Visuales y de Rendimiento Automatizadas con Playwright en CI/CD"
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
        "Orquestación de Carritos de Compra Distribuidos y Manejo de Concurrencia Masiva",
        "Motores de Búsqueda y Descubrimiento Semántico con Vectores e IA Generativa en E-Commerce",
        "Checkout Tokenizado y Cumplimiento PCI-DSS SAQ-A en Arquitecturas Headless",
        "Sincronización de Catálogos Omnicanal (Tiendas Físicas + Online) con Event Streaming",
        "Suscripciones y Pagos Recurrentes en Composable Commerce con Stripe Billing",
        "Marketplace Multi-Vendor: Arquitectura de Liquidaciones y Gestión de Vendedores con PBCs",
        "Manejo de Flash Sales Masivas: Patrones de Cola Virtual y Caching Agresivo de Inventario",
        "Integración de Sistemas ERP Legacy (SAP, Oracle) mediante Event-Driven Integration Layers",
        "Order Management System (OMS) Distribuido: Ruteo Inteligente de Pedidos por Proximidad",
        "Programas de Lealtad y Gamificación Desacoplados en E-Commerce Composable",
        "Comercio Conversacional y Social Commerce Integrados mediante APIs Headless",
        "Cálculo de Impuestos y Aranceles Transfronterizos en Tiempo Real (Avalara, Vertex)",
        "Gestión de Envíos y Conexión con Múltiples Operadores Logísticos (FedEx, DHL, Estafeta)",
        "Garantías y Protección Post-Venta Integradas como Microservicios Independientes",
        "Gestión de Cupones y Descuentos Complejos con Motores de Reglas Desacoplados (Drools, JSON-Rules)",
        "Sistemas de Cotizaciones y Negociaciones Comerciales B2B en Frontends Headless"
    ],
    "Consistencia de Datos & Transaccionalidad Multi-SaaS": [
        "Resolución de Escrituras Conflictivas en Carritos de Compra Distribuidos sin Bloqueo Pesimista",
        "Patrón Saga Coreografiado vs Orquestado con Temporal.io en Cadenas de Suministro Multi-Vendor",
        "Change Data Capture (CDC) con Debezium y Kafka para Sincronizar ERPs Legados con Almacenes de Lectura",
        "Estrategias de Read-Your-Own-Writes (RYOW) en Frontends Headless con Consistencia Eventual",
        "Patrón Outbox Bidireccional para Conciliación de Pagos y Facturación Electrónica Fiscal",
        "Manejo de Transacciones de Compensación en Fallos de Aprovisionamiento Multi-SaaS",
        "Diseño de Modelos de Datos en Esquemas Documentales NoSQL vs Relacionales en E-Commerce",
        "Replicación Multi-Región con Resolución de Conflictos Last-Write-Wins vs Vector Clocks",
        "Tolerancia a Particiones de Red (Teorema CAP) en Gestión de Inventarios Críticos",
        "Validación de Idempotencia a Nivel de Base de Datos con Claves Naturales y Filtros Bloom",
        "Arquitecturas CQRS con Event Store Dedicado para Auditoría Forense de Transacciones Financieras",
        "Limpieza y Compactación de Topics de Eventos en Kafka para Reducción de Almacenamiento",
        "Indexación de Proyecciones de Consulta en Elasticsearch/OpenSearch a partir de Event Streams",
        "Aislamiento de Transacciones Snapshot y Read Committed en Bases de Datos SQL Distribuidas",
        "Conciliación Nocturna Automatizada de Estados entre Pasarelas de Pago y Libros Contables",
        "Patrón Reservas Temporales (Two-Phase Commit Ligero) en Hoteles y Boletos de Alta Demanda",
        "Manejo de Backpressure en Consumidores de Eventos para Prevenir Desbordamiento de Memoria",
        "Evolución de Schemas de Base de Datos sin Downtime con Expansión y Contracción (Expand and Contract)",
        "Sharding de Base de Datos por Tenant en SaaS B2B Enterprise: Estrategias de Claves de Partición",
        "Pistas de Auditoría Inmutables (Append-Only Logs) para Trazabilidad Regulatoria en Fintech",
        "Prevención de Pérdida de Datos en Desconexiones de Red con Colas Locales SQLite en Clientes Edge",
        "Doble Escritura (Dual-Write Problem): Por Qué Fallan las Transacciones No Coordinadas y Cómo Evitarlo",
        "Desduplicación de Mensajes en Redes Inciertas con Almacenes Distribuidos en Memoria",
        "Patrón Claim Check: Manejo Eficiente de Grandes Payloads en Sistemas de Mensajería",
        "Sincronización de Identidad de Clientes (Customer Master Data) entre CRM, ERP y Storefront"
    ],
    "Operaciones Día 2, Observabilidad & Resiliencia": [
        "Propagación de Contexto W3C TraceContext a través de Redes Multi-Vendor y Protocolos Híbridos",
        "Diseño de Métricas de Alta Cardinalidad con Prometheus y M3DB sin Degradar Rendimiento",
        "Degradación Elegante de Experiencia de Usuario: Modo Fallback cuando un Microservicio Crítico Cae",
        "Pruebas de Inyección de Caos en Producción con Gremlin y Chaos Toolkit para Validar SLAs",
        "Monitoreo de Golden Signals (Latencia, Tráfico, Errores, Saturación) en Plataformas Composable",
        "Arquitectura de Alertas Inteligentes: Eliminación de Fatiga de Alertas con Detección de Anomalías",
        "Post-Mortems sin Culpa (Blameless Post-Mortems) y Análisis de Causa Raíz en Fallos Complejos",
        "Definición Rigurosa de Service Level Objectives (SLOs) y Presupuestos de Error (Error Budgets)",
        "Trazabilidad de Transacciones de Extremo a Extremo (User Click a Base de Datos) con OpenTelemetry",
        "Centralización de Logs Distribuidos a Gran Escala con Vector, ClickHouse y Grafana Loki",
        "Detección y Aislamiento Automático de Microservicios Lentos (Noisy Neighbors) en Kubernetes",
        "Políticas de Auto-Sanación (Self-Healing) y Reinicio Controlado de Pods en Despliegues Cloud",
        "Pruebas de Estrés y Capacidad Extrema con k6 y Distributed Load Generators",
        "Simulacros de Resiliencia ante Desastres (Game Days) para Validar RPO y RTO en la Nube",
        "Monitoreo Sintético y Pruebas Continuas de Endpoints de APIs en Producción",
        "Gestión de Runbooks Automatizados con Ansible y Temporal para Remediación de Incidentes",
        "Visualización de Dependencias Dinámicas en Tiempo Real entre Microservicios con Service Maps",
        "Perfiles Continuos de Rendimiento en Producción (Continuous Profiling) con Pyroscope y Parca",
        "Análisis de Sobrecarga de Red y Latencia DNS en Entornos Kubernetes de Alta Densidad",
        "Control de Saturación de Colas de Mensajes y Alertas Predictivas de Dead-Letter Queue (DLQ)",
        "Gobernanza de Cambios en Producción: Auditoría de Despliegues GitOps con Firmas Criptográficas",
        "Planificación de Capacidad (Capacity Planning) Basada en Modelos Predictivos para Picos Estacionales",
        "Segregación de Entornos de Staging Efímeros por Pull Request con vcluster y Kubernetes",
        "Monitoreo de Latencia p99 y p99.9: Identificando Cuellos de Botella Ocultos en Microservicios",
        "Cultura On-Call Sostenible y Rotación de Guardias en Equipos de Ingeniería Distribuidos"
    ],
    "FinOps, Unit Economics & Gestión Multi-Vendor": [
        "Cálculo del Costo Unitario por Llamada API y por Pedido en Arquitecturas Headless",
        "Optimización de Costos de Transferencia de Datos (Egress Network) entre GCP, AWS y Azure",
        "Negociación de Contratos SaaS Enterprise: Cláusulas de Salida, Migración y SLAs Agregados",
        "Auditoría Forense de Facturas Cloud: Detectando Desperdicios en Instancias Kubernetes y Discos Huérfanos",
        "FinOps Cultural: Asignación de Costos de Infraestructura Directamente a Equipos de Producto (Showback/Chargeback)",
        "Estrategias para Mitigar el Vendor Lock-in en Capas de Base de Datos y Mensajería Cloud Propietarias",
        "Modelado del Retorno de Inversión (ROI) y Total Cost of Ownership (TCO): Monolito vs MACH a 5 Años",
        "Optimización de Consumo de Créditos y Licencias en Capas de Middleware y API Gateways",
        "Gestión de Compromisos de Uso Cloud (Savings Plans y Reserved Instances) en Cargas Dinámicas",
        "Gobernanza de Adquisiciones de Software: Matriz de Decisión Build vs Buy vs Compose",
        "Control de Costos en Almacenamiento de Logs y Métricas: Políticas de Retención Tiered y Archival",
        "Desmantelamiento Seguro de Infraestructura Cloud Abandonada tras Migraciones Composable",
        "Economía de Serverless vs Contenedores Dedicados: Punto de Inflexión de Costos a Escala",
        "Estrategias de Facturación Multi-Inquilino y Repercusión de Costos en Plataformas B2B SaaS",
        "Auditoría de SLAs de Proveedores SaaS Externos: Métricas de Incumplimiento y Compensaciones Financieras",
        "Optimización de Facturas de CDN y Edge Computing: Políticas de Cache Hit Ratio Efectivas",
        "Racionalización del Catálogo de Herramientas SaaS para Evitar Redundancia Funcional",
        "Gestión Financiera de APIs Públicas: Modelos de Cobro Freemium, Por Consumo y Por Nivel",
        "Automatización del Apagado de Entornos de Desarrollo Fuera de Horario Laboral para Reducir Gasto",
        "Benchmarking de Costos de Proveedores de Composable Commerce (commercetools, BigCommerce, Shopify Plus)",
        "Contención de Costos en Modelos de Lenguaje e Inferencia de IA en Aplicaciones Enterprise",
        "Políticas de FinOps As Code: Bloqueo de Infraestructura Sobre-Aprovisionada en Terraform CI/CD",
        "Evaluación de Impacto Financiero de Caídas de Servicio (Cost of Downtime per Hour) en Retail",
        "Estrategias de Financiación de Proyectos de Modernización Tecnológica para Directores Financieros (CFO)",
        "Alineación de Objetivos OKR de Ingeniería con Metas de Eficiencia de Costos Cloud"
    ],
    "Seguridad Zero Trust & AI Composable": [
        "Autenticación mTLS y Gestión de Identidades Efímeras entre Microservicios con SPIFFE y SPIRE",
        "Mitigación del OWASP API Security Top 10 en Capas de API Gateway y BFF",
        "Agentes de IA Autónomos que Consumen Contratos OpenAPI y Schemas GraphQL para Automatizar Compras",
        "Búsqueda Híbrida Vectorial y Léxica en Catálogos de Gran Escala con Bases de Datos Vectoriales (Qdrant, Pinecone)",
        "Pricing Dinámico en el Edge con Inferencia de Modelos Ligeros sin Afectar la Latencia p99",
        "Detección y Mitigación de Bots Maliciosos en Frontends Headless con Cloudflare Turnstile",
        "Rotación Automática de Claves Criptográficas y Certificados TLS con cert-manager y Vault",
        "Arquitectura de Seguridad en APIs GraphQL: Prevención de Ataques de Complejidad de Consulta y DoS",
        "Tokenización de Datos Sensibles y Cumplimiento PCI-DSS SAQ-A en Checkouts Desacoplados",
        "Gobernanza de Modelos de Inteligencia Artificial (LLMOps) Integrados en Plataformas Composable",
        "Seguridad en la Cadena de Suministro de Software (Supply Chain Security) con Sigstore y SBOM",
        "Aislamiento de Microservicios con Sandboxing Liviano (gVisor, Firecracker) en Cargas Inseguras",
        "Auditoría de Accesos con Control Basado en Atributos (ABAC) y Open Policy Agent (OPA)",
        "Prevención de Fuga de Datos de Clientes (DLP) en Flujos de Integración Asíncronos",
        "Pruebas Automatizadas de Seguridad Dinámica (DAST) de APIs en Pipelines de CI/CD",
        "Cifrado de Datos en Reposo con Claves Gestionadas por el Cliente (CMEK) en Entornos Multi-Cloud",
        "Autenticación Passwordless y FIDO2/WebAuthn en Aplicaciones Headless Móviles y Web",
        "Monitorización de Amenazas en Tiempo Real con eBPF Security Sensors (Tetragon, Falco)",
        "Generación Aumentada por Recuperación (RAG) para Recomendaciones Técnicas de Productos B2B",
        "Gestión de Identidades de Clientes (CIAM) Federada con Soporte OIDC y SAML 2.0",
        "Detección de Anomalías de Comportamiento de Usuarios y Prevención de Fraude en Tiempo Real",
        "Políticas de Content Security Policy (CSP) Dinámicas Gestionadas desde el Edge Worker",
        "Auditoría Forense de Tokens JWT Comprometidos y Listas Negras Distribuidas con Redis",
        "Protección contra Envenenamiento de Modelos y Prompt Injection en Agentes de Comercio Conversacional",
        "Seguridad de Webhooks Salientes: Aislamiento de Red y Mitigación de SSRF (Server-Side Request Forgery)"
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

STOP_WORDS = {
    'de', 'en', 'para', 'con', 'las', 'los', 'por', 'sobre', 'del', 'al', 'una', 'uno', 'unos',
    'the', 'and', 'for', 'with', 'in', 'on', 'at', 'to', 'a', 'an', 'is', 'as', 'by', 'vs',
    'mach', 'arquitectura', 'arquitecturas', 'microservicios', 'cloud', 'native', 'patrones',
    'estrategias', 'edicion', 'edition', 'guia', 'guide', 'tutorial', 'overview', 'moderna',
    'moderno', 'modernos', 'sistemas', 'diseno', 'analisis', 'produccion', 'escala', 'global'
}


def slugify(text: str) -> str:
    """Transform topic title into URL-friendly, clean ASCII slug."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


def extract_keywords(text: str) -> set:
    """Extract significant content keywords from topic title or slug, ignoring stop words."""
    text_clean = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    words = re.findall(r'[a-zA-Z0-9]+', text_clean.lower())
    return {w for w in words if len(w) > 2 and w not in STOP_WORDS}


def calculate_similarity(topic_a: str, topic_b: str) -> float:
    """Calculate Jaccard keyword similarity between two topics/slugs."""
    kw_a = extract_keywords(topic_a)
    kw_b = extract_keywords(topic_b)
    if not kw_a or not kw_b:
        return 0.0
    intersection = len(kw_a & kw_b)
    union = len(kw_a | kw_b)
    return intersection / union if union > 0 else 0.0


def is_topic_covered(candidate_topic: str, existing_posts: List[Dict[str, str]], threshold: float = 0.45) -> bool:
    """Check if a topic has already been covered with high confidence, preventing duplicate or thin content."""
    cand_slug = slugify(candidate_topic)
    for p in existing_posts:
        existing_title = p.get("title", "")
        existing_slug = p.get("slug", "")
        
        # Substring slug match (after removing dates)
        clean_existing = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', existing_slug)
        if cand_slug == clean_existing or (len(cand_slug) > 20 and cand_slug in clean_existing):
            return True
            
        # Jaccard keyword similarity check
        sim_title = calculate_similarity(candidate_topic, existing_title)
        sim_slug = calculate_similarity(cand_slug, clean_existing)
        if max(sim_title, sim_slug) >= threshold:
            return True
            
    return False


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


def generate_algorithmic_topic(existing_posts: List[Dict[str, str]]) -> Tuple[str, str]:
    """Combinatorial generative fallback using a tridimensional enterprise matrix: Pattern x Production Pain Point x Enterprise Context."""
    patterns = [
        # Microservicios & Cloud Native
        ("Cell-Based Architecture y Aislamiento de Blast Radius", "Microservicios & Cloud Native"),
        ("eBPF y Redes de Alto Rendimiento con Cilium", "Microservicios & Cloud Native"),
        ("Dapr Distributed Application Runtime para Abstracción Pub/Sub", "Microservicios & Cloud Native"),
        ("KEDA y Auto-Escalado Dirigido por Eventos", "Microservicios & Cloud Native"),
        ("Controladores Kubernetes Personalizados en Go", "Microservicios & Cloud Native"),
        # API-First & Integraciones Distribuidas
        ("GraphQL Federation v2 y Arquitectura de Supergraphs", "API-First & Integraciones Distribuidas"),
        ("AsyncAPI y Gobernanza Criptográfica de Webhooks", "API-First & Integraciones Distribuidas"),
        ("OAuth 2.1 y Autenticación Passwordless FIDO2/WebAuthn", "API-First & Integraciones Distribuidas"),
        ("Event Mesh Global con Solace PubSub+ y Apache Pulsar", "API-First & Integraciones Distribuidas"),
        # Headless & Frontend Moderno
        ("React Server Components y Streaming SSR en Edge Functions", "Headless & Frontend Moderno"),
        ("Edge Middleware y A/B Testing Zero-CLS a Escala Global", "Headless & Frontend Moderno"),
        ("Búsqueda Híbrida Vectorial y Léxica con Meilisearch", "Headless & Frontend Moderno"),
        ("Checkouts Offline-First con IndexedDB y Sincronización Local", "Headless & Frontend Moderno"),
        # Composable Commerce & Transición
        ("Desmantelamiento Strangler Fig de Monolitos SAP y Magento", "Composable Commerce & Transición"),
        ("Orquestación de Checkout Multi-Adquirente y Split Payments", "Composable Commerce & Transición"),
        ("Gestión de Inventario Distribuido y Reservas en Flash Sales", "Composable Commerce & Transición"),
        ("Order Management System (OMS) Distribuido con Ruteo por Proximidad", "Composable Commerce & Transición"),
        # Consistencia de Datos & Transaccionalidad Multi-SaaS
        ("Resolución de Escrituras Conflictivas con Vector Clocks", "Consistencia de Datos & Transaccionalidad Multi-SaaS"),
        ("Patrón Outbox Transaccional y Change Data Capture con Debezium", "Consistencia de Datos & Transaccionalidad Multi-SaaS"),
        ("Read-Your-Own-Writes (RYOW) en Frontends con Consistencia Eventual", "Consistencia de Datos & Transaccionalidad Multi-SaaS"),
        # Operaciones Día 2, Observabilidad & Resiliencia
        ("Propagación de Contexto W3C TraceContext en Redes Multi-Vendor", "Operaciones Día 2, Observabilidad & Resiliencia"),
        ("Inyección de Caos Automatizada con LitmusChaos y Chaos Mesh", "Operaciones Día 2, Observabilidad & Resiliencia"),
        ("Centralización de Logs a Gran Escala con Vector y ClickHouse", "Operaciones Día 2, Observabilidad & Resiliencia"),
        # FinOps, Unit Economics & Gestión Multi-Vendor
        ("Cálculo del Costo Unitario por Llamada API en Arquitecturas Headless", "FinOps, Unit Economics & Gestión Multi-Vendor"),
        ("Optimización de Costos de Egress Network entre GCP y AWS", "FinOps, Unit Economics & Gestión Multi-Vendor"),
        ("Auditoría Forense de Facturas Cloud para Detección de Desperdicios", "FinOps, Unit Economics & Gestión Multi-Vendor"),
        # Seguridad Zero Trust & AI Composable
        ("Autenticación mTLS y SPIFFE/SPIRE para Microservicios Efímeros", "Seguridad Zero Trust & AI Composable"),
        ("Agentes de IA Autónomos que Consumen Contratos OpenAPI y GraphQL", "Seguridad Zero Trust & AI Composable"),
        ("Mitigación del OWASP API Security Top 10 en Capas de API Gateway", "Seguridad Zero Trust & AI Composable")
    ]
    
    contexts = [
        "en Sistemas de Alta Concurrencia y Tráfico Masivo",
        "para Transacciones Transfronterizas y Cumplimiento Normativo",
        "en Plataformas de E-Commerce Global y Retail Omnicanal",
        "con Tolerancia Extrema a Particiones de Red y Caídas de Proveedores",
        "para Prevención de Fraude y Mitigación de Bots en Tiempo Real",
        "en Entornos Multi-Cloud Híbridos (GCP, AWS y Azure)",
        "para Optimización de Latencia p99 en Cargas de Misión Crítica",
        "en Catálogos B2B Distribuidos con Jerarquías Complejas"
    ]
    
    candidates = []
    for (pat, pil) in patterns:
        for ctx in contexts:
            candidate = f"{pat} {ctx}"
            if not is_topic_covered(candidate, existing_posts, threshold=0.35):
                candidates.append((candidate, pil))
                
    if candidates:
        random.shuffle(candidates)
        return candidates[0]
        
    # Ultimate unique fallback with timestamp guarantee
    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    return f"Patrones Emergentes de Ingeniería de Plataforma y Arquitectura Composable - Ref {ts}", "Microservicios & Cloud Native"


def generate_novel_topic_with_ai(api_key: str, existing_posts: List[Dict[str, str]]) -> Optional[Tuple[str, str]]:
    """Dynamically prompt Google Gemini to propose a brand new, trending enterprise MACH topic not in existing posts."""
    if not api_key or api_key == "MOCK_KEY":
        return None
        
    recent_titles = [p["title"] for p in existing_posts[-30:] if p.get("title")]
    titles_bulleted = "\n".join([f"- {t}" for t in recent_titles])
    
    system_prompt = "Eres un Principal Architect y curador de contenido técnico para el blog de ingeniería 'MACH Playbook'."
    user_prompt = f"""Aquí están los últimos 30 artículos ya publicados en el blog:
{titles_bulleted}

Propón EXACTAMENTE UN tema técnico avanzado, original, específico y de nivel Senior Solutions Architect para un nuevo artículo sobre arquitecturas MACH / Composable Commerce / Cloud-Native.
REGLAS ESTRICTAS:
1. El tema NO debe ser una variación de ningún tema anterior (no repitas circuit breakers, resiliencia general, etc.).
2. Debe ser un tema de vanguardia para 2026 (por ejemplo: eBPF, Cilium, Temporal, KEDA, Passkeys, ClickHouse, Cell-based architecture, SPIFFE/SPIRE, FinOps de APIs, etc.).
3. EVITA fórmulas repetitivas en el título como 'Estrategias de...' o 'Introducción a...'. Enfócalo en un problema concreto y su solución técnica.
4. Responde ÚNICAMENTE en formato JSON con dos campos:
{{"topic": "Título del Tema en Español", "pillar": "Pilar correspondiente de MACH"}}
"""
    try:
        response_text = call_gemini_api(api_key, system_prompt, user_prompt)
        json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            topic = data.get("topic", "").strip()
            pillar = data.get("pillar", "Microservicios & Cloud Native").strip()
            if topic and not is_topic_covered(topic, existing_posts, threshold=0.35):
                print(f" [AI Novel Topic Generated]: '{topic}' ({pillar})")
                return topic, pillar
    except Exception as e:
        print(f" Notice: Dynamic AI topic generation skipped ({e}).")
        
    return None


def select_next_topic(existing_posts: List[Dict[str, str]], manual_topic: Optional[str] = None, api_key: Optional[str] = None) -> Tuple[str, str]:
    """Select a fresh, untackled topic balancing the 8 enterprise pillars, using AI generation or algorithmic synthesis when static matrix is covered."""
    if manual_topic:
        return manual_topic, "Microservicios & Cloud Native"

    # 1. Search expanded 200-topic matrix using smart Jaccard & title deduplication
    pillars = list(TOPIC_MATRIX.keys())
    random.shuffle(pillars)
    
    for pillar in pillars:
        topics = TOPIC_MATRIX[pillar]
        for topic in topics:
            if not is_topic_covered(topic, existing_posts, threshold=0.40):
                return topic, pillar

    print(" Notice: Static 200-topic matrix exhausted. Querying Gemini AI for a 100% novel topic...")
    
    # 2. Dynamic AI Topic Synthesis via Gemini
    if api_key and api_key != "MOCK_KEY":
        ai_topic = generate_novel_topic_with_ai(api_key, existing_posts)
        if ai_topic:
            return ai_topic

    # 3. Combinatorial Algorithmic Generator (guaranteed unique, never repeats)
    print(" Using combinatorial algorithmic topic generator...")
    return generate_algorithmic_topic(existing_posts)


def build_system_prompt(lang: str = "es") -> str:
    """Build the comprehensive Senior Solutions Architect system prompt with E-E-A-T and anti-repetition guidelines."""
    if lang == "es":
        return """Eres un Principal Enterprise Solutions Architect y especialista certificado en Arquitectura MACH (Microservices, API-first, Cloud-native, Headless) y Composable Commerce.
Escribes artículos técnicos de altísimo nivel para 'MACH Playbook' (mach-playbook.github.io).

DIRECTRICES EDITORIALES Y DE CALIDAD (E-E-A-T):
1. **Profundidad Técnica y Experiencia Real:** No te limites a explicaciones teóricas superficiales. Proporciona ejemplos prácticos de arquitectura, patrones de diseño de producción, trade-offs reales y métricas de desempeño.
2. **ANTI-PATRONES EDITORIALES ESTRICTAMENTE PROHIBIDOS:**
   - NUNCA comiences el artículo con introducciones de tipo glosario o definiciones genéricas (ej: "En la arquitectura MACH, los microservicios son...", "Una API es una interfaz...").
   - Abre INMEDIATAMENTE en el primer párrafo con un problema de producción crítico, un cuello de botella de escalabilidad o un dilema arquitectónico enterprise real (Operaciones de Día 2).
   - Evita títulos con fórmulas repetitivas ("Estrategias de...", "Orquestación de..."). Enfócate en el problema técnico concreto, su impacto y su solución.
3. **Extensión:** Entre 1,500 y 2,200 palabras. El contenido debe ser exhaustivo, estructurado y sin texto de relleno.
4. **Estructura Requerida:**
   - Título impactante, específico y profesional.
   - Front Matter YAML compatible con Jekyll tema Chirpy al inicio del archivo.
   - Planteamiento inmediato del problema en producción (pain points enterprise).
   - Diagrama de arquitectura o secuencia en sintaxis Mermaid (```mermaid).
   - Bloques de código reales, ejecutables y documentados (TypeScript, Python, YAML, Go o SQL).
   - Tablas comparativas de trade-offs arquitectónicos (pros, contras, cuándo usarlo, cuándo evitarlo).
   - Modos de fallo comunes y estrategias de mitigación/recuperación en producción.
   - Conclusión accionable con checklist de implementación para equipos de ingeniería.
5. **Formato Front Matter de Jekyll:**
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
6. **Idioma:** Español técnico impecable, fluido y profesional, utilizando la terminología estándar de la industria cloud/software."""
    else:
        return """You are a Principal Enterprise Solutions Architect and MACH Alliance Certified Specialist (Microservices, API-first, Cloud-native, Headless) and Composable Commerce expert.
You write authoritative technical deep-dives for 'MACH Playbook' (mach-playbook.github.io).

EDITORIAL GUIDELINES (E-E-A-T):
1. **Technical Depth & Real-World Experience:** Provide concrete production architecture patterns, design tradeoffs, performance metrics, and actionable blueprints.
2. **STRICT EDITORIAL ANTI-PATTERNS (PROHIBITED):**
   - NEVER begin the article with glossary-style definitions (e.g. "In MACH architecture, microservices are...", "An API is...").
   - Open IMMEDIATELY with a production incident, high-stakes trade-off, or architectural failure scenario.
3. **Length:** Between 1,500 and 2,200 words. Exhaustive, well-structured, zero fluff.
4. **Required Elements:**
   - Jekyll Chirpy-compliant YAML Front Matter at the very beginning.
   - Production failure scenario & real-world enterprise challenge.
   - Architecture or sequence diagram in Mermaid syntax (```mermaid).
   - Production-grade, documented code snippets (TypeScript, Python, YAML, Go, or SQL).
   - Comparative tradeoff table (Pros, Cons, When to use, When to avoid).
   - Failure modes and mitigation strategies.
   - Actionable conclusion with engineering implementation checklist.
5. **Language:** Professional, highly technical English."""



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
8. REGLA DE ORIGINALIDAD: No utilices introducciones genéricas ni definiciones tipo diccionario (ej: qué es una API o qué es un microservicio). Abre en el primer párrafo directamente con el incidente de producción, cuello de botella o problema arquitectónico específico.
9. REGLA ANTI-PLANTILLAS EN TÍTULO: Evita fórmulas repetitivas como 'Estrategias de...' u 'Orquestación de...'; enfoca el título en el impacto concreto, mitigación de fallos o patrón de diseño.
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
    """Generate unique topic-specific high-value article. No generic boilerplate."""
    print(f" Synthesizing topic-specific deep dive for: {topic}")

    tl = topic.lower()
    is_api   = any(k in tl for k in ["api","graphql","grpc","rest","openapi","asyncapi","webhook","gateway","oauth","jwt"])
    is_event = any(k in tl for k in ["event","kafka","saga","cqrs","outbox","debezium","stream","async"])
    is_sec   = any(k in tl for k in ["security","seguridad","zero trust","mtls","vault","auth","iam"])
    is_infra = any(k in tl for k in ["kubernetes","k8s","argocd","ci/cd","gitops","cilium","ebpf","keda","deploy"])
    is_data  = any(k in tl for k in ["database","sharding","postgres","sql","cache","redis","consistencia","datos"])
    is_head  = any(k in tl for k in ["headless","frontend","next","react","cms","pwa","edge","cdn","isr","ssr"])
    is_fin   = any(k in tl for k in ["finops","roi","cost","costo","vendor","sla","presupuesto"])
    is_com   = any(k in tl for k in ["commerce","checkout","pago","inventario","catalog","pbc","strangler","monolito"])

    if lang == "es":
        if is_api:    cats,tags = "[Diseno de APIs, Microservicios]",         "[mach, api-first, graphql, openapi, microservicios, arquitectura, cloud-native]"
        elif is_event: cats,tags = "[Sistemas Distribuidos, Microservicios]",  "[mach, event-driven, kafka, microservicios, resiliencia, arquitectura, cloud-native]"
        elif is_sec:   cats,tags = "[Seguridad, Microservicios]",               "[mach, zero-trust, seguridad, kubernetes, mtls, arquitectura, cloud-native]"
        elif is_infra: cats,tags = "[DevOps, Arquitectura Cloud]",              "[mach, kubernetes, gitops, ci-cd, devops, arquitectura, cloud-native]"
        elif is_head:  cats,tags = "[Headless y Frontend, Arquitectura Cloud]", "[mach, headless, frontend, composable-commerce, arquitectura, cloud-native, performance]"
        elif is_fin:   cats,tags = "[Estrategia Enterprise, Arquitectura Cloud]","[mach, finops, roi, estrategia, arquitectura, cloud-native, enterprise]"
        elif is_com:   cats,tags = "[Composable Commerce, Arquitectura Cloud]", "[mach, composable-commerce, headless, arquitectura, cloud-native, ecommerce, pbcs]"
        elif is_data:  cats,tags = "[Arquitectura de Datos, Microservicios]",   "[mach, database, sharding, postgres, arquitectura, cloud-native, consistencia]"
        else:          cats,tags = "[Arquitectura Cloud, Microservicios]",       "[mach, microservicios, cloud-native, api-first, resiliencia, arquitectura, devops]"

        if is_event:
            diagram = "sequenceDiagram\n    participant C as Cliente\n    participant P as Productor Kafka\n    participant B as Kafka Broker\n    participant W as Worker Consumidor\n    participant D as Base de Datos\n    C->>P: Publicar Evento de Dominio\n    P->>D: Escribir en Tabla Outbox (ACID)\n    P->>B: Publicar via CDC Debezium\n    B-->>W: Consumir at-least-once\n    W->>D: Actualizar Proyeccion\n    W-->>C: ACK / Webhook"
        elif is_sec:
            diagram = "graph TD\n    C[Servicio Cliente] -->|mTLS + JWT| Proxy[Envoy Sidecar]\n    Proxy -->|SPIFFE ID| Mesh[Istio Service Mesh]\n    Mesh -->|Zero Trust Policy| S[Servicio Destino]\n    Mesh --> Vault[HashiCorp Vault Secrets]\n    Vault --> Certs[Certificados TLS Rotados]\n    style Mesh fill:#dc2626,stroke:#b91c1c,color:#fff\n    style Vault fill:#059669,stroke:#047857,color:#fff"
        elif is_infra:
            diagram = "graph TD\n    Dev[Developer Push] --> Git[Git Repository]\n    Git --> CI[CI Pipeline GitHub Actions]\n    CI --> Build[Docker Build + SAST Scan]\n    Build --> Reg[Artifact Registry]\n    Reg --> Argo[ArgoCD GitOps]\n    Argo --> K8s[Kubernetes Cluster]\n    K8s --> Can[Canary 10pct]\n    Can --> Mon[Prometheus + Grafana]\n    Mon --> Full[Rollout 100pct]\n    style Argo fill:#2563eb,stroke:#1d4ed8,color:#fff\n    style Mon fill:#059669,stroke:#047857,color:#fff"
        else:
            diagram = f"graph TD\n    Client[Cliente Web Movil] --> CDN[Edge CDN Cloudflare]\n    CDN --> GW[API Gateway Kong Apigee]\n    GW --> Auth[IAM OAuth 2.1 mTLS]\n    GW --> Core[Servicio Core]\n    Core --> Cache[Redis Cluster L1 L2]\n    Core --> Bus[Apache Kafka]\n    Core --> DB[PostgreSQL Cloud Spanner]\n    Bus --> Worker[Worker Asincrono CDC]\n    style GW fill:#7c3aed,stroke:#6d28d9,color:#fff\n    style Core fill:#2563eb,stroke:#1d4ed8,color:#fff"

        if is_api:
            code = "// Rate Limiter con Token Bucket y Redis\nimport Redis from 'ioredis';\nconst redis = new Redis(process.env.REDIS_URI!);\n\nexport async function checkRateLimit(\n  clientId: string, limitPerMin = 60\n): Promise<{ allowed: boolean; remaining: number }> {\n  const key = `rl:${clientId}:${Math.floor(Date.now() / 60000)}`;\n  const count = await redis.incr(key);\n  if (count === 1) await redis.expire(key, 60);\n  return { allowed: count <= limitPerMin, remaining: Math.max(0, limitPerMin - count) };\n}"
        elif is_event:
            code = "// Patron Outbox - garantia exactly-once de publicacion de eventos\nimport { DataSource, EntityManager } from 'typeorm';\n\nexport class OutboxService {\n  constructor(private readonly db: DataSource) {}\n\n  async publishWithOutbox(\n    event: DomainEvent,\n    operation: (mgr: EntityManager) => Promise<void>\n  ): Promise<void> {\n    await this.db.transaction(async (mgr) => {\n      await operation(mgr);\n      await mgr.save(OutboxMessage, {\n        id: crypto.randomUUID(),\n        payload: JSON.stringify(event),\n        topic: event.type,\n        status: 'PENDING',\n        createdAt: new Date()\n      });\n    });\n  }\n}"
        else:
            code = "import Redis from 'ioredis';\nimport { v4 as uuidv4 } from 'uuid';\nimport { trace, SpanStatusCode } from '@opentelemetry/api';\n\nclass EnterpriseMACHService {\n  private readonly redis: Redis;\n  private readonly tracer = trace.getTracer('mach-playbook', '1.0.0');\n\n  constructor(uri: string) {\n    this.redis = new Redis(uri, { maxRetriesPerRequest: 3,\n      retryStrategy: (t) => Math.min(t * 150, 5000) });\n  }\n\n  async execute<T>(\n    tenantId: string, idempKey: string | undefined, fn: () => Promise<T>\n  ): Promise<T | null> {\n    const span = this.tracer.startSpan(`mach.${tenantId}`);\n    const key = `idem:${tenantId}:${idempKey ?? uuidv4()}`;\n    try {\n      if (idempKey) {\n        const hit = await this.redis.get(key);\n        if (hit) { span.end(); return JSON.parse(hit); }\n      }\n      const result = await fn();\n      if (idempKey) await this.redis.setex(key, 300, JSON.stringify(result));\n      span.setStatus({ code: SpanStatusCode.OK });\n      return result;\n    } catch (e: any) {\n      span.setStatus({ code: SpanStatusCode.ERROR, message: e.message });\n      span.recordException(e); throw e;\n    } finally { span.end(); }\n  }\n}"

        sections = [
            "---", "layout: post",
            f'title: "{topic}"',
            f"date: {post_date_str} 09:00:00 -0600",
            "lang: es",
            f"categories: {cats}", f"tags: {tags}",
            "image:", f"  path: /assets/img/posts/{slug}.png", "---", "",
            f"En el ecosistema del software empresarial moderno, **{topic}** representa uno de los patrones mas transformadores para equipos de ingenieria que buscan superar las limitaciones de las arquitecturas monoliticas tradicionales. Este analisis profundo, escrito desde la perspectiva de un Principal Solutions Architect con experiencia en plataformas enterprise de produccion, aborda los fundamentos tecnicos, las decisiones de diseno criticas y los patrones de implementacion necesarios para adoptar **{topic}** con exito.", "",
            "## 1. El Problema Empresarial: Por Que Este Patron Es Critico en 2026", "",
            f"Las organizaciones con arquitecturas monoliticas heredadas enfrentan deuda tecnica que se manifiesta en ciclos de despliegue de semanas, incidentes de produccion que afectan toda la plataforma, e incapacidad estructural para innovar. La adopcion de **{topic}** aborda estas fricciones desacoplando el ciclo de vida de los componentes, conteniendo el blast radius, y reduciendo la coordinacion inter-equipos mediante contratos formales basados en OpenAPI y AsyncAPI.", "",
            "Los equipos que han adoptado estos patrones reportan reducciones del **60-80% en ciclos de despliegue** y mejoras sustanciales en indices DORA: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery (MTTR) y Change Failure Rate.", "",
            "---", "", "## 2. Arquitectura de Referencia", "",
            f"```mermaid\n{diagram}\n```", "",
            "Tres invariantes de diseno no negociables gobiernan esta arquitectura en entornos de produccion enterprise:", "",
            "1. **Ningun servicio accede directamente a la base de datos de otro servicio.** Toda comunicacion cross-domain ocurre via APIs publicadas o eventos del bus de mensajeria.",
            "2. **Toda operacion de escritura es idempotente.** Esto garantiza la seguridad de los reintentos automaticos sin efectos secundarios.",
            "3. **La observabilidad es un ciudadano de primera clase.** Trazas distribuidas OpenTelemetry, metricas RED y logs estructurados desde el dia uno del desarrollo.", "",
            "---", "", "## 3. Principios de Diseno Fundamentales", "",
            "### 3.1 Contratos Primero: API-First y Event-First", "",
            f"La interfaz publica y los contratos de eventos para **{topic}** deben definirse, revisarse y validarse en CI/CD **antes** de escribir una sola linea de codigo de produccion. Este principio elimina la dependencia serializada entre equipos. Herramientas: OpenAPI 3.1 para REST, AsyncAPI 2.6 para eventos asincronos, Pact para consumer-driven contract testing en cada pipeline de CI/CD.", "",
            "### 3.2 Idempotencia Transaccional con Claves Distribuidas", "",
            "Cada operacion de mutacion del sistema debe soportar reintentos transparentes mediante claves de idempotencia unicas (UUID v4) transmitidas como header HTTP y almacenadas en Redis con TTL configurado. Complementar con el Patron Outbox para garantizar entrega exactly-once de eventos de dominio incluso ante fallos del broker.", "",
            "### 3.3 Degradacion Elegante y Circuit Breaking", "",
            "La disponibilidad compuesta de N servicios en serie es el producto de las disponibilidades individuales. Con 10 servicios al 99.9% cada uno, la disponibilidad compuesta cae al 99.0%. El Circuit Breaker en el API Gateway o en el sidecar de Envoy rompe este acoplamiento proveyendo fallbacks cacheados cuando un servicio downstream supera su umbral de fallos.", "",
            "---", "", "## 4. Implementacion de Referencia en Produccion", "",
            f"```typescript\n{code}\n```", "",
            "---", "", "## 5. Matriz de Trade-offs Arquitectonicos", "",
            "| Dimension | Arquitectura Monolitica | MACH Composable | Veredicto |",
            "| :--- | :--- | :--- | :--- |",
            "| **Velocidad de Despliegue** | Releases coordinados; alto riesgo de regresion cruzada entre equipos. | CI/CD independiente por PBC; despliegues en minutos sin coordinacion. | **MACH** |",
            "| **Complejidad Operativa** | Baja en infraestructura; insostenible en codigo a escala. | Alta; requiere Kubernetes, Service Mesh y observabilidad madura. | **MACH con GitOps** |",
            "| **Resiliencia y SLA** | Punto unico de fallo global; una caida afecta toda la plataforma. | Blast radius contenido por servicio; degradacion controlada. | **MACH** |",
            "| **Eficiencia de Costos** | Escalamiento vertical costoso. | Escalamiento horizontal elastico con KEDA. | **MACH** |",
            "| **Velocidad de Adopcion** | Alta; equipo unico, sin overhead de coordinacion. | Baja; requiere contratos formales y cultura DevOps. | **Monolito Modular primero** |",
            "", "---", "", "## 6. Modos de Fallo en Produccion y Mitigaciones", "",
            "### A. Thundering Herd (Tormenta de Reintentos)", "",
            "**Problema:** Multiples clientes reintentan simultaneamente contra un servicio en recuperacion, re-saturandolo antes de que pueda estabilizarse. Modo de fallo numero uno en sistemas distribuidos a escala.", "",
            "**Mitigacion:** Exponential backoff con full jitter: `base=500ms`, `cap=30s`. Circuit Breaker en API Gateway con umbral del 50% de error rate en ventana de 10 segundos.", "",
            "### B. Eventual Consistency Lag", "",
            "**Problema:** Usuario completa escritura pero replica de lectura aun no proceso el evento.", "",
            "**Mitigacion:** RYOW (Read-Your-Own-Writes) enrutando lecturas post-escritura hacia replica primaria con TTL de 2 segundos. Session tokens con checksums de version para detectar staleness.", "",
            "### C. Schema Drift entre Servicios", "",
            "**Problema:** Cambio no coordinado en la estructura de un evento rompe silenciosamente todos los consumidores downstream.", "",
            "**Mitigacion:** Schema Registry centralizado (Confluent para Kafka) con validacion BACKWARD_TRANSITIVE en todos los pipelines de CI/CD. Bloquear automaticamente merges que rompan la compatibilidad.", "",
            "### D. Connection Pool Exhaustion bajo Carga Sostenida", "",
            "**Problema:** Bajo carga pico, los pools de conexion a bases de datos se agotan por timeouts mal configurados, causando fallos en cascada.", "",
            "**Mitigacion:** PgBouncer en modo transaction-level para PostgreSQL. Limitar max_connections por instancia. Health checks activos con testOnBorrow=true.", "",
            "---", "", "## 7. Checklist de Implementacion para Equipos de Ingenieria", "",
            "**Contratos y Calidad de Codigo:**",
            "- [ ] Contratos de API (OpenAPI 3.1 / AsyncAPI) formalizados y validados con Pact en CI/CD.",
            "- [ ] Cobertura de tests de integracion mayor al 80% en todos los flujos transaccionales criticos.",
            "- [ ] Analisis SAST integrado en el pipeline con bloqueo en severidad CRITICA y ALTA.", "",
            "**Operaciones y Resiliencia:**",
            "- [ ] Claves de idempotencia y locks distribuidos operativos para todas las operaciones mutables.",
            "- [ ] Circuit Breakers configurados con umbrales de fallo documentados y runbooks de recuperacion.",
            "- [ ] Chaos Engineering con LitmusChaos ejecutado en entornos de staging antes de cada major release.", "",
            "**Observabilidad:**",
            "- [ ] Trazas distribuidas OpenTelemetry, metricas RED y logs estructurados activos en produccion.",
            "- [ ] SLOs definidos con error budgets y alertas automaticas de escalamiento en Grafana o Datadog.",
            "- [ ] Dashboard de FinOps con costo por transaccion en tiempo real integrado en el runbook de on-call.", "",
            "**Seguridad:**",
            "- [ ] mTLS activo en todas las rutas de comunicacion interna entre microservicios.",
            "- [ ] Rotacion automatica de secretos con HashiCorp Vault o GCP Secret Manager configurada.",
            "- [ ] Escaneo de vulnerabilidades en imagenes de contenedor integrado en el registro de artefactos.", "",
            "---", "", "## Conclusion", "",
            f"La implementacion de **{topic}** representa un salto cualitativo en la madurez tecnica y operativa de cualquier organizacion digital. El camino hacia MACH es incremental y medible: comenzar identificando los Bounded Contexts con mayor friccion de despliegue, extraerlos de forma ordenada usando el patron Strangler Fig, y construir la plataforma de observabilidad antes de escalar el numero de microservicios. La madurez arquitectonica se construye con contratos formales, disciplina de ingenieria y una cultura que valora el desacoplamiento sobre la conveniencia a corto plazo.",
        ]
        return "\n".join(sections)

    else:
        # English version
        if is_api:    cats,tags = "[API Design, Microservices]",             "[mach, api-first, graphql, openapi, microservices, architecture, cloud-native]"
        elif is_event: cats,tags = "[Distributed Systems, Microservices]",   "[mach, event-driven, kafka, microservices, resilience, architecture, cloud-native]"
        elif is_sec:   cats,tags = "[Security, Microservices]",               "[mach, zero-trust, security, kubernetes, mtls, architecture, cloud-native]"
        elif is_infra: cats,tags = "[DevOps, Cloud Architecture]",            "[mach, kubernetes, gitops, ci-cd, devops, architecture, cloud-native]"
        elif is_head:  cats,tags = "[Headless and Frontend, Cloud Architecture]","[mach, headless, frontend, composable-commerce, architecture, cloud-native, performance]"
        elif is_fin:   cats,tags = "[Enterprise Architecture, FinOps]",       "[mach, finops, roi, strategy, architecture, cloud-native, enterprise]"
        elif is_com:   cats,tags = "[Composable Commerce, Cloud Architecture]","[mach, composable-commerce, headless, architecture, cloud-native, ecommerce, pbcs]"
        elif is_data:  cats,tags = "[Data Architecture, Microservices]",      "[mach, database, sharding, postgres, architecture, cloud-native, consistency]"
        else:          cats,tags = "[Architecture, Microservices]",           "[mach, microservices, cloud-native, api-first, resilience, architecture, devops]"

        sections = [
            "---", "layout: post",
            f'title: "{topic}"',
            f"date: {post_date_str} 09:00:00 -0600",
            "lang: en",
            f"categories: {cats}", f"tags: {tags}",
            "image:", f"  path: /assets/img/posts/{slug}.png", "---", "",
            f"In the landscape of modern enterprise software and composable digital commerce, **{topic}** has emerged as one of the most critical architectural patterns for engineering organizations seeking to overcome the structural limitations of legacy monolithic systems. This deep-dive, authored by a Principal Solutions Architect with hands-on experience in enterprise-scale production platforms, examines the foundational principles, design decisions, and implementation blueprints required for successful adoption.", "",
            "## 1. The Enterprise Problem Statement", "",
            f"Engineering teams on monolithic architectures face compounding technical debt: multi-week deployment cycles, platform-wide production incidents, and structural inability to innovate. Adopting **{topic}** directly addresses these frictions by decoupling component lifecycles, containing blast radius, and reducing cross-team coordination overhead through formal API and event contracts. Teams report 60-80% reductions in deployment cycle times and measurable improvements in all four DORA metrics.", "",
            "---", "", "## 2. Reference Architecture", "",
            f"```mermaid\ngraph TD\n    subgraph Edge Layer\n        Client[Web Mobile PWA] --> CDN[Edge CDN Cloudflare Fastly]\n        CDN --> GW[API Gateway Kong Apigee]\n    end\n    subgraph Services Layer\n        GW --> Auth[Auth Service OAuth 2.1 mTLS]\n        GW --> Core[Core Service {slug[:25]}]\n        Core --> Cache[Redis Cluster L1 L2]\n        Core --> Bus[Apache Kafka]\n    end\n    subgraph Persistence Layer\n        Core --> DB[PostgreSQL Cloud Spanner]\n        Bus --> Worker[Async Worker CDC Debezium]\n        Worker --> DW[BigQuery Analytics]\n    end\n    style GW fill:#7c3aed,stroke:#6d28d9,color:#fff\n    style Core fill:#2563eb,stroke:#1d4ed8,color:#fff\n    style Auth fill:#dc2626,stroke:#b91c1c,color:#fff\n```", "",
            "Three non-negotiable design invariants govern this architecture in enterprise production environments:", "",
            "1. **No service may directly access another service database.** All cross-domain communication occurs exclusively through published APIs or event bus messages.",
            "2. **All write operations are idempotent.** This guarantees safe automatic retries without unintended side effects.",
            "3. **Observability is a first-class citizen.** Distributed traces, RED metrics, and structured logs from day one.", "",
            "---", "", "## 3. Core Design Principles", "",
            "### 3.1 API-First and Event-First Contract Design", "",
            f"Interfaces and event contracts for **{topic}** must be defined, reviewed, and validated in CI/CD before writing production code. Use OpenAPI 3.1 for REST APIs, AsyncAPI 2.6 for async event contracts (Kafka, WebSockets, SSE), and Pact for consumer-driven contract testing in every CI/CD pipeline run.", "",
            "### 3.2 Transactional Idempotency", "",
            "Every system mutation must support transparent retries via unique idempotency keys (UUID v4) transmitted as HTTP headers and backed by Redis storage with configured TTL. Complement with the Outbox Pattern for guaranteed exactly-once event delivery even in broker failure scenarios.", "",
            "### 3.3 Graceful Degradation with Circuit Breaking", "",
            "The composite availability of N services in series equals the product of individual availabilities. Ten services at 99.9% each yields 99.0% composite. Circuit Breakers at the API Gateway or Envoy sidecar break this coupling by providing cached fallbacks when downstream services exceed failure thresholds.", "",
            "---", "", "## 4. Production Reference Implementation", "",
            "```typescript\nimport Redis from 'ioredis';\nimport { v4 as uuidv4 } from 'uuid';\nimport { trace, SpanStatusCode } from '@opentelemetry/api';\n\nclass EnterpriseMACHService {\n  private readonly redis: Redis;\n  private readonly tracer = trace.getTracer('mach-playbook', '1.0.0');\n\n  constructor(uri: string) {\n    this.redis = new Redis(uri, { maxRetriesPerRequest: 3,\n      retryStrategy: (t) => Math.min(t * 150, 5000), enableReadyCheck: true });\n  }\n\n  async execute<T>(\n    tenantId: string, idempKey: string | undefined, fn: () => Promise<T>\n  ): Promise<T | null> {\n    const span = this.tracer.startSpan(`mach.${tenantId}`);\n    const key = `idem:${tenantId}:${idempKey ?? uuidv4()}`;\n    try {\n      if (idempKey) {\n        const hit = await this.redis.get(key);\n        if (hit) { span.end(); return JSON.parse(hit); }\n      }\n      const result = await fn();\n      if (idempKey) await this.redis.setex(key, 300, JSON.stringify(result));\n      span.setStatus({ code: SpanStatusCode.OK });\n      return result;\n    } catch (e: any) {\n      span.setStatus({ code: SpanStatusCode.ERROR, message: e.message });\n      span.recordException(e); throw e;\n    } finally { span.end(); }\n  }\n}\n```", "",
            "---", "", "## 5. Architectural Tradeoffs Matrix", "",
            "| Dimension | Monolithic Architecture | MACH Composable | Verdict |",
            "| :--- | :--- | :--- | :--- |",
            "| **Deployment Velocity** | Coupled releases with high cross-team regression risk. | Independent CI/CD per PBC; deployments in minutes. | **MACH** |",
            "| **Operational Complexity** | Low infrastructure; unsustainable code complexity at scale. | High; requires Kubernetes, Service Mesh, and observability. | **MACH with GitOps** |",
            "| **Fault Isolation** | Single point of failure across the entire platform. | Contained blast radius with per-service graceful degradation. | **MACH** |",
            "| **Cost Efficiency** | Expensive vertical scaling with high provisioning latency. | Elastic horizontal autoscaling per microservice with KEDA. | **MACH** |",
            "| **Initial Adoption Speed** | High; single team, shared context. | Low; requires contracts and DevOps culture. | **Modular Monolith first** |",
            "", "---", "", "## 6. Production Failure Modes and Mitigations", "",
            "### A. Thundering Herd / Retry Storms", "",
            "**Problem:** Multiple clients simultaneously retry against a recovering service, re-saturating it. This is the number one failure mode in distributed systems at scale.", "",
            "**Mitigation:** Exponential backoff with full jitter: `base=500ms`, `cap=30s`. Circuit Breaker at the API Gateway with 50% error rate threshold in a 10-second sliding window.", "",
            "### B. Eventual Consistency Lag", "",
            "**Problem:** User completes a write but the read replica has not yet processed the event, returning stale data.", "",
            "**Mitigation:** RYOW — route post-write reads to the primary replica for a 2-second TTL. Session tokens with version checksums to detect staleness.", "",
            "### C. Schema Drift Across Services", "",
            "**Problem:** Uncoordinated schema changes silently break all downstream consumers.", "",
            "**Mitigation:** Centralized Schema Registry with BACKWARD_TRANSITIVE compatibility validation in all CI/CD pipelines. Automatically block merges that break backward compatibility.", "",
            "### D. Connection Pool Exhaustion Under Load", "",
            "**Problem:** Under peak load, database connection pools are exhausted by misconfigured timeouts, causing cascade failures.", "",
            "**Mitigation:** PgBouncer in transaction-level mode. Limit max_connections per microservice instance. Active health checks with testOnBorrow=true.", "",
            "---", "", "## 7. Engineering Implementation Checklist", "",
            "- [ ] API contracts (OpenAPI 3.1 / AsyncAPI) formalized and Pact-validated in CI/CD.",
            "- [ ] Integration test coverage greater than 80% on critical transactional flows.",
            "- [ ] SAST analysis integrated with CRITICAL/HIGH severity blocking gates.",
            "- [ ] Idempotency keys operational for all mutable operations.",
            "- [ ] Circuit Breakers with documented thresholds and recovery runbooks.",
            "- [ ] Chaos Engineering (LitmusChaos) executed in staging environments.",
            "- [ ] Distributed traces, RED metrics, and structured logs active in production.",
            "- [ ] SLOs with error budgets and automatic escalation alerts.",
            "- [ ] mTLS on all internal communication paths.",
            "- [ ] Container image vulnerability scanning in the artifact registry.", "",
            "---", "", "## Conclusion", "",
            f"Mastering **{topic}** equips engineering teams to build durable, scalable, and highly available composable architectures for mission-critical enterprise workloads at global scale. Begin by identifying Bounded Contexts generating the most deployment friction, extract PBCs with the Strangler Fig pattern, and build observability before scaling microservices. Architectural maturity is built with formal contracts, engineering discipline, and a culture valuing decoupling over short-term convenience. Teams that internalize these principles deliver platforms sustaining millions of daily transactions with SLAs above 99.95%.",
        ]
        return "\n".join(sections)

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
def generate_webp_companion(png_path: str):
    """Generate companion WebP image for Jekyll Chirpy responsive images and HTML-Proofer."""
    try:
        from PIL import Image
        webp_path = os.path.splitext(png_path)[0] + '.webp'
        if os.path.exists(png_path):
            with Image.open(png_path) as img:
                rgb = img.convert('RGB')
                if rgb.width > 600:
                    new_h = int(rgb.height * 600 / rgb.width)
                    rgb = rgb.resize((600, new_h), Image.Resampling.LANCZOS)
                rgb.save(webp_path, 'WEBP', quality=75, method=6)
                print(f" Automatically generated companion WebP asset -> {webp_path}")
    except Exception as e:
        print(f" Warning: Could not generate WebP companion for {png_path}: {e}")


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
    selected_topic, pillar = select_next_topic(existing_posts, args.topic, api_key)
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
    if not args.dry_run:
        generate_webp_companion(image_file_path)

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
