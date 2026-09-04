# FE-006 — Add coverage for the ACH / bank-account add-payment-method path

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P1 |
| Test level | L5 e2e |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — ACH / bank account |
| Estimate | 4h |
| Labels | shift-left, test-coverage, e2e, revenue-path, ach |
| Evidence revision | `dd9e4952a6` |

## Summary
No E2E test ever selects the bank-account option, so the entire ACH add-payment-method path is
unexercised end to end — including its Financial Connections OAuth handoff.

## Context
Providers can pay by card or by bank account (ACH). ACH is the cheaper rail and is preferred for
larger practices, so the path carries real revenue. It is rendered by `AchFormContentV2.tsx` and
involves a Stripe Financial Connections flow that leaves the app.

## Current state
- `mockAchInfo` **exists** in the E2E fixtures — but **no spec ever selects the option that renders
  the ACH form**. The mock is dead weight: present, never reached.
- `AchFormContentV2.tsx:69` reads the `SHOULD_MOCK_STRIPE` test cookie, so even if a spec did reach
  it, it would exercise the mocked branch rather than the real one.
- Financial Connections OAuth (a redirect out of the app and back) is untested at every level.

## Why this matters
ACH entry can break completely and every test stays green. Blast radius: providers who pay by bank
account cannot set up payment — and these skew toward larger practices, so the revenue per failure
is higher than the card path. The OAuth redirect is exactly the kind of flow that only breaks in a
real browser, which is where we have no coverage.

## Acceptance criteria
- [ ] A spec selects the bank-account option and asserts the ACH form renders — closing the
      "`mockAchInfo` is never reached" gap.
- [ ] The happy path is asserted through to a saved ACH payment method.
- [ ] Validation errors on the ACH form are asserted (invalid routing/account input).
- [ ] The Financial Connections redirect boundary is covered at least to the handoff: assert the app
      initiates it correctly and handles the return. If a full OAuth round trip is not automatable,
      cover the handoff and **state the limitation in the spec as a comment**.
- [ ] Verification: `yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-settings-payment-element.spec.ts` passes.

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | Select bank account in add-payment-method | ACH form renders; `mockAchInfo` is actually consumed |
| 2 | Valid ACH details, submit | Method saves; appears in the list as a bank account |
| 3 | Invalid routing number | Visible validation error; submit blocked |
| 4 | Initiate Financial Connections | App hands off correctly with expected parameters |
| 5 | Return from Financial Connections | App handles the return and reflects the linked account |

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/billing-settings-payment-element.spec.ts` | change — add ACH tests |
| `apps/settings/e2e/fixtures.ts` | read only — confirm `mockAchInfo` is now reached |
| `apps/settings/src/pages/settingsPages/billingSettings/AddPaymentMethodModalV2/AchFormContentV2.tsx` | read only — subject under test |

## Out of scope
- Backend ACH settlement, returns, and NSF handling — backend repos own these.
- The real-Stripe harness itself — that is FE-001 and should land first.

## Verification
```
yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-settings-payment-element.spec.ts
```
Passing = the ACH branch is reached and asserted. Confirm `mockAchInfo` is genuinely consumed (a
breakpoint or a deliberate mock change should affect the test).

## Notes
Depends on FE-001 for the real-Stripe harness if case 4/5 are done against real Financial
Connections. Cases 1–3 can land against the existing mocked fixture immediately — do not block all
of this on FE-001.
