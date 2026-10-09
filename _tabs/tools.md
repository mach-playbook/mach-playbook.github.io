---
title: Tools
icon: fas fa-calculator
order: 5
mermaid: false
---

<div class="lang-block lang-es" markdown="1">

# Herramientas Interactivas y Calculadoras de Arquitectura MACH

Bienvenido al centro de herramientas interactivas de **MACH Playbook**. Diseñadas para arquitectos de software, tech leads y directores de ingeniería, estas herramientas cuantitativas te permiten diagnosticar el estado arquitectónico de tu organización, calcular costos operativos proyectados y tomar decisiones fundamentadas en datos.

---

## 1. Evaluador Interactivo de Madurez Arquitectónica MACH

Evalúa la madurez técnica de tu plataforma en las 4 dimensiones cardinales de **MACH (Microservices, API-First, Cloud-Native, Headless)** junto con Observabilidad y CI/CD. Selecciona la opción que mejor refleje la realidad operativa de tu organización.

<div class="card p-4 my-4 shadow-sm border" id="mach-calculator-app">
  <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
    <h3 class="h4 mb-0"><i class="fas fa-chart-line text-primary me-2"></i> Diagnóstico de Madurez MACH</h3>
    <span class="badge bg-primary fs-6 px-3 py-2" id="score-badge">0 / 100 Pts</span>
  </div>

  <div class="progress mb-4" style="height: 12px;">
    <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" id="score-progress" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
  </div>

  <form id="maturity-form">
    <!-- Dimensión 1: Microservicios -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-cubes text-secondary me-2"></i> 1. Desacoplamiento de Microservicios & Bases de Datos</h5>
      <p class="text-muted small mb-2">¿Cómo gestionan los servicios sus almacenes de persistencia y límites de dominio?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_0" value="0" checked>
        <label class="form-check-label small" for="q1_0">Base de datos compartida única para toda la aplicación (Monolito clásico).</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_1" value="5">
        <label class="form-check-label small" for="q1_1">Esquemas lógicos separados dentro del mismo motor relacional común.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_2" value="10">
        <label class="form-check-label small" for="q1_2">Servicios independientes con bases de datos aisladas ("Database-per-Service") y transacciones distribuidas eventuales.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q1" id="q1_3" value="15">
        <label class="form-check-label small" for="q1_3">Persistencia políglota autónoma por Bounded Context, consistencia vía Event Sourcing o Sagas orquestadas (Temporal/Kafka).</label>
      </div>
    </div>

    <!-- Dimensión 2: API-First -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-network-wired text-secondary me-2"></i> 2. Gobernanza de Contratos y API-First</h5>
      <p class="text-muted small mb-2">¿Cómo se diseñan, versionan y publican las interfaces de comunicación?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_0" value="0" checked>
        <label class="form-check-label small" for="q2_0">Endpoints creados sobre la marcha sin contratos formales ni especificación centralizada.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_1" value="5">
        <label class="form-check-label small" for="q2_1">Documentación generada a posteriori con Swagger/OpenAPI, sin validación en pipeline.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_2" value="10">
        <label class="form-check-label small" for="q2_2">Diseño de contratos OpenAPI v3.1 o schemas GraphQL previo a la implementación (Design-First) con API Gateway central.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q2" id="q2_3" value="15">
        <label class="form-check-label small" for="q2_3">Contratos estrictos gobernados en CI/CD con pruebas de contrato automatizadas (Pact), detección de breaking changes y API Gateway federado.</label>
      </div>
    </div>

    <!-- Dimensión 3: Cloud-Native -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-cloud text-secondary me-2"></i> 3. Infraestructura Cloud-Native y Despliegues</h5>
      <p class="text-muted small mb-2">¿Cómo se orquesta el ciclo de vida de ejecución y escalabilidad en la nube?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_0" value="0" checked>
        <label class="form-check-label small" for="q3_0">Máquinas virtuales estáticas o servidores dedicados con despliegues manuales por SSH/FTP.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_1" value="5">
        <label class="form-check-label small" for="q3_1">Contenedores Docker básicos desplegados con scripts CI/CD simples y reinicio con ventana de mantenimiento.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_2" value="10">
        <label class="form-check-label small" for="q3_2">Orquestación en Kubernetes o Serverless gestionado (Cloud Run / ECS) con autoescalado elástico y zero-downtime.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q3" id="q3_3" value="15">
        <label class="form-check-label small" for="q3_3">Infraestructura como Código (IaC) inmutable (Terraform), Service Mesh mTLS (Istio/Linkerd), GitOps (ArgoCD) y despliegues Canary/Blue-Green automatizados.</label>
      </div>
    </div>

    <!-- Dimensión 4: Headless -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-desktop text-secondary me-2"></i> 4. Frontend Desacoplado y Arquitectura Headless</h5>
      <p class="text-muted small mb-2">¿Cómo interactúa la capa de presentación con el backend y la lógica de negocio?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_0" value="0" checked>
        <label class="form-check-label small" for="q4_0">Vistas acopladas al servidor (PHP/JSP/Blade/Django Monolithic Templates) sin API intermediaria.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_1" value="5">
        <label class="form-check-label small" for="q4_1">SPA aislada que consume APIs REST de un CMS tradicional (Decoupled Headless parcial).</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_2" value="10">
        <label class="form-check-label small" for="q4_2">Frontend Next.js/Nuxt moderno desacoplado que consume servicios Headless especializados (Contentful, commercetools, Algolia) vía capa BFF.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q4" id="q4_3" value="15">
        <label class="form-check-label small" for="q4_3">Arquitectura Composable multi-canal en el Edge (Cloudflare Workers / Vercel Edge), hidratación parcial, ISR y federación de micro-frontends.</label>
      </div>
    </div>

    <!-- Dimensión 5: Observabilidad -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-eye text-secondary me-2"></i> 5. Observabilidad Distribuida y Resiliencia SRE</h5>
      <p class="text-muted small mb-2">¿Cómo supervisas y previenes fallos en cascada en entornos distribuidos?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_0" value="0" checked>
        <label class="form-check-label small" for="q5_0">Logs locales en disco (`/var/log`) y monitoreo reactivo ante caídas reportadas por usuarios.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_1" value="5">
        <label class="form-check-label small" for="q5_1">Agregación centralizada de logs (Elasticsearch / CloudWatch) con alertas de umbral de CPU/Memoria.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_2" value="10">
        <label class="form-check-label small" for="q5_2">Trazabilidad distribuida unificada (OpenTelemetry), métricas de las 4 Golden Signals y Circuit Breakers activos.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q5" id="q5_3" value="15">
        <label class="form-check-label small" for="q5_3">Observabilidad correlacionada (Traces + Metrics + Logs), SLOs/SLAs contractuales automatizados y mitigación adaptativa de incidentes en tiempo real.</label>
      </div>
    </div>

    <!-- Dimensión 6: Event-Driven & Integración Asíncrona -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-bolt text-secondary me-2"></i> 6. Arquitectura Orientada a Eventos (EDA)</h5>
      <p class="text-muted small mb-2">¿Cómo se comunican los módulos para operaciones no bloqueantes?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_0" value="0" checked>
        <label class="form-check-label small" for="q6_0">100% llamadas síncronas HTTP REST bloqueantes en cadena con alta latencia acumulada.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_1" value="5">
        <label class="form-check-label small" for="q6_1">Colas de trabajo simples (Redis / RabbitMQ) para tareas en segundo plano.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_2" value="10">
        <label class="form-check-label small" for="q6_2">Bus de eventos empresarial (Kafka / EventBridge) con especificación formal AsyncAPI y publicación pub/sub.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q6" id="q6_3" value="15">
        <label class="form-check-label small" for="q6_3">Event Streaming distribuido con Transactional Outbox Pattern (Debezium), control de idempotencia y CQRS.</label>
      </div>
    </div>

    <!-- Dimensión 7: DevOps y Automatización de Pruebas -->
    <div class="mb-4 p-3 rounded bg-light border">
      <h5 class="fw-bold text-dark"><i class="fas fa-tasks text-secondary me-2"></i> 7. CI/CD y Autonomía de Equipos</h5>
      <p class="text-muted small mb-2">¿Con qué velocidad y autonomía puede un equipo desplegar una nueva funcionalidad a producción?</p>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_0" value="0" checked>
        <label class="form-check-label small" for="q7_0">Despliegues mensuales o trimestrales coordinados entre múltiples áreas con pruebas manuales extensivas.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_1" value="4">
        <label class="form-check-label small" for="q7_1">Pipelines CI/CD semanales con tests unitarios automatizados, pero aprobación manual en cada etapa.</label>
      </div>
      <div class="form-check mb-1">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_2" value="7">
        <label class="form-check-label small" for="q7_2">Despliegues diarios por servicio mediante pipelines automatizados con pruebas de regresión y cobertura >80%.</label>
      </div>
      <div class="form-check">
        <input class="form-check-input maturity-radio" type="radio" name="q7" id="q7_3" value="10">
        <label class="form-check-label small" for="q7_3">Continuous Deployment continuo (múltiples veces al día) con Feature Flags (LaunchDarkly/PostHog), rollback automático y cero coordinación inter-equipos.</label>
      </div>
    </div>
  </form>

  <!-- Panel de Resultados Dinámicos -->
  <div class="mt-4 p-4 rounded border" id="calculator-results" style="background-color: var(--card-bg, #ffffff);">
    <h4 class="h5 fw-bold mb-3" id="result-title"><i class="fas fa-stethoscope text-primary me-2"></i> Diagnóstico de Arquitectura</h4>
    <div class="alert alert-info py-2 px-3 small" id="result-badge-container">
      <strong>Nivel de Madurez:</strong> <span id="result-level-text">Calculando...</span>
    </div>
    <p class="small text-muted" id="result-description">Selecciona las opciones anteriores para ver el análisis de tu arquitectura.</p>

    <div class="row g-3 my-2 text-center">
      <div class="col-6 col-md-3">
        <div class="p-2 border rounded bg-light">
          <small class="text-muted d-block">Microservicios</small>
          <strong class="fs-6 text-dark" id="pillar-m-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="p-2 border rounded bg-light">
          <small class="text-muted d-block">API-First</small>
          <strong class="fs-6 text-dark" id="pillar-a-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="p-2 border rounded bg-light">
          <small class="text-muted d-block">Cloud-Native</small>
          <strong class="fs-6 text-dark" id="pillar-c-score">0 / 15</strong>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="p-2 border rounded bg-light">
          <small class="text-muted d-block">Headless</small>
          <strong class="fs-6 text-dark" id="pillar-h-score">0 / 15</strong>
        </div>
      </div>
    </div>

    <div class="mt-3">
      <h6 class="fw-bold small text-dark"><i class="fas fa-lightbulb text-warning me-1"></i> Recomendación Arquitectónica Prioritaria:</h6>
      <p class="small mb-2 text-secondary" id="result-recommendation">Completa el formulario para obtener una recomendación precisa.</p>
    </div>

    <div class="mt-3 text-end">
      <button type="button" class="btn btn-sm btn-outline-primary" id="copy-report-btn">
        <i class="far fa-copy me-1"></i> Copiar Informe al Portapapeles
      </button>
      <span class="small text-success ms-2 d-none" id="copy-success-msg">¡Copiado!</span>
    </div>
  </div>
