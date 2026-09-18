# provider-fe-monorepo — Billing SOURCE File Inventory

**Analyzed revision:** `provider-fe-monorepo` @ `origin/main` `dd9e4952a6` (2026-09-03)
**Snapshot analyzed:** `/tmp/slv3/snapshots/provider-fe-monorepo/` (2647 files — a filtered subset; it has no
`package.json` and no `node_modules`, so Jest could **not** be executed. Every count below is a static count.)
**Scope:** non-E2E (Unit/Component/Integration) billing coverage. Browser Playwright/Cypress is another agent's scope. Note for the
orchestrator: the snapshot *does* contain `apps/settings/e2e/**` (e.g.
`apps/settings/e2e/PracticeSettingsPages/billing-settings-page-commands.ts:135`), which is a browser test and is excluded here.

## Method / counting conventions

- **Source file set:** 152 files (enumerated in `/tmp/scope_src.txt`), covering every path in the requested scope.
- **"Dedicated test"** = a test file named after the module (`<name>-tests.ts[x]`, `<name>.test.tsx`, or, for a
  `index.tsx` component, `<ComponentDir>-tests.tsx`). Anything else is recorded as *indirect*.
- **Kinds of test** follow `methodology/CONVENTIONS.md`. `Hook` marks a component test driven by `renderHook`
  rather than a component render — see `unit-tests.md` § "Unit/component boundary decision" for why those are component tests and not unit tests.
- **Classification** values: `business-logic`, `presentational`, `container`, `hook`, `schema/util`, `type`, `mock`.
- Feature flags: only 4 non-test source files in the whole billing scope read a flag/experiment. Everything else
  is `—`, verified by `grep -rn "useEntityFlag|getFeatureFlagVariant|useExperiments("` over the scope.

## A. apps/settings — page shell, containers, top-level sections

| File (under `apps/settings/src/pages/settingsPages/billingSettings/`) | Lines | Purpose | Class | Flags | Dedicated test |
|---|---|---|---|---|---|
| `BillingSettingsContainer.tsx` | 878 | Billing page root: exports `BillingSettingsContainer`, `BillingSettingsAllContentContainer`, `RECOVERY_UPDATED_TOAST`; owns experiment gates, recovery banner placement, Pay Now wiring, completion modal/toast | container | `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION`, `PAYMENT_RECOVERY_EXPERIENCE`, `REVIEW_AND_PAY_CTA`, `PAY_NOW_ENABLED`, `BILLING_PROVIDER_REPOSITIONING`, `ENABLE_BILLING_CSV_DOWNLOAD` (:88, :91, :111–135); `useEntityFlag(entityFlags.isCreatedViaRepositionFlow)` (:335); localStorage key `has_seen_billing_completion_modal` (:84) | yes — `BillingSettingsContainer-tests.tsx` (**Integration**) |
| `BillsContainer.tsx` | 320 | Invoice list + selection; exports `BillsContainer` and `Bill` | container | — | yes — `BillsContainer-tests.tsx` (Component) |
| `InvoiceDetailsContainer.tsx` | 243 | Chooses `FpbInvoiceView` vs `LegacyInvoiceView` (:201), builds invoice PDF URLs | container | — | yes — `InvoiceDetailsContainer-tests.tsx` (Component) |
| `PricingInformation.tsx` | 65 | **V1 adapter**: fetches `getProvidersDetails({ providerIds })` then renders `PricingInformationV2`; still imported by `BillingSettingsContainer.tsx:27` (rendered :549) | container | — | name-mismatched — only `PricingTab-tests.tsx` (Component, 2 blocks) renders it |
| `BillingContactInfo.tsx` | 134 | Billing email / business address rows + edit entry points | presentational | — | yes — `BillingContactInfo-tests.tsx` (Component) |
| `BillingCompletionModal.tsx` | 99 | "Billing setup complete" modal, FullAdmin-gated | presentational | — | yes — `BillingCompletionModal-tests.tsx` (Component) |
| `BillStatusLabel.tsx` | 49 | Paid/unpaid/overdue label for an invoice row | presentational | — | **no** |
| `EditBillingEmailModal.tsx` | 120 | Edit billing email modal | presentational | — | yes — `EditBillingEmailModal-tests.tsx` (Component) |
| `EditBusinessAddressModal.tsx` | 192 | Edit primary business address modal | presentational | — | yes — `EditBusinessAddressModal-tests.tsx` (Component) |
| `EditMonthlyLimitModalV2.tsx` | 177 | Per-card monthly spend limit modal | presentational | reads `Billing.MinimumPaymentMethodLimit` transitively via `schemaBuilder` | yes — `EditMonthlyLimitModalV2-tests.tsx` (Component) |
| `EditRolloversModalV2.tsx` | 338 | Card rollover-order editor | presentational | — | yes — `EditRolloversModalV2-tests.tsx` (Component) |
| `DeletePaymentMethodConfirmationModalV2.tsx` | 91 | Delete-card confirmation modal | presentational | — | yes — `DeletePaymentMethodConfirmationModalV2-tests.tsx` (Component) |
| `LegacyInvoiceView.tsx` | 346 | Pre-FPB invoice renderer; **still live** (`InvoiceDetailsContainer.tsx:16,201`) | presentational | — | yes — `LegacyInvoiceView-tests.tsx` (Component, 12 blocks) |
| `apiCalls.ts` | 463 | All 14 billing client functions (REST + generated `billing-monolith-api-client`) | business-logic | — | yes — `apiCalls-tests.ts` (Unit) + `triggerPayNow-tests.ts` (Unit) |
| `bookingSourceBreakdown.ts` | 44 | `normalizeBookingSourceBreakdown` — invoice booking-source row normalization | business-logic | — | yes — `bookingSourceBreakdown-tests.ts` (Unit) |
| `buildPaymentMethodsAfterReplace.ts` | 19 | Rebuilds the payment-method array after a recovery card replace | business-logic | — | yes — `buildPaymentMethodsAfterReplace-tests.ts` (Unit) |
| `getAdjustedFreeBookingCount.ts` | 18 | Free-booking count adjustment for invoice display | business-logic | — | yes — `getAdjustedFreeBookingCount-tests.ts` (Unit) |
| `invoiceHelpers.ts` | 47 | `formatDate` (:1), `getLastDayOfMonth` (:24), `capitalizeStatus` (:37) | schema/util | — | **no** |
| `SkuTitleMap.ts` | 33 | `getFullTitleFor(sku)` display-title map | schema/util | — | yes — `SkuTitleMap-tests.ts` (Unit) |
| `context/BillingSettingsContext.ts` | 12 | React context carrying practice/user billing state | type | — | **no** (used as a real provider by many component tests) |
| `fixtures/bookingSourceBreakdownFixtures.ts` | 59 | `mockBookingSourceBreakdown` fixture | mock | — | **no** (fixture) |

