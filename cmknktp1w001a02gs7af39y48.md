---
title: "System Design Interviews: The Scalability + Reliability Checklist You Must Recite"
seoTitle: "System Design Interview Checklist: Master Scalability & Reliability"
seoDescription: "Memorize this system design checklist to clearly explain scalability, reliability, data, security, and validation during interviews."
datePublished: Wed Jan 21 2026 05:22:36 GMT+0000 (Coordinated Universal Time)
cuid: cmknktp1w001a02gs7af39y48
slug: system-design-interview-scalability-reliability-checklist
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768972930575.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768972930575.png

---

# System Design Interviews: The Scalability + Reliability Checklist You Must Recite

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768972930575.png" alt="System Design Checklist" style="max-width:800px; width:100%; height:auto; display:block; margin:12px 0;" />

In system design interviews you don't win by drawing boxes — you win by showing you can make, justify, and trade off practical decisions. Below is a compact, interview-ready checklist that helps you present a complete, balanced design focused on scalability and reliability.

Use this as a script: state assumptions, call out tradeoffs, and support choices with numbers where possible.

---

## 1) Requirements — lock them down first
- Clarify functional requirements (features, request patterns, critical flows).
- Quantify non-functional requirements: latency SLOs (e.g., p95 < 100ms), throughput (RPS), availability target (e.g., 99.95%), and growth projections (user growth, transaction growth per month/year).
- Ask about constraints: budget, regulatory, data residency, client SDKs, device types.
- Outcome: write a 1–2 line requirements statement and target numbers.

## 2) Architecture — high-level choices and data flow
- Choose a deployment model: monolith vs microservices. State pros/cons (speed of iteration vs team independence and operational overhead).
- Show a clear data flow: clients → API gateway/load balancer → services → data stores/queues → caches.
- Define communication patterns: synchronous (REST/gRPC) vs asynchronous (message queues, pub/sub). Explain why.
- Draw one clear path for the critical request and annotate failure modes and latency.

## 3) Scale — horizontal first, then optimizations
- Prefer horizontal scaling: stateless service instances behind a load balancer.
- Add caching (e.g., Redis) for hot reads; explain TTL and cache invalidation strategy.
- Use CDNs for static content and edge caching.
- When a single data partition is the bottleneck, shard/partition the dataset: pick shard key and explain tradeoffs (hot keys, rebalancing complexity).
- Use read replicas for read-heavy workloads; consider write scalability (leader/follower, multi-leader tradeoffs).

## 4) Reliability — eliminate single points of failure
- Remove SPOFs: multiple instances, multi-AZ or multi-region deployments for critical services.
- Replication and redundancy: DB replication factor, cross-region replication for DR.
- Automated failover and leader election (e.g., Raft, ZooKeeper, managed DB failover).
- Graceful degradation: prioritized functionality when degraded (serve cached responses, limit feature set).
- Resilience patterns: circuit breakers, retries with exponential backoff, bulkheads.

## 5) Observability — detect and respond quickly
- Instrument metrics: latency (p50/p95/p99), error rates, throughput, saturation (CPU/memory), queue lengths.
- Distributed tracing for request flow and root-cause analysis.
- Structured logs and correlation IDs.
- Alerts: define thresholds and pages (avoid noisy alerts). Use escalation policies and runbooks.

## 6) Data — consistency, durability, and lifecycle
- Choose a consistency model: strong vs eventual. Explain impact on user experience and latency.
- Data model and storage choices: relational vs NoSQL vs object store — justify by access patterns.
- Backups and recovery: RPO (how much data you can lose) and RTO (how quickly you must recover).
- Retention and GDPR/CCPA considerations: archival, deletion, and legal hold.

## 7) Security and compliance
- Authentication (AuthN) and authorization (AuthZ): tokens, OAuth2/OpenID Connect, RBAC or ABAC.
- Encrypt in transit (TLS) and at rest (KMS-managed keys).
- Secrets management, key rotation, and least privilege for services.
- Audit logs, breach detection, rate limiting, and input validation.

## 8) Validation — prove it works at scale and under failure
- Load testing tools: k6, JMeter, Locust; test target RPS and bottlenecks.
- Chaos and failover tests: simulate AZ/region outages, instance termination, network partitioning.
- Canary releases and progressive rollouts to catch regressions early.
- Measure and tune: profiling, database slow query analysis, and cache hit ratios.

---

## Quick interview script (recite this)
1. Clear requirements with numbers (latency, throughput, availability).
2. High-level architecture and data flow diagram.
3. Scaling plan: stateless services, caching, sharding when needed.
4. Reliability: redundancy, failover, graceful degradation.
5. Observability: metrics, tracing, alerts and runbooks.
6. Data decisions: consistency, backups, retention.
7. Security: authN/authZ, encryption, auditing.
8. Validation: load tests, chaos/failover tests.

---

Tips for delivery:
- Always state assumptions and tradeoffs explicitly.
- Use concrete numbers; if unknown, propose realistic targets and explain why.
- If asked for alternatives, show one or two options and the triggers for choosing them.

Memorize this checklist and use it to structure answers that are both practical and defensible.
