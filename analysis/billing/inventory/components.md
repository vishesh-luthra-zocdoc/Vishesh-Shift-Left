# Component-to-Test Map

Every billing source component and whether it has a unit test (UT), Cypress test (CY), or nothing.

**Legend:** UT = Unit Test, CY = Cypress E2E, -- = No test

---

## Core Containers & Pages

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 1 | BillingSettingsContainer | BillingSettingsContainer-tests.tsx | billing-settings-page-tests.ts | UT covers tab rendering + coachmarks only |
| 2 | InvoiceDetailsContainer | InvoiceDetailsContainer-tests.tsx | -- | 9 tests: loading, error, routing, PDF URL |
| 3 | BillsContainer | -- | billing-settings-page-tests.ts (indirect) | **GAP: No unit test** |
| 4 | PricingInformation | PricingTab-tests.tsx | -- | UT only checks show/hide |

## Payment Methods — V1 (Legacy)

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 5 | PaymentMethodsList | -- | billing-settings-page-tests.ts | **GAP: No UT.** Gated behind `SHOW_NEW_BILLING_MEZZ_REVAMP=off` |
| 6 | PaymentMethod | -- | billing-settings-page-tests.ts | **GAP: No UT.** Contains set-default + delete API calls |
| 7 | PaymentMethodsPerProviderList | -- | -- | **GAP: No tests at all.** May be obsolete if V2 active |

## Payment Methods — V2 (Mezzanine)

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 8 | PaymentMethodsListV2 | PaymentMethodsListV2-tests.tsx (11) | billing-settings-v2-tests.ts | Well covered |
| 9 | PaymentMethodV2 | PaymentMethodV2-tests.tsx (22) | billing-settings-v2-tests.ts | Well covered |
| 10 | PaymentMethodsPerProviderModal | PaymentMethodsPerProviderModal-tests.tsx (5) | billing-settings-v2-tests.ts | Well covered |
| 11 | EditBillingContactInfoModal | -- | billing-settings-v2-tests.ts | **GAP: No UT.** Has form validation + 2 API calls |

## Modals

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 12 | AddCreditCardModal | AddCreditCardModal-tests.tsx (12) | billing-settings-page-tests.ts | UT covers validation + Stripe key |
| 13 | AddAchModal | AddAchModal-tests.tsx (8) | billing-settings-page-tests.ts | UT covers form validation |
| 14 | AddPaymentMethodModal | -- | billing-settings-page-tests.ts (indirect) | **GAP: No UT** |
| 15 | EditBillingEmailModal | EditBillingEmailModal-tests.tsx (2) | billing-settings-page-tests.ts | UT covers validation only |
| 16 | EditBusinessAddressModal | EditBusinessAddressModal-tests.tsx (8) | billing-settings-page-tests.ts | UT covers validation only |
| 17 | EditMonthlyLimitModal (V1) | EditMonthlyLimitModal-tests.tsx (3) | billing-settings-page-tests.ts | **POSSIBLY OBSOLETE** if V2 fully rolled out |
| 18 | EditMonthlyLimitModalV2 | EditMonthlyLimitModalV2-tests.tsx | billing-settings-v2-tests.ts | Well covered |
| 19 | EditRolloversModal | EditRolloversModal-tests.tsx (2) | billing-settings-page-tests.ts | UT tests validation only (not save flow) |
| 20 | DeletePaymentMethodConfirmationModal | -- | billing-settings-page-tests.ts | **GAP: No UT** |
| 21 | BillingCompletionModal | -- | billing-settings-page-tests.ts (indirect) | **GAP: No UT.** CY only checks show/hide |

## Invoice Views

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 22 | FpbInvoiceView | FpbInvoiceView-tests.tsx (22) | invoice-details-page-tests.ts | Well covered |
| 23 | LegacyInvoiceView | LegacyInvoiceView-tests.tsx (12) | -- | **POSSIBLY OBSOLETE** if new invoice flag is on |
| 24 | FeaturedProviderSection | FeaturedProviderSection-tests.tsx (7) | -- | UT covers single/multi/collapse |
| 25 | LicenseFeeSection | LicenseFeeSection-tests.tsx (5) | -- | UT covers fee + tax display |
| 26 | PatientBookingsSection | PatientBookingsSection-tests.tsx (7) | invoice-details-page-tests.ts | Well covered |

## Billing Contact Info

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 27 | BillingContactInfo | BillingContactInfo-tests.tsx (11) | billing-settings-v2-tests.ts | Well covered |
| 28 | BusinessAddress | -- | -- | **GAP:** Tested indirectly via parent. Presentational. |
| 29 | BillingEmail | -- | -- | **GAP:** Tested indirectly via parent. Presentational. |
| 30 | BillStatusLabel | -- | -- | **GAP:** Simple status→tag mapping. Low risk. |

## Pricing Calculator (YearlyValueCalcModal)

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 31 | YearlyValueCalcModal | -- | billing-settings-page-tests.ts (partial) | **GAP: No UT.** CY tests 6-step navigation only |
| 32 | StepContent | -- | -- | **GAP: ZERO tests** |
| 33 | ResultContent | -- | -- | **GAP: ZERO tests** |
| 34 | steps config | -- | -- | **GAP: Validation + step config untested** |

## Utilities & Hooks

| # | File | UT | Notes |
|---|------|----|-------|
| 35 | apiCalls.ts | apiCalls-tests.ts (26) | **All 10 API functions tested** |
| 36 | invoiceHelpers.ts | -- | **GAP: 3 functions untested** |
| 37 | SkuTitleMap.ts | SkuTitleMap-tests.ts (5) | Covered |
| 38 | billingDateUtils.ts | billingDateUtils-tests.ts (12) | Covered |
| 39 | schemaBuilder.ts | -- | **GAP: 7 schemas tested only indirectly** |
| 40 | shouldUseStripeSandbox.ts | useShouldUseStripeSandbox-tests.ts (6) | All 4 boolean branches covered |
| 41 | usePracticeBillingSettings hook | usePracticeBillingSettings-tests.ts (3) | Covered |

---

## Coverage Summary

| Category | Total | With UT | With CY | With Both | With Neither |
|----------|-------|---------|---------|-----------|--------------|
| Containers/Pages | 4 | 3 | 2 | 1 | 0 |
| Payment Methods V1 | 3 | 0 | 2 | 0 | 1 |
| Payment Methods V2 | 4 | 3 | 4 | 3 | 0 |
| Modals | 10 | 6 | 8 | 5 | 0 |
| Invoice Views | 5 | 5 | 2 | 2 | 0 |
| Contact Info | 4 | 1 | 1 | 1 | 2 |
| Pricing Calculator | 4 | 0 | 1 | 0 | 3 |
| Utilities/Hooks | 7 | 5 | 0 | 0 | 2 |
| **Total** | **41** | **23 (56%)** | **20 (49%)** | **12 (29%)** | **8 (20%)** |
