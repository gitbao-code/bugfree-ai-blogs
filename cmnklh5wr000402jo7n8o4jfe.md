---
title: "Airline Reservation OOD: Stop Treating “Seat” as a Boolean"
seoTitle: "Airline Reservation OOD — Stop Modeling Seat Availability as a Boolean"
seoDescription: "Model seats as stateful entities (Available, Held, Booked). Use temporary holds with expiry to prevent double-booking and handle payment failures explicitly."
datePublished: Sat Apr 04 2026 17:16:40 GMT+0000 (Coordinated Universal Time)
cuid: cmnklh5wr000402jo7n8o4jfe
slug: airline-reservation-ood-stop-modeling-seat-availability-boolean
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775322980783.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775322980783.png

---

# Airline Reservation OOD: Stop Treating “Seat” as a Boolean

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775322980783.png" alt="Seat state diagram" style="max-width:800px;width:100%;height:auto;display:block;margin:0 auto;" />

In interviews and real-world systems alike, one of the most common design mistakes is modeling Seat.availability as a simple boolean (true/false). A seat is not just "free/busy" — it has distinct states, rules for transitions, and business constraints. Treating it as a boolean hides complexity and invites race conditions, double-bookings, and brittle failure handling.

Below is a concise, practical approach to model seat state and enforce safe transitions.

## Model seats as stateful entities

Instead of a boolean flag, model a Seat with an explicit status enum and related metadata:

- Status: Available, Held, Booked (optionally: Blocked, Maintenance, Pending)
- Hold records: who holds it, when the hold expires, hold id / session id
- Booking records: booking id, payment state, timestamps, audit trail

This gives you a cleaner domain model and makes it easy to reason about concurrency and failures.

## Typical state machine

- Available -> Held: user starts checkout; create a temporary Hold with an expiry
- Held -> Booked: payment confirms; atomically convert Hold to a Booking
- Held -> Available: hold expires or user cancels
- Booked -> Available: cancellation or refund flow (according to policy)

Enforce transitions through the Booking/Hold APIs rather than letting callers flip a boolean directly.

## Implementation notes (practical tips)

- Create an immutable Hold entity with: hold_id, seat_id, user_id/session_id, created_at, expires_at.
- When a user begins checkout, insert a Hold and mark seat as Held (or associate hold with seat). The hold should have a short TTL (e.g., 5–15 minutes).
- Use a single atomic DB transaction when confirming payment to convert the Hold into a Booking. The transaction should:
  - Verify the Hold is still valid (not expired and matches hold_id)
  - Create the Booking record
  - Clear the Hold
  - Update seat status to Booked
- If payment fails or the gateway is down, explicitly release the Hold (or let the expiry background job release it). Do not rely on eventual cleanup only.
- Expired holds: run a background job (cron/worker) to remove expired holds and return seats to Available. Emit events if needed.

## Concurrency and correctness

- Naive boolean checks lead to race conditions: two processes can read Available simultaneously and both attempt to book.
- Use one of these techniques depending on your scale and DB:
  - Optimistic concurrency control (version numbers / CAS) on the seat row and check the Hold id within a transaction.
  - Pessimistic locking (SELECT ... FOR UPDATE) for small-scale systems where contention is low.
  - Dedicated seat allocation service that serializes operations (actor/queue-based) for very high concurrency.
- Make booking confirmation idempotent: use an idempotency key so retries from the payment system don't create duplicate bookings.

## Failure handling and observability

- Make external failures explicit: if payment gateway is down, the flow should fail gracefully and the Hold should either be released or retried within a bounded window.
- Keep audit logs: who held the seat, when, why it was released or booked. This simplifies debugging and chargeback disputes.
- Expose metrics: hold rates, hold expirations, booking success rate, average time from hold->booked.

## Why this is better than a boolean

- Prevents double-booking under concurrency
- Makes business rules explicit (hold durations, cancellation rules)
- Simplifies failure handling and retries
- Provides a clearer audit trail and easier testing

## Example (pseudocode)

Transaction confirmBooking(holdId, paymentInfo):
  hold = SELECT * FROM holds WHERE id = holdId FOR UPDATE
  if not hold or hold.expires_at < now:
    throw HoldInvalid
  charge = PaymentGateway.charge(paymentInfo)
  if not charge.success:
    throw PaymentFailed
  INSERT INTO bookings (seat_id, user_id, ...) VALUES (...)
  DELETE FROM holds WHERE id = holdId
  UPDATE seats SET status = 'Booked' WHERE id = hold.seat_id
  COMMIT

This pattern keeps the critical path atomic and makes the edge cases explicit.

---

Model seats as a small state machine, not a boolean. It reduces bugs, clarifies behavior, and scales much better when concurrency and external failures are in play.
