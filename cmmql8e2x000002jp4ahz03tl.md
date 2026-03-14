---
title: "Real-Time Scores: Event Ordering Per Game Is Non‑Negotiable"
seoTitle: "Real-Time Scores: Enforce Per-Game Event Ordering for Accurate Stats"
seoDescription: "Guarantee accurate real-time sports scores by enforcing per-game event ordering, idempotency, and persisting event logs before updating derived state."
datePublished: Sat Mar 14 2026 17:16:45 GMT+0000 (Coordinated Universal Time)
cuid: cmmql8e2x000002jp4ahz03tl
slug: real-time-scores-event-ordering-per-game
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773508568057.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773508568057.png

---

# Real-Time Scores: Event Ordering Per Game Is Non‑Negotiable

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773508568057.png" alt="Diagram: event ordering per game" width="640">

In any real-time sports scoring system, the single most critical — and often overlooked — requirement is strict event ordering per game. If a "goal at 60:00" is processed after a "red card at 61:00", the timeline, player stats, leaderboards, and fan notifications can all become inconsistent.

This isn't a UI problem or a flaky clock problem; it's an architectural requirement. Below is a concise, practical guide to designing systems that keep timelines correct and metrics reliable.

## The problem, in one sentence
Out-of-order events lead to incorrect aggregates, double counts, wrong notifications, and mistrust. Timestamps alone are not enough — processing order matters.

## Core principles
- Partition by game_id: Ensure all events for the same game are routed to the same ordered stream (topic partition or equivalent).
- Sequential processing per partition: Consume and apply events in the partition's order.
- Idempotency: Make handlers safe to run multiple times (use event_id as the dedupe key).
- Persist the event log first: Write the raw event to durable storage before updating derived state (score, PlayerStats, cache).

## Recommended architecture
1. Ingest events into a partitioned streaming system (e.g., Kafka) using game_id as the partition key. This guarantees per-game ordering within a partition.
2. Have a consumer group where each consumer processes one or more partitions sequentially.
3. For each event:
   - Persist the raw event to an append-only event store (or commit the offset only after durable write).
   - Deduplicate using event_id (a unique event identifier) to ensure idempotency.
   - Apply the event to aggregates (score, player stats) and update caches/state stores.
   - Emit derived events/notifications after state is updated.

This sequence (persist raw event → dedupe → update derived state → notify) preserves correctness across retries and failures.

## Practical patterns and details
- Partitioning: Use game_id as the partition key. If a game has too much throughput, shard by game_id + shard_id but still maintain ordering within each shard.
- Exactly-once vs at-least-once: Exactly-once semantics help but are often complex. A simpler, reliable approach is at-least-once processing + idempotent handlers + durable event logging.
- Deduplication store: Keep a compact dedupe index (e.g., Redis, RocksDB, or a local state store) keyed by event_id with TTL if appropriate.
- Commit strategy: Only commit the stream offset after the event is durably persisted and applied. This prevents data loss and reduces risk of reprocessing without dedupe.
- Derived state persistence: Use transactional updates where possible (e.g., write-ahead log + atomic update to aggregates) to avoid partial updates.
- UI ordering: Drive the UI from the same event log or from the derived state that was built from the ordered stream. Do not rely solely on client-side sorting by timestamp.

## Example pseudocode

```pseudo
for event in partitioned_stream(partition=game_id_partition):
  if dedupe_store.contains(event.event_id):
    continue

  persist_raw_event(event)           # durable append
  dedupe_store.add(event.event_id)

  apply_event_to_aggregates(event)   # update score, player stats
  update_cache_or_state_store()

  emit_notifications(event)
  commit_stream_offset(event)
```

## Failure and recovery
- On consumer crash, the consumer restarts and resumes from the last committed offset. Because events were persisted and handlers are idempotent, reprocessing is safe.
- For long-running reprocesses (e.g., backfills), replay from the event log to rebuild derived state deterministically.

## Interview-ready one-liner
"To guarantee correct real-time scores, partition the stream by game_id to preserve per-game order, make handlers idempotent using event_id, and always persist the raw event before updating derived state — ordering plus idempotency prevents double counts and out-of-order UIs." 

## Quick checklist
- [ ] Partition events by game_id
- [ ] Process each partition sequentially
- [ ] Persist raw event before state changes
- [ ] Use event_id for dedupe (idempotency)
- [ ] Commit offsets only after durable writes
- [ ] Drive UI from the event-derived state or event log

Keeping ordering and idempotency at the heart of your architecture makes real-time scoring robust, auditable, and easy to reason about — and it’s exactly what interviewers want to hear.
