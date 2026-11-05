# REQ-INT-007 Certificate generation

> **SIMULATED REQUIREMENT.** Package Functional Test Lab, milestone M1. Derived only from public documentation. This is not an Intellum configuration and not a claim of product experience.

| Field | Value |
| --- | --- |
| Requirement ID | REQ-INT-007 |
| Title | Issue one certificate when completion criteria are met |
| Workflow | Intellum-style learning |
| Topic | Certificate generation |

## Description

When an activity is configured to award a certificate, completion produces one certificate record linked to that completion.

## Business Rule

The public certification article says issuance is automated once completion criteria are met. Credential properties described there include a name, a unique code, an expiration length in months, and the facts printed for the learner: name, completion date, and a unique completion identity, plus the score when the program shows it. A blank name defaults to the activity name. A blank expiration length means the credential does not expire.

The public certifications API description includes a certification name, an active flag, and an expiry period. The lab stores those ideas on the issued certificate. It does not call that API.

## Source Link

- Intellum, "How to Administer a Certification Program at Scale": https://www.intellum.com/resources/blog/how-to-administer-a-certification-program-at-scale-in-intellum
- Intellum, "Certification Management": https://www.intellum.com/solutions/certifications
- Intellum experience page, "Certifications API": https://experience.intellum.com/student/activity/408684-certifications-api

The certification article describes automated issuance and the name, code, and expiration fields. The solutions page says certificates and digital credentials are issued on completion. The API page describes a certifications resource with name, active, and expiry period. Badge image, printable template, Credly, and LinkedIn sharing appear in the public articles and are outside this requirement (`plan/test-plan.md` section 5).

## Simulated Assumptions

- ASM-INT-09. The lab writes a certificate record. It does not render a PDF and does not call an external badge vendor.
- The code pattern is `SIM-CERT-{activityCode}-{year}-{sequence}`. Sequence increases by one for each certificate the lab issues in that activity and year.
- A blank configured name is stored as the activity name. A blank expiration length stores an empty expiration date.
- When the activity is configured to show a score, the passing score is copied onto the certificate. A content-only completion stores an empty score.
- One completion produces one certificate. A failed enrollment produces none.

## Acceptance Criteria

1. Completing an activity that has a certificate configured creates exactly one certificate linked to the learner, the activity, and the completion.
2. The certificate code matches `SIM-CERT-{activityCode}-{year}-{sequence}` and does not collide with an existing code.
3. A blank expiration configuration stores no expiration date. A configured length of 12 months stores an expiration date 12 months after the completion timestamp.
4. A failed enrollment, and a second completion signal on an existing completion, create no additional certificate.
5. An activity with certificate generation turned off can still be `Completed` and has no certificate identifier.
