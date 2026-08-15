---
title: Glossary
icon: fas fa-book
order: 5
---

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
- **FinOps:** An operational framework that unites engineering, finance, and product teams to bring financial accountability and automated cost optimization to variable cloud and SaaS spending.  
  *Related Guide:* [FinOps y Desmantelamiento Controlado en Cloud](/posts/finops-desmantelamiento-gcp/)

---

### G
- **gRPC & Protocol Buffers:** A high-performance, open-source universal RPC framework developed by Google that leverages HTTP/2 and Protocol Buffers for fast, binary-serialized internal communication.  
  *Related Guide:* [Diseño de APIs de Alto Rendimiento con gRPC y Protocol Buffers](/posts/diseno-de-apis-de-alto-rendimiento-con-grpc-y-protocol-buffers-para-comunicacion-interna/)

---

### H
- **Headless Architecture:** Decoupling the frontend presentation layer (web, mobile app, IoT) from backend business logic and database layers, communicating exclusively via APIs.  
  *Related Guide:* [Demystifying MACH: A Beginner's Guide to Modern Architecture](/posts/demystifying-mach-a-beginners-guide-to-modern-architecture/)
- **Headless CMS:** A back-end only content management system providing content creators with an editorial interface while exposing raw structured JSON data via REST or GraphQL APIs to any frontend.  
  *Related Guide:* [Understanding Headless CMS: Decoupling Content from Presentation](/posts/understanding-headless-cms-decoupling-content-from-presentation/)

---

### I
- **Idempotency:** A property of an API operation where making multiple identical requests produces the exact same outcome as a single request, preventing duplicate charges, orders, or records during network retries.  
  *Related Guide:* [Idempotency in API Design: Safe Retries for Payments](/posts/idempotency-in-api-design-safe-retries-for-payments-and-critical-operations/)

---

### M
- **MACH Architecture:** An acronym standing for **Microservices**, **API-First**, **Cloud-Native SaaS**, and **Headless**, representing modern best-of-breed enterprise architecture.  
  *Related Guide:* [Welcome to MACH: The Composable Architecture Blueprint](/posts/welcome-to-mach/)
- **Microservices Granularity:** Sizing service boundaries according to business domain capabilities rather than technical layer splitting.  
  *Related Guide:* [Sizing Your Microservices: How to Find the Right Granularity](/posts/sizing-your-microservices-how-to-find-the-right-service-granularity/)

---

### O
- **OpenAPI Specification (OAS):** A standardized, vendor-neutral description format for REST APIs that enables automated documentation, SDK generation, and contract validation in CI/CD pipelines.  
  *Related Guide:* [The Role of OpenAPI in Contract-Driven Development](/posts/the-role-of-openapi-in-contract-driven-development/)
- **Observability & Tracing:** The ability to infer internal system states through distributed traces, RED metrics, and structured logs.  
  *Related Guide:* [Centralized Observability: Distributed Tracing & Metrics](/posts/centralized-observability-distributed-tracing-logging-and-metrics-for-microservices/)

---

### P
- **Progressive Web App (PWA) & Offline-First:** A modern web application paradigm utilizing Service Workers, Cache Storage, and client-side state synchronizers to provide seamless offline capabilities and instant loading.  
  *Related Guide:* [State Management y Offline-First en PWAs de Alto Tráfico](/posts/state-management-y-offline-first-en-progressive-web-apps-pwa-de-alto-trafico/)

---

### S
- **Saga Pattern:** A distributed transaction management pattern that coordinates multiple local transactions across microservices using a sequence of compensating actions to maintain data consistency without two-phase commit (2PC) locks.  
  *Related Guide:* [The Saga Pattern: Distributed Transactions Without 2PC](/posts/the-saga-pattern-managing-distributed-transactions-without-two-phase-commit/)
- **Service Mesh vs API Gateway:** Differentiating internal east-west service-to-service communication from north-south client-to-backend traffic management.  
  *Related Guide:* [Service Mesh vs API Gateway: Choosing the Right Tool](/posts/service-mesh-vs-api-gateway-choosing-the-right-tool-for-the-right-layer/)
- **Strangler Fig Pattern:** An incremental architectural migration pattern that progressively replaces specific pieces of a monolithic system with microservices until the legacy monolith is completely decommissioned.  
  *Related Guide:* [The Strangler Fig Pattern: Migrating a Monolith Without a Big Bang Rewrite](/posts/the-strangler-fig-pattern-migrating-a-monolith-without-a-big-bang-rewrite/)

---

### Z
- **Zero Trust Security:** A security model requiring strict identity verification, mutual TLS authentication, and least-privilege authorization for every service attempting to access network resources.  
  *Related Guide:* [Seguridad Zero Trust en Microservicios MACH](/posts/seguridad-zero-trust-microservicios-mach/)
