---
title: "High-Score Interview Experience: Amazon SDE-2 Onsite — Behavioral + Tree & String Coding"
seoTitle: "Amazon SDE-2 Onsite Interview — Behavioral + Tree & String Coding (High-Score Experience)"
seoDescription: "First-hand Amazon SDE-2 onsite recap: leadership behavioral plus two DS&A problems — burning binary tree and remove k adjacent duplicates."
datePublished: Thu Jan 22 2026 02:29:09 GMT+0000 (Coordinated Universal Time)
cuid: cmkou2hbv000l02jvhi8jbixl
slug: amazon-sde2-onsite-behavioral-tree-string-coding
cover: https://hcti.io/v1/image/019be387-b804-7d15-bbcc-bdc74cecfa4e
ogImage: https://hcti.io/v1/image/019be387-b804-7d15-bbcc-bdc74cecfa4e

---

<img src="https://hcti.io/v1/image/019be387-b804-7d15-bbcc-bdc74cecfa4e" alt="Interview cover" style="max-width:700px; width:100%; height:auto;" />

# High-Score Interview Experience: Amazon SDE-2 Onsite — Behavioral + Tree & String Coding

A Bugfree-user shared a high-scoring Amazon SDE-2 onsite (Round 1) experience that blended leadership-oriented behavioral questions with core DS&A problems. Below is a concise, actionable summary you can use to prepare.

---

## Quick overview
- Format: Leadership-style behavioral + 2 coding problems (tree + string).
- Behavioral emphasis: ownership, trade-offs, measurable impact.
- Coding emphasis: clear BFS/stack patterns and explaining complexity.

---

## Behavioral highlights & how to answer
Focus on clarity, ownership, and measurable outcomes. Use STAR (Situation, Task, Action, Result) but be ready to dive deep into decisions and trade-offs.

- Tight deadline question
  - What they asked: Explain how you handled a tight deadline — what you did, what you sacrificed, and the outcome.
  - How to answer: Be concrete. State the timeline, the deliverables you prioritized, why you chose that scope, the technical trade-offs (e.g., temporary coupling vs. long-term maintainability), and the quantifiable result (e.g., "shipped feature X in 3 days, 20% reduced latency, follow-up refactor planned").

- Deep dive on current project
  - What they asked: Explain your role, decisions you made, and the impact.
  - How to answer: Explain the architecture, your responsibility, key technical decisions, the reason behind those decisions, observed impact (metrics), and the follow-ups or improvements you planned.

Behavioral tips:
- Own the decision — describe why your choice was pragmatic.
- Be crisp about trade-offs and mitigation plan.
- If you don’t know something, say how you’d find out and whom you’d involve.

---

## Coding focus — problems and approaches
Two core problems surfaced in this interview:
1. Burning a binary tree from a target node (time to burn whole tree). Follow-up: print burning sequence per time unit.
2. Remove k adjacent duplicates in a string (repeat until stable).

Below are clear approaches you can use in the interview.

### Problem 1 — Burning Binary Tree from a Target Node
Problem summary:
- Given a binary tree and a target node, fire spreads to parent and children each unit time. Compute the time to burn the whole tree.
- Follow-up: print nodes burned at each time unit (the burning sequence by level/time).

Approach (standard and robust):
1. Build a parent map for every node by traversing the tree (DFS/BFS). This lets you treat the tree as an undirected graph.
2. Start a BFS from the target node. Use a queue for current frontier and a visited set.
3. Each BFS level corresponds to one time unit. The number of BFS levels until the queue is empty is the time to burn the whole tree.
4. To print the burning sequence, record the nodes processed at each BFS level (e.g., append them to a list for that time unit).

Pseudo-steps:
- parentMap = {} ; build via DFS
- queue = [target]
- visited = {target}
- time = 0
- while queue not empty:
  - size = queue.size
  - nodesThisTime = []
  - for i in 0..size-1:
    - node = queue.pop
    - nodesThisTime.append(node.val)
    - for neighbor in [node.left, node.right, parentMap[node]]:
      - if neighbor and neighbor not visited:
        - visited.add(neighbor)
        - queue.push(neighbor)
  - record nodesThisTime (for printing sequence)
  - time += 1
- answer = time - 1 (since last increment happens after final level)

Complexity: O(n) time, O(n) space.

Edge cases & notes:
- If nodes can have duplicate values, identify the target node by reference or by path, not just value.
- If target might be null, handle early return.

### Problem 2 — Remove K Adjacent Duplicates in String (repeat until stable)
Problem summary:
- Given a string s and integer k, repeatedly remove groups of k identical adjacent characters until no more such groups exist, and return the final string.

Approach (stack of (char, count)):
- Use a stack that stores pairs: (character, current consecutive count).
- Iterate through characters of s:
  - If stack is empty or current char != stack.top.char, push (char, 1).
  - Else increment stack.top.count.
  - If stack.top.count == k, pop it (removes those k chars).
- At the end, rebuild the string by repeating each char by its count in the stack order.

This single-pass stack approach inherently handles repeated removals because popping may expose a previous run that can merge with future characters.

Example:
- s = "deeedbbcccbdaa", k = 3
- Process yields final string "aa".

Complexity: O(n) time, O(n) space.

Implementation note:
- For performance, store counts as integers and build result using a list/buffer instead of concatenating strings repeatedly.

---

## Key takeaways
- Behavioral: Be crisp about ownership, trade-offs, and measurable results. Prepare 2–3 deep-dive stories you can discuss for 10+ minutes.
- Coding: Know BFS on trees (including parent mapping) and stack/count techniques for string reductions.
- Explain complexity and edge cases out loud; interviewers care about thought process as much as the final code.

---

## Quick prep checklist
- Prepare STAR stories focusing on impact and follow-ups.
- Practice tree BFS where parent links are needed (burning tree pattern).
- Practice string-stack patterns like "remove k adjacent duplicates."
- Time-box practice problems and verbalize trade-offs.

Good luck—focus on ownership in behavioral answers and clear BFS/stack patterns for coding.

#SoftwareEngineering #InterviewPrep #DataStructures
