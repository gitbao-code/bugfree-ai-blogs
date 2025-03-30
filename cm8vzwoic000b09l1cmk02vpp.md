---
title: "Snapchat System Design: Design a Yelp-like System"
datePublished: Fri Feb 07 2025 18:32:13 GMT+0000 (Coordinated Universal Time)
cuid: cm8vzwoic000b09l1cmk02vpp
slug: snapchat-system-design-design-a-yelp-like-system-8ab8885680be
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1743360630248/90c6537c-e7b5-4636-9259-7ef85c79503e.png

---

This is one of the interview my student encountered. Building a system akin to Yelp requires addressing multiple complex technical challenges, including efficient search, personalized recommendations, scalability, data consistency, and system reliability. This document delves into the underlying mechanisms that make such a system function effectively.

System Design Diagram — Design Yelp

### System Performance and Scalability

**Distributed Architecture**

*   **Microservices-Based Approach**: Yelp-like platforms handle a wide range of functionalities, from user authentication to search and reviews. A microservices architecture decouples these services, enabling independent scaling and maintenance. For instance, the review service can be scaled separately from the business listing service, which helps manage load during high traffic events like a restaurant week when reviews spike.
*   **Stateless APIs**: By designing APIs to be stateless, the system can distribute requests evenly across multiple instances, which is crucial for handling millions of daily queries without bottlenecks. If a server instance fails, another instance can seamlessly take over without losing user data, enhancing system reliability.
*   **Service Discovery & Load Balancing**: Services like Consul or Eureka can dynamically locate available microservices, ensuring requests are routed to healthy instances. This is essential for a Yelp-like system, where user-generated content must be processed in real time, and delays could degrade user experience. Load balancers ensure that no single service instance is overwhelmed, maintaining consistent response times.

**Database Scaling**

*   **Sharding**: Yelp must store and query vast amounts of business data, reviews, and user profiles. Sharding the database based on geographic location (e.g., state or city) minimizes query times for location-specific searches. This approach is crucial to ensure that a user searching for restaurants in San Francisco isn’t impacted by data queries for New York restaurants.
*   **Replication**: To provide a fast, reliable user experience, Yelp can use read replicas across different geographical regions. This reduces latency for read-heavy operations, such as viewing business details or reading reviews, by routing requests to the nearest replica instead of the primary database.
*   **CQRS (Command Query Responsibility Segregation)**: By separating the write operations (e.g., posting a review) from read operations (e.g., retrieving business details), Yelp can optimize its data storage according to usage patterns. The write model can be optimized for consistent updates, while the read model is tuned for low-latency queries, crucial for delivering a snappy user experience.

**High Availability & Fault Tolerance**

*   **Replication & Redundancy**: For a system as large as Yelp, any downtime can significantly impact users and businesses. Implementing replication across multiple data centers ensures data availability even in case of hardware failures. Leader-follower replication allows a quick failover mechanism, which is essential to keep the service running without interruptions.
*   **Circuit Breakers & Rate Limiting**: Yelp needs to ensure that a spike in traffic (e.g., a viral post about a restaurant) does not crash the system. Circuit breakers help detect service failures and prevent cascading failures across dependent services. Rate limiting protects the system from abusive behavior, such as bots scraping data or users overwhelming the API with requests.

**Caching Strategies**

*   **Read-heavy Data Caching**: For a platform like Yelp, users frequently access popular business listings and reviews. Caching this data in memory (using Redis or Memcached) significantly reduces database load and improves response times, especially during peak hours.
*   **Write-through & Write-back Policies**: When a user posts a review, the data can be updated in the cache (write-through) to ensure consistency across read requests. This approach ensures that users immediately see their submitted reviews without having to wait for database updates.
*   **Cache Invalidation**: To avoid serving stale business information (e.g., a closed restaurant still appearing as “open”), Yelp can implement cache eviction policies like LRU and TTL. This ensures that the most current data is always presented to the user, maintaining data accuracy.

### User Discovery and Search

**Search Algorithms**

*   **Full-Text Search**: Yelp’s core functionality is finding businesses quickly based on user input. An inverted index allows the system to efficiently retrieve business listings or reviews containing specific keywords. This approach is crucial when dealing with millions of businesses and user-generated reviews.
*   **Tokenization & Stemming**: Since users might search for variations of words (e.g., “pizzeria” vs. “pizza place”), tokenization and stemming help standardize search queries, ensuring comprehensive search results. This improves the user experience by capturing all relevant listings.
*   **Ranking (BM25, TF-IDF)**: Yelp needs to return the most relevant businesses for a given query. Algorithms like BM25 prioritize results based on keyword relevance and frequency, ensuring that popular, well-reviewed businesses appear higher in the search results.

**Geolocation Search**

