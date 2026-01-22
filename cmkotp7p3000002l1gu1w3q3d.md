---
title: "Google SWE New Grad Interview Experience — 4 Rounds, Real Takeaways"
seoTitle: "Google SWE New Grad Interview Experience — 4 Rounds, Real Takeaways"
seoDescription: "First-hand Google SWE new-grad loop: 3 technical rounds (coding, system design, streaming) and 1 behavioral — solutions, pitfalls, and practical takeaways."
datePublished: Thu Jan 22 2026 02:18:50 GMT+0000 (Coordinated Universal Time)
cuid: cmkotp7p3000002l1gu1w3q3d
slug: google-swe-new-grad-interview-4-rounds-takeaways
cover: https://hcti.io/v1/image/019be37e-37cc-70fa-ad8d-3aca7a45d5ea
ogImage: https://hcti.io/v1/image/019be37e-37cc-70fa-ad8d-3aca7a45d5ea

---

<img src="https://hcti.io/v1/image/019be37e-37cc-70fa-ad8d-3aca7a45d5ea" alt="Interview cover" style="max-width:100%;height:auto;" />

# Google SWE New Grad Interview Experience — 4 Rounds, Real Takeaways

This is a high-score interview report shared by a "Bugfree" user who completed the Google Software Engineer (New Grad) loop: three technical rounds and one behavioral. The loop was challenging but fair. Below are the problems, solutions, follow-ups, and practical takeaways you can use for preparation.

---

## Quick overview
- Structure: 3 technical rounds (coding, system design, data/streaming) + 1 behavioral round
- Tone: challenging but reasonable; interviewers wanted correctness, clarity, and trade-off discussion

---

## Round 1 — Coding
Problem summary
- Find the maximum subarray sum with an added constraint that a[i] == a[j] for the endpoints of the subarray.

Approach (clean, optimal)
1. Convert the array into prefix sums: prefix[i] = sum(arr[0..i-1]).
2. For each value v that appears in the array, you want the max(prefix[j+1] - prefix[i]) for indices i <= j such that arr[i] == arr[j] == v. That can be rewritten as prefix[j+1] - min_prefix_for_v.
3. Maintain a hashmap keyed by value v that stores the minimum prefix sum seen so far for indices where arr[index] == v.
4. As you scan, compute candidate sums using the current prefix minus the stored min prefix for that value and update the global max.

Pseudo outline
```text
prefix = 0
minPrefixForValue = {}  # value -> min prefix when we've seen that value
maxSum = -inf
for i, val in enumerate(arr):
  prefix += val
  if val not in minPrefixForValue:
    minPrefixForValue[val] = previous prefix before this index (i.e., prefix - val)
  else:
    candidate = prefix - minPrefixForValue[val]
    maxSum = max(maxSum, candidate)
  minPrefixForValue[val] = min(minPrefixForValue[val], prefix - val)
```

Complexity
- Time: O(n)
- Space: O(u) where u is number of distinct values

Follow-ups & tips
- Clarify if subarray length must be >= 2 (endpoints distinct) or can be a single element.
- Consider negative numbers and all-negative arrays: initialize maxSum appropriately.
- Explain correctness: using prefix sums reduces subarray-sum queries to O(1) and the hashmap enforces the endpoint-equality constraint.

---

## Round 2 — System Design: Meeting Scheduler
Problem summary
- Start by designing a meeting scheduler for a single room. Then scale to multiple rooms and more realistic constraints.

Initial (single room)
- Requirements: book a time slot, check conflicts, cancel, list bookings.
- Minimal API: Book(start, end, user), Cancel(bookingId), GetBookings(range).
- Core component: interval store with conflict checks — you can use an ordered structure (e.g., balanced BST keyed by start time) or an ordered list if load is small.

Scaling to multiple rooms & realistic features
- Multi-room extension: room metadata, search for an available room given constraints (capacity, equipment, timezone).
- Architecture:
  - API layer: validates requests and authenticates users.
  - Scheduler service: handles booking logic and conflict resolution.
  - Storage layer: persistent DB (partition by building/room or use sharding by room id).
  - Cache: hot rooms and frequently-read schedules.
  - Worker/queue: to handle async operations (notifications, calendar sync).

