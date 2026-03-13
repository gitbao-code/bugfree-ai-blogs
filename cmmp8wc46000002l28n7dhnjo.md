---
title: "The One Detail That Makes √2 Irrational (and Interviewers Love It)"
seoTitle: "Why the 'Lowest-Terms' Step Makes √2 Irrational"
seoDescription: "Learn how the 'lowest-terms' assumption is the decisive step proving √2 is irrational—and why interviewers prize this insight."
datePublished: Fri Mar 13 2026 18:43:41 GMT+0000 (Coordinated Universal Time)
cuid: cmmp8wc46000002l28n7dhnjo
slug: why-lowest-terms-makes-sqrt2-irrational
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773427395732.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773427395732.png

---

![Cover image: diagram explaining the √2 proof](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1773427395732.png){width="600"}

> The decisive move in the classic √2 proof isn't just “use contradiction” — it's the *requirement that the fraction is in lowest terms*. That's what closes the argument.

Here's the proof, laid out to show exactly where that single constraint matters.

1. Assume √2 is rational. Then we can write
   a/b = √2
   where a and b are integers and, crucially, a/b is in lowest terms (a and b share no common factor).

2. Square both sides:
   a²/b² = 2  ⇒  a² = 2b².

3. From a² = 2b² we see a² is even, so a must be even. (If a were odd, a² would be odd.)

4. Write a = 2k for some integer k and substitute back:
   (2k)² = 2b²  ⇒  4k² = 2b²  ⇒  b² = 2k².

5. Now b² is even, so b is even. Therefore both a and b are divisible by 2.

6. That contradicts the original assumption that a/b was in lowest terms (no common factors). The contradiction means the assumption that √2 is rational is false. Hence √2 is irrational.

Why this matters: the algebraic manipulations produce the parity conclusions (a and b are even). Without the explicit “lowest-terms” constraint, you wouldn't have a contradiction — you would only conclude that the fraction can be simplified further. The contradiction arises because we forbade any common factor at the start.

Why interviewers like this proof

- It shows clear logical structure: an assumption, deduction, and a pinpointed contradiction.
- It tests attention to hidden but crucial assumptions (like "in lowest terms").
- It demonstrates fluency with basic number theory ideas (parity, divisibility) and proof techniques (proof by contradiction).

Quick generalization

The same pattern proves √p is irrational for any prime p: assume a/b in lowest terms with a² = p b². Then p divides a, write a = p k, substitute, and conclude p divides b too — contradicting lowest terms.

Takeaway

The “lowest-terms” requirement is the single detail that turns routine algebra into a contradiction. Recognizing and using such constraints is exactly why this proof is a favorite in interviews and teaching: it rewards careful assumptions and clean reasoning.