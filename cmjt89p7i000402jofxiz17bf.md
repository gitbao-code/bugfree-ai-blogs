---
title: "ATM OOD Interview Question: Nail the Classes, Not the Buzzwords"
seoTitle: "ATM OOD Interview: Focus on Classes, Not Buzzwords"
seoDescription: "Interview-ready ATM OOD guide: map requirements to classes (ATM, Account, Transaction), explain responsibilities, interactions, and failure handling."
datePublished: Tue Dec 30 2025 23:38:03 GMT+0000 (Coordinated Universal Time)
cuid: cmjt89p7i000402jofxiz17bf
slug: atm-ood-interview-nail-classes-not-buzzwords
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767137851088.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767137851088.png

---

![ATM OOD cover](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1767137851088.png "ATM OOD Diagram" =700x400)

# ATM OOD Interview Question: Nail the Classes, Not the Buzzwords

Interviewers are not testing your ability to recite OOD theory — they want a clear, maintainable design for the ATM problem. Start with concrete requirements, map them to objects, and explain responsibilities and interactions. If you can do that, you’ll pass.

## 1. Start from requirements (be explicit)

Minimum functional requirements to state out loud:

- Authenticate (card + PIN)
- Check balance
- Withdraw
- Deposit
- Transfer (between accounts)

Non-functional / constraints you might mention briefly:

- Consistency (no double-spend)
- Audit trail for transactions
- Security (PIN retries, encryption)
- Integration with bank backend
- ATM cash dispenser limits

## 2. Map requirements to core objects

A simple, interview-friendly mapping:

- ATM
  - Orchestrates a session, UI flow, and talks to hardware and bank backend.
- User (or Card / CardHolder)
  - Identity, authentication (card id + PIN flow).
- Account
  - Holds balance and enforces rules (overdraft, withdrawal limits).
- Transaction
  - Immutable audit entry. Concrete types: Deposit, Withdraw, Transfer.
- Session (optional)
  - Tracks current authenticated user and selected account.
- BankGateway / Dispenser (optional)
  - External services: bank backend for account ops, hardware for cash.

## 3. Responsibilities and encapsulation

Keep responsibilities tight and behavior on the objects that own the data:

- Account should own balance changes. Provide methods like deposit(amount) and withdraw(amount) which validate rules and update state.
- Transaction objects are append-only audit records describing the operation and outcome.
- ATM orchestrates UI, authentication, calls into Account or BankGateway, and records Transaction objects.

Example (Python‑like skeletons):

```python
class Account:
    def __init__(self, id, balance=0):
        self.id = id
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0: raise ValueError
        self._balance += amount
        return Transaction(type='deposit', amount=amount, account_id=self.id)

    def withdraw(self, amount):
        if amount <= 0 or amount > self._balance: raise InsufficientFunds
        self._balance -= amount
        return Transaction(type='withdraw', amount=amount, account_id=self.id)

class Transaction:
    def __init__(self, type, amount, account_id, timestamp=None):
        # immutable audit record
        ...
```

## 4. Inheritance and polymorphism (keep it practical)

- Inheritance: model SavingsAccount and CheckingAccount as subclasses when they have different rules (interest calc, overdraft).
- Polymorphism: treat Deposit/Withdraw/Transfer as implementations of a common Transaction interface. That allows code that logs or processes transactions to be written against the interface, not the concrete type.

Example:

```python
class Transaction:
    def apply(self):
        raise NotImplementedError

class Withdraw(Transaction):
    def apply(self, account):
        return account.withdraw(self.amount)

class Transfer(Transaction):
    def apply(self, from_account, to_account):
        ...
```

## 5. Typical interaction flow (withdraw)

1. Card inserted -> ATM creates Session
2. Prompt PIN -> authenticate with BankGateway
3. User selects account and amount
4. ATM requests withdraw from Account (or via BankGateway)
   - Account checks balance and business rules
   - Reserve or lock funds to avoid race conditions
5. ATM triggers cash dispenser
6. On success: commit transaction, create Transaction record, update account
7. On failure: rollback reservation, show error, log audit

Explaining this sequence clearly in an interview shows you understand orchestration and invariants.

## 6. Concurrency, consistency, and edge cases

Bring these up briefly to show depth:

- Race conditions: lock account or use atomic operations when debiting balance.
- Idempotency: network retries between ATM and bank should not create duplicate transactions.
- Partial failures: what if dispenser jams after balance deducted? Keep a reversible state or compensating actions and a clear audit trail.
- PIN attempts, card capture, transaction limits, and offline mode.

## 7. What to say in the interview (strategy)

- Start by listing requirements and constraints.
- Present the object map (ATM, User/Card, Session, Account, Transaction, BankGateway/Dispenser).
- For each class, state 1–2 responsibilities and a couple of methods.
- Walk through a concrete scenario (withdraw) step-by-step.
- Mention one or two tradeoffs (local locking vs. distributed transactions, when to call the bank, offline mode).

That level of clarity beats buzzwords. Interviewers want to hear: "Here are the objects, these are their responsibilities, this is how they interact, and these are the important failure modes." If you can explain that, you're golden.

## Quick checklist to mention

- Requirements: auth, balance, withdraw, deposit, transfer
- Core classes and responsibilities
- Encapsulation: Account mutates its own balance
- Inheritance: Savings/Checking extend Account when needed
- Polymorphism: Transaction types implement a common interface
- Sequence for a withdraw and failure handling
- Concurrency/consistency considerations

Good luck — focus on the classes and interactions, not on reciting patterns by name.