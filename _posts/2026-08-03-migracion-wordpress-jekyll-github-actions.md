---
layout: post
title: "De Monolito a Estático: Migrando de WordPress a Arquitecturas SSG con Jekyll y GitHub Actions"
date: 2026-08-03 10:00:00 -0600
lang: es
categories: [Headless & Frontend, Arquitectura Cloud]
tags: [architecture, ci-cd, cloud-native, headless]
image:
  path: /assets/img/posts/2026-08-03-migracion-wordpress-jekyll-github-actions.png
---

Durante la última década, WordPress democratizó la publicación web. Sin embargo, en el contexto de las arquitecturas empresariales modernas (MACH), acoplar estrechamente la base de datos, el motor de renderizado PHP y la capa de presentación introduce vulnerabilidades de seguridad, cuellos de botella en el rendimiento y una pesada carga de mantenimiento.

La modernización hacia un Generador de Sitios Estáticos (SSG) como Jekyll transforma por completo este paradigma. Este artículo detalla la estrategia de migración técnica de un CMS monolítico a un frontend inmutable desplegado mediante integración continua.

## El Problema del Acoplamiento en CMS Tradicionales

Un CMS tradicional requiere ejecutar consultas a la base de datos y procesar plantillas en el servidor por cada petición entrante (salvo que se utilicen capas de caché agresivas). Esto significa que un pico de tráfico inesperado puede saturar los hilos de procesamiento (PHP-FPM) y agotar las conexiones a la base de datos (MySQL), resultando en tiempos de inactividad. 

Además, la exposición constante del panel de administración (wp-admin) y la dependencia de plugins de terceros conforman una superficie de ataque inmensa.

## Transición a Jekyll y el Paradigma Inmutable

Al migrar a Jekyll, el proceso de renderizado se desplaza del momento de la *petición* al momento de la *compilación*. 

1.  **Extracción de Datos:** El primer paso es exportar el contenido existente de WordPress. Utilizando herramientas de scraping o la propia API REST de WordPress, los artículos se convierten de HTML a archivos Markdown puros, extrayendo los metadatos hacia el bloque de *Frontmatter* (YAML).
2.  **Infraestructura como Código (IaC):** Con Jekyll, el sitio web completo se convierte en un repositorio de código fuente. No hay bases de datos de producción que respaldar ni servidores web que parchear. La seguridad se delega completamente a los controles de acceso del repositorio (por ejemplo, GitHub).
3.  **Despliegue Inmutable:** El resultado de la compilación de Jekyll es un directorio de archivos HTML, CSS y JS estáticos. Esta carga útil es inmutable y puede ser servida directamente desde el borde de la red (Edge CDN), garantizando tiempos de respuesta (TTFB) menores a 50 milisegundos a nivel global.

## Automatización con GitHub Actions y GitHub Pages

El verdadero poder de esta arquitectura se desbloquea al integrar pipelines de CI/CD.

En lugar de transferir archivos manualmente por FTP, se configura un flujo de trabajo (Workflow) en GitHub Actions. Cada vez que un ingeniero realiza un `git push` con un nuevo archivo Markdown en el directorio `_posts`, el pipeline se dispara automáticamente:
*   Instala las dependencias de Ruby.
*   Compila el sitio estático de Jekyll.
*   Inyecta scripts de monetización o analíticas de forma dinámica.
*   Despliega los artefactos generados en GitHub Pages de forma atómica.

## Conclusión

Migrar de WordPress a una arquitectura SSG con Jekyll y GitHub Pages no es solo una mejora de rendimiento; es un cambio hacia la excelencia operativa. Elimina los costos de infraestructura de servidores dinámicos, erradica los vectores de ataque a bases de datos y alinea la publicación de contenido con las mejores prácticas de la ingeniería de software moderna.


---

## Análisis Arquitectónico Profundo: Patrones de Diseño Empresarial

Al implementar esta solución en entornos empresariales de misión crítica, los arquitectos de software deben abordar desafíos inherentes a los sistemas distribuidos, tales como la partición de red, la consistencia eventual y la gestión del aislamiento de fallos.

```
┌────────────────────────────────────────────────────────────────────────┐
│              TOPOLOGÍA DE ALTA DISPONIBILIDAD Y RESILIENCIA            │
├────────────────────────────────────────────────────────────────────────┤
│  Tráfico Externo -> [Ingress Perimetral / TLS 1.3]                     │
│                            │                                           │
│                     [API Gateway / Auth]                               │
│                            │                                           │
│             ┌──────────────┴──────────────┐                            │
│             ▼                             ▼                            │
│   [Microservicio Dominio A] <==gRPC==> [Microservicio Dominio B]       │
│          │                                   │                         │
│   (BD Independiente)                  (BD Independiente)               │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Implementación de Código Productivo y Middleware

El siguiente componente de software demuestra cómo estructurar la lógica de negocio con observabilidad integrada, manejo defensivo de excepciones e idempotencia transaccional:

```typescript
import { Request, Response, NextFunction } from 'express';
import { Counter, Histogram } from 'prom-client';

