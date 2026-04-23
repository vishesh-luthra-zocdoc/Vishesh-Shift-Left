# Obsolete & Dead Tests — Billing Domain (2026-04-23)

Tests that are dead weight or reference code paths that no longer exist.

---

## Critical: Confirmed Obsolete (Tear Down Immediately)

### LegacyInvoiceView Tests — CONFIRMED DEAD (Commit a88b14cba6)

**Files to delete:**
- `apps/settings/src/pages/settingsPages/billingSettings/__tests__/LegacyInvoiceView-tests.tsx` (6.6 KB, 12 tests)
- `apps/settings/src/pages/settingsPages/billingSettings/LegacyInvoiceView.tsx` (9.9 KB, source)
- Routing logic in `InvoiceDetailsContainer.tsx` (partial, ~20 lines)

**Status:** `SHOW_NEW_INVOICE_DETAILS_PAGE` flag was torn down in commit a88b14cba6 (April 2026).

**Evidence:**
- Git log shows: "chore(billing): tear down show_new_invoice_details_page feature flag (#10415)"
- grep confirms flag removed from BillingSettingsContainer.tsx
- Only FpbInvoiceView (v2) is now rendered in InvoiceDetailsContainer

**Total dead lines:** 120+ test lines + 10 source lines

**Action:** Delete both files immediately. No backward compatibility risk — flag is already gone.

**Effort:** 30 minutes (delete files + cleanup routing)

---

## High Priority: Conditional Obsolescence (Pending Experiment Status)

### V1 Billing UI (If SHOW_NEW_BILLING_MEZZ_REVAMP is 100% Rolled Out)

#### IF `SHOW_NEW_BILLING_MEZZ_REVAMP` = 100% ON:

**Files to delete:**

| Component | Type | Lines | Status |
|-----------|------|-------|--------|
| billing-settings-page-tests.ts | Cypress | 1,254 | V1 UI tests (redundant with V2 tests) |
| EditMonthlyLimitModal-tests.tsx | Unit | ~50 | V1 validation (replaced by EditMonthlyLimitModalV2) |
| EditBillingEmailModal-tests.tsx | Unit | ~30 | V1 form (replaced by combined EditBillingContactInfoModal) |
| EditBusinessAddressModal-tests.tsx | Unit | ~80 | V1 form (replaced by combined EditBillingContactInfoModal) |
| PaymentMethodsList.tsx | Source | ~210 | V1 component (replaced by PaymentMethodsListV2) |
| PaymentMethod.tsx | Source | ~150 | V1 component (replaced by PaymentMethodV2) |
| PaymentMethodsPerProviderList.tsx | Source | ~100 | V1 component (likely unused) |
| EditMonthlyLimitModal.tsx | Source | ~150 | V1 component (replaced by EditMonthlyLimitModalV2) |
| AddPaymentMethodModal.tsx | Source | ~80 | V1 component (replaced by AddPaymentMethodModalV2) |
| DeletePaymentMethodConfirmationModal.tsx | Source | ~60 | V1 component (replaced by V2 variant) |
| YearlyValueCalcModal/* (V1 files) | Source | ~200 | V1 calculator (replaced by YearlyValueCalcModalV2) |
| **Total if 100%** | | **~2,364** | **~11 files** |

**Action Required:**
1. Check AB platform for `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout status
2. If 100% → delete all files above
3. If still running → keep both, mark for future cleanup

**Current status:** Flag still referenced in code (InvoiceDetailsContainer.tsx, BillingSettingsContainer.tsx). Rollout status UNKNOWN — requires investigation.

**Effort if deleting:** 2 hours (file deletion + import cleanup)

---

## Medium Priority: Dead Experiment Code

### BILLING_PAGE_ENABLE_IFRAME_DEPRECATION — Possibly Dead

**Location:** `BillingSettingsContainer.tsx` (lines ~200-210)

**Status:**
- Referenced in source: YES
- Tested in unit tests: NO
- Tested in Cypress: NO
- Found in experiment setup commands: NO
- Found in any Cypress beforeEach: NO

**Investigation needed:** Search AB platform for this experiment. If:
- **Concluded/deprecated** → Delete the code
- **Still running** → Add tests for both ON/OFF branches
- **Fully ON** → Simplify code (remove branch)

**Current code impact:** Unknown (depends on rollout status)

**Effort:** 30 minutes investigation + 30 minutes code cleanup

---

## Redundant Test Coverage (Once V1 Deleted)

Once `SHOW_NEW_BILLING_MEZZ_REVAMP` reaches 100%, these tests will have overlapping coverage with V2 tests:

| Feature | V1 Test | V2 Test | Redundant Lines |
|---------|---------|---------|-----------------|
| Set default payment method | billing-settings-page-tests (lines 116-146) | billing-settings-v2-tests (lines 173-200) | ~30 |
| Delete payment method | billing-settings-page-tests (lines 94-115) | billing-settings-v2-tests (lines 274-317) | ~24 |
| Update billing email | billing-settings-page-tests (lines 148-182) | billing-settings-v2-tests (lines 520-554) | ~35 |
| Update business address | billing-settings-page-tests (lines 184-230) | billing-settings-v2-tests (lines 459-519) | ~47 |
| Edit rollovers | billing-settings-page-tests (lines 271-325) | billing-settings-v2-tests (lines 31-134) | ~55 |
| Monthly limit | billing-settings-page-tests (lines 327-400) | billing-settings-v2-tests (lines 201-272) | ~71 |
| **Total redundant** | | | **~262 lines** |

**Action:** Delete V1 tests when experiment reaches 100%.

---

## Summary: Cleanup Effort

| What | Lines | Effort | Urgency | Blocker |
|------|-------|--------|---------|---------|
| Delete LegacyInvoiceView + tests | 120 | 30 min | NOW | No |
| Audit `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | -- | 30 min | High | No |
| Check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout | -- | 15 min | High | Blocks V1 cleanup |
| Delete V1 UI + tests (if 100% rollout) | ~2,364 | 2 hours | High | Rollout check |
| **Total** | **2,484+** | **~3.5 hours** | | |

---

## Immediate Action Items

1. **TODAY:** Delete LegacyInvoiceView files (commit a88b14cba6 confirmation)
2. **THIS WEEK:** Check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout status in AB platform
3. **THIS WEEK:** Audit `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` (dead code?)
4. **NEXT SPRINT:** If V1 is 100% → Delete all V1 components and tests (~2,364 lines)

