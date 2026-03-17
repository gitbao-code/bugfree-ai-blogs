---
title: "High-Score (Bugfree) Amazon SDE-2 Interview Experience: In-Person Loop + Virtual Bar Raiser"
seoTitle: "Amazon SDE-2 Interview Experience: In-Person Loop + Virtual Bar Raiser (Hyderabad)"
seoDescription: "Detailed Amazon SDE-2 interview walkthrough: OA, in-person loop (LP, coding, LLD, HLD) and virtual bar-raiser. Tips, problems, and outcome (selected)."
datePublished: Tue Mar 17 2026 01:15:58 GMT+0000 (Coordinated Universal Time)
cuid: cmmtx8d46000602judry715tw
slug: amazon-sde-2-hyderabad-in-person-loop-virtual-bar-raiser
cover: https://hcti.io/v1/image/019cf95c-585f-7085-8fa8-1510f14b79a4
ogImage: https://hcti.io/v1/image/019cf95c-585f-7085-8fa8-1510f14b79a4

---

<img src="https://hcti.io/v1/image/019cf95c-585f-7085-8fa8-1510f14b79a4" alt="Amazon interview cover" style="max-width:800px; width:100%; height:auto; display:block; margin:0 auto 1rem;" />

# High-Score (Bugfree) Amazon SDE-2 Interview Experience

A concise write-up of my Amazon SDE-2 interview loop — applied via referral with ~2 years of fintech full-stack experience. The process included an online assessment, a pause by the recruiter due to location, reconnection for Hyderabad onsite scheduling, a 4-round in-person loop, and a virtual bar-raiser. Final status: selected.

## Quick timeline

- Applied via referral (2 years fintech, full-stack)
- Online assessment (OA): straightforward
- Recruiter paused because of location, later reconnected for Hyderabad
- In-person loop (3 rounds) + virtual bar-raiser (4th round)
- Final: selected

---

## Interview breakdown (round-by-round)

Round 1 — LP + Coding
- Leadership Principles (LP) behavioral questions
- Coding problems: "Max Points from Cards" and "Asteroid Collision"
- Notes: Did a dry run on Asteroid Collision, caught a bug, fixed it during the interview — good debugging demonstration

Round 2 — LP + Low-Level Design (LLD)
- LP discussion
- LLD: Tic-Tac-Toe
  - Covered required entities, class design, and class diagram
  - Implemented the game-over check method in C++

Round 3 — LP + High-Level Design (HLD)
- LP behavioral questions
- HLD: Event Booking System (architecture, components, scalability considerations)

Round 4 (Bar Raiser — virtual) — LP + Coding
- LP-focused behavioral assessment by the bar raiser
- Coding problems: "House Robber II" and "Boats to Save People"
  - House Robber II: circular DP variant — deal with circular constraint by splitting into two linear runs
  - Boats to Save People: two-pointer greedy approach to pair lightest and heaviest

---

## What worked well

- Clear LP stories: used STAR format (Situation, Task, Action, Result) and tied examples to Amazon's principles
- Dry runs: doing a hand-simulation helped catch a bug live (shows attention to detail)
- LLD/ HLD clarity: focusing on entities, APIs, data flow, fault tolerance, and scaling trade-offs
- Language comfort: implemented C++ method when asked — be comfortable in at least one language

## Quick tips if you're preparing for a similar loop

- Prepare 6–8 strong LP stories mapped to Amazon's Leadership Principles; rehearse concise STAR answers
- Practice dry runs for coding problems — simulate inputs/outputs and edge cases on paper
- For LLD: sketch entities, relationships, responsibilities, and one or two key methods
- For HLD: discuss capacity, data partitioning, caching, consistency, and failure scenarios
- Know common patterns: two-pointers, stacks, DP (including circular DP), and greedy strategies

---

## Final notes

Recruiter logistics questions (compensation, notice period, location) were asked toward the end and I accepted the offer. The combination of strong LP storytelling, careful dry runs during coding, and clear design explanations helped secure the role.

Good luck — and debug your dry run!

#AmazonInterview #SystemDesign #SoftwareEngineering