---
title: "Design Craigslist: The One Detail Interviewers Use to Separate Seniors from Juniors"
seoTitle: "Design Craigslist: Why Handling Images Separates Senior and Junior Engineers"
seoDescription: "In system design interviews, how you handle images reveals seniority—S3/GCS, CDNs, presigned uploads, thumbnails, caching matter."
datePublished: Sun Feb 15 2026 18:16:26 GMT+0000 (Coordinated Universal Time)
cuid: cmlo2h4zs000e02juc28e616i
slug: design-craigslist-images-seniority
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771179368731.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771179368731.png

---

<img src='https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771179368731.png' alt='Design Craigslist cover' width='700' style='max-width:100%;height:auto;' />

## Design Craigslist: don’t hand-wave images

In a system design interview about a classifieds site like Craigslist, everything looks simple until you quantify data and traffic. That’s where interviewers separate juniors from seniors: seniors *do the math* and treat images as a first-class bottleneck, not an afterthought.

From the estimates: ad metadata is ~0.5 GB/month, but images are ~40 GB/month. Images dominate storage costs, bandwidth, and latency. If you ignore them, your design won't scale.

Here’s a compact, interview-ready approach and why each piece matters:

- Store images in object storage (S3, GCS, Azure Blob).
  - Rationale: object stores are cheap, durable, and built for large binary blobs. They also integrate with CDNs and support lifecycle policies.
- Keep only image URLs (and light metadata) in the Ads DB.
  - Rationale: relational or document DBs should store structured data; offloading blobs reduces DB size, backup time, and query latency.
- Serve images through a CDN.
  - Rationale: CDNs reduce latency for users, offload origin bandwidth, and provide global caching.
- Upload via pre-signed (or signed) URLs directly to object storage.
  - Rationale: avoid proxying multi-megabyte uploads through your API servers (which would consume CPU, memory, and network). Pre-signed uploads keep your API layer lightweight and resilient.

If you miss any of these points in an interview, that’s a clear red flag: you’ll be describing a design that will break when traffic or catalog size grows.

Practical improvements and extensions (good things to mention if you want to show depth):

- Thumbnails & responsive images: serve appropriately sized versions (small thumbnails for lists, medium for detail pages) using pre-generated variants or an on-the-fly resizing service.
- Modern image formats & compression: convert uploads to WebP/AVIF where supported; apply lossy compression to reduce bytes without hurting UX.
- Lazy loading and srcset: client-side techniques to avoid downloading large images when not needed.
- Cache-control and CDN configuration: set long TTLs for immutable objects, use cache-busting paths for updates, and consider origin shielding.
- Signed URLs for private images: use short-lived signed URLs if images require access control.
- Lifecycle policies and storage classes: move infrequently accessed images to cheaper tiers, and expire old assets.
- Deduplication and content-addressed storage: avoid storing duplicate uploads by hashing content.
- Monitoring & cost metrics: track egress, requests, storage growth, and CDN hit ratios; these numbers guide optimizations.
- Security & validation: scan uploads for malware, validate image types & sizes, and rate-limit uploads.

Why interviewers care

Handling images correctly demonstrates systems thinking: you understand real-world costs (egress, requests, storage classes), operational concerns (scaling uploads, cache invalidation), and user experience (latency, responsive images). Junior answers often gloss over this and leave images in the DB or routed through app servers — solutions that work only at tiny scale.

Quick checklist to mention in an interview

- Object storage (S3/GCS) for blobs
- Keep only URLs in Ads DB
- CDN in front of object storage
- Presigned uploads to avoid proxying files through APIs
- Thumbnails/responsive sizes + compression
- Cache-control and lifecycle policies
- Monitoring (egress, storage growth, CDN hit rate)

Say these things, and you’ll move from junior-level hand-waving to a senior-level, production-ready design.

#SystemDesign #SoftwareEngineering #DataEngineering