const latenciaPeticionesHttp = new Histogram({
  name: 'http_duracion_peticion_segundos',
  help: 'Duracion de las peticiones HTTP en segundos',
  labelNames: ['metodo', 'ruta', 'codigo_estado'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});

export const middlewareMetricasResiliencia = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const inicio = process.hrtime();
  res.on('finish', () => {
    const [segundos, nanosegundos] = process.hrtime(inicio);
    const duracionSegundos = segundos + nanosegundos / 1e9;
    latenciaPeticionesHttp
      .labels(req.method, req.route?.path || req.path, res.statusCode.toString())
      .observe(duracionSegundos);
  });
  next();
};
```

---

## Modos de Fallo en Producción y Playbook de Mitigación (SRE)

La operación de arquitecturas desacopladas requiere procedimientos de respuesta claros ante incidentes de alta severidad. A continuación se presentan los escenarios de fallo más comunes y las acciones operativas recomendadas:

### Escenario A: Sobrecarga y Degradación por Latencia en Cascada
* **Causa Raíz:** Un microservicio secundario experimenta bloqueos de base de datos, agotando el grupo de conexiones (*connection pool*) del API Gateway perimetral.
* **Comando de Diagnóstico:**
  ```bash
  kubectl logs -n production -l app=microservicio-core --tail=100 | grep -E "TIMEOUT|504|DEADLINE_EXCEEDED"
  ```
* **Protocolo de Mitigación:**
  1. Activar el patrón *Circuit Breaker* en el Gateway para responder con *degraded fallback* inmediato a las peticiones no esenciales.
  2. Escalar horizontalmente el clúster de cómputo mientras se aíslan las consultas lentas en la base de datos.

### Escenario B: Desincronización de Eventos en Particiones de Red
* **Causa Raíz:** Interrupción temporal en la red entre proveedores de nube que impide la entrega oportuna de mensajes en colas asíncronas.
* **Comando de Diagnóstico:**
  ```bash
  curl -s "http://prometheus.internal:9090/api/v1/query?query=pubsub_undelivered_messages"
  ```
* **Protocolo de Mitigación:**
  1. Desviar las transacciones fallidas a una cola de mensajes no procesados (*Dead Letter Queue* o DLQ).
  2. Ejecutar un *script* de conciliación automática una vez restablecida la conectividad de red.

---

## Matriz de Evaluación de Compromisos Arquitectónicos (Trade-Offs)

Toda decisión técnica conlleva un balance entre rendimiento, complejidad operativa, tolerancia a fallos y costos de infraestructura:

| Paradigma Técnico | Perfil de Latencia | Tolerancia a Fallos | Complejidad Operativa | Eficiencia de Costos |
| :--- | :--- | :--- | :--- | :--- |
| **Monolito Síncrono** | Ultra-baja (en memoria) | Baja (Punto Único de Fallo) | Mínima | Alta en etapas tempranas |
| **API Gateway + REST Síncrono** | Moderada (sobrecarga de red) | Media (aislamiento por servicio) | Moderada | Moderada |
| **Malla de Eventos Asíncronos** | Consistencia eventual | Alta (mensajería duradera) | Alta (requiere trazabilidad) | Alta a escala masiva |
| **Caché Distribuida en el Borde** | Cercana a cero para lecturas | Alta (nodos réplica edge) | Moderada | Alto retorno de inversión |

---

## Lista de Verificación para Despliegue en Producción

Antes de autorizar el paso a producción de esta arquitectura, el equipo de ingeniería debe validar los siguientes puntos de control:

* [ ] Pruebas de contrato de APIs (OpenAPI / Schemas) ejecutadas con éxito en el pipeline de CI/CD.
* [ ] Trazabilidad distribuida mediante OpenTelemetry configurada en todos los puntos de entrada y salida.
* [ ] Umbrales de *Rate Limiting* y políticas de reintento exponencial probadas bajo escenarios de estrés.
* [ ] Cuotas de recursos (CPU/RAM) y políticas de autoescalado horizontal (HPA) asignadas correctamente.
* [ ] Procedimiento de despliegue sin tiempo de inactividad (*Canary* o *Blue/Green*) validado.
