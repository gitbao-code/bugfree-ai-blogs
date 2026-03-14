---
title: "High-Score (Bugfree Users) Atlassian Principal Engineer Interview: LRU Cache, Web-Scraping System Design & Org-Tree LCA"
seoTitle: "Atlassian Principal Engineer Interview: LRU Cache, Web-Scraping Design & Org-Tree LCA"
seoDescription: "Firsthand 6-round Atlassian Principal Engineer interview recap: LRU cache, live-edit design, web-scraping pipeline, cinema scheduling, org-tree LCA, and lessons learned."
datePublished: Sat Mar 14 2026 01:17:06 GMT+0000 (Coordinated Universal Time)
cuid: cmmpmy9kz000002kzb7na01rk
slug: atlassian-principal-engineer-interview-lru-web-scraping-org-tree-lca
cover: https://hcti.io/v1/image/019ce9e9-5262-7870-9dc7-f53c95e772a0
ogImage: https://hcti.io/v1/image/019ce9e9-5262-7870-9dc7-f53c95e772a0

---

# High-Score Atlassian Principal Engineer Interview (Remote) — What Happened and What I Learned

<img src="https://hcti.io/v1/image/019ce9e9-5262-7870-9dc7-f53c95e772a0" alt="Interview cover" width="700" />

This is a concise, practical recap of a remote 6-round Atlassian Principal Engineer interview loop shared by Bugfree users. It covers what was asked, typical solution approaches, and actionable tips for each round. The loop included a phone screen, Values + Leadership Craft deep dives, System Design, Code Design, Data Structures, and the final outcome.

Summary of rounds:

- Phone screen: LRU cache approach + quick design prompts (Google Docs live-editing / WebSockets; file storage + search using object store + Elasticsearch).
- Values + Leadership Craft: behavioral deep dives.
- System Design: web-scraping pipeline with POST /jobs, status, and results APIs.
- Code Design: cinema scheduling — placing a new movie into a fixed day without removing existing shows.
- Data Structures: employee org-tree — find the "closest common parent" (LCA).
- Outcome: candidate was down-leveled after one weak round and ultimately declined the role.

---

## 1) Phone screen — LRU cache and quick design questions

What came up

- Implementing an LRU cache (approach and complexity)
- Quick architecture sketches:
  - Google Docs-style live editing + WebSockets
  - File storage + search using object store + Elasticsearch

Suggested approach & key points

- LRU cache:
  - Use a hashmap (key -> node) + doubly linked list of nodes ordered most-recent -> least-recent for O(1) get/put.
  - On get: move node to head; on put: if exists update and move to head, else insert at head and evict tail if capacity exceeded.
  - Watch for concurrency: mutexes/locks or lock striping; consider concurrent LRU variants (ConcurrentHashMap + a segmented list) or approximations like CLOCK for very high throughput.
  - Edge cases: null keys/values, updating existing entries, eviction callbacks.

- Google Docs conflict handling + WebSockets:
  - Two common approaches: Operational Transform (OT) or CRDTs for concurrent edits. Explain the trade-offs: OT needs a central server transformation layer; CRDTs allow more decentralization but can be heavier.
  - Use WebSockets (or WebRTC) for low-latency update stream; server reconciles and broadcasts operations.
  - Versioning, history, conflict resolution and undo stack are important topics to highlight.

- File storage + search (object store + Elasticsearch):
  - Store blobs and large files in an object store (S3 or compatible). Store metadata and small searchable fields in a database and index full text/metadata into Elasticsearch for search.
  - Consider indexing pipeline, metadata enrichment, access control, lifecycle (tiering), and backup/restore.

Interview tips

- State assumptions early (consistency, scale targets, throughput, latency).
- Talk about trade-offs (consistency vs availability, complexity vs maintainability).
- Sketch a concise architecture and call out bottlenecks and mitigations.

---

## 2) Values + Leadership Craft

What they probe

- Behavioral deep dives into leadership, decision-making, trade-offs, and how you drive engineering outcomes at scale.

How to prepare

- Use STAR (Situation, Task, Action, Result) or a similar framework but keep it conversational.
- Bring 3–5 strong stories: influencing without authority, shipping under constraints, technical strategy, hiring/mentoring, dealing with failure.
- Quantify impact where possible (reduced latency by X%, improved availability to Y%, saved $Z).

---

## 3) System Design — Web-scraping pipeline (POST /jobs, status, results)

Problem outline

Design a web-scraping pipeline that exposes APIs to submit scraping jobs (POST /jobs), check status, and retrieve results.

