---
title: "System Design Interview: Key Considerations in Designing a Banking System"
datePublished: Sat Jun 07 2025 17:16:45 GMT+0000 (Coordinated Universal Time)
cuid: cmd1zflxd000e02l278ar3t89
slug: system-design-interview-key-considerations-in-designing-a-banking-system-d778de40445d
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1752429760018/ba64e292-c036-4cf1-b49d-066f82830a1d.png

---

Designing a banking system requires a deep understanding of distributed systems, concurrency, consistency, and secure state management. Below, we unpack each major component with detailed implementation mechanics that underlie a robust and scalable system.

### 1\. Account Management

#### Designing for Multiple Account Types

A common strategy is to use inheritance or composition to model different account behaviors. A typical design:

AbstractAccount  
├── SavingsAccount  
├── CheckingAccount  
└── CreditAccount

Each subclass implements operations such as `withdraw()`, `deposit()`, and `calculateInterest()` differently.

However, using polymorphism at runtime requires thoughtful encapsulation of business rules. For example, withdrawals from a `CreditAccount` may need additional checks for credit limits. You may also want to represent account metadata in a normalized schema like this:

Accounts Table  
\- account\_id (PK)  
\- user\_id (FK)  
\- account\_type (ENUM: savings, checking, credit)  
\- status (ENUM: active, frozen, closed)  
\- balance  
\- interest\_rate

Interest accrual can be implemented via a scheduled background job that iterates over accounts, calculating:

This operation must be idempotent and track the last applied timestamp to avoid duplicate accruals.

interest = balance × interest\_rate × (days\_since\_last\_calculation / 365)

#### Ensuring Secure User Authentication

Authentication must be fail-safe and resilient to replay attacks and credential theft.

A typical mechanism stack:

*   **Password-based auth**: Store passwords hashed with salts using algorithms like `bcrypt` or `argon2`.
*   **Token-based sessions**: Issue short-lived JWTs, optionally rotating refresh tokens every N hours.
*   **MFA**: Implement TOTP-based second factors using RFC 6238. On server side, store the shared secret securely and validate tokens with a ±30s window.
*   **Session Hijack Protection**: Regenerate session identifiers on login and track device fingerprints or IP shifts.

Login flow example:

\[User submits credentials\] → \[Password Check\] → \[MFA Challenge\] → \[Token Issuance\]

All operations must be logged with traceable metadata (IP, User-Agent, geolocation if applicable).

#### Handling Account Operations

Operations like freezing an account should follow a **state machine** pattern. For example:

States: Active → Frozen → Closed  
Allowed Transitions:  
  Active → Frozen  
  Frozen → Active  
  Active/Frozen → Closed

This can be enforced via application logic or database triggers to ensure invariant consistency.

Implementing **event sourcing**? A log-based structure like this:

{  
  "event\_type": "ACCOUNT\_FROZEN",  
  "account\_id": "123",  
  "timestamp": "2025-04-04T10:00:00Z",  
  "metadata": { "reason": "Suspicious activity" }  
}

Each operation becomes an event, and the current state is derived by replaying all events. This enables temporal debugging (“What was the state at time T?”) and full auditability.

### 2\. Transaction Processing

#### Ensuring Transaction Consistency and Atomicity

Transactional correctness is critical. All operations must honor the **ACID** properties. For single-node systems, relational databases handle this inherently. For distributed or microservice systems, more nuance is needed.

*   **2PC (Two-Phase Commit)**:
*   **Prepare Phase**: All participants vote to commit or abort.
*   **Commit Phase**: Coordinator finalizes based on votes.
*   Downside: Can block if a participant crashes.
*   **Saga Pattern**: Each operation in a saga has a corresponding compensating transaction.

\[Debit A\] → \[Credit B\]  
     ↑           ↑  
