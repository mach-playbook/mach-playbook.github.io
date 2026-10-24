---
mermaid: true
layout: post
title: "Dominando la Explosión de Cardinalidad: OpenTelemetry, Jaeger y Métricas RED Bajo Cargas Masivas"
date: 2026-10-24 09:00:00 -0600
lang: es
categories: [Cloud Native, Microservicios]
tags: [opentelemetry, jaeger, metricas-red, observabilidad, tracing-distribuido, kubernetes, rendimiento]
image:
  path: /assets/img/posts/2026-10-24-observabilidad-cardinal-con-opentelemetry-jaeger-y-metricas-red-en-microservicios.png
---

Durante un evento de alta concurrencia con 120,000 solicitudes por segundo, el clúster de Prometheus colapsa por un fallo catastrófico de Out-Of-Memory (OOMKilled). Simultáneamente, el backend de almacenamiento de Jaeger sufre una saturación de I/O que eleva la latencia de escritura a más de cuatro segundos por lote de spans, provocando el descarte masivo de trazas en los buffers de memoria de las aplicaciones. 

La causa raíz no fue un ataque DDoS ni una fuga de memoria en la lógica de negocio: fue la inyección descuidada de identificadores únicos (`order_id`, `user_id` y `payment_intent_id`) como etiquetas (*labels*) en las métricas de Prometheus, sumada a una política de muestreo ingenuo (*head-based sampling* al 100%) en OpenTelemetry.

En arquitecturas distribuidas enterprise basadas en principios MACH, la observabilidad no es simplemente emitir telemetría; es gestionar la densidad de información sin destruir la infraestructura que la procesa. 

Cuando los microservicios escalan a cientos de pods, la intersección entre métricas de alta dimensionalidad y trazabilidad distribuida exige desacoplar el modelo de datos operacional del modelo de datos diagnóstico. La solución arquitectónica radica en estructurar la telemetría bajo el patrón **RED (Rate, Errors, Duration)** a baja cardinalidad para la detección inmediata, correlacionada mediante **OpenTelemetry Exemplars** y procesadores de **Tail-Based Sampling** hacia backends analíticos distribuidos como Jaeger.

---

## Anatomía del Fallo: El Abismo de la Hiper-Cardinalidad

Una métrica en Prometheus o VictoriaMetrics se define por su nombre y un conjunto de pares clave-valor (etiquetas). Cada combinación única de etiquetas crea una **serie temporal independiente** en la memoria del motor Time Series Database (TSDB):

$$\text{Series Totales} = \prod_{i=1}^{n} |V(L_i)|$$

Donde $|V(L_i)|$ es el número de valores únicos posibles para la etiqueta $i$.

Si un servicio expone `http_requests_total` con las etiquetas `method` (4 valores), `status_code` (10 valores), `route` (50 valores) y un ingeniero agrega `customer_id` (1,000,000 clientes activos en el catálogo Composable), el espacio muestral pasa de $4 \times 10 \times 50 = 2,000$ series temporales a:

$$4 \times 10 \times 50 \times 1,000,000 = 2,000,000,000 \text{ series activas}$$

Este volumen satura el índice invertido del TSDB, destruye el buffer de bloques (*head chunks* en disco) y eleva el uso de RAM más allá de los 64 GB en cuestión de minutos.

Por otro lado, capturar trazas distribuidas completas de todas las transacciones para compensar la falta de contexto en las métricas genera un costo de transferencia (*egress*) y almacenamiento descomunal: generar 2 KB por span a 100,000 peticiones/segundo con una profundidad promedio de 8 spans por traza produce:

$$\frac{100,000 \times 8 \times 2 \text{ KB}}{1,024 \times 1,024} \approx 1.52 \text{ GB/segundo} \implies 131 \text{ TB/día}$$

El dilema arquitectónico es claro: **necesitamos la granularidad del dato contextual para resolver incidentes en Día 2, pero no podemos permitir que la dimensionalidad de las métricas destruya la telemetría.**

---

## Arquitectura de Telemetría Cardinal con OpenTelemetry y Jaeger

Para resolver esta tensión, la arquitectura desacopla la recolección, el procesamiento y la exportación utilizando el patrón **Two-Tier OpenTelemetry Collector**:

