---
title: "Interview OOD Drill: Design Uber in 5 Classes (and Explain It Clearly)"
seoTitle: "Design Uber in 5 Classes — OOD Interview Drill"
seoDescription: "Model Uber in five clean OOD classes: User, Driver, Ride, RideManager, Payment. Learn responsibilities, state transitions, and extensibility for interviews."
datePublished: Mon Apr 06 2026 17:17:48 GMT+0000 (Coordinated Universal Time)
cuid: cmnngec4f000002l6f3m41zwf
slug: design-uber-5-classes-ood-interview-drill
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775495772005.png" alt="Design Uber in 5 Classes" style="max-width:800px;height:auto;" />

# Interview OOD Drill: Design Uber in 5 Classes (and Explain It Clearly)

If you can model Uber with a small set of clean object-oriented classes and defend the design, you'll handle many system-design and OOD interview questions. Here is a compact, interview-friendly approach using five core classes and the reasoning you'd use to explain and extend it.

## The five core classes

1. User
   - Represents a generic user of the system (rider or driver account).
   - Key fields: id, name, phone, rating
   - Key methods: updateProfile(), addPaymentMethod()

2. Driver (extends User)
   - Driver is a User plus driving-specific data: vehicle, currentLocation, availabilityStatus
   - Key fields: vehicleInfo, currentLocation, status (available / busy / offline)
   - Key methods: updateLocation(), acceptRide(), goOffline()

3. Ride
   - Represents a trip with pickup/dropoff and lifecycle state
   - Key fields: id, rider (User), driver (Driver|null), pickupLocation, dropoffLocation, fare, status
   - Status (example): PENDING -> ACCEPTED -> IN_PROGRESS -> COMPLETED -> BILLED
   - Also handle CANCELLED and FAILED states

4. RideManager
   - Coordinates matching riders to drivers and transitions ride states
   - Responsibilities: findAvailableDrivers(), dispatchDriver(), startRide(), completeRide(), cancelRide()
   - Keeps business logic out of domain objects (Ride/Driver) and centralizes matching & state transitions

5. Payment
   - Handles charging, refunds, and integrating with payment providers
   - Responsibilities: calculateFare(ride), charge(ride), refund(ride)

### Compact class sketch (pseudo-code)

```
class User { id, name, phone, rating }
class Driver extends User { vehicleInfo, currentLocation, status }
class Ride { id, rider, driver, pickup, dropoff, fare, status }
class RideManager {
  findAvailableDrivers(pickup)
  matchRiderToDriver(ride)
  startRide(ride)
  completeRide(ride)
  cancelRide(ride)
}
class Payment { calculateFare(ride), charge(ride), refund(ride) }
```

## Ride state transitions

A simple state machine you can draw and explain:

- PENDING —(driver accepts)→ ACCEPTED —(rider picked up)→ IN_PROGRESS —(trip ends)→ COMPLETED —(charge)→ BILLED
- PENDING/ACCEPTED —(cancel)→ CANCELLED
- Any failure —> FAILED

When answering, explain who triggers and enforces transitions (RideManager handles transitions; persistent store records states; Payment invoked on COMPLETED).

## Why this separation? (defend responsibilities)

- Single Responsibility: each class has one reason to change — domain objects (User/Driver/Ride) store state, RideManager encapsulates orchestration, Payment isolates billing.
- Low coupling & high cohesion: RideManager coordinates but doesn’t implement charging logic; Payment can be swapped for another provider.
- Clear extension points: adding surge, cancellations, ratings, or new matching strategies doesn’t force major changes to core classes.

## Extensibility & real-world considerations

- Pricing: add a PricingService (or extend Payment) that supports base fare, distance/time, surge multipliers, promotions.
- Surge & dispatch strategy: keep matching algorithm in RideManager or extract to a MatchingService to try different strategies (nearest, ETA, pooled rides).
- Cancellations & refunds: RideManager signals CANCELLED and Payment handles partial/conditional refunds.
- Ratings & history: User and Driver keep rating summaries; a separate Audit/History store keeps ride events for analytics.
- Concurrency: driver availability and matching require locking or optimistic updates (e.g., compare-and-swap) and fast caches for location queries.
- Scaling: split services — Authentication, RideService, MatchingService, PaymentService — and use event-driven flows (messages) for state changes and billing.

## How to explain this in an interview

- Start with assumptions (single city vs global, real-time constraints, offline drivers, cancellation policy).
- Present the 5-class model and walk through a ride lifecycle: request → match → accept → start → complete → bill.
- Explain responsibilities (who changes what and why), state transitions, and where to add features like surge or pooled rides.
- Discuss operational concerns: scaling, consistency, failure handling, and how you'd split into services.

## Quick summary

Model Uber with these core classes: User, Driver (extends User), Ride, RideManager, and Payment. This keeps domain state, orchestration, and billing separated and makes it easy to defend responsibilities, add features, and reason about state transitions during an interview.

