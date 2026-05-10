---
title: "Hospital System OOD: Stop Modeling IDs—Model Relationships"
seoTitle: "Hospital System OOD — Model Relationships, Not IDs"
seoDescription: "Design hospital systems by modeling relationships and ownership (Patient–Appointment–Staff) first. IDs and tables come later—after invariants and lifecycles are clear."
datePublished: Sun May 10 2026 17:16:15 GMT+0000 (Coordinated Universal Time)
cuid: cmp01bb48000j02jzarfgha1q
slug: hospital-system-ood-model-relationships-not-ids
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778433354404.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778433354404.png

---

# Hospital System OOD: Stop Modeling IDs—Model Relationships

<img src="https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1778433354404.png" alt="Hospital system relationships diagram" style="max-width:800px; width:100%; height:auto; display:block; margin:12px 0;"/>

Too many designs start by naming fields: patientID, staffID, appointmentID. Those are storage details, not domain concepts. In object-oriented design (OOD) — especially in interviews — model the relationships and business rules first. Let IDs be an implementation detail you add only after you understand ownership, lifecycle, and invariants.

## The principle

Design around domain relationships and responsibilities, not around unique identifiers. A relationship-first model forces you to answer important questions:

- Who owns what? (ownership)
- When can something be created/removed? (lifecycle)
- What rules must always hold? (invariants)

Once those are clear, tables and APIs follow trivially.

## Common relationships in a hospital system

- Patient has many Appointments
- Staff (doctors, nurses) has many Appointments
- Patient has many MedicalRecords
- Patient has many Bills
- Appointment references exactly one Patient and exactly one Staff

Modeling these explicitly makes you define ownership: e.g., MedicalRecord is conceptually owned by a Patient (who can have multiple records); an Appointment is a relationship between a Patient and Staff with its own lifecycle.

## Example invariants and lifecycle rules

- Appointment must reference exactly one Patient and one Staff.
- Appointment status transitions: Scheduled → (Completed | Cancelled). Some transitions may be forbidden (e.g., Completed → Scheduled).
- MedicalRecord entries are append-only; edits require explicit amendment records or versioning.
- A Bill belongs to a Patient; payment state transitions (Unpaid → PartiallyPaid → Paid) should be explicit.

Explicitly listing these invariants helps you reason about validation, transactions, and concurrency.

## From relationships to APIs and tables (an approach)

1. Draw the domain relationships (boxes + lines). Annotate multiplicities and ownership.
2. For each entity, define lifecycle events and allowed state transitions.
3. Implement business logic in domain methods that enforce invariants.
4. Map to persistence: add IDs and foreign keys to represent relationships.
5. Expose REST/GraphQL APIs that mirror domain operations rather than raw CRUD on IDs.

Example pseudo-classes (conceptual):

class Patient
- name
- contactInfo
- appointments: List<Appointment>
- medicalRecords: List<MedicalRecord>

class Staff
- name
- role
- appointments: List<Appointment>

class Appointment
- patient: Patient
- staff: Staff
- scheduledAt
- status  // Scheduled, Completed, Cancelled
- reschedule(newTime) { /* validate transitions */ }
- complete() { /* set status and enforce rules */ }

And the persistence mapping is straightforward once relationships are clear:

appointments table
- id
- patient_id  -- FK to patients
- staff_id    -- FK to staff
- scheduled_at
- status

medical_records table
- id
- patient_id
- record_data
- created_at

bills table
- id
- patient_id
- amount
- status

Note: IDs appear here as implementation details (primary keys / foreign keys), but your domain design should have been done before you decide on these columns.

## Interview tips

- Start by drawing relationships, not tables. Use boxes for aggregates and arrows for ownership.
- Call out invariants and allowed state transitions on your diagram.
- Describe who owns deletion rights: can a Patient be deleted? What happens to their MedicalRecords and Bills?
- Explain how your domain methods enforce invariants (do not rely solely on DB constraints).
- Only after the model is clear, sketch the APIs and persistence schema.

## Benefits of this approach

- Clearer reasoning about business rules, ownership, and consistency.
- Fewer surprises when you implement workflows or enforce validation.
- APIs that reflect real use cases (e.g., cancelAppointment(patient, appointmentId) instead of deleteById).
- Easier to spot transactional boundaries and concurrency issues.

## Summary

Stop leading with IDs. Model relationships, lifecycles, and invariants first. Once the domain is explicit, IDs, tables, and APIs are just a straightforward mapping from that model.

#ObjectOrientedDesign #SystemDesign #SoftwareEngineering
