---
title: 'When NOT to Use Microservices: A Decision Framework'
author: mach-playbook
date: '2026-04-04'
categories:
  - guides
tags: ''
image:
  path: >-
    /assets/img/posts/2026-04-04-when-not-to-use-microservices-a-decision-framework.png
---

The honest counterweight to MACH advocacy. Microservices are not a default — they are a trade-off. This post gives a concrete framework for deciding when a modular monolith is the right call.

## The Cost Nobody Talks About in Conference Talks

Network latency, distributed debugging, data consistency across boundaries, operational overhead per service, and the cognitive load on every engineer who has to understand how 40 services interact.

## Team Size as a Primary Input: Conway's Law in Practice

If you have fewer teams than you have services, someone is responsible for multiple services and you have lost the autonomy benefit that justified the move. Conway's Law is not optional.

## The Maturity Checklist

Before adopting microservices, verify: Do you have CI/CD for every service? Centralized logging and tracing? A defined on-call rotation? If the answer to any of these is no, microservices will amplify your pain, not reduce it.

## The Modular Monolith: Not a Consolation Prize

A well-structured modular monolith with clear internal boundaries is a legitimate architecture — and for most teams, a better starting point than microservices. You can always extract services later when the team and domain complexity justify it.
