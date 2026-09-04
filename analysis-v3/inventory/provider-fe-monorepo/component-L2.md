# provider-fe-monorepo — L2 (component) Billing Tests

**Analyzed revision:** `provider-fe-monorepo` @ `origin/main` `dd9e4952a6` (2026-09-03)
**Snapshot:** `/tmp/slv3/snapshots/provider-fe-monorepo/` — no `package.json`, no `node_modules`, so Jest was not
run. All counts are static: **declared blocks** = lines matching `^\s*(it|test)[.(]`; an `it.each([...])` counts as
one declared block though it expands to N runtime cases. `describe` names are quoted verbatim.

## This is the biggest bucket — and the v2 correction

v2 counted these as "unit tests". They are not. **54 of the 90 non-E2E billing test files (60%) mount React**, and
they hold **562 of 856 declared blocks (66%)**. The L1 tier is 34 files / 224 blocks. The pyramid is inverted at
the component layer and there is no meaningful integration layer (see `integration-L3.md`).

Two sub-kinds are separated here because they behave very differently in CI and in failure mode:

| Sub-level | Mechanism | Files | Declared blocks |
|---|---|---|---|
| **L2** component render | `renderComponent(...)` / `render(...)` from RTL, single component under test, data layer mocked | 45 | 515 |
| **L2H** hook render | `renderHook(...)` — no DOM assertions, but it does mount a host component and use `act()` | 9 | 47 |
| **L2 total** | | **54** | **562** |

Why `renderHook` is L2 and not L1: CONVENTIONS.md L1 requires "no React render". `renderHook` mounts through the
reconciler, so these tests can fail on effect ordering, `act()` warnings, and React version changes — failure modes
a pure-function test cannot have. They are not L3 either: each drives one hook with its data source `jest.mock`ed.

The render helper in this monorepo is `renderComponent` from `@zocdoc/provider-core/lib/testUtils` (settings,
provider-home) or `@zocdoc-frontend-common/test-utils` / a local `../../testUtils` (shared/core). A grep for bare
`render(` misses most of this tier — that is likely how v2 mislabelled it.

## L2 — apps/settings, billing page (32 files, 401 blocks)

