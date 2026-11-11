---
lang: en
layout: post
title: "The Strangler Fig Pattern: Migrating a Monolith Without a Big Bang Rewrite"
author: leninmeza
date: 2026-04-04 00:00:00 -0600
categories: [Architecture, Microservices]
tags: [architecture, devops, microservices]
image:
  path: /assets/img/posts/2026-04-04-the-strangler-fig-pattern-migrating-a-monolith-without-a-big-bang-rewrite.png
mermaid: true
---

Attempting a "Big Bang" rewrite of a critical enterprise monolithic system—where engineering freezes feature development for a year to rewrite the entire codebase from scratch—is one of the most high-risk maneuvers in software engineering. Statistics show that the majority of Big Bang rewrites exceed budget, suffer massive delays, or fail outright due to lost business logic edge cases.

Named by Martin Fowler after the Australian vine that gradually grows around a host tree until it completely replaces it, the **Strangler Fig Pattern** provides a low-risk, incremental strategy for migrating monolithic applications to microservices.

This article provides an end-to-end execution guide for applying the Strangler Fig pattern in cloud-native environments.

## The Strangler Fig Architecture Strategy

```
Phase 1: Intercept Routing                 Phase 2: Incremental Extraction           Phase 3: Complete Decommission
[ API Gateway / Proxy ]                    [ API Gateway / Proxy ]                   [ API Gateway / Proxy ]
       |                                          |            |                            |            |
       v                                          v            v                            v            v
+---------------+                          +----------+  +-------------+             +----------+  +-------------+
| Legacy        |                          | Legacy   |  | New Micro-  |             | New Svc  |  | New Svc B   |
| Monolith      |                          | Monolith |  | service A   |             | A        |  |             |
+---------------+                          +----------+  +-------------+             +----------+  +-------------+
                                                                                       (Monolith fully retired)
```

Rather than replacing the entire monolith at once, the Strangler Fig pattern intercepts incoming network requests using an API Gateway or Reverse Proxy. Features are extracted one domain at a time into independent microservices while the legacy monolith continues handling un-migrated paths.

## Step-by-Step Migration Execution Plan

### Step 1: Position an Intercepting Proxy / API Gateway
Insert a reverse proxy (e.g., NGINX, YARP, Kong, or AWS API Gateway) in front of the production environment. Initially, route 100% of incoming traffic directly to the legacy monolith.

```nginx
# Example NGINX Strangler Intercept Router
server {
    listen 80;
    server_name api.example.com;

    # Migrated endpoint: Routed to new microservice
    location /api/v1/orders {
        proxy_pass http://order-microservice.internal;
    }

    # Un-migrated legacy endpoints: Default fallback to monolith
    location / {
        proxy_pass http://legacy-monolith.internal;
    }
}
```

### Step 2: Select a High-Value, Low-Dependency Domain Context
Identify the first feature domain to extract. Choose a capability with clear business value, low database coupling, and moderate traffic (e.g., `Notification Service` or `Catalog Search Service`).

### Step 3: Implement the New Microservice & Data Sync Strategy
Build the new microservice with its own dedicated database. If the new service relies on data historically stored in the monolith's database, implement a dual-write sync strategy using Change Data Capture (CDC) tools like **Debezium** or Kafka event streams.

### Step 4: Shift Traffic Dynamically via Canary Routing
Update the API Gateway routing rules to direct a small percentage (e.g., 5%) of production traffic to the new microservice:
- Monitor error rates, system latency, and log output.
- Gradually increase traffic allocation to 100% as confidence grows.

### Step 5: Delete Legacy Code Paths in Monolith
Once 100% of traffic is successfully handled by the new microservice for 30 consecutive days, remove the legacy code path and database tables from the monolithic codebase. Repeat the process for the next domain context.

## Managing Data Migration Risks

Data migration is the hardest part of strangling a monolith. Follow these data safety rules:
1. **Never Share Databases**: Do not allow the new microservice to read directly from the legacy monolith database tables.
2. **Use CDC for Real-Time Sync**: Stream changes from the legacy database to the new microservice database using Debezium over Kafka so the new service always operates on up-to-date data during the transition period.
3. **Implement Feature Flags**: Wrap gateway routing changes in feature flags to enable instant rollback if unexpected issues occur in production.

## Conclusion

The Strangler Fig pattern mitigates risk by turning an overwhelming system overhaul into a series of small, verifiable deployments. By placing an intercepting proxy, extracting domains incrementally, and leveraging event-driven data sync, organizations modernize legacy systems continuously without halting business operations.


