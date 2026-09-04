# FE-008 — Move the three layout-geometry assertions out of the functional E2E suite

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P2 |
| Test level | L5 e2e |
| Action | shift-left |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — visual regression |
| Estimate | 4h |
| Labels | shift-left, e2e, visual-regression |
| Evidence revision | `dd9e4952a6` |

## Summary
Three E2E tests exist **only** to assert pixel geometry, and they are currently the sole
justification for keeping those tests alive. Move the assertions to a visual-regression check so the
functional suite can shrink without losing the layout guarantees.

## Context
Of the 5 billing E2E tests classified `keep-e2e`, **3 are kept purely for layout measurements** — not
for any integration behaviour. That means the functional suite's "floor" is mostly geometry, and
FE-009/FE-010 cannot proceed cleanly until these assertions live somewhere appropriate.

## Current state
| Test | What it asserts |
|---|---|
| `billing-invoice-summary.spec.ts:297` | Reads `boundingBox()` y-coordinates to assert row ordering |
| `payment-recovery.spec.ts:156` | Real toast geometry — `overflow === 0`, `height === 68` |
| `payment-recovery.spec.ts:233` | `scrollTop === 0` when content overflows (BILL-1083) |

The `height === 68` assertion traces to `ad433d2bee` (#11628, BILL-1097) `match the toast's vertical
padding to the design spec` — a **real design bug** was fixed and guarded. The guard simply landed at
the most expensive level available.

## Why this matters
These are legitimate regressions to guard — a collapsed toast or a mis-ordered invoice table is
provider-visible. But guarding them inside functional E2E has two costs: each assertion pays a full
browser boot on a serial CI job, and their presence blocks the removal of ~58 mocked browser tests
because they are the only thing keeping their host tests alive.

Deleting them would lose real coverage. Leaving them blocks the shift-left. Moving them resolves both.

## Tests being moved
| # | From | To |
|---|---|---|
| 1 | `billing-invoice-summary.spec.ts:297` (row ordering via `boundingBox()`) | Visual-regression snapshot of the invoice summary table |
| 2 | `payment-recovery.spec.ts:156` (toast `height === 68`, `overflow === 0`) | Visual-regression snapshot of the recovery toast |
| 3 | `payment-recovery.spec.ts:233` (`scrollTop === 0` on overflow) | Visual-regression snapshot, overflowing-content state |

## Acceptance criteria
- [ ] Confirm the mechanism first: does the repo already have a visual-regression setup (Playwright
      `toHaveScreenshot`, Chromatic, Percy)? **Use the existing one if so** — do not introduce a
      second. Record the finding on the ticket.
- [ ] Each of the three assertions has an equivalent visual check that fails when the layout breaks.
- [ ] Prove it: revert `ad433d2bee`'s padding change locally; the new toast check must **fail**.
- [ ] The three host E2E tests are re-classified — they no longer need `keep-e2e` status and become
      eligible for FE-009/FE-010.
- [ ] Verification: the visual suite passes, and the sabotage check above fails.

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/billing-invoice-summary.spec.ts` | change — remove geometry assertion |
| `apps/settings/e2e/PracticeSettingsPages/payment-recovery.spec.ts` | change — remove 2 geometry assertions |
| visual-regression location (TBD by the first AC) | **create** — 3 checks |

## Out of scope
Broader visual coverage of Billing Settings. Move these three; do not open a general visual-testing
programme here.

## Verification
Run the visual suite; then revert `ad433d2bee` locally and confirm the toast check fails. A visual
check that cannot detect the bug it replaced is not a replacement.

## Notes
- `payment-recovery.spec.ts:96` (the full money-recovery journey across a page transition) is the
  **one** genuinely integration-valuable E2E test in the suite. It stays regardless of this ticket.
- Blocks FE-009 and FE-010 in the recommended sequencing.
