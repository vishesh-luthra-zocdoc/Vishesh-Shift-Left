# Feature Flag & Experiment Audit — Billing Domain

Every experiment and feature flag used in billing code, and whether it's properly tested.

---

## Experiments (A/B Tests)

| # | Experiment Name | What It Controls | Where Used | Unit Tests | Cypress Tests | Action Needed |
|---|----------------|-----------------|------------|------------|---------------|---------------|
| 1 | `SHOW_NEW_BILLING_MEZZ_REVAMP` | V2 Mezzanine UI for payment methods and billing contact | BillingSettingsContainer, PaymentMethodsList | Not directly tested | billing-settings-v2-tests (always ON) | **Check rollout status. If 100% → remove V1 code + tests** |
| 2 | `SHOW_NEW_INVOICE_DETAILS_PAGE` | New FPB invoice detail view vs Legacy | InvoiceDetailsContainer, Cypress setup | Not directly tested | Set to ON in V2 tests | **Check rollout status. If 100% → remove LegacyInvoiceView** |
| 3 | `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | Shows paid vs free bookings breakdown on invoices | FpbInvoiceView | FpbInvoiceView-tests.tsx (4 tests) | invoice-details-page-tests.ts (2 tests) | Active experiment. Well tested. |
| 4 | `BILLING_PAID_VS_FREE_DATE_GUARD` | Date filter: only show paid/free breakdown for invoices >= Jan 2026 | FpbInvoiceView | FpbInvoiceView-tests.tsx (3 tests) | Not tested in Cypress | Active. Unit tests cover ON + OFF + boundary date. |
| 5 | `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | Deprecates iframe usage on billing page | BillingSettingsContainer (referenced) | Not tested | Not tested | **Investigate. May be dead code — referenced in source but not found in test setup.** |

---

## Feature Flags (Server-Side Toggles)

| # | Flag Name | What It Controls | Where Used | Tested? | Notes |
|---|-----------|-----------------|------------|---------|-------|
| 1 | `Billing.MinimumPaymentMethodLimit` | Minimum value for monthly dollar limit (default $500) | schemaBuilder.ts, EditMonthlyLimitModal | Yes — EditMonthlyLimitModal-tests.tsx | Active flag |
| 2 | `Billing.EnableStripeSandbox` | Enables Stripe sandbox mode for test practices | shouldUseStripeSandbox.ts | Yes — useShouldUseStripeSandbox-tests.ts (6 tests) | All 4 boolean branches covered |

---

## Entity Flags

| # | Flag Name | What It Controls | Where Used | Tested? |
|---|-----------|-----------------|------------|---------|
| 1 | `shouldEnableStripeSandboxForPractice` | Per-practice override for Stripe sandbox | shouldUseStripeSandbox.ts | Yes — part of the 6-test suite |

---

## Detailed Findings

### SHOW_NEW_BILLING_MEZZ_REVAMP — Likely Cleanup Candidate

This is the biggest flag in billing. It gates:
- `PaymentMethodsList.tsx` → routes to `PaymentMethodsListV2.tsx` when ON
- `BillingSettingsContainer.tsx` → shows V2 billing contact info section when ON
- Separate modals: V1 uses `EditBillingEmailModal` + `EditBusinessAddressModal`, V2 uses `EditBillingContactInfoModal`
- Separate monthly limit modal: V1 uses `EditMonthlyLimitModal`, V2 uses `EditMonthlyLimitModalV2`

**If fully rolled out**, we can delete:
- 3 V1 source components (~450 lines)
- 3 V1 unit test files (~160 lines)
- 1 V1 Cypress spec (1,208 lines)

### BILLING_PAGE_ENABLE_IFRAME_DEPRECATION — Possibly Dead

This experiment is:
- Referenced in `BillingSettingsContainer.tsx`
- NOT tested in any unit test
- NOT configured in any Cypress test
- NOT found in experiment setup commands

**Action:** Search the AB platform for this experiment. If it's concluded or deprecated, the code referencing it can be cleaned up.

### BILLING_PAGE_BREAKDOWN_PAID_VS_FREE — Well Tested

This is the most thoroughly tested experiment in billing:
- 4 unit tests in `FpbInvoiceView-tests.tsx` covering ON/OFF + date guard combinations
- 2 Cypress tests in `invoice-details-page-tests.ts` covering ON/OFF display
- Date guard flag adds additional protection (only shows for invoices >= Jan 2026)

No action needed.

---

## Recommendations

| # | Action | Effort | Priority |
|---|--------|--------|----------|
| 1 | Check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout status | 15 min | High — determines if 1,800+ lines can be deleted |
| 2 | Check `SHOW_NEW_INVOICE_DETAILS_PAGE` rollout status | 15 min | High — determines if ~340 lines can be deleted |
| 3 | Investigate `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | 30 min | Medium — may be dead experiment code |
| 4 | No action on `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | — | Already well tested |
| 5 | No action on `Billing.MinimumPaymentMethodLimit` | — | Already tested |
| 6 | No action on `Billing.EnableStripeSandbox` | — | Already well tested |
