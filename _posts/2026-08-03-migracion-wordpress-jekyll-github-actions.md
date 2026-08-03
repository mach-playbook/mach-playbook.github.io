---
layout: post
title: "De Monolito a Estático: Migrando de WordPress a Arquitecturas SSG con Jekyll y GitHub Actions"
date: 2026-08-03 10:00:00 -0600
categories: [Arquitectura Cloud, Desarrollo Web]
tags: [wordpress, jekyll, github actions, ssg, ci-cd, migracion, mach]
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
