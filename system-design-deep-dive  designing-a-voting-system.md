---
title: "System Design Deep Dive — Designing a Voting System"
datePublished: Sat May 10 2025 17:12:37 GMT+0000 (Coordinated Universal Time)
cuid: cmd1zftbh000b02jr8invhulq
slug: system-design-deep-dive-designing-a-voting-system-bff917dbdcd2
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1752429769731/df23a94e-078d-4192-b710-6a525473e313.png

---

### Key Considerations in Designing a Voting System

Designing a voting system involves much more than just building a web application — it requires solving problems related to identity, consistency under high load, data security, and trustworthiness. Below are the **core design areas** you must address and the **mechanisms** behind them.

System Design Diagram — Design a Voting System

### 1\. User Authentication & Authorization

### User Verification

At its core, user verification involves establishing a unique, verifiable identity per voter while preventing duplicates.

*   **Two-Factor Authentication (2FA)**  
     Internally, 2FA adds an additional verification step during login. After validating the password (typically using a salted hash like bcrypt), the server generates a one-time token (e.g., TOTP or SMS code). This token must match a value known only to the server and user’s device. Rate limiting and nonce tracking prevent brute force attacks.
*   **Biometric Verification**  
     Biometric inputs are typically matched against encrypted templates stored on-device or in a secure enclave. Instead of transmitting raw fingerprints, you hash and match biometric signatures using homomorphic encryption or local trusted environments to protect sensitive data.
*   **De-duplication**  
     A unique user must not be allowed to vote more than once. Behind the scenes, this could involve using a deterministic hash (e.g., SHA-256) of a national ID or social security number stored securely, with all operations occurring in constant time to prevent side-channel attacks.

### Role Management

Roles are enforced at every access point to the system using Access Control Lists (ACLs) or Role-Based Access Control (RBAC).

*   **RBAC Implementation**  
     Permissions are defined as a matrix: `Role x Resource -> Allowed Actions`. During request processing, middleware intercepts the user token, extracts roles, and checks the action against the matrix. This can be cached for performance.
*   **Dynamic Role Assignment**  
     This may be implemented using rules-based engines. For example: if a user performs more than N admin-like actions over M time units, the system may elevate privileges in a sandboxed scope and log the escalation. These decisions often use event logs or a streaming rules engine.

### Session Management

*   **Token-Based Authentication**  
     Rather than server-side sessions, use JWT (JSON Web Tokens) with short TTLs. The token includes the user ID, role, issued-at timestamp, and a digital signature. Since it’s stateless, the server doesn’t store anything — all validation occurs via public key signature verification.
*   **Session Monitoring**  
     Each token can be tagged with a session ID stored in a secure store like Redis. Actions are logged against this ID. Real-time monitoring services can flag if a single session ID appears from geographically distant IPs within a short window — triggering auto logout or CAPTCHA.

### 2\. Scalability & Performance

Voting systems experience sudden, short-lived, and highly spiky loads — often millions of concurrent users in a narrow time window. This section breaks down how to scale such a system predictably.

### 2.1 Handling High Traffic

#### Connection Handling and Rate Limiting

Before application logic is even executed, **connection-level limits** protect servers:

*   Use **connection pools** to avoid exhausting resources like DB threads.
*   Apply **rate limiting at the gateway or CDN level** using algorithms like:
*   **Token Bucket**: Allows bursts but enforces average throughput.
*   **Leaky Bucket**: Enforces strict rate over time, ideal for anti-spam.

For example, a rule like “max 10 requests/sec per IP” is enforced in the gateway. Internally, Redis or a lightweight in-memory store tracks tokens per IP.

#### Concurrency Management

Each vote request must be:

*   Accepted (queued),
*   Validated (check if user already voted),
*   Persisted (write to DB or log),
*   Acknowledged (send confirmation to user).

To avoid contention:

*   Use **message queues** (e.g., Kafka-style commit logs) to buffer incoming vote requests and process them sequentially per user ID or voting precinct (using consistent partitioning).
*   This decouples *write load* from *processing logic* and allows back-pressure.

#### Horizontal Scaling

All stateless services (auth, validation, vote submission) can scale horizontally by:

*   Keeping no session state in-memory.
*   Using a distributed cache (e.g., Redis or Memcached) for temporary session data.
*   Distributing traffic with a **load balancer** using **round-robin**, **least connections**, or **geo-aware routing**.

### 2.2 Data Consistency under Load

Voting systems require *write-heavy consistency*, unlike most read-optimized web apps. Key constraints:

*   **One person, one vote.**
*   **Votes must not be lost or duplicated.**

#### Write Serialization

Use **logical sharding** per precinct or region. For each shard:

*   Serialize writes using **single-writer queues** or **leader-election (e.g., Raft)**.
*   Within a shard, use distributed locks or optimistic concurrency control (OCC) to detect conflicts (e.g., if two votes from the same voter arrive at the same time).

#### Optimistic Locking vs. Pessimistic Locking