1. **Tier 1 (Agent DaemonSet):** Corre localmente en cada nodo de Kubernetes. Recibe datos vía gRPC/OTLP (`4317`) desde los pods de la aplicación, realiza enriquecimiento con metadatos de Kubernetes (namespace, pod_name, container_id) y aplica rate-limiting inicial.
2. **Tier 2 (Gateway StatefulSet):** Clúster escalable con enrutamiento consistente por `trace_id`. Aplica **Tail-Based Sampling** para retener únicamente las trazas que contienen errores (HTTP 5xx, excepciones de base de datos) o cuya duración supera el percentil 99 ($p99$).
3. **Pipeline RED Derivado (SpanMetrics):** El Collector genera métricas de infraestructura (Rate, Errors, Duration) directamente de los spans en tránsito, manteniendo etiquetas normalizadas (baja cardinalidad), e inyecta el `trace_id` como un **Exemplar** en las muestras enviadas a Prometheus.

```mermaid
flowchart TD
    subgraph K8s_Nodes ["Nodos de Kubernetes (Tier 1)"]
        subgraph Pod_A ["Order Service"]
            AppA[App Pod - Go/Node] -->|OTLP Traces| OTelAgent1[OTel Collector Agent]
        end
        subgraph Pod_B ["Inventory Service"]
            AppB[App Pod - Java] -->|OTLP Traces| OTelAgent2[OTel Collector Agent]
        end
    end

    subgraph OTel_Gateway_Cluster ["Gateway Cluster (Tier 2 - StatefulSet)"]
        Router[Load-Balancing Exporter\nHash(trace_id)]
        OTelGW1[Collector Gateway 1\nTail-Based Sampling]
        OTelGW2[Collector Gateway 2\nTail-Based Sampling]
        Router --> OTelGW1
        Router --> OTelGW2
    end

    OTelAgent1 -->|gRPC Load-Balanced| Router
    OTelAgent2 -->|gRPC Load-Balanced| Router

    subgraph Storage_Layer ["Capa de Persistencia y Visualización"]
        Prometheus[Prometheus / Thanos\nRED Metrics + Exemplars]
        Jaeger[Jaeger Query / UI]
        ClickHouse[(ClickHouse / Cassandra\nJaeger Spans)]
    end

    OTelGW1 -->|SpanMetrics Processor| Prometheus
    OTelGW2 -->|SpanMetrics Processor| Prometheus

    OTelGW1 -->|Sampled Spans: Errores + p99| ClickHouse
    OTelGW2 -->|Sampled Spans: Errores + p99| ClickHouse

    ClickHouse --> Jaeger
    Prometheus -.->|Jump via Exemplar Trace ID| Jaeger
```

---

## Implementación del OpenTelemetry Collector Gateway

La configuración del Collector de segundo nivel (Gateway) debe aislar el procesamiento de trazas, derivar métricas RED y aplicar el muestreo inteligente. A continuación se presenta una especificación de producción optimizada para cargas críticas.

### Configuración: `otel-collector-gateway.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-gateway-config
  namespace: observability
data:
  otel-collector-config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
            max_concurrent_streams: 1024
          http:
            endpoint: 0.0.0.0:4318

    processors:
      memory_limiter:
        check_interval: 1s
        limit_percentage: 75
        spike_limit_percentage: 20

      # Derivación de Métricas RED desde Spans sin alta cardinalidad
      spanmetrics:
        metrics_exporter: prometheus
        latency_histogram_buckets: [5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s]
        dimensions:
          - name: http.status_code
          - name: http.method
          - name: http.route
        dimensions_cache_size: 10000
        aggregation_temporality: "AGGREGATION_TEMPORALITY_CUMULATIVE"

      # Muestreo basado en colas (Tail-Based Sampling)
      tail_sampling:
        decision_wait: 10s
        num_traces: 50000
        expected_new_traces_per_sec: 5000
        policies:
          # 1. Conservar el 100% de trazas con errores (HTTP 5xx o Span Status Error)
          - name: error-policy
            type: status_code
            status_code: { status_codes: [ ERROR ] }
          
          # 2. Conservar trazas donde la latencia supere el umbral SLA (ej. 1500ms)
          - name: latency-sla-policy
            type: latency
            latency: { threshold_ms: 1500 }

          # 3. Muestreo probabilístico estocástico del 2% para tráfico exitoso estándar
          - name: probabilistic-policy
            type: probabilistic
            probabilistic: { sampling_percentage: 2.0 }

      batch:
        send_batch_size: 8192
        timeout: 1s
        send_batch_max_size: 16384

    exporters:
      prometheus:
        endpoint: 0.0.0.0:8889
        namespace: "service_red"
        send_timestamps: true
        enable_open_metrics: true # Habilita Exemplars nativos

      otlp/jaeger:
        endpoint: jaeger-collector.observability.svc.cluster.local:4317
        tls:
          insecure: true

    service:
      telemetry:
        logs:
          level: "warn"
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, spanmetrics, tail_sampling, batch]
          exporters: [otlp/jaeger]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [prometheus]
