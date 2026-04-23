# REST API Endpoint Coverage — Billing Domain (2026-04-23)

Mapping of billing API endpoints to source code, server handlers, and test coverage.

---

## API Endpoints Summary

| Method | Endpoint | Source | API Client | Unit Tests | Cypress | Status |
|--------|----------|--------|-----------|-----------|---------|--------|
| POST | `/api/provider/v1/billing/payment-methods` | apiCalls.ts | addPaymentMethod | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| DELETE | `/api/provider/v1/billing/payment-methods/{id}` | apiCalls.ts | deletePaymentMethod | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| PATCH | `/api/provider/v1/billing/payment-methods/{id}/default` | apiCalls.ts | setDefaultPaymentMethod | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| GET | `/api/provider/v1/billing/invoices` | apiCalls.ts | getInvoices | Yes (apiCalls-tests) | Indirect | Covered |
| GET | `/api/provider/v1/invoices/{id}` | apiCalls.ts | getInvoiceDetails | Yes (apiCalls-tests) | invoice-details | Covered |
| GET | `/api/provider/v1/invoices/{id}/pdf` | — | — | NO | Indirect | **GAP** |
| PATCH | `/api/provider/v1/billing/contact-info/email` | apiCalls.ts | updatePracticeBillingEmail | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| PATCH | `/api/provider/v1/billing/contact-info/address` | apiCalls.ts | updatePrimaryBusinessAddress | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| PATCH | `/api/provider/v1/billing/monthly-limit` | apiCalls.ts | updateMonthlyLimit | Yes (apiCalls-tests) | V1+V2 Cypress | Covered |
| PATCH | `/api/provider/v1/billing/rollovers` | apiCalls.ts | updateRollovers | Yes (apiCalls-tests) | V1 Cypress | Covered |
| GET | `/graphql` (getSkuMappings) | — | GraphQL | Indirect | Indirect | Covered (implicit) |

---

## API Client Functions (apiCalls.ts)

**File:** `apps/settings/src/pages/settingsPages/billingSettings/apiCalls.ts`

**Test coverage:** apiCalls-tests.ts (25 tests)

### Function Details

| Function | HTTP Method | Endpoint | Success Tests | Error Tests | Status |
|----------|-------------|----------|---------------|------------|--------|
| `addPaymentMethod` | POST | `/api/provider/v1/billing/payment-methods` | Yes | Yes | ✓ |
| `deletePaymentMethod` | DELETE | `/api/provider/v1/billing/payment-methods/{id}` | Yes | Yes | ✓ |
| `setDefaultPaymentMethod` | PATCH | `/api/provider/v1/billing/payment-methods/{id}/default` | Yes | Yes | ✓ |
| `getInvoices` | GET | `/api/provider/v1/billing/invoices` | Yes | Yes | ✓ |
| `getInvoiceDetails` | GET | `/api/provider/v1/invoices/{id}` | Yes | Yes | ✓ |
| `updatePracticeBillingEmail` | PATCH | `/api/provider/v1/billing/contact-info/email` | Yes | Yes | ✓ |
| `updatePrimaryBusinessAddress` | PATCH | `/api/provider/v1/billing/contact-info/address` | Yes | Yes | ✓ |
| `updateMonthlyLimit` | PATCH | `/api/provider/v1/billing/monthly-limit` | Yes | Yes | ✓ |
| `updateRollovers` | PATCH | `/api/provider/v1/billing/rollovers` | Yes | Yes | ✓ |
| `getPaymentMethodsByProvider` | GET | `/api/provider/v1/billing/payment-methods/by-provider` | Yes | Yes | ✓ |

**Summary:** All 10 API client functions have unit tests with success + error paths covered.

---

## Server Handlers (Backend)

**File:** `apps/settings/src/server/controllers/practiceBillingSettingsPage/`

| Handler | Endpoint | Backend Logic | Frontend Mapping |
|---------|----------|---------------|------------------|
| `GET_INVOICES` | `/api/provider/v1/billing/invoices` | Fetch practice invoices | getInvoices() |
| `GET_INVOICE_DETAILS` | `/api/provider/v1/invoices/{id}` | Fetch invoice details + line items | getInvoiceDetails() |
| `GET_INVOICE_PDF_DOWNLOAD_URL` | `/api/provider/v1/invoices/{id}/pdf` | Generate PDF URL | NOT MAPPED |
| `POST_PAYMENT_METHOD` | `/api/provider/v1/billing/payment-methods` | Create payment method | addPaymentMethod() |
| `DELETE_PAYMENT_METHOD` | `/api/provider/v1/billing/payment-methods/{id}` | Delete payment method | deletePaymentMethod() |
| `PATCH_DEFAULT_PAYMENT_METHOD` | `/api/provider/v1/billing/payment-methods/{id}/default` | Set default | setDefaultPaymentMethod() |
| `PATCH_BILLING_EMAIL` | `/api/provider/v1/billing/contact-info/email` | Update email | updatePracticeBillingEmail() |
| `PATCH_BUSINESS_ADDRESS` | `/api/provider/v1/billing/contact-info/address` | Update address | updatePrimaryBusinessAddress() |
| `PATCH_MONTHLY_LIMIT` | `/api/provider/v1/billing/monthly-limit` | Update limit | updateMonthlyLimit() |
| `PATCH_ROLLOVERS` | `/api/provider/v1/billing/rollovers` | Update rollovers | updateRollovers() |

