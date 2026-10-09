---
title: Glossary
icon: fas fa-book
order: 6
---

<div class="lang-block lang-es" markdown="1">

# Glosario de Arquitectura MACH y Composable

Diccionario de referencia exhaustivo y alfabético de términos fundamentales, patrones de diseño y conceptos empresariales en **Microservicios, API-First, Cloud-Native, Headless y Composable Commerce**.

---

### A
- **API-First Design:** Estrategia arquitectónica donde las interfaces de programación de aplicaciones (APIs) se tratan como ciudadanos de primera clase. Las interfaces y contratos (OpenAPI/AsyncAPI) se planifican, diseñan y validan antes de escribir el código de implementación.  
  *Guía Relacionada:* [API-First vs Code-First: Por qué el contrato antes del código vence](/posts/api-first-vs-code-first-why-contract-before-code-wins/)
- **Gobernanza de APIs:** Práctica de aplicar políticas arquitectónicas centralizadas, reglas de linting, verificaciones de seguridad y seguimiento del ciclo de vida a todos los endpoints de la organización.  
  *Guía Relacionada:* [Implementando Gobernanza de APIs: Coherencia en todos los servicios](/posts/implementing-api-governance-enforcing-consistency-across-all-your-services/)
- **AsyncAPI:** Estándar abierto y legible por máquina para documentar y gobernar arquitecturas guiadas por eventos, brokers de mensajería (Kafka, RabbitMQ) y webhooks asíncronos.  
  *Guía Relacionada:* [AsyncAPI para la Gobernanza de Event Streams y Webhooks](/posts/asyncapi-para-la-gobernanza-de-event-streams-y-webhooks-en-tiempo-real/)

---

### B
- **Backends for Frontends (BFF):** Patrón donde se construyen capas intermedias de traducción de backend específicas para clientes frontend determinados (ej. App Móvil vs Web Desktop), evitando endpoints genéricos sobrecargados.
- **Patrón Bulkhead (Mamparos):** Patrón de aislamiento inspirado en los mamparos de barcos que segmenta recursos críticos (pools de hilos, memoria, cómputo) para que el fallo en un subsistema no agote los recursos ni colapse el sistema entero.  
  *Guía Relacionada:* [Patrón Bulkhead: Aislando fallos en flotas distribuidas](/posts/bulkhead-pattern-isolating-failures-so-one-service-cant-sink-the-fleet/)
- **Bounded Context (Contexto Delimitado):** Patrón central de Domain-Driven Design (DDD) que define límites lingüísticos y lógicos explícitos dentro de los cuales un modelo de dominio se aplica de forma coherente.  
  *Guía Relacionada:* [Límites de Servicio por Dominio: Aplicando DDD a Microservicios](/posts/service-boundaries-by-domain-applying-ddd-bounded-contexts-to-microservices/)

---

### C
- **Despliegues Canarios (Canary):** Técnica de entrega progresiva donde las nuevas versiones se liberan a un pequeño porcentaje de usuarios antes del despliegue total, monitoreando tasas de error para prevenir interrupciones.  
  *Guía Relacionada:* [Feature Flagging y Despliegues Canarios para Cero Downtime](/posts/feature-flagging-in-cloud-native-deployments-canary-releases-and-zero-downtime-rollouts/)
- **Circuit Breaker (Interruptor de Circuito):** Patrón de estabilidad que detecta fallos aguas abajo y previene caídas en cascada abriendo el circuito rápidamente para fallar rápido o retornar datos de fallback sin agotar conexiones.  
  *Guía Relacionada:* [Patrón Circuit Breaker: Protegiendo servicios ante fallos en cascada](/posts/circuit-breaker-pattern-protecting-your-services-from-cascading-failures/)
- **Composable Commerce:** Enfoque de comercio digital modular que selecciona componentes tecnológicos especializados (*best-of-breed*: PIM, Checkout, Búsqueda, CMS) unificados mediante APIs en lugar de depender de suites monolíticas rígidas.  
  *Guía Relacionada:* [Composición Tecnológica Best-of-Breed: Por qué los especialistas superan a las suites](/posts/composing-best-of-breed-technology-why-specialized-vendors-beat-all-in-one-suites/)
