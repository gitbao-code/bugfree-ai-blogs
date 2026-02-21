---
title: "High-Score (Bugfree Users) Microsoft SDE Interview Experience: OA → DSA → System Design"
seoTitle: "Microsoft SDE Interview Experience: OA → DSA → System Design"
seoDescription: "Microsoft SDE interview walkthrough: OA, DSA, HLD/LLD rounds with problem breakdowns, schema tips, DP advice, and interview strategies."
datePublished: Sat Feb 21 2026 02:20:16 GMT+0000 (Coordinated Universal Time)
cuid: cmlvoyluu000302l4gwno125n
slug: microsoft-sde-interview-oa-dsa-system-design
cover: https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b
ogImage: https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b

---

<img src="https://hcti.io/v1/image/019c7dfd-c98e-766c-a60d-ff7385ab094b" alt="Interview Cover" style="max-width:800px; width:100%; height:auto;" />

# High-Score (Bugfree Users) Microsoft SDE Interview Experience: OA → DSA → System Design

A succinct, high-signal recap of a Microsoft SDE interview shared by Bugfree users. This covers the rounds, the exact problems encountered, approaches, design pointers, and actionable learnings you can apply to your prep.

## Candidate background
- Experience: 1.10 years
- Education: Tier-2 graduate

## Interview rounds (summary)
1. OA (Online Assessment)
   - Problems: Graph problem + HashMap problem
   - Focus: Correctness and reduction to known patterns

2. DSA (Onsite / Technical)
   - Problem 1: Two Sum — count unique pairs while handling duplicates
   - Problem 2: Delete and Earn — dynamic programming variant (House Robber style)

3. HLD + LLD (High-Level & Low-Level Design)
   - Notification service: brokers, scaling, fault tolerance, storage, ordering and delivery guarantees
   - Employee management DB schema: entities and relationships, constraints, and common queries

---

## Detailed problem notes & suggested approaches

### OA: Graph + HashMap problems
- Graph problem: clarify directed vs undirected, constraints (n, m), expected traversal (BFS/DFS) or shortest path (Dijkstra/Bellman-Ford). Draw small examples and verify edge cases.
- HashMap problem: likely frequency/counting or grouping. State expected time/space complexity.

Prep tip: when faced with graph/hashtable tasks, always mention expected complexity and choose appropriate representation (adj list for sparse graphs, adj matrix only for dense or small n).

### DSA problem 1 — Two Sum (unique pairs, handle duplicates)
Goal: Count unique value pairs (a, b) such that a + b = target, treating duplicate values carefully.

Two common approaches:
- Sorting + two pointers
  - Sort the array, use left/right pointers, skip duplicates when moving pointers to ensure unique pairs.
  - Time: O(n log n) for sort, O(n) two-pointer scan.
- HashMap counting
  - Build frequency map. For each value x, look for target - x. For x == target-x, combinations = nC2 from count.
  - Use seen-set to avoid double counting.
  - Time: O(n), Space: O(n).

Example pseudo steps (hashmap):
1. Count frequency of each number.
2. For each distinct x:
   - y = target - x
   - If x < y and y exists -> add 1 unique pair
   - If x == y and freq[x] > 1 -> add 1 unique pair

### DSA problem 2 — Delete and Earn (DP / House Robber style)
Observation: Deleting value v removes v-1 and v+1 opportunities. Transform problem into a House Robber on a value-indexed array.

Steps:
1. Compute sum[v] = v * freq[v] for all values present.
2. Sort distinct values or iterate from min to max value and treat missing values as 0.
3. Apply DP: dp[i] = max(dp[i-1], dp[i-2] + sum[i])

This reduces to classic robber DP where adjacent indices conflict. Time: O(maxValue) or O(k) for number of distinct values.

---

## HLD & LLD — Notification Service and Employee Management Schema

### Notification service — high-level requirements
- Deliver notifications to users with reasonable latency
- Support fan-out to many subscribers
- Provide persistence for at-least-once and optionally exactly-once delivery
- Handle ordering where required and support retries/deduplication
- Scalable: horizontally partition topics and consumers

Suggested components and patterns:
- API Gateway / Ingress -> Authentication & rate limiting
- Producer clients push messages to a message broker (e.g., Kafka, Pulsar)
- Brokers partition topics for scale. Use partition key (userId or topic) to achieve ordering per key.
- Consumer groups for processing; maintain offsets for consumer progress.
- Durable storage: brokers persist messages; also use a secondary persistent store (e.g., DB or object store) for long-term archival if needed.
- Delivery guarantees: implement deduplication tokens, idempotent consumers, and retry/backoff policies.
- Fan-out: for large fan-out operations, use async worker pool or specialized push services to handle per-device deliveries.
- Monitoring & fault tolerance: health checks, auto-rebalance for broker failures, and circuit breakers for downstream systems.

Important considerations to call out in interview:
- How you will partition topics for scale and preserve ordering
- What happens when a consumer is slow or down (backpressure, retention, dead-letter queues)
- How to ensure durability and recover from broker failures (replication, ISR, leader election)
- Cost vs latency trade-offs (in-memory caches for hot notifications)

### Employee management — LLD / DB schema (example)
Key entities:
- Employee (employee_id PK, first_name, last_name, email UNIQUE, phone, hire_date, manager_id FK -> Employee)
- Department (department_id PK, name, manager_id FK -> Employee)
- Role (role_id PK, title, permissions)
- EmployeeRole (emp_role_id PK, employee_id FK, role_id FK, start_date, end_date)
- EmploymentHistory (history_id PK, employee_id FK, from_date, to_date, title, department_id)

Notes:
- Use foreign keys for referential integrity. For large orgs, consider soft deletes and historical tables for audit.
- Index fields used frequently in queries (email, manager_id, department_id).
- If multi-tenancy or many employees, shard or partition large tables by company_id or region.

Sample query scenarios to mention:
- List direct reports for a manager
- Find current role and department for an employee
- Audit changes over time (use EmploymentHistory or CDC pipeline)

---

## Key learnings (from the candidate)
- Don’t skip dynamic programming — problems like Delete and Earn are classic DP transformations.
- LLD interviews expect practical schema modeling, not just design patterns. Be ready to sketch tables, constraints, and common queries.
- Keep reasoning out loud. Interviewers want to hear trade-offs and thought process — avoid rejecting yourself prematurely.

## Practical interview tips
- Clarify requirements and constraints up front (scale, consistency, latency, failure modes).
- For algorithm questions: state brute-force, optimize step-by-step, and analyze complexity.
- For DP problems: show how to convert the problem to a standard DP pattern (e.g., knapsack, robber, LIS).
- For design rounds: propose a simple design first, then iterate to add scaling, fault tolerance, and security.
- Communicate: narrate your assumptions, ask for feedback, and validate edge cases with small examples.

## Quick prep checklist
- Brush up on DP patterns and common transformations
- Practice hashmap and two-pointer patterns (handling duplicates)
- Read system design basics: message brokers, load balancing, caching, replication
- Practice LLD: schema design, relationships, indexing, and typical queries
- Do mock interviews and practice thinking out loud

## Resources
- LeetCode (Two Sum variants, Delete and Earn)
- System Design Primer (GitHub)
- Grokking the System Design Interview
- Distributed messaging docs: Kafka/Pulsar fundamentals

---

Good luck — focus on patterns, explain trade-offs, and practice communicating clearly. This candidate’s path shows that with ~1 year of experience and solid preparation you can navigate OA → DSA → HLD/LLD rounds successfully.

#SoftwareEngineering #SystemDesign #DataStructures