## B. apps/settings — shared presentational primitives (`components/`)

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `components/ArrowRedirectionLink.tsx` | 59 | `ArrowRedirectLink` — link with trailing arrow | presentational | **no** |
| `components/BillingCoachmark.tsx` | 220 | `BillingPageCoachmark` + `BillPageCoachmarkState` type | presentational | **no** |
| `components/BillingToastStyleOverrides.ts` | 42 | styled overrides for billing toasts | presentational | **no** |
| `components/ButtonIfCanEdit.tsx` | 11 | Renders a button only when the user may edit | presentational | **no** |
| `components/CentralizedLoader.tsx` | 26 | Centered spinner wrapper | presentational | **no** |
| `components/CreditCardImage.tsx` | 22 | Card-brand image | presentational | yes — `CreditCardImage-tests.tsx` (Component) |
| `components/DropdownIfCanEdit.tsx` | 13 | Permission-gated dropdown | presentational | **no** |
| `components/ErrorMessage.tsx` | 9 | Styled inline error text | presentational | **no** |
| `components/FlexRowDiv.tsx` | 10 | `FlexRowDiv`, `CentreAlignedFlexRowDiv` | presentational | **no** |
| `components/LinkIfCanEdit.tsx` | 37 | `LinkIfCanEdit`, `DisabledLink` | presentational | **no** |
| `components/RowItemContainer.tsx` | 17 | Row layout wrapper | presentational | **no** |
| `components/SectionTitle.tsx` | 44 | `SectionTitle`, `SectionTitleWithSubtitle` | presentational | **no** |
| `components/StyledDiv.tsx` | 9 | Styled div | presentational | **no** |
| `components/TooltipText.tsx` | 10 | Styled tooltip text | presentational | **no** |
| `components/modal/ActionButtons.tsx` | 109 | Modal save/cancel button pair | presentational | **no** |
| `components/modal/InputWithTitle.tsx` | 124 | Labeled RHF input used by every billing modal | presentational | **no** |
| `components/modal/ModalWrapper.tsx` | 5 | Styled modal body wrapper | presentational | **no** |
| `components/modal/StateZipContainer.tsx` | 7 | State+ZIP row layout | presentational | **no** |
| `components/modal/StyledRHFDropdown.tsx` | 9 | Styled react-hook-form dropdown | presentational | **no** |
| `components/v2/BillingModalFooter.tsx` | 79 | `BillingModalFooter` used by Pay Now steps | presentational | **no** |

## C. apps/settings — invoice / FPB rendering

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `v2/FpbInvoiceView.tsx` | 857 | Full "fee per booking" invoice: totals, taxes/fees, sponsored results, PDF + bookings-CSV download | container | yes — `v2/__tests__/FpbInvoiceView-tests.tsx` (Component, 52 blocks — largest file) |
| `v2/TaxesAndFeesSection.tsx` | 192 | Taxes & fees invoice section | presentational | yes — `TaxesAndFeesSection-tests.tsx` (Component) |
| `FpbInvoiceDetailsComponents/PatientBookingsSection.tsx` | 217 | `PatientBookingsSection` + `FreeVsPaidBookingsSection` | presentational | yes — `PatientBookingsSection-tests.tsx` (Component) |
| `FpbInvoiceDetailsComponents/FeaturedProviderSection.tsx` | 143 | Sponsored/featured-provider invoice section; defines its **own local** `formatCurrency` at :8 | presentational | yes — `FeaturedProviderSection-tests.tsx` (Component) |
| `FpbInvoiceDetailsComponents/LicenseFeeSection.tsx` | 130 | License-fee invoice section; defines its **own local** `formatCurrency` at :9 | presentational | yes — `LicenseFeeSection-tests.tsx` (Component) |
| `FpbInvoiceDetailsComponents/BookingSourceRows.tsx` | 80 | Renders booking-source breakdown rows | presentational | **no** |
| `FpbInvoiceDetailsComponents/formatCurrency.ts` | 6 | Shared cents→USD formatter | schema/util | **no** |
| `FpbInvoiceDetailsComponents/grid.tsx` | 155 | `Grid` layout primitives for the invoice | presentational | **no** |
| `FpbInvoiceDetailsComponents/FpbInvoiceView.types.ts` | 67 | `FpbInvoiceViewProps`, booking-source view models | type | **no** |
| `utils/billingDateUtils.ts` | 69 | `formatInvoiceDate`, `isFutureInvoice`, `isStrictlyFutureInvoice`, `getYearFromInvoiceName`, `getLegacyInvoiceTitle` | schema/util | yes — `billingDateUtils-tests.ts` (Unit) |

## C2. apps/settings — pricing tab (`v2/`)

| File | Lines | Purpose | Class | Flags | Dedicated test |
|---|---|---|---|---|---|
| `v2/PricingInformationV2.tsx` | 350 | Pricing tab body: marketplace enrolment states, bookable-presence card, FAQs, contact footer, calculator entry | container | `useExperiments([...])` (:143) incl. `BILLING_PROVIDER_REPOSITIONING` + `BILLING_UPDATED_CALCULATOR_COPY`; `useEntityFlag(entityFlags.isCreatedViaRepositionFlow, practiceId)` (:159) | yes — `PricingInformationV2-tests.tsx` (Component, 40 blocks) |
| `v2/MarketplaceCard.tsx` | 310 | Marketplace pricing card incl. "Calculate my yearly new patient revenue" and "View price by provider" | presentational | receives `isProviderRepositioning` as a prop | yes — `v2/MarketplaceCard.test.tsx` (Component, 10 blocks) |
| `v2/BookablePresenceCard.tsx` | 54 | Bookable-presence pricing card | presentational | — | yes — `v2/BookablePresenceCard.test.tsx` (Component, 4 blocks, uses raw `render`) |
| `v2/FAQsSection.tsx` | 283 | Pricing-tab FAQ accordion + click analytics | presentational | — | **no** |
| `v2/FreeProductsCard.tsx` | 186 | Free-products pricing card | presentational | — | **no** |

