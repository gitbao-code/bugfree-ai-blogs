---
title: "System Design — Design Web Crawler — Key Points"
datePublished: Thu Sep 19 2024 01:02:05 GMT+0000 (Coordinated Universal Time)
cuid: cm5buhjug000n08l2dlzsckkf
slug: system-design-design-web-crawler-key-points-d44cf328534e
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1735611856296/233714ae-6d30-42f8-9f93-ca9a2ccaf5c5.png

---

Today we continue to work with system design newbees on frequently asked system design interview questions, **Design a Web Crawler**. This question kept being asked in these years many times.

And the student achieved 85 scores in [bugfree.ai](https://bugfree.ai/practice/system-design), which is considered a fairly complete solution.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735611849604/dc31f081-4031-4854-8b2d-653a788cf93b.png)

### Below are the main points to consider:

#### 1\. URL Duplication

**Problem:** How to ensure the same URL isn’t crawled multiple times?

**Solution:** Use a cache to record URLs that have already been crawled. Before crawling a new URL, check the cache. After successfully crawling the URL, update the cache with its status.

#### 2\. Failure Safety

**Problem:** How to handle situations where the crawl service crashes unexpectedly and ensure no URLs are lost?

**Solution:** Keep track of the crawling status for each URL. Assign states such as “Not Started”, “In Progress”, and “Completed” to each URL so that if the system restarts, it can resume from where it left off without losing progress.

#### 3\. Cold Start

**Problem:** How to select the initial set of web URLs (the “golden dataset”) to begin crawling?

**Solution:** Choose high-traffic, highly-indexed web pages as starting points. These pages are more likely to lead to a broad discovery of new URLs.

#### 4\. Crawl Algorithms

**Problem:** Should the crawler use DFS (Depth First Search) or BFS (Breadth First Search)? What are the pros and cons of each? How can you avoid getting stuck in an infinite loop?

**Solution:**

*   **BFS** is often preferred for crawling because it helps maintain a more even coverage of the web.
*   **DFS** might be faster in exploring deep links but could risk missing important sections of the web.
*   To avoid infinite loops, implement cycle detection and track visited URLs.

#### 5\. Media Content Handling

**Problem:** How to store image or video data, and how to ensure the same media content isn’t stored multiple times?

**Solution:** Use hashing to handle duplicate media files. Before storing any media, compute a hash of the file and check if that hash already exists in the database. If it does, skip storing the media again.

#### 6\. Other Product Optimizations

Some additional product-related considerations include:

*   **a)** How can clients retrieve the crawl status and information of a particular URL?
*   **b)** How can you implement page ranking and prioritize URLs based on their importance?
*   **c)** What methods can be used to speed up the crawling process? What are the potential bottlenecks that affect crawl speed?

For more detailed thoughts and answers, you can refer to the system design diagrams and mind maps available at [bugfree.ai](https://bugfree.ai/practice/system-design/web-crawler/solutions)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735611851254/5c48b97d-5fe3-4d5e-b813-414d20215bf1.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735611852987/a1ce8963-d560-4402-a251-14a0d7ad9e94.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735611854560/673660c2-7b02-41b8-8d0b-c35b34da4738.png)