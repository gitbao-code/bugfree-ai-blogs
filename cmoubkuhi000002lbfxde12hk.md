---
title: "Collaborative Spreadsheets: Why Optimistic Concurrency Beats Locking in Interviews"
seoTitle: "Optimistic Concurrency vs Locking for Collaborative Spreadsheets — Interview Guide"
seoDescription: "Why optimistic concurrency beats locking in collaborative spreadsheets: low latency, no deadlocks, with clear conflict-handling strategies (LWW, OT/CRDT)."
datePublished: Wed May 06 2026 17:16:59 GMT+0000 (Coordinated Universal Time)
cuid: cmoubkuhi000002lbfxde12hk
slug: optimistic-concurrency-vs-locking-collaborative-spreadsheets
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778087783825.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778087783825.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778087783825.png" alt="Collaborative spreadsheet" style="max-width:800px;width:100%;height:auto;margin-bottom:16px;" />

# Collaborative Spreadsheets: Why Optimistic Concurrency Beats Locking in Interviews

Building a collaborative spreadsheet isn’t primarily about streaming realtime updates — it’s about correctness when multiple users edit the same data simultaneously. In interviews, the simplest clear correctness story often wins. Optimistic concurrency gives you that story with low latency and fewer system-level complications than locking.

## The core idea

- Accept client edits locally and send them to the server without acquiring global locks.
- Attach a version identifier (or timestamp) to each cell or update.
- On write, the server compares the client's base version against the current version.
  - If the base version matches, accept and increment the version.
  - If it’s stale, either reject and surface a conflict to the client or try a deterministic merge.

This approach keeps latency low (no waiting on locks), avoids deadlocks, and forces you to define a clear conflict policy — exactly the kind of principled trade-off interviewers expect.

## Conflict-handling strategies (short and practical)

- Reject + UI merge: Server rejects and returns the newer value and metadata; client shows a diff and asks the user to pick/merge.
- Last-Write-Wins (LWW): For simple value cells, accept the latest timestamped write. Cheap but may lose edits.
- Merge rules: For structured cells (numbers, formulas) define deterministic merge rules (e.g., sum deltas, pick max).
- OT / CRDT: For rich collaborative operations (text, formulas with ranges), mention Operational Transformation or CRDTs — they provide automatic convergent merges but add complexity.

## Simple server-side protocol (pseudo)

1. Client reads cell -> receives value + version.
2. Client edits and submits {cellId, baseVersion, newValue}.
3. Server reads currentVersion:
   - if baseVersion == currentVersion: accept, store newValue, currentVersion++ and broadcast.
   - else: conflict -> either reject with current value or apply merge policy.

Example (JSON payload):

{
  "cellId": "A1",
  "baseVersion": 42,
  "newValue": "100"
}

Response when stale:

{
  "status": "conflict",
  "currentValue": "95",
  "currentVersion": 43
}

## Why this is interview-friendly

- Correctness story: You can clearly explain how conflicts are detected and handled (server compares versions and applies a rule).
- Trade-offs: You can justify low-latency optimistic approach vs. heavy-handed locks and discuss where locking might be appropriate (multi-step transactions or when strong invariants must be enforced).
- Scalability & availability: Optimistic approaches compose well with sharding and eventual consistency models — mention LWW, OT/CRDT when appropriate.

## When might locking be appropriate?

- If operations require atomic multi-cell invariants (e.g., balance transfers that must not be concurrent), a transaction or short-lived lock may be necessary.
- Prefer coarse-grained, short locks only when you must enforce strict serializability. For per-cell edits, optimistic approaches usually suffice.

## Interview talking points (concise)

- Explain your protocol: versioned writes + conflict detection on the server.
- Present a conflict policy and why you chose it (LWW for simplicity, OT/CRDT for rich editing).
- Discuss UX: how you surface conflicts to users and when to auto-merge vs. ask.
- Mention system concerns: broadcast via WebSockets, per-cell version counters, sharding keys, and eventually consistent replication.

## Bottom line

Optimistic concurrency gives you a low-latency, deadlock-free design with a clear, testable correctness story. In interviews, that clarity, plus thoughtful trade-offs and a conflict-resolution plan, is far more convincing than proposing a heavy locking system.

#SystemDesign #DistributedSystems #WebSockets
