# Diff — Billing Gap Analysis v2 vs v1

**v1 analysis:** `analysis/billing/` — produced 2026-04-14
**v2 analysis:** `analysis-v2/billing/` — produced 2026-04-23
**Commits to billing between runs:** 51 (Mezzanine migration accelerated)

Companion docs:
- **[validation/billing/CALLOUT-VALIDATION.md](../validation/billing/CALLOUT-VALIDATION.md)** — every v1 callout re-checked line by line.
- **[validation/billing/SHIFT-LEFT-CANDIDATES.md](../validation/billing/SHIFT-LEFT-CANDIDATES.md)** — Cypress → Jest migration plan.

---

## Headline Numbers

| Metric | v1 (Apr 14) | v2 (Apr 23) | Δ |
|---|---|---|---|
| Source components | 70 | 87 | +17 |
| Unit test files | 25 | 33 | +8 |
| Unit test cases | ~265 | ~365 | **+100 (+38%)** |
| Cypress spec files | 3 | 6 | +3 |
| Cypress test cases | 31 | 96 | **+65 (+210%)** |
| REST API endpoints | 11 | 11 | 0 |
| Components with ZERO tests | 12 | 4 | **−8 (−67%)** |
| P0 gaps open | 2 | 1 true gap + 1 cleanup | −1 |
| P1 gaps open | 4 | 1 (schemaBuilder) + 1 conditional | −2 |
| Potentially obsolete test lines | ~1,200 | ~120 confirmed + ~1,254 conditional | see below |

**Net direction:** the team shipped real test coverage. Most P0/P1 callouts from v1 have been closed by named BILL-* tickets. The remaining backlog is smaller and sharper.

---

## Callout-Level Rollup

Of 22 callouts in the v1 analysis:

| Outcome | Count |
|---|---|
| ✅ Resolved — tests now exist | 8 |
| ✅ Still valid — gap real, still open | 3 |
| 🟡 Partially valid — indirect coverage but no direct test | 1 |
| ⚠️ Was low-risk / wrong to flag | ~1 |
| 📦 Context-dependent (gated by flag rollout) | ~11 (V1 code, V1 Cypress, V1/V2 redundancy) |
| ❌ Outright wrong | 0 |

Full per-row evidence lives in [CALLOUT-VALIDATION.md](../validation/billing/CALLOUT-VALIDATION.md).

---

## What Got Fixed Since v1

| v1 Callout | Resolved By | Evidence |
|---|---|---|
| P0.1 YearlyValueCalcModal (6 files, 0 tests) | BILL-196 — 66dd3a81f7 (mezzify revenue calculator) | `YearlyValueCalcModalV2-tests.tsx`, 17 tests |
| P1.3 EditBillingContactInfoModal | BILL-575 — cf97e215d0 (billing toasts) | `EditBillingContactInfoModal-tests.tsx`, 14 tests |
| P1.4 BillsContainer | BILL-558 — beed49c030 (current-month summary) | `BillsContainer-tests.tsx`, 21 tests |
| P1.6 DeletePaymentMethodConfirmationModal | BILL-198 — 1495b5c04d (mezzify delete modal) | `DeletePaymentMethodConfirmationModalV2-tests.tsx`, 5 tests |
| P2.7 AddPaymentMethodModal (V2) | (V2 variant) | `AddPaymentMethodModalV2-tests.tsx`, 16 tests |
| BILL-343 healthcare platforms row | BILL-343 | +6 tests on `v2/FpbInvoiceView` |
| BILL-580 FAQs visibility | BILL-580 (b9ca3b481e) | `PricingInformationV2`, 4 tests |
| BILL-575 toast routing | BILL-575 (cf97e215d0) | `useBillingToast-tests`, 8 tests |

Brand-new Cypress specs:
- `billing-invoice-summary-tests` — 18 tests (BILL-558)
- `billing-pricing-v2-tests` — 10 tests (BILL-580)

---

## What v1 Flagged And Is Now Actually Obsolete (Delete This)

| Item | Lines | Confirmation |
|---|---|---|
| `LegacyInvoiceView.tsx` + `LegacyInvoiceView-tests.tsx` | ~320 src + ~120 test | Commit **a88b14cba6** `chore(billing): tear down show_new_invoice_details_page feature flag`. V1 predicted ~340 lines — actual ~440. |
| Routing branch in `InvoiceDetailsContainer` | ~20 | Same commit |