## D. apps/settings — payment methods list

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `PaymentMethodsList/PaymentMethodsList.tsx` | 58 | **V1 adapter** still imported by `BillingSettingsContainer.tsx:26`; builds `onAddPaymentMethod`/`onSetDefaultPaymentMethod`/`onDeletePaymentMethod` then renders `PaymentMethodsListV2`. `onSetDefaultPaymentMethod` mutates the props array in place (`props.paymentMethods.filter(p => p.isDefault)[0].isDefault = false`) | container | **no** |
| `PaymentMethodsList/PaymentMethodsListV2.tsx` | 203 | Card list + add/edit entry points | presentational | yes — `PaymentMethodsListV2-tests.tsx` (Component) |
| `PaymentMethodsList/components/v2/PaymentMethodV2.tsx` | 354 | One card row: menu, set-default, delete, limits, rollover tag | container | yes — `PaymentMethodV2-tests.tsx` (Component, 33 blocks) |
| `PaymentMethodsList/components/v2/EditBillingContactInfoModal.tsx` | 294 | Per-card billing contact modal | presentational | yes — `EditBillingContactInfoModal-tests.tsx` (Component) |
| `PaymentMethodsList/components/v2/PaymentMethodsPerProviderModal.tsx` | 373 | Assign payment methods per provider (search + dropdown) | presentational | yes — `PaymentMethodsPerProviderModal-tests.tsx` (Component) |

## E. apps/settings — payment recovery / Pay Now

| File (under `.../billingSettings/PaymentRecovery/`) | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `PayNowModal.tsx` | 352 | Pay-Now step machine: itemized balance → card entry → review → charge; uses `addPaymentMethodV3` (:23, :199, :260) | container | yes — `PayNowModal-tests.tsx` (**Integration**, 35 blocks) |
| `steps/CardEntryStep.tsx` | 194 | Card/ACH entry inside Pay Now; imports **legacy split Card Elements** path (`getStripePromise` :7, `shouldUseStripeSandbox` :8, `CreditCardFormContentV2` :9, `AchFormContentV2` :10, `PaymentMethodTypeRadioGroup` :12) | container | yes — `CardEntryStep-tests.tsx` (Component) |
| `steps/ReviewStep.tsx` | 83 | Review screen; composes core `FailedPaymentsByMonth` | presentational | yes — `ReviewStep-tests.tsx` (Component, zero `jest.mock` — renders real core collaborators) |
| `steps/BalanceLoadFallback.tsx` | 79 | Loading/error fallback for the itemized balance read | presentational | **no** |
| `usePaymentRecoveryFlow.ts` | 80 | Recovery flow phase machine (`RecoveryFlowPhase`) | hook | yes — `usePaymentRecoveryFlow-tests.ts` (Hook) |
| `useRecoveryBalanceDetail.ts` | 45 | Fetches + retries the itemized recovery balance | hook | yes — `useRecoveryBalanceDetail-tests.ts` (Hook) |
| `resolvePaymentOutcome.ts` | 51 | Maps a charge result to a resolved outcome | business-logic | yes — `resolvePaymentOutcome-tests.ts` (Unit) |
| `buildUpdatedCardIdentity.ts` | 16 | Builds the identity record for a replaced card | business-logic | yes — `buildUpdatedCardIdentity-tests.ts` (Unit) |
| `payNowScenarios.ts` | 118 | URL-driven dev scenarios: `getPayNowScenarioFromUrl`, `getPayNowScenarioHasMultiple` | mock | **no** |
| `copy.ts` | 2 | `RECOVERY_PAY_BALANCE_SUBTITLE` | schema/util | **no** |
| `types.ts` | 40 | `ChargeResult`, `ResolvedOutcome`, `ResolvePaymentOutcome` | type | **no** |
| `__fixtures__/payNowFixtures.ts` | 114 | Shared Pay-Now fixtures (`sampleFailedMethods`, `sampleMonthGroups`, `makeMockResolvePaymentOutcome`, …) | mock | **no** (fixture) |

## F. apps/settings — Yearly Value Calculator

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `YearlyValueCalcModal/YearlyValueCalcModalV2.tsx` | 200 | Multi-step revenue calculator modal | container | yes — `YearlyValueCalcModalV2-tests.tsx` (Component, 30 blocks) |
| `YearlyValueCalcModal/StepContentV2.tsx` | 157 | One calculator step's inputs | presentational | **no** |
| `YearlyValueCalcModal/ResultContentV2.tsx` | 54 | Result screen incl. thousand-separator formatting | presentational | yes — `ResultContentV2-tests.tsx` (Component) |
| `YearlyValueCalcModal/steps.ts` | 65 | `steps` metadata + `validationSchema` (yup) | schema/util | yes — `steps-tests.ts` (Unit) |
| `YearlyValueCalcModal/types.ts` | 47 | Calculator form/step types | type | **no** |

## G. apps/settings — AddPaymentMethodModalV2 (legacy split Card Elements + new core bridge)

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `AddPaymentMethodModalV2/index.tsx` | 14 | `AddPaymentMethodModalV2` shell | presentational | yes — `AddPaymentMethodModalV2-tests.tsx` (Component) |
| `AddPaymentMethodModalV2/AddPaymentMethodModalV2Content.tsx` | 51 | Bridges settings → **core** `AddPaymentMethodElementModal` (:6, :43) | container | **no** (indirect, and the covering test mocks the core modal) |
| `AddPaymentMethodModalV2/CreditCardFormContentV2.tsx` | 452 | Legacy split-Card-Element credit-card form; calls `createSetupIntentV2` (:18, :120) | container | yes — `CreditCardFormContentV2-tests.tsx` (Component, 2 blocks / ZIP restrictions only) |
| `AddPaymentMethodModalV2/AchFormContentV2.tsx` | 339 | ACH / Financial Connections form; `createSetupIntentV2` (:27, :93), `prepareSetupIntentV2` (:26, :183); exports `achV2Schema` | container | yes ×2 — `AchFormContentV2-schema-tests.ts` (Unit) + `AchFormContentV2-handleConnectBank-tests.tsx` (Component) |
| `AddPaymentMethodModalV2/PaymentMethodTypeRadioGroup.tsx` | 43 | Card vs bank radio group | presentational | **no** |
| `AddPaymentMethodModalV2/styles.ts` | 17 | `FormSection`, `Disclaimer` | presentational | **no** |
| `AddPaymentMethodModalV2/types.ts` | 29 | `PaymentMethodType`, `AddCreditCardFormInputs`, `allowedStripeCardBrands` | type | **no** |

