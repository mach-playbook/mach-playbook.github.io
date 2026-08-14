---
layout: post
title: "Infraestructura Inmutable y Despliegues Blue/Green en Google Cloud Run"
date: 2026-07-31 15:00:00 -0600
lang: es
categories: [DevOps, Cloud Computing]
tags: [cloud run, ci-cd, blue-green, github actions, gcp, serverless]
image:
  path: /assets/img/posts/2026-07-31-infraestructura-inmutable-despliegues-blue-green-cloud-run.png
---

La promesa de los servicios serverless como Google Cloud Run es la escalabilidad instantánea. Sin embargo, en entornos de producción de misión crítica, desplegar nuevas versiones de una aplicación directamente sobre el tráfico en vivo es una receta para interrupciones del servicio. 

Para alcanzar la madurez en DevOps, los ingenieros deben adoptar el principio de la "Infraestructura Inmutable" combinado con estrategias basadas en liberación de tráfico, como los despliegues Blue/Green o Canary.

## El Principio de la Infraestructura Inmutable

En Cloud Run, cada vez que se despliega una nueva imagen de contenedor, se crea una *Revisión* inmutable. Esta revisión es una instantánea exacta del código y la configuración en ese instante de tiempo.
A diferencia de los servidores tradicionales donde se aplican parches sobre la marcha, si una revisión de Cloud Run presenta errores, no se repara; se descarta, y el tráfico se redirige inmediatamente a la revisión anterior (Rollback).

## Estrategia Blue/Green con Control de Tráfico

La división de tráfico nativa de Cloud Run permite realizar pruebas seguras en producción antes de comprometer al 100% de los usuarios.

1.  **Despliegue de la Versión Green (Nueva):** Mediante un pipeline de CI/CD (por ejemplo, GitHub Actions), la nueva imagen de contenedor se despliega en Cloud Run, pero se configura explícitamente para recibir el **0% del tráfico público**.
2.  **Validación Interna (Smoke Testing):** Se asigna una etiqueta de tráfico (Traffic Tag) a esta nueva revisión. Esto genera una URL interna dedicada (ej. `green---mi-servicio.run.app`) que el equipo de QA o los scripts de automatización pueden atacar para validar que las conexiones a la base de datos (Cloud SQL) y la lógica de negocio funcionen correctamente.
3.  **Conmutación (Cutover):** Una vez validada, el pipeline actualiza la configuración del servicio para enrutar el 100% del tráfico de la revisión Blue (Antigua) a la revisión Green. En Cloud Run, este cambio es atómico y ocurre sin pérdida de peticiones (Zero Downtime).

## El Desafío de las Migraciones de Bases de Datos

El verdadero reto en los despliegues Blue/Green no es el cómputo, sino el estado (State). Si la versión Green requiere un cambio destructivo en el esquema de la base de datos (por ejemplo, renombrar una columna en PostgreSQL), la versión Blue fallará instantáneamente.

Para solucionar esto, los cambios de esquema deben ser siempre retrocompatibles:
*   Fase 1: Añadir la nueva columna (Blue y Green funcionan).
*   Fase 2: Desplegar Green para que escriba en ambas columnas.
*   Fase 3: Backfill de datos antiguos.
*   Fase 4: Desplegar una nueva revisión que solo dependa de la nueva columna, y finalmente, eliminar la antigua.

## Conclusión

Dominar las capacidades de división de tráfico de Cloud Run transforma el despliegue de software de un evento estresante a una rutina aburrida y predecible. Integrar estas prácticas en los pipelines de automatización es el sello distintivo de un equipo de ingeniería de alto rendimiento.


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
