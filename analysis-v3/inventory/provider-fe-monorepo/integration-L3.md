# provider-fe-monorepo — L3 (integration) Billing Tests

**Analyzed revision:** `provider-fe-monorepo` @ `origin/main` `dd9e4952a6` (2026-09-03)
**Snapshot:** `/tmp/slv3/snapshots/provider-fe-monorepo/` — no `package.json`, no `node_modules`; Jest was not run.
All counts are static (declared blocks = lines matching `^\s*(it|test)[.(]`).

## Headline finding: there is no real-boundary integration tier

**Zero billing tests cross a real boundary.** Stated plainly, because an empty L3 tier in a frontend is itself the
finding:

- **No MSW.** `grep -rln "msw|setupServer|setupWorker" --include="*.ts" --include="*.tsx"` over the whole snapshot
  returns three files, and all three are false positives — base64/byte-string fixtures that happen to contain the
  substring: `shared/core/src/dev/mock-server/mockJpegByteString.ts`,
  `apps/settings/src/server/controllers/practiceProfileSettingsPage/providerProfileExcelBase64MockData.ts`,
  `apps/provider-home-webapp/src/server/mocks/base64File.ts`. There is no `setupServer(...)` call anywhere.
- **No `nock`.** `grep -rln "nock("` returns nothing.
- **No in-memory HTTP pipeline, no test DB, no LocalStack** — none apply to this repo, and nothing equivalent exists.
- Every test that needs data mocks the module that fetches it: `jest.mock('pages/settingsPages/billingSettings/apiCalls')`
  (8 files), `jest.mock('../billingApiClient')`, `jest.mock('@zocdoc/billing-monolith-api-client')`,
  `jest.mock('@zocdoc/provider-core/lib/utils/fetchHelperV2')`, `jest.mock('gql/gqlHelper')`.

Consequence: **no non-E2E test in the billing scope ever asserts a request/response contract against a real HTTP
layer.** The URL templates in `apps/settings/src/config/routes.ts`, the serialization in `apiCalls.ts`, and the
generated `@zocdoc/billing-monolith-api-client` are all verified against mocks that the same tests define. A backend
field rename, a status-code change, or a route-template typo is caught only at L5 (Playwright) or in production.
See `api-coverage.md` for the endpoint-by-endpoint view; the L4 tier is also empty (0 files).

What *does* exist at L3 is **in-process composition**: two files that render a multi-component tree through a real
React context/provider with two or more real collaborators and no browser. Under the CONVENTIONS.md rule
("multi-component tree with a real provider/context" → L3) they qualify, and they are catalogued below — but they are
a weaker kind of L3 than the definition's "real infra" examples, and I flag them as such rather than letting the
count imply boundary coverage.

## L3 files (2 files, 70 declared blocks)

### 1. `apps/settings/src/pages/settingsPages/billingSettings/__tests__/BillingSettingsContainer-tests.tsx`

1141 lines, **35 declared blocks**, 4 `it.each`, 11 `describe`, 17 `jest.mock`.

`describe` names, verbatim:

1. `Billing page tests` (:230)
2. `bootstrap decouple experiment` (:322)
3. `billing completion modal vs toast (BILL-894)` (:386)
4. `recovery banner placement (BILL-967)` (:526)
5. `Review and pay CTA gate reads billing_review_and_pay_cta independently (BILL-971)` (:599)
6. `Pay Now modal gating (BILL-971)` (:685)
7. `page state after a recovery card is replaced (BILL-1084)` (:756)
8. `recovery summary refresh on a default-card change (BILL-1113)` (:861)
9. `rollover-blocked ids derived from the payment-method list (BILL-1017)` (:885)
10. `experiment readiness gate` (:902)
11. `recovery banner suppression` (:935)

**Why L3, not L2.** It renders the real page shell inside a real `MemoryRouter` (`:21`, `:298`) and the container
mounts the real `BillingSettingsContext.Provider` (`BillingSettingsContainer.tsx:257–288`). Left **unmocked** and
therefore real: `PaymentMethodsList.tsx` (V1 adapter) → `PaymentMethodsListV2.tsx` → `PaymentMethodV2.tsx`,
`PricingInformation.tsx` → `PricingInformationV2.tsx`, `BillsContainer.tsx`, `BillingContactInfo.tsx`,
`BillingCompletionModal.tsx`, and the real core suppression helpers imported at `:23–28`
(`buildSuppressionKey`, `evaluateRecoverySuppression`, `suppressRecoveryBanner`) operating over jsdom
`localStorage` (`:425` removes `'has_seen_billing_completion_modal'`). That is a multi-component tree plus a real
provider plus a real persistence mechanism — 2+ real collaborators, no browser.

