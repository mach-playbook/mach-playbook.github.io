---
layout: post
title: "Observabilidad con OpenTelemetry en MACH: Trazas, Metricas y Logs Unificados"
date: 2026-09-01 09:00:00 -0600
lang: es
categories: [DevOps, Observabilidad]
tags: [opentelemetry, observability, tracing, prometheus, grafana, mach, microservices]
image:
  path: /assets/img/posts/2026-09-01-observability-opentelemetry-mach.png
---

La observabilidad es la capacidad de entender el estado interno de un sistema a partir de sus salidas externas. En una arquitectura MACH con decenas de microservicios distribuidos, la observabilidad no es opcional: es un requisito fundamental de operacion. Sin ella, diagnosticar un problema que afecta la conversion de e-commerce puede llevar horas o dias en lugar de minutos.

**OpenTelemetry** (OTel) es el estandar de observabilidad de codigo abierto que ha unificado el ecosistema: una sola instrumentacion para generar trazas distribuidas, metricas y logs en cualquier lenguaje de programacion, compatible con cualquier backend de observabilidad (Grafana Tempo, Jaeger, Datadog, New Relic, Honeycomb).

## Los Tres Pilares de la Observabilidad en MACH

### Pilar 1: Trazas Distribuidas

Las trazas distribuidas son la herramienta mas poderosa para diagnosticar problemas en sistemas MACH. Cuando una request del usuario pasa por 8 microservicios diferentes, una traza distribuida muestra exactamente cuanto tiempo tomo cada servicio, donde hubo errores, y cuales fueron las dependencias de cada operacion.

OpenTelemetry genera trazas mediante la propagacion de un Trace Context a traves de todos los servicios que participan en una request. Cuando el API Gateway recibe una request, genera un trace_id unico y un span_id. Al llamar al siguiente microservicio, agrega el Trace Context en headers HTTP (traceparent segun el estandar W3C Trace Context). Cada microservicio lee estos headers, crea sus propios spans hijos, y los envia al backend de trazas al finalizar su procesamiento.

La instrumentacion automatica de OpenTelemetry maneja esto transparentemente para los frameworks mas comunes: Express.js, FastAPI, Spring Boot, Gin. Solo se necesita inicializar el SDK de OTel al arrancar el microservicio y la instrumentacion del framework se aplica automaticamente.

### Pilar 2: Metricas con Prometheus

Las metricas cuantifican el comportamiento del sistema a lo largo del tiempo. El estandar de metricas en MACH es Prometheus, que usa un modelo pull (Prometheus scrape periodicamente los endpoints /metrics de cada servicio) con un lenguaje de query poderoso llamado PromQL.

Las metricas mas importantes para microservicios MACH son las metricas RED: Request Rate (requests por segundo), Error Rate (porcentaje de errores), y Duration (latencia en percentiles p50, p90, p99). Estas tres metricas son suficientes para detectar el 90 porciento de los problemas en produccion.

OpenTelemetry permite exportar metricas en formato Prometheus desde cualquier lenguaje usando el SDK de OTel, eliminando la necesidad de librerias de instrumentacion especificas por lenguaje como promclient (Python) o prometheus-client (Java).

### Pilar 3: Logs Estructurados

Los logs en MACH deben ser estructurados (en formato JSON) y contener siempre el trace_id y span_id de la traza activa. Esto permite correlacionar logs con trazas y metricas para diagnosticar problemas complejos.

El campo trace_id en los logs es critico: cuando Grafana muestra una traza con un span que tiene duracion de 5 segundos inesperada, el developer puede hacer click en ese span y ver directamente los logs del microservicio durante ese periodo especifico, filtrados por trace_id. Sin esta correlacion, buscar los logs relevantes en un volumen de millones de registros por minuto seria extremadamente lento.

## Implementacion de OpenTelemetry en un Microservicio MACH

La implementacion de OTel en un microservicio Node.js sigue el patron de inicializacion anticipada (antes de importar cualquier otro modulo de la aplicacion) con auto-instrumentacion de frameworks populares.