A robust architecture

- API layer: REST endpoints for POST /jobs, GET /jobs/{id}/status, GET /jobs/{id}/results.
- Queue: Jobs go into a durable queue (Kafka, SQS, RabbitMQ) to decouple request ingestion from workers.
- Worker fleet: Dedicated or autoscaled worker pool that pulls jobs off the queue and executes scraping tasks.
- Rate limiting & politeness: Domain-based rate limiting, per-target concurrency limits, robots.txt respecting, and backoff.
- Storage:
  - Raw results and large payloads -> object store (S3).
  - Parsed metadata and indexes -> database and Elasticsearch for searching results.
- Monitoring & observability: metrics (jobs/sec, success rate), logs, tracing, and alerting for errors.
- Retries & failure handling: exponential backoff, dead-letter queue for persistent failures, and idempotency keys to avoid duplicate processing.
- Security & isolation: sandbox scraping (containers or lambda-style functions), runtime limits (CPU, memory), and network egress controls.

APIs & data model

- POST /jobs { url, rules, schedule?, callback? }
  - Return job id and location for polling or a webhook/callback URL.
- GET /jobs/{id}/status -> queued|running|succeeded|failed
- GET /jobs/{id}/results -> pointer to object store (S3 URL) + parsed JSON or indexed search results

Scaling considerations

- Shard by domain to ensure politeness and balanced load.
- Use a central scheduler for recurring jobs and a worker autoscaler based on queue depth and processing latency.
- For millions of pages, use distributed crawling with checkpointing and deduplication.

Common pitfalls to call out

- Not handling politeness / rate limits per target domain.
- Hard-to-recover stateful workers; prefer stateless workers + checkpointing.
- Not planning for large result sizes (streaming, chunked upload to object store).

---

## 4) Code design — Cinema scheduling problem

Problem summary

Fit a new movie showing into a fixed day schedule without removing existing shows.

Practical approach

- Model existing shows as intervals sorted by start time.
- Walk the sorted list and check gaps between consecutive shows for one that can fit the new movie duration plus prep/cleanup buffer.
- Also check:
  - Gap before the first show (day start -> first start)
  - Gap after the last show (last end -> day end)
- Complexity: O(n) for scanning a sorted list; O(n log n) if you need to sort first.

Edge cases & additions

- Buffer times between shows (cleaning/prep).
- Multiple screens / auditoriums: treat each screen independently or run a packing algorithm across screens.
- Optimization goal variants: earliest slot, maximize revenue, or minimize audience disruption.

---

## 5) Data structures — Org-tree "closest common parent" (LCA)

Problem summary

Given an employee org-tree, find the lowest common ancestor (closest common parent) of two employees.

Solutions & trade-offs

- Naive upward-walk: Build a set of ancestors for one node, then walk up the other node's parents until you find a match. O(h) time and O(h) extra space (h = tree height).
- Binary lifting (preprocessing): Precompute 2^k ancestors for each node to answer LCA queries in O(log N) time and O(N log N) space. Good for many queries.
- Euler tour + RMQ: Flatten tree to Euler tour with depths; use RMQ for O(1) LCA after O(N log N) preprocessing. Good for extremely fast queries.

What to mention during interview

- Clarify whether the tree is static or dynamic (adds/moves change choice of algorithm).
- Talk about constraints (N, query count) to justify preprocessing costs.

---

## Outcome & lessons learned

- Outcome: The candidate was down-leveled because of one weaker round and ultimately declined the offer.

Takeaways

- A single weak round can significantly influence the final leveling even if other rounds go well. Aim for consistent performance.
- Preparation breadth matters for senior roles: expect both deep system design and leadership/communication proficiency.
- For system and code design rounds: state assumptions, outline alternatives, and explicitly call out trade-offs.

---

## Quick interview prep checklist

- LRU cache: be ready to diagram hashmap + doubly-linked list and mention concurrency implications.
- Live-edit systems: know OT vs CRDT basics and how WebSockets fit into low-latency architectures.
- Scraping systems: design for rate limiting, queues, worker autoscaling, and storage/indexing.
- Scheduling problems: think in terms of interval scanning and buffers.
- LCA: know naive and advanced (binary lifting / Euler tour + RMQ) solutions and when to use them.
- Behavior: prepare leadership stories with measurable impact.

---

If you'd like, I can expand any of the rounds into a longer walkthrough (example code for LRU, a full system design diagram for the scraper, or a sample LCA implementation). Happy to help you practice any of these rounds.

#SystemDesign #SoftwareEngineering #InterviewPrep