</div>

---

## 2. Simulador Interactivo de TCO y Latencia (Monolito vs Microservicios vs Serverless)

Ajusta los parámetros operativos de tu organización para visualizar las proyecciones cuantitativas de latencia media P99 y costo mensual de infraestructura según el paradigma arquitectónico seleccionado.

<div class="card p-4 my-4 shadow-sm border" id="tco-simulator-app">
  <div class="row g-4">
    <!-- Controles -->
    <div class="col-12 col-md-5 border-end">
      <h4 class="h5 fw-bold mb-3"><i class="fas fa-sliders-h text-primary me-2"></i> Parámetros de Operación</h4>

      <div class="mb-3">
        <label for="rps-slider" class="form-label small fw-bold d-flex justify-content-between">
          <span>Peticiones por Segundo (RPS):</span>
          <span class="text-primary fw-bold" id="rps-val">2,500 RPS</span>
        </label>
        <input type="range" class="form-range" id="rps-slider" min="100" max="25000" step="100" value="2500">
        <div class="d-flex justify-content-between text-muted" style="font-size: 0.75rem;">
          <span>100</span>
          <span>10,000</span>
          <span>25,000+</span>
        </div>
      </div>

      <div class="mb-3">
        <label for="services-slider" class="form-label small fw-bold d-flex justify-content-between">
          <span>Número de Dominios / Servicios:</span>
          <span class="text-primary fw-bold" id="services-val">8 Servicios</span>
        </label>
        <input type="range" class="form-range" id="services-slider" min="1" max="40" step="1" value="8">
        <div class="d-flex justify-content-between text-muted" style="font-size: 0.75rem;">
          <span>1 (Monolito)</span>
          <span>20</span>
          <span>40 (Mesh)</span>
        </div>
      </div>

      <div class="mb-3">
        <label for="releases-slider" class="form-label small fw-bold d-flex justify-content-between">
          <span>Despliegues Mensuales:</span>
          <span class="text-primary fw-bold" id="releases-val">12 Despliegues</span>
        </label>
        <input type="range" class="form-range" id="releases-slider" min="1" max="100" step="1" value="12">
        <div class="d-flex justify-content-between text-muted" style="font-size: 0.75rem;">
          <span>1 (Mensual)</span>
          <span>30 (Diario)</span>
          <span>100+ (Continuo)</span>
        </div>
      </div>
    </div>

    <!-- Comparativa Proyectada -->
    <div class="col-12 col-md-7">
      <h4 class="h5 fw-bold mb-3"><i class="fas fa-balance-scale text-primary me-2"></i> Comparativa de Paradigmas Proyectados</h4>

      <div class="table-responsive">
        <table class="table table-bordered table-sm align-middle small text-center">
          <thead class="table-light">
            <tr>
              <th class="text-start">Métrica</th>
              <th>Monolito Clásico</th>
              <th>MACH Microservicios</th>
              <th>Serverless Headless</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-start fw-bold">Latencia P99</td>
              <td id="lat-monolith">180 ms</td>
              <td id="lat-mach" class="text-success fw-bold">45 ms</td>
              <td id="lat-serverless">120 ms (Cold start)</td>
            </tr>
            <tr>
              <td class="text-start fw-bold">Costo Cloud Est. / Mes</td>
              <td id="cost-monolith">$1,250 USD</td>
              <td id="cost-mach">$850 USD</td>
              <td id="cost-serverless" class="text-primary fw-bold">$420 USD</td>
            </tr>
            <tr>
              <td class="text-start fw-bold">Riesgo de Regresión en Deploy</td>
              <td class="text-danger">Alto (Blast radius global)</td>
              <td class="text-success">Mínimo (Canary por servicio)</td>
              <td class="text-success">Bajo (Funciones aisladas)</td>
            </tr>
            <tr>
              <td class="text-start fw-bold">Overhead de Observabilidad</td>
              <td>Bajo (Monolítico)</td>
              <td class="text-warning">Moderado (OpenTelemetry / Mesh)</td>
              <td>Bajo (Cloud Managed)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="alert alert-secondary p-3 mt-3 mb-0 small" id="tco-verdict">
        <strong>Veredicto de Ingeniería:</strong> <span id="verdict-text">Calculando...</span>
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

  function calculateMaturity() {
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

    let level = "";
    let desc = "";
    let rec = "";

    if (totalScore <= 25) {
      level = "Nivel 1 — Monolito Legado Altamente Acoplado (Legacy)";
      desc = "Tu plataforma depende de bases de datos compartidas y despliegues coordinados de alto riesgo. La velocidad de iteración está limitada por el radio de explosión (blast radius) de cada release.";
      rec = "Aplica el patrón Strangler Fig: crea un API Gateway perimetral e inicia extrayendo servicios de lectura hacia esquemas satélite antes de desacoplar transacciones críticas.";
    } else if (totalScore <= 50) {
      level = "Nivel 2 — Monolito Modularizado y Desacoplamiento Inicial";
      desc = "Has iniciado la transición hacia contratos formales y contenedores, pero aún existen cuellos de botella en la persistencia o sincronización síncrona bloqueante entre servicios.";
      rec = "Implementa gobernanza de contratos OpenAPI v3.1 con validación estricta en CI/CD y migra la sincronización entre servicios hacia colas asíncronas con Apache Kafka o RabbitMQ.";
    } else if (totalScore <= 75) {
      level = "Nivel 3 — Composable Híbrido & MACH Pragmático";
      desc = "Tu arquitectura cuenta con bases sólidas: frontend desacoplado, contenedores orquestados y APIs estructuradas. Estás preparado para optimizaciones avanzadas de resiliencia y Edge computing.";
      rec = "Adopta observabilidad unificada OpenTelemetry en el 100% de los servicios, implementa políticas mTLS Zero Trust (Istio/SPIFFE) y añade despliegues Canary automatizados.";
    } else {
      level = "Nivel 4 — MACH Enterprise Nativo de Alto Rendimiento";
      desc = "Arquitectura de vanguardia: componentes completamente autónomos, contratos respaldados por pruebas automáticas, observabilidad integral y despliegues continuos con cero fricción.";
      rec = "Enfócate en la optimización continua de costos Cloud (FinOps), evaluación de WebAssembly / Edge Workers para micro-frontends y gobernanza de agentes de IA autónomos con MCP.";
    }

    if (resultLevelText) resultLevelText.textContent = level;
    if (resultDescription) resultDescription.textContent = desc;
    if (resultRecommendation) resultRecommendation.textContent = rec;
  }

  maturityForm.addEventListener("change", calculateMaturity);
  calculateMaturity();

  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      const radios = maturityForm.querySelectorAll(".maturity-radio:checked");
      let totalScore = 0;
      radios.forEach(r => totalScore += parseInt(r.value, 10));
      const textToCopy = "=== MACH PLAYBOOK ARCHITECTURE AUDIT REPORT ===\n" +
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
    const rps = parseInt(rpsSlider.value, 10);
    const services = parseInt(servicesSlider.value, 10);
    const releases = parseInt(releasesSlider.value, 10);

    rpsVal.textContent = rps.toLocaleString() + " RPS";
    servicesVal.textContent = services + " Servicios";
    releasesVal.textContent = releases + " Despliegues";

    // Estimación Latencia P99 (ms)
    // Monolito bajo carga alta sufre contención de DB y bloqueo de threads
    const p99Mono = Math.round(70 + (rps * 0.015) + (services * 2));
    // MACH con caching en edge y escalabilidad horizontal mantiene latencia baja
    const p99Mach = Math.round(25 + (rps * 0.002) + (services * 0.8));
    // Serverless cold starts aumentan latencia si hay demasiados micro-servicios
    const p99Serv = Math.round(40 + (services * 3.5) + (rps > 8000 ? 50 : 10));

    latMonolith.textContent = p99Mono + " ms";
    latMach.textContent = p99Mach + " ms";
    latServerless.textContent = p99Serv + " ms";

    // Estimación Costo Cloud ($ USD / Mes)
    // Monolito: instancias gigantes sobredimensionadas para soportar picos
    const costMono = Math.round(400 + (rps * 0.28) + (services * 25));
    // MACH: microservicios escalan elásticamente según demanda de cada dominio
    const costM = Math.round(250 + (rps * 0.16) + (services * 45));
    // Serverless: costo por invocación / gigabyte-segundo
    const costS = Math.round(120 + (rps * 0.22) + (services * 15));

    costMonolith.textContent = "$" + costMono.toLocaleString() + " USD";
    costMach.textContent = "$" + costM.toLocaleString() + " USD";
    costServerless.textContent = "$" + costS.toLocaleString() + " USD";

    // Veredicto
    let verdict = "";
    if (rps < 1000 && services <= 5) {
      verdict = "Para un volumen moderado (< 1,000 RPS) y pocos servicios, un Monolito Modularizado o Serverless ofrece la mejor relación costo-efectividad sin incurrir en overhead de orquestación de clústeres.";
    } else if (releases > 25 || rps > 5000) {
      verdict = "Con tu alta tasa de despliegues y volumen de tráfico, la arquitectura MACH desacoplada (Kubernetes / Service Mesh) es indispensable para mitigar el radio de explosión en producción y optimizar latencia P99.";
    } else {
      verdict = "Tu entorno se encuentra en el umbral óptimo de transición: un enfoque Composable Híbrido con Edge caching te permitirá reducir costos inmediatos antes de migrar la totalidad de dominios.";
    }
    verdictText.textContent = verdict;
  }

  if (rpsSlider && servicesSlider && releasesSlider) {
    rpsSlider.addEventListener("input", updateTCO);
    servicesSlider.addEventListener("input", updateTCO);
    releasesSlider.addEventListener("input", updateTCO);
    updateTCO();
  }
});
</script>