| Test file (under `apps/settings/src/pages/settingsPages/billingSettings/`) | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `__tests__/BillsContainer-tests.tsx` | 17 | 0 | `BillsContainer`, `edge cases`, `empty state`, `bill selection`, `internal user visibility` | Bill list rendering, selection, empty state, internal-only affordances | Mocks `urlNavigator`, `utils-frontend-metrics`, `components-dropdown` |
| `__tests__/BillingContactInfo-tests.tsx` | 14 | 1 | `BillingContactInfo` | Contact rows, edit affordances, permission variants | **Zero `jest.mock`** — relies on props only |
| `__tests__/BillingCompletionModal-tests.tsx` | 5 | 0 | `BillingCompletionModal`, `when user is not FullAdmin` | Post-setup confirmation modal, role gating | Mocks `urlNavigator`, modal context, navbar, `featureFlagUtils` |
| `__tests__/InvoiceDetailsContainer-tests.tsx` | 17 | 0 | `InvoiceDetailsContainer`, `Routing Logic`, `PDF URL Generation` | Legacy-vs-FPB invoice routing and the PDF URL it builds | Mocks `../apiCalls`, `useExperiments`, toast, **and `v2/FpbInvoiceView`** — so the FPB branch is asserted only as "the right child was chosen" |
| `__tests__/LegacyInvoiceView-tests.tsx` | 12 | 0 | `LegacyInvoiceView` | The legacy invoice table (still live — rendered at `InvoiceDetailsContainer.tsx:201`) | Zero mocks; pure props |
| `v2/__tests__/FpbInvoiceView-tests.tsx` | 52 | 8 | `FpbInvoiceView`, `PDF button toast behavior`, `Bookings CSV download (BILL-1135)`, `Totals and Payments`, `Sponsored Results`, `Taxes and Fees Section`, `from Zocdoc Marketplace`, `Shadow PDF download popover`, `Healthcare platforms row (fallback path)`, `booking source breakdown rows` | **The largest L2 suite in the scope** (1283 lines): the whole FPB invoice — money rows, totals, taxes, sponsored results, CSV/PDF download, booking-source fallbacks | Only mocks `components-toast`; renders real sections and real `formatCurrency` |
| `v2/__tests__/TaxesAndFeesSection-tests.tsx` | 7 | 1 | `TaxesAndFeesSection` | Tax/fee rows and totals | Zero mocks |
| `__tests__/FeaturedProviderSection-tests.tsx` | 7 | 0 | `FeaturedProviderSection` | Featured-provider invoice section | Zero mocks; exercises the file's own local `formatCurrency` copy |
| `__tests__/LicenseFeeSection-tests.tsx` | 6 | 1 | `LicenseFeeSection` | License-fee invoice section | Zero mocks; second local `formatCurrency` copy |
| `__tests__/PatientBookingsSection-tests.tsx` | 7 | 0 | `PatientBookingsSection` | Per-booking invoice rows | Zero mocks |
| `__tests__/PricingInformationV2-tests.tsx` | 40 | 0 | `PricingInformationV2`, `Loading state`, `Marketplace enrolled state`, `Empty state`, `Bookable Presence card`, `Marketplace card selected but not activated`, `FAQs section`, `Contact footer`, `Error state`, `with providers prop (decoupled from bootstrap)`, `Provider Repositioning gating (feature flag AND entity flag)`, `Updated calculator copy gating (billing_updated_calculator_copy)` | Pricing tab in all states plus both flag gates | Heaviest mock set in the scope (10 `jest.mock`s incl. `gql/gqlHelper`, `useExperiments`, `useEntityFlag`, dialog, avatar, spinner, metrics, analytics) |
| `__tests__/PricingTab-tests.tsx` | 2 | 0 | `Billing page pricing tab tests` | The **V1** `PricingInformation.tsx` adapter — 2 blocks, and the file name matches neither component | 9 `jest.mock`s; no assertion on the fetch-then-render contract V1 exists to provide |
| `v2/MarketplaceCard.test.tsx` | 10 | 0 | `MarketplaceCard`, `repositioning variant (isProviderRepositioning=true)`, `calculate revenue button`, `non-repositioning variant (isProviderRepositioning=false)` | Both repositioning variants and the calculator CTA | Mocks `utils-frontend-metrics` |
| `v2/BookablePresenceCard.test.tsx` | 4 | 0 | `BookablePresenceCard` | Card copy/state | Zero mocks. Note the `.test.tsx` suffix — the only two billing files that break the repo's `-tests.tsx` convention are this and `MarketplaceCard.test.tsx` |
| `__tests__/YearlyValueCalcModalV2-tests.tsx` | 30 | 4 | `YearlyValueCalcModalV2`, `initial render`, `step navigation`, `result calculation`, `legal copy gating (showUpdatedCalculatorCopy)`, `start over`, `form validation`, `decimal / fractional input handling`, `field metadata (defaultValues, prefix, suffix)`, `large results render with separators end-to-end` | The full calculator wizard incl. validation and the copy flag | Mocks analytics only. Overlaps `steps-tests.ts` (L1) on schema/metadata |
| `__tests__/ResultContentV2-tests.tsx` | 5 | 3 | `ResultContentV2`, `thousand-separator formatting (THOUSAND_SEPARATOR_REGEX)`, `.toFixed(0) rounding at the .5 boundary`, `edge-case results`, `copy variant does not affect the formatted value` | Result rendering + number formatting | **3 of 5 describes are pure formatting rules asserted through a DOM render** — belongs at L1 (gap L2-5) |
| `__tests__/EditMonthlyLimitModalV2-tests.tsx` | 13 | 2 | `Edit Monthly Limit Modal V2`, `monthly limit validation`, `handleSave behavior`, `remove monthly limit` | Monthly-limit edit, validation messages, save, removal | Mocks analytics + `apiCalls`. **The min-limit assertion at :129-133 re-evaluates the source's own `getFeatureFlagVariant(...) \|\| '500'` expression**, so it cannot catch a wrong default |
| `__tests__/EditRolloversModalV2-tests.tsx` | 13 | 3 | `Edit Rollovers Modal V2`, `error message uses Mezzanine ErrorMessage with icon (BILL-550)` | Rollover edit + error presentation | Mocks analytics + `apiCalls` |
| `__tests__/EditBillingEmailModal-tests.tsx` | 2 | 0 | `Edit Billing Email Modal`, `billing email validation` | Email field validation | Mocks analytics. Only 2 blocks for a field whose schema lives in the untested `schemaBuilder.ts` |
| `__tests__/EditBusinessAddressModal-tests.tsx` | 9 | 0 | `Edit Business Address Modal`, `address line 1 validation`, `address line 2 validation`, `city validation`, `zip code validation` | Address field validation, per field | Mocks analytics; the schema itself (`schemaBuilder.ts`) has no direct test — this suite is its only coverage |
| `__tests__/DeletePaymentMethodConfirmationModalV2-tests.tsx` | 5 | 0 | `DeletePaymentMethodConfirmationModalV2` | Delete confirmation copy + callbacks | Mocks modal context |
| `__tests__/CreditCardImage-tests.tsx` | 2 | 1 | `CreditCardImage` | Brand → image | Zero mocks |
| `__tests__/AddPaymentMethodModalV2-tests.tsx` | 5 | 0 | `AddPaymentMethodModalV2` | Settings-side wiring into the unified core modal: practiceId, `stripeKeys.liveKey`/`sandboxKey`, `paymentMethodToReplaceId`, `onAdded`, `onCancel` | **`jest.mock`s the core `AddPaymentMethodElementModal` (:30)** — a deliberate stub, documented in a comment at :26-28. No real Payment Element behaviour crosses this seam |
| `__tests__/CreditCardFormContentV2-tests.tsx` | 2 | 1 | `CreditCardFormContentV2 ZIP code field input restrictions` | ZIP input restrictions **only** — 2 blocks for a 452-line legacy card form | Mocks `@stripe/react-stripe-js`, `@zocdoc/provider-core`, `apiCalls`. Nothing on tokenization, `createSetupIntentV2`, or submit errors |
| `__tests__/AchFormContentV2-handleConnectBank-tests.tsx` | 5 | 0 | `AchFormContentV2 handleConnectBank` | The Financial Connections "connect bank" handler | Mocks `@stripe/react-stripe-js`, `@zocdoc/provider-core`, `apiCalls`. Field validation is split out to `AchFormContentV2-schema-tests.ts` (L1) — the correct pattern |
| `__tests__/billing-analytics-events-tests.tsx` | 11 | 1 | `Billing Settings — FE Analytics Events`, `Section 1: Pricing and Policy`, `MarketplaceCard — Calculate My Yearly New Patient Revenue`, `MarketplaceCard — View price by provider`, `FAQ click analytics events`, `Section 2: Payment Methods`, `Section 3: Invoice Summary Billing Page`, `Section 4: Bonus Metrics` | Analytics event names/payloads across the page | **Renders 5 different components in one file** (`FAQsSection`, `MarketplaceCard`, `PaymentMethodsListV2`, `BillingContactInfo`, `Bill`) inside a real `BillingSettingsContext` with real `initializeMetricsDataOnWindow`; only 2 `jest.mock`s. It is the only coverage `FAQsSection.tsx` has |
| `PaymentMethodsList/__tests__/PaymentMethodsListV2-tests.tsx` | 14 | 0 | `PaymentMethodsListV2` | Card list, default-card presentation, empty/error states | Mocks `useBillingToast`, modal context. **The V1 adapter `PaymentMethodsList.tsx` has no test at all** |
| `PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-tests.tsx` | 33 | 3 | `PaymentMethodV2`, `menu items visibility`, `API calls` | The single-card row: menu permissions, set-default, delete, replace, per-provider assignment | Mocks `apiCalls`, modal context. 847 lines — largest single-component suite |
| `PaymentMethodsList/components/v2/__tests__/PaymentMethodsPerProviderModal-tests.tsx` | 21 | 0 | `PaymentMethodsPerProviderModal`, `dropdown display value`, `search` | Per-provider card assignment, dropdown label, provider search | Mocks `apiCalls`, `useBillingToast` |
| `PaymentMethodsList/components/v2/__tests__/EditBillingContactInfoModal-tests.tsx` | 12 | 1 | `EditBillingContactInfoModal`, `form validation`, `save toast` | Contact edit form, validation, success toast | 7 `jest.mock`s incl. `apiCalls`, `useBillingToast`, dropdown, overlay, error-message |
| `PaymentRecovery/steps/__tests__/CardEntryStep-tests.tsx` | 7 | 3 | `CardEntryStep` | The recovery card-entry step incl. inline error handling | Mocks `@stripe/react-stripe-js` and `@stripe/stripe-js`. This is the **legacy split Card Elements** path — it has not migrated to Payment Element |
| `PaymentRecovery/steps/__tests__/ReviewStep-tests.tsx` | 12 | 2 | `ReviewStep` | The Pay Now review step: month groups, updated/blocked card states, inline error, submit state | **Zero `jest.mock`** — renders the real core `FailedPaymentsByMonth` → real `FailedPaymentMethodCard` → real `recoveryCopy`. Borderline L3 (see `integration-L3.md`) |

