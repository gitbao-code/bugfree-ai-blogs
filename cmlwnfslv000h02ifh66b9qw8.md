---
title: "Stop Double-Booking: The One Concurrency Detail Interviewers Actually Test"
seoTitle: "Stop Double-Booking: The Concurrency Detail Interviewers Test"
seoDescription: "Enforce concurrency at the DB boundary to prevent double-booking: transactions, row locks, or optimistic locking—the key detail interviewers test."
datePublished: Sat Feb 21 2026 18:25:24 GMT+0000 (Coordinated Universal Time)
cuid: cmlwnfslv000h02ifh66b9qw8
slug: stop-double-booking-db-concurrency
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771698299992.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771698299992.png

---

# Stop Double-Booking: The One Concurrency Detail Interviewers Actually Test

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771698299992.png" alt="Hotel booking concurrency diagram" width="640" style="max-width:100%; height:auto;">

In a hotel booking system, "prevent double-booking" is rarely a UI problem — it's a transactional one. If two users try to book the last room at the same time, a naive flow like:

1. Check availability
2. Insert booking

will race and allow an overbook.

Interviewers often don't need complex diagrams to test you — they want to know where you enforce correctness. The answer is: at the database boundary.

## The right approach (high level)

- Wrap "reserve room + create booking" inside a single database transaction.
- Lock the inventory row (or use optimistic locking with a version/timestamp field).
- Only commit if availability is still valid; otherwise roll back and return "sold out" or retry.

If you can't explain this, you aren't designing a booking system — you're describing a UI flow.

## Typical implementation patterns

### 1) Pessimistic locking (row lock)

Start a transaction, lock the inventory row, validate, update, insert booking, commit.

Pseudo-SQL:

```sql
BEGIN;
SELECT available_rooms FROM inventory WHERE room_id = 123 FOR UPDATE;
-- check available_rooms > 0
UPDATE inventory SET available_rooms = available_rooms - 1 WHERE room_id = 123;
INSERT INTO bookings (room_id, user_id, start_date, end_date) VALUES (...);
COMMIT;
```

Why this works: SELECT ... FOR UPDATE prevents another transaction from reading the same row for modification until you commit or rollback.

Trade-offs: simpler to reason about, but long transactions or heavy contention can cause blocking and deadlocks.

### 2) Optimistic locking (version field)

Read the row with a version number, perform business checks outside the DB, then attempt an update that includes the original version. If the update affects 0 rows, someone else changed the row — retry or fail.

Pseudo-SQL:

```sql
-- read
SELECT available_rooms, version FROM inventory WHERE room_id = 123;
-- do checks
UPDATE inventory
  SET available_rooms = available_rooms - 1, version = version + 1
  WHERE room_id = 123 AND version = <old_version> AND available_rooms > 0;
-- check rows affected == 1
INSERT INTO bookings ...;
```

Why this works: avoids long locks; better for high-concurrency workloads where conflicts are rare.

Trade-offs: needs retry logic and careful ordering so updates and inserts remain consistent.

### 3) Constraints and uniqueness

Sometimes you can rely on strong DB constraints to enforce invariants — e.g., a unique constraint on (room_id, date) for a single-room booking — and handle constraint-violation errors as "sold out." This is great when the domain maps to a uniqueness invariant.

### 4) Using a separate inventory service / queue

For massive scale you might:

- Introduce a dedicated inventory service that serializes reservations (single writer), or
- Use a reservation queue where an external worker commits bookings in order.

These patterns move the concurrency control out of your general DB transactions and into a service designed for high-throughput coordination.

## Common pitfalls

- Doing "check availability" in one transaction and then making the booking in another — this is racy.
- Long-running transactions hold locks and reduce throughput.
- Forgetting to handle retries or constraint-violation errors leads to poor UX.
- Relying on eventual consistency without a reservation window can still overbook.

## Interview tip

When asked "how do you prevent double-booking?" you should:

1. State clearly you enforce it at the DB boundary.
2. Explain either a pessimistic (FOR UPDATE) or optimistic (version) approach and why you chose it.
3. Mention trade-offs: throughput vs simplicity, deadlocks vs retries, and alternatives for extreme scale (reservation queues, inventory service).

That concrete, DB-focused answer is what interviewers expect.

## TL;DR

Prevent double-booking by enforcing concurrency at the database boundary: wrap reserve+create in a transaction, lock or version the inventory row, then commit only if availability holds. This is the one concurrency detail interviewers actually test.

#SystemDesign #BackendEngineering #Databases
