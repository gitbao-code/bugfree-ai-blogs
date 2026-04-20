---
title: "LSP Isn’t Theory—It’s How You Stop Inheritance Bugs in Interviews"
seoTitle: "LSP Isn’t Theory — Use It to Catch Inheritance Bugs in Interviews"
seoDescription: "Use Liskov Substitution Principle to spot inheritance bugs in interviews. Learn the Rectangle–Square trap, interview checks, and safer alternatives."
datePublished: Mon Apr 20 2026 17:17:55 GMT+0000 (Coordinated Universal Time)
cuid: cmo7gkegq000002lecb7a7ujd
slug: lsp-stop-inheritance-bugs-interviews-1
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png

---

# LSP Isn’t Theory—It’s How You Stop Inheritance Bugs in Interviews

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png" alt="Liskov Substitution Principle diagram" width="600" style="display:block;margin:16px auto;"/>

The Liskov Substitution Principle (LSP) is simple and practical: if S is a subtype of T, you must be able to use S anywhere T is expected without breaking correctness. In interviews, this is less academic rule and more of a bug-catching litmus test for inheritance design.

## The classic trap: Square inherits Rectangle

It often "looks" right to model a Square as a special Rectangle. But the trouble starts when the parent exposes mutation operations like setWidth and setHeight.

Example (Java-like pseudocode):

```java
class Rectangle {
  int width, height;
  void setWidth(int w) { width = w; }
  void setHeight(int h) { height = h; }
  int area() { return width * height; }
}

class Square extends Rectangle {
  void setWidth(int w) { width = w; height = w; }
  void setHeight(int h) { width = h; height = h; }
}

// Client code expecting a Rectangle:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(4);
// Expected area: 20, actual area: 16 — substitution broke correctness
```

Why it fails: a Rectangle allows width and height to vary independently. A Square enforces an invariant (width == height). When a client relies on Rectangle's contract (independent setters), substituting a Square violates that contract.

## How to use LSP in interviews (quick checklist)

- Ask about the parent type's public contract: which operations and invariants does it expose?
- Ask whether instances are mutable or immutable. Mutable setters often reveal substitution problems.
- Check for strengthened preconditions or weakened postconditions in the subclass — both are red flags.
- If a proposed subclass cannot honor all behaviors the parent promises, it shouldn’t extend the parent.

When explaining your decision in an interview, say explicitly: "If this subclass can't maintain the parent's contract for every client, I'd avoid inheritance and choose composition or a different abstraction." That shows both theory and practical judgment.

## Safer alternatives

- Composition: give Square a Rectangle internally or store side length directly. Expose only the behaviors you can guarantee.
- Interface segregation: separate immutable/querying behavior (e.g., area(), perimeter()) from mutating behavior (e.g., setWidth()).
- Factory methods or distinct types: provide distinct constructors or builders for shapes that don't share a mutating contract.
- Design by contract / tests: write tests that validate substitution (e.g., pass instances of the subtype to existing client tests for the parent).

Example: prefer composition over inheritance

```java
class Square {
  private final int side;
  Square(int side) { this.side = side; }
  int area() { return side * side; }
}

// or
class RectangleLike {
  private int width, height;
  // only expose operations you can honestly support
}
```

## Final tip for interviewers and candidates

Treat LSP as a practical question: when asked to extend or refactor types, explicitly reason about the parent contract and client expectations. If substitution would change observable behavior, choose composition or redesign the abstraction. That reasoning—clear, testable, and tied to correctness—is what interviewers want to hear.

#SOLID #SoftwareEngineering #SystemDesign
