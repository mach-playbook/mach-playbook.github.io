---
layout: post
title: "Estrategias de Testing para Microservicios MACH: De Unit Tests a Contract Testing"
date: 2026-08-26 09:00:00 -0600
lang: es
categories: [Testing, DevOps]
tags: [testing, contract-testing, pact, microservices, mach, devops, tdd]
image:
  path: /assets/img/posts/2026-08-26-testing-estrategias-microservicios-mach.png
---

En una arquitectura MACH con 30 o mas microservicios independientes, la estrategia de testing se convierte en uno de los pilares mas criticos de la ingenieria de software. El testing en sistemas distribuidos tiene caracteristicas unicas que lo diferencian radicalmente del testing de aplicaciones monoliticas: no se puede probar el sistema completo en un entorno local, los servicios evolucionan de forma independiente con sus propios ciclos de release, y los fallos ocurren frecuentemente en los puntos de integracion entre servicios, no dentro de los servicios mismos.

Este articulo explora la piramide de testing especifica para microservicios MACH, con enfasis en las tecnicas mas efectivas y los antipatrones que se deben evitar.

## La Piramide de Testing para Microservicios

La piramide clasica de testing (Unit -> Integration -> E2E) requiere una adaptacion significativa para microservicios MACH. En el contexto de arquitecturas distribuidas, la piramide se extiende en varias capas adicionales.

### Nivel 1: Unit Tests (Base de la piramide)

Los unit tests en microservicios tienen las mismas caracteristicas que en cualquier otro sistema: prueban funciones y clases de forma aislada, son rapidos (milisegundos), y son deterministas (siempre dan el mismo resultado). En un microservicio de 10,000 lineas de codigo, deberia haber entre 200 y 500 unit tests con cobertura por encima del 80 por ciento de la logica de negocio.

El foco debe estar en probar la logica de negocio pura (calculos de precios, validaciones de pedidos, transformaciones de datos) sin dependencias externas. Todas las dependencias (bases de datos, APIs externas) deben ser mockeadas en unit tests.

### Nivel 2: Integration Tests (Pruebas de Integracion)

Los integration tests prueban como el microservicio interactua con sus dependencias inmediatas: la base de datos, el cache, el bus de mensajes. A diferencia de los unit tests, las dependencias reales (o versiones dockerizadas de ellas) son usadas.

Un patron efectivo para integration tests en microservicios es el uso de Testcontainers, una libreria disponible para Java, Go, Python y otros lenguajes que levanta contenedores Docker de las dependencias (PostgreSQL, Redis, Kafka) directamente desde el test, ejecuta los tests, y los destruye al finalizar. Esto garantiza que los integration tests sean reproducibles en cualquier maquina y no dependan de ambientes compartidos.

### Nivel 3: Contract Tests (La Capa Critica en MACH)

El Contract Testing es la tecnica mas importante y diferenciadora para microservicios MACH. Resuelve el problema fundamental de las arquitecturas distribuidas: como verificar que el consumidor y el proveedor de una API son compatibles entre si sin necesitar un ambiente de integracion compartido.

La herramienta de referencia para Contract Testing es **Pact**. El flujo funciona de la siguiente forma: el equipo del microservicio consumidor (por ejemplo, el frontend que consume el Order Service) escribe tests que documentan exactamente que datos espera recibir de la API. Pact genera un archivo de contrato (pact file) que especifica los requests y responses esperados. El equipo del proveedor (Order Service) corre estos contratos en sus propios pipelines de CI usando el Pact Broker, verificando que su API cumple con todos los contratos de todos sus consumidores.

Si un equipo cambia su API de forma que rompe un contrato existente, el pipeline de CI falla automaticamente antes de llegar a produccion. Esto permite a los equipos evolucionar sus APIs de forma independiente con la confianza de que no rompen a sus consumidores.

### Nivel 4: Component Tests

Los component tests prueban el microservicio completo en aislamiento, con todas sus dependencias mockeadas o simuladas. A diferencia de los integration tests que prueban capas individuales, un component test ejecuta el servicio completo y valida su comportamiento observable externamente (los endpoints HTTP, los mensajes publicados al broker, los cambios en la base de datos).

Para microservicios con APIs REST, WireMock es una herramienta excelente que simula las APIs de los servicios externos de los que depende el microservicio bajo prueba.

### Nivel 5: End-to-End Tests (Cima de la piramide)

Los E2E tests en microservicios deben ser minimos y enfocados en los happy paths criticos del negocio. La regla de oro es: si el flujo de negocio falla, el negocio pierde dinero. Por ejemplo, en una plataforma de e-commerce MACH, los E2E tests criticos serian: buscar un producto, agregarlo al carrito, completar el checkout, y verificar que el pedido aparece en el historial del usuario.

Los E2E tests son costosos de mantener y lentos de ejecutar. El antipatron mas comun es tener centenares de E2E tests que prueban escenarios de edge cases que podrian cubrirse mejor con contract tests o component tests a nivel de servicio individual.

## Testing de Event-Driven Architecture

En MACH, muchos microservicios se comunican de forma asincrona a traves de eventos (Kafka, SNS/SQS, EventBridge). El testing de estos flujos requiere un enfoque especifico.

Para unit y integration tests de productores de eventos, el patron es publicar el evento y verificar que el mensaje publicado tiene la estructura correcta usando Testcontainers con Kafka. Para los consumidores, el test publica un mensaje de prueba al broker y verifica que el consumidor lo procesa correctamente y produce los efectos esperados en la base de datos o en otros servicios.

El Contract Testing tambien aplica a eventos. **Pact** soporta mensajeria asincrona (PactV3) y permite definir contratos entre productores y consumidores de eventos, garantizando que la estructura del evento es compatible entre ambas partes.

## Chaos Engineering: Probando la Resiliencia

En MACH, la resiliencia ante fallos parciales es critica. El Chaos Engineering, popularizado por Netflix con su Chaos Monkey, es la practica de inyectar fallos controlados en produccion o en ambientes de staging para verificar que el sistema se comporta correctamente ante ellos.

Las herramientas modernas de Chaos Engineering para Kubernetes incluyen Chaos Mesh, LitmusChaos y AWS Fault Injection Simulator. Los experimentos tipicos son: latencia artificial en la red entre servicios, fallo de pods de Kubernetes, agotamiento de CPU o memoria en contenedores especificos, y particiones de red entre zonas de disponibilidad.

Antes de correr un experimento de Chaos Engineering, se debe definir una hipotesis clara: si el Order Service tiene un timeout de 500ms con el Inventory Service y este ultimo empieza a responder en 1 segundo, entonces el checkout deberia fallar gracefully con un mensaje de error al usuario en lugar de bloquearse indefinidamente.

## Conclusion: Testing como Habilitador de Velocidad

En una arquitectura MACH madura, la estrategia de testing no es un obstaculo para la velocidad de desarrollo: es el habilitador que permite a los equipos desplegar con confianza varias veces al dia. Los equipos que invierten en una piramide de testing solida con Contract Tests en el centro pueden refactorizar y evolucionar sus servicios de forma independiente sin miedo a romper la integracion con otros equipos.

La inversion en testing tiene un ROI claro: menos incidentes en produccion, deploys mas frecuentes, y developers mas confiados que pueden mover rapido sin romper cosas.
