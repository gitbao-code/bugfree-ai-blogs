---
title: "Popular Object Oriented Design Problem — Design ATM Machine"
datePublished: Thu Jan 23 2025 20:06:01 GMT+0000 (Coordinated Universal Time)
cuid: cm8vzwwjn000209l26y6y03gu
slug: popular-object-oriented-design-problem-design-atm-machine-0fcb4d2f2752
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1743360640623/bc3e47f4-db93-4f97-9400-42b33183968b.png

---

Design ATM is a typical Object Oriented Design question in software engineer interview, for testing if an engineer can abstract the actual objects and functionalities in the sense of system architecture.

System Design Diagram — Design ATM Machine

### 1\. Requirements Definition

#### Functional Requirements:

*   Authenticate users and allow access to their accounts.
*   Support key operations like **withdrawals**, **deposits**, **balance inquiries**, and **transfers**.
*   Dispense cash and print receipts.
*   Allow multi-language user interfaces.

#### Non-Functional Requirements:

*   Ensure high availability and fault tolerance.
*   Provide strong security for user authentication and transaction data.
*   Support scalability for future user base and feature expansion.
*   Handle concurrent operations without compromising consistency.

### 2\. Core Entities Identification

The system can be modeled around the following primary entities:

1.  **ATM**: Represents the physical ATM machine, responsible for interfacing with users, handling hardware interactions (card readers, cash dispensers, printers), and connecting to the central server.
2.  **User**: Represents the person interacting with the ATM, identified through a bank card and PIN or biometric data.
3.  **Account**: Represents a financial account (savings, checking) associated with a user.
4.  **Transaction**: Models financial operations like withdrawals, deposits, and balance inquiries.
5.  **Bank**: Represents the organization managing accounts, user data, and transaction validations.
6.  **Card**: Represents the physical debit/credit card used for authentication and linking to the user account.

### 3\. Entity Relationships and Use Cases Establishment

#### Entity Relationships:

*   **ATM** interacts with **User** via **Card** to authenticate and perform transactions.
*   **User** owns one or more **Accounts**.
*   Each **Transaction** is associated with one **Account** and logged for audit purposes.
*   **ATM** communicates with the **Bank** for operations requiring centralized validation (e.g., account balance checks, transaction authorization).

#### Use Cases:

#### Primary Use Cases:

*   **Authenticate User**: Insert card -> Verify credentials -> Retrieve associated accounts.
*   **Withdraw Cash**: User selects account -> Enters amount -> ATM validates and dispenses cash -> Logs transaction.
*   **Deposit Cash**: User inserts cash -> ATM validates -> Updates account balance -> Logs transaction.
*   **Balance Inquiry**: User selects account -> ATM retrieves balance from the bank -> Displays on screen.

#### Secondary Use Cases:

*   **Failure Scenarios** (e.g., card retention on multiple incorrect PIN entries).
*   **Maintenance Activities** (e.g., refilling cash, hardware diagnostics).

### 4\. API Design

#### ATM Interface:

class ATM {  
    boolean authenticateUser(Card card, String pin);  
    Transaction performTransaction(User user, TransactionType type, double amount);  
    double checkBalance(Account account);  
    void dispenseCash(double amount);  
    void depositCash(double amount);  
    void printReceipt(Transaction transaction);  
}

#### Bank Interface:

class Bank {  
    boolean validateUser(Card card, String pin);  
    boolean authorizeTransaction(Transaction transaction);  
    double fetchAccountBalance(Account account);  
    void updateAccountBalance(Account account, double amount);  
    void logTransaction(Transaction transaction);  
}

#### Transaction Class:

class Transaction {  
    String transactionId;  
    Date timestamp;  
    TransactionType type;  // WITHDRAWAL, DEPOSIT, INQUIRY  
    double amount;  
    Account account;  
    TransactionStatus status;  // SUCCESS, FAILURE  
}

### 5\. Request Flows

**a) User Authentication**:

*   ATM reads the card, prompts for a PIN, and forwards authentication to the Bank API.
*   The Bank validates credentials and returns user details.

**b) Transaction Request**:

*   User selects “Withdraw,” specifies account and amount.
*   ATM checks cash availability locally and requests authorization from the bank for the withdrawal.

**c) Transaction Execution**:

*   On approval, the ATM dispenses cash and prints a receipt.
*   The Bank updates the account balance and logs the transaction.

**d) Error Handling**:

*   If cash is unavailable or authorization fails, the user is notified, and no money is dispensed.

### 6\. Scalability and Flexibility Consideration

#### Scalability:

*   Use a **distributed architecture** to offload transaction handling from a single server.
*   Introduce **load balancers** for handling peak transaction loads.
*   Deploy **edge servers** for faster local processing of non-critical requests (e.g., PIN validation).

#### Flexibility:

*   Design modular components to support future hardware (e.g., NFC readers, biometric scanners).
*   Implement feature toggles for smooth rollout of new functionalities (e.g., voice-guided interface).

### 7\. Failure Scenarios Analysis

#### User Errors:

*   **Forgot PIN**: Allow limited retries with account lockout after three failed attempts.
*   **Incorrect Inputs**: Provide clear instructions and the ability to cancel operations safely.

#### Hardware Failures:

*   **Cash Jam in Dispenser**: Detect and report the issue, preventing deduction from the user’s account.
*   **Card Reader Failure**: Notify users and flag the ATM for maintenance.

#### Network Failures:

*   Implement a **retry mechanism** for transient failures and queue transactions locally for delayed processing when communication with the bank is restored.

#### Software Failures:

*   Use robust exception handling and fail-safe mechanisms to ensure the ATM remains operational for basic tasks.

Full Answer: [https://bugfree.ai/practice/object-oriented-design/atm-machine/solutions/zFg9xkuDXgLG5Mem](https://bugfree.ai/practice/object-oriented-design/atm-machine/solutions/zFg9xkuDXgLG5Mem)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360638977/8276279e-76a6-4b41-8b0b-e30240c23737.png)

System Design Answer — Design ATM Machine