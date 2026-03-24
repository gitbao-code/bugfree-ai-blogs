---
title: "High-Score Interview Experience: Expedia SDE-2 (3 YOE) — DSA Wins, Password Manager LLD, Manager Round"
seoTitle: "Expedia SDE-2 Interview Experience: DSA Wins & Password Manager LLD Lessons"
seoDescription: "Expedia SDE-2 interview recap (3 YOE): DSA success, password-manager LLD pitfalls, manager round insights and actionable takeaways."
datePublished: Tue Mar 24 2026 01:16:07 GMT+0000 (Coordinated Universal Time)
cuid: cmn3xbj6c000002jmfwym2kce
slug: expedia-sde-2-interview-dsa-password-manager-lld-takeaways
cover: https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587
ogImage: https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587

---

<img src="https://hcti.io/v1/image/019d1d68-e330-7ecf-a292-fe00acaf0587" alt="Expedia Interview" width="800" style="max-width:100%;height:auto;border-radius:8px;" />

# High-Score Interview Experience: Expedia SDE-2 (3 YOE)

A Bugfree user shared a condensed recap of their Expedia SDE-2 interview (Bengaluru) after ~3 years of experience and a referral. The process had four rounds, with the last two scheduled only after clearing the first two. There's no HLD for SDE-2 in this loop.

This post summarizes the rounds, what went well, what didn’t, and practical takeaways—especially around why strong DSA alone didn't secure an offer.

## Quick overview

- Role & location: Expedia SDE-2 (Bengaluru)
- Experience: ~3 years (referral)
- Rounds: 4 total (R1 DSA, R2 DSA, R3 LLD, R4 Manager)
- Note: Last two rounds were scheduled only after clearing R1 and R2
- Outcome: Rejected (feedback pointed to LLD clarity)

---

## Round-by-round breakdown

### R1 — DSA
- Two problems: a string problem and a sliding-window problem.
- Result: Cleared.
- Tips: Communicate approach, consider edge cases, and write clean code. Sliding-window problems reward careful window boundary handling and complexity justification.

### R2 — DSA
- Problems: a rod-cutting DP variant and a tree problem.
- Result: Positive feedback & cleared.
- Tips: For DP, clarify recursion vs iterative, memoization, and complexity. For trees, be explicit about traversal order and base cases.

### R3 — LLD (Low-Level Design)
- Task: Design a password manager supporting create/edit/forgot flows, token generation, and password policies.
- Approach used: SOLID principles and patterns (Singleton, Strategy, Observer).
- Interviewer feedback: Not strong enough — judged to be lacking end-to-end clarity.

What was expected but possibly missed:
- Clear API surface and request/response shapes for key flows (create, update, reset)
- Concrete data model showing how passwords/tokens/policies are stored
- Security details: hashing, salting, encryption at rest, rotation, and secure recovery flows
- Token lifecycle: generation, expiry, refresh, revocation
- Error handling and edge cases (expired/invalid token, rate limits, concurrent writes)
- Scaling and storage choices (when to use DB vs KVS, sharding, caching)
- Sequence diagrams showing interactions (client, auth service, DB, notification service)

### R4 — Manager round
- Focus: Deep resume dive and scenario questions on distributed systems and tradeoffs.
- Tips: Be ready to discuss design decisions from your resume, scalability trade-offs, and how you'd operate/monitor systems in production.

---

## Outcome & primary lesson

Although the candidate performed well on DSA rounds, the interview ended in rejection based on LLD feedback. Key takeaway: strong DSA skills are necessary but not sufficient. For SDE-2 roles, clarity and completeness in end-to-end LLD matters.

---

## Actionable LLD checklist (for the password manager and similar designs)

1. Scope & assumptions
   - Start by stating what you will and won’t cover (e.g., browser/extension/CLI clients, enterprise features).
2. API design
   - Define endpoints and payloads for Create Password, Update, Get (with masking), Request Reset, Confirm Reset.
   - Example: POST /v1/passwords { userId, name, secret, policyId }
3. Data model
   - Tables/collections for Users, PasswordEntries, Policies, Tokens, AuditLogs.
   - Show relevant fields (e.g., secretHash, salt, iv, createdAt).
4. Security & crypto
   - Hash secrets with a strong KDF (bcrypt/Argon2) + salt; encrypt secrets at rest with a key management system (KMS).
   - Discuss key rotation and access controls.
5. Token lifecycle
   - Access tokens vs. reset tokens: generation, TTL, revocation, one-time tokens for reset flows.
6. Policies & validation
   - Enforce password policies (length, complexity, reuse restrictions) and rate limits for sensitive endpoints.
7. Workflows & sequence diagrams
   - Show steps for create, update, forgot-reset flows (client → auth service → KMS → DB → email/SMS service).
8. Consistency & concurrency
   - Locking strategies or optimistic concurrency for edits; idempotency for critical ops.
9. Scaling & storage choices
   - When to cache, read replicas, sharding by user ID, and using a separate key-value store for tokens.
10. Operational concerns
   - Metrics, logging, alerting, rollbacks, and disaster recovery.
11. Testing & privacy
   - Unit tests, integration tests, and privacy considerations (masking PII in logs).

Use this checklist as a mental template during interviews and explicitly walk the interviewer through these sections.

---

## Practical tips to improve LLD clarity

- Start with a one-paragraph summary of your system.
- Draw the core components and data flow quickly (sequence or component diagram).
- Define key APIs and the data model early.
- Explain how security is applied end-to-end (transport, auth, storage, rotation).
- Discuss failure modes and your mitigation strategies.
- Use examples: sample payloads, token formats, TTL values.
- Keep the interviewer engaged: ask clarifying questions and confirm assumptions.

---

## Suggested resources for focused practice

- System Design Primer (GitHub) — practical examples and templates
- Grokking the System Design Interview — for high-level design patterns (note: complement with low-level practice)
- Practice LLD problems (design a ticketing system, notification service, secret manager) with peers or mock interviews
- Read up on crypto basics relevant to password management (Argon2, KMS, key rotation)

---

## Final thoughts

This interview story is a useful reminder: solving algorithmic problems is vital, but for mid-level SDE roles you must also clearly communicate a secure, end-to-end design. Practice LLD with the checklist above, and treat each LLD like a short specification: define APIs, data models, security, failure modes, and scaling considerations.

If you want, I can:
- Draft a sample LLD answer for the password manager (APIs + data model + sequence diagram text)
- Provide a targeted study plan for the next 4 weeks

Good luck — DSA wins you the interviews, LLD helps you win the role.