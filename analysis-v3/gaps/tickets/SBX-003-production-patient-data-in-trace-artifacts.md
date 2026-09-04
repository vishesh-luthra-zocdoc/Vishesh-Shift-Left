# SBX-003 — Review trace/screenshot/video retention on the spec that reads production patient data

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P1 |
| Test level | L5 e2e |
| Action | investigate |
| Repo | sandbox |
| Area | Provider-Billing — test data handling |
| Estimate | 2h |
| Labels | e2e, compliance, test-data |
| Evidence revision | `eef9429d` (`origin/main`) |

## Summary
One spec in the billing file navigates a **production** provider inbox and asserts on patient data,
while Playwright is configured to retain traces, screenshots, and video on failure. Confirm what
those artifacts capture and where they are stored before the next failure produces them.

> **This ticket deliberately contains no captured data, no identifiers, and no credentials — only the
> mechanism.** Anyone investigating should treat the artifacts themselves as sensitive until reviewed.

## Context
`billing-user-flow.spec.ts` opens with a test titled
`"Billing user can navigate to appointment report and view patient data (PROVPERF-2665)"`. It runs
against production `zocdoc.com` as a real provider-side user and views an appointment report — a
screen that by design displays patient information.

## Current state
- The spec navigates a production provider inbox and asserts on the appointment report contents.
- Playwright artifact retention is enabled on failure (trace, screenshot, video). A retained trace
  contains full DOM snapshots and network payloads of the pages visited.
- The URLs involved embed real production identifiers.

**What is not yet established** — and is the point of this ticket:
1. Exactly what patient-identifying content, if any, appears in a retained trace/screenshot/video.
2. Where those artifacts are written, how long they are kept, and who can read them (local
   `test-output/`? CI build artifacts? an uploaded report?).
3. Whether any artifact path leaves Zocdoc-controlled storage.

## Why this matters
If a failure retains a trace containing patient information and that artifact is uploaded to a
location with broad access or long retention, it becomes a data-handling problem rather than a test
problem. The blast radius depends entirely on question 2, which is why this is an `investigate` and
not yet a fix.

Zocdoc policy treats patient names, appointment details, and anything plausibly identifying a patient
as PHI, and prohibits it leaving controlled systems.

## Decision rule
| Finding | Action |
|---|---|
| Artifacts contain no patient-identifying content | Close with the evidence recorded. No change needed. |
| Artifacts contain patient-identifying content **and** stay in Zocdoc-controlled, access-limited, short-retention storage | Document the handling, add a note to `OWNERSHIP.md`, close. |
| Artifacts contain patient-identifying content and are broadly accessible or long-retained | **Fix:** disable trace/screenshot/video retention for this spec specifically (`use: { trace: 'off', screenshot: 'off', video: 'off' }` at the describe level), or mask the region, or move the test to a non-production data set. Raise with whoever owns data handling. |

## Acceptance criteria
- [ ] Reproduce one failure locally and inspect the retained artifacts directly. Record **what
      categories** of data appear — do not paste the data into the ticket, Jira, or any PR.
- [ ] Document where artifacts are written in local runs and in CI, with retention and access.
- [ ] Apply the matching branch of the decision rule.
- [ ] If any content is patient-identifying, loop in the data-handling owner **before** closing. Do
      not self-clear.
- [ ] Record the outcome in `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md`.

## Files
| Path | Change |
|---|---|
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | read only — subject of the review; change only if the fix branch applies |
| `playwright.config.ts` | read only — confirm retention settings |
| `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` | change — record the outcome |

## Out of scope
- The broader question of running any tests against production patient data. Worth asking; too big
  for this ticket.
- Deduplication (SBX-001) — note that SBX-001 keeps this test, so this ticket survives it.

## Verification
Force a failure in the spec, inspect `test-output/`, and confirm the applied branch. If retention was
disabled, confirm no trace/screenshot/video is produced.

## Notes
Related but separate: the billing specs contain **hardcoded plaintext passwords** for test accounts.
That is SBX-004 and should not be bundled here — different risk, different fix.
