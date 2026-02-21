---
title: "Stop Overthinking User Test Selection: It’s Just a Geometric Waiting Time"
seoTitle: "Stop Overthinking User Test Selection — Use the Geometric Waiting Time"
seoDescription: "Model days-until-selection as geometric: p=0.001 ⇒ mean wait 1/p = 1000 days (~2.7 years). Say “constant p ⇒ geometric” in interviews."
datePublished: Sat Feb 21 2026 18:45:53 GMT+0000 (Coordinated Universal Time)
cuid: cmlwo64iw000102kwhs6eb1jz
slug: stop-overthinking-user-test-selection-geometric-waiting-time
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771699530131.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771699530131.png

---

# Stop Overthinking User Test Selection: It’s Just a Geometric Waiting Time

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771699530131.png" alt="Geometric waiting time diagram" width="600" />

TL;DR: If each day a user has the same chance p of being picked, the number of days until that user is first selected follows a geometric distribution. Memorize the key rule: E[wait] = 1/p. For p = 1000/1,000,000 = 0.001, the average wait is 1/0.001 = 1000 days (~2.7 years).

## Problem setup

Imagine an interviewer asks: "A service randomly chooses 1,000 users each day from a population of 1,000,000. How long until a given user is selected?"

Assumptions implicit in the simplest model:
- Each day is an independent trial.
- The per-day selection probability for that user is constant (p = 1000 / 1,000,000 = 0.001).
- Sampling is effectively with replacement relative to an individual user (the population is large and daily draws don't materially change p).

When those hold, the waiting time (measured in days) until the first selection is geometric.

## The geometric solution (the piece you should say in an interview)

- PMF: P(T = k) = (1 - p)^(k-1) * p
- Mean: E[T] = 1 / p
- Memoryless property: P(T > n + k | T > n) = P(T > k)

Plugging numbers: p = 0.001
- Expected wait: E[T] = 1 / 0.001 = 1000 days (~2.7 years).
- Probability selected on day 1: p = 0.001 (0.1%).
- Probability selected within 365 days: 1 - (1 - p)^365 ≈ 30.6%.
- Probability selected within 1000 days: 1 - (1 - p)^1000 ≈ 1 - e^{-1} ≈ 63.2%.

Quick intuition: constant, independent daily chance ⇒ "each day is a fresh coin flip" until the first success. That is exactly the geometric scenario.

## When this model breaks

The geometric model is the right first answer for interview-level reasoning, but note possible caveats in real systems:
- If draws are strictly without replacement at the population level and the population is small, you'd use a negative-hypergeometric or something similar. For very large populations and small daily samples, the geometric approximation is excellent.
- If p changes over time (e.g., the user is more/less likely on certain days), the simple geometric model no longer applies.

## Interview tip

Say: "Since each day is an independent trial with constant p, the days-until-first-selection is geometric. So E[wait] = 1/p, which here gives 1000 days." Saying the constant-p ⇒ geometric connection quickly demonstrates you know the right model.

## Takeaway

Stop overcomplicating it: when you can justify constant per-trial success probability, use the geometric distribution. Memorize E[T] = 1/p and the PMF; that combination solves many quick interview questions.

#DataScience #Statistics #InterviewPrep
