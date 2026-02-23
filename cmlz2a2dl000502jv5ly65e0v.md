---
title: "The Interview Detail Most Candidates Miss: Coupon Expiry Is a Data Problem"
seoTitle: "Coupon Expiry Is a Data Problem — Design Patterns for Coupons & Deals"
seoDescription: "Design coupon expiry as a data contract: query behavior, state model, and retention. Tips for indexing, archival, analytics, and interview answers."
datePublished: Mon Feb 23 2026 10:56:24 GMT+0000 (Coordinated Universal Time)
cuid: cmlz2a2dl000502jv5ly65e0v
slug: coupon-expiry-data-problem-design-patterns
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771844150260.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771844150260.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771844150260.png" alt="Coupon expiry design" style="max-width:800px;width:100%;height:auto;margin-bottom:16px;">

# The Interview Detail Most Candidates Miss: Coupon Expiry Is a Data Problem

In a Coupons & Deals platform, “expiry” is not just a UI label — it’s a core data contract that touches correctness, performance, and reporting. How you model and enforce expiration affects queries, analytics, user experience, and compliance.

Below is a concise, interview-friendly summary of the decisions you should make and why they matter, plus practical implementation patterns and gotchas.

---

## 1) Query path: exclude expired by default

Behavior:
- Default search/listing queries should exclude expired coupons.
- Use an indexed expiry field (e.g., `expiry_date`) so the filter is fast and selective.

Why:
- Keeps user-facing search performant and correct (users shouldn't see unusable coupons).
- Prevents accidentally applying expired coupons in checkout logic.

Implementation notes:
- Add a persistent boolean or computed field like `is_active` if your DB supports it, but still keep `expiry_date` as the source of truth.
- In SQL: create a composite index on `(is_active, expiry_date)` or on `expiry_date` alone if `is_active` is derived.
- In document stores: use a TTL index for automatic deletes if you want hard-deletes after a retention period (see Cleanup).

Example (SQL):

SELECT *
FROM coupons
WHERE expiry_date > CURRENT_TIMESTAMP
  AND active = TRUE
ORDER BY priority DESC, expiry_date ASC;

---

## 2) State model: mark as expired (don’t delete immediately)

Behavior:
- When `expiry_date` passes, change the coupon state to `expired` (soft-delete style) instead of immediate hard delete.

Why:
- Preserves historical data for analytics, audits, and dispute resolution.
- Enables investigation of incidents (e.g., "Why was this applied?" or "Was this coupon active at this timestamp?").

Recommended fields:
- `created_at`, `starts_at`, `expiry_date`
- `state` enum: `draft`, `active`, `scheduled`, `expired`, `archived`, `deleted`
- `expired_at` timestamp (when the system marked it expired)
- `deleted_at` timestamp for eventual hard-deletion

---

## 3) Cleanup: archive/purge after a retention window

Behavior:
- Run scheduled jobs (daily/weekly) to move expired coupons into an archive or to purge them after a retention window.

Why:
- Keeps primary indexes and tables small for performance.
- Satisfies storage cost and compliance requirements while preserving data for a defined period.

Options:
- Archive to a cost-effective store (S3/parquet) for long-term analytics.
- Use DB partitioning by date and drop old partitions.
- Use TTL indexes (MongoDB) or scheduled jobs to delete after retention.

Retention policy considerations:
- Business/Legal retention requirements
- Audit and dispute windows
- GDPR/CCPA: implement a path for user data removal that can override retention when necessary

---

## 4) Indexing & performance tips

- Index `expiry_date` (or a combined index with other common filters) to allow the DB to skip expired rows quickly.
- Consider maintaining a materialized view or denormalized table for active coupons used in high-throughput queries.
- Cache active coupons carefully and invalidate cache when state changes (or use short TTLs).
- For search engines (Elasticsearch): exclude expired docs at ingestion or use a filter that’s cheap to evaluate.

---

## 5) Analytics & reporting

- Keep expired coupons in your analytics DB long enough to analyze redemption rates over time.
- Store the coupon state transitions in an event log so you can reconstruct the state at any historical point (useful for billing disputes and A/B testing).
- Tag analytic events with the coupon version/id and the coupon `expiry_date` so joins are straightforward.

---

## 6) Edge cases & gotchas

- Timezones & clock skew: store timestamps in UTC and compare against server/DB time. Be explicit about whether `expiry_date` is inclusive or exclusive (e.g., expires at 00:00:00 UTC of the given date).
- Grace periods: business might want a short grace window for UX reasons — implement explicitly, not implicitly.
- Overlapping promos & stacking rules: expired coupons must not interact with stacking logic.
- Race conditions at checkout: validate coupon validity again at redemption time (server-side) even if shown as active in the UI.
- Compliance: users’ right-to-be-forgotten requests may require earlier deletion of records; have a process to reconcile with analytics needs.

---

## 7) What to say in interviews (concise checklist)

When asked about coupon expiry, state explicitly:

- "Expiry is a data contract affecting correctness (can't apply expired coupons), performance (filter/index), and reporting (analytics & audits)."
- Describe default query behavior: "Exclude expired items by default; index expiry_date." 
- Describe state management: "Mark as expired (soft-delete) and retain for a configured retention window to support audits." 
- Describe cleanup: "Archive or purge via scheduled jobs/TTL after retention, and handle compliance exceptions." 
- Mention edge cases: timezone, race conditions at checkout, cache invalidation, and legal retention or deletion requirements.

This hits technical design, operational concerns, and compliance — the areas interviewers want to hear about.

---

## 8) Example data model (JSON-like)

{
  "id": "coupon_123",
  "code": "SUMMER20",
  "starts_at": "2026-06-01T00:00:00Z",
  "expiry_date": "2026-06-30T23:59:59Z",
  "state": "expired",
  "expired_at": "2026-07-01T00:00:00Z",
  "created_at": "2026-05-01T12:00:00Z",
  "deleted_at": null
n}

---

## Final takeaway

Treat expiry as a first-class data design problem, not a cosmetic UI tag. In interviews, call out the three pillars: query behavior (performance/correctness), durable state model (analytics/auditability), and cleanup/retention (costs/compliance). That concise framing shows you understand both system design and operational realities.

#SystemDesign #BackendEngineering #DataEngineering