```

El procesador `spanmetrics` computa automáticamente las métricas RED en tiempo real antes de aplicar el `tail_sampling`. De esta forma:
* **Rate:** Calculado mediante el conteo del histograma generado por `spanmetrics`.
* **Errors:** Agrupados por `status_code` o error nativo del span.
* **Duration:** Capturada en el histograma de latencia por percentiles.

Incluso si el `tail_sampling` descarta el 98% de las trazas exitosas para proteger el almacenamiento de Jaeger, las métricas RED reflejan **matemáticamente el 100% del tráfico** que atravesó el sistema.

---

## Instrumentación en Aplicaciones: Gestión de Contexto y Alta Cardinalidad

El código de los microservicios debe seguir una regla categórica: **los datos de alta cardinalidad solo deben persistirse como atributos de span (atributos de traza), nunca como etiquetas de métricas.**

A continuación se muestra un microservicio de procesamiento de pedidos implementado en Go con instrumentación nativa de OpenTelemetry SDK v1.28+, demostrando la propagación de contexto, inyección segura de atributos de diagnóstico y asociación de exemplars.

```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/metric"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
)

var (
	tracer = otel.Tracer("checkout-orchestrator")
	meter  = otel.Meter("checkout-metrics")

	// Métrica RED de baja cardinalidad
	orderDurationHistogram metric.Float64Histogram
)

func initMetrics() {
	var err error
	orderDurationHistogram, err = meter.Float64Histogram(
		"checkout.order.processing.duration",
		metric.WithDescription("Latencia de procesamiento de checkout"),
		metric.WithUnit("s"),
	)
	if err != nil {
		panic(err)
	}
}

func OrderCheckoutHandler(w http.ResponseWriter, r *http.Request) {
	startTime := time.Now()

	// 1. Extraer el contexto propagado (W3C TraceContext)
	ctx := otel.GetTextMapPropagator().Extract(r.Context(), propagation.HeaderCarrier(r.Header))
	
	// 2. Iniciar el Span de la transacción
	ctx, span := tracer.Start(ctx, "OrderCheckoutHandler",
		trace.WithSpanKind(trace.SpanKindServer),
	)
	defer span.End()

	// 3. Extracción de datos del payload
	customerTier := r.Header.Get("X-Customer-Tier") // Baja cardinalidad: "bronze", "silver", "gold"
	orderID := r.Header.Get("X-Order-ID")           // ALTA CARDINALIDAD: UUID único
	paymentGateway := "stripe"

	// ANTI-PATRÓN EVITADO: No incluir 'orderID' en los labels de la métrica.
	// REGLA MACH: Alta cardinalidad -> Atributos del Span únicamente.
	span.SetAttributes(
		attribute.String("checkout.order_id", orderID),
		attribute.String("checkout.customer_tier", customerTier),
		attribute.String("checkout.gateway", paymentGateway),
	)

	// Simulación de procesamiento de la orden y llamada RPC a inventario
	err := processOrderSaga(ctx, orderID)
	duration := time.Since(startTime).Seconds()

	if err != nil {
		// Marcar span con error
		span.RecordError(err)
		span.SetStatus(codes.Error, err.Error())
		
		// Registro en histograma con etiqueta de status
		metricLabels := metric.WithAttributes(
			attribute.String("status", "error"),
			attribute.String("customer_tier", customerTier),
		)
		orderDurationHistogram.Record(ctx, duration, metricLabels)

		http.Error(w, `{"error":"failed to process order"}`, http.StatusInternalServerError)
		return
	}

	span.SetStatus(codes.Ok, "Order processed successfully")

	// Métrica exitosa: Solo etiquetas con dimensionalidad acotada
	metricLabels := metric.WithAttributes(
		attribute.String("status", "success"),
		attribute.String("customer_tier", customerTier),
	)
	orderDurationHistogram.Record(ctx, duration, metricLabels)

	w.WriteHeader(http.StatusAccepted)
	w.Write([]byte(`{"status":"processing"}`))
}

