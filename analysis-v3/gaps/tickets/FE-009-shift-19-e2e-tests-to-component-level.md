# FE-009 — Shift 19 mocked E2E tests down to component tests

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P2 |
| Kind of test | Component test |
| Action | shift-left |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — E2E suite |
| Estimate | 1d |
| Labels | shift-left, e2e, component |
| Evidence revision | `dd9e4952a6` |

## Summary
Nineteen billing E2E tests assert component-level behaviour with a fully mocked backend — Component
confidence at browser-test cost. Re-implement each as a jsdom component test, then remove the browser test.

## Context
Every one of the 63 billing E2E tests mocks its entire backend: 13 REST endpoints stubbed, auth
stubbed, `/login/*` deliberately 500'd, and Stripe.js replaced by a fake installed unconditionally
for the whole directory (`apps/settings/e2e/fixtures.ts:32`). Nothing in the suite talks to a real
dependency, so no integration confidence is lost by moving a test down — only browser rendering,
which these 19 tests do not depend on.

## Current state
Per-test classification with the destination component named for each of the 19 is in
[`../../shift-left/E2E-TEST-BY-TEST.md`](../../shift-left/E2E-TEST-BY-TEST.md)
(verdict `shift-to-component`, 19 of 63 rows). The existing component suite these join is already substantial:
45 files / 515 tests, plus 9 hook files / 47 tests.

## Why this matters
Cost and feedback speed, not correctness. CI runs these serially (`playwright.config.ts:14`,
`workers: isCI ? 1 : undefined`) with a 60 s timeout each; the component-test equivalents run in milliseconds.
Faster signal also means less incentive to skip the suite locally.

## Tests being moved
19 tests, each `shift-to-component`. Rather than one ticket doing all 19, split by destination component so
each PR is reviewable:

| Batch | Source spec | Destination |
|---|---|---|
| A | `billing-settings-v2.spec.ts` | `PaymentMethodsList` / `PaymentMethodV2` component tests |
| B | `billing-invoice-summary.spec.ts` | Invoice summary component tests |
| C | `billing-pricing-v2.spec.ts` | `PricingInformationV2` / `PricingTab` component tests |
| D | `billing-settings-page.spec.ts`, `invoice-details-page.spec.ts` | Respective container component tests |

Exact per-test destinations come from the test-by-test file. Do not guess — each row names its target.

## Acceptance criteria
- [ ] For each of the 19: an component test exists asserting the same behaviour, **and it lands before** the
      E2E test is removed. In that order, in the same PR or an earlier one — never the reverse.
- [ ] Each new component test is named so its origin is traceable (reference the E2E test in a comment or
      the PR body).
- [ ] Where the E2E test asserted something jsdom genuinely cannot do (real layout, iframe), it is
      **not** shifted — it is escalated to FE-008's visual-regression treatment instead. Record any
      such case.
- [ ] E2E billing test count drops by 19 with no net loss of asserted behaviour.
- [ ] Verification: `yarn test .../billingSettings` and `yarn playwright test apps/settings/e2e/PracticeSettingsPages/` both pass.

## Files
| Path | Change |
|---|---|
| `apps/settings/src/pages/settingsPages/billingSettings/**/__tests__/*-tests.tsx` | change / **create** — 19 new component tests |
| `apps/settings/e2e/PracticeSettingsPages/*.spec.ts` | change — remove 19 E2E tests |

## Out of scope
The 39 `delete-redundant` tests (FE-010) — those are already covered at the component level and need no replacement.

## Blocked by
- **FE-001** — the real-Stripe smoke must exist first, or the suite loses its last real integration
  signal.
- **FE-008** — geometry assertions relocated first, so it is clear which tests genuinely need a browser.
- **FE-004** — six tests currently pass vacuously; fix them before deciding what they cover.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings
yarn playwright test apps/settings/e2e/PracticeSettingsPages/
```
Both green, E2E count down 19.

## Notes
**Residual caveat that applies to this whole ticket:** component tests prove a component *fires* an API
call; they do not prove the page wires that component up. For any single test that distinction is
immaterial. Across 19 + 39 removals it is real erosion — which is exactly what FE-001 exists to
backstop. Do not run this ticket without it.
