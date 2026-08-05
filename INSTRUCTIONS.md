Context: We need to push two new Spanish-language technical blog posts to the MACH Playbook to strengthen the site's E-E-A-T profile for AdSense. The first article covers enterprise API integration using Apigee, MuleSoft, and Salesforce Data Cloud. The second article focuses on intelligent E2E test automation using Playwright combined with local machine learning models via Ollama. 

Execute the exact following steps:

1. Create a new file at `_posts/2026-08-05-gestion-apis-apigee-mulesoft-salesforce.md`.
2. Inject the following content into the file exactly as written (including the YAML frontmatter):
---
layout: post
title: "Gestión de APIs Empresariales: Integrando Apigee, MuleSoft y Salesforce Data Cloud"
date: 2026-08-05 09:00:00 -0600
categories: [Arquitectura Cloud, Integración]
tags: [apigee, mulesoft, salesforce, data-cloud, api-gateway, mach, gcp]
---

En arquitecturas empresariales modernas (MACH), la proliferación de microservicios exige una estrategia de integración y exposición de datos altamente disciplinada. A menudo, los equipos confunden el rol de un API Gateway con el de un Bus de Servicio Empresarial (ESB) o plataforma de integración (iPaaS). 

Este artículo detalla un patrón arquitectónico donde Google Cloud Apigee, MuleSoft y Salesforce Data Cloud operan en conjunto, aprovechando las fortalezas específicas de cada plataforma para crear un ecosistema unificado y seguro.

## La Separación de Responsabilidades: Apigee vs. MuleSoft

Para evitar cuellos de botella y arquitecturas monolíticas disfrazadas de microservicios, es crucial delimitar las funciones de la capa de red y la capa de integración.

1.  **Apigee como la Puerta de Enlace Perimetral (Edge Gateway):** 
    Apigee se posiciona en el borde de la red (típicamente en GCP) y actúa como el escudo de seguridad y control de tráfico. Su responsabilidad principal no es transformar datos complejos, sino aplicar políticas:
    *   **Validación de Tokens (OAuth 2.0 / JWT):** Intercepta y valida credenciales antes de que el tráfico toque la red interna.
    *   **Protección contra Amenazas (Spike Arrest / Quotas):** Previene ataques de denegación de servicio (DDoS) limitando la tasa de peticiones por cliente.
    *   **Monetización y Analítica:** Rastrea el uso de las APIs por parte de desarrolladores externos o *partners* para facturación.
2.  **MuleSoft como el Motor de Integración (iPaaS):**
    Detrás del firewall protector de Apigee se encuentra MuleSoft. Aquí es donde ocurre el levantamiento pesado (heavy lifting). MuleSoft conecta sistemas dispares (ERP, bases de datos legadas, servicios SOAP) utilizando su vasta biblioteca de conectores y transforma los formatos de datos (ej. XML a JSON) mediante DataWeave. 
    *   MuleSoft orquesta las llamadas a múltiples microservicios internos y consolida las respuestas en un único *payload* optimizado que luego devuelve a Apigee.

## Ingesta hacia Salesforce Data Cloud

El objetivo final de esta arquitectura suele ser la unificación del perfil del cliente. Salesforce Data Cloud requiere ingestas de datos masivas y precisas en tiempo real para segmentación y marketing automatizado.

*   **Flujo de Datos:** Cuando ocurre un evento transaccional (ej. una compra procesada por un microservicio interno), MuleSoft captura el evento, aplica reglas de normalización de datos (resolución de identidades) y utiliza la API de Ingesta de Salesforce para inyectar el registro en Data Cloud.
*   **Exposición Segura:** Si Salesforce necesita consultar el estado de inventario en tiempo real, realiza una petición saliente que es recibida e inspeccionada por Apigee. Apigee valida la identidad de Salesforce y enruta la petición a MuleSoft, quien finalmente consulta la base de datos de inventario.

## Conclusión

Integrar Apigee para la gestión y seguridad perimetral, MuleSoft para la orquestación profunda y Salesforce Data Cloud como el cerebro de datos del cliente, crea una topología robusta. Esta separación de intereses garantiza que las políticas de seguridad perimetral no entorpezcan la lógica de integración, logrando una arquitectura verdaderamente escalable a nivel global.