## H. apps/settings — hooks, schemas, Stripe utils

| File | Lines | Purpose | Class | Flags | Dedicated test |
|---|---|---|---|---|---|
| `hooks/usePracticeBillingSettings.ts` | 44 | Loads the practice billing view model | hook | — | yes — Hook |
| `hooks/useRecoverySummary.ts` | 76 | Loads + maps the recovery summary, tracks refresh | hook | — | yes — Hook (9 blocks) |
| `hooks/useBillingToast.ts` | 50 | Billing toast queue incl. top-layer promotion + auto-dismiss | hook | — | yes — Hook (10 blocks) |
| `hooks/usePrewarmBillingStripe.ts` | 29 | Pre-loads Stripe.js for the billing page | hook | — | yes — Hook |
| `utils/schemaBuilder.ts` | 130 | 5 yup schemas: `editBillingEmailModalSchema` (:16), `editBusinessAddressModalSchema` (:28), `addCreditCardModalSchema` (:49), `editBillingContactInfoModalSchema` (:71), `editMonthlyLimitModalSchema` (:102) | schema/util | `getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit')` (:6, :99); hardcoded `maximumMonthlyLimit = 500000` (:101) | **no** |
| `utils/getStripePromise.ts` | 30 | `loadStripe` wrapper taking `shouldUseSandbox: boolean`, reads `config/environment` | schema/util | — | yes — `getStripePromise-tests.ts` (Unit) |
| `utils/shouldUseStripeSandbox.ts` | 2 | `window.ZdBootstrapPracticeDetails?.is_test_practice ?? false` — **byte-identical** to the `shared/core` copy | schema/util | — | yes — `utils/__tests__/shouldUseStripeSandbox-tests.ts` (Unit) |

## I. apps/settings — routes, types, dev-server mocks

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `apps/settings/src/config/routes.ts` | 683 | Route templates incl. 12 billing endpoints (:562–:683) | schema/util | **no** (URL shapes asserted indirectly in `apiCalls-tests.ts`) |
| `apps/settings/src/types/practiceBillingSettingsTypes.ts` | 45 | `PracticeBillingSettingsViewModelType`, `PaymentMethodInfo`, `BillInfo`, `BillStatus`, … | type | **no** |
| `apps/settings/src/server/controllers/practiceBillingSettingsPage/practiceBillingSettings.ts` | 486 | 18 exported Express dev-server handlers (`postSetupIntent`, `postSetupIntentWithCustomer`, `postPaymentMethodV2`, `postPrepareSetupIntent`, `getInvoicePdfDownloadUrl`, …) | mock | **no** |
| `apps/settings/src/server/controllers/practiceBillingSettingsPage/mocks.ts` | 490 | `mockPracticeBillingSettingsViewModel`, `mockCreditCardInfo`, `mockAchInfo`, `mockBillSummaryResponse`, `ACTIVE_MOCK_SCENARIO = 1` | mock | **no** — but imported as the fixture source by many component tests, so a change here silently moves assertions in several suites |

## J. shared/core/src/billing — the extracted Payment Element layer

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `useConfirmPaymentSetup.ts` | 120 | Deferred-intent driver: `elements.submit()` → `createSetupIntentWithCustomer` → `stripe.confirmSetup({ redirect: 'if_required' })`; caches `confirmedPaymentMethodIdRef` so a retry cannot mint a second payment method/Stripe Customer; `ProviderFacingError` marker object (deliberately not a subclass — es5 `instanceof`); exports `GENERIC_SUBMIT_ERROR_MESSAGE` | hook | yes — `useConfirmPaymentSetup-tests.tsx` (Component, 11 blocks) |
| `createSetupIntentWithCustomer.ts` | 44 | POST setup intent w/ customer; 400 → `errorMessage`, other non-200 → throw | business-logic | yes — Unit |
| `addPaymentMethod.ts` | 50 | Persists the tokenized method; exports `SAVE_FAILED_MESSAGE` | business-logic | yes — Unit |
| `getBillingAddress.ts` | 47 | Reads the stored billing address; returns `null` on any failure. Own JSDoc: "Values arrive unvalidated — the read carries none of the write's format constraints" | business-logic | **no** |
| `updateBillingAddress.ts` | 59 | Writes the billing address: 204 = success, ≥500 logs + generic copy, 400 surfaces `response.data.message`; exports `SAVE_ADDRESS_FAILED_MESSAGE` | business-logic | **no** |
| `billingApiClient.ts` | 20 | `getBillingApiClient()` lazy singleton over the generated client | business-logic | **no** |
| `billingAddressSchema.ts` | 40 | yup schema for the billing address | schema/util | yes — Unit |
| `usStateOptions.ts` | 61 | `US_STATE_OPTIONS`, `US_STATE_CODES` | schema/util | yes — Unit |
| `useBillingAddressForm.ts` | 35 | react-hook-form setup for the address fields | hook | **no** |
| `useBillingAddressPrefill.ts` | 54 | Prefills the address form from `getBillingAddress` | hook | yes — Hook |
| `getBillingStripePromise.ts` | 37 | Memoized `loadStripe` keyed by publishable key; logs and resolves `null` when the key is missing | schema/util | yes — Unit (6 blocks) |
| `shouldUseStripeSandbox.ts` | 2 | Sandbox switch — byte-identical duplicate of the `apps/settings` copy | schema/util | yes — Unit |
| `paymentElementOptions.ts` | 43 | `ELEMENTS_OPTIONS`, `PAYMENT_ELEMENT_OPTIONS` (Stripe appearance/layout config) | schema/util | **no** |
| `types.ts` | 47 | `PaymentMethodInfo`, `CreateSetupIntentResult`, `AddPaymentMethodResult`, … | type | **no** |
| `index.ts` | 33 | Barrel | type | **no** |

