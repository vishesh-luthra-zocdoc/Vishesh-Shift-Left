# FE-007 — Delete the empty E2E test and the four intra-suite duplicates

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Chore |
| Priority | P2 |
| Test level | L5 e2e |
| Action | delete |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — E2E suite |
| Estimate | 45m |
| Labels | shift-left, e2e, cleanup |
| Evidence revision | `dd9e4952a6` |

## Summary
Five billing E2E tests can be removed with **zero** coverage risk: one has an empty body, and four
duplicate another test in the same suite. This is the free-wins phase of the shift-left plan.

## Current state
- `billing-settings-v2.spec.ts:175` — **verified empty body**. Lines `:175-179` contain a single
  `setUpRoutesAndVisitBillingPage(page, practiceId, {})` call and **no assertions**. Its title is
  copy-pasted from the test at `:56`.
- Four further tests duplicate an earlier test in the same spec (6.3% of the 63-test suite). Each is
  identified with its duplicate in
  [`../../analysis-scratch/e2e-shift-left-candidates.md`](../../analysis-scratch/e2e-shift-left-candidates.md).

## Why this matters
Low blast radius — this is cost and clarity, not correctness. Each test costs a browser boot on a CI
job that runs **one worker** (`apps/settings/playwright.config.ts:14`, `workers: isCI ? 1 :
undefined`) with a 60 s timeout. The empty test is actively misleading: it reports coverage of a
scenario it does not touch.

## Tests being removed
| # | Test | Why removable |
|---|---|---|
| 1 | `billing-settings-v2.spec.ts:175` | Empty body, zero assertions. Deleting cannot reduce coverage. |
| 2–5 | 4 intra-suite duplicates | Each asserts exactly what an earlier test in the same file asserts. Cite the surviving test in the PR. |

## Acceptance criteria
- [ ] `billing-settings-v2.spec.ts:175-179` deleted.
- [ ] The four duplicates deleted, each with its **surviving counterpart named in the PR description**
      (per the `delete`-must-cite rule).
- [ ] Suite still green; test count drops from 63 to 58.
- [ ] Verification: `yarn playwright test apps/settings/e2e/PracticeSettingsPages/` passes.

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts` | change — delete tests |

## Out of scope
The 39 `delete-redundant` candidates (FE-010) and the 19 L2 shifts (FE-009). Those change coverage
posture and are gated on FE-001. This ticket is only the risk-free subset.

## Verification
```
yarn playwright test apps/settings/e2e/PracticeSettingsPages/
```
Passing with 58 tests instead of 63.

## Notes
Do FE-004 first. It repairs six tests that currently pass vacuously — one of them may turn out to be
a sixth free win once it is made to assert honestly.