- **CQRS (Command Query Responsibility Segregation):** Patrón que separa las operaciones de lectura (queries) de las de escritura (commands), permitiendo optimización, escalado y caché independientes.  
  *Guía Relacionada:* [CQRS y Event Sourcing: Separando lecturas y escrituras](/posts/cqrs-and-event-sourcing-separating-reads-and-writes-in-data-heavy-services/)

---

### D
- **Propiedad de Datos (Database-per-Service):** Regla estricta de microservicios que establece que cada servicio administra exclusivamente su propio almacén de datos, evitando dependencias ocultas por llaves foráneas.  
  *Guía Relacionada:* [Propiedad de Datos en Microservicios: Por qué cada servicio debe poseer su base de datos](/posts/data-ownership-in-microservices-why-services-must-own-their-databases/)
- **Monolito Distribuido:** Antipatrón donde una aplicación se divide en múltiples microservicios que permanecen fuertemente acoplados mediante bases de datos compartidas, cascadas síncronas o despliegues coordinados.  
  *Guía Relacionada:* [La Trampa del Monolito Distribuido](/posts/the-distributed-monolith-trap-how-microservices-become-what-they-replace/)
- **Distributed SQL:** Arquitectura de base de datos que escala horizontalmente entre regiones geográficas manteniendo garantías transaccionales ACID estrictas.  
  *Guía Relacionada:* [Sistemas SQL Distribuidos y Resiliencia con YugabyteDB](/posts/sistemas-sql-distribuidos-yugabytedb/)

---

### E
- **Arquitectura Dirigida por Eventos (EDA):** Paradigma arquitectónico donde componentes desacoplados se comunican asíncronamente produciendo, detectando y consumiendo eventos discretos.  
  *Guía Relacionada:* [Arquitectura Dirigida por Eventos en E-Commerce](/posts/event-driven-architecture-in-e-commerce-async-messaging-for-orders-inventory-and-shipping/)
- **Caché en el Edge & CDN:** Distribución geográfica de respuestas de API y activos estáticos cerca del usuario final en nodos perimetrales para reducir la latencia de origen.  
  *Guía Relacionada:* [Estrategias de Caché Distribuida y Edge en Headless](/posts/estrategias-cache-distribuida-edge-headless/)

---

### F
- **FinOps para Arquitecturas Cloud:** Marco operativo y disciplina cultural que une finanzas, ingeniería y DevOps para medir, controlar y optimizar el costo unitario de transacción en arquitecturas cloud y contratos SaaS multi-vendor.  
  *Guía Relacionada:* [FinOps para MACH: Control de Costos y Facturación Multi-Vendor](/posts/finops-para-mach-control-de-costos-y-optimizacion-de-facturacion-multi-vendor/)

---

### G
- **GraphQL Federation (Apollo Federation):** Arquitectura modular que permite componer múltiples subgrafos autónomos administrados por microservicios independientes en un único supergrafo unificado sin crear un monolito central de API.  
  *Guía Relacionada:* [Federación de GraphQL (Apollo Federation v2) vs REST Gateway](/posts/federacion-de-graphql-apollo-federation-v2-vs-rest-gateway-en-ecosistemas-composable/)

---

### H
- **Arquitectura Headless:** Desacoplamiento total entre la capa de presentación frontend (UI/UX) y la lógica de negocio y persistencia backend, comunicándose únicamente vía APIs.  
  *Guía Relacionada:* [Entendiendo el CMS Headless: Desacoplando contenido de presentación](/posts/understanding-headless-cms-decoupling-content-from-presentation/)

---

### I
- **Idempotencia Transaccional (Idempotency Key):** Propiedad matemática y arquitectónica donde una solicitud puede ejecutarse repetidamente produciendo exactamente el mismo resultado y estado en el sistema, esencial para procesar pagos y webhooks sin duplicaciones.  
  *Guía Relacionada:* [Idempotencia de Pagos y Webhooks Distribuidos con Colas Dead-Letter](/posts/idempotencia-de-pagos-y-webhooks-distribuidos-con-colas-dead-letter-dlq/)

---

### M
- **Arquitectura MACH:** Principio tecnológico que combina **M**icroservices, **A**PI-first, **C**loud-native y **H**eadless para construir software empresarial componible, escalable y libre de vendor lock-in.
- **Micro-Frontends & Module Federation:** Extensión del desacoplamiento de microservicios al cliente web, permitiendo que múltiples equipos autónomos desarrollen, prueben y desplieguen fragmentos de la UI en tiempo de ejecución sin recompilar la aplicación principal.  
  *Guía Relacionada:* [Micro-Frontends con Module Federation: Modularización sin Pérdida de Rendimiento](/posts/micro-frontends-con-module-federation-modularizacion-sin-perdida-de-rendimiento/)

