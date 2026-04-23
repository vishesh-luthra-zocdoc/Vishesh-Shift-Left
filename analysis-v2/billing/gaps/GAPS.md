# Test Coverage Gaps — Billing Domain (2026-04-23)

Prioritized list of remaining missing test coverage.

---

## P0 — Critical (Business Logic With No Tests)

### 1. invoiceHelpers.ts — 3 Exported Functions, Zero Tests

**File:** `apps/settings/src/pages/settingsPages/billingSettings/invoiceHelpers.ts`

| Function | What It Does | Usage |
|----------|-------------|-------|
| `formatDate` | Converts YYYY-MM-DD to "Mon DD, YYYY" | FpbInvoiceView, v2/FpbInvoiceView |
| `getLastDayOfMonth` | Returns last day of a given month | InvoiceDetailsContainer |
| `capitalizeStatus` | Normalizes bill status strings | FpbInvoiceView |

**Why it matters:** Date formatting bugs = wrong invoice dates displayed to providers. These are pure functions — trivial to test but critical for correctness.

**Test plan:**
- formatDate: Known inputs → expected outputs (e.g., "2026-04-23" → "Apr 23, 2026")
- getLastDayOfMonth: Each month + leap year edge cases
- capitalizeStatus: Status normalization (e.g., "pending" → "Pending")

**Effort:** 45 minutes
**Risk if not fixed:** Medium (data formatting bugs are subtle but high-impact in production)

---

## P1 — High Priority (Important Logic, Should Test Soon)

### 2. schemaBuilder.ts — 7 Yup Schemas, Only Indirectly Tested

**File:** `apps/settings/src/pages/settingsPages/billingSettings/utils/schemaBuilder.ts`

**7 schemas defined:**
1. `editBillingEmailModalSchema` — Email validation
2. `editBusinessAddressModalSchema` — Address validation
3. `addCreditCardModalSchema` — Credit card validation
4. `addAchModalSchema` — ACH validation
5. `editMonthlyLimitModalSchema` — Monthly limit + feature flag minimum
6. `editBillingContactInfoModalSchema` — V2 combined address + email
7. `editRolloversModalSchema` — Rollover validation

**Current testing:** Only tested indirectly through modal component tests. Edge cases not covered:
- Boundary values (min/max field lengths)
- Special characters in address/name fields
- Email format edge cases (+ addressing, subdomains)
- Exact validation error messages

**Why it matters:** If a schema is wrong, users can submit invalid data or see incorrect validation messages. Schema bugs are hard to catch without direct testing.

**Test plan:**
- Direct schema validation with `.validate()` calls
- Known valid inputs → should pass
- Known invalid inputs → should fail with specific error messages
- Boundary values (e.g., 150 char address limit)

**Effort:** 2 hours
**Risk if not fixed:** Medium-High (validation bugs surface in production)

---

### 3. AddPaymentMethodModal (V1) — No Unit Test

**File:** `apps/settings/src/pages/settingsPages/billingSettings/AddPaymentMethodModal.tsx`

**What it does:** Dropdown to select payment method type (Credit Card or ACH), then routes to appropriate sub-modal.

**Current testing:** Only Cypress test (billing-settings-page-tests.ts). No unit test.

**Note:** V2 variant (AddPaymentMethodModalV2) is fully tested (16 tests). If `SHOW_NEW_BILLING_MEZZ_REVAMP` is still running, V1 may still be in use.

**Why it matters:** If experiment is still active, this is a gap. If experiment is fully rolled out, this component is dead.

**Test plan:**
- Modal renders correctly
- Click "Credit Card" routes to AddCreditCardModal
- Click "ACH" routes to AddAchModal
- Close button works

**Effort:** 30 minutes (but only if V1 still in use)
**Risk if not fixed:** Low (only if `SHOW_NEW_BILLING_MEZZ_REVAMP` still running)

---

### 4. BillingCompletionModal — No Unit Test

**File:** `apps/settings/src/pages/settingsPages/billingSettings/BillingCompletionModal.tsx`

**What it does:** Congratulations modal after completing billing setup. Shows message, then redirects to homepage on button click.

**Current testing:** Cypress test (billing-settings-page-tests.ts) only checks show/hide. No unit test.

**Why it matters:** Low complexity, but it's user-facing. Worth having a basic test.

**Test plan:**
- Renders completion message
- Button click triggers redirect callback
- Modal closes on action

**Effort:** 30 minutes
**Risk if not fixed:** Very Low (simple modal, low interaction complexity)

---

## P2 — Medium Priority

### 5. BusinessAddress.tsx — No Unit Test

**File:** `apps/settings/src/pages/settingsPages/billingSettings/BusinessAddress.tsx`

**What it does:** Display-only component showing business address (address1, address2, city, state, zip).

**Current testing:** Tested indirectly via BillingContactInfo parent.

**Why it matters:** Purely presentational. Low risk.

**Effort:** 15 minutes (if added for completeness)
**Risk if not fixed:** Very Low

---

### 6. BillingEmail.tsx — No Unit Test

**File:** `apps/settings/src/pages/settingsPages/billingSettings/BillingEmail.tsx`

**What it does:** Display-only component showing billing email.

**Current testing:** Tested indirectly via BillingContactInfo parent.

**Why it matters:** Purely presentational. Low risk.

**Effort:** 15 minutes (if added for completeness)
**Risk if not fixed:** Very Low

---

### 7. BillStatusLabel.tsx — No Unit Test

**File:** `apps/settings/src/pages/settingsPages/billingSettings/BillStatusLabel.tsx`

**What it does:** Simple status → badge/label mapping (e.g., "pending" → warning badge).

**Current testing:** Tested indirectly via invoice view tests.

**Why it matters:** Simple logic. Low risk.

**Effort:** 15 minutes (if added for completeness)
**Risk if not fixed:** Very Low

---

## Shift-Left Opportunities

These Cypress tests could be replaced with faster unit tests:

| Cypress Test | Unit Test Alternative | Benefit |
|--------------|----------------------|---------|
| billing-settings-page-tests.ts (V1 form validation, lines 150-200) | Direct schema validation | Removes ~100 slow Cypress lines |
| billing-settings-v2-tests.ts (modal open/close, lines 50-100) | RTL button click + isOpen prop | Faster, more granular |
| invoice-details-page-tests.ts (PDF link generation) | Unit test with mock invoice data | Isolated, no page load needed |

**Estimated savings:** ~30 min of Cypress runtime per test run if shifted left.

---

## Summary: Gap Closure Roadmap

| Priority | Component | Tests to Add | Effort | Urgency |
|----------|-----------|-------------|--------|---------|
| P0 | invoiceHelpers.ts | 3 | 45 min | Fix now |
| P0 | schemaBuilder.ts | 7 | 2 hours | Fix now |
| P1 | AddPaymentMethodModal (V1) | 1 | 30 min | If V1 active |
| P1 | BillingCompletionModal | 1 | 30 min | Nice to have |
| P2 | Presentational components | 3 | 45 min | Polish |

**Total estimated effort: ~5 hours (includes all P0 + P1 + P2)**