(32 rows above; `apps/settings` L2-component subtotal **32 files / 401 declared blocks** — verified mechanically.)

## L2 — shared/core (12 files, 110 blocks)

| Test file (under `shared/core/src/`) | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `components/AddPaymentMethodModal/__tests__/AddPaymentMethodElementModal-tests.tsx` | 14 | 0 | `AddPaymentMethodElementModal`, `AddPaymentMethodElementModal billing address` | The unified Payment Element modal: Stripe `Elements` wiring, submit, error surfacing, billing-address collection | 8 `jest.mock`s — `@stripe/react-stripe-js`, `billingApiClient`, `addPaymentMethod`, `getBillingStripePromise`, `getBillingAddress`, `updateBillingAddress`, `useConfirmPaymentSetup`, dropdown. Confirmation logic is asserted separately in `useConfirmPaymentSetup-tests.tsx` |
| `components/AddPaymentMethodModal/__tests__/AddPaymentMethodModal-tests.tsx` | 8 | 0 | `AddPaymentMethodModal` | The modal shell contract: title `Add a payment method`, `add-payment-method-modal`, submit/cancel test ids, error slot, the synchronous `isSubmittingRef` re-entrancy guard | **Zero mocks** — pure shell |
| `components/AddPaymentMethodModal/__tests__/BillingAddressFields-tests.tsx` | 5 | 0 | `BillingAddressFields` | Address inputs + state dropdown | Mocks dropdown only; uses the **real** `useBillingAddressForm` → borderline L3 |
| `components/AddPaymentMethodModal/__tests__/PaymentElementFields-tests.tsx` | 3 | 0 | `PaymentElementFields` | That the Stripe `PaymentElement` is mounted with the expected options | Mocks `@stripe/react-stripe-js` |
| `billing/__tests__/useConfirmPaymentSetup-tests.tsx` | 11 | 2 | `useConfirmPaymentSetup` | The deferred-intent sequence `elements.submit()` → `createSetupIntentWithCustomer` → `confirmSetup({redirect:'if_required'})`, `ProviderFacingError` surfacing, and the `confirmedPaymentMethodIdRef` cache that stops a retry minting a second payment method / Stripe Customer | Mocks `@stripe/react-stripe-js`, `../createSetupIntentWithCustomer`, `@zocdoc/logger`. Classified L2 (not L2H) because it renders a component wrapper, not a bare hook |
| `components/FailedPaymentMethodCard/__tests__/FailedPaymentMethodCard-tests.tsx` | 29 | 2 | `FailedPaymentMethodCard`, `when the card carries a rollover order` | Failed-card states: decline lines, provider tooltips/counts, updated state, rollover-blocked | **Zero mocks** — real copy helpers |
| `components/FailedPaymentsByMonth/__tests__/FailedPaymentsByMonth-tests.tsx` | 13 | 0 | `FailedPaymentsByMonth` | Month grouping, subtotals, updated-card propagation | **Zero mocks** — renders real `FailedPaymentMethodCard` and real `recoveryCopy` |
| `components/PaymentSetupBanner/__tests__/PaymentSetupBanner-tests.tsx` | 7 | 0 | `PaymentSetupBanner` | Setup-banner copy/CTA/dismiss | Zero mocks |
| `components/PaymentMethodLogo/__tests__/PaymentMethodLogo-tests.tsx` | 3 | 1 | `PaymentMethodLogo` | Brand → logo | Zero mocks |
| `components/RecoveryStatusBanner/__tests__/RecoveryStatusBanner-tests.tsx` | 9 | 1 | `RecoveryStatusBanner` | Banner variants, CTA, dismiss | Zero mocks; real `recoveryBannerCopy` |
| `components/RecoveryOutcomeBanner/__tests__/RecoveryOutcomeBanner-tests.tsx` | 6 | 2 | `RecoveryOutcomeBanner` | Outcome banner per `OutcomeVariant` | Zero mocks; real `recoveryOutcomeCopy` |
| `components/RecoveryProcessingBanner/__tests__/RecoveryProcessingBanner-tests.tsx` | 2 | 0 | `RecoveryProcessingBanner` | Processing banner renders + copy | 24 lines — the smallest suite in the scope |
| `components/PriceByProviderModal/` | — | — | — | — | **No test file exists** for `PriceByProviderModal.tsx` (109 lines, has `__stories__`). Its only coverage is indirect: it is a real child of `PricingInformationV2` and is opened by one block at `apps/settings/.../__tests__/PricingInformationV2-tests.tsx:215` (`opens PriceByProviderModal when "View price by provider" is clicked`). Nothing asserts its contents |

