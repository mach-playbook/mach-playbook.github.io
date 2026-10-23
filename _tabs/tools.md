---
title: Tools
icon: fas fa-calculator
order: 5
mermaid: false
---

<style>
/* ==========================================================================
   MACH Playbook - Tools & Calculators Custom Styles
   WCAG AAA High Contrast & Theme-Aware (Dark & Light Mode)
   ========================================================================== */

#mach-calculator-app,
#tco-simulator-app {
  background-color: var(--card-bg, #1e1e22) !important;
  border: 1px solid var(--card-border-color, #2d2d34) !important;
  border-radius: 12px !important;
  color: var(--text-color, #cbd5e1) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
}

/* App Header Titles */
.tools-app-title {
  color: #f8fafc !important;
  font-weight: 700 !important;
}
[data-bs-theme="light"] .tools-app-title,
[data-mode="light"] .tools-app-title {
  color: #0f172a !important;
}

/* Dimension Cards */
.tool-dimension-card {
  background-color: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid #334155 !important;
  border-radius: 10px !important;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}
.tool-dimension-card:hover {
  border-color: #3b82f6 !important;
  background-color: rgba(255, 255, 255, 0.045) !important;
}
[data-bs-theme="light"] .tool-dimension-card,
[data-mode="light"] .tool-dimension-card {
  background-color: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}
[data-bs-theme="light"] .tool-dimension-card:hover,
[data-mode="light"] .tool-dimension-card:hover {
  border-color: #3b82f6 !important;
  background-color: #f1f5f9 !important;
}

/* Question Titles */
.dimension-title {
  color: #f8fafc !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  margin-bottom: 0.35rem !important;
}
[data-bs-theme="light"] .dimension-title,
[data-mode="light"] .dimension-title {
  color: #0f172a !important;
}

/* Question Subtitles / Context */
.dimension-subtitle {
  color: #94a3b8 !important;
  font-size: 0.88rem !important;
  margin-bottom: 0.75rem !important;
  display: block !important;
}
[data-bs-theme="light"] .dimension-subtitle,
[data-mode="light"] .dimension-subtitle {
  color: #475569 !important;
}

/* Form check option rows */
.dimension-option-item {
  display: flex !important;
  align-items: flex-start !important;
  padding: 0.5rem 0.65rem !important;
  margin-bottom: 0.35rem !important;
  border-radius: 6px !important;
  border: 1px solid transparent !important;
  transition: background-color 0.15s ease, border-color 0.15s ease;
  cursor: pointer !important;
}
.dimension-option-item:hover {
  background-color: rgba(59, 130, 246, 0.1) !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
}
[data-bs-theme="light"] .dimension-option-item:hover,
[data-mode="light"] .dimension-option-item:hover {
  background-color: #eff6ff !important;
  border-color: #bfdbfe !important;
}

.dimension-option-item input[type="radio"] {
  margin-top: 0.2rem !important;
  margin-right: 0.75rem !important;
  flex-shrink: 0 !important;
  accent-color: #3b82f6 !important;
  cursor: pointer !important;
  width: 1.15rem !important;
  height: 1.15rem !important;
}

.dimension-option-label {
  color: #f1f5f9 !important;
  font-size: 0.9rem !important;
  line-height: 1.45 !important;
  cursor: pointer !important;
  margin-bottom: 0 !important;
  user-select: none;
  font-weight: 400 !important;
}
[data-bs-theme="light"] .dimension-option-label,
[data-mode="light"] .dimension-option-label {
  color: #1e293b !important;
}

/* Dynamic Results Panel */
.tool-results-panel {
  background-color: #16161a !important;
  border: 1px solid #3b82f6 !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
}
[data-bs-theme="light"] .tool-results-panel,
[data-mode="light"] .tool-results-panel {
  background-color: #f8fafc !important;
  border: 1px solid #3b82f6 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
}

.results-panel-title {
  color: #f8fafc !important;
  font-weight: 700 !important;
}
[data-bs-theme="light"] .results-panel-title,
[data-mode="light"] .results-panel-title {
  color: #0f172a !important;
}

.results-description {
  color: #cbd5e1 !important;
  font-size: 0.92rem !important;
}
[data-bs-theme="light"] .results-description,
[data-mode="light"] .results-description {
  color: #334155 !important;
}

/* Pillar Score Cards */
.pillar-score-card {
  background-color: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid #334155 !important;
  border-radius: 8px !important;
  padding: 0.65rem 0.5rem !important;
  text-align: center !important;
}
[data-bs-theme="light"] .pillar-score-card,
[data-mode="light"] .pillar-score-card {
  background-color: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
}

.pillar-score-label {
  color: #94a3b8 !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  display: block !important;
  margin-bottom: 0.25rem !important;
}
[data-bs-theme="light"] .pillar-score-label,
[data-mode="light"] .pillar-score-label {
  color: #475569 !important;
}

.pillar-score-value {
  color: #38bdf8 !important;
  font-size: 1.25rem !important;
  font-weight: 800 !important;
}
[data-bs-theme="light"] .pillar-score-value,
[data-mode="light"] .pillar-score-value {
  color: #0284c7 !important;
}

/* Recommendation Box */
.recommendation-heading {
  color: #f8fafc !important;
  font-size: 0.95rem !important;
  font-weight: 700 !important;
}
[data-bs-theme="light"] .recommendation-heading,
[data-mode="light"] .recommendation-heading {
  color: #0f172a !important;
}

.recommendation-content {
  color: #e2e8f0 !important;
  font-size: 0.92rem !important;
  line-height: 1.55 !important;
}
[data-bs-theme="light"] .recommendation-content,
[data-mode="light"] .recommendation-content {
  color: #334155 !important;
}

/* TCO Simulator Table */
.tco-table {
  color: #e2e8f0 !important;
  border-color: #334155 !important;
  margin-bottom: 0 !important;
}
.tco-table th,
.tco-table td {
  border-color: #334155 !important;
  vertical-align: middle !important;
}
.tco-table thead th {
  background-color: rgba(255, 255, 255, 0.06) !important;
  color: #f8fafc !important;
  font-weight: 700 !important;
  border-bottom: 2px solid #475569 !important;
}
[data-bs-theme="light"] .tco-table,
[data-mode="light"] .tco-table {
  color: #1e293b !important;
  border-color: #cbd5e1 !important;
}
[data-bs-theme="light"] .tco-table th,
[data-bs-theme="light"] .tco-table td,
[data-mode="light"] .tco-table th,
[data-mode="light"] .tco-table td {
  border-color: #cbd5e1 !important;
}
[data-bs-theme="light"] .tco-table thead th,
[data-mode="light"] .tco-table thead th {
  background-color: #f1f5f9 !important;
  color: #0f172a !important;
  border-bottom: 2px solid #cbd5e1 !important;
}

/* TCO Verdict Box */
.tco-verdict-box {
  background-color: rgba(59, 130, 246, 0.1) !important;
  border-left: 4px solid #3b82f6 !important;
  border-radius: 8px !important;
  color: #f1f5f9 !important;
}
.tco-verdict-label {
  color: #60a5fa !important;
  font-weight: 700 !important;
}
.tco-verdict-text {
  color: #e2e8f0 !important;
}
[data-bs-theme="light"] .tco-verdict-box,
[data-mode="light"] .tco-verdict-box {
  background-color: #eff6ff !important;
  border-left: 4px solid #2563eb !important;
  color: #1e293b !important;
}
[data-bs-theme="light"] .tco-verdict-label,
[data-mode="light"] .tco-verdict-label {
  color: #1d4ed8 !important;
}
[data-bs-theme="light"] .tco-verdict-text,
[data-mode="light"] .tco-verdict-text {
  color: #334155 !important;
}

/* Sliders labels */
.slider-header-label {
  color: #f8fafc !important;
}
[data-bs-theme="light"] .slider-header-label,
[data-mode="light"] .slider-header-label {
  color: #0f172a !important;
}
.slider-markers-text {
  color: #94a3b8 !important;
  font-size: 0.75rem !important;
}
[data-bs-theme="light"] .slider-markers-text,
[data-mode="light"] .slider-markers-text {
  color: #64748b !important;
}
</style>

<div class="lang-block lang-es" markdown="1">

# Herramientas Interactivas y Calculadoras de Arquitectura MACH

Bienvenido al centro de herramientas interactivas de **MACH Playbook**. Diseñadas para arquitectos de software, tech leads y directores de ingeniería, estas herramientas cuantitativas te permiten diagnosticar el estado arquitectónico de tu organización, calcular costos operativos proyectados y tomar decisiones fundamentadas en datos.

---

## 1. Evaluador Interactivo de Madurez Arquitectónica MACH

Evalúa la madurez técnica de tu plataforma en las 4 dimensiones cardinales de **MACH (Microservices, API-First, Cloud-Native, Headless)** junto con Observabilidad y CI/CD. Selecciona la opción que mejor refleje la realidad operativa de tu organización.

</div>

<div class="lang-block lang-en d-none" markdown="1">

# Interactive Tools & MACH Architecture Calculators

Welcome to the **MACH Playbook** interactive engineering workspace. Built for software architects, engineering managers, and technical leads, these quantitative tools allow you to evaluate your team's architectural maturity, project infrastructure latency, and estimate operational total cost of ownership (TCO).

---

## 1. MACH Architectural Maturity Assessment

Evaluate your platform's operational status across the 4 core pillars of **MACH (Microservices, API-First, Cloud-Native, Headless)**, along with Observability and CI/CD automation. Select the option that best reflects your team's operational reality.

</div>

<div class="card p-4 my-4 shadow-sm border" id="mach-calculator-app">
  <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
    <h3 class="h4 mb-0 tools-app-title">
      <i class="fas fa-chart-line text-primary me-2"></i>
      <span data-i18n-es="Diagnóstico de Madurez MACH" data-i18n-en="MACH Maturity Assessment">Diagnóstico de Madurez MACH</span>
    </h3>
    <span class="badge bg-primary fs-6 px-3 py-2" id="score-badge">0 / 100 Pts</span>
  </div>

  <div class="progress mb-4" style="height: 12px; background-color: rgba(255, 255, 255, 0.1);">
    <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" id="score-progress" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
  </div>

  <form id="maturity-form">
    <!-- Dimensión 1: Microservicios -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-cubes text-primary me-2"></i>
        <span data-i18n-es="1. Desacoplamiento de Microservicios & Bases de Datos" data-i18n-en="1. Microservices Decoupling & Databases">1. Desacoplamiento de Microservicios & Bases de Datos</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo gestionan los servicios sus almacenes de persistencia y límites de dominio?" data-i18n-en="How do services manage persistence stores and domain boundaries?">¿Cómo gestionan los servicios sus almacenes de persistencia y límites de dominio?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q1_0" data-i18n-es="Base de datos compartida única para toda la aplicación (Monolito clásico)." data-i18n-en="Single shared database for the entire application (Classic Monolith).">Base de datos compartida única para toda la aplicación (Monolito clásico).</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_1" value="5">
        <label class="form-check-label dimension-option-label" for="q1_1" data-i18n-es="Esquemas lógicos separados dentro del mismo motor relacional común." data-i18n-en="Separate logical schemas within the same shared relational engine.">Esquemas lógicos separados dentro del mismo motor relacional común.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_2" value="10">
        <label class="form-check-label dimension-option-label" for="q1_2" data-i18n-es="Servicios independientes con bases de datos aisladas (&quot;Database-per-Service&quot;) y transacciones distribuidas eventuales." data-i18n-en="Independent services with isolated databases (&quot;Database-per-Service&quot;) and eventual distributed transactions.">Servicios independientes con bases de datos aisladas ("Database-per-Service") y transacciones distribuidas eventuales.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_3" value="15">
        <label class="form-check-label dimension-option-label" for="q1_3" data-i18n-es="Persistencia políglota autónoma por Bounded Context, consistencia vía Event Sourcing o Sagas orquestadas (Temporal/Kafka)." data-i18n-en="Autonomous polyglot persistence per Bounded Context, consistency via Event Sourcing or orchestrated Sagas (Temporal/Kafka).">Persistencia políglota autónoma por Bounded Context, consistencia vía Event Sourcing o Sagas orquestadas (Temporal/Kafka).</label>
      </div>
    </div>

    <!-- Dimensión 2: API-First -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-network-wired text-primary me-2"></i>
        <span data-i18n-es="2. Gobernanza de Contratos y API-First" data-i18n-en="2. Contract Governance & API-First">2. Gobernanza de Contratos y API-First</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo se diseñan, versionan y publican las interfaces de comunicación?" data-i18n-en="How are communication interfaces designed, versioned, and published?">¿Cómo se diseñan, versionan y publican las interfaces de comunicación?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q2_0" data-i18n-es="Endpoints creados sobre la marcha sin contratos formales ni especificación centralizada." data-i18n-en="Ad-hoc endpoints created on the fly without formal contracts or centralized specifications.">Endpoints creados sobre la marcha sin contratos formales ni especificación centralizada.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_1" value="5">
        <label class="form-check-label dimension-option-label" for="q2_1" data-i18n-es="Documentación generada a posteriori con Swagger/OpenAPI, sin validación en pipeline." data-i18n-en="Documentation generated post-facto with Swagger/OpenAPI, without CI/CD pipeline validation.">Documentación generada a posteriori con Swagger/OpenAPI, sin validación en pipeline.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_2" value="10">
        <label class="form-check-label dimension-option-label" for="q2_2" data-i18n-es="Diseño de contratos OpenAPI v3.1 o schemas GraphQL previo a la implementación (Design-First) con API Gateway central." data-i18n-en="OpenAPI v3.1 design or GraphQL schemas created prior to implementation (Design-First) with central API Gateway.">Diseño de contratos OpenAPI v3.1 o schemas GraphQL previo a la implementación (Design-First) con API Gateway central.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_3" value="15">
        <label class="form-check-label dimension-option-label" for="q2_3" data-i18n-es="Contratos estrictos gobernados en CI/CD con pruebas de contrato automatizadas (Pact), detección de breaking changes y API Gateway federado." data-i18n-en="Strict contracts governed in CI/CD with automated consumer-driven contract testing (Pact), breaking change detection, and federated API Gateway.">Contratos estrictos gobernados en CI/CD con pruebas de contrato automatizadas (Pact), detección de breaking changes y API Gateway federado.</label>
      </div>
    </div>

    <!-- Dimensión 3: Cloud-Native -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-cloud text-primary me-2"></i>
        <span data-i18n-es="3. Infraestructura Cloud-Native y Despliegues" data-i18n-en="3. Cloud-Native Infrastructure & Deployments">3. Infraestructura Cloud-Native y Despliegues</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo se orquesta el ciclo de vida de ejecución y escalabilidad en la nube?" data-i18n-en="How is execution lifecycle and cloud elasticity orchestrated?">¿Cómo se orquesta el ciclo de vida de ejecución y escalabilidad en la nube?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q3_0" data-i18n-es="Máquinas virtuales estáticas o servidores dedicados con despliegues manuales por SSH/FTP." data-i18n-en="Static virtual machines or bare-metal servers with manual deployments via SSH/FTP.">Máquinas virtuales estáticas o servidores dedicados con despliegues manuales por SSH/FTP.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_1" value="5">
        <label class="form-check-label dimension-option-label" for="q3_1" data-i18n-es="Contenedores Docker básicos desplegados con scripts CI/CD simples y reinicio con ventana de mantenimiento." data-i18n-en="Basic Docker containers deployed via simple CI/CD scripts with maintenance window downtime restarts.">Contenedores Docker básicos desplegados con scripts CI/CD simples y reinicio con ventana de mantenimiento.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_2" value="10">
        <label class="form-check-label dimension-option-label" for="q3_2" data-i18n-es="Orquestación en Kubernetes o Serverless gestionado (Cloud Run / ECS) con autoescalado elástico y zero-downtime." data-i18n-en="Kubernetes orchestration or managed Serverless (Cloud Run / ECS) with elastic autoscaling and zero-downtime.">Orquestación en Kubernetes o Serverless gestionado (Cloud Run / ECS) con autoescalado elástico y zero-downtime.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_3" value="15">
        <label class="form-check-label dimension-option-label" for="q3_3" data-i18n-es="Infraestructura como Código (IaC) inmutable (Terraform), Service Mesh mTLS (Istio/Linkerd), GitOps (ArgoCD) y despliegues Canary/Blue-Green automatizados." data-i18n-en="Immutable Infrastructure as Code (Terraform), Service Mesh mTLS (Istio/Linkerd), GitOps (ArgoCD), and automated Canary/Blue-Green rollouts.">Infraestructura como Código (IaC) inmutable (Terraform), Service Mesh mTLS (Istio/Linkerd), GitOps (ArgoCD) y despliegues Canary/Blue-Green automatizados.</label>
      </div>
    </div>

    <!-- Dimensión 4: Headless -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-desktop text-primary me-2"></i>
        <span data-i18n-es="4. Frontend Desacoplado y Arquitectura Headless" data-i18n-en="4. Decoupled Frontend & Headless Architecture">4. Frontend Desacoplado y Arquitectura Headless</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo interactúa la capa de presentación con el backend y la lógica de negocio?" data-i18n-en="How does the presentation layer interface with backend business logic?">¿Cómo interactúa la capa de presentación con el backend y la lógica de negocio?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q4_0" data-i18n-es="Vistas acopladas al servidor (PHP/JSP/Blade/Django Monolithic Templates) sin API intermediaria." data-i18n-en="Server-coupled templates (PHP/JSP/Blade/Django Monolithic Templates) without intermediate APIs.">Vistas acopladas al servidor (PHP/JSP/Blade/Django Monolithic Templates) sin API intermediaria.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_1" value="5">
        <label class="form-check-label dimension-option-label" for="q4_1" data-i18n-es="SPA aislada que consume APIs REST de un CMS tradicional (Decoupled Headless parcial)." data-i18n-en="Isolated Single Page Application consuming REST APIs from a traditional CMS (Partial Decoupled Headless).">SPA aislada que consume APIs REST de un CMS tradicional (Decoupled Headless parcial).</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_2" value="10">
        <label class="form-check-label dimension-option-label" for="q4_2" data-i18n-es="Frontend Next.js/Nuxt moderno desacoplado que consume servicios Headless especializados (Contentful, commercetools, Algolia) vía capa BFF." data-i18n-en="Modern decoupled Next.js/Nuxt frontend consuming specialized Headless services (Contentful, commercetools, Algolia) via BFF layer.">Frontend Next.js/Nuxt moderno desacoplado que consume servicios Headless especializados (Contentful, commercetools, Algolia) vía capa BFF.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_3" value="15">
        <label class="form-check-label dimension-option-label" for="q4_3" data-i18n-es="Arquitectura Composable multi-canal en el Edge (Cloudflare Workers / Vercel Edge), hidratación parcial, ISR y federación de micro-frontends." data-i18n-en="Multi-channel Composable Architecture at the Edge (Cloudflare Workers / Vercel Edge), partial hydration, ISR, and micro-frontend federation.">Arquitectura Composable multi-canal en el Edge (Cloudflare Workers / Vercel Edge), hidratación parcial, ISR y federación de micro-frontends.</label>
      </div>
    </div>

    <!-- Dimensión 5: Observabilidad -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-eye text-primary me-2"></i>
        <span data-i18n-es="5. Observabilidad Distribuida y Resiliencia SRE" data-i18n-en="5. Distributed Observability & SRE Resilience">5. Observabilidad Distribuida y Resiliencia SRE</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo supervisas y previenes fallos en cascada en entornos distribuidos?" data-i18n-en="How do you monitor and prevent cascading failures in distributed topologies?">¿Cómo supervisas y previenes fallos en cascada en entornos distribuidos?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q5_0" data-i18n-es="Logs locales en disco (/var/log) y monitoreo reactivo ante caídas reportadas por usuarios." data-i18n-en="Local disk logs (/var/log) and reactive incident triage based on customer bug reports.">Logs locales en disco (/var/log) y monitoreo reactivo ante caídas reportadas por usuarios.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_1" value="5">
        <label class="form-check-label dimension-option-label" for="q5_1" data-i18n-es="Agregación centralizada de logs (Elasticsearch / CloudWatch) con alertas de umbral de CPU/Memoria." data-i18n-en="Centralized log aggregation (Elasticsearch / CloudWatch) with static CPU/Memory threshold alarms.">Agregación centralizada de logs (Elasticsearch / CloudWatch) con alertas de umbral de CPU/Memoria.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_2" value="10">
        <label class="form-check-label dimension-option-label" for="q5_2" data-i18n-es="Trazabilidad distribuida unificada (OpenTelemetry), métricas de las 4 Golden Signals y Circuit Breakers activos." data-i18n-en="Unified distributed tracing (OpenTelemetry), Four Golden Signals monitoring, and active Circuit Breakers.">Trazabilidad distribuida unificada (OpenTelemetry), métricas de las 4 Golden Signals y Circuit Breakers activos.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_3" value="15">
        <label class="form-check-label dimension-option-label" for="q5_3" data-i18n-es="Observabilidad correlacionada (Traces + Metrics + Logs), SLOs/SLAs contractuales automatizados y mitigación adaptativa de incidentes en tiempo real." data-i18n-en="Fully correlated observability (Traces + Metrics + Logs), automated contractual SLOs/SLAs, and real-time self-healing mitigation.">Observabilidad correlacionada (Traces + Metrics + Logs), SLOs/SLAs contractuales automatizados y mitigación adaptativa de incidentes en tiempo real.</label>
      </div>
    </div>

    <!-- Dimensión 6: Event-Driven & Integración Asíncrona -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-bolt text-primary me-2"></i>
        <span data-i18n-es="6. Arquitectura Orientada a Eventos (EDA)" data-i18n-en="6. Event-Driven Architecture (EDA)">6. Arquitectura Orientada a Eventos (EDA)</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Cómo se comunican los módulos para operaciones no bloqueantes?" data-i18n-en="How do modules communicate for non-blocking asynchronous workflows?">¿Cómo se comunican los módulos para operaciones no bloqueantes?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q6_0" data-i18n-es="100% llamadas síncronas HTTP REST bloqueantes en cadena con alta latencia acumulada." data-i18n-en="100% synchronous chained HTTP REST blocking requests with accumulated tail latency.">100% llamadas síncronas HTTP REST bloqueantes en cadena con alta latencia acumulada.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_1" value="5">
        <label class="form-check-label dimension-option-label" for="q6_1" data-i18n-es="Colas de trabajo simples (Redis / RabbitMQ) para tareas en segundo plano." data-i18n-en="Simple point-to-point worker queues (Redis / RabbitMQ) for isolated background tasks.">Colas de trabajo simples (Redis / RabbitMQ) para tareas en segundo plano.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_2" value="10">
        <label class="form-check-label dimension-option-label" for="q6_2" data-i18n-es="Bus de eventos empresarial (Kafka / EventBridge) con especificación formal AsyncAPI y publicación pub/sub." data-i18n-en="Enterprise event bus (Kafka / EventBridge) with formal AsyncAPI contracts and pub/sub topology.">Bus de eventos empresarial (Kafka / EventBridge) con especificación formal AsyncAPI y publicación pub/sub.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_3" value="15">
        <label class="form-check-label dimension-option-label" for="q6_3" data-i18n-es="Event Streaming distribuido con Transactional Outbox Pattern (Debezium), control de idempotencia y CQRS." data-i18n-en="Distributed Event Streaming with Transactional Outbox Pattern (Debezium), idempotency guarantees, and CQRS.">Event Streaming distribuido con Transactional Outbox Pattern (Debezium), control de idempotencia y CQRS.</label>
      </div>
    </div>

    <!-- Dimensión 7: DevOps y Automatización de Pruebas -->
    <div class="mb-4 p-3 rounded tool-dimension-card">
      <h5 class="dimension-title">
        <i class="fas fa-tasks text-primary me-2"></i>
        <span data-i18n-es="7. CI/CD y Autonomía de Equipos" data-i18n-en="7. CI/CD & Team Delivery Autonomy">7. CI/CD y Autonomía de Equipos</span>
      </h5>
      <p class="dimension-subtitle" data-i18n-es="¿Con qué velocidad y autonomía puede un equipo desplegar una nueva funcionalidad a producción?" data-i18n-en="How rapidly and autonomously can engineering deploy new capabilities to production?">¿Con qué velocidad y autonomía puede un equipo desplegar una nueva funcionalidad a producción?</p>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_0" value="0" checked>
        <label class="form-check-label dimension-option-label" for="q7_0" data-i18n-es="Despliegues mensuales o trimestrales coordinados entre múltiples áreas con pruebas manuales extensivas." data-i18n-en="Monthly or quarterly coordinated releases across departments with extensive manual regression tests.">Despliegues mensuales o trimestrales coordinados entre múltiples áreas con pruebas manuales extensivas.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_1" value="4">
        <label class="form-check-label dimension-option-label" for="q7_1" data-i18n-es="Pipelines CI/CD semanales con tests unitarios automatizados, pero aprobación manual en cada etapa." data-i18n-en="Weekly CI/CD pipelines with automated unit tests, but manual gate approvals for promotion.">Pipelines CI/CD semanales con tests unitarios automatizados, pero aprobación manual en cada etapa.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_2" value="7">
        <label class="form-check-label dimension-option-label" for="q7_2" data-i18n-es="Despliegues diarios por servicio mediante pipelines automatizados con pruebas de regresión y cobertura &gt;80%." data-i18n-en="Daily deployments per service via automated pipelines with regression tests and coverage &gt;80%.">Despliegues diarios por servicio mediante pipelines automatizados con pruebas de regresión y cobertura &gt;80%.</label>
      </div>
      <div class="form-check dimension-option-item">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_3" value="10">
        <label class="form-check-label dimension-option-label" for="q7_3" data-i18n-es="Continuous Deployment continuo (múltiples veces al día) con Feature Flags (LaunchDarkly/PostHog), rollback automático y cero coordinación inter-equipos." data-i18n-en="Continuous Deployment (multiple times per day) with Feature Flags (LaunchDarkly/PostHog), automated rollback, and zero cross-team coordination.">Continuous Deployment continuo (múltiples veces al día) con Feature Flags (LaunchDarkly/PostHog), rollback automático y cero coordinación inter-equipos.</label>
      </div>
    </div>
  </form>

  <!-- Panel de Resultados Dinámicos -->
  <div class="mt-4 p-4 rounded tool-results-panel" id="calculator-results">
    <h4 class="h5 results-panel-title mb-3" id="result-title">
      <i class="fas fa-stethoscope text-primary me-2"></i>
      <span data-i18n-es="Diagnóstico de Arquitectura" data-i18n-en="Architecture Diagnosis">Diagnóstico de Arquitectura</span>
    </h4>
    <div class="alert alert-info py-2 px-3 small" id="result-badge-container">
      <strong data-i18n-es="Nivel de Madurez:" data-i18n-en="Maturity Level:">Nivel de Madurez:</strong>
      <span id="result-level-text">Calculando...</span>
    </div>
    <p class="small results-description" id="result-description" data-i18n-es="Selecciona las opciones anteriores para ver el análisis de tu arquitectura." data-i18n-en="Select the options above to view the real-time architectural audit.">Selecciona las opciones anteriores para ver el análisis de tu arquitectura.</p>

    <div class="row g-3 my-2 text-center">
      <div class="col-6 col-md-3">
        <div class="pillar-score-card">
          <span class="pillar-score-label" data-i18n-es="Microservicios" data-i18n-en="Microservices">Microservicios</span>
          <strong class="pillar-score-value" id="pillar-m-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="pillar-score-card">
          <span class="pillar-score-label" data-i18n-es="API-First" data-i18n-en="API-First">API-First</span>
          <strong class="pillar-score-value" id="pillar-a-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="pillar-score-card">
          <span class="pillar-score-label" data-i18n-es="Cloud-Native" data-i18n-en="Cloud-Native">Cloud-Native</span>
          <strong class="pillar-score-value" id="pillar-c-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="pillar-score-card">
          <span class="pillar-score-label" data-i18n-es="Headless" data-i18n-en="Headless">Headless</span>
          <strong class="pillar-score-value" id="pillar-h-score">0 / 15</strong>
        </div>
      </div>
    </div>

    <div class="mt-3">
      <h6 class="recommendation-heading mb-2">
        <i class="fas fa-lightbulb text-warning me-1"></i>
        <span data-i18n-es="Recomendación Arquitectónica Prioritaria:" data-i18n-en="Priority Architectural Recommendation:">Recomendación Arquitectónica Prioritaria:</span>
      </h6>
      <p class="recommendation-content mb-2" id="result-recommendation" data-i18n-es="Completa el formulario para obtener una recomendación precisa." data-i18n-en="Complete the questions to generate a precise recommendation.">Completa el formulario para obtener una recomendación precisa.</p>
    </div>

    <div class="mt-3 text-end">
      <button type="button" class="btn btn-sm btn-outline-primary" id="copy-report-btn">
        <i class="far fa-copy me-1"></i>
        <span data-i18n-es="Copiar Informe al Portapapeles" data-i18n-en="Copy Report to Clipboard">Copiar Informe al Portapapeles</span>
      </button>
      <span class="small text-success ms-2 d-none" id="copy-success-msg" data-i18n-es="¡Copiado!" data-i18n-en="Copied!">¡Copiado!</span>
    </div>
  </div>
</div>

---

<div class="lang-block lang-es" markdown="1">

## 2. Simulador Interactivo de TCO y Latencia (Monolito vs Microservicios vs Serverless)

Ajusta los parámetros operativos de tu organización para visualizar las proyecciones cuantitativas de latencia media P99 y costo mensual de infraestructura según el paradigma arquitectónico seleccionado.

</div>

<div class="lang-block lang-en d-none" markdown="1">

## 2. Infrastructure TCO & P99 Latency Simulator (Monolith vs MACH vs Serverless)

Tune peak requests per second (RPS), domain count, and monthly release cadence to visualize side-by-side trade-offs between Traditional Monolith, Enterprise MACH, and Event-Driven Serverless architectures.

</div>

<div class="card p-4 my-4 shadow-sm border" id="tco-simulator-app">
  <div class="row g-4">
    <!-- Controles -->
    <div class="col-12 col-md-5 border-end">
      <h4 class="h5 fw-bold mb-3 tools-app-title">
        <i class="fas fa-sliders-h text-primary me-2"></i>
        <span data-i18n-es="Parámetros de Operación" data-i18n-en="Operating Parameters">Parámetros de Operación</span>
      </h4>

      <div class="mb-3">
        <label for="rps-slider" class="form-label small fw-bold d-flex justify-content-between slider-header-label">
          <span data-i18n-es="Peticiones por Segundo (RPS):" data-i18n-en="Requests per Second (RPS):">Peticiones por Segundo (RPS):</span>
          <span class="text-primary fw-bold" id="rps-val">2,500 RPS</span>
        </label>
        <input type="range" class="form-range" id="rps-slider" min="100" max="25000" step="100" value="2500">
        <div class="d-flex justify-content-between slider-markers-text">
          <span>100</span>
          <span>10,000</span>
          <span>25,000+</span>
        </div>
      </div>

      <div class="mb-3">
        <label for="services-slider" class="form-label small fw-bold d-flex justify-content-between slider-header-label">
          <span data-i18n-es="Número de Dominios / Servicios:" data-i18n-en="Domains / Services Count:">Número de Dominios / Servicios:</span>
          <span class="text-primary fw-bold" id="services-val">8 Servicios</span>
        </label>
        <input type="range" class="form-range" id="services-slider" min="1" max="40" step="1" value="8">
        <div class="d-flex justify-content-between slider-markers-text">
          <span data-i18n-es="1 (Monolito)" data-i18n-en="1 (Monolith)">1 (Monolito)</span>
          <span>20</span>
          <span data-i18n-es="40 (Mesh)" data-i18n-en="40 (Mesh)">40 (Mesh)</span>
        </div>
      </div>

      <div class="mb-3">
        <label for="releases-slider" class="form-label small fw-bold d-flex justify-content-between slider-header-label">
          <span data-i18n-es="Despliegues Mensuales:" data-i18n-en="Monthly Deployments:">Despliegues Mensuales:</span>
          <span class="text-primary fw-bold" id="releases-val">12 Despliegues</span>
        </label>
        <input type="range" class="form-range" id="releases-slider" min="1" max="100" step="1" value="12">
        <div class="d-flex justify-content-between slider-markers-text">
          <span data-i18n-es="1 (Mensual)" data-i18n-en="1 (Monthly)">1 (Mensual)</span>
          <span data-i18n-es="30 (Diario)" data-i18n-en="30 (Daily)">30 (Diario)</span>
          <span data-i18n-es="100+ (Continuo)" data-i18n-en="100+ (Continuous)">100+ (Continuo)</span>
        </div>
      </div>
    </div>

    <!-- Comparativa Proyectada -->
    <div class="col-12 col-md-7">
      <h4 class="h5 fw-bold mb-3 tools-app-title">
        <i class="fas fa-balance-scale text-primary me-2"></i>
        <span data-i18n-es="Comparativa de Paradigmas Proyectados" data-i18n-en="Projected Paradigms Comparison">Comparativa de Paradigmas Proyectados</span>
      </h4>

      <div class="table-responsive">
        <table class="table table-bordered table-sm align-middle small text-center tco-table">
          <thead class="tco-table-head">
            <tr>
              <th class="text-start" data-i18n-es="Métrica" data-i18n-en="Metric">Métrica</th>
              <th data-i18n-es="Monolito Clásico" data-i18n-en="Classic Monolith">Monolito Clásico</th>
              <th data-i18n-es="MACH Microservicios" data-i18n-en="MACH Microservices">MACH Microservicios</th>
              <th data-i18n-es="Serverless Headless" data-i18n-en="Serverless Headless">Serverless Headless</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-start fw-bold" data-i18n-es="Latencia P99" data-i18n-en="P99 Latency">Latencia P99</td>
              <td id="lat-monolith">180 ms</td>
              <td id="lat-mach" class="text-success fw-bold">45 ms</td>
              <td id="lat-serverless">120 ms</td>
            </tr>
            <tr>
              <td class="text-start fw-bold" data-i18n-es="Costo Cloud Est. / Mes" data-i18n-en="Est. Cloud Cost / Mo">Costo Cloud Est. / Mes</td>
              <td id="cost-monolith">$1,250 USD</td>
              <td id="cost-mach">$850 USD</td>
              <td id="cost-serverless" class="text-primary fw-bold">$420 USD</td>
            </tr>
            <tr>
              <td class="text-start fw-bold" data-i18n-es="Riesgo de Regresión en Deploy" data-i18n-en="Deploy Regression Risk">Riesgo de Regresión en Deploy</td>
              <td class="text-danger" data-i18n-es="Alto (Blast radius global)" data-i18n-en="High (Global blast radius)">Alto (Blast radius global)</td>
              <td class="text-success" data-i18n-es="Mínimo (Canary por servicio)" data-i18n-en="Minimal (Canary per service)">Mínimo (Canary por servicio)</td>
              <td class="text-success" data-i18n-es="Bajo (Funciones aisladas)" data-i18n-en="Low (Isolated functions)">Bajo (Funciones aisladas)</td>
            </tr>
            <tr>
              <td class="text-start fw-bold" data-i18n-es="Overhead de Observabilidad" data-i18n-en="Observability Overhead">Overhead de Observabilidad</td>
              <td data-i18n-es="Bajo (Monolítico)" data-i18n-en="Low (Monolithic)">Bajo (Monolítico)</td>
              <td class="text-warning" data-i18n-es="Moderado (OpenTelemetry / Mesh)" data-i18n-en="Moderate (OpenTelemetry / Mesh)">Moderado (OpenTelemetry / Mesh)</td>
              <td data-i18n-es="Bajo (Cloud Managed)" data-i18n-en="Low (Cloud Managed)">Bajo (Cloud Managed)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="tco-verdict-box p-3 mt-3 mb-0 small" id="tco-verdict">
        <strong class="tco-verdict-label" data-i18n-es="Veredicto de Ingeniería:" data-i18n-en="Engineering Verdict:">Veredicto de Ingeniería:</strong>
        <span class="tco-verdict-text ms-1" id="verdict-text">Calculando...</span>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  // 1. LÓGICA DE LA CALCULADORA DE MADUREZ MACH
  const maturityForm = document.getElementById("maturity-form");
  const scoreBadge = document.getElementById("score-badge");
  const scoreProgress = document.getElementById("score-progress");
  const resultLevelText = document.getElementById("result-level-text");
  const resultDescription = document.getElementById("result-description");
  const resultRecommendation = document.getElementById("result-recommendation");
  const copyBtn = document.getElementById("copy-report-btn");
  const copySuccessMsg = document.getElementById("copy-success-msg");

  const pM = document.getElementById("pillar-m-score");
  const pA = document.getElementById("pillar-a-score");
  const pC = document.getElementById("pillar-c-score");
  const pH = document.getElementById("pillar-h-score");

  function isEnglish() {
    return localStorage.getItem('mach_playbook_lang') === 'en';
  }

  function calculateMaturity() {
    if (!maturityForm) return;
    let totalScore = 0;
    const radios = maturityForm.querySelectorAll(".maturity-radio:checked");
    radios.forEach(r => totalScore += parseInt(r.value, 10));

    const q1 = parseInt((maturityForm.querySelector("input[name='q1']:checked") || {}).value || 0, 10);
    const q2 = parseInt((maturityForm.querySelector("input[name='q2']:checked") || {}).value || 0, 10);
    const q3 = parseInt((maturityForm.querySelector("input[name='q3']:checked") || {}).value || 0, 10);
    const q4 = parseInt((maturityForm.querySelector("input[name='q4']:checked") || {}).value || 0, 10);

    if (pM) pM.textContent = q1 + " / 15";
    if (pA) pA.textContent = q2 + " / 15";
    if (pC) pC.textContent = q3 + " / 15";
    if (pH) pH.textContent = q4 + " / 15";

    if (scoreBadge) scoreBadge.textContent = totalScore + " / 100 Pts";
    if (scoreProgress) {
      scoreProgress.style.width = totalScore + "%";
      if (totalScore < 30) {
        scoreProgress.className = "progress-bar bg-danger progress-bar-striped";
      } else if (totalScore < 60) {
        scoreProgress.className = "progress-bar bg-warning progress-bar-striped";
      } else {
        scoreProgress.className = "progress-bar bg-success progress-bar-striped";
      }
    }

    const en = isEnglish();
    let level = "";
    let desc = "";
    let rec = "";

    if (totalScore <= 25) {
      level = en
        ? "Tier 1 — Highly Coupled Legacy Monolith"
        : "Nivel 1 — Monolito Legado Altamente Acoplado (Legacy)";
      desc = en
        ? "Your platform relies on shared persistence and high-risk coordinated releases. Engineering velocity is constrained by the blast radius of each release."
        : "Tu plataforma depende de bases de datos compartidas y despliegues coordinados de alto riesgo. La velocidad de iteración está limitada por el radio de explosión (blast radius) de cada release.";
      rec = en
        ? "Apply the Strangler Fig pattern: establish an edge API Gateway and extract read-heavy capabilities into satellite schemas before decoupling core transaction domains."
        : "Aplica el patrón Strangler Fig: crea un API Gateway perimetral e inicia extrayendo servicios de lectura hacia esquemas satélite antes de desacoplar transacciones críticas.";
    } else if (totalScore <= 50) {
      level = en
        ? "Tier 2 — Modular Monolith & Initial Service Decoupling"
        : "Nivel 2 — Monolito Modularizado y Desacoplamiento Inicial";
      desc = en
        ? "You have begun transitioning toward formal contracts and containers, but persistence bottlenecks or blocking synchronous RPCs persist between services."
        : "Has iniciado la transición hacia contratos formales y contenedores, pero aún existen cuellos de botella en la persistencia o sincronización síncrona bloqueante entre servicios.";
      rec = en
        ? "Implement OpenAPI v3.1 contract governance with strict CI/CD gate validation, and migrate point-to-point service calls to asynchronous queues with Apache Kafka or RabbitMQ."
        : "Implementa gobernanza de contratos OpenAPI v3.1 con validación estricta en CI/CD y migra la sincronización entre servicios hacia colas asíncronas con Apache Kafka o RabbitMQ.";
    } else if (totalScore <= 75) {
      level = en
        ? "Tier 3 — Pragmatic MACH & Composable Hybrid"
        : "Nivel 3 — Composable Híbrido & MACH Pragmático";
      desc = en
        ? "Solid architectural foundations: decoupled presentation layer, containerized orchestrations, and structured APIs. Ready for advanced resilience and Edge computing optimizations."
        : "Tu arquitectura cuenta con bases sólidas: frontend desacoplado, contenedores orquestados y APIs estructuradas. Estás preparado para optimizaciones avanzadas de resiliencia y Edge computing.";
      rec = en
        ? "Adopt unified OpenTelemetry distributed tracing across 100% of services, roll out mTLS Zero Trust service mesh policies (Istio/SPIFFE), and add automated canary rollouts."
        : "Adopta observabilidad unificada OpenTelemetry en el 100% de los servicios, implementa políticas mTLS Zero Trust (Istio/SPIFFE) y añade despliegues Canary automatizados.";
    } else {
      level = en
        ? "Tier 4 — Cloud-Native Enterprise MACH Leader"
        : "Nivel 4 — MACH Enterprise Nativo de Alto Rendimiento";
      desc = en
        ? "Cutting-edge distributed architecture: fully autonomous components, consumer-driven automated contract tests, end-to-end observability, and frictionless continuous delivery."
        : "Arquitectura de vanguardia: componentes completamente autónomos, contratos respaldados por pruebas automáticas, observabilidad integral y despliegues continuos con cero fricción.";
      rec = en
        ? "Focus on continuous cloud cost engineering (FinOps), evaluate WebAssembly / Edge Workers for micro-frontends, and govern autonomous AI agent interactions via MCP."
        : "Enfócate en la optimización continua de costos Cloud (FinOps), evaluación de WebAssembly / Edge Workers para micro-frontends y gobernanza de agentes de IA autónomos con MCP.";
    }

    if (resultLevelText) resultLevelText.textContent = level;
    if (resultDescription) resultDescription.textContent = desc;
    if (resultRecommendation) resultRecommendation.textContent = rec;
  }

  maturityForm.addEventListener("change", calculateMaturity);
  calculateMaturity();

  // Escuchar cambios de idioma para recalcular textos dinámicos
  window.addEventListener("storage", function (e) {
    if (e.key === 'mach_playbook_lang') calculateMaturity();
  });
  document.querySelectorAll('[data-lang]').forEach(btn => {
    btn.addEventListener('click', () => setTimeout(calculateMaturity, 50));
  });

  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      const radios = maturityForm.querySelectorAll(".maturity-radio:checked");
      let totalScore = 0;
      radios.forEach(r => totalScore += parseInt(r.value, 10));
      const en = isEnglish();
      const textToCopy = en
        ? "=== MACH PLAYBOOK ARCHITECTURE AUDIT REPORT ===\n" +
          "Audit Score: " + totalScore + " / 100 Pts\n" +
          "Maturity Level: " + (resultLevelText ? resultLevelText.textContent : "") + "\n" +
          "Diagnosis: " + (resultDescription ? resultDescription.textContent : "") + "\n" +
          "Priority Recommendation: " + (resultRecommendation ? resultRecommendation.textContent : "") + "\n" +
          "Audited at: https://mach-playbook.github.io/tools/\n"
        : "=== MACH PLAYBOOK ARCHITECTURE AUDIT REPORT ===\n" +
          "Puntaje Obtenido: " + totalScore + " / 100 Pts\n" +
          "Nivel: " + (resultLevelText ? resultLevelText.textContent : "") + "\n" +
          "Diagnóstico: " + (resultDescription ? resultDescription.textContent : "") + "\n" +
          "Recomendación Prioritaria: " + (resultRecommendation ? resultRecommendation.textContent : "") + "\n" +
          "Auditado en: https://mach-playbook.github.io/tools/\n";

      navigator.clipboard.writeText(textToCopy).then(function () {
        if (copySuccessMsg) {
          copySuccessMsg.classList.remove("d-none");
          setTimeout(() => copySuccessMsg.classList.add("d-none"), 3000);
        }
      });
    });
  }

  // 2. LÓGICA DEL SIMULADOR TCO Y LATENCIA
  const rpsSlider = document.getElementById("rps-slider");
  const rpsVal = document.getElementById("rps-val");
  const servicesSlider = document.getElementById("services-slider");
  const servicesVal = document.getElementById("services-val");
  const releasesSlider = document.getElementById("releases-slider");
  const releasesVal = document.getElementById("releases-val");

  const latMonolith = document.getElementById("lat-monolith");
  const latMach = document.getElementById("lat-mach");
  const latServerless = document.getElementById("lat-serverless");

  const costMonolith = document.getElementById("cost-monolith");
  const costMach = document.getElementById("cost-mach");
  const costServerless = document.getElementById("cost-serverless");
  const verdictText = document.getElementById("verdict-text");

  function updateTCO() {
    if (!rpsSlider || !servicesSlider || !releasesSlider) return;
    const rps = parseInt(rpsSlider.value, 10);
    const services = parseInt(servicesSlider.value, 10);
    const releases = parseInt(releasesSlider.value, 10);
    const en = isEnglish();

    rpsVal.textContent = rps.toLocaleString() + " RPS";
    servicesVal.textContent = services + (en ? " Services" : " Servicios");
    releasesVal.textContent = releases + (en ? " Releases" : " Despliegues");

    // Estimación Latencia P99 (ms)
    const p99Mono = Math.round(70 + (rps * 0.015) + (services * 2));
    const p99Mach = Math.round(25 + (rps * 0.002) + (services * 0.8));
    const p99Serv = Math.round(40 + (services * 3.5) + (rps > 8000 ? 50 : 10));

    latMonolith.textContent = p99Mono + " ms";
    latMach.textContent = p99Mach + " ms";
    latServerless.textContent = p99Serv + " ms" + (en ? " (Cold start)" : " (Cold start)");

    // Estimación Costo Cloud ($ USD / Mes)
    const costMono = Math.round(400 + (rps * 0.28) + (services * 25));
    const costM = Math.round(250 + (rps * 0.16) + (services * 45));
    const costS = Math.round(120 + (rps * 0.22) + (services * 15));

    costMonolith.textContent = "$" + costMono.toLocaleString() + " USD";
    costMach.textContent = "$" + costM.toLocaleString() + " USD";
    costServerless.textContent = "$" + costS.toLocaleString() + " USD";

    // Veredicto
    let verdict = "";
    if (rps < 1000 && services <= 5) {
      verdict = en
        ? "For moderate throughput (< 1,000 RPS) and few domains, a Modular Monolith or Managed Serverless offers the optimal cost-to-benefit ratio without incurring cluster orchestration overhead."
        : "Para un volumen moderado (< 1,000 RPS) y pocos servicios, un Monolito Modularizado o Serverless ofrece la mejor relación costo-efectividad sin incurrir en overhead de orquestación de clústeres.";
    } else if (releases > 25 || rps > 5000) {
      verdict = en
        ? "With high deployment cadence and high traffic velocity, decoupled MACH architecture (Kubernetes / Service Mesh) is critical to minimize blast radius and maintain sub-50ms P99 latency."
        : "Con tu alta tasa de despliegues y volumen de tráfico, la arquitectura MACH desacoplada (Kubernetes / Service Mesh) es indispensable para mitigar el radio de explosión en producción y optimizar latencia P99.";
    } else {
      verdict = en
        ? "Your workload is in the ideal transitional sweet spot: a Composable Hybrid strategy with Edge caching will unlock immediate cost savings before fully breaking down remaining domains."
        : "Tu entorno se encuentra en el umbral óptimo de transición: un enfoque Composable Híbrido con Edge caching te permitirá reducir costos inmediatos antes de migrar la totalidad de dominios.";
    }
    if (verdictText) verdictText.textContent = verdict;
  }

  if (rpsSlider && servicesSlider && releasesSlider) {
    rpsSlider.addEventListener("input", updateTCO);
    servicesSlider.addEventListener("input", updateTCO);
    releasesSlider.addEventListener("input", updateTCO);
    updateTCO();

    window.addEventListener("storage", function (e) {
      if (e.key === 'mach_playbook_lang') updateTCO();
    });
    document.querySelectorAll('[data-lang]').forEach(btn => {
      btn.addEventListener('click', () => setTimeout(updateTCO, 50));
    });
  }
});
</script>