**Action:** these tests reference a flag that no longer exists — they are safe to delete now.

---

## What v1 Flagged That's Still Conditional (No Change)

Two cleanup items remain gated by rollout checks we haven't done:

| Flag | Predicted Cleanup | Status |
|---|---|---|
| `SHOW_NEW_BILLING_MEZZ_REVAMP` = 100% | Delete V1 billing-settings-page-tests.ts (**1,254 lines** in v2, was 1,208 in v1 — V1 actually grew) + ~450 lines of V1 source | **Still open — someone needs to check AB platform** |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | May be dead — referenced but never tested | **Still open** — no investigation done |

---

## What's Still Genuinely Open (v2 P0/P1)

| v1 # | v2 Priority | Item | Why still open |
|---|---|---|---|
| P0.2 (v1) | **P0** | `invoiceHelpers.ts` — 3 pure functions, 0 tests | Nobody added the tests. Still pure, still trivial (~45 min). |
| P1.5 (v1) | **P0/P1** | `schemaBuilder.ts` — 7 Yup schemas, indirect only | Covered through modal tests but no direct schema assertions. |
| — | P1 (new) | `AddPaymentMethodModal` (V1) | Was implicitly v1 P2.7 — V1 variant still untested if `SHOW_NEW_BILLING_MEZZ_REVAMP` isn't 100%. |
| P2.8 (v1) | P3 | `BillingCompletionModal` | Presentational, Cypress touches it, unit test not worth it — v1 slightly over-flagged. |
| P3 (v1) | P3 | `BusinessAddress`, `BillingEmail`, `BillStatusLabel` | Still presentational, still indirect — unchanged. |

**Trimmed backlog estimate:** v1 said ~1–2 days; v2 says ~5 hours (all priorities combined).

---

## New Things v2 Surfaces That v1 Missed / Didn't Yet Exist

1. **`billing-settings-page-tests.ts` grew to 1,254 lines** — V1 spec is 46 lines longer than at v1-time despite V2 rollout. Someone is still editing V1.
2. **Two brand-new Cypress specs** (`billing-invoice-summary-tests`, `billing-pricing-v2-tests`, 28 tests total) created without corresponding unit coverage for the same logic — prime **shift-left targets**. See SHIFT-LEFT-CANDIDATES.md.
3. **`useBillingToast` hook (BILL-575)** — net new code, 8 tests added on arrival. No gap.
4. **Net +65 Cypress tests vs +100 unit tests** — Cypress grew disproportionately (+210% vs +38%). The shift-left pressure is increasing, not decreasing.

---

## Shift-Left Takeaways (for your review)

From [SHIFT-LEFT-CANDIDATES.md](../validation/billing/SHIFT-LEFT-CANDIDATES.md):

| Bucket | Count | Notes |
|---|---|---|
| Keep in Cypress (real integration value) | 3 V2 tests | Stripe iframe, cross-page nav, happy-path E2E |
| Shift left (Cypress → Jest/RTL) | 16 V2 + 2 invoice = 18 tests | Form validation, modal open/close, error render |
| Delete as already covered by unit | 6 V2 + 2 invoice = 8 tests | Redundant assertions |
| Deferred until V1 removal | 35 V1 tests | Wait on `SHOW_NEW_BILLING_MEZZ_REVAMP` 100% |
| New unit tests to add | 4–5 | `invoiceHelpers`, `schemaBuilder`, possibly `AddPaymentMethodModal` V1 |

**Estimated CI impact of shift-left + delete:** 40–50 seconds/run (per subagent estimate, generously). **Effort:** 7–10 hours over ~4 weeks.

---

## How to Read This Bundle

1. **Start here** — you're reading it.
2. **Want the current-state snapshot** → [`analysis-v2/billing/SUMMARY.md`](billing/SUMMARY.md).
3. **Want to prove each v1 callout is right or wrong** → [`validation/billing/CALLOUT-VALIDATION.md`](../validation/billing/CALLOUT-VALIDATION.md) — every row has a commit hash or file:line.
4. **Want to present a shift-left plan** → [`validation/billing/SHIFT-LEFT-CANDIDATES.md`](../validation/billing/SHIFT-LEFT-CANDIDATES.md) — per-test classification (keep / shift / delete).
5. **Want to see what deterred / confirmed gaps** → [`analysis-v2/billing/gaps/GAPS.md`](billing/gaps/GAPS.md).
