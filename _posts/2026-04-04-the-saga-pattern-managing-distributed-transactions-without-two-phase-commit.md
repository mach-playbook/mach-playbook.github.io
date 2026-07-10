---
title: 'The Saga Pattern: Managing Distributed Transactions Without Two-Phase Commit'
author: mach-playbook
date: '2026-04-04'
categories:
  - patterns
tags: ''
image:
  path: >-
    /assets/img/posts/2026-04-04-the-saga-pattern-managing-distributed-transactions-without-two-phase-commit.png
---

ACID transactions do not cross service boundaries. The Saga pattern is the standard answer — but most explanations skip the hard parts: failure compensation, idempotency, and event ordering.

## Why Distributed Transactions Are a MACH Anti-Pattern

Two-phase commit requires tight coupling and a central coordinator — the opposite of what MACH architectures aim for. Sagas achieve eventual consistency without sacrificing service autonomy.

## Choreography vs. Orchestration

**Choreography:** Each service listens for events and reacts independently. Simple to start, hard to debug at scale. **Orchestration:** A central coordinator directs the flow. Easier to reason about, but the orchestrator can become a bottleneck.

## A Checkout Flow Modeled as a Saga

Step 1: Reserve inventory. Step 2: Charge payment. Step 3: Confirm order. If payment fails, compensate by releasing the inventory reservation. Each step is idempotent and each compensation is its own atomic operation.

## Idempotency Keys: Making Retries Safe

Every saga step must be idempotent — executing it twice produces the same result. This is typically achieved through idempotency keys: unique identifiers that let the receiving service detect and deduplicate repeated requests.