---

## Architectural Deep Dive: Envoy Traffic Shadowing & Dark Launch Strangling

The most reliable mechanism for executing a Strangler Fig migration without user-facing downtime is **Traffic Shadowing (Dark Launching)**. Using an edge proxy like Envoy or Cloudflare Workers, incoming live production traffic to legacy endpoints is simultaneously mirrored to the newly developed microservice.

The legacy monolith's response is returned to the user, while the new microservice's response, latency, and database persistence are evaluated asynchronously in the background.

```mermaid
flowchart TD
    Client["Client Request<br/>POST /api/checkout"] --> Proxy["Envoy Interceptor Proxy"]

    Proxy -->|Primary Live Call| Monolith["Legacy Monolith<br/>(Returns 200 OK to User)"]
    Monolith --> Client

    Proxy -.->|Shadow Copy (100% Asynchronous)| NewService["New Checkout Microservice<br/>(Canary Staging)"]
    NewService --> ComparisonEngine["Shadow Comparator Engine<br/>(Verifies Response Consistency)"]
```

### 1. Concrete Implementation: Envoy Traffic Shadowing Specification

The following Envoy / Istio `VirtualService` configuration mirrors 100% of production traffic from the legacy monolith to the new microservice:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: strangler-checkout-route
  namespace: production
spec:
  hosts:
    - api.machplaybook.com
  http:
    - match:
        - uri:
            prefix: /api/checkout
      route:
        - destination:
            host: legacy-monolith.production.svc.cluster.local
            port:
              number: 8080
          weight: 100
      # Asynchronously mirror real traffic to new microservice
      mirror:
        host: new-checkout-service.production.svc.cluster.local
        port:
          number: 8080
      mirrorPercentage:
        value: 100.0
```

---

## SRE Failure Modes & Production Troubleshooting Playbook

### Incident Scenario A: Shadow Traffic Mutating Legacy Production Storage (Write Leak)
* **Root Cause:** A shadowed POST request reached the new microservice, which was accidentally configured with connection credentials to the production database instead of a shadow/mock database, causing duplicate records.
* **Telemetry & Diagnostic Command:**
  ```bash
  # Check for shadow transaction headers in production database logs
  SELECT count(*) FROM orders WHERE user_agent LIKE '%Envoy-Shadow%';
  ```
* **Mitigation Protocol:**
  1. Enforce read-only or dry-run database credentials in shadowed canary environments.
  2. Implement an application-level header check (`X-Envoy-Decorated: shadow`) that skips database writes in mirrored pipelines.

### Incident Scenario B: Route Splitting Drift Causing Split-Brain Session State
* **Root Cause:** An edge routing rule migrated `/orders` to the new microservice while `/cart` remained on the legacy monolith. Session state was stored in legacy PHP cookies rather than centralized Redis, logging users out when viewing orders.
* **Telemetry & Diagnostic Command:**
  ```bash
  # Count HTTP 401 Unauthorized spikes on strangler cutover endpoints
  awk '$7 ~ /^\/orders/ && $9 == 401' /var/log/nginx/access.log | wc -l
  ```
* **Mitigation Protocol:**
  1. Externalize session management to a shared distributed Redis cluster before starting endpoint strangling.
  2. Implement a unified JWT authentication gateway that validates credentials upstream of both legacy and modern services.

---

## Architectural Trade-off Analysis: Strangler Migration Approaches

| Approach | Risk Profile | Rollback Speed | Operational Overhead | Infrastructure Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Big-Bang Rewrite** | Catastrophic (All or nothing) | Impossible (Months of work lost) | Low until launch | Low until launch |
| **Edge Proxy Strangler (Envoy)** | Minimal (Endpoint by endpoint) | Instantaneous (Change proxy rule)| Moderate (Dual infrastructure)| Moderate |
| **CDC Event-Driven Strangler** | Very Low (Asynchronous sync) | High | High (Debezium, Kafka sync) | High |

---

## Strangler Fig Production Migration Checklist

* [ ] Unified authentication gateway established upstream of both legacy and new services.
* [ ] Session storage externalized from legacy application memory into shared Redis.
* [ ] Traffic shadowing (dark launching) executed and compared with zero discrepancies.
* [ ] Automated database synchronization (CDC) active between legacy and modern databases.
* [ ] Granular instant rollback routing rules verified in edge reverse proxies.
