# Master Test Inventory — Billing Domain (2026-04-23)

Complete count of every test, organized by type.

---

## Test Counts at a Glance

| Test Type | Files | Test Cases | Lines of Code |
|-----------|-------|------------|---------------|
| Unit Tests (Jest + RTL) | 33 | ~365 | 8,977 |
| Cypress E2E Tests | 6 | 96 | 2,946 |
| **Total** | **39** | **~461** | **11,923** |

---

## Unit Tests by Category

### Form Validation & Modals (~100 tests)

| Test File | Tests | What It Validates |
|-----------|-------|-------------------|
| AddAchModal-tests.tsx | 9 | Account holder name, bank name, routing number, account number |
| AddCreditCardModal-tests.tsx | 12 | Card name, address fields, zip code, Stripe key selection |
| AddPaymentMethodModalV2-tests.tsx | 16 | Payment type selector (Credit Card / ACH), routing to correct sub-modal |
| EditBillingEmailModal-tests.tsx | 2 | Email required + format |
| EditBusinessAddressModal-tests.tsx | 9 | Address1, address2, city, state, zip code |
| EditMonthlyLimitModal-tests.tsx | 3 | Non-numbers, floats, minimum limit |
| EditMonthlyLimitModalV2-tests.tsx | 11 | V2 variant: enhanced validation, error states |
| EditRolloversModal-tests.tsx | 2 | Rollover requirement validation |
| EditRolloversModalV2-tests.tsx | 12 | V2 variant: advanced rollover scenarios |
| DeletePaymentMethodConfirmationModalV2-tests.tsx | 5 | Confirmation dialog, cancel/confirm buttons |

### Component Rendering (~120 tests)

| Test File | Tests | What It Renders |
|-----------|-------|-----------------|
| BillingContactInfo-tests.tsx | 13 | Address display, email display, edit button visibility |
| BillingSettingsContainer-tests.tsx | 4 | Tab visibility, coachmarks, experiment flags |
| FeaturedProviderSection-tests.tsx | 7 | Single/multi provider fees, expand/collapse |
| FpbInvoiceView-tests.tsx (legacy) | 22 | PDF links, totals, payments, credits, status messages |
| FpbInvoiceView-tests.tsx (v2) | 28 | Healthcare platforms row, numApiBookings, paid vs free breakdown |
| InvoiceDetailsContainer-tests.tsx | 14 | Loading/error states, routing between V1/V2, PDF URL generation |
| LegacyInvoiceView-tests.tsx | 12 | (OBSOLETE) Table headers, line items, totals |
| LicenseFeeSection-tests.tsx | 5 | Fee display, expand/collapse, date range |
| PatientBookingsSection-tests.tsx | 7 | Multi-provider bookings, expand/collapse |
| PricingTab-tests.tsx | 2 | SKU-dependent pricing visibility |
| PricingInformationV2-tests.tsx | 23 | V2 pricing display, feature flag FAQs visibility (BILL-580) |
| TaxesAndFeesSection-tests.tsx | 6 | Tax and fee calculations, display |

### Payment Methods — V2 (Mezzanine) (~60 tests)

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| PaymentMethodsListV2-tests.tsx | 14 | Payment list rendering, add/delete buttons, modals, links |
| PaymentMethodV2-tests.tsx | 26 | Payment display, menu items, API calls, default/delete behavior |
| PaymentMethodsPerProviderModal-tests.tsx | 21 | Modal rendering, provider list, dropdown, search functionality (BILL-486) |

### API & Integration (~50 tests)

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| apiCalls-tests.ts | 25 | All 10 API functions: success + error paths |
| useBillingToast-tests.ts | 8 | Toast notifications (BILL-575) |
| usePracticeBillingSettings-tests.ts | 3 | Hook: null practiceId, success, error |
| useShouldUseStripeSandbox-tests.ts | 6 | Stripe sandbox feature flag + entity flag combinations |

### Business Logic (~40 tests)

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| billingDateUtils-tests.ts | 6 | Date formatting, future invoice detection |
| BillsContainer-tests.tsx | 21 | Invoice list rendering, filtering, empty state, analytics |
| SkuTitleMap-tests.ts | 2 | SKU type → display title mapping |
| YearlyValueCalcModalV2-tests.tsx | 17 | Step navigation, validation, calculation formula, edge cases |

### Utilities (No Direct Tests)

| Utility | Tests | Status |
|---------|-------|--------|
| invoiceHelpers.ts | 0 | **GAP: 3 functions untested** |
| schemaBuilder.ts | 0 | **GAP: 7 schemas tested only indirectly** |

### SKU Services (provider-home-webapp) (~50 tests)

| Test File | Tests | What It Tests |
|-----------|-------|---------------|
| skuService-test.ts | ~25 | SKU updates, task status transitions |
| skuValidator-tests.ts | ~20 | SKU activation/selection/enrollment status |

---

## Cypress E2E Tests (2026-04-23)

| Spec File | Tests | Lines | Purpose |
|-----------|-------|-------|---------|
| billing-invoice-summary-tests.ts | 18 | 182 | Invoice summary page (NEW) |
| billing-pricing-v2-tests.ts | 10 | 193 | V2 pricing with FAQs (NEW, BILL-580) |
| billing-settings-page-commands.ts | 4 | 326 | Custom test setup commands (infrastructure) |
| billing-settings-page-tests.ts | 35 | 1,254 | V1 (Legacy) UI tests |
| billing-settings-v2-tests.ts | 25 | 927 | V2 (Mezzanine) UI tests |
| invoice-details-page-tests.ts | 4 | 64 | Invoice detail page navigation |
| **Total** | **96** | **2,946** | — |

### Supporting Cypress Infrastructure

| File | Purpose |
|------|---------|
| billing-settings-page-commands.ts | Custom commands for experiment setup, mock data, navigation |
| BillingSettingsPagePageObject.ts | Page object for contact info verification |
| EditBillingContactInfoModalPageObject.ts | Page object for billing contact modal |
| selectors.ts (lines 42-205) | 14 selector groups for billing elements |
| mocks.ts | 6 mock data objects (payment methods, invoices) |

---

## Test Coverage Summary

| Category | Total Components | With Unit Tests | With Cypress | With Both | With Neither |
|----------|------------------|-----------------|--------------|-----------|-------------|
| Containers/Pages | 4 | 3 | 2 | 1 | 0 |
| Payment Methods V1 | 3 | 0 | 2 | 0 | 1 |
| Payment Methods V2 | 4 | 3 | 4 | 3 | 0 |
| Modals (V1 + V2) | 10 | 9 | 8 | 7 | 0 |
| Invoice Views | 5 | 5 | 2 | 2 | 0 |
| Contact Info | 4 | 2 | 1 | 1 | 1 |
| Utilities/Hooks | 7 | 5 | 0 | 0 | 2 |
| **Total** | **37** | **27 (73%)** | **19 (51%)** | **14 (38%)** | **4 (11%)** |

---

## Source Files Without Any Tests

Only 4 components have **zero** unit tests AND zero direct Cypress coverage:

| Component | File | Why It Matters |
|-----------|------|----------------|
| invoiceHelpers | `invoiceHelpers.ts` | **3 exported functions** — date formatting + status normalization |
| schemaBuilder | `utils/schemaBuilder.ts` | **7 Yup validation schemas** — tested only indirectly via modals |
| BusinessAddress | `BusinessAddress.tsx` | Presentational, tested indirectly via BillingContactInfo |
| BillingEmail | `BillingEmail.tsx` | Presentational, tested indirectly via parent |
