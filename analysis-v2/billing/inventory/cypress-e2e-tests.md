# Cypress E2E Test Catalog — Billing Domain (2026-04-23)

Complete spec breakdown with test counts, custom commands, page objects, and selectors.

---

## E2E Test Specs Summary

| Spec | Tests | Lines | Focus Area | Status |
|------|-------|-------|-----------|--------|
| billing-invoice-summary-tests.ts | 18 | 182 | Invoice summary page | NEW |
| billing-pricing-v2-tests.ts | 10 | 193 | V2 pricing + FAQs (BILL-580) | NEW |
| billing-settings-page-tests.ts | 35 | 1,254 | V1 (Legacy) UI | Active, may be obsolete |
| billing-settings-v2-tests.ts | 25 | 927 | V2 (Mezzanine) UI | Active, primary |
| invoice-details-page-tests.ts | 4 | 64 | Invoice detail routing | Basic |
| **Subtotal** | **92** | **2,620** | | |
| billing-settings-page-commands.ts | 4 | 326 | Infrastructure | Commands/setup |
| **Total** | **96** | **2,946** | | |

---

## Spec Details

### billing-invoice-summary-tests.ts (NEW)

**Purpose:** Test invoice summary page display (BILL-558, BILL-343)

**Test Coverage (18 tests):**
- Healthcare platforms row visibility
- API bookings count display
- Summary totals calculation
- Empty states
- Loading states
- Error handling
- Feature flag variants (showApiPartnerBookings toggle)

**Key assertions:**
- Conditional rendering based on showApiPartnerBookings flag
- numApiBookings field properly displayed
- Row visibility for different practice types

---

### billing-pricing-v2-tests.ts (NEW)

**Purpose:** Test V2 pricing information page with FAQs (BILL-580)

**Test Coverage (10 tests):**
- Marketplace enrollment visibility
- FAQs section show/hide based on SKU selection
- FAQs hidden when no Marketplace enrollment
- Contact us footer visibility
- Empty state display
- Feature flag control (BILL-580 logic)

**Key assertions:**
- Hide FAQs when not enrolled in Marketplace
- Hide FAQs when no SKUs selected
- Show contact-us footer to PricingInformationV2

---

### billing-settings-page-tests.ts (V1 Legacy)

**Purpose:** Test V1 (Legacy) billing settings UI

**Test Count (35 tests):**
- Payment method management (add, set default, delete)
- Billing contact info editing (email, address)
- Monthly limit + rollover editing
- Form validation
- Error handling
- Modal interactions
- Pricing calculator navigation

**Coverage Breakdown:**
- Add payment methods: Credit Card, ACH
- Set/remove default payment
- Delete payment method with confirmation
- Update billing email (validation)
- Update business address (validation)
- Edit monthly limit
- Edit rollovers
- View pricing calculator (6-step navigation)
- Error states and toasts

**Status:** May be redundant with V2 tests if `SHOW_NEW_BILLING_MEZZ_REVAMP` is fully rolled out.

---

### billing-settings-v2-tests.ts (V2 Mezzanine)

**Purpose:** Test V2 (Mezzanine) billing settings UI

**Test Count (25 tests):**
- All payment method operations (V2 variants)
- Billing contact info combined modal
- Monthly limit editing (V2)
- Rollover editing (V2)
- Search in payment method by provider modal (BILL-486)
- Error handling
- Modal interactions
- Toast notifications (BILL-575)

**Coverage Breakdown:**
- Rollover editing (12 tests)
- Monthly limit (8 tests)
- Billing contact info (8 tests)
- Payment methods (13 tests including search)
- Overall interactions (~25 total)

---

### billing-settings-page-commands.ts (Infrastructure)

**Purpose:** Custom Cypress commands for test setup and data mocking

**4 Custom Commands:**
1. `givenBillingPageExperiments` — Set experiment flags
2. `givenBillingPageMocks` — Mock API responses
3. `thenBillingPageRenders` — Assert page loaded
4. `andNavigateToBillingPage` — Navigate + wait for load

**Mock Data Sets:**
- Payment methods (Credit Card, ACH)
- Practice billing settings
- Invoice data
- Experiment assignments

---

### invoice-details-page-tests.ts

**Purpose:** Test invoice detail page routing and display

**Test Count (4 tests):**
- Navigate to invoice detail
- Verify FpbInvoiceView renders
- Verify invoice data loads
- Handle loading/error states

**Simple spec** — covers basic navigation and routing. Detailed invoice rendering covered by FpbInvoiceView unit tests.

---

## Supporting Infrastructure

### Page Objects

| File | Purpose |
|------|---------|
| BillingSettingsPagePageObject.ts | Query billing settings page elements |
| EditBillingContactInfoModalPageObject.ts | Query contact info modal elements |

**Pattern:** Encapsulate selectors and common interactions (fill form, submit, etc.)

### Selectors (selectors.ts)

**Billing selector groups (lines 42-205):**
1. Contact info section
2. Payment methods section
3. Monthly limit section
4. Rollovers section
5. Pricing information section
6. Form fields
7. Buttons/controls
8. Modals
9. Success/error messages
10. Tabs
11. Loading states
12. Empty states
13. Invoice sections
14. Healthcare platforms row (new)

**Total:** 14 selector groups, ~160 lines

### Mock Data (mocks.ts)

**6 mock data objects:**
1. Payment method (Credit Card)
2. Payment method (ACH)
3. Practice billing settings
4. Invoice summary
5. Invoice details
6. API response wrappers

---

## Test Execution Notes

### Command to Run Cypress Tests

```bash
yarn workspace settings cypress run --spec "cypress/e2e/PracticeSettingsPages/billing-*.ts"
```

### Expected Runtime

- Full suite: ~5-8 minutes (headless)
- V1 tests alone: ~2-3 minutes
- V2 tests alone: ~2-3 minutes
- Invoice tests: ~30 seconds

### Environment Setup (beforeEach)

1. Set cookies for experiments
2. Set `SHOW_NEW_BILLING_MEZZ_REVAMP` (ON for v2 tests, OFF for v1)
3. Mock API endpoints
4. Set viewport (macbook-16)
5. Navigate to billing page
6. Wait for data load

---

## Recent Changes (Since 2026-04-14)

| Spec | Change | Tests Added | Commits |
|------|--------|-------------|---------|
| billing-invoice-summary-tests.ts | NEW | 18 | BILL-343, BILL-558 |
| billing-pricing-v2-tests.ts | NEW | 10 | BILL-580 |
| billing-settings-v2-tests.ts | Enhanced | +4 | BILL-486 (search) |
| billing-settings-page-tests.ts | Unchanged | 0 | Stable |
| invoice-details-page-tests.ts | Unchanged | 0 | Stable |

**Total new tests since last analysis: +32 Cypress tests**