*   **Optimistic**: Read `has_voted=false`, attempt update with a version number or timestamp. If another write has occurred, reject and retry.
*   **Pessimistic**: Acquire lock on `voter_id`, write vote, release. Safer but lower throughput.

Use optimistic locking for scale and pessimistic for critical race-sensitive paths.

### 2.3 Read/Write Path Separation

Split your system into:

*   **Hot path**: Vote submission — needs strong consistency.
*   **Cold path**: Analytics, real-time dashboards — can tolerate eventual consistency.

Use **Command Query Responsibility Segregation (CQRS)**:

*   Write-heavy services write to master DB and publish events.
*   Read replicas or materialized views update asynchronously.

This enables **real-time dashboards** to scale independently without affecting vote integrity.

### 2.4 Caching Strategies

#### Types of Cached Data

*   **User session tokens**
*   **Public vote count (read-only, eventually consistent)**
*   **Polling station metadata**
*   **Voter eligibility rules (frequently read, rarely written)**

#### Cache Coherency

Maintaining consistency between cache and DB is hard at scale:

*   **Write-through cache**: Writes go to DB and cache together. Ensures consistency but adds latency.
*   **Write-around cache**: Writes go to DB only, reads populate the cache. Improves write throughput but stale reads possible.
*   **Write-back cache**: Writes go to cache, flushed to DB later. High risk in mission-critical systems like voting — generally **not recommended**.

For vote-related data, use **write-through** or **no-cache** at all — correctness is paramount.

### 3\. Data Storage & Management (Expanded)

Voting data is critical infrastructure — **accuracy, durability, traceability, and verifiability** are non-negotiable.

### 3.1 Database Selection & Design

#### Core Data Model

Use **relational databases** for high-integrity data. Tables might include:

VOTERS (  
  voter\_id UUID PRIMARY KEY,  
  name TEXT,  
  precinct\_id TEXT,  
  has\_voted BOOLEAN DEFAULT false  
)

VOTES (  
  vote\_id UUID PRIMARY KEY,  
  voter\_id UUID REFERENCES VOTERS(voter\_id),  
  candidate\_id TEXT,  
  timestamp TIMESTAMP,  
  location TEXT  
)

*   Enforce `UNIQUE (voter_id)` in `VOTES` to prevent duplicates.
*   Use foreign keys to maintain referential integrity.
*   Use indexes on `precinct_id`, `candidate_id` for tally queries.

#### Why Not NoSQL for Vote Casting?

*   NoSQL lacks strong ACID guarantees by default.
*   Even with configurable consistency (e.g., quorum reads/writes in Cassandra), you’re trading performance for complexity.
*   For mission-critical voting paths, use **PostgreSQL** or **MySQL with strict isolation (Serializable level)**.

Use **NoSQL** for:

*   Logs (`vote_cast` events)
*   Audit trails
*   High-throughput analytics pipelines

### 3.2 Write Guarantees and Idempotency

Vote submission must be **idempotent** — even if a user retries due to network failure, the vote must only be counted once.

Mechanism:

*   Each vote carries a **deduplicated idempotency token** (e.g., UUID or hash of `voter_id + election_id`).
*   Store vote with this token. If token exists, reject or return the same response.

This avoids double counting due to retries or race conditions.

### 3.3 Auditability and Tamper-Proofing

#### Immutable Audit Logs

Implement **append-only logs** per voting event:

*   Use write-once, read-many storage (WORM).
*   Use **hash chains**: every entry contains hash of previous log + current data.
*   Periodically checkpoint these logs (e.g., every 10,000 votes) and sign the checkpoint with a private key. This makes tampering evident.

#### Merkle Trees for Tally Verification

Each vote can be inserted into a Merkle tree:

*   Root hash is stored on-chain or in public bulletin board.
*   Anyone can verify that a vote exists in the tree without revealing the vote contents (zero-knowledge proof techniques can enhance privacy).

This adds cryptographic auditability.

### 3.4 Redundancy, Backups, and Disaster Recovery

#### Multi-Zone & Multi-Region

*   Use **leader-follower replication** across zones.
*   Sync using logical replication (stream WAL logs) to read replicas.
*   In cross-region DR setups, async replication is acceptable — data loss of a few seconds can be mitigated with idempotent design.

#### Backups

*   **Full snapshot daily**, **incremental every 5–10 minutes**.
*   Store backups in isolated, immutable storage with checksums.
*   Backup verification job runs nightly: restores backup into a sandbox, runs consistency checks.

#### Disaster Recovery Testing

*   Run regular chaos drills: disable primary DB, simulate network partition, verify failover.
*   Use infrastructure as code (e.g., Terraform) to spin up fresh environments in case of regional failure.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1752429768012/c79fddea-203d-4427-a0f8-6a97b34c6dca.png)

System Design Answer — Design a Voting System

Full Answer: [https://bugfree.ai/practice/system-design/voting-system/solutions/BbJ9EbA2sXL2C4xc](https://bugfree.ai/practice/system-design/voting-system/solutions/BbJ9EbA2sXL2C4xc)