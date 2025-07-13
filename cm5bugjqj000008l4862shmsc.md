---
title: "Google Senior Engineer System Design Interview: Design YouTube"
datePublished: Sat Dec 07 2024 19:02:13 GMT+0000 (Coordinated Universal Time)
cuid: cm5bugjqj000008l4862shmsc
slug: google-senior-engineer-system-design-interview-design-youtube-2f10e15339ff
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1735611809554/8e065f87-c859-4042-b3e4-644cef4667f3.png

---

Recently, I had the chance to conduct a mock system design interview with a Google Senior Software Engineer who has been at the company for 5 years and climbed the ranks to Senior.

The topic is **Design YouTube**. Here are some of the key aspects we discussed during the interview, including important considerations and possible solutions.

system design diagram — design youtube

### Key Topics and Discussions:

#### 1\. Video Processing and Handling

Efficient handling of video uploads is critical. Here are some of the main points we covered:

**Transcoding:**  
Every uploaded video needs to be transcoded into multiple resolutions (e.g., 144p, 360p, 720p, 1080p, etc.) to support different user devices, internet speeds, and screen sizes. But how many resolutions should we prepare? The answer depends on platform usage and device distribution metrics.

**Device Optimization:**  
Should video transcoding vary by screen type (e.g., smartphones vs. desktops) or platform (e.g., iOS vs. Android)? It’s essential to decide whether a one-size-fits-all approach or tailored transcoding is more efficient.

**Compression and Storage Efficiency:**  
Modern codecs like H.264 or H.265 (HEVC) can reduce video size significantly while maintaining quality, but they come with higher computational costs during encoding. Balancing quality, size, and processing time is critical.

#### 2\. Scalability and Storage

YouTube processes **millions of videos per day**, which creates massive scalability challenges. Here’s how to think about this:

**Database Sharding**

Videos and metadata (e.g., titles, descriptions, tags) must be stored across a distributed database. By using techniques like sharding, you can partition the data.

For instance:

*   Shard by **video ID** for uniform distribution.
*   Shard by **uploader** for easier management of user-specific content.

**CDN (Content Delivery Network)**

CDNs are essential for minimizing latency and ensuring fast video delivery. Popular CDNs like Akamai, Cloudflare, or in-house solutions can store copies of frequently accessed videos closer to users.

*   **Cost Efficiency:** Consider leveraging **tiered caching** to store high-traffic content in memory (e.g., Redis), while older or less-accessed videos can stay in cold storage.
*   **Regional Strategies:** Should storage and CDNs be optimized differently for each region? For example, videos in North America might need higher bandwidth capacity compared to areas with lower internet penetration.

#### 3\. Handling Very Popular Videos and Influencers

What happens when an influencer uploads a video that goes viral? With limited computational resources, it’s crucial to prioritize user experience for both creators and viewers:

**Creator Side:**  
For large influencers or viral videos, prioritize transcoding and delivery. Their content often drives significant traffic, so ensure it’s processed and delivered as quickly as possible.

**User Side:**  
Adjust the user’s experience based on their internet speed:

*   For slower connections, deliver **lower-resolution** versions first to reduce buffering.
*   For faster connections, deliver **higher-resolution** content for an optimal experience.

This dynamic adaptation can be achieved using **adaptive bitrate streaming (ABR)**, which allows the video player to switch between resolutions seamlessly based on real-time bandwidth.

#### 4\. Additional Features and Personalization

YouTube isn’t just about storing and streaming videos. It’s also about **engagement and user experience.** Here’s how we tackled some advanced features:

**Highlights Detection:**  
How can we automatically detect the most “exciting” moments in a video?

*   Use data like **playback heatmaps** (where users frequently pause, replay, or watch repeatedly).
*   Combine this with ML models trained on engagement metrics (e.g., likes, comments, shares) to extract the highlights automatically.

**Trending and Popular Content:**  
To surface the most popular videos, analyze metrics such as:

*   Total views, shares, and likes within a specific time period.
*   Real-time data processing pipelines (e.g., Apache Kafka, Spark) to calculate trends.

**Personalized Recommendations:**  
Use collaborative filtering and content-based algorithms to recommend videos based on a user’s history and preferences. YouTube’s recommendation engine is famously powered by **deep learning models** that analyze watch history, search queries, and user interactions at scale.

For full answer, visit bugfree.ai [https://bugfree.ai/practice/system-design/video-streaming-service/solutions/S5wS9NgVIXW1Dc5Y](https://bugfree.ai/practice/system-design/video-streaming-service/solutions/S5wS9NgVIXW1Dc5Y)