func processOrderSaga(ctx context.Context, orderID string) error {
	tr := otel.Tracer("order-saga")
	childCtx, span := tr.Start(ctx, "ExecutePaymentReservation")
	defer span.End()

	span.SetAttributes(attribute.String("internal.saga.id", fmt.Sprintf("saga-%s", orderID)))

	// Simulación de latencia de red
	time.Sleep(35 * time.Millisecond)

	return nil
}
```

---

## El Rol Crítico de los Exemplars en Métricas RED

Un **Exemplar** es una referencia cruzada que vincula una muestra de métrica específica con una traza distribuida en Jaeger. Permite navegar visualmente desde un pico inusual en una gráfica de percentiles en Grafana directamente a la traza que provocó esa latencia, sin que la métrica deba almacenar IDs únicos.

OpenTelemetry SDK vincula el contexto activo (`TraceID` y `SpanID`) en el almacenamiento temporal de Prometheus cuando se invoca `Record(ctx, value, attributes)`. 

### Consulta de Detección de Anomalías con PromQL:
Para detectar saturación en microservicios dentro de un clúster Kubernetes utilizando las métricas derivadas por `spanmetrics`:

```promql
# Tasa de Errores RED (Errors / Rate) calculada en ventanas de 5 minutos
sum(rate(service_red_calls_total{status_code="STATUS_CODE_ERROR"}[5m])) by (service_name, http_route)
/
sum(rate(service_red_calls_total[5m])) by (service_name, http_route) > 0.05
```

Cuando esta alerta se dispara en el dashboard de monitoreo, la interfaz gráfica extrae el Exemplar subyacente:

```text
Histogram bucket (le=2.5s) -> Value: 142 -> Exemplar: {trace_id="4bf92f3577b34da6a3ce929d0e0e4736"}
```

Al hacer clic en el punto de datos dentro de Grafana, el operador salta instantáneamente a la traza en Jaeger, identificando el microservicio específico dentro del árbol de ejecución que bloqueó el proceso.

---

## Comparativa Arquitectónica de Ingesta y Diagnóstico

Evaluar la estrategia adecuada de observabilidad requiere ponderar el consumo de recursos de infraestructura contra la capacidad diagnóstica en sistemas de misión crítica:

| Dimensión Arquitectónica | Head-Based Sampling (Naive) | SpanMetrics + Tail-Based Sampling (Gateway) | Full High-Cardinality Metrics (Anti-patrón) |
| :--- | :--- | :--- | :--- |
| **Consumo de Memoria TSDB** | Muy bajo (solo almacena métricas predefinidas). | **Óptimo y predecible**: cardinalidad fijada en procesadores. | **Crítico / Inestable**: riesgo constante de OOM. |
| **Costo de Almacenamiento Spans**| Lineal descontrolado ($O(N)$ del tráfico total). | **Reducción del 85% al 95%**: solo almacena anomalías y fallos. | N/A (Generalmente no se almacena traza, se sobrecarga la métrica). |
| **Capacidad de Análisis Forense**| Deficiente: si se muestrea al 1%, el 99% de los fallos transitorios se pierden. | **Máxima**: retención determinista de cualquier traza con error o latencia $> SLA$. | Nula para flujos complejos distribuidos (no hay span graphs). |
| **Impacto de Red (Egress)** | Muy alto si se usa un colector central sin agentes. | **Controlado**: filtrado local mediante compresión gRPC/OTLP y batches. | Alto debido a transferencias constantes de series efímeras. |
| **Complejidad de Mantenimiento** | Baja (configuración básica). | **Media-Alta**: requiere topología StatefulSet con Load-Balancing exporter. | Extrema: necesidad constante de tuning de memoria en Prometheus/TSDB. |

---

## Modos de Fallo Comunes en Producción y Mitigación

### 1. Fuga de Memoria por Fragmentación de Trazas en Tail-Based Sampling

* **Escenario de fallo:** El procesador `tail_sampling` mantiene las trazas en memoria durante `decision_wait: 10s` para verificar si algún span hijo emite un error. En arquitecturas asíncronas basadas en colas (Kafka/RabbitMQ), un consumidor puede tardar minutos en procesar un mensaje. Si la ventana de espera se incrementa imprudentemente a 60 segundos con cargas de 20,000 req/s, la memoria del Collector se agota.
* **Mitigación:** Configurar el procesador `memory_limiter` antes del `tail_sampling` como primera línea de defensa. Implementar el **Load-Balancing Exporter** en el agente local (DaemonSet) usando la clave de partición `trace_id`. Esto garantiza que todos los spans de una misma traza converjan en la **misma réplica del Gateway**, permitiendo mantener ventanas de decisión cortas ($\le 5\text{s}$) sin perder la coherencia de la traza.

### 2. Rotura de Context Propagation en Mensajería Asíncrona

* **Escenario de fallo:** En arquitecturas de Composable Commerce desacopladas por eventos, una orden pasa de un API Gateway a Kafka y luego a un Payment Worker. Si el productor escribe el payload pero olvida inyectar los headers de telemetría en los metadatos del registro de Kafka, Jaeger fragmentará la transacción en dos trazas aisladas, haciendo invisible la latencia del intermediario.
* **Mitigación:** Estandarizar wrappers obligatorios en las librerías de infraestructura internas para serializar y deserializar con `otel.GetTextMapPropagator()`:

```go
// Inyección en los Headers del Mensaje de Kafka
carrier := propagation.MapCarrier{}
otel.GetTextMapPropagator().Inject(ctx, carrier)
for k, v := range carrier {
    kafkaRecord.Headers = append(kafkaRecord.Headers, kafka.Header{Key: k, Value: []byte(v)})
}
```

### 3. Saturación de Descriptores de Red en Exporters hacia Jaeger

* **Escenario de fallo:** Cuando Jaeger se satura, rechaza conexiones gRPC del Collector Gateway. El buffer interno del exportador se desborda y comienza a descartar telemetría indiscriminadamente (*dropped_spans*).
* **Mitigación:** Implementar un almacenamiento intermedio (*persistent queue*) respaldado por disco dentro del propio Collector mediante la propiedad `sending_queue`:

```yaml
exporters:
  otlp/jaeger:
    endpoint: jaeger-collector:4317
    sending_queue:
      enabled: true
      num_consumers: 16
      queue_size: 50000
      storage: file_storage
