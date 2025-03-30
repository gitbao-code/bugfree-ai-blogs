---
title: "Meta Mock System Design Interview: Top-K Request Analysis System"
datePublished: Thu Jan 09 2025 01:28:04 GMT+0000 (Coordinated Universal Time)
cuid: cm8vzx9sn000408lb8t76gwbh
slug: meta-mock-system-design-interview-top-k-request-analysis-system-8f181aa06e78
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1743360657562/c3bdb989-12e0-4f27-9e45-01217de973fa.png

---

This time, the mock interview is with a friend from Meta who is a senior engineer. Since it’s the end of the year and PSC season, it’s time to start preparing just in case. 😂

The topic this time is **Top K**, a classic data processing problem. The Engineer has covered a lot of topics across different domains, and while in real interviews, it is recommended to focus 3–4 and do a deepdive.

System Design Diagram — Design a Top-K Request Analysis System

### **Data Collection & Aggregation**

#### Efficient Data Collection

To efficiently collect data from multiple sources in real-time, the system must focus on:

*   **Ingestion Pipelines**: Establishing a distributed data ingestion mechanism ensures the system can handle high data volumes. This involves:
*   **Message Queuing**: Data is captured via producers and queued for consumption. Using partitioning strategies (e.g., hashing based on request type or origin) ensures even load distribution.
*   **Schema Validation**: A schema definition enforced at the producer and consumer ends ensures consistency. Implement schema evolution strategies to accommodate changes without breaking downstream systems.

#### **Data Validation and Deduplication**:

*   Validate incoming data to filter out malformed or irrelevant records early.
*   Deduplication mechanisms based on unique keys (e.g., timestamp and request ID combination) prevent redundant processing.

#### **Fault Tolerance**:

*   Employ a distributed storage buffer to handle system failures, ensuring that data is not lost during processing or ingestion bottlenecks.

### Data Aggregation Strategies

Identifying Top-K requests in real-time requires efficient aggregation:

#### **Sliding Window Aggregation**

*   The sliding window technique processes data in fixed-size intervals while allowing partial overlap. For example, a 5-minute window sliding every minute ensures recent data visibility.
*   To optimize processing, pre-aggregate partial results in smaller windows, combining these results at higher intervals to form complete aggregations.

#### **Data Structures for Top-K Computation**:

*   **Heap-based Approach**: A min-heap of size K maintains the Top-K elements. For every new data point, compare and replace elements in the heap if the new value qualifies.
*   **Count-Min Sketch**: For approximate results, this probabilistic data structure provides low memory overhead and fast updates by hashing requests into a frequency table.

#### **Distributed Aggregation**:

*   Shard data by key (e.g., request type) across nodes. Each shard performs local aggregation, and a centralized reducer combines these results to compute the global Top-K.

### System Scalability

The system must dynamically adapt to changing workloads. Key design strategies include:

#### **Partitioning and Sharding**

*   Partition data based on request characteristics (e.g., user ID, geolocation) to evenly distribute the load across nodes.
*   Employ consistent hashing to minimize rebalancing when nodes are added or removed.

#### **Dynamic Scaling**:

*   Monitor system metrics (e.g., CPU, memory usage, request rate) to trigger scaling actions.
*   Use techniques like auto-splitting of partitions or horizontal scaling by adding more processing nodes.

#### **Load Balancing**:

*   Route incoming data intelligently to prevent bottlenecks. Adaptive load balancing, guided by real-time monitoring, can redirect traffic to underutilized nodes.

### Performance Optimization

#### **In-Memory Processing**:

*   Use in-memory data structures for frequently accessed data to reduce latency. Priority queues, hash maps, and prefix trees (trie) are efficient options for real-time lookups.

#### **Batch vs. Stream Processing**:

*   Combine real-time stream processing for immediate insights with periodic batch jobs for larger-scale aggregations and accuracy.

#### **Optimized Query Execution**:

*   Use indexed data storage to speed up query lookups.
*   Shard and partition data across multiple nodes to distribute query load and reduce latency for large datasets.

### Data Storage Model

#### **Column Databases for Analytics**:

*   Store data in a column-oriented format for efficient aggregation and filtering during queries.
*   Partition by time (e.g., hourly, daily) for quicker range scans in historical analysis.

#### **Indexing Strategies**:

*   Use composite indexes for multi-dimensional queries (e.g., by time and request type).
*   Employ bitmap indexes for categorical data to speed up aggregations.

#### **Replication and Consistency**:

*   Replicate data across nodes for fault tolerance, and choose consistency levels (e.g., eventual vs. strong consistency) based on real-time requirements.

### Data Cleanup and Retention

Implement lifecycle policies to manage storage efficiently:

#### **Retention Policies**:

*   Define rules to archive or delete older data (e.g., retain only the past 30 days for real-time analysis).
*   Use compaction to merge small files into larger blocks for storage optimization.

#### **Archival Storage**:

*   Move infrequently accessed data to low-cost archival storage, ensuring it remains accessible for historical analysis.

### **Real-Time Analysis**

#### **Stream Processing Framework**:

*   Employ a distributed stream processing mechanism that ingests, aggregates, and emits results in near real-time.
*   Utilize parallel execution to process multiple streams concurrently, reducing latency.

#### **Efficient Top-K Updates**:

*   Incrementally update Top-K results as new data arrives, avoiding re-computation of the entire dataset.
*   Use windowed joins to correlate real-time streams with historical reference data for context-aware analysis.

### Reporting and Visualization

#### **Aggregation Layers**:

*   Separate raw data processing from aggregation layers. Store pre-aggregated results for quick retrieval and rendering in dashboards.

#### **User-Friendly Dashboards**:

*   Use intuitive visualization techniques such as bar charts, heatmaps, and real-time leaderboards.
*   Enable user-defined filters and drill-down capabilities to explore data interactively.

#### **Alerting Mechanisms**:

*   Implement threshold-based alerts (e.g., if a request type exceeds a certain frequency) to notify users of anomalies or trends in real-time.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360654679/9c79bac2-4b75-49d8-894a-209e2dc66381.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360656111/b54c0912-3013-4fbe-802f-fee7d1cfc8fa.png)

System Design Solution — Design a Top-K Request Analysis System

Full Answer: [https://bugfree.ai/practice/system-design/top-k-analysis/solutions/KuOkqlrh2jmPQl\_n](https://bugfree.ai/practice/system-design/top-k-analysis/solutions/KuOkqlrh2jmPQl_n)