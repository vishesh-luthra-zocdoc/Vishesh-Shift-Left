# v3 Gap Backlog

**18 tickets.** Every one is a self-contained file in [`tickets/`](tickets/), ready to paste into
Jira with no further thinking. Shape defined by [`TICKET-TEMPLATE.md`](TICKET-TEMPLATE.md).

**Jira project: BILL** for everything.

Before creating these in Jira, spot-check the findings using
[`../VERIFY-THIS-FIRST.md`](../VERIFY-THIS-FIRST.md) — ten minutes of copy-pasteable commands against
the highest-risk claims.

**Status: backend tickets pending.** `zocdoc_web` (176 billing test files) and `provider-billing`
(80 files, never analyzed in v1/v2) are mid-analysis. `WEB-*` and `PB-*` tickets land in a follow-up
commit. The 18 below are complete and independently verified.

---

## By priority

### P0 — untested logic that can corrupt money or provider-facing data

| ID | Title | Level | Action | Est. |
|---|---|---|---|---|
| [FE-001](tickets/FE-001-real-stripe-payment-element-untested.md) | Add an integration test that a real Stripe Payment Element mounts and accepts a card | L5 | add-coverage | 1d |
| [FE-002](tickets/FE-002-monthly-limit-tautological-test.md) | Replace the tautological monthly-limit assertion with hardcoded boundary values | L1 | add-coverage | 45m |
| [FE-003](tickets/FE-003-invoice-helpers-untested.md) | Add unit tests for `invoiceHelpers.ts` | L1 | add-coverage | 45m |
| [X-001](tickets/X-001-cross-repo-selector-contract.md) | Prevent monorepo DOM changes from silently breaking the sandbox suite | L5 | add-coverage | 1d |

### P1 — real user-visible failure mode, or material CI cost

| ID | Title | Level | Action | Est. |
|---|---|---|---|---|
| [FE-004](tickets/FE-004-conditional-assertions-green-noops.md) | Fix six E2E tests whose assertions are entirely inside `if (mock.find(...))` | L5 | add-coverage | 2h |
| [FE-005](tickets/FE-005-zero-api-contract-tests.md) | Add API contract tests for the billing endpoints the UI consumes | L4 | add-coverage | 1d |
| [FE-006](tickets/FE-006-ach-no-e2e-coverage.md) | Add coverage for the ACH / bank-account add-payment-method path | L5 | add-coverage | 4h |
| [SBX-001](tickets/SBX-001-billing-specs-are-75-percent-duplicates.md) | Deduplicate the two sandbox billing specs (~75% identical) | L5 | delete | 2h |
| [SBX-002](tickets/SBX-002-billing-specs-cannot-run-in-parallel.md) | Make the billing specs safe to run in parallel (or enforce serialization) | L5 | investigate | 4h |
| [SBX-003](tickets/SBX-003-production-patient-data-in-trace-artifacts.md) | Review trace/screenshot/video retention on the spec that reads production patient data | L5 | investigate | 2h |
| [SBX-004](tickets/SBX-004-hardcoded-plaintext-test-credentials.md) | Move hardcoded plaintext test-account passwords out of the billing specs | L5 | add-coverage | 2h |

### P2 — meaningful gap, low blast radius

| ID | Title | Level | Action | Est. |
|---|---|---|---|---|
| [FE-007](tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) | Delete the empty E2E test and the four intra-suite duplicates | L5 | delete | 45m |
| [FE-008](tickets/FE-008-move-geometry-assertions-to-visual-regression.md) | Move the three layout-geometry assertions out of the functional E2E suite | L5 | shift-left | 4h |
| [FE-009](tickets/FE-009-shift-19-e2e-tests-to-component-level.md) | Shift 19 mocked E2E tests down to L2 component tests | L2 | shift-left | 1d |
| [FE-010](tickets/FE-010-delete-39-redundant-e2e-tests.md) | Delete 39 E2E tests already covered by named L2 tests | L5 | delete | 1d |
| [FE-011](tickets/FE-011-investigate-iframe-deprecation-flag.md) | Determine the `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` ramp state | L2 | investigate | 2h |
| [FE-012](tickets/FE-012-legacy-invoice-view-coverage.md) | Assess coverage of `LegacyInvoiceView`, now that it renders unconditionally | L2 | investigate | 2h |

### P3 — polish

| ID | Title | Level | Action | Est. |
|---|---|---|---|---|
| [FE-013](tickets/FE-013-thirteen-source-files-with-no-coverage.md) | Add coverage for the 13 billing source files with no tests at all | L2 | add-coverage | 1d |

---

## Sequencing — read this before starting the E2E work

The shift-left tickets are **ordered on purpose**. Running FE-007 + FE-009 + FE-010 without FE-001
leaves the billing E2E suite with essentially **one** test exercising a multi-page journey. Every
individual verdict would be correct and the suite would still be worse: cheaper, and blind to whether
the page wires itself together at all.

```
FE-004  (make the suite tell the truth — 6 tests currently pass vacuously)
   ↓
FE-001  (establish the floor — the ONLY real-dependency test)
FE-008  (relocate geometry assertions so it's clear what needs a browser)
   ↓
FE-007  (free wins — empty test + 4 duplicates)
   ↓
FE-009  (shift 19 down to L2 — each L2 test lands BEFORE its E2E counterpart is removed)
   ↓
FE-010  (bulk delete 39 — last, deliberately)
```

`X-001` should land before `FE-011`, since FE-011 is a flag teardown of exactly the kind that broke
the sandbox suite on 2026-09-02.

`SBX-001` before `SBX-002` and `SBX-004` — deduplication removes two racing tests and one credential
site for free.

## Independent, no sequencing

`FE-002`, `FE-003`, `FE-005`, `FE-012`, `FE-013`, `SBX-003`. Start any of these today.

## Fastest value

| Ticket | Est. | Why |
|---|---|---|
| FE-003 | 45m | Pure functions, no mocking, no async. Cheapest P0 in the backlog. |
| FE-002 | 45m | Converts a test that *cannot fail* into one that can. |
| FE-007 | 45m | Deletes 5 tests with zero coverage risk. |

## Jira key mapping

Filled in after creation, so the local handles stay traceable:

| Local ID | Jira key |
|---|---|
| FE-001 | _pending_ |
| FE-002 | _pending_ |
| FE-003 | _pending_ |
| FE-004 | _pending_ |
| FE-005 | _pending_ |
| FE-006 | _pending_ |
| FE-007 | _pending_ |
| FE-008 | _pending_ |
| FE-009 | _pending_ |
| FE-010 | _pending_ |
| FE-011 | _pending_ |
| FE-012 | _pending_ |
| FE-013 | _pending_ |
| SBX-001 | _pending_ |
| SBX-002 | _pending_ |
| SBX-003 | _pending_ |
| SBX-004 | _pending_ |
| X-001 | _pending_ |