(12 test files above; `shared/core` L2-component subtotal **12 files / 110 declared blocks**. The final row documents an absent file, not a test.)

## L2 — other apps (1 file, 4 blocks)

| Test file | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `apps/provider-home-webapp/src/pages/homepage/reposition/components/__tests__/ActivationAddPaymentMethodModal-tests.tsx` | 4 | 0 | `ActivationAddPaymentMethodModal` | Homepage activation wiring into the core modal: practiceId, `stripeKeys`, `shouldCollectBillingAddress`, `onAdded`, `onCancel` | **`jest.mock`s the core `AddPaymentMethodElementModal` (:31)** with a comment at :26-29 explaining core owns the behaviour. Also mocks modal context and `MarketplaceActivationSuccessModal`. Does not reference the `'billing_inline_activation_payment_modal'` experiment that gates the flow |

## L2H — hook render (9 files, 47 blocks)

| Test file | Blocks | `it.each` | `describe` names | Mocked boundary | Covers | Deliberately does not |
|---|---|---|---|---|---|---|
| `apps/settings/.../hooks/__tests__/useBillingToast-tests.ts` | 10 | 1 | `useBillingToast`, `top-layer promotion`, `auto-dismiss` | `@zocdoc-mezzanine/components-toast` | Toast queueing, top-layer promotion, auto-dismiss timing | Real toast rendering |
| `apps/settings/.../hooks/__tests__/usePracticeBillingSettings-tests.ts` | 4 | 0 | `usePracticeBillingSettings` | `apiCalls` | Load / error / loading states for the page's primary read | Real HTTP |
| `apps/settings/.../hooks/__tests__/useRecoverySummary-tests.ts` | 9 | 1 | `useRecoverySummary` | `apiCalls` | Recovery summary fetch, refresh, error, empty | Real HTTP; mapping is L1-tested in `mapRecoveryToSummary-tests.ts` |
| `apps/settings/.../hooks/__tests__/usePrewarmBillingStripe-tests.ts` | 3 | 0 | `usePrewarmBillingStripe` | `getBillingStripePromise`, `config/environment` | That Stripe.js load starts on mount and is not re-triggered | Real `loadStripe` |
| `apps/settings/.../__tests__/usePaymentRecoveryFlow-tests.ts` | 5 | 0 | `usePaymentRecoveryFlow` | **none** | The recovery flow state machine transitions | Nothing mocked — closest L2H file to L1 |
| `apps/settings/.../PaymentRecovery/__tests__/useRecoveryBalanceDetail-tests.ts` | 3 | 0 | `useRecoveryBalanceDetail` | `apiCalls` | Balance-detail fetch states | Real HTTP; only 3 blocks for the itemized-money read |
| `shared/core/src/billing/__tests__/useBillingAddressPrefill-tests.ts` | 4 | 0 | `useBillingAddressPrefill` | `../getBillingAddress` | Prefill population and the no-address path | Uses the **real** `useBillingAddressForm` → borderline L3 |
| `apps/provider-home-webapp/.../hooks/__tests__/useRecoveryStatusSummary.test.ts` | 7 | 1 | `useRecoveryStatusSummary`, `suppression` | `ab/useExperiments`, `apis/recoveryApi` | Homepage recovery summary + the `billing_payment_recovery_experience` gate + suppression | Real HTTP; uses the **real** core suppression helpers over jsdom `localStorage` |
| `apps/spo-webapp/src/hooks/__tests__/useIsClosedBillingPeriod-tests.ts` | 2 | 1 | `useIsClosedBillingPeriod` | `hooks/useSpoDateRange` | Closed-period predicate | Only 2 declared blocks (1 is `it.each`) |