---

### O
- **OpenTelemetry (OTel):** Estándar de observabilidad neutral de la CNCF para la recopilación, instrumentación y exportación unificada de trazas distribuidas, métricas y logs.  
  *Guía Relacionada:* [Observabilidad Centralizada y Trazas Distribuidas para Microservicios](/posts/centralized-observability-distributed-tracing-logging-and-metrics-for-microservices/)
- **Patrón Outbox Transaccional:** Patrón de consistencia que garantiza la publicación confiable de eventos hacia brokers (Kafka, RabbitMQ) registrándolos en una tabla local dentro de la misma transacción SQL antes de capturarlos vía CDC (Change Data Capture / Debezium).  
  *Guía Relacionada:* [Patrón Outbox Transaccional y Debezium en Arquitecturas Distribuidas](/posts/patron-outbox-transaccional-y-debezium-en-arquitecturas-de-microservicios-distribuidas/)

---

### P
- **Packaged Business Capabilities (PBCs):** Agrupaciones modulares de microservicios y datos que encapsulan una función de negocio autónoma y bien delimitada (como Checkout, Catálogo o Promociones) reutilizable entre canales digitales.  
  *Guía Relacionada:* [Modelado y Delimitación de Packaged Business Capabilities (PBCs)](/posts/modelado-y-delimitacion-de-packaged-business-capabilities-pbcs-en-comercio-digital/)
- **PIM Composable (Product Information Management):** Motor especializado en centralizar, validar y enriquecer catálogos de productos para sincronizarlos omnicanalmente vía APIs desacopladas.  
  *Guía Relacionada:* [Transición de Catálogos Monolíticos a Motores Composable PIM (Akeneo, Pimcore)](/posts/transicion-de-catalogos-monoliticos-a-motores-composable-pim-akeneo-pimcore/)

---

### R
- **Rate Limiting Adaptativo & Token Bucket:** Algoritmo en API Gateways que asigna tokens a una tasa constante para regular el tráfico entrante, protegiendo microservicios downstream ante picos y abusos.  
  *Guía Relacionada:* [Estrategias de Rate Limiting Adaptativo y Algoritmos Token Bucket](/posts/estrategias-de-rate-limiting-adaptativo-y-algoritmos-token-bucket-en-api-gateways/)
- **React Server Components (RSC) & Hidratación Parcial:** Arquitectura frontend donde componentes computacionalmente intensivos se ejecutan en el servidor sin transferir JavaScript al cliente, optimizando dramáticamente Core Web Vitals (INP y LCP).  
  *Guía Relacionada:* [Estrategias de Hidratación Parcial y React Server Components](/posts/estrategias-de-hidratacion-parcial-y-react-server-components-en-arquitecturas-headless/)

---

### S
- **Patrón Saga:** Patrón de diseño para gestionar transacciones distribuidas complejas en microservicios a través de secuencias de transacciones locales coordinadas mediante coreografía u orquestación.  
  *Guía Relacionada:* [Patrón Saga: Coreografiado vs Orquestado con Temporal.io](/posts/patron-saga-coreografiado-vs-orquestado-con-temporalio-en-cadenas-de-suministro-multi-vendor/)
- **Malla de Servicios (Service Mesh):** Capa de infraestructura dedicada (como Istio o Linkerd) para controlar, proteger y observar la comunicación síncrona servicio a servicio mediante sidecars.  
  *Guía Relacionada:* [Service Mesh vs API Gateway: Eligiendo la herramienta correcta](/posts/service-mesh-vs-api-gateway-choosing-the-right-tool-for-the-right-layer/)
- **Patrón Strangler Fig:** Estrategia de modernización que reemplaza gradualmente funcionalidades específicas de un monolito por microservicios hasta desmantelar el sistema heredado por completo.  
  *Guía Relacionada:* [El Patrón Strangler Fig: Migrando un monolito sin reescritura total](/posts/the-strangler-fig-pattern-migrating-a-monolith-without-a-big-bang-rewrite/)

