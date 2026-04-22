---
title: "Stop Guessing: Why “0 Impressions” Is a Binomial Problem"
seoTitle: "Stop Guessing: Model '0 Impressions' as a Binomial Problem"
seoDescription: "Model '0 impressions' as a Binomial event: P(X=0) = (1-1/A)^B. Clear assumptions, approximations, and interview tips."
datePublished: Wed Apr 22 2026 17:16:47 GMT+0000 (Coordinated Universal Time)
cuid: cmoabenij000602l4guykgjck
slug: stop-guessing-0-impressions-binomial-problem
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776878170358.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776878170358.png

---

# Stop Guessing: Why “0 Impressions” Is a Binomial Problem

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776878170358.png" alt="Cover: Binomial Impression Diagram" width="600" />

Quick answer

If there are A users and B impressions, and each impression independently lands on John with probability p = 1/A, then the number of impressions John gets is Binomial(B, p). The probability John gets zero impressions is simply:

`P(X = 0) = (1 - 1/A)^B`.

Why this is Binomial (short):

- Each impression is a trial. There are B trials.
- Each trial has the same chance p = 1/A of "success" (hitting John).
- Trials are independent under the usual random-allocation assumption.

So the event "John gets 0 impressions" means all B trials are misses — i.e., B independent misses — which yields `(1 - p)^B`.

Derivation

Treat each impression as a Bernoulli trial with success probability `p = 1/A`. Let `X` be the number of impressions John receives. Then `X ~ Binomial(B, p)` and

`P(X = 0) = C(B,0) p^0 (1 - p)^B = (1 - p)^B = (1 - 1/A)^B`.

Numerical intuition

- Example: A = 1,000 users, B = 50 impressions. Then
  `P(X = 0) = (1 - 1/1000)^50 ≈ e^{-50/1000} = e^{-0.05} ≈ 0.951`.
  So John has a ~95% chance of seeing zero impressions — unsurprising when impressions are scarce relative to the audience.

Useful approximation (Poisson)

When A is large and p is small (so Bp = B/A is moderate), you can use the Poisson approximation:

`P(X = 0) ≈ e^{-B/A}`

This often simplifies quick mental math in interviews.

When the assumption fails (say it’s without replacement or nonuniform)

- Without replacement (each impression is shown to a distinct user, B ≤ A): the correct model is hypergeometric. Then
  `P(X = 0) = C(A-1, B) / C(A, B)` (choose all B impressions from the other A−1 users).
- Nonuniform selection (some users have higher weight): replace `p` with John's actual selection probability; the count for John is still binomial if trials are independent and identical for John.
- If impressions are correlated (not independent), you must model that dependence explicitly.

Interview tips

- State your assumptions up front: independence, identical probability p, and whether selection is with or without replacement.
- Write the Binomial argument clearly: B trials, p = 1/A, P(0) = (1 - p)^B.
- Offer the hypergeometric alternative if the interviewer suggests "no user sees more than one impression."
- Mention the Poisson approximation for large-A, small-p regimes to show practical instinct.

Bottom line

“John gets 0 impressions” is neither mysterious nor hand-wavy: it’s the probability of B independent misses. State the setup, pick the right distribution, and compute `P(X = 0) = (1 - 1/A)^B`.

#Statistics #DataScience #InterviewPrep