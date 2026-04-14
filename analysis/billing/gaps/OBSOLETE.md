# Potentially Obsolete Tests — Billing Domain

Tests that may be dead weight if certain experiments are fully rolled out.

---

## The V1 vs V2 Problem

The billing UI has **two parallel implementations** gated behind the `SHOW_NEW_BILLING_MEZZ_REVAMP` experiment:

- **V1 (Legacy)** — Original UI with custom styling
- **V2 (Mezzanine)** — Redesigned UI using Zocdoc's Mezzanine design system

Both have their own tests. If V2 is fully rolled out to 100%, the V1 code and tests are dead.

### What's at Stake

| If V2 is 100% rolled out... | Lines | Files |
|-----------------------------|-------|-------|
| billing-settings-page-tests.ts (V1 Cypress) | 1,208 | 1 |
| EditMonthlyLimitModal-tests.tsx (V1 unit) | ~50 | 1 |
| EditBillingEmailModal-tests.tsx (V1 unit) | ~30 | 1 |
| EditBusinessAddressModal-tests.tsx (V1 unit) | ~80 | 1 |
| PaymentMethodsList.tsx (V1 source) | ~200 | 1 |
| PaymentMethod.tsx (V1 source) | ~150 | 1 |
| PaymentMethodsPerProviderList.tsx (V1 source) | ~100 | 1 |
| EditMonthlyLimitModal.tsx (V1 source) | ~150 | 1 |
| **Total potentially dead** | **~1,968** | **8** |

### Action Required

Check the rollout status of `SHOW_NEW_BILLING_MEZZ_REVAMP` in the AB platform:
- If **100% on** → Delete all V1 code and tests listed above
- If **still running** → Keep both, but know the V1 tests will eventually be removed
- If **deprecated/concluded** → Same as 100% — clean up

---

## The Legacy Invoice Problem

Similarly, `SHOW_NEW_INVOICE_DETAILS_PAGE` gates the old vs new invoice view:

| If new invoice page is 100%... | Lines | Files |
|--------------------------------|-------|-------|
| LegacyInvoiceView-tests.tsx (unit) | ~120 | 1 |
| LegacyInvoiceView.tsx (source) | ~200 | 1 |
| Routing path in InvoiceDetailsContainer | ~20 | partial |
| **Total potentially dead** | **~340** | **2+** |

### Action Required

Check rollout of `SHOW_NEW_INVOICE_DETAILS_PAGE`:
- If **100% on** → Remove LegacyInvoiceView and its tests
- If **still running** → Keep

---

## Redundant Tests (V1 + V2 Overlap)

These features are tested in BOTH V1 and V2 Cypress tests. Once V1 is removed, this overlap goes away. But until then:

| Feature | V1 Cypress | V2 Cypress | Redundant? |
|---------|-----------|-----------|------------|
| Set default payment method | billing-settings-page-tests (line 116-146) | billing-settings-v2-tests (line 173-200) | Yes — same API, different UI |
| Delete payment method | billing-settings-page-tests (line 94-115) | billing-settings-v2-tests (line 274-317) | Yes |
| Update billing email | billing-settings-page-tests (line 148-182) | billing-settings-v2-tests (line 520-554) | Yes |
| Update business address | billing-settings-page-tests (line 184-230) | billing-settings-v2-tests (line 459-519) | Yes |
| Edit rollovers | billing-settings-page-tests (line 271-325) | billing-settings-v2-tests (line 31-134) | Yes |
| Monthly limit | billing-settings-page-tests (line 327-400) | billing-settings-v2-tests (line 201-272) | Yes |

**Total redundant Cypress test lines: ~500+**

---

## Summary: Cleanup Effort

| Action | Effort | Impact |
|--------|--------|--------|
| Check experiment rollout status | 30 min | Determines scope of cleanup |
| Remove V1 Cypress tests (if V2 is 100%) | 1 hour | Removes 1,208 lines |
| Remove V1 source components (if V2 is 100%) | 1 hour | Removes ~600 lines of dead code |
| Remove LegacyInvoiceView (if new page is 100%) | 30 min | Removes ~320 lines |
| **Total** | **~3 hours** | **~2,100+ lines removed** |
