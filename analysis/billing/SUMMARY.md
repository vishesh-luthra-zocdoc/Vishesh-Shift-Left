# Billing Test Analysis — Executive Summary

**Date:** 2026-04-14
**Scope:** Billing features in `provider-fe-monorepo` (Settings app)
**Author:** Vishesh Luthra

---

## The Big Picture

The billing domain has **decent test coverage overall**, but there are clear holes that could bite us in production. Here's the quick scorecard:

| What We Looked At | Count |
|-------------------|-------|
| Source components | 70 files |
| Components with unit tests | 25 files (~265 tests) |
| Components with Cypress E2E tests | 3 specs (31 tests) |
| REST API endpoints | 11 |
| **Components with ZERO tests** | **12** |
| **Potentially obsolete test lines** | **~1,200+** |

## What's Working Well

- **API layer is solid** — All 10 API client functions have unit tests covering success + error paths. 10 of 11 REST endpoints are also intercepted in Cypress.
- **V2 (Mezzanine) components are well tested** — PaymentMethodsListV2, PaymentMethodV2, PaymentMethodsPerProviderModal all have good unit + E2E coverage.
- **Invoice views have good coverage** — FpbInvoiceView has 22 unit tests covering totals, payments, experiments, and edge cases.
- **Form validation is thoroughly tested** — Credit card, ACH, email, address, and monthly limit modals all have validation unit tests.

## What Needs Attention

### P0 — Fix Now (High Risk, Easy Wins)

1. **YearlyValueCalcModal (pricing calculator)** — 6 files, ZERO tests. This calculates pricing shown to providers. If the formula is wrong, providers see wrong numbers. These are pure functions — easy to test.
2. **`invoiceHelpers.ts`** — 3 exported functions (`formatDate`, `getLastDayOfMonth`, `capitalizeStatus`) with no tests. Date formatting bugs = wrong invoice dates displayed.

### P1 — Fix Soon

3. **`EditBillingContactInfoModal`** (V2) — Combines address + email update with 2 API calls. No unit test.
4. **`BillsContainer`** — Lists all invoices. No unit test for rendering/filtering.
5. **`schemaBuilder.ts`** — 7 Yup validation schemas only tested indirectly through modal tests.
6. **`DeletePaymentMethodConfirmationModal`** — Confirmation dialog with delete action. No unit test.

### Cleanup Needed

7. **~1,200 lines of V1 Cypress tests** may be dead if `SHOW_NEW_BILLING_MEZZ_REVAMP` is fully rolled out.
8. **`LegacyInvoiceView` tests** may be dead if `SHOW_NEW_INVOICE_DETAILS_PAGE` is fully rolled out.
9. **`BILLING_PAGE_ENABLE_IFRAME_DEPRECATION`** experiment referenced in code but not found in any test — may be dead code.

## Recommended Next Steps

| # | Action | Effort | What It Fixes |
|---|--------|--------|---------------|
| 1 | Check experiment rollout status for V1→V2 flags | 30 min | Determines if 1,200+ lines of V1 tests can be deleted |
| 2 | Add unit tests for `invoiceHelpers.ts` | 1 hour | P0 gap — 3 pure functions |
| 3 | Add unit tests for YearlyValueCalcModal calculation | 2 hours | P0 gap — pricing calculator |
| 4 | Add unit test for `EditBillingContactInfoModal` | 2 hours | P1 gap — V2 modal |
| 5 | Add unit test for `BillsContainer` | 1 hour | P1 gap — invoice list |
| 6 | Remove V1 tests if experiments fully rolled out | 2 hours | Cleans up 1,200+ dead lines |

**Total estimated effort: ~1-2 days**

## Deeper Dives

- **What tests exist today?** → [inventory/MASTER-INVENTORY.md](inventory/MASTER-INVENTORY.md)
- **Every single test listed out** → [inventory/DETAILED-TEST-CATALOG.md](inventory/DETAILED-TEST-CATALOG.md)
- **Which component has which test?** → [inventory/components.md](inventory/components.md)
- **Cypress test details** → [inventory/cypress-e2e-tests.md](inventory/cypress-e2e-tests.md)
- **API endpoint coverage** → [inventory/api-endpoint-coverage.md](inventory/api-endpoint-coverage.md)
- **Full gap list with priorities** → [gaps/GAPS.md](gaps/GAPS.md)
- **Dead/outdated tests** → [gaps/OBSOLETE.md](gaps/OBSOLETE.md)
- **Feature flag cleanup** → [gaps/feature-flag-audit.md](gaps/feature-flag-audit.md)
