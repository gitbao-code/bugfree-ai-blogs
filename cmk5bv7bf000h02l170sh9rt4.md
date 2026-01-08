---
title: "Real-Time Bidding Interviews: The One Detail You Must Nail—Async Bid Processing"
seoTitle: "RTB Interviews: Nail Async Bid Processing to Protect Latency"
seoDescription: "In RTB, accept bids fast and evaluate them asynchronously. Use events, idempotency, and partitioning to protect latency and handle spikes."
datePublished: Thu Jan 08 2026 10:51:59 GMT+0000 (Coordinated Universal Time)
cuid: cmk5bv7bf000h02l170sh9rt4
slug: rtb-interviews-async-bid-processing
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767869494492.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767869494492.png

---

<div style="text-align:center">
  <img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767869494492.png" alt="RTB async bid processing" width="800" style="max-width:100%;height:auto;" />
</div>

## The single rule for RTB systems: protect latency

In a real-time bidding (RTB) system, never evaluate bids synchronously on the request path. The primary goal of your bidding API is to accept bids quickly and protect end-to-end latency for bidders and the auctioneer.

If your request path tries to do heavy evaluation, persist state, or run business rules inline, you'll introduce latency, increase timeouts during traffic spikes, and make retries risky. Instead, embrace an asynchronous, event-driven flow.

## Correct approach (high-level)

1. Accept the incoming bid fast (respond to the client).
2. Persist the raw bid record to durable storage (database or write-ahead store).
3. Publish a bid event to a message queue or streaming system.
4. A separate Bid Evaluator service consumes events, compares bids, and updates the current best bid for that auction.
5. An Auction Manager (or scheduler) closes the auction at its configured end_time and finalizes the winner.

This decoupling keeps your API fast, increases throughput, and makes retries safe when combined with idempotency and deduplication.

## Why this pattern works

- Latency protection: The request path only does a quick accept + persist. Heavy evaluation happens off the critical path.
- Higher throughput: Consumers can be scaled independently of the API layer. You can tune partitioning and parallelism for the evaluator.
- Resilience to spikes: Message queues buffer bursts and smooth processing.
- Safe retries: With idempotency keys and dedup, at-least-once delivery from the queue won't corrupt auction state.

## Implementation details and best practices

- Persist immediately: Write the raw bid (auction_id, bidder_id, bid_amount, timestamp, idempotency_key) to durable storage before returning success.

- Use an event stream: Publish a compact event (e.g., bid_id, auction_id) to Kafka, Kinesis, Pub/Sub, or SQS for the evaluator to consume.

- Partition by auction_id: Ensure events for the same auction go to the same consumer partition to maintain ordering and avoid cross-consumer conflicts.

- Idempotency & dedup:
  - Use a unique idempotency_key per bid submission.
  - Keep a deduplication store keyed by idempotency_key (or persist uniqueness constraints in the DB) so retries don't create duplicate effects.
  - Consumers should handle at-least-once semantics by checking whether a bid has already been applied.

- Best-bid updates:
  - The Bid Evaluator should read the current best bid and apply a compare-and-set (or DB transaction) to update only if the incoming bid is better.
  - Define "better" explicitly (price, timestamp tie-breaker, bidder priority).
  - Use optimistic concurrency control or database transactions to avoid lost updates.

- Auction closing:
  - Auction Manager monitors auction end_time and finalizes the winner.
  - It should consider late-arriving bids according to your lateness policy (reject, accept within a grace window, or extend auction).

- Monitoring & observability:
  - Track queue lag, consumer throughput, persistence latencies, and discarded/duplicate events.
  - Create alerts for increasing queue lag or persistent consumer errors.

## Common pitfalls

- Evaluating on the request path: Causes timeouts and cascading failures during spikes.
- Not partitioning properly: If events for the same auction can be processed concurrently on different consumers, you’ll introduce race conditions.
- Ignoring idempotency: Without dedup, retries and at-least-once delivery can double-apply bids.
- Overly strict ordering assumptions: Don’t assume perfect ordering from distributed queues; design with at-least-once and potential reordering in mind.

## Minimal pseudocode

Request handler:

```
onBidRequest(bid):
  persistBid(bid)                # durable write
  publishEvent({ bid_id })       # lightweight event
  return 200 OK                   # respond fast
```

Consumer (Bid Evaluator):

```
onBidEvent(event):
  bid = fetchBid(event.bid_id)
  if alreadyProcessed(bid.idempotency_key):
    return
  currentBest = readBestBid(bid.auction_id)
  if isBetter(bid, currentBest):
    updateBestBid(bid.auction_id, bid)  # CAS/transactional update
  markProcessed(bid.idempotency_key)
```

Auction finalization:

```
onAuctionClose(auction_id):
  winner = readBestBid(auction_id)
  finalizeWinner(winner)
```

## TL;DR

Do not process bid evaluation synchronously on the request path. Accept and persist quickly, publish an event, and evaluate bids asynchronously with idempotency and proper partitioning. This pattern protects latency, increases throughput, and makes your RTB system robust to spikes and retries.

#SystemDesign #DistributedSystems #AdTech
