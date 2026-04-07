---
title: "OOD Interviews: Stop Guessing Classes—Identify Core Entities Like a Pro"
seoTitle: "OOD Interviews: Identify Core Entities—Stop Guessing Classes"
seoDescription: "Learn a step-by-step method to find core entities in OOD interviews: extract nouns, assign responsibilities, model relationships, and iterate."
datePublished: Tue Apr 07 2026 17:16:27 GMT+0000 (Coordinated Universal Time)
cuid: cmnovsgfw000102i88oonesc1
slug: ood-interviews-identify-core-entities
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png

---

# OOD Interviews: Stop Guessing Classes—Identify Core Entities Like a Pro

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1775582170115.png" alt="Class identification diagram" width="600" />

In object-oriented design (OOD) interviews, hiring managers rarely want clever one-liners — they want to see that you can reliably find the domain's core entities and justify their responsibilities. Instead of guessing classes, use a repeatable process to identify the objects that own both data and behavior (e.g., Product, Order, Member).

## Why this matters
- Interviewers assess your ability to model a domain, not memorized class names.  
- Clear entities + single, well-justified responsibilities = maintainable, testable code.  
- Demonstrates understanding of SRP (Single Responsibility Principle) and relationships between objects.

## A simple, systematic approach
1. Understand the domain: ask clarifying questions. What are the business goals, flows, and constraints?  
2. Extract candidate entities: scan requirements for nouns (Book, Member, Loan, Product, Order). Treat nouns as seeds, not final answers.  
3. Assign responsibilities: give each candidate one primary reason to change. If a class has multiple unrelated duties, split it.  
4. Define relationships: decide associations (e.g., Member has many Loans; Loan references a Book). Model multiplicity and ownership.  
5. Iterate: refine as you uncover new requirements or edge cases.

## Example (library system)
- Nouns: Book, Member, Loan, Catalog  
- Responsibilities:  
  - Book: metadata and availability logic  
  - Member: contact info, borrowing limits  
  - Loan: due date, renew, return behavior  
- Relationships: Member 1..* Loan; Loan -> Book

## Interview tips
- Talk your process out loud—explain how you found nouns and assigned responsibilities.  
- Use SRP as a guiding rule to split or merge classes.  
- Draw a quick class/relationship diagram and walk through typical use cases.  
- Admit assumptions and show how your model adapts when requirements change.

Focus on discoverability and rationale, not a perfect diagram. If you can consistently identify core entities and justify why each exists and what it does, you'll stand out in OOD interviews.