```

---

## Checklist Operacional para Equipos de Ingeniería

Para certificar que una plataforma de microservicios está lista para soportar eventos de hiper-tráfico sin perder visibilidad ni colapsar sus herramientas de observabilidad:

- [ ] **Validación de Métricas:** Ninguna métrica de Prometheus contiene etiquetas dinámicas generadas por el usuario (`email`, `cart_id`, `uuid`, `timestamp`).
- [ ] **Control de Cardinalidad:** Se aplican reglas en el pipeline CI/CD (usando analizadores estáticos o linters como `promtool`) para rechazar código que registre métricas con nombres de etiquetas prohibidos.
- [ ] **Topología de Doble Capa:** OpenTelemetry opera con Agentes en cada nodo K8s y un Gateway horizontalmente escalable con balanceo hash por `trace_id`.
- [ ] **Políticas RED Estandarizadas:** Las métricas operacionales críticas provienen directamente de `spanmetrics` o contadores normalizados a nivel de middleware HTTP/gRPC.
- [ ] **Filtrado Determinista:** El 100% de los códigos 5xx y las llamadas que superan el percentil 99 ($p99$) son retenidos por el `tail_sampling`. El tráfico exitoso nominal es sub-muestreado a un porcentaje sostenible ($\le 5\%$).
- [ ] **Configuración de Memory Limiter:** Cada instancia de OTel Collector tiene definidos límites duros (`limit_percentage`) para evitar terminaciones por Linux OOM Killer.
- [ ] **Exemplars Habilitados:** La bandera `--enable-feature=exemplar-storage` está encendida en Prometheus y el backend de Grafana tiene configurado el data link directo hacia la instancia de Jaeger Query.