## K. shared/core/src/paymentRecovery + paymentMethodArtwork

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `recoveryBannerSuppression.ts` | 161 | `SUPPRESSION_TTL_MS = 36h`, `buildSuppressionKey`, `suppressRecoveryBanner`, `evaluateRecoverySuppression` (browser-storage backed) | business-logic | yes — Unit (20 blocks, 444 lines) |
| `mapRecoveryToSummary.ts` | 48 | API recovery payload → `RecoveryStatusSummary` | business-logic | yes — Unit |
| `mapRecoveryBalanceDetail.ts` | 53 | API balance-detail payload → month groups | business-logic | yes — Unit |
| `mapRecoveryMethodDisplay.ts` | 45 | Failed method → display model | business-logic | **no** |
| `deriveOutcome.ts` | 43 | Charge result → `OutcomeVariant` | business-logic | yes — Unit (single `it.each`) |
| `selectRecoveryVariant.ts` | 23 | Chooses the banner variant | business-logic | yes — Unit |
| `buildRecoveryBillingUrl.ts` | 15 | Builds the deep link into the billing page | business-logic | **no** |
| `recoveryCopy.ts` | 134 | `formatBalance`, `formatShortMonth`, `formatLongMonth`, `getRecoveryCopy` (per surface) | schema/util | yes — Unit |
| `recoveryBannerCopy.ts` | 50 | `getRecoveryBannerCopy` | schema/util | yes — Unit |
| `recoveryOutcomeCopy.ts` | 130 | `getRecoveryOutcomeCopy` | schema/util | yes — Unit |
| `failedPaymentMethodCopy.ts` | 96 | `getProviderCount`, `getProviderTooltipText/Label`, `getFailedMethodHeading`, `ROLLOVER_BLOCKED_LINE`, decline line | schema/util | yes — Unit |
| `mockRecovery.ts` | 398 | Dev scenario fixtures (`ACTIVE_MOCK_SCENARIO = 1`), `getMockRecoveryResponse`, `getScenarioFromUrl` | mock | yes — Unit (8 blocks) |
| `recoveryStatusTypes.ts` | 157 | `FailedPaymentMethod`, `RecoveryMethodDisplay`, `UpdatedCardIdentity`, … | type | **no** |
| `index.ts` | 51 | Barrel | type | **no** |
| `paymentMethodArtwork/getPaymentMethodArtwork.ts` | 38 | Brand → artwork mapping | schema/util | yes — Unit (single `it.each`) |

## L. shared/core/src/components (billing/recovery components)

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `AddPaymentMethodModal/index.tsx` | 128 | `AddPaymentMethodModal` chrome: title/data-test contract, submit + cancel buttons, synchronous `isSubmittingRef` re-entrancy guard ("Deliberately still submitting") | presentational | yes — `AddPaymentMethodModal-tests.tsx` (Component) |
| `AddPaymentMethodModal/AddPaymentMethodElementModal.tsx` | 142 | Unified Payment Element modal; exports `BILLING_ADDRESS_INCOMPLETE_MESSAGE`; consumed by settings **and** provider-home | container | yes — `AddPaymentMethodElementModal-tests.tsx` (Component, 14 blocks) |
| `AddPaymentMethodModal/PaymentElementFields.tsx` | 23 | Stripe `PaymentElement` wrapper; applies `EXCLUDE_FROM_FULLSTORY_CLASS` | presentational | yes — Component (3 blocks) |
| `AddPaymentMethodModal/BillingAddressFields.tsx` | 85 | Address fields on the real `useBillingAddressForm` | presentational | yes — Component (5 blocks) |
| `AddPaymentMethodModal/styles.ts` | 36 | Styled sections for the modal | presentational | **no** |
| `FailedPaymentMethodCard/index.tsx` | 304 | Failed-card card incl. rollover-order state; exports `cardLabel` | presentational | yes — Component (29 blocks, 572 lines) |
| `FailedPaymentsByMonth/index.tsx` | 142 | Groups failed cards by month with subtotals | presentational | yes — Component (13 blocks) |
| `RecoveryStatusBanner/index.tsx` | 79 | "Update your payment method" banner + CTA | presentational | yes — Component (9 blocks) |
| `RecoveryOutcomeBanner/index.tsx` | 103 | Post-charge outcome banner | presentational | yes — Component (6 blocks) |
| `RecoveryProcessingBanner/index.tsx` | 73 | "Processing your payment…" `role=status` banner | presentational | yes — Component (2 blocks, 24-line test) |
| `PaymentSetupBanner/index.tsx` | 55 | "Add a payment method" banner; exports title/body/CTA copy constants | presentational | yes — Component (7 blocks) |
| `PaymentMethodLogo/index.tsx` | 39 | Brand logo | presentational | yes — Component (3 blocks) |
| `PriceByProviderModal/PriceByProviderModal.tsx` | 109 | Per-provider price breakdown modal (has `__stories__`, no test) | presentational | **no** |
| `shared/core/src/testing/installStripeJsFake.ts` | 130 | Test helper that fakes `window.Stripe` | mock | **no** (it is itself test infrastructure) |

## M. apps/provider-home-webapp (billing/payment/SKU only)

