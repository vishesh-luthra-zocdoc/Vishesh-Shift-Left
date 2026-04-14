# Test Coverage Gaps — Billing Domain

Prioritized list of missing test coverage. P0 = fix now, P3 = fix when convenient.

---

## P0 — Critical (Business Logic With No Tests)

These are the scariest gaps. If something breaks here, we find out in production.

### 1. YearlyValueCalcModal — Pricing Calculator (6 files, ZERO tests)

| File | What It Does |
|------|-------------|
| `YearlyValueCalcModal/index.tsx` | Multi-step modal calculating yearly value |
| `YearlyValueCalcModal/steps.ts` | Step definitions + validation schemas |
| `YearlyValueCalcModal/StepContent.tsx` | Individual step rendering |
| `YearlyValueCalcModal/ResultContent.tsx` | Calculated result display |
| `YearlyValueCalcModal/Common.ts` | Calculation utilities |
| `YearlyValueCalcModal/types.ts` | TypeScript types |

**Why it matters:** This calculates pricing shown to providers. If the formula is wrong, providers see incorrect ROI numbers. The calculation logic is pure functions — very easy to unit test.

**What to test:**
- Calculation formula with known inputs → expected outputs
- Step navigation (forward/backward)
- Field validation per step
- Edge cases (zero inputs, large numbers)

**Effort:** ~2 hours

### 2. invoiceHelpers.ts — 3 Exported Functions, Zero Tests

| Function | What It Does |
|----------|-------------|
| `formatDate` | Formats YYYY-MM-DD to "Mon DD, YYYY" |
| `getLastDayOfMonth` | Returns last day of a given month |
| `capitalizeStatus` | Normalizes bill status strings |

**Why it matters:** Date formatting bugs = wrong invoice dates displayed to providers. `capitalizeStatus` handles status normalization — if it breaks, invoice status labels show wrong text.

**What to test:** These are pure functions. Give inputs, check outputs. 10 minutes of work.

**Effort:** ~30 minutes

---

## P1 — High Priority (Important Logic, Should Test Soon)

### 3. EditBillingContactInfoModal (V2) — No Unit Test

**What it does:** Combines business address + billing email editing in a single V2 modal with 2 separate API calls (`updatePrimaryBusinessAddress` + `updatePracticeBillingEmail`).

**Why it matters:** This is the V2 replacement for the separate address/email modals. It's the modal users actually see if V2 is rolled out. Has form validation + error handling for 2 independent API calls.

**What to test:**
- Form prepopulation from context
- Validation (address1 required, email format, zip code)
- Successful save (both APIs called)
- Partial failure (one API succeeds, other fails)
- Error message display

**Effort:** ~2 hours

### 4. BillsContainer — No Unit Test

**What it does:** Renders the list of invoices/bills. Filters out future invoices using `isFutureInvoice`. Handles empty state. Tracks bill clicks for analytics.

**Why it matters:** If filtering logic breaks, providers might see future (empty) invoices, or miss current ones.

**What to test:**
- Renders bill list from props
- Filters out future invoices
- Shows empty state when no bills
- Click handler fires with correct bill ID

**Effort:** ~1 hour

### 5. schemaBuilder.ts — 7 Yup Schemas, Only Indirectly Tested

**What it does:** Defines Yup validation schemas for all billing forms:
1. Email validation schema
2. Business address schema
3. Credit card schema
4. ACH schema
5. Monthly limit schema (with feature flag minimum)
6. Contact info schema (V2)
7. Rollover schema

**Why it matters:** These schemas are currently tested only through modal component tests — if a modal test passes, we assume the schema works. But schema edge cases (boundary values, special characters) aren't covered.

**What to test:** Direct schema validation with known inputs. Each schema is a pure function.

**Effort:** ~2 hours

### 6. DeletePaymentMethodConfirmationModal — No Unit Test

**What it does:** Shows confirmation dialog before deleting a payment method. Has confirm + cancel buttons.

**Why it matters:** Low complexity, but it's the last gate before a destructive action (deleting a payment method). Worth having a basic test.

**What to test:**
- Renders confirmation message
- Cancel button calls onCancel
- Confirm button calls onConfirm

**Effort:** ~30 minutes

---

## P2 — Medium Priority

### 7. AddPaymentMethodModal — No Unit Test

**What it does:** Dropdown to select payment method type (Credit Card or ACH), then opens the appropriate sub-modal.

**Why it matters:** Simple routing logic. Covered by Cypress but no unit test.

**Effort:** ~30 minutes

### 8. BillingCompletionModal — No Unit Test

**What it does:** Congratulations modal after completing billing setup. Redirects to homepage.

**Why it matters:** Only shown during onboarding. Low risk.

**Effort:** ~30 minutes

### 9. PDF Download Endpoint — No Tests Anywhere

**Endpoint:** `GET /api/provider/v1/invoices` (mapped as `GET_INVOICE_PDF_DOWNLOAD_URL`)

**What it does:** Returns PDF file for invoice download.

**Why it matters:** The endpoint exists in routes and server handlers but has no unit test in `apiCalls-tests.ts` and no Cypress intercept. If PDF generation breaks, we won't catch it.

**Effort:** ~1 hour

### 10. getSkuMappings GraphQL Query — No Tests

**What it does:** Fetches SKU mappings for pricing display.

**Why it matters:** Used in PricingInformation component. Only test if modifying pricing logic.

**Effort:** ~1 hour

---

## P3 — Low Priority (Presentational, Low Risk)

| Component | Why It's OK |
|-----------|------------|
| BusinessAddress.tsx | Purely presentational. Tested indirectly via BillingContactInfo parent. |
| BillingEmail.tsx | Purely presentational. Tested indirectly via parent. |
| BillStatusLabel.tsx | Simple status→tag mapping. 5 lines of logic. |
| V1 PaymentMethodsList.tsx | May be dead code if V2 fully rolled out. Don't invest in tests. |
| V1 PaymentMethod.tsx | Same — may be dead code. |
| V1 PaymentMethodsPerProviderList.tsx | Same — may be dead code. No tests exist. |

---

## Shift-Left Opportunities

These Cypress tests could be replaced with faster unit tests:

| What Cypress Tests | Why Unit Tests Are Better |
|--------------------|--------------------------|
| Form validation (email format, zip code, required fields) | Already covered in unit tests — Cypress re-tests the same rules, slower |
| Modal open/close behavior | Button click → modal appears is faster in RTL |
| Error message display after API failure | Check error message rendering in unit test |
| Pricing calculator 6-step navigation | Step logic is testable without browser automation |

**If shifted left, we could reduce Cypress runtime without losing coverage.**
