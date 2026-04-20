---
title: "LSP Isn’t Theory—It’s How You Stop Inheritance Bugs in Interviews"
seoTitle: "LSP Isn’t Theory — How to Stop Inheritance Bugs in Interviews"
seoDescription: "Use the Liskov Substitution Principle to avoid inheritance bugs like Square vs Rectangle in interviews. Prefer composition when subclassing breaks contracts."
datePublished: Mon Apr 20 2026 17:16:37 GMT+0000 (Coordinated Universal Time)
cuid: cmo7giqi7000102jpd6tectap
slug: lsp-stop-inheritance-bugs-interviews
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png

---

# LSP Isn’t Theory—It’s How You Stop Inheritance Bugs in Interviews

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1776705362533.png" alt="Diagram illustrating Liskov Substitution Principle" width="700" style="max-width:100%;height:auto;" />

The Liskov Substitution Principle (LSP) is simple and practical: if type S extends type T, you must be able to use S anywhere T is expected without breaking correctness. In other words, a subtype must preserve the behavior (contract) of its parent.

This isn't academic nitpicking—it's the rule that prevents a common and deceptively sneaky bug in interviews and code reviews: the Square–Rectangle problem.

## The classic trap: Square inheriting Rectangle

At first glance, it makes sense: a square is a rectangle with equal sides, so why not subclass Rectangle? The problem shows up when Rectangle exposes mutating operations like setWidth and setHeight. A Rectangle lets you change one side independently; a Square doesn't. If your Square subclass overrides these methods to keep sides equal, substituting a Square where a Rectangle is expected can break client code that relies on independent width/height changes.

Example (pseudo-code):

```
class Rectangle {
  int width, height;
  void setWidth(int w) { width = w; }
  void setHeight(int h) { height = h; }
}

class Square extends Rectangle {
  void setWidth(int w) {
    width = w; height = w; // breaks Rectangle's contract
  }
  void setHeight(int h) {
    width = h; height = h;
  }
}

// Client code expecting Rectangle:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(10);
// Client expected width=5, height=10, but Square forces width=height
```

The client’s expectations (the parent contract) are violated by the subclass behavior. That’s an LSP violation.

## Interview rule of thumb

When asked about inheritance or asked to design types in an interview, treat LSP as a go/no-go check:

- Ask: what invariants and behaviors does the parent type guarantee? (mutability, side effects, method semantics)
- If a candidate subtype cannot uphold those guarantees, it must not inherit.
- If inheritance would require overriding to change or restrict behaviors in ways that break clients, prefer composition or redesign.

## Practical alternatives

- Use composition: a Square can hold a Rectangle (or a Dimensions object) and expose a clearer API.
- Make the parent immutable or provide a different abstraction (e.g., Shape with area/perimeter, or Separate Width/Height types).
- Introduce separate hierarchies: MutableRectangle vs ImmutableRectangle, or Rectangle and Square as different branches that don't extend one another.

## Quick checklist for interviews (and code reviews)

- Does the subclass honor all public method contracts of the parent?
- Will client code relying on the parent’s behavior still work with the subclass?
- Are there methods in the parent that the subclass cannot implement without changing semantics?
- If the answer is no, prefer composition or redesign the abstraction.

## Bottom line

LSP is not an abstract rule you can ignore in interviews—it's the practical guardrail that keeps inheritance from introducing subtle, correctness-breaking bugs. When a subclass cannot preserve the parent's contract, don’t force inheritance: redesign or compose instead.

#SOLID #SoftwareEngineering #SystemDesign