</div>

<div class="lang-block lang-en d-none" markdown="1">

# Interactive Tools & MACH Architecture Calculators

Welcome to the **MACH Playbook** interactive engineering workspace. Built for software architects, engineering managers, and technical leads, these quantitative tools allow you to evaluate your team's architectural maturity, project infrastructure latency, and estimate operational total cost of ownership (TCO).

---

## 1. MACH Architectural Maturity Assessment

Evaluate your platform's operational status across the 4 core pillars of **MACH (Microservices, API-First, Cloud-Native, Headless)**, along with Observability and CI/CD automation.

Visit the interactive calculator above to select your current engineering realities and receive:
- **0–100 Quantitative Score** and maturity level tier (Legacy Monolith to Native Enterprise MACH).
- **Per-Pillar Breakdown** identifying architectural debt.
- **Actionable Strategic Recommendation** based on modern cloud-native patterns.
- **One-Click Clipboard Export** for engineering alignment reviews.

---

## 2. Infrastructure TCO & P99 Latency Simulator

Tune peak requests per second (RPS), domain count, and monthly release cadence to visualize side-by-side trade-offs between:
1. **Traditional Monolith**: Shared database contention and large blast radius.
2. **Enterprise MACH**: Elastic horizontal scaling, mTLS zero-trust networking, and low tail latency.
3. **Event-Driven Serverless**: Pay-per-invocation elasticity and minimal idle infrastructure waste.

</div>
