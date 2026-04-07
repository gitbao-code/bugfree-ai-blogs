---
title: "OOD Interviews: Stop Guessing Classes—Identify Core Entities Like a Pro"
seoTitle: "OOD Interviews: Identify Core Entities & Design Classes Like a Pro"
seoDescription: "Learn a practical 5-step method to identify domain entities, assign responsibilities, and define relationships for OOD interviews."
datePublished: Tue Apr 07 2026 17:17:41 GMT+0000 (Coordinated Universal Time)
cuid: cmnovu1ip000002lhe77h9m18
slug: ood-interviews-identify-core-entities-1
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png" alt="OOD diagram cover" style="max-width:700px;width:100%;height:auto;display:block;margin:0 auto 1rem;" />

# OOD Interviews: Stop Guessing Classes—Identify Core Entities Like a Pro

In object-oriented design (OOD) interviews, interviewers aren't impressed by a long list of classes — they're looking for a systematic approach. The quickest way to show you know what you're doing is to identify the domain's core entities: objects that own both data and behavior (for example, Product or Order). Here's a practical, repeatable method to do that confidently.

## A 5-step checklist for finding core entities

1. Understand the domain first

   - Ask clarifying questions to reveal goals, constraints, and key flows. Don't assume terminology — confirm what the interviewer means by terms like "user," "account," or "session."

2. Extract nouns from requirements

   - Scan the problem statement and notes for nouns: Book, Member, Loan, Product, Cart, Payment.
   - Nouns are candidates for entities. Keep them as seeds, not final answers.

3. Assign clear responsibilities (apply SRP)

   - For each candidate entity, ask: what is this responsible for? A class should have one primary reason to change.
   - Example: Loan manages borrowing dates and status; Member tracks member details and loan history; Book contains bibliographic info and availability.

4. Define relationships and ownership

   - Map associations: Member has many Loans; Loan links to Book; Order contains OrderItems; Product has Inventory.
   - Decide aggregation vs. composition and which side owns lifecycle (does deleting a Member delete their Loans?).

5. Iterate and refine as requirements evolve

   - As you add features (reservation, fines, search), some nouns split into new entities or become value objects.
   - Refactor responsibilities to keep classes cohesive and decoupled.

## Mini example: library system

- Noun extraction: Book, Member, Loan, Reservation
- Responsibilities:
  - Book: metadata, availability check
  - Member: profile, borrowing limits, fines
  - Loan: start/end dates, renewal, status
  - Reservation: queue position, notify on availability
- Relationships: Member 1..* Loan; Loan -> Book; Reservation associates Member and Book

Show this thought process in the interview—draw a simple UML or diagram and narrate why each class exists and what it does.

## Interview tips — what to say and show

- Think aloud: explain how you derived entities from nouns and scenarios.
- Prioritize: highlight the core entities first, then secondary ones.
- Justify responsibilities: use SRP as your reasoning for why a class has (or doesn't have) a responsibility.
- Discuss trade-offs: when to merge vs. split classes, or use value objects instead of full entities.
- Iterate: ask "what if" questions (concurrency, deletes, scale) and show how your model adapts.

## Quick checklist to use during interviews

- Did I extract nouns from the prompt?
- Can I name 3–6 core entities and their main responsibilities?
- Have I defined relationships and ownership?
- Can I point to one reason each class might change (SRP)?
- Did I sketch a small diagram and explain it clearly?

Identify entities like this and you'll stop guessing classes — you'll design them deliberately.

#ObjectOrientedDesign #SystemDesign #SoftwareEngineering
