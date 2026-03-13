---
title: "High-Score (Bugfree Users) Uber India L5 Interview Experience: Trees, Grid Robots & Real-Time Eats Metrics"
seoTitle: "Uber India L5 (SSE) Interview Experience — Trees, Grid Robots & Real-Time Eats Metrics"
seoDescription: "High-score Uber India L5 interview: tree DSA, grid robots, real-time Eats metrics, LLD, and HM insights—detailed problems and practical tips."
datePublished: Fri Mar 13 2026 18:46:06 GMT+0000 (Coordinated Universal Time)
cuid: cmmp8zfqe000002jod8pvelq3
slug: uber-india-l5-interview-trees-grid-robots-realtime-eats
cover: https://hcti.io/v1/image/019ce884-1984-79a8-bcaa-a781f3721bb8
ogImage: https://hcti.io/v1/image/019ce884-1984-79a8-bcaa-a781f3721bb8

---

<p align="center">
  <img src="https://hcti.io/v1/image/019ce884-1984-79a8-bcaa-a781f3721bb8" alt="Uber India L5 Interview" style="max-width:800px; width:100%; height:auto;" />
</p>

# High-Score (Bugfree Users) Uber India L5 Interview Experience

This post summarizes a high-scoring loop for Uber India L5 (SSE) interviews shared by Bugfree users. The loop blends core DSA problems with system and low-level design, and a hiring-manager deep dive. Below you'll find clear problem descriptions, practical approaches, trade-offs, and interview tips.

## Interview Overview
Rounds covered:

- R1 — Trees with parent pointers: a race from root vs leaf and scoring based on arrival timing
- R2 — Grid robots: preprocess nearest blockers (L/T/B/R) to answer movement/match queries quickly
- R3 — System design: near real-time Uber Eats metrics (order value + Top-K items) for 1h/1d/1w windows
- R4 — Low-level design (LLD): meeting-room booking with history and scheduling constraints
- R5 — Hiring manager deep dive: architecture trade-offs, stack choices, and learnings

Each section below breaks the problem, a recommended approach, complexity, and interview tips.

---

## R1 — Tree with Parent Pointers: Root vs Leaf Race
Problem sketch

You’re given a tree where each node has a pointer to its parent (and possibly children). Two parties race starting from different positions (one from the root, another from a leaf). Points are awarded based on who arrives first to nodes — full points for faster arrival, half for ties, zero otherwise. Compute the maximum points possible given arrival times and movement rules.

Approach

- Clarify movement rules, time per edge, and scoring precisely first. Ask about whether movement is synchronous or asynchronous and how ties are handled.
- Convert parent pointers into an adjacency representation (or keep parent pointers and build child lists) so you can traverse up and down efficiently.
- Compute shortest arrival times from each start position to all nodes using BFS/DFS if edges are unweighted, or Dijkstra for weighted edges. With tree structure, simple DFS with distances works in O(N).
- For each node, compare arrival times and assign score: full/half/zero. Sum scores to get the total.
- If you need to maximize points by choosing an optimal starting leaf (or route), precompute distances from root to all nodes, and for each candidate start compute the aggregated score smartly using prefix/suffix or subtree contributions to avoid O(N^2).

Complexity

- Single-source distances on a tree: O(N).
- If evaluating many candidate starts, aim to reuse precomputed distance arrays and aggregate in O(N) per candidate; with heavy optimization you can reduce repeated work with DP.

Interview tips

- Always state assumptions and confirm edge cases (single-node tree, equal arrival times).
- Describe how you'd reuse computation if multiple queries (different starting leaves) are expected.
- Walk through a small example on the board.

---

## R2 — Grid Robots: Precompute Nearest Blockers (Left/Top/Bottom/Right)
Problem sketch

Robots move on a 2D grid. Each cell may contain obstacles. Queries ask about robot movement/stopping or matching multiple robots’ reachable cells. You need to respond quickly, so precompute nearest blocking cells in the four cardinal directions for each cell.

Approach

- Preprocessing:
  - For each row, scan left-to-right to compute nearest blocker to the left for every cell. Then right-to-left for nearest right blocker.
  - For each column, scan top-to-bottom for nearest top blocker, then bottom-to-top for nearest bottom blocker.
  - These four scans are linear: O(R*C) for an R x C grid.
- With nearest-blocker info per cell, you can answer range/movement queries in O(1): compute how far a robot can go in any direction without iterating per-cell.
- For more complex queries (multiple robots, collisions, or matching reachable sets):
  - Reduce to interval comparisons on rows/columns, or build union-find on free segments if connectivity queries are frequent.
  - Use sweep-line or two-pointer techniques to match robots/targets using the precomputed ranges.

Complexity

- Preprocessing: O(R*C)
- Query: O(1) or O(log N) depending on additional data structures (segment tree / interval tree) for aggregated queries.

Interview tips

- Explain why four directional scans suffice and why they’re linear.
- If asked to extend to dynamic obstacles, propose maintaining segment trees per row/column or spatial indexes and discuss update/query trade-offs.

---

## R3 — System Design: Near Real-Time Uber Eats Metrics
Problem sketch

Design a system to compute near real-time metrics for Uber Eats:

- Order value (sum, count, averages)
- Top-K items sold
- Rolling windows: 1 hour, 1 day, 1 week

Focus on latency/cost/correctness trade-offs for streaming metrics and Top-K queries.

High-level architecture

- Ingestion: user events (orders) stream into a durable message bus (Kafka or similar).
- Stream processing:
  - Use a streaming engine (Flink, Kafka Streams, or Beam) to compute windowed aggregates and approximate heavy hitters.
  - Use sliding-window or hopping-window logic with watermarks to account for late events.
