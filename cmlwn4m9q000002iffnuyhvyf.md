---
title: "Inventory Design Interview: Stop Storing Stock as a Simple Number"
seoTitle: "Inventory Design Interview: Model Inventory with Immutable Transactions"
seoDescription: "Model inventory as an append-only ledger of immutable transactions. Cache stockLevel for reads, but derive truth from the ledger for auditability and safety."
datePublished: Sat Feb 21 2026 18:16:43 GMT+0000 (Coordinated Universal Time)
cuid: cmlwn4m9q000002iffnuyhvyf
slug: inventory-design-interview-stop-storing-stock-as-a-number
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771697772827.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771697772827.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771697772827.png" alt="Inventory ledger diagram" width="800" style="max-width:100%; height:auto;" />

# Inventory Design Interview: Stop Storing Stock as a Simple Number

In e-commerce inventory design, treat the inventory ledger — not a single numeric field — as the source of truth. Instead of relying on a mutable `stockLevel` field, model every change as an immutable `InventoryTransaction` (Add / Remove / Return / Reserve). Derive the current stock from the transaction ledger. This simple mental shift gives you auditability, safer debugging, and robust handling of returns, cancellations, and edge cases.

Why this matters

- Auditability: an append-only ledger records who changed inventory, why, and when. You can answer: "When was the stock adjusted? By whom? For which order?"
- Reproducibility: you can rebuild stock state from the ledger at any time — useful after bugs, migrations, or for analytics.
- Safer debugging: instead of guessing what mutated `stockLevel`, you inspect transactions to trace the cause.
- Correct business semantics: returns, cancellations, reservations, and compensations are explicit transactions, not ad-hoc decrements/increments.
- Concurrency & consistency: when designed correctly, the pattern makes reasoning about races and compensating actions clearer.

Core model

Store immutable transactions with fields similar to:

```sql
InventoryTransaction {
  id            : uuid,
  product_id    : uuid,
  delta         : integer,   -- + for add/return, - for remove/sale
  type          : enum(ADD, REMOVE, RETURN, RESERVE, RELEASE),
  reason        : string,     -- e.g. orderId or returnId
  created_by    : uuid,       -- user/service id
  created_at    : timestamp
}
```

The current stock can be derived as:

```
stock = SUM(delta) WHERE product_id = X
```

Caching for performance

Computing SUM(delta) on the fly can be expensive. Keep a `stockLevel` as a cache for fast reads, but do not treat it as the authoritative source. Always append an `InventoryTransaction` first and update the cached `stockLevel` in the same atomic operation.

Recommended approaches:

- Database transaction: append the transaction row and update the stock cache in a single DB transaction so they stay in sync.
- Optimistic concurrency: store a version number on the cached row and use CAS/optimistic locking when updating, retrying on conflict.
- Event-sourcing / CQRS: emit an immutable inventory event to an event log, then materialize read models; provide reconciliation jobs to repair divergence.

Reservations vs. committed stock

Don’t conflate reservation (holding stock for a pending checkout) with committed sale. Model reservations explicitly as transactions (RESERVE/RELEASE) or as a separate ledger. This avoids accidental overselling and makes TTL or expiration handling explicit.

Handling idempotency and retries

Make transaction creation idempotent by using stable request IDs (e.g. order id + line id) or unique constraints so duplicate requests don’t create duplicate deltas. This is crucial for network retries and webhook replays.

Concurrency patterns

- Single DB row locking (SELECT ... FOR UPDATE) can be simple and correct for moderate scale.
- Optimistic updates with retries scale better in high-concurrency scenarios.
- Partitioning by product (or product shard) and routing requests avoids cross-shard contention.

What to say in an interview

Keep the message clear and concise. Example phrasing:

"I treat inventory as an append-only ledger of immutable InventoryTransactions. The ledger is the source of truth; `stockLevel` is a cached read model updated atomically alongside each transaction. This gives us a full audit trail, easier debugging, explicit handling of returns/reservations, and the ability to rebuild state if needed. For correctness I either update the transaction and cache in a DB transaction, or use an event-sourced pattern with reconciliation and idempotency guarantees." 

Quick checklist to mention if asked follow-ups:

- Show the transaction schema and examples (ADD, REMOVE, RETURN, RESERVE).
- Explain atomic update strategy (DB transaction, optimistic lock, or event sourcing + materializer).
- Discuss reservations vs committed stock and TTL for holds.
- Describe idempotency keys to avoid duplicate deltas.
- Mention reconciliation jobs to repair any divergence between ledger and cached read model.

Summary

Stop treating `stockLevel` as the source of truth. Model every inventory change as a transaction in an append-only ledger, derive current quantities from that ledger, and maintain `stockLevel` only as a cached, performant read model updated atomically. This approach improves auditability, correctness, and maintainability — and it's a strong, interview-ready design decision.

#SystemDesign #OOP #SoftwareEngineering