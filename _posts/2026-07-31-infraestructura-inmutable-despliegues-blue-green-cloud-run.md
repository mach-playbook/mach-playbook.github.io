---
layout: post
title: "Infraestructura Inmutable y Despliegues Blue/Green en Google Cloud Run"
date: 2026-07-31 15:00:00 -0600
lang: es
categories: [DevOps, Cloud Computing]
tags: [cloud run, ci-cd, blue-green, github actions, gcp, serverless]
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
