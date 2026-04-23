# Component-to-Test Map

Every billing source component and whether it has a unit test (UT), Cypress test (CY), or nothing.

**Legend:** UT = Unit Test, CY = Cypress E2E, -- = No test

---

## Core Containers & Pages

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 1 | BillingSettingsContainer | BillingSettingsContainer-tests.tsx | billing-settings-page-tests.ts | Experiment flags tested |
| 2 | InvoiceDetailsContainer | InvoiceDetailsContainer-tests.tsx (14) | invoice-details-page-tests.ts | Routing V1 → V2, loading states |
| 3 | BillsContainer | BillsContainer-tests.tsx (21) | (indirect) | NEW: invoice list filtering + analytics |

## Payment Methods — V1 (Legacy)

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 4 | PaymentMethodsList | -- | billing-settings-page-tests.ts | May be gated behind experiment |
| 5 | PaymentMethod | -- | billing-settings-page-tests.ts | V1 only, no UT |
| 6 | PaymentMethodsPerProviderList | -- | -- | May be obsolete |

## Payment Methods — V2 (Mezzanine)

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 7 | PaymentMethodsListV2 | PaymentMethodsListV2-tests.tsx (14) | billing-settings-v2-tests.ts | Well covered |
| 8 | PaymentMethodV2 | PaymentMethodV2-tests.tsx (26) | billing-settings-v2-tests.ts | Well covered |
| 9 | PaymentMethodsPerProviderModal | PaymentMethodsPerProviderModal-tests.tsx (21) | billing-settings-v2-tests.ts | Includes search (BILL-486) |
| 10 | EditBillingContactInfoModal | EditBillingContactInfoModal-tests.tsx (14) | billing-settings-v2-tests.ts | NEW: address + email in one modal |

## Modals — Payment Methods

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 11 | AddCreditCardModal | AddCreditCardModal-tests.tsx (12) | billing-settings-page-tests.ts | UT covers validation |
| 12 | AddAchModal | AddAchModal-tests.tsx (9) | billing-settings-page-tests.ts | UT covers validation |
| 13 | AddPaymentMethodModal | -- | billing-settings-page-tests.ts | V1 modal selector, no UT |
| 14 | AddPaymentMethodModalV2 | AddPaymentMethodModalV2-tests.tsx (16) | billing-settings-v2-tests.ts | NEW: comprehensive V2 coverage |
| 15 | DeletePaymentMethodConfirmationModal | -- | billing-settings-page-tests.ts | V1, no UT |
| 16 | DeletePaymentMethodConfirmationModalV2 | DeletePaymentMethodConfirmationModalV2-tests.tsx (5) | billing-settings-v2-tests.ts | NEW: V2 confirmation |

## Modals — Billing Info

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 17 | EditBillingEmailModal | EditBillingEmailModal-tests.tsx (2) | billing-settings-page-tests.ts | V1 only |
| 18 | EditBusinessAddressModal | EditBusinessAddressModal-tests.tsx (9) | billing-settings-page-tests.ts | V1 only |
| 19 | EditMonthlyLimitModal | EditMonthlyLimitModal-tests.tsx (3) | billing-settings-page-tests.ts | V1 only |
| 20 | EditMonthlyLimitModalV2 | EditMonthlyLimitModalV2-tests.tsx (11) | billing-settings-v2-tests.ts | NEW: enhanced V2 |
| 21 | EditRolloversModal | EditRolloversModal-tests.tsx (2) | billing-settings-page-tests.ts | V1 only |
| 22 | EditRolloversModalV2 | EditRolloversModalV2-tests.tsx (12) | billing-settings-v2-tests.ts | NEW: enhanced V2 |
| 23 | BillingCompletionModal | -- | billing-settings-page-tests.ts | Onboarding modal, no UT |

## Invoice Views

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 24 | FpbInvoiceView (legacy) | FpbInvoiceView-tests.tsx (22) | invoice-details-page-tests.ts | Original version |
| 25 | FpbInvoiceView (v2) | FpbInvoiceView-tests.tsx (28) | invoice-details-page-tests.ts | NEW: healthcare platforms (BILL-343), numApiBookings |
| 26 | LegacyInvoiceView | LegacyInvoiceView-tests.tsx (12) | -- | **OBSOLETE** - flag torn down (a88b14cba6) |
| 27 | FeaturedProviderSection | FeaturedProviderSection-tests.tsx (7) | invoice-details-page-tests.ts | Provider fee breakdown |
| 28 | LicenseFeeSection | LicenseFeeSection-tests.tsx (5) | -- | License fee display |
| 29 | PatientBookingsSection | PatientBookingsSection-tests.tsx (7) | invoice-details-page-tests.ts | Patient bookings breakdown |
| 30 | TaxesAndFeesSection | TaxesAndFeesSection-tests.tsx (6) | -- | NEW: tax/fee calculations |

