---
title: "Strategy vs State Pattern: Stop Confusing Them in Interviews"
seoTitle: "Strategy vs State Pattern: Clear Differences, When to Use, and Interview Tips"
seoDescription: "Learn the key differences between Strategy and State patterns, when to use each, and how to explain them clearly in interviews."
datePublished: Mon Feb 23 2026 22:48:03 GMT+0000 (Coordinated Universal Time)
cuid: cmlzrp8zi000502kz8ica9lcf
slug: strategy-vs-state-pattern-stop-confusing-them
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771886855256.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771886855256.png

---

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1771886855256.png" alt="Strategy vs State diagram" width="700" />

# Strategy vs State Pattern: Stop Confusing Them in Interviews

Two design patterns that often get mixed up in interviews are Strategy and State. They look similar on the surface—both encapsulate behavior in separate objects—but their intent and usage are different. Here’s a concise, interview-ready explanation and a practical checklist to tell them apart.

## One-line definitions

- Strategy: choose *how* to do a task. Swap algorithms/behaviors at runtime; selection usually comes from the client or configuration.
- State: choose *what the object is right now*. The object’s behavior changes based on its internal state; transitions are driven by the object’s lifecycle.

## When to use which

- Use Strategy when:
  - You have multiple interchangeable algorithms or policies (e.g., different sorting strategies, payment processors: CreditCard vs PayPal).
  - Clients should be able to pick or inject the algorithm.
  - You want Open/Closed extensibility: add new strategies without modifying existing code.

- Use State when:
  - An object’s behavior depends on its internal state (e.g., Playing / Paused / Stopped in a media player).
  - The object itself controls state transitions and should avoid large if/else or switch statements.
  - You want to encapsulate state-specific behavior and transitions in separate state classes.

## Key distinguishing rule

Strategy is selected by the client/context; State is driven by the object’s lifecycle.

## Short examples (pseudo-code)

Strategy (client picks behavior):

```java
interface PaymentStrategy { void pay(Order o); }
class CreditCardStrategy implements PaymentStrategy { ... }
class PayPalStrategy implements PaymentStrategy { ... }

// Client configures which strategy to use
class Checkout {
  PaymentStrategy strategy;
  void checkout(Order o) { strategy.pay(o); }
}
```

State (object changes behavior internally):

```java
interface PlayerState { void pressPlay(MediaPlayer p); }
class PlayingState implements PlayerState { void pressPlay(MediaPlayer p) { p.pause(); p.setState(new PausedState()); } }
class PausedState implements PlayerState { void pressPlay(MediaPlayer p) { p.resume(); p.setState(new PlayingState()); } }

class MediaPlayer {
  PlayerState state;
  void pressPlay() { state.pressPlay(this); }
  void setState(PlayerState s) { state = s; }
}
```

In the Strategy example, an external actor chooses the payment algorithm. In the State example, the MediaPlayer transitions itself between states as actions occur.

## Interview tips: short answers you can give

- If the question is about swapping algorithms or policies provided by the caller: say "Strategy." 
- If it’s about an object whose operations change depending on its internal mode and it transitions between modes: say "State." 
- Bonus: mention the rule—"Strategy is selected by the client; State is driven by the object's lifecycle." That demonstrates understanding, not just memorization.

## Quick checklist to decide

- Who chooses the behavior? Client -> Strategy. Object itself -> State.
- Do you need to model transitions between behaviors? If yes, State is likely a better fit.
- Is the goal to add new algorithms without changing existing code? Strategy.

## Summary

Both patterns decouple behavior into classes, but their intent differs. Use Strategy to expose interchangeable algorithms to clients; use State to encapsulate internal modes and transitions. Remember: selection by the client vs. driven by the object.

#SoftwareEngineering #SystemDesign #ObjectOrientedProgramming