---

## Routes Mapping

**File:** `apps/settings/src/config/routes.ts`

**Billing routes exposed:**
```
/api/provider/v1/billing/*
/api/provider/v1/invoices/*
```

All 11 endpoints mapped. Route configuration is stable.

---

## Test Coverage Details

### Unit Test Coverage (apiCalls-tests.ts)

**Test file structure:**

```
apiCalls-tests.ts (25 tests total)
├── addPaymentMethod (2 tests: success, error)
├── deletePaymentMethod (2 tests)
├── setDefaultPaymentMethod (2 tests)
├── getInvoices (2 tests)
├── getInvoiceDetails (2 tests)
├── updatePracticeBillingEmail (2 tests)
├── updatePrimaryBusinessAddress (2 tests)
├── updateMonthlyLimit (2 tests)
├── updateRollovers (2 tests)
└── getPaymentMethodsByProvider (2 tests)
    └── Error scenarios (5 additional tests)
```

### Cypress Coverage

| Endpoint | V1 Tests | V2 Tests | invoice-details | Coverage |
|----------|----------|----------|---|----------|
| POST payment-methods | Yes | Yes | — | Complete |
| DELETE payment-methods | Yes | Yes | — | Complete |
| PATCH default PM | Yes | Yes | — | Complete |
| GET invoices | Yes | Yes | — | Complete |
| GET invoice/{id} | Yes | Yes | Yes | Complete |
| PATCH email | Yes | Yes | — | Complete |
| PATCH address | Yes | Yes | — | Complete |
| PATCH monthly-limit | Yes | Yes | — | Complete |
| PATCH rollovers | Yes | Yes | — | Complete |
| GET PM by provider | Yes | Yes | — | Complete |
| GET invoice PDF | — | — | — | **MISSING** |

---

## Coverage Gaps

### Missing Unit Test

**Endpoint:** `GET_INVOICE_PDF_DOWNLOAD_URL` (`/api/provider/v1/invoices/{id}/pdf`)

**Status:**
- Handler exists in server code
- Not mapped to frontend apiCalls.ts
- Not tested in unit tests
- Not tested in Cypress
- PDF download URL is generated but never validated

**Why it matters:** If PDF generation logic breaks, we won't catch it in tests. End-to-end PDF download scenarios are untested.

**Test plan:**
- Add `getInvoicePdfUrl()` function to apiCalls.ts
- Test with valid invoice ID → returns PDF URL
- Test with invalid invoice ID → returns error
- Add Cypress test to verify PDF link clicks work

**Effort:** 1 hour

---

## GraphQL Endpoints

**Query:** `getSkuMappings`

**Purpose:** Fetch SKU pricing mappings for display

**Usage:** PricingInformation, PricingInformationV2

**Test coverage:** Indirect (tested through component rendering tests)

**Status:** Adequate for current scope. GraphQL testing is handled separately by Apollo Client.

---

## API Security Notes

All billing endpoints require:
- Authentication header (Bearer token)
- Practice context (practiceId)
- Authorization checks (user has billing access)

These are enforced at backend + tested via component integration tests.

---

## Recent API Changes

| Change | Endpoint | Impact | Commits |
|--------|----------|--------|---------|
| Add numApiBookings field | GET invoice/{id} | Invoice detail DTO expanded | BILL-343 |
| Add showApiPartnerBookings toggle | GET invoices | Summary display conditional | BILL-343 |
| Toast routing (BILL-575) | POST/PATCH all | Toast notifications added | BILL-575 |
| Search in PM by provider (BILL-486) | GET PM by provider | Modal UX enhanced | BILL-486 |

No breaking changes. All endpoints backward-compatible.

---

## Recommendations

1. **Add unit test for PDF download endpoint** — 1 hour effort
2. **Verify all API error responses** — Already covered via apiCalls-tests.ts
3. **No breaking changes detected** — Safe to maintain current test suite
4. **Monitor GraphQL schema evolution** — PricingTab tests cover current usage