- State and storage:
  - Maintain state in the stream processor (keyed state) and persist snapshots to durable storage (RocksDB + checkpoints).
  - Periodically write aggregates to a serving store (Cassandra, Redis, or ClickHouse) for fast reads.
- Serving layer:
  - Expose APIs that read precomputed aggregates and Top-K lists from the serving store. Use caches (Redis) for high QPS endpoints.

Top-K strategies

- Exact Top-K: maintain counts per item and compute top-K during each window boundary — accurate but expensive when cardinality is high.
- Approximate: use algorithms like SpaceSaving, Count-Min Sketch + Heavy-Hitters, or Frequent items to get memory-efficient, near-accurate Top-K with much lower cost.
- Hybrid: keep exact counts for hot items (cache) and approximate for the long tail.

Windowing and correctness

- Use event-time processing with watermarks to handle late-arriving data.
- Decide window semantics: tumbling vs sliding vs session windows. For 1h/1d/1w rolling windows, sliding windows or a combination of incremental aggregates usually works best.
- For correctness guarantees, decide between at-least-once and exactly-once semantics; exactly-once is preferred for monetary metrics but comes at complexity and cost.

Latency vs Cost trade-offs

- Lower latency: smaller processing intervals and materialize more frequent updates to the serving layer. Higher cost due to increased compute and state churn.
- Lower cost: increase batching, use approximation, downsample while accepting higher query latency or slight inaccuracy.

Scaling & optimization

- Partition streams by restaurant or region for parallelism.
- Use TTLs/compaction to evict old state for 1w windows (and pre-aggregate daily rollups to reduce history size).
- For Top-K with massive cardinality, use distributed heavy-hitter sketches and periodically merge results.

Monitoring & reliability

- Track latency percentiles end-to-end, correctness (sample-based cross-checks vs batch jobs), and backlog in Kafka.
- Build rollbacks and fallbacks: if real-time pipeline lags, fall back to last-known snapshot or batch-computed aggregates.

Interview tips

- Sketch architecture quickly, then dive into your chosen trade-offs: why Flink/Beam vs Spark Structured Streaming, why approximate Top-K, how to handle late data.
- Be explicit about operational concerns (monitoring, scaling, cost).

---

## R4 — Low-Level Design: Meeting Room Booking
Problem sketch

Design a meeting-room booking service that supports:

- Create/cancel bookings
- Conflict detection
- Booking history and query by time ranges
- Scheduling (one-off and recurring meetings)

MVP approach (what to implement fast in an interview)

- Define simple entities: Room, Booking (room_id, start_time, end_time, organizer_id, recurrence_info), User
- Core APIs:
  - POST /rooms/{id}/bookings — create booking
  - GET /rooms/{id}/availability?start=...&end=... — check availability
  - GET /users/{id}/bookings — booking history
- Data model:
  - Use a relational DB with an index on (room_id, start_time). Bookings table stores start/end and recurrence references.

Conflict detection algorithms

- For a single room: simple overlap check using a range query: exists booking where start < new_end && end > new_start.
- For many rooms and to find first available: maintain an interval tree or an availability calendar per room.

Concurrency and correctness

- Acquire a DB-level lock or use optimistic concurrency with transactional insert and uniqueness constraints.
- For high throughput, use advisory locks or an external lock service (Redis-based) to serialize bookings per room.

Recurring meetings

- Expand recurrence into discrete occurrences lazily: only materialize near-term occurrences (e.g., next 6 months) to avoid infinite expansion.
- Store recurrence rules (RFC 5545-style) and expand during availability checks or in a background job.

Interview tips

- Deliver a minimal working prototype: a clean Booking class, an overlap-check function, and a few unit tests.
- Focus on correctness for conflicts and clear API contracts.
- If asked to scale, discuss sharding rooms by region, caching availability, and how to handle cross-room searches.

---

## R5 — Hiring Manager Deep Dive: Trade-offs & Learnings
Topics typically discussed

- Trade-offs you made: consistency vs latency, exactness vs approximation, cost vs freshness.
- Stack choices: language/runtime (e.g., Java/Go for strong typing and performance), streaming tech (Flink/Kafka Streams), storage (ClickHouse for analytical reads, Redis for fast cache).
- Observability: what metrics, alerts, and dashboards you’d add (latency p50/p95/p99, error rate, backlog size, state size).
- Post-mortems and resilience: how you’d detect, mitigate, and roll back failures.

How to prepare

- Be ready to justify every major design decision and the alternatives you considered.
- Discuss concrete learnings from past systems (cost control, debugging production flakiness, migrating stateful streaming jobs).
- Show awareness of operational concerns: runbooks, SLOs, and on-call implications.

---

## Key Takeaways & Interview Tips

- Clarify requirements early, especially window semantics and tie-breaking rules.
- For DSA: precompute and reuse state; demonstrate correctness and complexity bounds.
- For grids: four-direction linear scans are powerful; consider dynamic variants and discuss updates.
- For system design: pick a clear architecture, then justify trade-offs (exact vs approximate, latency vs cost).
- For LLD: implement a minimal but correct core; show you can extend it to production concerns.
- For HM: be explicit about trade-offs, monitoring, and operational readiness.

Practice suggestions

- Implement small end-to-end streaming examples locally (Kafka + local Flink or Kafka Streams).
- Solve tree/grid problems on a whiteboard, then write a clean working version in your preferred language.
- Rehearse design explanations with time constraints: 10–15 minute sketches and 30–45 minute deep dives.

---

If you want, I can:

- Expand any round into a full walkthrough with code snippets (e.g., BFS/Dijkstra on the tree, the four-direction grid scan), or
- Provide a runnable skeleton for the meeting-room booking service (API + overlap check), or
- Draft a sample real-time metrics architecture diagram with component-level details.

Which would you like next?