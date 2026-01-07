---
title: "Serverless Interviews: The One Reliability Detail Candidates Miss—Dead Letter Queues (DLQ)"
seoTitle: "Serverless Interviews: Why Dead Letter Queues (DLQ) Matter for Reliability"
seoDescription: "Don't rely on retries—use DLQs with backoff, monitoring, and a replay tool to handle poison messages in serverless systems."
datePublished: Wed Jan 07 2026 18:20:11 GMT+0000 (Coordinated Universal Time)
cuid: cmk4cfr1w000102l18phs1puk
slug: serverless-interviews-dead-letter-queues-dlq
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767809980210.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767809980210.png

---

![Dead Letter Queues diagram](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767809980210.png){style="max-width:100%;height:auto;"}

# Serverless Interviews: The One Reliability Detail Candidates Miss—Dead Letter Queues (DLQ)

In serverless systems, "retries" are not a reliability plan—they're a risk. When functions (Lambda or other FaaS) process events, some failures are permanent: malformed payloads, schema drift, or missing external dependencies. If you rely on blind retries you risk creating poison messages, incurring rising costs, and building up a processing backlog.

A Dead Letter Queue (DLQ) is the safety valve for those permanent failures: after a configured number of unsuccessful attempts, the event is moved to a separate queue or topic for inspection and replay.

Below is how to explain DLQs clearly in interviews, and best practices to actually make them useful.

## How to explain DLQs in an interview (short, crisp)

1. Set a sensible max-retries and exponential backoff — stop retrying forever.
2. Route repeated failures to a DLQ (separate queue/topic) for inspection.
3. Alert on DLQ depth and provide tooling to inspect, fix, and replay failed events.

## Why retries alone are dangerous

- Poison messages: an event that always fails will keep being reprocessed, wasting compute and pushing other messages back.
- Rising costs: repeated invocations or processing retries increase bills.
- Backlog and latency: retries can increase queue depth and add unpredictable delays.

## What a good DLQ strategy looks like

- Configure max retries and backoff: e.g., limit attempts (commonly 3) with exponential backoff so transient issues have time to recover.
- Move failed events to a DLQ after the limit is reached, preserving the original payload and metadata (timestamps, error messages, attempt counts).
- Monitor DLQ depth and rate: alert when DLQ items appear or when depth grows.
- Provide a replay tool: a safe way to inspect, repair, and re-inject events into the pipeline with proper tracing.

## Practical recommendations

- Preserve context: store the original event, error details, and attempt history in the DLQ so you can diagnose quickly.
- Make replays idempotent: ensure handlers can process replays without causing duplicate side effects.
- Automate alert thresholds: e.g., alert on any new DLQ item for critical pipelines, or on a growth rate for high-volume systems.
- Add tagging/labels: categorize failures (schema, validation, downstream) to route to the right owner.

## Platform notes (AWS-focused)

- AWS Lambda (async) historically supports dead-letter queues (SQS/SNS) and also offers "Destinations" to send OnFailure events to SQS, SNS, or EventBridge. Either approach can be used to capture failed async invocations.
- For event-driven systems using SQS or SNS directly, attach an SQS DLQ or a separate SNS topic to gather failed messages.

(Exact configuration varies by platform — the interview answer should show you know the pattern and the trade-offs, not necessarily every CLI flag.)

## Designing a replay tool (must-have features)

- Preview: show payload, error, and attempt history before replaying.
- Edit/patch: allow safe fixes (e.g., fix schema issues, add missing fields) before re-injection.
- Controlled replay: replay a single message or a batch, with rate limits.
- Audit trail: log who replayed what and when.
- Safety checks: prevent replaying messages that will cause harmful side effects unless explicitly confirmed.

## Common interview pitfalls to avoid

- Saying "we just retry until it succeeds" — that signals you don't handle permanent failures.
- Not mentioning monitoring/alerts for DLQs — moving messages to a DLQ without visibility is useless.
- Forgetting to preserve original metadata — without it, debugging and replaying is painful.

## One-liner to close with in an interview

"Retries are a mitigation for transient errors; DLQs are the plan for permanent ones—configure retries and backoff, route to a DLQ, alert on depth, and provide a safe replay path."

---

Tags: #Serverless #CloudComputing #AWS
