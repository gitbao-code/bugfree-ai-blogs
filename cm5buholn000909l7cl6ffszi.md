---
title: "Key Points of a Common System Design Interview Question — Photo Sharing Platform"
datePublished: Sun Sep 22 2024 19:37:40 GMT+0000 (Coordinated Universal Time)
cuid: cm5buholn000909l7cl6ffszi
slug: key-points-of-a-common-system-design-interview-question-photo-sharing-platform-91f52fa4bf05
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1735611862603/544f4c9b-2c06-4fc4-a7ea-96a2d1713535.png

---

This problem can be seen as a simplified version of designing a platform like Facebook or Twitter, but with a more focused use case. The core functionality revolves around **uploading images** and **accessing images**. Despite the simplicity, there are still many extended requirements that can be discussed.

Here’s a high-level **design diagram** from Bugfree, outlining the main components, although it’s kept fairly simple.

### Key Points:

1.  **Media File Storage**:

*   How should images be stored?
*   What should the database schema look like for efficient storage of media files? (e.g., using **Blob Storage**)

**2\. Handling High-Volume Traffic for Media Files**:

*   How do we ensure the system remains available under high traffic?
*   What kind of caching strategies should be used and where?
*   What technologies are appropriate? (e.g., **CDN**, **Redis**, etc.)

**3\. Handling Duplicate Images**:

*   What if users upload a large number of duplicate images? How can we optimize to reduce database storage?
*   This could involve using **hashing** or **similarity algorithms** to detect and handle duplicates.

**4\. Discussion on Extended Features**:

*   a) How would we implement a feature for **liking** or **rating** images?
*   b) How could we support **image search** functionality?
*   c) What would be the best way to add **privacy controls** for images?
*   d) How could we implement a feature like **Snapchat’s “view once” functionality** where the image is deleted after viewing?

### Additional Tips:

While for a **junior engineer**, it’s sufficient to clearly explain the core functionalities, present a well-structured design diagram, and logically reason through the solution. However, to stand out, you’ll need to:

1.  **Drive the discussion** yourself, steering the conversation in a direction that shows your understanding.
2.  Beyond the core features, guide the interviewer through extended functionalities or areas you are **comfortable and experienced** with, which can demonstrate a higher level of competency.

(**Note**: It’s important to stick to areas you are familiar with, as the interviewer may follow up with more detailed questions, and you don’t want to get caught in a tough spot.)