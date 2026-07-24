---
lang: en
layout: post
title: "Sizing Your Microservices: How to Find the Right Service Granularity"
author: leninmeza
date: 2026-04-04 00:00:00 -0600
categories: [Architecture, Microservices]
tags: [microservices, architecture, service-granularity, ddd, refactoring]
image:
  path: /assets/img/posts/2026-04-04-sizing-your-microservices-how-to-find-the-right-service-granularity.png
---

One of the most frequent questions software architects face is: *"How big or small should a microservice be?"* 

Extremes in either direction create serious engineering problems. Creating services that are too large leads back to a monolithic codebase; creating services that are too small ("nano-services") results in extreme network latency, distributed transaction failure modes, and deployment complexity.

Finding the optimal service granularity requires balancing business domain boundaries, team organization, operational capabilities, and transactional integrity.

## The Granularity Spectrum: From Monolith to Nano-Service

```
[ Monolith ] ---------> [ Macro-Service ] ---------> [ Microservice ] ---------> [ Nano-Service ]
(Single Heap)          (Domain Context)            (Single Bounded)             (Single Function)
Low Network Cost       Balanced Latency            Optimal Autonomy             High Network Cost
Coarse Boundaries      Clear Boundaries            Resilient Scaling            Extreme Complexity
```

### 1. The Nano-Service Anti-Pattern
A **nano-service** is an over-decomposed service that encapsulates a trivial amount of logic (e.g., a service dedicated solely to formatting a date or calculating a single tax percentage).
- **Warning Signs**:
  - The service cannot fulfill a single business request without making 4+ blocking synchronous calls to sibling services.
  - Modifying a feature requires making pull requests across 5 different repositories simultaneously.
  - The line count of infrastructure config (Docker, Helm, CI/CD) exceeds the lines of business logic code.

### 2. The Macro-Service (Right-Sized Service)
A **macro-service** (or properly scoped microservice) encompasses a complete, coherent business capability bounded by a single Domain-Driven Design (DDD) Bounded Context.
- **Characteristics**:
  - Owns its data store exclusively.
  - Communicates asynchronously via domain events for non-critical paths.
  - Can be developed, tested, and deployed independently by a single two-seater engineering team.

## The Granularity Decision Matrix

To evaluate whether a service should be split or merged, analyze these four engineering dimensions:

| Dimension | Indicator to Split Service | Indicator to Merge / Keep Together |
| :--- | :--- | :--- |
| **Team Ownership** | Two separate engineering teams are making concurrent edits to the same codebase. | A single developer or small team manages both components easily. |
| **Scalability Profiles** | Component A requires 100x CPU scaling (e.g., image rendering) while Component B is low-traffic CRUD. | Both components share similar CPU, memory, and scaling metrics. |
| **Data Dependencies** | Components operate on completely disjoint database tables with zero joins. | Components require ACID database transactions and frequent immediate consistency. |
| **Release Cadence** | Component A requires daily deployments while Component B is updated quarterly. | Both components are tested and released together on the same schedule. |

## Practical Heuristics for Granularity

### Heuristic 1: The Two-Shirt Rule (Team Boundaries)
Align service boundaries with Conway's Law: *"Organizations design systems that mirror their communication structures."* A service should be small enough to be owned comfortably by a single small team (4–7 engineers), but large enough that the team does not have to manage 20 separate repositories.

### Heuristic 2: The Single Database Owner Rule
If Service A directly queries or writes to Service B's database tables, your services are incorrectly sized. Merge them into a single service or refactor them to communicate strictly through public APIs and domain events.

### Heuristic 3: Transaction Boundary Heuristic
If a business transaction requires immediate ACID consistency across three operations, those operations belong inside the same service boundary. If eventual consistency is acceptable, split them and coordinate via the Saga pattern.

## Conclusion

Right-sizing microservices is an iterative architectural process, not a one-time decision. When starting new projects, prefer coarser service boundaries (macro-services). It is significantly easier to split a well-structured macro-service later than it is to untangle dozens of tightly coupled nano-services.