---

### T
- **Temporal.io (Workflow as Code):** Motor de ejecución determinista y duradero que permite implementar sagas orquestadas complejas con reintentos transparentes, timeouts infinitos y compensación transaccional garantizada.  
  *Guía Relacionada:* [Patrón Saga: Coreografiado vs Orquestado con Temporal.io](/posts/patron-saga-coreografiado-vs-orquestado-con-temporalio-en-cadenas-de-suministro-multi-vendor/)

---

### Z
- **Seguridad Zero Trust & Autenticación mTLS:** Principio de seguridad estricto que asume que la red interna está comprometida, verificando criptográficamente la identidad de cada microservicio emisor y receptor mediante TLS mutuo con SPIFFE/SPIRE.  
  *Guía Relacionada:* [Seguridad Zero Trust y Autenticación mTLS entre Microservicios](/posts/seguridad-zero-trust-y-autenticacion-mtls-entre-microservicios-con-spiffe-y/)

</div>

<div class="lang-block lang-en d-none" markdown="1">

# MACH & Composable Architecture Glossary

A comprehensive, alphabetical reference dictionary of foundational terms, design patterns, and enterprise concepts in **Microservices, API-First, Cloud-Native, Headless, and Composable Commerce**.

---

### A
- **API-First Design:** An architectural strategy where application programming interfaces (APIs) are treated as first-class citizens. Interfaces and contracts (OpenAPI/AsyncAPI) are planned, mocked, and validated before writing backend implementation logic.  
  *Related Guide:* [API-First vs Code-First: Why Contract Before Code Wins](/posts/api-first-vs-code-first-why-contract-before-code-wins/)
- **API Governance:** The practice of applying centralized architectural policies, linting rules, security verifications, and lifecycle tracking to all organizational endpoints.  
  *Related Guide:* [Implementing API Governance: Enforcing Consistency Across Services](/posts/implementing-api-governance-enforcing-consistency-across-all-your-services/)
- **AsyncAPI:** An open-source, machine-readable specification standard for documenting and governing event-driven architectures, message brokers (Kafka, RabbitMQ), and asynchronous webhooks.  
  *Related Guide:* [AsyncAPI para la Gobernanza de Event Streams y Webhooks](/posts/asyncapi-para-la-gobernanza-de-event-streams-y-webhooks-en-tiempo-real/)

---

### B
- **Backends for Frontends (BFF):** A pattern where specialized backend translation layers are created for specific frontend clients (e.g., Mobile App vs Web Desktop), avoiding generic bloated endpoints.
- **Bulkhead Pattern:** An isolation pattern inspired by ship hulls that segments critical system resources (thread pools, memory, compute pools) so that a failure in one subsystem cannot exhaust resources and crash the entire system.  
  *Related Guide:* [Bulkhead Pattern: Isolating Failures in Distributed Fleets](/posts/bulkhead-pattern-isolating-failures-so-one-service-cant-sink-the-fleet/)
- **Bounded Context:** A central domain-driven design (DDD) pattern defining explicit linguistic and logical boundaries within which a domain model applies consistently.  
  *Related Guide:* [Service Boundaries by Domain: Applying DDD to Microservices](/posts/service-boundaries-by-domain-applying-ddd-bounded-contexts-to-microservices/)

---

### C
- **Canary Deployments:** A progressive delivery technique where new software versions are rolled out to a small percentage of users before full deployment, monitoring error rates to prevent outages.  
  *Related Guide:* [Feature Flagging & Canary Releases for Zero Downtime](/posts/feature-flagging-in-cloud-native-deployments-canary-releases-and-zero-downtime-rollouts/)
- **Circuit Breaker:** A stability design pattern that detects downstream failures and prevents cascading system crashes by quickly tripping open to fail fast or return fallback data without exhausting upstream connections.  
  *Related Guide:* [Circuit Breaker Pattern: Protecting Services from Cascading Failures](/posts/circuit-breaker-pattern-protecting-your-services-from-cascading-failures/)
- **Composable Commerce:** A modular digital commerce approach selecting best-of-breed software components (PIM, Checkout, Search, CMS) unified via APIs rather than relying on monolithic all-in-one software suites.  
  *Related Guide:* [Composing Best-of-Breed Technology: Why Specialized Vendors Beat Suites](/posts/composing-best-of-breed-technology-why-specialized-vendors-beat-all-in-one-suites/)
