# FE-001 — Add an integration test that a real Stripe Payment Element mounts and accepts a card

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P0 |
| Kind of test | Browser test |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — add payment method |
| Estimate | 1d |
| Labels | shift-left, test-coverage, e2e, revenue-path |
| Evidence revision | `dd9e4952a6` |

## Summary
Adding a payment method — the single most revenue-critical action in Billing Settings — is untested
against a real Stripe at every level. This ticket adds one E2E test that mounts a genuine Stripe
Payment Element and completes a card entry, so a Stripe.js break is caught before providers hit it.

## Context
Providers add a card or bank account in Billing Settings so Zocdoc can bill them. Since
`70a384854e` (2026-09-02) tore down the `billing_payment_element_flow` flag, the Stripe Payment
Element is the **only** path — there is no legacy fallback to catch us. The Element is an iframe
served by Stripe and mounted by Stripe.js at runtime.

## Current state
**No test at any level exercises a real Stripe Payment Element.**

- All 63 billing E2E tests run with a fake Stripe.js installed unconditionally for every test in the
  directory: `apps/settings/e2e/fixtures.ts:32`.
- All 13 backend REST endpoints are stubbed in the same fixture; `/login/*` is deliberately 500'd.
- The component tests (`AddPaymentMethodElementModal-tests.tsx`) render in jsdom, where a Stripe iframe
  cannot mount at all.
- Production components additionally branch on a test-only cookie, `SHOULD_MOCK_STRIPE`
  (`AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:52`,
  `AddPaymentMethodModalV2/AchFormContentV2.tsx:69`) — so the E2E green path runs code real users
  never run. (`dd9e4952a6` is already moving this mock out of production code.)

Net: nothing proves a real Element mounts, validates a card, or that a saved method persists.

## Why this matters
A Stripe.js version bump, a publishable-key misconfiguration, or a CSP change breaks card entry in
production **with all 63 E2E tests green**. Blast radius: every provider who tries to add a payment
method. They cannot pay Zocdoc; we do not collect revenue; the failure is invisible to CI and shows
up as support tickets.

This is the highest-value gap in the entire v3 analysis. It is worth more than the 39-test deletion
in FE-010 — that saves CI minutes, this prevents a revenue outage.

## Acceptance criteria
- [ ] Create `apps/settings/e2e/PracticeSettingsPages/billing-payment-element-real.spec.ts`.
- [ ] The spec does **not** call `installStripeJsFake` and does **not** set `SHOULD_MOCK_STRIPE`.
- [ ] It loads Billing Settings against a real backend, opens the add-payment-method modal, and
      asserts the Stripe Element iframe is present and interactive.
- [ ] It enters a Stripe **test** card (`4242 4242 4242 4242`) and asserts the method is saved.
- [ ] It asserts a declined test card (`4000 0000 0000 0002`) surfaces a user-visible error.
- [ ] The spec is tagged so it can run separately from the mocked suite (e.g. `@real-stripe`), and
      is excluded from the default `yarn e2e` run if it needs credentials.
- [ ] Verification: `yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-payment-element-real.spec.ts` passes.

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | Open add-payment-method modal | Stripe Element iframe mounts and is interactive |
| 2 | Enter test card `4242 4242 4242 4242`, submit | Method saves; appears in the payment methods list |
| 3 | Enter declined card `4000 0000 0000 0002`, submit | User-visible decline error; no method saved |
| 4 | Submit with an empty Element | Validation error from Stripe, submit blocked |

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/billing-payment-element-real.spec.ts` | **create** |
| `apps/settings/e2e/fixtures.ts` | change — allow opting out of `installStripeJsFake` (currently unconditional at `:32`) |
| `apps/settings/playwright.config.ts` | change — add a project/tag for real-dependency specs |

## Out of scope
- 3DS / SCA challenge flows — a follow-up once this harness exists.
- ACH / bank account entry — that is FE-006.
- Removing the mocked suite — that is FE-009/FE-010, and must land *after* this.

## Verification
```
yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-payment-element-real.spec.ts
```
Passing = the Element mounted, the test card saved, and the declined card produced a visible error.

## Notes
- **This is the "floor" test.** FE-009 and FE-010 remove or downgrade large parts of the E2E suite;
  neither should merge until this exists, or the suite loses its last real integration signal.
- `a633542cab` (#11400, 2026-07-22) `use Stripe sandbox for all test practices (drop entity-flag
  gate)` means test practices already point at a Stripe sandbox — check whether that supplies the
  credentials this spec needs before building new plumbing.
- Requires a Stripe test-mode publishable key available to CI. If that is blocked, land the spec
  as a locally-runnable check and open a follow-up for CI wiring rather than dropping the ticket.
