---
title: "OOD Interview Drill: Design a Social Media Feed (in 60 seconds)"
seoTitle: "Design a Social Media Feed — OOD Interview Drill (60s)"
seoDescription: "Quick OOD design for a social feed: users, posts, likes, comments, feed aggregation and notifications. Clear relationships and scaling notes."
datePublished: Wed Jan 21 2026 04:55:52 GMT+0000 (Coordinated Universal Time)
cuid: cmknjvb0x000602js05lbflos
slug: ood-interview-drill-design-social-media-feed-60s
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768971307194.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768971307194.png

---

# OOD Interview Drill: Design a Social Media Feed (in 60 seconds)

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1768971307194.png" alt="Social feed diagram" style="max-width:700px;width:100%;height:auto;" />

If you can model a social feed cleanly, you can handle many object-oriented design (OOD) interviews. Below is a compact, interview-friendly design that meets the requirements and explains relationships and justifications.

## Requirements (must-haves)
- Users can create, edit, and delete posts.
- Feed shows posts from followed users.
- Users can like and comment on posts.
- Notifications are generated for relevant events (e.g., likes, comments, new followers).

## Core classes (concise design)

```text
User
- id
- name
- posts: List<Post>        // posts authored by this user
- following: Set<User>     // users this user follows
- notifications: List<Notification>
+ create_post(content)
+ edit_post(post_id, content)
+ delete_post(post_id)
+ follow(user)
+ unfollow(user)
```

```text
Post
- id
- content
- author: User
- likes: Set<User>
- comments: List<Comment>
- created_at
+ like(user)
+ unlike(user)
+ add_comment(user, content)
+ edit(content)
+ delete()
```

```text
Comment
- id
- content
- author: User
- post: Post
- created_at
+ edit(content)
+ delete()
```

```text
Feed
- user: User
+ get_feed_posts(limit, cursor)
  // aggregates posts from user.following and self.user (sorted by created_at)
  // supports pagination
```

```text
Notification
- id
- user: User        // recipient
- message: String
- type: Enum        // LIKE, COMMENT, FOLLOW, etc.
- related_id        // e.g., post_id or comment_id
- read: Boolean
- created_at
```

## Relationships and justifications
- User -> Post (composition/ownership): a user "owns" posts. Keep a list of posts for quick retrieval of a user's content and for delete/ownership checks.
- Post -> Author (association): post references its author. This is necessary to display metadata and enforce edit/delete permissions.
- Post -> Likes (association to User): likes are best modeled as a set of Users (or user IDs) to prevent duplicates and to support quick membership checks.
- Post -> Comments (composition): comments are tightly coupled to a post; deleting a post typically removes its comments.
- Feed aggregates posts (association, not ownership): a Feed composes results from many users' posts — it does not own the posts.
- Notification -> User (ownership): notifications belong to a recipient user and are stored so they can be read/cleared.

Why IDs vs object references: in a real system, store IDs in the persistence layer to avoid heavyweight object graphs and to enable lazy-loading or joins. In-memory or interview diagrams can show object references for clarity.

## Typical flows (short)

- Create post
  1. User.create_post(content) -> Post created with author set.
  2. Save post to DB; append post id to user's posts list.
  3. Optionally push to followers' feeds (see scaling).

- Like post
  1. Post.like(user) adds user to post.likes set.
  2. Create Notification for post.author (if liker != author).

- Add comment
  1. Post.add_comment(user, content) creates a Comment referencing post and author.
  2. Save comment; append to post.comments.
  3. Create Notification for post.author (and possibly other participants).

- Follow
  1. follower.follow(target) adds target to follower.following.
  2. Optionally create Notification for target.

## Implementation notes & interview talking points
- Concurrency: like/comment should be idempotent and handle concurrent updates to likes/comments (use optimistic locking or atomic DB operations).
- Data modeling: store lists (likes, comments) as separate tables/collections for scalability; paginate comments.
- Feed generation strategies:
  - Pull model: compute feed on read by querying posts from followed users (simple, consistent, good for small scale).
  - Push model (fan-out): when a user posts, push the post to followers' feed timelines (fast reads, more write work and storage, required at large scale).
  - Hybrid: push to active followers, pull for the rest.
- Notifications: batch or debounce frequent events to avoid spam (e.g., multiple likes from same user or bot-like activity).
- Performance: index by author and created_at for efficient feed queries; cache recent feeds; use materialized timelines for heavy users.
- Security/permissions: check author on edit/delete; validate inputs for comments and posts.

## What to say in an interview
- Start with responsibilities of each class.
- Explain relationships (ownership vs association) and why you chose them.
- Mention persistence choices (IDs vs objects) and concurrency considerations.
- Discuss feed generation trade-offs (pull vs push) and how you'd scale.

This compact model demonstrates the key OOD ideas interviewers look for: clear responsibilities, correct relationships, simple APIs, and awareness of scaling and concurrency.

#ObjectOrientedDesign #SystemDesign #SoftwareEngineering
