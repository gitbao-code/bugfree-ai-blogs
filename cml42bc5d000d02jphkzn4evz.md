---
title: "Coffee Machine OOD: Stop Mixing UI, Payment, and Brewing Logic"
seoTitle: "Coffee Machine OOD — Keep UI, Payment, and Brewing Logic Separate"
seoDescription: "Design a coffee machine with separate UI, payment, and brewing components to avoid god objects, isolate failures, and enable safe extensions."
datePublished: Sun Feb 01 2026 18:16:32 GMT+0000 (Coordinated Universal Time)
cuid: cml42bc5d000d02jphkzn4evz
slug: coffee-machine-ood-separate-ui-payment-brewing-logic
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769969771679.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769969771679.png

---

# Coffee Machine OOD: Stop Mixing UI, Payment, and Brewing Logic

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1769969771679.png" alt="Coffee Machine Architecture" width="600" />

In a coffee machine system-design interview, the clearest winning move is to enforce a strict separation of concerns. The CoffeeMachine should orchestrate components — not implement every feature itself. Let small, focused modules own their responsibilities:

- UserInterface: input/output, presentation, user interactions
- PaymentSystem: transaction processing, payment validation
- Brewer / TemperatureController: brewing logic, temperature management

This avoids a "god object," isolates failures (a UI freeze shouldn't break brewing), and makes safe extension possible (add Apple Pay or a new CoffeeType without rewriting the core flow). Interviewers look for designs that can change safely and predictably.

## Recommended components and responsibilities

- UserInterface
  - Collects user choices (menu, size, strength)
  - Displays status and errors
  - Translates user actions into high-level commands (e.g., "startBrew(coffeeType, size)")

- PaymentSystem
  - Handles payment initiation and confirmation
  - Exposes simple outcomes (success, failure, pending)
  - Isolates gateway specifics (Apple Pay, NFC, card reader)

- BrewController (Brewer)
  - Executes brew recipe steps (grind, water flow, extraction time)
  - Controls temperature via TemperatureController
  - Reports progress and final status

- TemperatureController
  - Maintains target temperature
  - Exposes stable readouts and alerts

- CoffeeMachine (Orchestrator)
  - Coordinates the above components
  - Applies business rules (e.g., require successful payment before brew)
  - Handles retries, timeouts, and compensations

## Interaction flow (example)

1. UI collects order and requests payment.
2. UI asks PaymentSystem to authorize.
3. PaymentSystem returns success/failure asynchronously.
4. On success, CoffeeMachine instructs BrewController to begin.
5. BrewController uses TemperatureController and reports progress.
6. On completion or error, CoffeeMachine notifies UI and optionally refunds via PaymentSystem.

## Why this separation matters

- Avoids god objects: responsibilities are small and testable.
- Failure isolation: UI or payment issues won't stop brewing hardware logic.
- Easier extensions: add new payment methods or coffee recipes by implementing small adapters.
- Safer changes: modify one component without cascading side effects.

## Common mistakes to avoid

- Embedding payment logic inside the UI or brewer.
- Letting the CoffeeMachine class hold all business and hardware code.
- Mixing synchronous blocking calls across layers (causes UI freezes).

## How to show this in an interview

- Start by naming components and their responsibilities.
- Sketch a simple sequence of interactions (who calls whom and why).
- Mention failure modes and how you would handle them (timeouts, retries, partial failures).
- Show how you'd add features (e.g., Apple Pay or a new CoffeeType) with minimal change.

## Small example (pseudocode interfaces)

```
interface IPaymentSystem {
  Task<PaymentResult> authorize(PaymentInfo info);
}

interface IBrewController {
  Task<BrewResult> startBrew(CoffeeType type, Size size);
}

class CoffeeMachine {
  void processOrder(Order order) {
    var payment = paymentSystem.authorize(order.payment);
    if (payment.success) brewController.startBrew(order.type, order.size);
  }
}
```

Keep each module small and focused. In interviews, designs that separate concerns, handle errors, and demonstrate safe extensibility score highly.

#SystemDesign #OOD #SoftwareEngineering
