---
title: 'Service Boundaries by Domain: Applying DDD Bounded Contexts to Microservices'
author: mach-playbook
date: '2026-04-04'
categories:
  - patterns
tags: ''
image:
  path: >-
    /assets/img/posts/2026-04-04-service-boundaries-by-domain-applying-ddd-bounded-contexts-to-microservices.png
---

The single most common reason microservices get messy is wrong service boundaries. Domain-Driven Design gives a principled method for drawing those lines — this post makes DDD practical for engineers who do not have time to read the blue book.

## The Bounded Context in Plain Language

A bounded context is a boundary within which a particular model is defined and applicable. Outside that boundary, the same word might mean something completely different. 'Order' in fulfillment is not 'Order' in billing.

## Mapping Business Capabilities to Service Candidates

Start with what the business does, not how the code is structured. Each business capability — pricing, inventory, fulfillment, identity — is a candidate for a service boundary. The organizational structure will confirm or reject each candidate.

## The Context Map

A context map identifies which bounded contexts exist and how they relate: upstream/downstream, shared kernel, customer/supplier, or conformist. This map is the most important diagram in a microservices architecture.

## Anti-Corruption Layer: Protecting Your Domain

When you integrate with a service that has a different model, an anti-corruption layer translates between the two. Without it, the external model leaks into your domain and your service loses its conceptual integrity.

## Worked Example: E-Commerce Order Domain

Consider an e-commerce platform. The order domain decomposes into: Cart (pre-purchase), Checkout (payment orchestration), Fulfillment (logistics), and Returns (post-purchase). Each has its own model of 'order' and its own lifecycle. Drawing boundaries here prevents the 50-field Order table that every team is afraid to touch.
