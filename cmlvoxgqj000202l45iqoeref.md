---
title: "Microsoft SDE Interview Experience — OA → DSA → System Design (High Score)"
seoTitle: "Microsoft SDE Interview Experience — OA, DSA & System Design (1.1 yrs)"
seoDescription: "Walkthrough of a Microsoft SDE interview: OA (graph/hash), DSA (Two Sum variant, Delete & Earn), and HLD+LLD tips from a 1.1yr candidate."
datePublished: Sat Feb 21 2026 02:19:22 GMT+0000 (Coordinated Universal Time)
cuid: cmlvoxgqj000202l45iqoeref
slug: microsoft-sde-interview-experience-oa-dsa-system-design
cover: https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b
ogImage: https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b

---

# Microsoft SDE Interview Experience — OA → DSA → System Design

<img src="https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b" alt="Interview cover" style="max-width:700px; width:100%; height:auto;" />

A concise, high-score interview walkthrough shared by a Bugfree community user. This candidate had ~1.1 years of experience and graduated from a tier-2 college. The interview flow included an online assessment (OA), a DSA round, and a combined high-level + low-level design round.

---

## Background
- Experience: ~1.1 years
- Education: Tier‑2 college
- Outcome: Strong performance across rounds

---

## Round-by-round breakdown

### 1) Online Assessment (OA)
- Topics: Graph problem and a HashMap problem.
- Tip: For OA, focus on correctness first, then optimize. Practice common graph patterns (BFS/DFS, shortest-path, connected components) and hashing-based counting/lookups.

### 2) DSA (Coding) Round
Problems asked:
- Two Sum variant: count unique pairs — must handle duplicates correctly.
  - Approach: Sort + two pointers or use a hashmap with careful duplicate handling (e.g., store seen numbers and ensure pairs counted once).
- Delete and Earn (Leetcode-style): DP problem reducible to House Robber pattern.
  - Approach: Aggregate points per value into an array keyed by number, then run the House Robber DP that decides to take or skip each value.

Tips for DSA:
- Read constraints first (n, value ranges) to decide between sorting, hashing, or DP.
- For duplicate-sensitive pair problems, explicitly reason about how you deduplicate (set/hash) or sweep in sorted order.
- For DP problems, write the recurrence and base cases before coding. If you map the problem to a known pattern (like House Robber), mention that aloud.

### 3) HLD + LLD (High-level + Low-level Design)
Two components covered:

1. Notification Service
- Discussed requirements: brokers, scaling, fault tolerance, storage and delivery guarantees.
- Key design decisions to cover:
  - Architecture: producer → broker(s) → consumer(s)
  - Broker choices and tradeoffs (e.g., Kafka vs RabbitMQ): throughput vs ordering vs persistence
  - Partitioning and consumer groups for scale
  - Persistence/retention strategy and when to use durable storage vs ephemeral
  - Failure modes and recovery (replication, leader election, retries, dead-letter queues)
  - Delivery semantics: at-most-once, at-least-once, exactly-once (and when each is appropriate)

2. Employee Management DB Schema (LLD / schema modeling)
- Entities and relations to think about: Employee, Department, Role, Manager (self-relation), Employment history, Access control/permissions.
- Normalization vs denormalization tradeoffs depending on read/write patterns.
- Indexing strategies for common queries (by employee_id, department_id, manager_id).

Tips for HLD/LLD:
- LLD is not only design patterns — you must model the schema, entities and relationships when asked.
- Talk through scale assumptions (QPS, data volume, retention) — they guide storage and partitioning choices.
- Draw clear component boundaries and mention operational concerns (monitoring, alerts, backups).

---

## Key learnings & interview advice
- Don’t skip Dynamic Programming: it's commonly evaluated; know base patterns (0/1 knapsack, house robber, LIS, etc.).
- LLD includes schema modeling: be ready to define entities, relations and indexes — not just class diagrams or patterns.
- Vocalize your thoughts: explain tradeoffs, assumptions and next steps. Interviewers want to hear your reasoning — don’t self-reject early.
- Clarify requirements and constraints before diving into design or code.

---

## Quick prep checklist
- Practice 100–200 problems covering hashing, two pointers, graph traversal, and DP patterns.
- Revisit design patterns for distributed systems (pub/sub, load balancing, sharding, replication).
- Practice schema design: model common business problems and justify indices and normalization.
- Mock interviews: focus on communicating assumptions and walking through solutions step-by-step.

---

If you’re prepping for Microsoft SDE or similar interviews, concentrate on these core areas and practice explaining your choices clearly. Good luck!

#SoftwareEngineering #SystemDesign #DataStructures