| File | Lines | Purpose | Class | Flags | Dedicated test |
|---|---|---|---|---|---|
| `apis/recoveryApi.ts` | 29 | `fetchRecovery` for the homepage banner | business-logic | — | yes — Unit (3 blocks) |
| `pages/homepage/hooks/useRecoveryStatusSummary.ts` | 71 | Homepage recovery banner state; must never throw or flash on a failed read (:15–18) | hook | `PAYMENT_RECOVERY_EXPERIMENTS` → `'billing_payment_recovery_experience'` (`ab/experiments.ts:160`) | yes — `useRecoveryStatusSummary.test.ts` (Hook, 7 blocks) |
| `pages/homepage/reposition/components/ActivationAddPaymentMethodModal.tsx` | 32 | Renders core `AddPaymentMethodElementModal` (:3, :24) with `getBillingStripeKeys()`, then opens the activation success modal | container | `'billing_inline_activation_payment_modal'` (`ab/experiments.ts:179`) is read by `useActivateMarketplace.tsx`, not here | yes — Component (4 blocks) — but it **mocks the core modal**, so only wiring is asserted |
| `pages/identityVerification/StripeContext.tsx` | 32 | `StripeProvider` / `useStripeContext` for identity verification | container | — | **no** |
| `pages/signUpPortal/.../RecommendationsStep/SkuModal.tsx` | 255 | SKU selection modal (`SkuModal`, `SkuModalView`) | container | — | **no** |
| `services/skuService.ts` | 136 | `updateSkus` — SKU add/remove incl. ClaimYourProfile practices | business-logic | — | yes — `skuService-test.ts` (Unit, 16 blocks) |
| `utils/skuValidator.ts` | 66 | `SkuValidator` | business-logic | — | yes — Unit (6 blocks) |
| `server/mocks/billingAddressData.ts` | 93 | Dev-server billing-address mocks incl. `ADDRESS_ERROR_SCENARIO` | mock | — | **no** |
| `server/mocks/paymentSetupData.ts` | 129 | Dev-server setup-intent mocks; `createSandboxSetupIntent` talks to the real `https://api.stripe.com/v1` sandbox | mock | — | **no** |
| `server/mocks/skuTasksData.ts` | 52 | `TASKS_BY_SKU_LIST` | mock | — | **no** |

## N. apps/spo-webapp (billing-related only)

| File | Lines | Purpose | Class | Dedicated test |
|---|---|---|---|---|
| `hooks/useIsClosedBillingPeriod.ts` | 39 | Derives `isDateRangeWithinClosedMonth` / `doesDateRangeSpanFullMonth` from the SPO date range | hook | yes — Hook (2 blocks) |
| `pages/EnrollV2Page/utils/buildPaymentMessage.ts` | 19 | `buildPaymentMessage` for SPO enrollment | schema/util | yes — Unit (2 blocks, both `it.each`) |

## Source files with ZERO dedicated test coverage (64 of 152)

Indirect coverage is only claimed where a named test actually imports/renders the module.

