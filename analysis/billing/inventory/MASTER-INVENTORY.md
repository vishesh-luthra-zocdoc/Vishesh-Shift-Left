# Master Test Inventory — Billing Domain

A complete count of every test, organized by type.

---

## Test Counts at a Glance

| Test Type | Files | Test Cases | Lines of Code |
|-----------|-------|------------|---------------|
| Unit Tests (Jest + RTL) | 25 | ~265 | — |
| Cypress E2E Tests | 3 | 31 | 1,900 |
| **Total** | **28** | **~296** | — |

---

## Unit Tests by Category

### Form Validation (~45 tests)
Tests that check form field requirements, format rules, and length limits.

| Test File | Tests | What It Validates |
|-----------|-------|-------------------|
| AddAchModal-tests.tsx | 8 | Account holder name, bank name, routing number (9 digits), account number (max 20) |
| AddCreditCardModal-tests.tsx | 12 | Card name, address fields, zip code (5 digits), Stripe key selection |
| EditBillingEmailModal-tests.tsx | 2 | Email required + format |
| EditBusinessAddressModal-tests.tsx | 8 | Address1, address2 (150 char max), city (50 char max), zip code (5 digits) |
| EditMonthlyLimitModal-tests.tsx | 3 | Non-numbers, floats, minimum limit from feature flag |
| EditRolloversModal-tests.tsx | 2 | Rollover requirement when limit set, last rollover restriction |

### Component Rendering (~80 tests)
Tests that check if components display the right content.

| Test File | Tests | What It Renders |
|-----------|-------|-----------------|
| BillingContactInfo-tests.tsx | 11 | Address display, email display, edit button visibility |
| BillingSettingsContainer-tests.tsx | 4 | Tab visibility, coachmark tutorial steps |
| FeaturedProviderSection-tests.tsx | 7 | Single/multi provider fees, expand/collapse, sorting |
| FpbInvoiceView-tests.tsx | 22 | PDF links, totals, payments, credits, status messages, paid vs free experiment |
| InvoiceDetailsContainer-tests.tsx | 9 | Loading/error states, FPB vs Legacy routing, PDF URL generation |
| LegacyInvoiceView-tests.tsx | 12 | Table headers, line items, totals, disclaimers, print |
| LicenseFeeSection-tests.tsx | 5 | Fee display, expand/collapse, date range, sales tax |
| PatientBookingsSection-tests.tsx | 7 | Multi-provider bookings, expand/collapse, sorting |
| PricingTab-tests.tsx | 2 | SKU-dependent pricing visibility |
| PaymentMethodsListV2-tests.tsx | 11 | Payment list rendering, buttons, modals, links |
| PaymentMethodV2-tests.tsx | 22 | Payment display, menu items, API calls, default/delete behavior |
| PaymentMethodsPerProviderModal-tests.tsx | 5 | Modal rendering, provider list, dropdown, API calls |

### API & Integration (~50 tests)
Tests for API client functions and data fetching hooks.

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| apiCalls-tests.ts | 26 | All 10 API functions: success + error paths for each |
| usePracticeBillingSettings-tests.ts | 3 | Hook: null practiceId, success fetch, error state |
| useShouldUseStripeSandbox-tests.ts | 6 | Stripe sandbox: feature flag + test practice + entity flag combinations |

### Business Logic (~20 tests)
Tests for utility functions and data transformations.

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| billingDateUtils-tests.ts | 12 | Date formatting, future invoice detection, legacy title generation |
| SkuTitleMap-tests.ts | 5 | SKU type → display title mapping |

### SKU Services (provider-home-webapp) (~50 tests)
Tests for SKU management outside the main billing settings area.

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| skuService-test.ts | ~25 | SKU updates, task status transitions for ClaimYourProfile |
| skuValidator-tests.ts | ~20 | SKU activation/selection/enrollment status checking |

---

## Cypress E2E Tests

| Spec File | Tests | Lines | Version |
|-----------|-------|-------|---------|
| billing-settings-page-tests.ts | 33 | 1,208 | V1 (Legacy UI) |
| billing-settings-v2-tests.ts | 13 | 628 | V2 (Mezzanine UI) |
| invoice-details-page-tests.ts | 2 | 64 | — |
| **Total** | **48** | **1,900** | — |

### Supporting Cypress Infrastructure

| File | Purpose |
|------|---------|
| billing-settings-page-commands.ts | 8 custom commands for test setup |
| BillingSettingsPagePageObject.ts | Page object for contact info verification |
| EditBillingContactInfoModalPageObject.ts | Page object for billing contact modal |
| selectors.ts (lines 42-205) | 14 selector groups for billing elements |
| mocks.ts | 6 mock data objects (payment methods, invoices, etc.) |

---

## Source Files Without Any Tests

These 12 components have **zero** unit tests AND zero direct Cypress coverage:

| Component | File | Why It Matters |
|-----------|------|----------------|
| YearlyValueCalcModal | `YearlyValueCalcModal/index.tsx` | Pricing calculator — shows money to providers |
| StepContent | `YearlyValueCalcModal/StepContent.tsx` | Calculator step UI |
| ResultContent | `YearlyValueCalcModal/ResultContent.tsx` | Calculator result display |
| steps config | `YearlyValueCalcModal/steps.ts` | Calculator validation + step config |
| BillsContainer | `BillsContainer.tsx` | Invoice list rendering |
| AddPaymentMethodModal | `AddPaymentMethodModal.tsx` | Payment type selector |
| DeletePaymentMethodConfirmationModal | `DeletePaymentMethodConfirmationModal.tsx` | Delete confirmation |
| BillingCompletionModal | `BillingCompletionModal.tsx` | Onboarding completion |
| EditBillingContactInfoModal | `EditBillingContactInfoModal.tsx` | V2 contact info editor |
| BusinessAddress | `BusinessAddress.tsx` | Address display (presentational) |
| BillingEmail | `BillingEmail.tsx` | Email display (presentational) |
| BillStatusLabel | `BillStatusLabel.tsx` | Status badge (presentational) |
| invoiceHelpers | `invoiceHelpers.ts` | Date/status formatting functions |
| schemaBuilder | `utils/schemaBuilder.ts` | 7 Yup validation schemas |
