---
title: "Health Checks: The One Detail That Makes Your Load Balancer “Real” in Interviews"
seoTitle: "Health Checks for Load Balancers — The Interview-Winning Detail"
seoDescription: "Never route to untrusted servers. Use periodic probes, hysteresis, in-memory healthy set for fast routing, and persist status for visibility and alerts."
datePublished: Wed Feb 18 2026 18:16:39 GMT+0000 (Coordinated Universal Time)
cuid: cmlscszgw000402jp66xm9xmh
slug: health-checks-load-balancer-interview-detail
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771438576809.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771438576809.png

---

![Load Balancer Health Checks](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771438576809.png "Health Checks Diagram")

> In a load balancer design, health checks are not a side feature — they decide whether your system is reliable.

Health checks are the small detail interviewers listen for. If you can’t prove a server is healthy, you should not route traffic to it. Skip this and your fancy load balancing becomes "round-robin-to-failure." Here’s a concise, interview-ready summary of what to implement and why.

## Core principles

- Never route to a server you cannot currently trust. The dispatcher should only use a maintained "healthy set."
- Keep the routing decision in memory for speed, but persist health status for visibility, monitoring, and postmortems.
- Avoid flapping: use hysteresis (failure and success thresholds) so nodes aren’t rapidly toggled.

## Recommended implementation (practical defaults)

- Probe endpoint: GET /health (or an equivalent lightweight check).
- Frequency: probe every 5–15 seconds (10s is a reasonable default).
- Failure threshold: mark unhealthy after N consecutive failures (N = 3 is common).
- Success threshold: re-admit after M consecutive successes (M = 2 or 3).
- Timeouts: keep the probe timeout shorter than your probe interval (e.g., 1–2s timeout for a 10s interval).
- Keep an in-memory healthy set for ultra-fast routing decisions; persist events to a datastore, logs, or metrics pipeline for visibility.

## Simple pseudocode

```
on_probe_result(node, ok):
  if ok:
    node.fail_count = 0
    node.success_count += 1
    if node.status == UNHEALTHY and node.success_count >= success_threshold:
      mark node HEALTHY
  else:
    node.success_count = 0
    node.fail_count += 1
    if node.status == HEALTHY and node.fail_count >= fail_threshold:
      mark node UNHEALTHY
```

Persist a timestamped status change event and emit metrics (e.g., healthy/unhealthy counts, probe latencies).

## Additional considerations and interview talking points

- Passive + active checks: combine probes (active) with passive failure detection (connection resets, high error rates) for faster reaction to real user failures.
- Connection draining: when marking a node unhealthy, stop sending new requests but allow existing connections to finish or be migrated.
- Backoff and probe throttling: after marked unhealthy, reduce probe frequency or use exponential backoff to avoid hammering a failing instance.
- Security: restrict /health so only the load balancer (or an authenticated probe) can call it; otherwise attackers might infer internal state.
- Scalability: probe fan-out can be expensive at large scale — consider hierarchical health checking (region-level probes) or offloading probes to agents on each host.
- Weighted routing and sticky sessions: health checks should influence weight adjustments and session rebalancing decisions.

## Why persist health status?

In-memory decisions are fast (required for low-latency routing), but persistence gives you:
- Historical visibility for debugging and RCA
- Alerts when services degrade
- Metrics for SLO/SLA reporting

Persist status changes (not every probe line), with timestamps and reason codes.

## How to talk about this in interviews

- State the defaults (probe endpoint, frequency, fail/success thresholds) and explain trade-offs (faster detection vs false positives).
- Mention hysteresis to avoid flapping and the importance of draining connections.
- Say you keep decisions in-memory for speed but persist events for monitoring and postmortem analysis.
- Bring up passive checks and security considerations if asked for deeper detail.

Conclusion

Health checks are the single detail that turns a conceptual load balancer into a production-ready system. Implement periodic probes, use hysteresis, keep fast in-memory routing decisions, and persist status for observability — and you’ll have a robust answer that wins interviews.

#SystemDesign #BackendEngineering #SRE