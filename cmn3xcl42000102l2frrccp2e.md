---
title: "Expedia SDE-2 Interview Experience — DSA Wins, Password Manager LLD Lessons"
seoTitle: "Expedia SDE-2 Interview Experience — DSA Success, LLD Lessons"
seoDescription: "Expedia SDE-2 interview recap: DSA rounds aced but LLD (password manager) lacked clarity. Key lesson: master end-to-end low-level design."
datePublished: Tue Mar 24 2026 01:16:56 GMT+0000 (Coordinated Universal Time)
cuid: cmn3xcl42000102l2frrccp2e
slug: expedia-sde-2-interview-dsa-lld-password-manager
cover: https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587
ogImage: https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587

---

<img src="https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587" alt="Expedia Interview" style="max-width:800px; width:100%; height:auto; display:block; margin:0 auto 1rem;" />

## Overview

A Bugfree user shared a high-score interview experience for Expedia SDE-2 (Bengaluru). Candidate profile: ~3 years of experience, interviewed via referral. The on-site/process had four rounds in total (note: no HLD round for SDE-2). The final two rounds were scheduled only after clearing the first two.

Quick summary of rounds:

- R1 (DSA): 2 problems — a string problem and a sliding-window problem.
- R2 (DSA): A rod-cutting DP variant and a tree problem; got positive feedback.
- R3 (LLD): Design a password manager (create/edit/forgot flows), token generation, password policies. Used SOLID principles and patterns (Singleton / Strategy / Observer), but feedback was weak.
- R4 (Manager): Deep resume dive plus scenario questions on distributed systems.

Outcome: Rejected. The stated reason: weaker LLD feedback. Key lesson: strong DSA is necessary but not sufficient — end-to-end clarity in low-level design matters.

---

## What happened in each round (details & takeaways)

### Round 1 — DSA
- Problems: one string problem and one sliding-window problem.
- Takeaway: Classic pattern recognition (sliding window) and careful implementation win here. Focus on clean code and test edge cases.

### Round 2 — DSA
- Problems: rod-cutting dynamic programming variant and a tree problem.
- Outcome: Received positive feedback. DP and tree fundamentals were handled well.
- Takeaway: Practice variants of standard DP problems and common tree traversals/transformations.

### Round 3 — Low-Level Design (LLD)
- Prompt: Design a password manager supporting create, edit, forgot-password flows; design token generation and password policy enforcement.
- Approach used: Applied SOLID principles and patterns (Singleton, Strategy for policies, Observer for notifications). However, feedback suggested the design lacked clarity or end-to-end completeness.
- Likely gaps: API contracts, data models, token lifecycle/expiry, encryption/storage details, failure modes, scaling considerations, and clear flow diagrams.
- Takeaway: In LLD you must be explicit and cover the whole flow — request/response shapes, database schema, sample APIs, edge cases, and how components interact in failure scenarios.

### Round 4 — Manager Round
- Focus: Deep resume walkthrough and scenario-based questions (distributed systems, tradeoffs, operational concerns).
- Takeaway: Be ready to justify design decisions, discuss tradeoffs, and show ownership and impact from your prior work.

---

## Why the rejection (and what to improve)

The candidate performed well on algorithmic rounds but the LLD round lacked the end-to-end clarity interviewers expect. For SDE-2, interviewers want to see:

- Clear API design and contracts (request/response examples)
- Concrete data model and schema decisions (tables/fields, indexes)
- Security considerations (encryption at rest/in transit, token structure)
- Token lifecycle: generation, storage, validation, expiry, revocation
- Error handling and edge cases (concurrent edits, rate limits)
- Component interactions and sequence flows (how requests move across services)
- Reasoned tradeoffs and complexity estimates

In short: DSA correctness helps you get to later rounds, but LLD communication and completeness often decide the outcome.

---

## Actionable prep checklist

- DSA
  - Practice sliding window, DP variants, and tree problems.
  - Write correct, testable code; narrate complexity and edge cases.

- LLD
  - Practice end-to-end designs for small services: auth, payments, notifications, password management.
  - Always draw a sequence diagram or step-by-step flow.
  - Define APIs (example request/response), DB schema, and important indexes.
  - Explain security: hashing, salting, encryption, token format (JWT vs opaque), refresh/revocation.
  - Discuss failure modes, scaling (caching, sharding), and monitoring/alerts.
  - Use SOLID and design patterns where they add clarity, but avoid overusing patterns for their own sake.

- Manager/Behavioral
  - Prepare a concise resume walkthrough: technical decisions, tradeoffs, measurable outcomes.
  - Expect scenario questions on system reliability, scaling, and team processes.

---

## Example checklist for the Password Manager LLD

1. Scope: create/edit/forgot-password flows, token generation & validation, password policy enforcement.
2. APIs: POST /users, PUT /users/{id}/password, POST /auth/forgot, POST /auth/reset
3. Data model: Users table (id, email, password_hash, salt, reset_token, reset_expiry, created_at)
4. Security: bcrypt/argon2 for hashing, TLS in transit, encrypt sensitive fields at rest.
5. Token: use opaque reset tokens stored server-side (or signed JWT with short expiry + revocation list).
6. Flow: diagram the forgot -> send token -> validate token -> reset password -> invalidate token.
7. Edge cases: multiple reset requests, token reuse, expired tokens, brute-force protection, rate limiting.
8. Observability: logs (no plaintext secrets), metrics on reset attempts, alerts on spikes.

---

## Final takeaway

Cracking DSA problems is essential to move forward, but for SDE-2 roles you must pair algorithmic strength with crisp, end-to-end low-level design communication. Practice small-service LLDs with concrete APIs, data models, token flows, and failure scenarios — and narrate them clearly during the interview.

Good luck — focus on clarity and completeness for LLD, and the rest will fall into place.

#SoftwareEngineering #InterviewPrep #SystemDesign