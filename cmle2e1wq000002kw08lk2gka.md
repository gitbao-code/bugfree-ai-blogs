---
title: "Facebook Search: Privacy Filtering Is NOT Optional—It’s a System Design Constraint"
seoTitle: "Facebook Search: Privacy Filtering Is NOT Optional—It’s a System Design Constraint"
seoDescription: "Privacy in search is a system constraint. Enforce batch access-control filtering before ranking to avoid leaks and per-result RPC overhead."
datePublished: Sun Feb 08 2026 18:16:20 GMT+0000 (Coordinated Universal Time)
cuid: cmle2e1wq000002kw08lk2gka
slug: facebook-search-privacy-filtering-system-design-constraint
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770574557479.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770574557479.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1770574557479.png" alt="Search privacy flow" width="800" />

> Treating privacy as a UI toggle is the easiest way to fail. Privacy is a hard system constraint that must be enforced in the search path.

When you design a large-scale search system (think Facebook-level scale), the inverted index is excellent at returning candidate IDs quickly. But those candidates can include content the viewer must not see: private posts, group-only content, restricted profiles, or items subject to complex ACLs. Relying on the index alone is dangerous — it was never designed to be the final arbiter of access.

The right approach: apply access-control filtering inside the Search Service before you rank or return results. Do this in batches to avoid the per-result RPC overhead that kills throughput and latency.

Why this matters

- The index is an optimization structure, not an access-control authority. Indexes optimize discovery, not visibility.
- If you defer access checks until after ranking or in the client/UI, you risk leaking sensitive items (snippets, counts, caching artifacts) and creating audit and compliance nightmares.
- Per-result RPC checks are expensive. They add CPU, network round-trips, and unpredictable tail latency.

Recommended design pattern

1. Query arrives at Search Service.
2. Inverted index (or candidate generator) returns candidate IDs quickly.
3. Search Service calls a Visibility Checker / Access Control Service in batches with those candidate IDs and the requesting principal.
4. The Access Control Service returns a filtered subset (and optionally per-ID visibility metadata).
5. Pass filtered candidates to the Ranker and produce results for the client.

This pattern keeps expensive checks off the critical path of per-result ranking and avoids leaking unauthorized content.

Implementation tips

- Batch checks: Group candidates and perform a single RPC per batch rather than per item. Choose batch sizes that balance payload size, parallelism, and tail latency.
- Parallelize with limits: Run a few in-flight batch checks concurrently; throttling protects backend stability.
- Cache visibility results: Cache per-principal or per-object visibility bits where possible with short TTLs. Beware of stale ACLs — use conservative caching or invalidation hooks.
- Conservative indexing: If you pre-annotate the index with coarse visibility (e.g., "public", "friends-only", "restricted"), treat that as a hint, not a guarantee. Always enforce the authoritative check at query time.
- Precompute where safe: For stable ACLs (e.g., public pages), you can pre-filter at index time. For dynamic ACLs (frequent membership changes), prefer runtime checks.
- Use efficient encodings: Bitmaps, bloom filters, or packed ACL representations can accelerate batch checks but must be used carefully to avoid false positives that could leak data.
- Fail closed: On errors/timeouts from the Visibility Checker, default to hiding ambiguous results rather than exposing them.

Operational concerns

- Monitor tail latency: Access checks add latency; track P95/P99 for the whole search path and for the Visibility Checker itself.
- Audit logging: Record which candidate IDs were filtered and why. This helps for incident response and for proving compliance.
- Test adversarially: Fuzz queries and simulate ACL churn to ensure no leakage across sharding, caching, or ranking components.
- Rolling changes: When changing ACL representation or caching semantics, roll out carefully and include feature flags so you can revert if leaks are detected.

Security mantra

Never trust the index alone. Treat the index as an optimization layer and enforce visibility checks in the critical search path. Defense-in-depth — multiple checks at index-time (conservative hints), query-time (authoritative checks), and UI-time (sanity checks) — reduces risk.

Quick checklist

- [ ] Index returns candidates only — do not assume they are visible.
- [ ] Enforce batch access-control checks before ranking.
- [ ] Use caching with conservative TTLs and invalidation hooks.
- [ ] Fail closed on visibility service errors.
- [ ] Monitor latency, errors, and audit filtered results.
- [ ] Run adversarial and regression tests focused on ACLs.

Privacy isn’t a feature toggle you can add in the UI. It’s a system design constraint baked into the search path.

#SystemDesign #DataEngineering #Search