\[Undo Debit A\] \[Undo Credit B

If credit fails, the saga invokes the “undo debit” step to maintain balance.

State transitions in the saga must be stored persistently so they can be resumed in case of failure (e.g., via a saga log table).

#### Managing Concurrent Transactions

Banking systems often run under high contention. For concurrency control:

*   **Optimistic Locking**: Add a `version` field to each row. During updates, use:
*   `UPDATE accounts SET balance = balance - 100, version = version + 1 WHERE account_id = 123 AND version = 7;`
*   If affected rows = 0, a concurrent modification occurred → retry.
*   **Pessimistic Locking**: Use row-level locks: `SELECT ... FOR UPDATE`. Best for high-value, low-volume updates.

Deadlock detection is essential. For example, always lock rows in a canonical order (e.g., ascending account\_id) to avoid cyclical waits.

#### Designing Real-Time Fraud Detection

A practical approach

1.  **Rule-based engine**: Fast filters like “more than X transactions in Y minutes”, or “transfer to blacklisted country”.
2.  **Streaming anomaly detection**:

*   Maintain rolling statistics per user (e.g., median transfer size, login time ranges).
*   Use distance metrics (Euclidean, Mahalanobis) to score outliers.

1.  **Feature extraction pipeline**: Convert raw events into structured features

*   `{ "txn_amount": 500, "hour_of_day": 23, "device_id_mismatch": true, "geolocation_change": true }`

Deploy lightweight models in a streaming architecture (e.g., per-user fraud score with thresholding) that raise alerts or block transactions temporarily.

### 3\. Data Storage and Security

#### Securing Stored Data

Use a **data encryption hierarchy**:

*   **Envelope Encryption**:
*   Each data record encrypted with a unique Data Encryption Key (DEK).
*   DEKs are encrypted with a Master Key.
*   Master Key stored in Hardware Security Module (HSM) or equivalent.

All sensitive fields (e.g., SSNs, card numbers) should be encrypted at column level.

Key rotation strategies must support *re-encryption in place* or *dual-decryption* (old + new key during transition).

#### Choosing the Right Database

**Relational databases** remain the gold standard for:

*   ACID transactions
*   Referential integrity
*   Strong schema enforcement

For **append-only systems** like logs or event stores:

*   Use wide-column or log-structured merge-tree stores (e.g., LevelDB-style architecture).
*   Benefits: fast sequential writes, compaction for reads.

Sharding by `user_id % N` can horizontally scale reads/writes while preserving locality per user.

#### Data Backup and Recovery

Backups must be:

*   **Incremental**: Store only diffs since last backup.
*   **Consistent Snapshots**: Use write-ahead logs to restore to a transactionally consistent state.
*   **Tested**: Regular DR drills to verify restore scripts.

Recovery point objective (RPO) and recovery time objective (RTO) should be defined per data tier.

### 4\. Scalability and Performance

#### Designing Load Balancing Mechanisms

Internal request routing can be layered:

*   **L7 load balancer**: Routes based on URL paths or headers (e.g., `/transactions → txn-service`)
*   **Connection-aware**: Sticky sessions via consistent hashing (`user_id % N`) ensure request affinity.

Maintain session state in a distributed cache if needed for sticky-less routing.

### Real-Time System Monitoring

Monitoring should capture:

*   Latency percentiles (P50, P95, P99)
*   Error rates per API route
*   Resource saturation (CPU, memory, disk IOPS)

Introduce **circuit breakers** for downstream service calls — stop retrying failing endpoints until they recover. This prevents cascading failures.

### Designing for Future Expansion

**Modular design** principles:

*   Services communicate via asynchronous messaging (e.g., publish-subscribe model)
*   Schema evolution handled via versioned contracts (e.g., `TransactionV1`, `TransactionV2` structs).
*   Database migrations performed in phases:
*   Add new fields (non-breaking)
*   Populate in background
*   Switch logic
*   Drop old fields

Full Answer: [https://bugfree.ai/practice/system-design](https://bugfree.ai/practice/system-design)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1752429758359/7c6165fe-250c-4d0f-89ae-866f2e7dd3f6.png)