**What it covers.** Tab routing; the bootstrap-decoupling gate; completion-modal-vs-toast precedence; recovery
banner placement and suppression; the `billing_review_and_pay_cta`, Pay Now, and `billing_payment_recovery_experience`
gates read independently; page state after a recovery card replacement; recovery-summary refresh on a default-card
change; rollover-blocked id derivation.

**What it does not cover.** The 17 mocks are the boundary: `apiCalls`, `usePracticeBillingSettings` (:55),
`useRecoverySummary` (:61), `InvoiceDetailsContainer` (:69), `gql/gqlHelper` (:44),
`getBillingStripePromise` (:41), `useExperiments` (:49), `useEntityFlag` (:52), `useBillingToast` (:136),
modal context (:140), toast (:132), `utils-frontend-metrics` (:184), and — importantly — the core
`RecoveryStatusBanner` (:205). So the banner it asserts is a stub, not the real core component.
**`PayNowModal` is never rendered here**: the modal context is mocked and the test reads the props off the
`openModal` mock via `getLastPayNowModalProps()` (:150–152), matching on the component identity. The Pay Now tree
itself is covered by the second L3 file.

**Snapshot caveat.** This file imports `PAYMENT_RECOVERY_EXPERIENCE` and `REVIEW_AND_PAY_CTA` from `ab/experiments`
(:32–35), and `apps/settings/src/ab/` is **not present in the snapshot** (it was outside the filtered scope). The
constants' values are therefore UNVERIFIED — I would need `apps/settings/src/ab/experiments.ts` to resolve them.
The literal experiment keys asserted in this file are visible at `:425`, `:599`, `:633`, `:652`.

### 2. `apps/settings/src/pages/settingsPages/billingSettings/PaymentRecovery/__tests__/PayNowModal-tests.tsx`

796 lines, **35 declared blocks**, 2 `it.each`, 4 `describe`, 6 `jest.mock`.

`describe` names, verbatim:

1. `PayNowModal step machine` (:225)
2. `itemized balance load` (:242)
3. `rollover-blocked methods` (:331)
4. `update-only mode (payNowEnabled=false)` (:573)

**Why L3, not L2.** It renders the real `PayNowModal` → real `ReviewStep` → real core `FailedPaymentsByMonth`
(`ReviewStep.tsx:3`) → real core `FailedPaymentMethodCard` (`FailedPaymentsByMonth/index.tsx:14`) → real
`recoveryCopy` helpers (`formatBalance`, `formatShortMonth`, `FailedPaymentsByMonth/index.tsx:11–13`), plus the real
`BillingModalFooter`. Four real collaborators across the `apps/settings` → `shared/core` package boundary in one
tree, no browser.

**What it covers.** The Pay Now step machine end to end in-process: itemized balance load and its fallback,
rollover-blocked method handling, and the update-only mode when `payNowEnabled=false`.

**What it does not cover.** Mocks: `utils-frontend-metrics` (:15), modal context (:19),
`components-overlay` (:28), `CardEntryStep` (:108), `apiCalls` (:160), `useRecoveryBalanceDetail` (:170). The
`CardEntryStep` stub is documented in the file as mirroring the real `handleTokenized` (awaits `onComplete`,
swallows rejection), with inline-error behaviour deferred to `CardEntryStep-tests.tsx` (L2). So **no test renders
the real Stripe card entry inside the real Pay Now tree** — the highest-risk composition in the billing product
(entering a new card to clear a failed balance) is split across an L3 tree with a stubbed card step and an L2 card
step with stubbed Stripe.

## Borderline L2/L3 — flagged, counted as L2

These four render 2+ real collaborators but a single component under test, so I kept them at L2. Listing them so the
L3 count is not read as "only two files compose real code".

| File | Level assigned | Real collaborators | Why not L3 |
|---|---|---|---|
| `PaymentRecovery/steps/__tests__/ReviewStep-tests.tsx` (12 blocks) | L2 | **Zero `jest.mock`.** Real core `FailedPaymentsByMonth` → real `FailedPaymentMethodCard` → real `recoveryCopy` | One component under test with props; no provider/context and no data layer at all. Closest file in the scope to L3 without being it |
| `__tests__/billing-analytics-events-tests.tsx` (11 blocks) | L2 | Real `BillingSettingsContext.Provider`, real `initializeMetricsDataOnWindow`, five real components (`FAQsSection`, `MarketplaceCard`, `PaymentMethodsListV2`, `BillingContactInfo`, `Bill`) | Renders the five independently rather than as one tree; the concern is analytics wiring, not composition |
| `shared/core/src/components/AddPaymentMethodModal/__tests__/BillingAddressFields-tests.tsx` (5 blocks) | L2 | Real `useBillingAddressForm` (react-hook-form + `billingAddressSchema`) | Single component, one mock (dropdown) |
| `shared/core/src/billing/__tests__/useBillingAddressPrefill-tests.ts` (4 blocks) | L2H | Real `useBillingAddressForm` + real schema, only `getBillingAddress` mocked | Hook under test, not a tree |
| `shared/core/src/components/FailedPaymentsByMonth/__tests__/FailedPaymentsByMonth-tests.tsx` (13 blocks) | L2 | **Zero mocks**; real `FailedPaymentMethodCard` + real copy helpers | Single component under test with props |