## Billing Contact Info

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 31 | BillingContactInfo | BillingContactInfo-tests.tsx (13) | billing-settings-v2-tests.ts | Contact display + edit |
| 32 | BusinessAddress | -- | -- | Presentational, tested via parent |
| 33 | BillingEmail | -- | -- | Presentational, tested via parent |
| 34 | BillStatusLabel | -- | -- | Status badge, simple mapping |

## Pricing

| # | Component | UT | CY | Notes |
|---|-----------|----|----|-------|
| 35 | PricingInformation | PricingTab-tests.tsx (2) | -- | V1 pricing |
| 36 | PricingInformationV2 | PricingInformationV2-tests.tsx (23) | billing-pricing-v2-tests.ts | NEW: BILL-580 FAQs visibility |
| 37 | YearlyValueCalcModal (legacy) | -- | billing-settings-page-tests.ts | V1, no UT |
| 38 | YearlyValueCalcModalV2 | YearlyValueCalcModalV2-tests.tsx (17) | billing-settings-v2-tests.ts | NEW: step navigation + calculation |

## Utilities & Hooks

| # | File | UT | Notes |
|---|------|----|-------|
| 39 | apiCalls.ts | apiCalls-tests.ts (25) | All 10 API functions covered |
| 40 | invoiceHelpers.ts | -- | **GAP: 3 functions untested** |
| 41 | SkuTitleMap.ts | SkuTitleMap-tests.ts (2) | SKU display mapping |
| 42 | billingDateUtils.ts | billingDateUtils-tests.ts (6) | Date utilities |
| 43 | schemaBuilder.ts | -- | **GAP: 7 schemas indirect only** |
| 44 | shouldUseStripeSandbox.ts | useShouldUseStripeSandbox-tests.ts (6) | Stripe sandbox logic |
| 45 | usePracticeBillingSettings hook | usePracticeBillingSettings-tests.ts (3) | Data fetching |
| 46 | useBillingToast hook | useBillingToast-tests.ts (8) | NEW: toast notifications |

---

## Coverage Summary (Snapshot)

| Category | Total | With UT | With CY | With Both | With Neither |
|----------|-------|---------|---------|-----------|--------------|
| Containers/Pages | 3 | 3 | 2 | 1 | 0 |
| Payment Methods (V1 + V2) | 7 | 3 | 6 | 3 | 1 |
| Modals (Payment) | 6 | 5 | 6 | 5 | 0 |
| Modals (Billing Info) | 7 | 6 | 6 | 5 | 1 |
| Invoice Views | 6 | 5 | 3 | 2 | 0 |
| Contact Info | 4 | 1 | 1 | 1 | 2 |
| Pricing | 4 | 3 | 2 | 2 | 1 |
| Utilities/Hooks | 7 | 5 | 0 | 0 | 2 |
| **Total** | **44** | **31 (70%)** | **26 (59%)** | **19 (43%)** | **7 (16%)** |

---

## Recent Changes (Since 2026-04-14)

| Completed | Tests Added | Notes |
|-----------|------------|-------|
| BillsContainer | 21 | Was P0 gap, now fully tested |
| YearlyValueCalcModalV2 | 17 | Was P0 gap, now fully tested |
| AddPaymentMethodModalV2 | 16 | New V2 variant |
| EditBillingContactInfoModal | 14 | Was P1 gap, now fully tested |
| EditMonthlyLimitModalV2 | 11 | Enhanced from V1 (3 tests) |
| EditRolloversModalV2 | 12 | Enhanced from V1 (2 tests) |
| DeletePaymentMethodConfirmationModalV2 | 5 | New V2 variant |
| FpbInvoiceView (v2) | 28 | Enhanced with BILL-343 (healthcare platforms) |
| PaymentMethodsPerProviderModal | 21 | Enhanced with BILL-486 (search) |
| PricingInformationV2 | 23 | Enhanced with BILL-580 (FAQs) |
| TaxesAndFeesSection | 6 | New component |
| useBillingToast | 8 | New hook (BILL-575) |
| BillingContactInfo | 13 | Enhanced |
