# provider-fe-monorepo — L1 (unit) Billing Tests

**Analyzed revision:** `provider-fe-monorepo` @ `origin/main` `dd9e4952a6` (2026-09-03)
**Snapshot:** `/tmp/slv3/snapshots/provider-fe-monorepo/` — 2647 files, **no `package.json` and no `node_modules`**,
so Jest could not be executed. Every number below is a static count from the source text.

## Counting convention (applies to all v3 files in this directory)

Jest cannot be run against this snapshot, so **runtime case counts are not verifiable**. I report
**declared blocks** = lines matching `^\s*(it|test)[.(]`. An `it.each([...])(...)` counts as **one** declared
block even though it expands to N runtime cases at run time, so the real executed-case count is strictly higher
than every number here. The `it.each` column makes that gap visible. Where a total matters I label it
"declared blocks", never "tests".

## L1/L2 boundary decision (read this before comparing counts with v2)

CONVENTIONS.md L1 says "No React render". Nine billing test files drive a hook with `renderHook`, which *does*
mount a React host component through the reconciler and `act()`. I classified those as **L2 (hook render)**, tagged
`L2H`, and they live in `component-L2.md`. This is the single judgement call that moves counts:

| If `renderHook` counts as… | L1 files | L1 declared blocks | L2 files | L2 declared blocks |
|---|---|---|---|---|
| **L2 (what I did)** | **34** | **224** | **54** | **562** |
| L1 (the alternative) | 43 | 271 | 45 | 515 |

Nothing else in the billing scope is borderline on this axis.

## L1 test files (34 files, 224 declared blocks)

### apps/settings — billing page logic