Key design concerns & solutions
- Concurrency: use optimistic locking with retries or distributed locks for a room when booking; you can also use compare-and-set operations in DB.
- Availability search: maintain an index per room or an occupancy bitmap for time buckets to speed-up availability checks.
- Recurring meetings: expand into multiple booking entries or store recurrence rules and materialize on read.
- Time zones & daylight saving: store all times in UTC, convert on client side for display.
- Edge cases: partial overlaps, back-to-back bookings, daylight-adjusted times, meeting durations spanning days.

Trade-offs to discuss
- Complexity vs latency: precomputed availability (fast reads, costly writes) vs on-demand search (slower reads, simpler writes).
- Strong consistency for bookings vs eventual consistency for notifications and analytics.

---

## Round 3 — Data Structures / Streaming
Problem summary
- Compute the average of the last K items in a stream (FIFO). Follow-up: remove the top X outliers before averaging.

Base solution (average of last K)
- Maintain a fixed-size queue (or circular buffer) storing last K values and a running sum.
- On push:
  - If buffer size < K, push value and add to sum.
  - Else, pop oldest value, subtract from sum, push new value, add to sum.
- Average = sum / current_size

Complexity
- Time per update: O(1)
- Space: O(K)

Follow-up (remove top X outliers)
Options to handle removing top X before averaging:
1. Two heaps (max-heap for top X, min-heap for bottom K-X, plus the middle window):
   - Maintain three groups: top X, middle (the rest), bottom if needed.
   - As elements enter/leave, rebalance heaps to ensure top heap contains the current top X.
   - Maintain sums for each group to compute the average quickly.
   - Complexity: O(log K) per update.

2. Balanced BST / order-statistics tree (e.g., multiset with counts):
   - Keep K elements in a balanced BST keyed by value. Maintain prefix sums in nodes or keep separate tracking of sum of largest X via traversal/augmented tree.
   - Complexity: O(log K) per insertion/deletion; average calculation needs maintained sums.

3. If values are bounded or discretized: use counting buckets to track frequencies and cumulative counts for O(1) or O(U) updates (U = bucket range).

Practical recommendation
- For general numeric data with no special bounds, two heaps (or two heaps plus a middle heap) with lazy deletion is a common, robust approach.
- Always track group sums to return the average quickly.

---

## Round 4 — Behavioral
Topics covered
- Inclusion initiative: describing a concrete contribution that helped someone from an underrepresented group feel included.
- Time vs quality trade-offs: when you chose shipping speed over polish (or vice versa), what metrics and mitigations you used.
- Managing a remote team: communication patterns, async collaboration, and how you build trust.

How to structure answers
- Use STAR (Situation, Task, Action, Result).
- Quantify impact where possible (e.g., "reduced onboarding time by 20%", "increased test coverage by X").
- Be honest about trade-offs and lessons learned.

Example pointers
- Inclusion: describe initiative, stakeholders engaged, and measurable outcomes (attendance, feedback improvements).
- Time vs quality: show that you considered risk, rollback plans, monitoring, and prioritization.
- Remote team mgmt: highlight tooling, regular rituals (standups, retrospective cadence), and metrics for team health.

---

## Final takeaways & prep tips
- Clarify assumptions early and explicitly; interviewers reward clear thinking.
- Talk through correctness and edge cases before optimizing.
- For coding: master prefix sums, sliding windows, hashmaps, heaps, and common patterns (two pointers, dynamic programming).
- For system design: use a structured approach — requirements, API, data model, components, scaling, trade-offs, and edge cases.
- For streaming problems: know O(1) rolling techniques and O(log K) approaches for order-statistics maintenance.
- Behavioral: prepare 6–8 stories with measurable outcomes, and tailor them to common themes (leadership, inclusion, failure/recovery).

Good luck — practice problems under timed conditions, do mock interviews, and focus on communicating clearly and verifying assumptions.

---

#Tags
#SoftwareEngineering #InterviewPrep #SystemDesign
