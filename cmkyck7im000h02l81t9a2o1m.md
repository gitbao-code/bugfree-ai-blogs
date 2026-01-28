---
title: "Food Delivery OOD: The One Relationship Interviewers Watch Closely"
seoTitle: "Food Delivery OOD — Why Separating Order and Delivery Matters"
seoDescription: "Why separating Order (commercial) from Delivery (fulfillment) matters in food delivery system design — cleaner boundaries, safer failures, better scalability."
datePublished: Wed Jan 28 2026 18:16:45 GMT+0000 (Coordinated Universal Time)
cuid: cmkyck7im000h02l81t9a2o1m
slug: food-delivery-ood-separate-order-delivery
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769624178306.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769624178306.png

---

![Order vs Delivery diagram](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769624178306.png){width="600"}

> In a food-delivery design, the most important modeling decision is separating Order from Delivery (1:1).

## The core idea — Order vs Delivery

Keep two distinct concepts:

- **Order** — the customer's commercial record: items, restaurant, price, taxes, payment state, and refund history. This is the immutable (ish) business contract between customer and platform/merchant.
- **Delivery** — the fulfillment workflow: assigned courier, pickup/drop-off tasks, route, and delivery status. This is the operational state machine that drives real-world activity.

Although an Order and its Delivery are tightly linked (usually a 1:1 relationship), separating them is a powerful design choice.

## Why this separation matters

1. Separation of concerns
   - Orders capture money, liability, and refunds. Delivery captures logistics and physical state changes. Keeping them separate prevents operational noise from corrupting financial records.

2. Safer failure handling
   - Deliveries can be reassigned, retried, delayed, or marked failed without mutating the core commercial record. That makes it easier to reason about refunds, chargebacks, and SLA calculations.

3. Clear state machines
   - Orders and Deliveries have different life cycles. Example:
     - Order states: Created → Paid → Cancelled → Refunded
     - Delivery states: Unassigned → Assigned → PickedUp → EnRoute → Delivered → Failed
   - Modeling them separately avoids state explosion and reduces edge-case complexity.

4. Transaction boundaries & consistency
   - Payment operations need strong consistency and auditability. Delivery operations can often be eventually consistent, with retries and compensation. Splitting models helps you choose the right consistency level per domain.

5. Auditability & compliance
   - Financial records should be auditable and tamper-resistant. Keeping delivery events in an operational log (events, telemetry) while storing payment events on the Order makes compliance easier.

6. Scalability & ownership
   - You can scale/order-service and delivery-service independently, assign different teams, and evolve each model without coupling.

## Signals interviewers look for

When you propose or explain this separation in interviews, you demonstrate several important design skills:

- Domain boundaries: understanding what belongs where.
- Failure modes: recognizing transient operational failures vs. durable commercial state.
- State machine design: defining clear, testable transitions for both Order and Delivery.
- Transaction strategy: which operations must be ACID vs. which can be eventually consistent with compensation.
- Idempotency and retries: how to safely retry delivery actions (e.g., assigning a courier) without duplicating charges.
- Observability and audit trails: storing events and timelines for debugging and compliance.

Interviewers may follow up with questions like:
- What happens if a delivery is never assigned? (timeouts, compensation, cancellation)
- How would you model partial deliveries or multi-drop orders? (1:many Delivery per Order or Delivery with multiple stops)
- How do refunds interact with failed deliveries? (separate refund flow, hold funds until certain Delivery states)
- How to ensure idempotent assignment and notification flows? (use unique operation IDs, event deduplication)

## Implementation patterns (practical tips)

- Use separate services/tables/aggregates for Order and Delivery with a stable link (order_id on delivery).
- Keep payment events on the Order aggregate. Keep ephemeral operational events (courier pings, routing updates) on Delivery or an events store.
- Model compensating actions explicitly (e.g., refund on failed delivery) rather than trying to merge the two flows.
- Provide a canonical timeline view by joining ordered events from both sides for UIs and audits.

## Bottom line

Splitting Order (commercial) from Delivery (operational) is a small modeling decision with big downstream benefits: clearer boundaries, safer failure handling, simpler state machines, and better scalability. In interviews, this separation signals that you understand domain boundaries, transactional concerns, and the real-world failure modes that make production systems hard.

#SystemDesign #OOD #SoftwareEngineering
