---
layout: post
title: "Automatización Inteligente: Pruebas E2E con Playwright y Modelos Locales mediante Ollama"
date: 2026-08-05 14:00:00 -0600
lang: es
categories: [Ingeniería de Software, QA]
tags: [playwright, ollama, ia, machine-learning, e2e-testing, automatizacion, ci-cd]
image:
  path: /assets/img/posts/2026-08-05-automatizacion-e2e-playwright-ollama.png
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

```python
import time
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mach.resiliencia")

class ManejadorOperacionDistribuida:
    def __init__(self, nombre_servicio: str, reintentos_maximos: int = 3, base_retroceso_seg: float = 0.5):
        self.nombre_servicio = nombre_servicio
        self.reintentos_maximos = reintentos_maximos
        self.base_retroceso_seg = base_retroceso_seg

    def ejecutar_con_resiliencia(self, carga_util: Dict[str, Any]) -> Dict[str, Any]:
        intento = 0
        while intento < self.reintentos_maximos:
            try:
                intento += 1
                logger.info(f"[{self.nombre_servicio}] Ejecutando intento {intento}/{self.reintentos_maximos}")
                if not carga_util.get("clave_idempotencia"):
                    raise ValueError("Falta la clave de idempotencia obligatoria")
                return {"estado": "EXITO", "intento": intento, "datos": carga_util}
            except Exception as ex:
                logger.warning(f"[{self.nombre_servicio}] Error transitorio detectado: {ex}")
                if intento >= self.reintentos_maximos:
                    logger.error(f"[{self.nombre_servicio}] Reintentos agotados. Disparando circuito de compensacion.")
                    raise RuntimeError(f"Fallo critico tras {self.reintentos_maximos} intentos: {ex}")
                time.sleep(self.base_retroceso_seg * (2 ** (intento - 1)))
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
