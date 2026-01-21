---
title: "Ride-Sharing OOD: Stop Treating RideRequest as a “Simple DTO”"
seoTitle: "Ride-Sharing OOD: Treat RideRequest as a Stateful Entity"
seoDescription: "Model RideRequest as a stateful entity with enforced lifecycle transitions to prevent impossible states and express real OOD invariants."
datePublished: Wed Jan 21 2026 18:16:28 GMT+0000 (Coordinated Universal Time)
cuid: cmkocgw09000302l1dprw4r75
slug: ride-sharing-ood-stop-treating-riderequest-as-a-simple-dto
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769019365511.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769019365511.png

---

# Ride-Sharing OOD: Stop Treating RideRequest as a “Simple DTO”

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769019365511.png" alt="RideRequest lifecycle" style="max-width:700px; width:100%; height:auto; display:block; margin:0 auto;" />

In ride-sharing systems, the RideRequest isn't just a lightweight payload passed between services — it's the backbone of the domain. Treating it as a plain Data Transfer Object (DTO) leads to scattered rules, fragile code, and impossible states. Instead, model RideRequest as a stateful domain entity with a strict lifecycle and operations that enforce invariants.

## The core idea

Give RideRequest a small, explicit state machine and encapsulate state transitions behind methods. A canonical lifecycle looks like:

PENDING → ACCEPTED → COMPLETED

and from PENDING you can also go to:

PENDING → CANCELLED

Make these transitions explicit in methods such as accept(), cancel(), and complete(). Each method should validate the current state and any required preconditions (e.g., payment or driver assignment) before changing state.

## Why this matters

- Prevents impossible combinations (e.g., COMPLETED but unpaid, or CANCELLED after COMPLETED).
- Centralizes business rules and invariants, making the system easier to reason about and test.
- Makes concurrency and recovery semantics clearer (you can decide how to handle duplicate accept/cancel requests).
- Shows true object-oriented design (invariants and behavior), not just structure.

Interviewers care about these aspects: invariants, correctness under concurrent operations, and clear ownership of rules.

## Minimal example (pseudocode)

```java
enum State { PENDING, ACCEPTED, COMPLETED, CANCELLED }

class RideRequest {
  State state = State.PENDING;
  boolean paid = false;

  synchronized void accept(Driver driver) {
    if (state != State.PENDING) throw new IllegalStateException("Can only accept from PENDING");
    if (driver == null) throw new IllegalArgumentException("Driver required");
    // assign driver, notify parties...
    state = State.ACCEPTED;
  }

  synchronized void complete() {
    if (state != State.ACCEPTED) throw new IllegalStateException("Can only complete from ACCEPTED");
    if (!paid) throw new IllegalStateException("Cannot complete unpaid ride");
    // finalize metrics, receipts...
    state = State.COMPLETED;
  }

  synchronized void cancel() {
    if (state == State.COMPLETED) throw new IllegalStateException("Cannot cancel a completed ride");
    // side effects, refunds if applicable...
    state = State.CANCELLED;
  }

  void markPaid() { paid = true; }
}
```

Notes:
- Use synchronization or optimistic locking when persisting to handle concurrent requests (e.g., two drivers accepting at once).
- Consider idempotency for external commands (accept request retries) to avoid duplicate side effects.

## Beyond the basics

- Aggregate root: In a DDD context, RideRequest can be an aggregate root that owns related entities (driver assignment, fare, payment status).
- Event sourcing: Model transitions as domain events (RideAccepted, RideCompleted) to get an audit trail and easier recovery.
- Validation boundaries: Keep cross-aggregate validations (e.g., driver availability) outside the RideRequest, but enforce internal invariants here.

## Testing and documentation

- Unit test all valid and invalid transitions.
- Property-test timeouts or edge cases: what happens when payment arrives after completion attempts?
- Document the allowed state transitions clearly in code and API docs.

## Takeaway

Treat RideRequest as a small stateful domain object, not a throwaway DTO. Encapsulate transitions, enforce invariants, and you get safer, clearer, and more interview-ready designs.

#SystemDesign #ObjectOrientedDesign #SoftwareEngineering