## Candidate Gaps

| # | What's missing | Level | Path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| L3-1 | **No MSW (or any) request-boundary layer exists.** Nothing between "module mocked in Jest" and "Playwright against production" | L3 | Whole scope; `apps/settings/.../apiCalls.ts`, `apps/settings/src/config/routes.ts:562–683`, `shared/core/src/billing/billingApiClient.ts` | Every request shape, route template, and response mapping on the billing money path is validated only against mocks the tests themselves author. Backend field renames and status-code changes are invisible until L5. Standing up MSW once unlocks real coverage for all 12 route templates | M (setup) + S per suite | **P0** |
| L3-2 | No test renders the real Stripe card entry inside the real Pay Now tree — `PayNowModal-tests.tsx:108` stubs `CardEntryStep`, and `CardEntryStep-tests.tsx` stubs `@stripe/react-stripe-js` and `@stripe/stripe-js` | L3 | `PaymentRecovery/__tests__/PayNowModal-tests.tsx`, `steps/__tests__/CardEntryStep-tests.tsx`, `shared/core/src/testing/installStripeJsFake.ts` | The declined-card recovery flow is the product's highest-consequence path; the composition of card entry + charge is asserted nowhere below L5. `installStripeJsFake.ts` (130 lines) already exists and is used only by `apps/settings/e2e/fixtures.ts` and a Storybook story | M | **P0** |
| L3-3 | No test composes an app consumer with the real core `AddPaymentMethodElementModal` — both consumers stub it (`AddPaymentMethodModalV2-tests.tsx:30`, `ActivationAddPaymentMethodModal-tests.tsx:31`) | L3 | those two files + `shared/core/src/components/AddPaymentMethodModal/AddPaymentMethodElementModal.tsx` | The Stripe Payment Element extraction created a package seam with tests on both sides and nothing across it; a prop-contract break ships | M | **P1** |
| L3-4 | `BillingSettingsContainer-tests.tsx` mocks the core `RecoveryStatusBanner` (:205) even though the real one is a zero-mock component with its own 9-block suite | L3 | `__tests__/BillingSettingsContainer-tests.tsx:205` | Un-mocking it would make the banner-placement and suppression describes assert real rendered copy instead of a stub, at near-zero cost | XS | P2 |
| L3-5 | Pure derivations asserted through a full-page L3 render: `rollover-blocked ids derived from the payment-method list (BILL-1017)` and parts of `recovery banner suppression` | L1 | `__tests__/BillingSettingsContainer-tests.tsx:885,935` | Slowest possible place to test a pure function; extract the derivation and cover it at L1, leave the wiring assertion at L3 | S | P2 |
| L3-6 | The only two L3 files are both in `apps/settings`; `shared/core`, `provider-home-webapp` and `spo-webapp` have **no L3 tests at all** | L3 | `shared/core/src/**`, `apps/provider-home-webapp/src/**`, `apps/spo-webapp/src/**` | `shared/core` is the package every consumer depends on, and it is verified only as isolated units and components | M | P2 |

## Level Summary

| Level | Files | Declared blocks | `it.each` declarations | `describe` blocks |
|---|---|---|---|---|
| L1 unit | 34 | 224 | 49 | 73 |
| L2 component render | 45 | 515 | 43 | 112 |
| L2H hook render | 9 | 47 | 4 | 12 |
| **L3 integration (this file)** | **2** | **70** | **6** | **15** |
| — of which cross a real network/infra boundary | **0** | **0** | — | — |
| — of which are in-process composition only | 2 | 70 | 6 | 15 |
| L4 api | 0 | 0 | 0 | 0 |
| Total non-E2E billing | **90** | **856** | **102** | **212** |

L3 by area: `apps/settings` 2 files / 70 blocks. `shared/core` 0. `apps/provider-home-webapp` 0. `apps/spo-webapp` 0.
Both L3 files are among the four largest test files in the scope (1141 and 796 lines; only `FpbInvoiceView-tests.tsx`
at 1283 and `PaymentMethodV2-tests.tsx` at 847 are comparable).