*   **Spatial Indexing**: Since Yelp heavily relies on proximity searches (e.g., “restaurants near me”), spatial indexing enables efficient location-based queries. This reduces the query time significantly when filtering businesses by location.
*   **Haversine Formula**: Yelp users frequently look for businesses within a specific radius. The Haversine formula helps calculate distances accurately, ensuring that the nearest locations are recommended first.
*   **Geohashing**: By converting geographic coordinates into geohashes, Yelp can quickly identify and group businesses located near each other. This is particularly useful for displaying clustered results on maps and for efficient geospatial queries.

**Keyword Matching & Ranking**

*   **TF-IDF**: TF-IDF helps Yelp determine the importance of words within business descriptions or reviews, improving the relevance of search results. This is especially useful for filtering businesses by specific features (e.g., “vegan-friendly”).
*   **Semantic Search**: Implementing semantic search allows Yelp to understand user queries more contextually. For instance, if a user searches for “child-friendly cafes,” the system can return results that are marked as family-friendly, even if the exact term doesn’t appear in business descriptions.

### Personalization

**Collaborative Filtering**

*   **User-based Filtering**: Yelp can recommend restaurants that similar users enjoyed. This is particularly effective when new users join, as they can get tailored recommendations based on users with similar tastes.
*   **Item-based Filtering**: By analyzing user interactions, Yelp can identify which businesses are frequently reviewed together. This helps in suggesting complementary businesses (e.g., a coffee shop near a frequently visited bookstore).
*   **Matrix Factorization (SVD, ALS)**: Decomposing the user-business interaction matrix helps Yelp understand deeper patterns in user preferences, which is crucial for generating personalized business recommendations, even for users with limited interaction history.

**Content-Based Filtering**

*   **Feature Engineering**: Yelp can analyze business attributes like cuisine type, pricing, and ambiance to create detailed profiles for businesses. This enables the system to suggest similar businesses when a user likes a particular type of place.
*   **TF-IDF Vectorization**: Business descriptions and user reviews are vectorized to find businesses with similar profiles. This is useful for recommending new places based on previously liked businesses, even in different geographical areas.

**Machine Learning Models**

*   **Deep Neural Networks (DNNs)**: DNNs can learn complex user behavior patterns, such as preferred cuisines and locations, to deliver more accurate recommendations. This approach helps Yelp enhance user engagement by providing relevant suggestions.
*   **Gradient Boosted Decision Trees (GBDTs)**: Yelp can use GBDTs to rank search results based on various structured features, ensuring the most relevant businesses appear at the top for each user query.

### Data Collection and Integration

**Third-Party Data Integration**

*   **API Rate Limits & Caching**: Yelp integrates data from external sources (e.g., Google Maps for geolocation). Caching this data helps avoid excessive API calls, reducing costs and improving response times for users.
*   **Data Synchronization Strategies**: Regular data synchronization through ETL pipelines ensures that business details are current, minimizing discrepancies between Yelp and external data sources. This is critical for maintaining an accurate business directory.

**User-Generated Content Handling**

*   **Content Moderation**: Since Yelp relies heavily on user-generated reviews, maintaining the quality of this content is crucial. Rule-based filtering and machine learning models help detect spam or inappropriate content, ensuring that reviews remain trustworthy.
*   **Storage Optimization**: Yelp stores massive amounts of media files (photos, videos). Distributed file systems like Amazon S3 optimize storage costs and provide scalability, accommodating the ever-growing volume of user-generated content.

### Review and Rating System

**Standardization and Bias Mitigation**

*   **Normalization**: Yelp’s rating system benefits from normalization, as it adjusts for user-specific biases (e.g., some users consistently give high or low ratings), ensuring a fair representation of business quality.
*   **Bias Detection**: Yelp can identify fraudulent reviews using clustering techniques. This helps maintain the integrity of the review system, protecting businesses from unfair ratings.

**Sentiment Analysis**

*   **NLP-based Sentiment Analysis**: Sentiment analysis helps Yelp extract the overall mood of user reviews, which can be used to rank businesses or highlight key aspects (e.g., excellent service, poor ambiance).
*   **Feature Engineering**: Extracting features from reviews (e.g., specific compliments or complaints) gives Yelp deeper insights into business attributes, allowing for more nuanced search and recommendations.

Full Answer: [https://bugfree.ai/practice/system-design/yelp/solutions/5fzZJbPBFRs-Lx46](https://bugfree.ai/practice/system-design/yelp/solutions/5fzZJbPBFRs-Lx46)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360626697/1a1cade3-1f3d-4a46-87a5-ddaa2276019d.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360628425/626ea1db-bb0e-4701-85e1-b0c2bddea72a.png)

System Design Solution — Design Yelp