- **CQRS (Command Query Responsibility Segregation):** A pattern separating read operations (queries) from write operations (commands), enabling independent optimization, scaling, and caching for data models.  
  *Related Guide:* [CQRS and Event Sourcing: Separating Reads and Writes](/posts/cqrs-and-event-sourcing-separating-reads-and-writes-in-data-heavy-services/)

---

### D
- **Data Ownership (Database-per-Service):** A strict microservice rule stating that a service exclusively owns and manages its underlying datastore, preventing hidden foreign-key couplings.  
  *Related Guide:* [Data Ownership in Microservices: Why Services Must Own Their Databases](/posts/data-ownership-in-microservices-why-services-must-own-their-databases/)
- **Distributed Monolith:** An anti-pattern where an application is decomposed into multiple microservices that remain tightly coupled through shared databases, synchronous cascades, or coordinated deployments.  
  *Related Guide:* [The Distributed Monolith Trap](/posts/the-distributed-monolith-trap-how-microservices-become-what-they-replace/)
- **Distributed SQL:** A database architecture that scales horizontally across geographic regions while maintaining ACID transactional guarantees.  
  *Related Guide:* [Sistemas SQL Distribuidos y Resiliencia con YugabyteDB](/posts/sistemas-sql-distribuidos-yugabytedb/)

---

### E
- **Event-Driven Architecture (EDA):** A software architecture paradigm where decoupled software components communicate asynchronously by producing, detecting, and consuming discrete events.  
  *Related Guide:* [Event-Driven Architecture in E-Commerce](/posts/event-driven-architecture-in-e-commerce-async-messaging-for-orders-inventory-and-shipping/)
- **Edge Caching & CDN:** Distributing cached API payloads and static assets geographically close to end users at edge nodes to reduce origin latency.  
  *Related Guide:* [Estrategias de Caché Distribuida y Edge en Headless](/posts/estrategias-cache-distribuida-edge-headless/)

---

### F
- **FinOps for Cloud Architectures:** An operational framework and cultural practice uniting finance, engineering, and DevOps to monitor and optimize unit economic costs across multi-vendor cloud and SaaS contracts in real time.  
  *Related Guide:* [FinOps para MACH: Control de Costos y Facturación Multi-Vendor](/posts/finops-para-mach-control-de-costos-y-optimizacion-de-facturacion-multi-vendor/)

---

### G
- **GraphQL Federation (Apollo Federation):** A composable architecture allowing multiple autonomous subgraphs governed by independent microservices to be composed into a unified supergraph without building a centralized monolithic API gateway.  
  *Related Guide:* [Federación de GraphQL (Apollo Federation v2) vs REST Gateway](/posts/federacion-de-graphql-apollo-federation-v2-vs-rest-gateway-en-ecosistemas-composable/)

---

### H
- **Headless Architecture:** Decoupling the frontend presentation layer from the backend business logic and datastores, exposing capabilities strictly via APIs.  
  *Related Guide:* [Understanding Headless CMS: Decoupling Content from Presentation](/posts/understanding-headless-cms-decoupling-content-from-presentation/)

---

### I
- **Transactional Idempotency (Idempotency Key):** A mathematical and architectural guarantee ensuring an API request or event can be executed multiple times with identical results, preventing duplicate charges, inventory reservations, or side effects.  
  *Related Guide:* [Idempotencia de Pagos y Webhooks Distribuidos con Colas Dead-Letter](/posts/idempotencia-de-pagos-y-webhooks-distribuidos-con-colas-dead-letter-dlq/)

---

### M
- **MACH Architecture:** An architectural philosophy combining **M**icroservices, **A**PI-first, **C**loud-native, and **H**eadless to build agile, composable, and vendor-lock-in-free enterprise digital systems.
- **Micro-Frontends & Module Federation:** Extending microservice decoupling to client applications, enabling cross-functional teams to autonomously build and deploy runtime-composed UI fragments without rebuilding the container host.  
  *Related Guide:* [Micro-Frontends con Module Federation: Modularización sin Pérdida de Rendimiento](/posts/micro-frontends-con-module-federation-modularizacion-sin-perdida-de-rendimiento/)

---