## Candidate Gaps

| # | What's missing | Level | Path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| L2-1 | `CreditCardFormContentV2.tsx` (452 lines) has **2 declared blocks**, both about ZIP input restrictions. Nothing covers tokenization, `createSetupIntentV2`, submit failure, or duplicate-submit | L2 | `apps/settings/.../__tests__/CreditCardFormContentV2-tests.tsx`, `AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:18,120` | This is the live card form for the Pay Now recovery flow — a failure here means a practice cannot fix a declined card | M | **P0** |
| L2-2 | `PaymentMethodsList.tsx` (V1 adapter) has no test, and its only logic mutates the props array in place (`props.paymentMethods.filter(p => p.isDefault)[0].isDefault = false`) | L2 | `apps/settings/.../PaymentMethodsList/PaymentMethodsList.tsx` | Prop mutation on the default-card swap; the V2 suite (14 blocks) does not exercise the adapter | S | **P1** |
| L2-3 | The `shared/core` → app Payment Element seam has no test at any non-E2E level: both consumers stub the core modal | L2/L3 | `AddPaymentMethodModalV2-tests.tsx:30`, `ActivationAddPaymentMethodModal-tests.tsx:31`, `shared/core/src/testing/installStripeJsFake.ts` | A prop-contract break across the package boundary is caught only at L5. `installStripeJsFake.ts` already exists for exactly this and is unused below L5 | M | **P1** |
| L2-4 | `useRecoveryBalanceDetail-tests.ts` has 3 blocks and `useIsClosedBillingPeriod-tests.ts` has 2, for hooks that decide what a practice is shown they owe | L2H | `apps/settings/.../PaymentRecovery/useRecoveryBalanceDetail.ts`, `apps/spo-webapp/src/hooks/useIsClosedBillingPeriod.ts` | Thin coverage on money-visible state | S | P2 |
| L2-5 | Pure number-formatting rules asserted through a DOM render | L1 | `__tests__/ResultContentV2-tests.tsx` (`thousand-separator formatting (THOUSAND_SEPARATOR_REGEX)`, `.toFixed(0) rounding at the .5 boundary`) | Extract the formatter, test the rounding contract at L1; keeps it runnable without React | S | P2 |
| L2-6 | `FAQsSection.tsx` (283 lines) has **no dedicated suite** — its only coverage is `describe('FAQ click analytics events')` inside the cross-cutting analytics file. `PriceByProviderModal.tsx` (109 lines) has none either — one block at `PricingInformationV2-tests.tsx:215` opens it and asserts nothing about its contents | L2 | `apps/settings/.../v2/FAQsSection.tsx`, `shared/core/src/components/PriceByProviderModal/PriceByProviderModal.tsx`, `__tests__/billing-analytics-events-tests.tsx`, `__tests__/PricingInformationV2-tests.tsx:215` | FAQ content regressions surface as an analytics-test failure in a file no one owns; the price-by-provider breakdown (a money-facing table) has no content assertion at all | S | P2 |
| L2-7 | `FreeProductsCard.tsx` (186 lines) has no test at any level, dedicated or indirect | L2 | `apps/settings/.../v2/FreeProductsCard.tsx` | Renders what a practice is *not* charged for | S | P2 |
| L2-8 | `billing-analytics-events-tests.tsx` renders 5 unrelated components in one 475-line file | L2 | `apps/settings/.../__tests__/billing-analytics-events-tests.tsx` | Cannot be run as "the tests for X"; blocks selective CI and obscures ownership. Split per component, or keep it and add the missing dedicated suites (L2-6) | M | P3 |
| L2-9 | `PricingTab-tests.tsx` (2 blocks) is the only coverage of `PricingInformation.tsx` and asserts nothing about the fetch-then-render contract that V1 exists to provide | L2 | `apps/settings/.../__tests__/PricingTab-tests.tsx`, `PricingInformation.tsx` | 9 mocks, 2 assertions; the V1/V2 seam is effectively untested | S | P2 |
| L2-10 | Two files break the repo naming convention (`.test.tsx` instead of `-tests.tsx`) | — | `apps/settings/.../v2/BookablePresenceCard.test.tsx`, `v2/MarketplaceCard.test.tsx` (also `apps/provider-home-webapp/.../useRecoveryStatusSummary.test.ts`) | They also sit next to the source instead of under `__tests__/`; any glob-based tooling that assumes the convention silently skips them | XS | P3 |

## Level Summary

| Level | Files | Declared blocks | `it.each` declarations | `describe` blocks |
|---|---|---|---|---|
| L1 unit | 34 | 224 | 49 | 73 |
| **L2 component render (this file)** | **45** | **515** | **43** | **112** |
| **L2H hook render (this file)** | **9** | **47** | **4** | **12** |
| **L2 total** | **54** | **562** | **47** | **124** |
| L3 integration | 2 | 70 | 6 | 15 |
| L4 api | 0 | 0 | 0 | 0 |
| Total non-E2E billing | **90** | **856** | **102** | **212** |

L2-component render by area: `apps/settings` **32 files / 401 blocks**; `shared/core` **12 / 110**;
`apps/provider-home-webapp` **1 / 4**. Sum **45 / 515** — matches the mechanical total.
L2H by area: `apps/settings` 6 / 34; `shared/core` 1 / 4; `apps/provider-home-webapp` 1 / 7; `apps/spo-webapp` 1 / 2.
Sum **9 / 47**.