| File | Class | Indirect coverage (covering test) |
|---|---|---|
| `apps/settings/.../invoiceHelpers.ts` | schema/util | Only transitively, through the renderers that import it: `InvoiceDetailsContainer.tsx:21` → `InvoiceDetailsContainer-tests.tsx` (Component), `v2/FpbInvoiceView.tsx:22` → `FpbInvoiceView-tests.tsx` (Component). **No test imports it directly.** |
| `apps/settings/.../utils/schemaBuilder.ts` | schema/util | Only through the 5 modals that import it (`EditMonthlyLimitModalV2:8`, `EditBillingEmailModal:12`, `EditBusinessAddressModal:12`, `CreditCardFormContentV2:17`, `EditBillingContactInfoModal:11`). **No test imports it directly.** |
| `apps/settings/.../PaymentMethodsList/PaymentMethodsList.tsx` | container | **None.** `PaymentMethodsListV2-tests.tsx` renders V2 directly and skips this adapter; `BillingSettingsContainer-tests.tsx` (Integration) renders it as a real child but asserts on page behaviour, not the in-place mutation. |
| `apps/settings/.../AddPaymentMethodModalV2/AddPaymentMethodModalV2Content.tsx` | container | `AddPaymentMethodModalV2-tests.tsx` (Component) renders the shell around it, but mocks the core `AddPaymentMethodElementModal` it exists to bridge. |
| `apps/settings/.../AddPaymentMethodModalV2/PaymentMethodTypeRadioGroup.tsx` | presentational | `CardEntryStep-tests.tsx` (Component) renders it as a real child. |
| `apps/settings/.../PaymentRecovery/steps/BalanceLoadFallback.tsx` | presentational | `PayNowModal-tests.tsx` (Integration) `describe('itemized balance load')` renders the loading/error states through it. |
| `apps/settings/.../PaymentRecovery/payNowScenarios.ts` | mock | **None.** |
| `apps/settings/.../PaymentRecovery/copy.ts` | schema/util | `PayNowModal-tests.tsx` (Integration) asserts the subtitle string. |
| `apps/settings/.../PaymentRecovery/types.ts` | type | Type-only. |
| `apps/settings/.../PaymentRecovery/__fixtures__/payNowFixtures.ts` | mock | Consumed by `PayNowModal-tests.tsx`, `ReviewStep-tests.tsx`, `BillingSettingsContainer-tests.tsx`, `resolvePaymentOutcome-tests.ts`, `usePaymentRecoveryFlow-tests.ts`. |
| `apps/settings/.../YearlyValueCalcModal/StepContentV2.tsx` | presentational | `YearlyValueCalcModalV2-tests.tsx` (Component) drives it via the modal (`describe('step navigation')`, `describe('form validation')`). |
| `apps/settings/.../YearlyValueCalcModal/types.ts` | type | Type-only. |
| `apps/settings/.../BillStatusLabel.tsx` | presentational | `BillsContainer-tests.tsx` (Component) renders bill rows containing it. |
| `apps/settings/.../components/BillingCoachmark.tsx` | presentational | `BillingSettingsContainer-tests.tsx` (Integration) imports `BillPageCoachmarkState` and renders the page that mounts it. |
| `apps/settings/.../components/modal/InputWithTitle.tsx` | presentational | Rendered by every edit-modal component test (`EditBillingEmailModal-tests.tsx`, `EditBusinessAddressModal-tests.tsx`, `EditMonthlyLimitModalV2-tests.tsx`, `EditBillingContactInfoModal-tests.tsx`). |
| `apps/settings/.../components/modal/ActionButtons.tsx` | presentational | Same edit-modal component tests (save/cancel clicks). |
| `apps/settings/.../components/modal/ModalWrapper.tsx` | presentational | Same edit-modal component tests. |
| `apps/settings/.../components/modal/StateZipContainer.tsx` | presentational | `EditBusinessAddressModal-tests.tsx` (Component). |
| `apps/settings/.../components/modal/StyledRHFDropdown.tsx` | presentational | `EditBusinessAddressModal-tests.tsx` (Component), `PaymentMethodsPerProviderModal-tests.tsx` (Component). |
| `apps/settings/.../components/v2/BillingModalFooter.tsx` | presentational | `PayNowModal-tests.tsx` (Integration) and `ReviewStep-tests.tsx` (Component) click through it. |
| `apps/settings/.../components/ArrowRedirectionLink.tsx` | presentational | **None identified.** |
| `apps/settings/.../components/BillingToastStyleOverrides.ts` | presentational | **None identified.** |
| `apps/settings/.../components/ButtonIfCanEdit.tsx` | presentational | `PaymentMethodsListV2-tests.tsx` / `PaymentMethodV2-tests.tsx` exercise the permission-gated affordances. |
| `apps/settings/.../components/DropdownIfCanEdit.tsx` | presentational | `PaymentMethodV2-tests.tsx` `describe('menu items visibility')`. |
| `apps/settings/.../components/LinkIfCanEdit.tsx` | presentational | `BillingContactInfo-tests.tsx` (Component). |
| `apps/settings/.../components/CentralizedLoader.tsx` | presentational | `PricingInformationV2-tests.tsx` `describe('Loading state')`. |
| `apps/settings/.../components/ErrorMessage.tsx` | presentational | Edit-modal component validation tests. |
| `apps/settings/.../components/FlexRowDiv.tsx` | presentational | Layout only; rendered widely, asserted nowhere. |
| `apps/settings/.../components/RowItemContainer.tsx` | presentational | Layout only. |
| `apps/settings/.../components/SectionTitle.tsx` | presentational | Layout only. |
| `apps/settings/.../components/StyledDiv.tsx` | presentational | Layout only. |
| `apps/settings/.../components/TooltipText.tsx` | presentational | `FailedPaymentMethodCard-tests.tsx` covers the core equivalent; this copy is asserted nowhere. |
| `apps/settings/.../context/BillingSettingsContext.ts` | type | Used as a **real** provider by `billing-analytics-events-tests.tsx`, `PaymentMethodsListV2-tests.tsx`, `AddPaymentMethodModalV2-tests.tsx`, `BillingContactInfo-tests.tsx`. |
| `apps/settings/.../fixtures/bookingSourceBreakdownFixtures.ts` | mock | Fixture. |
| `apps/settings/.../FpbInvoiceDetailsComponents/BookingSourceRows.tsx` | presentational | `FpbInvoiceView-tests.tsx` `describe('booking source breakdown rows')`. |
| `apps/settings/.../FpbInvoiceDetailsComponents/formatCurrency.ts` | schema/util | Via `FpbInvoiceView-tests.tsx` / `TaxesAndFeesSection-tests.tsx` / `PatientBookingsSection-tests.tsx` assertions on rendered amounts. Note `FeaturedProviderSection.tsx:8` and `LicenseFeeSection.tsx:9` do **not** use it — they each define a local `formatCurrency`. |
| `apps/settings/.../FpbInvoiceDetailsComponents/grid.tsx` | presentational | Layout only. |
| `apps/settings/.../FpbInvoiceDetailsComponents/FpbInvoiceView.types.ts` | type | Type-only (imported by `FpbInvoiceView-tests.tsx`). |
| `apps/settings/.../v2/FAQsSection.tsx` | presentational | `billing-analytics-events-tests.tsx` `describe('FAQ click analytics events')` + `PricingInformationV2-tests.tsx` `describe('FAQs section')`. No dedicated test for a 283-line component. |
| `apps/settings/.../v2/FreeProductsCard.tsx` | presentational | **None identified** (186 lines). |
| `apps/settings/src/config/routes.ts` | schema/util | `apiCalls-tests.ts` (Unit) asserts the resolved URLs. |
| `apps/settings/src/types/practiceBillingSettingsTypes.ts` | type | Type-only. |
| `apps/settings/src/server/.../practiceBillingSettings.ts` | mock | **None.** 18 dev-server handlers, incl. all four setup-intent endpoints. |
| `apps/settings/src/server/.../mocks.ts` | mock | **None** — yet it is the fixture source for `BillingSettingsContainer-tests.tsx`, `apiCalls-tests.ts`, `billing-analytics-events-tests.tsx`, `PaymentMethodsListV2-tests.tsx`, `EditMonthlyLimitModalV2-tests.tsx`, `AddPaymentMethodModalV2-tests.tsx`. |
| `shared/core/src/billing/getBillingAddress.ts` | business-logic | Only through `useBillingAddressPrefill-tests.ts` (Hook) and `AddPaymentMethodElementModal-tests.tsx` (Component), both of which mock it. **The unvalidated-read path its own JSDoc warns about is untested.** |
| `shared/core/src/billing/updateBillingAddress.ts` | business-logic | Only through `AddPaymentMethodElementModal-tests.tsx` (Component), which mocks it. **400/≥500 branches and `SAVE_ADDRESS_FAILED_MESSAGE` untested.** |
| `shared/core/src/billing/billingApiClient.ts` | business-logic | Mocked out by `addPaymentMethod-tests.ts`, `createSetupIntentWithCustomer-tests.ts`, `AddPaymentMethodElementModal-tests.tsx`. Singleton behaviour untested. |
| `shared/core/src/billing/paymentElementOptions.ts` | schema/util | Passed through by `AddPaymentMethodElementModal-tests.tsx` (Component); the option values themselves are asserted nowhere. |
| `shared/core/src/billing/useBillingAddressForm.ts` | hook | Real (unmocked) in `useBillingAddressPrefill-tests.ts` (Hook) and `BillingAddressFields-tests.tsx` (Component). |
| `shared/core/src/billing/types.ts` | type | Type-only. |
| `shared/core/src/billing/index.ts` | type | Barrel. |
| `shared/core/src/components/AddPaymentMethodModal/styles.ts` | presentational | Rendered by the two AddPaymentMethodModal component suites. |
| `shared/core/src/components/PriceByProviderModal/PriceByProviderModal.tsx` | presentational | Indirect (Component) — rendered as a real child of `PricingInformationV2`; opened at `apps/settings/.../__tests__/PricingInformationV2-tests.tsx:215` (`opens PriceByProviderModal when "View price by provider" is clicked`). No dedicated suite; has `__stories__`. |
| `shared/core/src/paymentRecovery/mapRecoveryMethodDisplay.ts` | business-logic | **None.** No test imports it; `sampleMethodDisplays` in `payNowFixtures.ts` hand-builds the shape instead. |
| `shared/core/src/paymentRecovery/buildRecoveryBillingUrl.ts` | business-logic | **None.** |
| `shared/core/src/paymentRecovery/recoveryStatusTypes.ts` | type | Type-only. |
| `shared/core/src/paymentRecovery/index.ts` | type | Barrel. |
| `shared/core/src/testing/installStripeJsFake.ts` | mock | Test infrastructure. |
| `apps/provider-home-webapp/src/pages/identityVerification/StripeContext.tsx` | container | **None.** |
| `apps/provider-home-webapp/src/pages/signUpPortal/.../SkuModal.tsx` | container | **None** (255 lines). |
| `apps/provider-home-webapp/src/server/mocks/billingAddressData.ts` | mock | **None.** |
| `apps/provider-home-webapp/src/server/mocks/paymentSetupData.ts` | mock | **None** — and it calls the live Stripe sandbox API. |
| `apps/provider-home-webapp/src/server/mocks/skuTasksData.ts` | mock | **None.** |

