# Billing Test Analysis — Executive Summary

**Date:** 2026-04-23
**Scope:** Billing features in `provider-fe-monorepo` (Settings app)
**Prior Analysis:** 2026-04-14
**Commits Since Last Analysis:** 51 (significant drift detected)

---

## The Big Picture

**Significant progress since April 14:** Many prior P0/P1 gaps have been filled. Key milestones:
- **LegacyInvoiceView torn down** (commit a88b14cba6) — flag removed from codebase
- **P0 gaps addressed:** YearlyValueCalcModalV2, BillsContainer, AddPaymentMethodModalV2, EditBillingContactInfoModal now tested
- **51 billing-focused commits** with multiple BILL-* tickets (BILL-343, BILL-558, BILL-575, BILL-580, etc.) — Mezzanine migration accelerating

| What We Looked At | Count |
|-------------------|-------|
| Source components | 87 files |
| Components with unit tests | 33 files (~365 tests) |
| Components with Cypress E2E tests | 6 specs (96 tests) |
| REST API endpoints | 11 |
| **Components with ZERO tests** | **4** (down from 12) |
| **Newly obsolete test lines** | **~120** (LegacyInvoiceView-tests) |

## What's Working Well

- **P0 gaps largely closed** — YearlyValueCalcModalV2 (17 tests), BillsContainer (21 tests), AddPaymentMethodModalV2 (16 tests) all now have unit coverage.
- **V2 Mezzanine fully tested** — All V2 modals, components, and hooks have good unit + E2E coverage (EditBillingContactInfoModal, DeletePaymentMethodConfirmationModalV2, etc.).
- **New Healthcare platforms row (BILL-343)** — Covered with Cypress tests.
- **Invoice views mature** — FpbInvoiceView has 28 unit tests (v2 version), covers new numApiBookings field.
- **API layer solid** — All 10 API functions have unit tests covering success + error paths.

## What Needs Attention

### P0 — Critical (High Risk, Requires Action)

1. **LegacyInvoiceView-tests.tsx (OBSOLETE)** — 120 lines, 12 tests. Flag `SHOW_NEW_INVOICE_DETAILS_PAGE` was torn down in commit a88b14cba6. These tests reference code path that no longer exists.
2. **`invoiceHelpers.ts` (NO TESTS)** — 3 exported functions: `formatDate`, `getLastDayOfMonth`, `capitalizeStatus`. Used in FpbInvoiceView + v2/FpbInvoiceView. Date formatting bugs would surface in production.

### P1 — High Priority (Should Fix)

3. **`schemaBuilder.ts` (INDIRECT TESTING ONLY)** — 7 Yup validation schemas tested only through modal components. Edge cases not covered (boundary values, special characters, exact length validation).
4. **AddPaymentMethodModal (V1)** — Original version has no unit test. V2 variant (AddPaymentMethodModalV2) is tested, but V1 may still be in use if `SHOW_NEW_BILLING_MEZZ_REVAMP` not fully rolled out.

### P2/P3 — Low Priority (Presentational, Indirect Testing)

5. **Presentational components** — BusinessAddress, BillingEmail, BillStatusLabel tested only indirectly via parents. Low risk.
6. **billing-settings-page-tests.ts (1,254 lines)** — V1 Cypress spec may be redundant if `SHOW_NEW_BILLING_MEZZ_REVAMP` is fully rolled out. Maintains duplicate coverage with billing-settings-v2-tests.ts.

## Recommended Next Steps

| # | Action | Effort | What It Fixes |
|---|--------|--------|---------------|
| 1 | Delete LegacyInvoiceView and its tests | 30 min | P0 — removes 120+ dead test lines |
| 2 | Add unit tests for `invoiceHelpers.ts` | 45 min | P0 — 3 pure functions, easy to test |
| 3 | Check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout status | 30 min | Determines if ~1,254 lines of V1 Cypress tests can be deleted |
| 4 | Add direct unit tests for `schemaBuilder.ts` | 2 hours | P1 — validates edge cases in 7 schemas |
| 5 | Audit `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` experiment | 30 min | May be dead code — referenced but never tested |

**Total estimated effort: ~1 day**

## Monolith Selenium Tests (zocdoc_web)

In addition to the frontend analysis above, **76 Selenium integration tests** in the `zocdoc_web` monolith test backend billing logic. See the prior analysis for triage results (38 keep, 38 remove). No changes detected to this set.

---

## Notable Deltas from v1 Analysis (2026-04-14)

| Change | Impact | Notes |
|--------|--------|-------|
| LegacyInvoiceView flag torn down | -120 test lines | Commit a88b14cba6 removed SHOW_NEW_INVOICE_DETAILS_PAGE flag entirely |
| YearlyValueCalcModalV2 tested | +17 tests | Was P0 gap, now covered |
| BillsContainer tested | +21 tests | Was P0 gap, now covered |
| AddPaymentMethodModalV2 tested | +16 tests | New V2 variant with comprehensive coverage |
| EditBillingContactInfoModal tested | +14 tests | Was P1 gap, now covered |
| DeletePaymentMethodConfirmationModalV2 tested | +5 tests | New V2 variant tested |
| TaxesAndFeesSection tested | +6 tests | New section from BILL-580 |
| EditMonthlyLimitModalV2 tests added | +8 tests | Expanded from v1 tests |
| EditRolloversModalV2 tests added | +10 tests | Expanded from v1 tests |
| BillingContactInfo tests updated | +2 tests | Enhanced validation coverage |
| FpbInvoiceView (v2) tests | +28 tests | Includes healthcare platforms row (BILL-343), numApiBookings field |
| billing-invoice-summary-tests added | +18 tests | New invoice summary Cypress spec |
| billing-pricing-v2-tests added | +10 tests | New pricing Cypress spec with BILL-580 FAQs logic |
| Unit test count | +100 tests | 265 → 365 |
| Cypress test count | +65 tests | 31 → 96 |

## Key Feature Flags Under Review

| Flag | Status | Action |
|------|--------|--------|
| `SHOW_NEW_INVOICE_DETAILS_PAGE` | TORN DOWN (a88b14cba6) | Delete LegacyInvoiceView + tests |
| `SHOW_NEW_BILLING_MEZZ_REVAMP` | **Still active** | Check rollout — may be 100% |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | **Investigate** | Referenced but not tested anywhere |
| `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | Active, well tested | No action needed |

---

## Deeper Dives

- **What tests exist today?** → [inventory/MASTER-INVENTORY.md](inventory/MASTER-INVENTORY.md)
- **Which component has which test?** → [inventory/components.md](inventory/components.md)
- **Cypress test details** → [inventory/cypress-e2e-tests.md](inventory/cypress-e2e-tests.md)
- **API endpoint coverage** → [inventory/api-endpoint-coverage.md](inventory/api-endpoint-coverage.md)
- **Full gap list with priorities** → [gaps/GAPS.md](gaps/GAPS.md)
- **Obsolete/dead tests** → [gaps/OBSOLETE.md](gaps/OBSOLETE.md)
- **Feature flag cleanup** → [gaps/feature-flag-audit.md](gaps/feature-flag-audit.md)