### O
- **OpenTelemetry (OTel):** A vendor-neutral CNCF observability framework providing a unified standard for collecting, instrumenting, and exporting distributed traces, metrics, and logs.  
  *Related Guide:* [Centralized Observability & Distributed Tracing for Microservices](/posts/centralized-observability-distributed-tracing-logging-and-metrics-for-microservices/)
- **Transactional Outbox Pattern:** A resilience pattern ensuring reliable at-least-once message publishing by writing events to an Outbox table inside the local database transaction before asynchronous capture via CDC (Debezium).  
  *Related Guide:* [Patrón Outbox Transaccional y Debezium en Arquitecturas Distribuidas](/posts/patron-outbox-transaccional-y-debezium-en-arquitecturas-de-microservicios-distribuidas/)

---

### P
- **Packaged Business Capabilities (PBCs):** Gartner-defined building blocks aggregating microservices and data models around a well-defined business capability (e.g., Checkout, Product Catalog, Pricing) consumed via standard APIs.  
  *Related Guide:* [Modelado y Delimitación de Packaged Business Capabilities (PBCs)](/posts/modelado-y-delimitacion-de-packaged-business-capabilities-pbcs-en-comercio-digital/)
- **Composable PIM (Product Information Management):** A dedicated engine for aggregating, enriching, and syndicating master product data across omnichannel headless touchpoints.  
  *Related Guide:* [Transición de Catálogos Monolíticos a Motores Composable PIM (Akeneo, Pimcore)](/posts/transicion-de-catalogos-monoliticos-a-motores-composable-pim-akeneo-pimcore/)

---

### R
- **Adaptive Rate Limiting & Token Bucket:** Throttling algorithms enforced at the API gateway layer to protect downstream microservices from volumetric attacks and cascading queue buildups.  
  *Related Guide:* [Estrategias de Rate Limiting Adaptativo y Algoritmos Token Bucket](/posts/estrategias-de-rate-limiting-adaptativo-y-algoritmos-token-bucket-en-api-gateways/)
- **React Server Components (RSC) & Partial Hydration:** A modern frontend rendering pattern where heavy computation and dependencies execute strictly on the server with zero client JavaScript payload, drastically improving Core Web Vitals.  
  *Related Guide:* [Estrategias de Hidratación Parcial y React Server Components](/posts/estrategias-de-hidratacion-parcial-y-react-server-components-en-arquitecturas-headless/)

---

### S
- **Saga Pattern:** A design pattern for managing complex distributed transactions across multiple microservices via sequences of coordinated local transactions using choreography or orchestration.  
  *Related Guide:* [Patrón Saga: Coreografiado vs Orquestado con Temporal.io](/posts/patron-saga-coreografiado-vs-orquestado-con-temporalio-en-cadenas-de-suministro-multi-vendor/)
- **Service Mesh:** A dedicated infrastructure layer (such as Istio or Linkerd) that controls, secures, and observes synchronous service-to-service communication via proxy sidecars.  
  *Related Guide:* [Service Mesh vs API Gateway: Choosing the Right Tool](/posts/service-mesh-vs-api-gateway-choosing-the-right-tool-for-the-right-layer/)
- **Strangler Fig Pattern:** A legacy modernization strategy incrementally replacing specific parts of a monolith with microservices until the monolithic system can be completely retired.  
  *Related Guide:* [The Strangler Fig Pattern: Migrating a Monolith Without a Big Bang Rewrite](/posts/the-strangler-fig-pattern-migrating-a-monolith-without-a-big-bang-rewrite/)

---

### T
- **Temporal.io (Workflow as Code):** A developer-first, durable execution platform that orchestrates distributed sagas and mission-critical transactions with deterministic state recovery and automated compensations.  
  *Related Guide:* [Patrón Saga: Coreografiado vs Orquestado con Temporal.io](/posts/patron-saga-coreografiado-vs-orquestado-con-temporalio-en-cadenas-de-suministro-multi-vendor/)

---

### Z
- **Zero Trust Security & mTLS:** A security paradigm enforcing cryptographic verification for every cross-service request via Mutual TLS (SPIFFE/SPIRE) regardless of network perimeter boundaries.  
  *Related Guide:* [Seguridad Zero Trust y Autenticación mTLS entre Microservicios](/posts/seguridad-zero-trust-y-autenticacion-mtls-entre-microservicios-con-spiffe-y/)

</div>
