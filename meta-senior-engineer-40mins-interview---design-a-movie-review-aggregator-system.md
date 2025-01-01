---
title: "Meta Senior Engineer 40mins Interview - Design a Movie Review Aggregator System"
datePublished: Wed Dec 11 2024 17:31:36 GMT+0000 (Coordinated Universal Time)
cuid: cm5bum37c000h09l447167yz9
slug: meta-senior-engineer-40mins-interview-design-a-movie-review-aggregator-system-a11054bf6ebe
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1735612067767/72aa89a0-5d55-4118-91b8-d6c6d5dec744.png

---

Recently, I had a system design interview: **“Design a Movie Review Aggregator System.”** with a Meta Senior Engineer. This exercise was part of a mock interview scenario, and I give 40 minutes to brainstorm and outline the solution. Despite the time crunch, the candidate was able to identify key components of the system and focus on critical areas for deeper discussion.

Here’s a breakdown of the main points:

System Design — Movie Review Aggregator

### 1\. Acquiring Data from Third-Party Sources

One of the first challenges is figuring out how to gather movie review data from multiple external sources like IMDB, Rotten Tomatoes, and Metacritic. This includes designing mechanisms to ensure the data is accurate, up-to-date, and compatible across all sources.

#### Key considerations:

**Data Refresh:**

*   How do we ensure that the data remains up-to-date? This can be done through either periodic polling (e.g., scheduled API calls) or event-driven approaches like webhooks for real-time updates.
*   We also need a strategy for handling rate limits imposed by third-party APIs.

**Multi-Source Data Collection:**

What’s the best way to fetch data from multiple sources? Options include:

*   Using APIs (if provided by the source).
*   Implementing web scraping for platforms without public APIs.
*   Ensure compatibility by normalizing data formats and handling differences in schema or structure between sources.

### 2\. Querying Functionality

The system should allow users to query aggregated movie reviews efficiently. This includes implementing features like search, filters, and sorting options.

#### Key considerations:

**Efficient Query Design:**

*   Support advanced querying capabilities, such as:
*   Pagination for browsing large datasets.
*   Keyword search (e.g., by movie title, director, or actor).
*   Filters for sorting reviews by rating, date, or review source.

**Scalability for Future Features:**

*   Design APIs with extensibility in mind. For example, the system should be flexible enough to incorporate new data sources or add advanced query filters without significant rework.

### 3\. Data Storage

Choosing the right database architecture is crucial for storing, querying, and scaling review data.

#### Key considerations:

**Database Type:**

*   For structured, relational data (e.g., movies, scores, sources), relational databases like **MySQL** or **PostgreSQL** are a good fit.
*   For semi-structured data or flexible schemas (e.g., user-generated reviews), NoSQL databases like **MongoDB** or **DynamoDB** may be more suitable.
*   If tracking rating trends over time is necessary, consider a **time-series database** like **TimescaleDB** to efficiently manage historical data.

**Storage Optimization:**

*   Use indexing strategies to speed up frequent queries (e.g., searching by movie ID, rating, or review source).
*   Partition or shard the database to support scaling as the dataset grows.
*   For hot data like trending movies or frequently accessed reviews, leverage caching layers (e.g., **Redis**) to reduce database load.

### 4\. Review Data Analysis

Aggregating review data involves not only storing and querying information but also analyzing it to provide meaningful insights.

#### Key considerations:

**Data Normalization:**

*   Different review sources often have different scoring systems (e.g., a 1–10 scale vs. a percentage-based system). Normalize these scores to a unified scale for easier comparison and aggregation.

**Aggregation Techniques:**

*   Calculate overall ratings using weighted averages. Assign different weights to each review source based on reliability or popularity.
*   Handle outliers by removing extreme scores that may distort the overall rating.

**Sentiment Analysis:**

*   Extract sentiment scores from text reviews using **natural language processing (NLP)**. This can add another dimension to the ratings by analyzing user sentiments like positive, negative, or neutral tones.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735612066008/cfe9986c-b47b-49e1-b0ff-202e3577638f.png)

part of the system design answer