---
title: "System Design with Meta Senior Eng— Design Meeting Room Booking System"
datePublished: Sat Dec 21 2024 23:13:34 GMT+0000 (Coordinated Universal Time)
cuid: cm5bulth4000h09l7af219j4t
slug: system-design-with-meta-senior-eng-design-meeting-room-booking-system-780675db8d08
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1735612055108/012d7060-10a3-4768-9298-84d29f3cae19.png

---

The mock interview is with a Meta Senior Eng, it is good that the engineer bought up most of the key points of the system design problem.

System Design Diagram — Design a Conference Room Booking System

Key points as followings:

### 1\. Availability and Scheduling

#### Room Availability

Real-time room availability must reflect accurately across all users and clients.

**Real-Time Updates:**

*   Implement a **publish-subscribe model** where changes in room availability (e.g., a new booking, cancellation, or modification) are published as events.
*   Maintain an in-memory **distributed event queue** to propagate these events to all subscribed clients. This ensures updates are pushed immediately, reducing polling overhead.
*   Synchronize changes across a distributed system using **consensus protocols** like Paxos or Raft to ensure consistency when multiple servers are handling room states.

**Centralized Availability State:**

*   Store availability data in a high-performance in-memory database. For each room, maintain a record of current bookings indexed by time slots.
*   Use atomic operations to update this state, ensuring that simultaneous attempts to book the same room are handled in a thread-safe manner.

**Calendar Integration:**

*   Design an abstraction layer for calendar management, where each user’s personal schedule and room bookings are merged.
*   Use a conflict-resolution mechanism (detailed below) to handle overlapping entries when merging schedules dynamically.

#### Conflict Resolution

Efficient conflict detection and resolution are critical for ensuring data integrity during booking operations.

**Automated Conflict Detection:**

*   Implement a **range-based query system** to check for overlaps. When a user attempts a booking, query the room’s schedule for the desired time range.
*   Ensure the query operation is transactionally consistent, using **row-level locking** to prevent race conditions in overlapping time checks.
*   Use a **quorum-based write mechanism** to confirm that the booking does not conflict across distributed nodes before committing.

**Resolution Mechanisms:**

*   Suggest alternative time slots or rooms by:
*   Querying adjacent time slots for availability in the same room.
*   Identifying nearby rooms with similar configurations within the same time slot.
*   Maintain a scoring mechanism for alternatives, considering proximity, user preferences, and historical booking patterns, to rank suggestions.

#### Time Zone Handling

Time zones are a complex aspect, especially for systems used globally.

**Time Zone Storage:**

*   Store all booking times in a universal format, such as UTC, in the backend.
*   Include metadata about the user’s local time zone with each request, allowing the backend to interpret and store times correctly.

**Conversion Mechanisms:**

*   At the display layer, calculate the user’s local time by applying timezone offsets and daylight saving rules.
*   Maintain a precomputed offset table for common time zones to optimize conversions during runtime.

### 2\. User Management and Access Control \[Optional\]

Note: This topic is optional if you are not familiar to user access control.

#### User Roles

Role-based permissions define access and functionality for different users.

**Role Management:**

*   Create a database schema where roles are stored as distinct entities, each associated with a set of permissions.
*   Implement an **access control matrix** that maps roles to resources (e.g., rooms, schedules) and actions (e.g., read, write, delete).

**Dynamic Role Assignment:**

*   Assign roles dynamically based on user context. For example, grant elevated privileges temporarily when a user is designated as an administrator for a specific room or resource.

#### Authentication and Authorization

User authentication ensures secure access, while authorization enforces permissions.

**Authentication Mechanism:**

*   Use hashed credentials and store salted hashes in the database. During login, verify the credentials by hashing the input and comparing it to the stored value.
*   Manage user sessions with signed tokens that include an expiration time to minimize security risks from stale sessions.

**Authorization Logic:**

*   Evaluate user permissions at each endpoint by checking the token against the **access control matrix**.
*   Implement a hierarchical evaluation where permissions can cascade (e.g., an organization admin inherits all permissions of a room admin).

#### Guest Access

External users often require temporary, limited access.

**Time-Limited Access Tokens:**

*   Generate unique, non-reusable access tokens for guests with embedded metadata, such as expiration times and allowed actions.
*   Store a server-side record of issued tokens for validation, ensuring the system can revoke or expire tokens when necessary.

**Scoped Permissions:**

*   Define a minimal set of actions (e.g., view-only) that guests can perform. Include this scope in the token payload to ensure compliance across the system.

### 3\. Scalability and Performance

#### Load Handling

The system must maintain consistent performance even under high traffic.

**Request Distribution:**

*   Use a **hash-based partitioning scheme** to distribute requests across multiple servers. For example, partition rooms by IDs to ensure that related requests are handled by the same server.
*   Maintain a routing table at the entry point of the system to direct incoming requests to the appropriate partitions.

**Dynamic Resource Allocation:**

*   Monitor system load using metrics such as response time, request rates, and resource usage. Dynamically provision additional resources (e.g., servers or threads) when predefined thresholds are exceeded.

#### Database Optimization

Efficient data access ensures minimal latency during operations.

**Indexing Strategies:**

*   For booking data, use **composite indexes** on room ID and time range fields to enable efficient range queries.
*   Periodically analyze query patterns and optimize indexes based on frequency and complexity.

**Data Partitioning:**

*   Partition the booking table by date or region to limit the size of individual partitions. This ensures faster lookups and reduces contention.

#### Horizontal Scaling

Scaling the system horizontally allows it to handle increased demand.

**Stateless Services:**

*   Design services to be stateless, with all session or user-specific data stored in a distributed session store or included in requests. This allows any instance of a service to handle any request.

**Data Replication:**

*   Implement **asynchronous replication** for read-heavy workloads. For example, replicate room availability data across nodes, with updates propagated asynchronously to ensure consistency.

### 4\. Notifications and Reminders

#### Notification Channels

Effective notifications require real-time and scheduled delivery mechanisms.

**Real-Time Delivery:**

*   Use a **message queue system** to handle notification events. Producers (e.g., booking services) enqueue messages, and notification workers consume them to send notifications.
*   Maintain user-specific delivery preferences in a lookup table, ensuring that messages are sent via the preferred channel (e.g., email, SMS).

**Failover Mechanisms:**

*   Implement retry logic for undelivered notifications. Store pending messages in a queue and periodically attempt re-delivery.

#### Reminder Scheduling

Reminders improve user engagement by prompting timely actions.

**Batch Processing:**

*   Use a background job scheduler to periodically query upcoming bookings and send reminders in batches, reducing the system’s real-time load.
*   Store reminder configurations (e.g., timing and method) alongside booking details for easy retrieval.

**Dynamic Timing:**

*   Calculate optimal reminder times based on booking details. For example, for meetings involving multiple time zones, send reminders adjusted to each participant’s local time.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735612053607/352bea44-c816-4ef2-81a0-8c2f56685f92.png)

System Design Solution — Design a Conference Room Booking System