## Candidate Gaps

| # | What's missing | Level | Path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| SC-1 | No direct test for `utils/schemaBuilder.ts` — all 5 billing yup schemas, incl. the `Billing.MinimumPaymentMethodLimit` flag read (:99) and the hardcoded `maximumMonthlyLimit = 500000` (:101) | Unit | `apps/settings/src/pages/settingsPages/billingSettings/utils/schemaBuilder.ts` | These schemas are the only guard on money limits and billing email/address writes. Today a bad boundary is caught only if one of 5 modal component suites happens to type the failing value | S (1 file, ~40 cases) | **P0** |
| SC-2 | No direct test for `invoiceHelpers.ts` (`formatDate`, `getLastDayOfMonth`, `capitalizeStatus`) | Unit | `apps/settings/.../invoiceHelpers.ts` | `getLastDayOfMonth` drives invoice period labels; a month-boundary/DST bug misstates the billing period on a customer-visible invoice | XS | **P1** |
| SC-3 | `updateBillingAddress.ts` + `getBillingAddress.ts` have no test at any level; only mocked | Unit | `shared/core/src/billing/updateBillingAddress.ts`, `getBillingAddress.ts` | The write's 400/≥500 branching and `SAVE_ADDRESS_FAILED_MESSAGE` decide whether a provider sees a real error or a silent success; the read is explicitly documented as unvalidated | S | **P0** |
| SC-4 | `PaymentMethodsList.tsx` (V1 adapter) untested, and it mutates the props array in place to clear the previous default | Component | `apps/settings/.../PaymentMethodsList/PaymentMethodsList.tsx` | `filter(p => p.isDefault)[0].isDefault = false` throws when no card is currently default; this is the default-payment-method path | S | **P1** |
| SC-5 | `mapRecoveryMethodDisplay.ts` untested while its 9 sibling mappers in the same folder each have a unit suite | Unit | `shared/core/src/paymentRecovery/mapRecoveryMethodDisplay.ts` | Card identity shown on the failed-payment card comes from here; fixtures hand-build the shape so drift is invisible | XS | **P2** |
| SC-6 | `buildRecoveryBillingUrl.ts` untested | Unit | `shared/core/src/paymentRecovery/buildRecoveryBillingUrl.ts` | It is the deep link from the homepage banner into billing; a wrong URL silently dead-ends the recovery funnel | XS | **P2** |
| SC-7 | `FAQsSection.tsx` (283 lines) and `FreeProductsCard.tsx` (186 lines) have no dedicated test | Component | `apps/settings/.../v2/FAQsSection.tsx`, `v2/FreeProductsCard.tsx` | Largest untested presentational surfaces on the pricing tab | M | P2 |
| SC-8 | `practiceBillingSettings.ts` (18 dev-server handlers) and `mocks.ts` (490 lines) untested, yet `mocks.ts` is the fixture source for 6+ suites | Unit | `apps/settings/src/server/controllers/practiceBillingSettingsPage/*` | A change to `mockPracticeBillingSettingsViewModel` silently shifts assertions across unrelated suites; nothing pins the mock's shape to the real view model type | S | P2 |
| SC-9 | `paymentSetupData.ts` calls the live Stripe sandbox from the dev server and is untested | Unit | `apps/provider-home-webapp/src/server/mocks/paymentSetupData.ts` | Outbound Stripe call from a "mock" file; nothing asserts it stays sandbox-only | S | P2 |
| SC-10 | `PriceByProviderModal.tsx`, `StripeContext.tsx`, `SkuModal.tsx` untested | Component | `shared/core/src/components/PriceByProviderModal/PriceByProviderModal.tsx`, `apps/provider-home-webapp/src/pages/identityVerification/StripeContext.tsx`, `.../RecommendationsStep/SkuModal.tsx` | Shipped UI with zero regression net; `StripeContext` is a Stripe integration point | M | P3 |

## Level Summary

| Metric | Count |
|---|---|
| Billing source files in scope | **152** |
| Source files with a dedicated test file | **88** |
| Source files with ZERO dedicated test file | **64** |
| …of those, with no identified indirect coverage either | **13**: `payNowScenarios.ts`, `ArrowRedirectionLink.tsx`, `BillingToastStyleOverrides.ts`, `FreeProductsCard.tsx`, `practiceBillingSettings.ts`, `mocks.ts`, `mapRecoveryMethodDisplay.ts`, `buildRecoveryBillingUrl.ts`, `StripeContext.tsx`, `SkuModal.tsx`, `billingAddressData.ts`, `paymentSetupData.ts`, `skuTasksData.ts` (`PriceByProviderModal.tsx` was moved out of this list on re-verification: it is rendered indirectly at `PricingInformationV2-tests.tsx:215`) |
| Dedicated coverage by level: unit-level only | 33 files |
| Dedicated coverage by level: Unit + Component | 1 file (`AchFormContentV2.tsx`) |
| Dedicated coverage by level: Component (component render) | 43 files |
| Dedicated coverage by level: Hook (`renderHook`) | 9 files |
| Dedicated coverage by level: Integration | 2 files |
| Billing test files in scope | **90** |
| Declared `it`/`test` blocks across them | **856** |
| Classification: `presentational` | 61 |
| Classification: `business-logic` | 21 |
| Classification: `container` | 18 |
| Classification: `schema/util` | 21 |
| Classification: `hook` | 11 |
| Classification: `type` | 10 |
| Classification: `mock` | 10 |
| (classification total) | 152 |
