---
title: "Interview OOD Drill: Design Uber in 5 Classes (and Explain It Clearly)"
seoTitle: "Design Uber in 5 Classes: Clear OOD for Interviews"
seoDescription: "Model Uber with 5 classes: User, Driver, Ride, RideManager, Payment. Explain responsibilities, state transitions, matching, payments and extensibility."
datePublished: Mon Apr 06 2026 17:16:37 GMT+0000 (Coordinated Universal Time)
cuid: cmnngctfm000102l40uv62ule
slug: design-uber-in-5-classes
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png

---

<!-- Cover image -->
<p align="center"><img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png" alt="Uber OOD diagram" style="max-width:700px; width:100%; height:auto;"/></p>

# Interview OOD Drill: Design Uber in 5 Classes (and Explain It Clearly)

If you can model a ride-hailing system like Uber with clean object-oriented design (OOD), you can handle many system-design interview problems. Here’s a compact, interview-friendly way to model the core domain in five classes, with responsibilities, state transitions, and common extensions.

## High-level idea

Start small and defend the responsibilities you give each class. Focus on: core entities, coordinators that operate on those entities, and how the system evolves (state transitions). Keep the design open for pricing, cancellations, surge, driver ratings, etc.

## The 5 classes (core model)

1. User
   - Represents a person using the app (rider or driver account).
   - Fields: id, name, contactInfo, paymentMethods, userType (RIDER / DRIVER) or role flag.
   - Methods: updateProfile(), addPaymentMethod(), getLocation() (if available).

2. Driver (extends User)
   - Inherits User. Adds domain-specific attributes and behavior.
   - Fields: vehicleInfo, currentLocation, isAvailable, rating.
   - Methods: updateLocation(), setAvailability(), acceptRide(), finishRide().

3. Ride
   - Represents a single trip request and lifecycle.
   - Fields: id, riderId, driverId (nullable until matched), pickupLocation, dropoffLocation, price, status.
   - Status lifecycle: PENDING -> IN_PROGRESS -> COMPLETED (and other states: CANCELED, FAILED).
   - Methods: transitionTo(newStatus) with validation, requestCancellation(), estimatePrice().

4. RideManager (coordinator)
   - Responsible for matching riders to available drivers and managing ride state transitions.
   - Responsibilities:
     - Receive ride requests, find candidate drivers (by proximity, filters), and notify drivers.
     - Assign accepted driver to Ride and move status from PENDING to IN_PROGRESS.
     - Handle timeouts, retries, re-matching when drivers decline.
   - Example API: requestRide(rider, pickup, dropoff) -> Ride; driverAccepts(rideId, driverId); cancelRide(rideId).

5. Payment (coordinator/service)
   - Responsible for charging after ride completion and handling refunds/cancellations.
   - Responsibilities:
     - Calculate final fare (base fare + distance + time + surge + taxes + fees).
     - Charge rider’s payment method and distribute payout to driver (or schedule payout).
     - Handle failed payments and retries.
   - Example API: charge(ride) -> PaymentReceipt; refund(ride).

## State transitions (ride lifecycle)

- PENDING: Rider requested. Searching for driver.
  - on driver accept -> IN_PROGRESS
  - on rider cancel -> CANCELED
  - on timeout/no driver -> FAILED or RE-QUEUE

- IN_PROGRESS: Driver accepted and trip started.
  - on arrival at destination -> COMPLETED
  - on user/driver cancel (rare after start) -> CANCELED

- COMPLETED: Trip finished — trigger Payment. Mark driver available.

Make sure transition logic is centralized (e.g., Ride.transitionTo()) and validated to prevent invalid moves.

## Example matching sequence (simplified)

1. Rider calls RideManager.requestRide(rider, pickup, dropoff).
2. RideManager creates Ride(status=PENDING) and queries available drivers nearby.
3. RideManager notifies drivers (push) — first driver to accept calls driverAccepts(rideId, driverId).
4. RideManager assigns driver: ride.driverId = driverId; ride.transitionTo(IN_PROGRESS).
5. When driver reports trip end, RideManager calls ride.transitionTo(COMPLETED) and triggers Payment.charge(ride).

## Responsibilities: how to defend this design in an interview

- Single Responsibility: Each class has a clear purpose — entities hold data and small behaviors, managers coordinate processes, payment encapsulates billing.
- Separation of concerns: RideManager handles matching and lifecycle, Payment handles money. This prevents mixing matching logic with billing logic.
- Extensibility: New features (surge pricing, cancellation policies, promos, shared rides) should be added as services or strategies rather than bloating Ride or RideManager.
- Testability: Keep side effects (network calls, DB, push notifications, payment gateway) out of pure logic; inject them as interfaces/clients so you can mock in tests.

## Extensibility & common features

- Pricing strategies: Implement a PricingStrategy interface (FlatRate, DistanceBased, SurgePricing) and inject it into Payment or Ride for final fare calculation.
- Cancellations: Add cancellation policies with penalties. Implement as a CancellationPolicy service invoked by RideManager.
- Surge: Surge rules can be a separate service consulted by PricingStrategy.
- Ratings: Add a Rating service to allow drivers and riders to rate each other; store rating in Driver/User aggregates and compute averages asynchronously.
- Shared rides / pooling: Model a Ride as a composition that can include multiple riders, or create a PoolRide subclass.

## Concurrency and scaling notes (quick)

- Matching: Use spatial indices (geohash/quadtrees) and an event-driven queue for driver notifications.
- Consistency: Use optimistic locking or distributed locks when assigning drivers to avoid double-assign.
- Events: Emit events (RideStarted, RideCompleted, PaymentProcessed) so other services (analytics, notifications) can react asynchronously.

## Common interview pitfalls

- Overloading Ride or Driver with too many responsibilities (payment logic, notification delivery, complex matching) — explain why you separate concerns.
- Forgetting invalid state transitions — show you validated allowed moves.
- Not discussing failures (what happens if payment fails or driver cancels at last minute).

## Quick checklist to present in an interview

- List the 5 classes and their responsibilities.
- Explain ride state transitions and where you enforce them.
- Describe how matching works at a high level and how you avoid race conditions.
- Show how Payment is decoupled and how pricing/surge can be added.
- Call out testability and extension points (strategies, policies, events).

With this concise model and talking points you can clearly explain an OOD for Uber in interviews: 3 core entities (User/Driver/Ride) and 2 coordinators (RideManager/Payment), with a focus on responsibilities, valid state transitions, and easy extensibility.