3. Create a second file at `_posts/2026-08-05-automatizacion-e2e-playwright-ollama.md`.
4. Inject the following content into the file exactly as written (including the YAML frontmatter):
---
layout: post
title: "Automatización Inteligente: Pruebas E2E con Playwright y Modelos Locales mediante Ollama"
date: 2026-08-05 14:00:00 -0600
categories: [Ingeniería de Software, QA]
tags: [playwright, ollama, ia, machine-learning, e2e-testing, automatizacion, ci-cd]
---

Las pruebas End-to-End (E2E) tradicionales suelen ser frágiles. Pequeños cambios en el DOM o en los selectores CSS pueden romper cientos de *scripts* de prueba, generando falsos positivos y cuellos de botella en los flujos de Integración Continua (CI). 

Para mitigar la "fatiga de mantenimiento" en QA, los ingenieros de software están combinando frameworks de automatización de última generación, como Playwright, con la inferencia de Modelos de Lenguaje Grande (LLMs) ejecutados localmente a través de Ollama.

## Playwright: Estabilidad y Ejecución Cross-Browser

Playwright ha superado a herramientas legacy gracias a su arquitectura fuera de proceso (out-of-process) y su comunicación directa con el navegador mediante el protocolo DevTools.

*   **Auto-espera (Auto-waiting):** A diferencia de *Selenium*, Playwright espera de forma inherente a que los elementos sean interactivos (visibles, habilitados, sin animaciones) antes de realizar una acción (clic, escritura). Esto elimina la necesidad de `Thread.sleep()` artificiales en el código.
*   **Aislamiento de Contextos:** Permite levantar múltiples contextos de navegador anónimos en milisegundos dentro de la misma instancia, ideal para probar flujos multi-usuario simultáneos en tiempo real (ej. aplicaciones de chat o juegos estratégicos sincronizados).

## Inyectando Inteligencia Artificial Local con Ollama

La dependencia estricta de selectores (`xpath`, `css`) es el talón de Aquiles de las pruebas. Al integrar Ollama, podemos correr modelos como `Llama 3` o `Mistral` directamente en el agente de CI (sin costos de API ni problemas de privacidad) para dotar al *script* de razonamiento heurístico.

### Casos de Uso Avanzados

1.  **Validación de Datos No Estructurados:**
    Supongamos que el test debe verificar que un ticket de soporte autogenerado tenga un tono "amable y resolutivo". En lugar de aserciones de cadenas de texto rígidas, Playwright extrae el texto del DOM y lo envía al modelo local en Ollama:
    ```javascript
    // Pseudo-código de Playwright + Ollama
    const ticketText = await page.locator('.ticket-body').innerText();
    const evaluation = await ollama.chat({
      model: 'mistral',
      messages: [{ role: 'user', content: `Evalúa si este texto es amable y resolutivo respondiendo solo YES o NO: "${ticketText}"` }]
    });
    expect(evaluation.message.content).toBe('YES');
    ```
2.  **Auto-reparación (Self-Healing) Básica:**
    Si un selector estricto falla, el *script* de Playwright puede capturar el HTML del componente actual, enviarlo a Ollama y pedirle que identifique el nuevo selector semántico más probable basándose en roles de accesibilidad (ARIA) o texto visible, permitiendo que la prueba continúe y reporte el cambio.

## Conclusión

La sinergia entre el motor de automatización determinista de Playwright y las capacidades heurísticas locales de Ollama está redefiniendo los límites del Quality Assurance. Las pruebas E2E ya no se limitan a verificar que un botón exista; ahora pueden interpretar, razonar y adaptarse a interfaces dinámicas, manteniendo los datos sensibles completamente dentro de la red corporativa.

5. Verify that the filenames strictly follow the Jekyll date-prefix convention (`YYYY-MM-DD-title.md`). Ensure the date matches today: `2026-08-05`.
6. Open a terminal and run the following Git commands sequentially to push the changes:
   - `git add _posts/2026-08-05-gestion-apis-apigee-mulesoft-salesforce.md _posts/2026-08-05-automatizacion-e2e-playwright-ollama.md`
   - `git commit -m "feat: add Apigee/MuleSoft integration and Playwright/Ollama automation articles in Spanish"`
   - `git push origin main`

Monitor the console output, wait for the push to complete, and confirm that the GitHub Pages deployment action has triggered successfully.