| Test file | Blocks | of which `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `__tests__/apiCalls-tests.ts` | 29 | 0 | `apiCalls`, `fetchPracticeBillingSettings`, `fetchRecovery`, `fetchRecoveryBalanceDetail`, `fetchInvoiceDetails`, `setDefaultPaymentMethod`, `deletePaymentMethod`, `updatePracticeBillingEmail`, `updatePrimaryBusinessAddress`, `setDefaultPaymentMethodForProvider`, `addPaymentMethodV3`, `savePaymentMethodAttributes` | Request shape (resolved URL, method, body), success mapping and error mapping for 11 of the 14 client functions | Real HTTP: mocks `@zocdoc/provider-core/lib/utils/fetchHelperV2`, `@zocdoc/billing-monolith-api-client` and `@zocdoc/logger`. **No `describe` for `createSetupIntentV2` (apiCalls.ts:323) or `prepareSetupIntentV2` (:402)** |
| `__tests__/triggerPayNow-tests.ts` | 2 | 0 | `triggerPayNow` | The pay-now POST via `executeRequestIncludeCredentials` | Mocks `fetchHelperV2`; only 2 blocks for a money-moving call |
| `__tests__/bookingSourceBreakdown-tests.ts` | 4 | 2 | `normalizeBookingSourceBreakdown` | Row normalization + aggregation for invoice booking sources | No render |
| `__tests__/buildPaymentMethodsAfterReplace-tests.ts` | 4 | 1 | `buildPaymentMethodsAfterReplace` | Rebuilding the card array after a recovery replace | The in-place-mutation sibling in `PaymentMethodsList.tsx` (see `source-components.md` SC-4) |
| `__tests__/getAdjustedFreeBookingCount-tests.ts` | 2 | 1 | `getAdjustedFreeBookingCount` | Free-booking adjustment arithmetic | — |
| `__tests__/resolvePaymentOutcome-tests.ts` | 3 | 0 | `makeMockResolvePaymentOutcome`, `resolvePaymentOutcome` | Charge result → resolved outcome, plus the fixture factory itself | Mocks `pages/settingsPages/billingSettings/apiCalls` |
| `__tests__/SkuTitleMap-tests.ts` | 2 | 0 | `Sku Title Map tests` | `getFullTitleFor` display titles | — |
| `__tests__/steps-tests.ts` | 15 | 9 | `YearlyValueCalcModal steps`, `validationSchema — common rules`, `validationSchema — showUps range (1-10)`, `validationSchema — patientReturns range (1-100)`, `step descriptions`, `step field metadata (defaultValue, prefix, suffix)` | The calculator's yup schema ranges and per-step metadata | Rendering — that is `YearlyValueCalcModalV2-tests.tsx` (L2) |
| `__tests__/AchFormContentV2-schema-tests.ts` | 7 | 4 | `AchFormContentV2 schema`, `account holder name`, `email` | `achV2Schema` field validation in isolation | The form itself and Stripe Financial Connections — split into `AchFormContentV2-handleConnectBank-tests.tsx` (L2) |
| `PaymentRecovery/__tests__/buildUpdatedCardIdentity-tests.ts` | 4 | 1 | `buildUpdatedCardIdentity` | Identity record for a replaced card | — |
| `utils/__tests__/billingDateUtils-tests.ts` | 8 | 2 | `formatInvoiceDate`, `getLegacyInvoiceTitle`, `getYearFromInvoiceName`, `isFutureInvoice`, `isStrictlyFutureInvoice` | All 5 exported date helpers | `invoiceHelpers.ts`, the *other* invoice date module, which has no test at all |
| `utils/__tests__/getStripePromise-tests.ts` | 2 | 0 | `getStripePromise` | Live vs sandbox key selection | Mocks `@stripe/stripe-js/pure` and `config/environment`; no memoization assertion |
| `utils/__tests__/shouldUseStripeSandbox-tests.ts` | 1 | 1 | `shouldUseStripeSandbox` | `window.ZdBootstrapPracticeDetails?.is_test_practice` fallback | — |

### shared/core/src/billing

| Test file | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `__tests__/addPaymentMethod-tests.ts` | 7 | 1 | `addPaymentMethod` | Success path, `SAVE_FAILED_MESSAGE` on failure, logging | Mocks `../billingApiClient` and `@zocdoc/logger` |
| `__tests__/createSetupIntentWithCustomer-tests.ts` | 4 | 1 | `createSetupIntentWithCustomer` | 200 mapping, 400 → `errorMessage`, other non-200 → throw | Mocks `../billingApiClient`, `@zocdoc/logger` |
| `__tests__/billingAddressSchema-tests.ts` | 5 | 3 | `billingAddressSchema` | Address yup field rules | The read path (`getBillingAddress.ts`) that its own JSDoc says returns unvalidated values |
| `__tests__/usStateOptions-tests.ts` | 3 | 0 | `US_STATE_OPTIONS` | Option list / code list integrity | — |
| `__tests__/getBillingStripePromise-tests.ts` | 6 | 0 | `getBillingStripePromise` | Memoization keyed on publishable key, sandbox switch, missing-key → logs + resolves `null` | Mocks `@stripe/stripe-js/pure`, `../shouldUseStripeSandbox`, `@zocdoc/logger` |
| `__tests__/shouldUseStripeSandbox-tests.ts` | 3 | 1 | `shouldUseStripeSandbox` | Same 2-line predicate as the `apps/settings` copy | — (this is the duplicate; see Cross-Cutting #5) |

### shared/core/src/paymentRecovery + paymentMethodArtwork

| Test file | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `__tests__/recoveryBannerSuppression-tests.ts` | 20 | 6 | `recoveryBannerSuppression`, `buildSuppressionKey`, `suppressRecoveryBanner + evaluateRecoverySuppression`, `cross-surface key normalization`, `falsy practiceId on write`, `server-flag rule` | The 36h TTL (`SUPPRESSION_TTL_MS`), key building/normalization across surfaces, falsy-practiceId write guard, server-flag precedence | Nothing significant — the deepest L1 suite in the scope (444 lines) |
| `__tests__/mapRecoveryToSummary-tests.ts` | 8 | 2 | `mapRecoveryToSummary`, `providerName` | API payload → `RecoveryStatusSummary`, provider-name derivation | — |
| `__tests__/mapRecoveryBalanceDetail-tests.ts` | 5 | 0 | `mapRecoveryBalanceDetail` | Balance-detail payload → month groups + subtotals | — |
| `__tests__/deriveOutcome-tests.ts` | 1 | 1 | `deriveOutcome` | Charge result → `OutcomeVariant` — a single `it.each` table is the whole suite | — |
| `__tests__/selectRecoveryVariant-tests.ts` | 4 | 0 | `selectRecoveryVariant` | Banner variant selection | — |
| `__tests__/recoveryCopy-tests.ts` | 11 | 2 | `formatBalance`, `getRecoveryCopy`, `getRecoveryCopy (homepage surface)`, `formatShortMonth` | Money/month formatting and per-surface copy | `formatLongMonth` has no `describe` |
| `__tests__/recoveryBannerCopy-tests.ts` | 6 | 1 | `getRecoveryBannerCopy` | Banner copy per state | — |
| `__tests__/recoveryOutcomeCopy-tests.ts` | 11 | 2 | `getRecoveryOutcomeCopy` | Outcome copy + actions per outcome kind | — |
| `__tests__/failedPaymentMethodCopy-tests.ts` | 11 | 4 | `getProviderCount`, `getProviderTooltipText`, `getProviderTooltipLabel`, `getFailedMethodHeading`, `getDeclineLine` | All copy helpers for the failed-card component | `ROLLOVER_BLOCKED_LINE` has no `describe` (it is asserted in the L2 card suite instead) |
| `__tests__/mockRecovery-tests.ts` | 8 | 0 | `describe.each(SCENARIOS)('mock recovery scenario %i', …)`, `mock recovery scenario 0` | That every dev mock scenario produces a self-consistent payload | It tests fixtures, not product code — see gap L1-6 |
| `paymentMethodArtwork/__tests__/getPaymentMethodArtwork-tests.ts` | 1 | 1 | `getPaymentMethodArtwork` | Brand → artwork mapping, one `it.each` | — |

### apps/provider-home-webapp and apps/spo-webapp

| Test file | Blocks | `it.each` | `describe` names | Covers | Deliberately does not |
|---|---|---|---|---|---|
| `provider-home-webapp/src/apis/__tests__/recoveryApi-tests.ts` | 3 | 1 | `fetchRecovery` | Homepage recovery read + failure handling | Mocks `@zocdoc/billing-monolith-api-client` |
| `provider-home-webapp/src/services/__tests__/skuService-test.ts` | 16 | 0 | `skuService tests`, `updateSkus`, `updateSkus for practices with ClaimYourProfile` | SKU add/remove request building incl. the ClaimYourProfile branch | Mocks `pages/homepage/controller` |
| `provider-home-webapp/src/utils/__tests__/skuValidator-tests.ts` | 6 | 0 | `skuValidator tests` | `SkuValidator` rules | — |
| `spo-webapp/src/pages/EnrollV2Page/utils/__tests__/buildPaymentMessage-tests.ts` | 2 | 2 | `buildPaymentMessage` | Enrollment payment message copy (both blocks are `it.each`) | Mocks `@zocdoc/logger` |

## Cross-Cutting Findings

### 1. Exact totals (billing scope, this snapshot)

| Level | Files | Declared `it`/`test` blocks | of which `it.each` declarations |
|---|---|---|---|
| L1 unit | 34 | 224 | 49 |
| L2 component (component render) | 45 | 515 | 43 |
| L2H component (`renderHook`) | 9 | 47 | 4 |
| **L2 total** | **54** | **562** | **47** |
| L3 integration | 2 | 70 | 6 |
| L4 api | **0** | 0 | 0 |
| L5 e2e | out of scope (another agent) — note the snapshot does contain `apps/settings/e2e/**` | — | — |
| **Total non-E2E** | **90** | **856** | **102** |

Source side: **152** billing source files, **88** with a dedicated test file, **64** with none.
Test-to-source file ratio 90:152. Ratio of L1 to L2 declared blocks: **224 : 562 ≈ 1 : 2.5** — the pyramid is
inverted at the component layer, and there is effectively no integration layer.

### 2. Feature flags referenced in billing code

Only 4 non-test billing source files read a flag at all (`grep -rn "useExperiments(|useEntityFlag|getFeatureFlagVariant"`).

| Flag / experiment | Where read | Underlying key | Tested? | Dead? |
|---|---|---|---|---|
| `PAYMENT_RECOVERY_EXPERIENCE` | `BillingSettingsContainer.tsx:91,111` (via `BILLING_SETTINGS_TOP_LEVEL_EXPERIMENTS`) | `'billing_payment_recovery_experience'` (`apps/provider-home-webapp/src/ab/experiments.ts:160`, `providerHomeAbExperimentIdsType.ts:20`) | Yes — `BillingSettingsContainer-tests.tsx:652` (`hides the banner entirely when billing_payment_recovery_experience is off…`) and `useRecoveryStatusSummary.test.ts` | Live |
| `REVIEW_AND_PAY_CTA` | `BillingSettingsContainer.tsx:91,111–135` | `billing_review_and_pay_cta` (name appears only in the test at `BillingSettingsContainer-tests.tsx:599,633`) | Yes — `describe('Review and pay CTA gate reads billing_review_and_pay_cta independently (BILL-971)')` | Live |
| `PAY_NOW_ENABLED` | `BillingSettingsContainer.tsx` (3 references) | UNVERIFIED — the settings `ab/experiments` module is not in the snapshot | Yes — `describe('Pay Now modal gating (BILL-971)')` | Live |
| `BILLING_PROVIDER_REPOSITIONING` | `BillingSettingsContainer.tsx:88`, `PricingInformationV2.tsx:143` | `'billing_provider_repositioning'` (asserted at `PricingInformationV2-tests.tsx:164,453`) | Yes — `describe('Provider Repositioning gating (feature flag AND entity flag)')` | Live |
| `BILLING_UPDATED_CALCULATOR_COPY` | `PricingInformationV2.tsx:143` | `'billing_updated_calculator_copy'` (`PricingInformationV2-tests.tsx:539`) | Yes — `describe('Updated calculator copy gating (billing_updated_calculator_copy)')` + `YearlyValueCalcModalV2-tests.tsx` `describe('legal copy gating (showUpdatedCalculatorCopy)')` | Live |
| `ENABLE_BILLING_CSV_DOWNLOAD` | `BillingSettingsContainer.tsx` (3 references) | UNVERIFIED — constant not in snapshot | Yes, indirectly — `FpbInvoiceView-tests.tsx` `describe('Bookings CSV download (BILL-1135)')`; the container's threading is asserted in `BillingSettingsContainer-tests.tsx` | Live |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | `BillingSettingsContainer.tsx` (3 references) | UNVERIFIED — constant not in snapshot | Yes — `describe('bootstrap decouple experiment')` | **Looks stale.** It is an iframe-deprecation kill switch; the tests treat the decoupled path as the default and `PricingInformationV2-tests.tsx` has `describe('with providers prop (decoupled from bootstrap)')`. Candidate for removal, but I cannot see the ramp state from the code — UNVERIFIED as dead |
| `useEntityFlag(entityFlags.isCreatedViaRepositionFlow)` | `BillingSettingsContainer.tsx:335`, `PricingInformationV2.tsx:159` | entity flag, not AB | Yes — both gate tests mock `useEntityFlag` and assert flag AND entity-flag together | Live |
| `Billing.MinimumPaymentMethodLimit` | `utils/schemaBuilder.ts:6,99` (`getFeatureFlagVariant(...) \|\| '500'`); typed at `shared/core/src/types/featureFlags.ts:86` | `'Billing.MinimumPaymentMethodLimit'` | **Effectively no.** `EditMonthlyLimitModalV2-tests.tsx:129-133` calls the **real, unmocked** `getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') \|\| '500'` and then asserts the message built from that same expression — a tautology that cannot catch a wrong default or a variant-parse bug | Live |
| `'billing_inline_activation_payment_modal'` | `apps/provider-home-webapp/src/ab/experiments.ts:179`, read by `pages/homepage/useActivateMarketplace.tsx:35`; mocked in `server/mocks/abExperimentMockData.ts:68` | own key | **Not in the billing scope's tests.** `ActivationAddPaymentMethodModal-tests.tsx` does not reference it | Live |
| localStorage `'has_seen_billing_completion_modal'` | `BillingSettingsContainer.tsx:84` | not a flag, a suppression key | Yes — `BillingSettingsContainer-tests.tsx:425` clears it; `describe('billing completion modal vs toast (BILL-894)')` | Live |

### 3. `invoiceHelpers.ts` and `utils/schemaBuilder.ts` — both previous P0/P1 gaps are still OPEN

- **`invoiceHelpers.ts`** (47 lines; `formatDate` :1, `getLastDayOfMonth` :24, `capitalizeStatus` :37) — still has
  **no direct test**. Evidence: no file named `invoiceHelpers*` exists under any `__tests__/`, and no test file in
  the 90-file set imports it. Its only importers are product code: `InvoiceDetailsContainer.tsx:21` and
  `v2/FpbInvoiceView.tsx:22`. Note the confusing near-duplicate: `utils/billingDateUtils.ts` *is* fully tested at L1
  (`billingDateUtils-tests.ts`, 8 blocks / 5 describes), which makes this gap easy to mistake for closed.
- **`utils/schemaBuilder.ts`** (130 lines; 5 exported schemas at :16, :28, :49, :71, :102) — still has **no direct
  test**. No test file imports it. Its 5 importers are all modals: `EditMonthlyLimitModalV2.tsx:8`,
  `EditBillingEmailModal.tsx:12`, `EditBusinessAddressModal.tsx:12`, `CreditCardFormContentV2.tsx:17`,
  `PaymentMethodsList/components/v2/EditBillingContactInfoModal.tsx:11`. The money boundaries live here
  (`maximumMonthlyLimit = 500000` at :101, minimum from the flag at :99) and are exercised only by whatever values
  the modal L2 suites happen to type — and the minimum-limit assertion is the tautology described in #2.

### 4. `LegacyInvoiceView` — still present, and NOT dead

`LegacyInvoiceView.tsx` (346 lines) and `__tests__/LegacyInvoiceView-tests.tsx` (12 blocks, 190 lines) both still
exist. The previous analysis's "delete them" recommendation is **wrong at this revision**: it is imported at
`InvoiceDetailsContainer.tsx:16` and rendered at `InvoiceDetailsContainer.tsx:201`, so it is live code on the
non-FPB invoice path. Its 12-block suite should stay.

### 5. V1-vs-V2 duplicates still both present

| Pair | Status | Test split |
|---|---|---|
| `PaymentMethodsList.tsx` (58) → `PaymentMethodsListV2.tsx` (203) | Both live; V1 is a thin adapter imported by `BillingSettingsContainer.tsx:26` | **Asymmetric.** V2: `PaymentMethodsListV2-tests.tsx` (14 blocks). V1: **no test**. The V1-only logic is the default-card swap that mutates the props array in place: `props.paymentMethods.filter(p => p.isDefault)[0].isDefault = false` |
| `PricingInformation.tsx` (65) → `v2/PricingInformationV2.tsx` (350) | Both live; V1 fetches `getProvidersDetails` then renders V2, imported at `BillingSettingsContainer.tsx:27`, rendered :549 | **Asymmetric.** V2: `PricingInformationV2-tests.tsx` (40 blocks / 12 describes). V1: only `PricingTab-tests.tsx` (2 blocks) — and the file name matches neither component |
| `apps/settings/.../utils/shouldUseStripeSandbox.ts` vs `shared/core/src/billing/shouldUseStripeSandbox.ts` | **Byte-identical**, both live | Both tested separately — `utils/__tests__/shouldUseStripeSandbox-tests.ts` (1 block) and `shared/core/src/billing/__tests__/shouldUseStripeSandbox-tests.ts` (3 blocks). Duplicate code *and* duplicate tests |
| `apps/settings/.../utils/getStripePromise.ts` (30) vs `shared/core/src/billing/getBillingStripePromise.ts` (37) | Near-duplicates, both live. Settings version takes `shouldUseSandbox: boolean` and reads `config/environment`; core version takes `{liveKey, sandboxKey}`, calls `shouldUseStripeSandbox()` itself and logs on a missing key | Both tested separately (2 blocks vs 6 blocks). Only the core version asserts the missing-key path |
| Local `formatCurrency` ×2 vs the shared one | `FeaturedProviderSection.tsx:8` and `LicenseFeeSection.tsx:9` each define their own; `FpbInvoiceDetailsComponents/formatCurrency.ts` (6 lines) is used by `FpbInvoiceView`/`TaxesAndFeesSection`/`PatientBookingsSection`/`BookingSourceRows` | Three implementations of money formatting on one invoice, none with a direct L1 test |
| `AddPaymentMethodModalV2` (settings, legacy split Card Elements) vs `AddPaymentMethodModal` + `AddPaymentMethodElementModal` (core, unified Payment Element) | Both live — see #7 | Both tested at L2, but the settings suite mocks the core modal, so no test crosses the seam |

### 6. Test files that mix levels

| File | Mix | Why it matters |
|---|---|---|
| `__tests__/billing-analytics-events-tests.tsx` (11 blocks, 8 describes, 475 lines) | Single L2 file that renders **five different components** — `FAQsSection`, `MarketplaceCard`, `PaymentMethodsListV2`, `BillingContactInfo`, `Bill` — inside a real `BillingSettingsContext.Provider`, with real `initializeMetricsDataOnWindow`. Level is uniformly L2, but the *subject* is a cross-cutting concern, not a component | Cannot be run as "the tests for X"; an analytics regression in any of 5 components surfaces in one file that no one owns |
| `__tests__/ResultContentV2-tests.tsx` (5 blocks, 5 describes) | L2 by mechanism (`renderComponent`) but 3 of 5 describes are pure-function assertions in disguise: `thousand-separator formatting (THOUSAND_SEPARATOR_REGEX)`, `.toFixed(0) rounding at the .5 boundary`, `copy variant does not affect the formatted value` | Number-formatting rules are being verified through a DOM render; they belong in an L1 suite next to the formatter |
| `__tests__/BillingSettingsContainer-tests.tsx` (35 blocks, 11 describes, 1141 lines) | Classified **L3**, but `describe('rollover-blocked ids derived from the payment-method list (BILL-1017)')` and `describe('recovery banner suppression')` are pure derivation/predicate logic asserted through a full page render | Slowest possible way to test a pure derivation; also see `integration-L3.md` |
| `AchFormContentV2` | **Correctly** split across two files by level: `AchFormContentV2-schema-tests.ts` (L1) and `AchFormContentV2-handleConnectBank-tests.tsx` (L2). This is the pattern the rest of the scope should follow | — (positive example) |

No file mixes L1 and L2 *within itself*.

### 7. Stripe Payment Element migration — what the code shows

I do **not** have `docs/plans/2026-08-18-unified-payment-element-core-extraction-split.md` in the snapshot and make
no claims about it. Purely from the code:

**What moved to `shared/core`** — the unified Payment Element stack, with its own tests:
`shared/core/src/components/AddPaymentMethodModal/{index.tsx (128), AddPaymentMethodElementModal.tsx (142),
PaymentElementFields.tsx (23), BillingAddressFields.tsx (85), styles.ts}` plus
`shared/core/src/billing/{useConfirmPaymentSetup.ts (120), createSetupIntentWithCustomer.ts, addPaymentMethod.ts,
getBillingAddress.ts, updateBillingAddress.ts, billingAddressSchema.ts, useBillingAddressForm.ts,
useBillingAddressPrefill.ts, getBillingStripePromise.ts, paymentElementOptions.ts, billingApiClient.ts}`.
The deferred-intent flow lives in `useConfirmPaymentSetup.ts`: `elements.submit()` → `createSetupIntentWithCustomer`
→ `stripe.confirmSetup({ redirect: 'if_required' })`, with `confirmedPaymentMethodIdRef` caching so a retry cannot
mint a second payment method / Stripe Customer.

**What stayed in `apps/settings`** — the legacy split Card Elements stack, still live:
`AddPaymentMethodModalV2/{CreditCardFormContentV2.tsx (452), AchFormContentV2.tsx (339),
PaymentMethodTypeRadioGroup.tsx}`, `utils/getStripePromise.ts`, `utils/shouldUseStripeSandbox.ts`, and the
`createSetupIntentV2` / `prepareSetupIntentV2` / `addPaymentMethodV3` client functions in `apiCalls.ts`.

**The migration is partial, and the split runs along a flow boundary, not a code boundary:**

| Flow | Stack | Evidence |
|---|---|---|
| Add a payment method from billing settings | **New** (core Payment Element) | `AddPaymentMethodModalV2Content.tsx:6,43` renders core `AddPaymentMethodElementModal` |
| Add a payment method during homepage activation | **New** (core Payment Element) | `ActivationAddPaymentMethodModal.tsx:3,24` renders core `AddPaymentMethodElementModal` |
| **Pay Now / payment recovery card entry** | **Legacy split Card Elements** | `PaymentRecovery/steps/CardEntryStep.tsx:7-12` imports `getStripePromise`, `shouldUseStripeSandbox`, `CreditCardFormContentV2`, `AchFormContentV2`, `PaymentMethodTypeRadioGroup`; `CreditCardFormContentV2.tsx:18,120` uses `createSetupIntentV2`; `AchFormContentV2.tsx:26,27,93,183` uses `createSetupIntentV2` + `prepareSetupIntentV2`; `PayNowModal.tsx:23,199,260` uses `addPaymentMethodV3` |

**How coverage splits across the boundary — the seam is untested.** Core's own tests are solid
(`AddPaymentMethodElementModal-tests.tsx` 14 blocks, `AddPaymentMethodModal-tests.tsx` 8,
`useConfirmPaymentSetup-tests.tsx` 11, `PaymentElementFields-tests.tsx` 3, `BillingAddressFields-tests.tsx` 5).
But **both** consumer tests mock the core modal out —
`AddPaymentMethodModalV2-tests.tsx:30-32` and `ActivationAddPaymentMethodModal-tests.tsx:31-33` both
`jest.mock('@zocdoc/provider-core/lib/components/AddPaymentMethodModal/AddPaymentMethodElementModal')` — so they
assert prop wiring only. No non-E2E test renders a real Payment Element modal inside a real app consumer, which
means a prop-contract break across the `shared/core` → app boundary is caught only at L5.

Related: `shared/core/src/testing/installStripeJsFake.ts` (130 lines) is a Stripe.js fake built for exactly this
kind of test, and **no L1/L2/L3 test uses it**. Its only consumers in the snapshot are
`apps/settings/e2e/fixtures.ts` (L5) and
`apps/provider-home-webapp/src/pages/homepage/reposition/components/__stories__/ActivationAddPaymentMethodModal-stories.tsx`.
The tool to close the seam gap already exists and is unused below L5.

## Candidate Gaps

| # | What's missing | Level | Path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| L1-1 | No `describe` for `createSetupIntentV2` (`apiCalls.ts:323`) or `prepareSetupIntentV2` (:402) — 2 of 14 client functions, both on the money path, both still used by the Pay Now flow | L1 | `apps/settings/.../__tests__/apiCalls-tests.ts`, `apiCalls.ts:323,402` | Every other client function has a `describe`; these two build the setup-intent requests for card and ACH entry during recovery | S | **P0** |
| L1-2 | `utils/schemaBuilder.ts` has no direct test, and the one flag assertion that exists is tautological (`EditMonthlyLimitModalV2-tests.tsx:129-133` re-evaluates the source expression) | L1 | `apps/settings/.../utils/schemaBuilder.ts` | Monthly-limit min/max are the only client guard on a money field; a wrong default silently ships | S | **P0** |
| L1-3 | `invoiceHelpers.ts` has no direct test | L1 | `apps/settings/.../invoiceHelpers.ts` | `getLastDayOfMonth` drives customer-visible invoice period labels | XS | **P1** |
| L1-4 | `triggerPayNow` has only 2 declared blocks for a batch-charge POST | L1 | `apps/settings/.../__tests__/triggerPayNow-tests.ts`, `apiCalls.ts:426` | This is the call that actually charges a practice's failed balance; error/retry shapes are unasserted | S | **P1** |
| L1-5 | `formatLongMonth` (`recoveryCopy.ts`) and `ROLLOVER_BLOCKED_LINE` (`failedPaymentMethodCopy.ts`) have no `describe` while every sibling export does | L1 | `shared/core/src/paymentRecovery/recoveryCopy.ts`, `failedPaymentMethodCopy.ts` | Small, cheap, and inconsistent with an otherwise complete copy suite | XS | P3 |
| L1-6 | `mockRecovery-tests.ts` (8 blocks) tests dev fixtures, while the real mapper `mapRecoveryMethodDisplay.ts` next to it has no test at all | L1 | `shared/core/src/paymentRecovery/mockRecovery.ts`, `mapRecoveryMethodDisplay.ts` | Test effort is pointed at fixtures instead of product logic | XS | P2 |
| L1-7 | `installStripeJsFake.ts` is unused below L5, so the Payment Element seam has no in-process test | L2/L3 | `shared/core/src/testing/installStripeJsFake.ts`, `AddPaymentMethodModalV2-tests.tsx:30`, `ActivationAddPaymentMethodModal-tests.tsx:31` | A ready-made fake exists; using it in one consumer test would cover the `shared/core` → app prop contract that is currently E2E-only | M | **P1** |
| L1-8 | `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` looks like a fully-ramped kill switch still carrying test branches | L1 | `BillingSettingsContainer.tsx` (3 refs), `BillingSettingsContainer-tests.tsx` `describe('bootstrap decouple experiment')` | Dead-flag cleanup removes a whole gate + its test branches; needs a ramp-state check first (UNVERIFIED from code alone) | S | P3 |
| L1-9 | Number-formatting rules asserted through a DOM render instead of L1 | L1 | `apps/settings/.../__tests__/ResultContentV2-tests.tsx` (`describe('thousand-separator formatting (THOUSAND_SEPARATOR_REGEX)')`, `describe('.toFixed(0) rounding at the .5 boundary')`) | Extract the formatter and test it at L1; keeps the rounding contract runnable without React | S | P2 |

## Level Summary

| Level | Files | Declared blocks | `it.each` declarations |
|---|---|---|---|
| **L1 (this file)** | **34** | **224** | **49** |
| L2 component | 45 | 515 | 43 |
| L2H (`renderHook`) | 9 | 47 | 4 |
| L3 integration | 2 | 70 | 6 |
| L4 api | 0 | 0 | 0 |
| Total non-E2E billing | **90** | **856** | **102** |

L1 file breakdown by area: `apps/settings` 13 files / 83 blocks; `shared/core/src/billing` 6 / 28;
`shared/core/src/paymentRecovery` 10 / 85; `shared/core/src/paymentMethodArtwork` 1 / 1;
`apps/provider-home-webapp` 3 / 25; `apps/spo-webapp` 1 / 2.