El SDK de OTel para Node.js incluye instrumentacion automatica para Express, Fastify, HTTP/HTTPS nativo, gRPC, MongoDB, Redis, PostgreSQL y muchos otros. Una vez inicializado, el SDK intercepta automaticamente estas llamadas y genera spans con la informacion relevante (URL, metodo HTTP, codigo de respuesta, etc.) sin cambios en el codigo de la aplicacion.

Para instrumentacion manual de partes especificas del codigo de negocio, OTel provee una API simple para crear spans personalizados, agregar atributos y registrar eventos:

El tracer es el objeto central para crear spans. Cada span puede tener atributos personalizados (datos de contexto de negocio como el order_id o customer_id) que son invaluables para el debugging porque permiten buscar todas las trazas relacionadas con un pedido especifico.

## El Stack de Observabilidad: Grafana, Tempo, Loki y Prometheus

La combinacion mas comun de herramientas de observabilidad open-source para MACH en 2026 es:

**Grafana**: dashboard y visualizacion unificada de todos los signals de observabilidad. Grafana puede correlacionar metricas, trazas y logs en una sola vista, permitiendo la navegacion fluida entre los tres pilares.

**Prometheus + Thanos**: Prometheus para la recoleccion de metricas a corto plazo (2 semanas), Thanos para la federacion y retencion a largo plazo (1 ano) y la alta disponibilidad del almacenamiento de metricas.

**Grafana Tempo**: backend de trazas distribuidas compatible con OpenTelemetry, Jaeger, Zipkin y otros formatos. Almacena trazas en object storage (GCS, S3) de forma muy economica.

**Grafana Loki**: agregacion y busqueda de logs con el mismo lenguaje de query que Prometheus (LogQL). Indexa solo los metadatos (labels) de los logs, no el contenido completo, lo que lo hace muy eficiente en almacenamiento comparado con Elasticsearch.

Este stack completo puede desplegarse en Kubernetes con el Helm chart de kube-prometheus-stack (para Prometheus y Grafana) mas Tempo y Loki. El costo de operacion es significativamente menor que las soluciones SaaS equivalentes para volumenes altos de datos.

## Correlacion de Signals: El Superpower de OpenTelemetry

El verdadero valor de OpenTelemetry es la correlacion automatica entre los tres pilares. Cuando un microservicio genera un log, la instrumentacion de OTel agrega automaticamente el trace_id y span_id de la traza activa al log. Esto permite en Grafana ir de una metrica anomala (pico de latencia en el Order Service) a una traza especifica que muestra el comportamiento del sistema durante ese pico, y de ahi a los logs detallados de ese span especifico.

Esta correlacion que antes requeria instrumentacion manual en cada microservicio ahora es automatica con OpenTelemetry, democratizando la observabilidad profunda para todos los microservicios de la plataforma.

## SLOs y Error Budgets: Observabilidad Orientada al Negocio

Las metricas y trazas son medios para un fin: garantizar que los SLOs (Service Level Objectives) del negocio se cumplan. Un SLO tipico para una plataforma de e-commerce MACH seria: el 99.5 porciento de las requests de checkout deben completarse con exito en menos de 2 segundos.

El Error Budget es el margen de fallo permitido por el SLO: si el SLO es 99.5 porciento de disponibilidad, el error budget es el 0.5 porciento restante, que equivale a aproximadamente 3.65 horas de downtime permitidas al mes. Monitorear el consumo del error budget permite a los equipos tomar decisiones informadas: si se ha consumido el 80 porciento del error budget en los primeros 15 dias del mes, el equipo debe priorizar la estabilidad sobre nuevas features para el resto del mes.

## Conclusion: OpenTelemetry como Estandar de Facto

OpenTelemetry ha resuelto el problema de fragmentacion de la observabilidad en microservicios: ya no es necesario decidir entre Jaeger o Zipkin para trazas, Prometheus o StatsD para metricas, o diferentes librerias de logging por lenguaje. Una sola instrumentacion, multiple backends.

Para equipos MACH que buscan implementar observabilidad de clase mundial, la combinacion de OpenTelemetry para la instrumentacion con el stack Grafana para la visualizacion ofrece una solucion completa, open-source y sin vendor lock-in, con capacidades equivalentes a las mejores soluciones SaaS del mercado a una fraccion del costo.
