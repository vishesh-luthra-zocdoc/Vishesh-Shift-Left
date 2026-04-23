# Feature Flag & Experiment Audit — Billing Domain (2026-04-23)

Every experiment and feature flag used in billing code, and its test coverage status.

---

## Active Experiments (A/B Tests)

| # | Experiment | Controls | Where Used | Unit Tests | Cypress Tests | Status |
|---|-----------|----------|-----------|------------|---------------|--------|
| 1 | `SHOW_NEW_BILLING_MEZZ_REVAMP` | V2 Mezzanine UI vs V1 Legacy | BillingSettingsContainer, InvoiceDetailsContainer | Not tested | billing-settings-v2-tests.ts (V2 ON) | **CHECK ROLLOUT** |
| 2 | `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | iframe usage | BillingSettingsContainer | Not tested | Not tested | **INVESTIGATE** |
| 3 | `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | Paid vs free breakdown | FpbInvoiceView | FpbInvoiceView-tests.tsx (4 tests) | invoice-details-page-tests.ts (2 tests) | Active, well tested |
| 4 | `BILLING_PAID_VS_FREE_DATE_GUARD` | Date filter for breakdown | FpbInvoiceView | FpbInvoiceView-tests.tsx (3 tests) | Not tested | Active, unit tested |
| 5 | `SHOW_NEW_INVOICE_DETAILS_PAGE` | New invoice view | (TORN DOWN a88b14cba6) | (tests deleted) | (tests deleted) | **DELETED** |

---

## Feature Flags (Server-Side Toggles)

| # | Flag | Controls | Where Used | Tested? | Notes |
|---|------|----------|-----------|---------|-------|
| 1 | `Billing.MinimumPaymentMethodLimit` | Min monthly limit ($500 default) | schemaBuilder.ts | Yes — EditMonthlyLimitModal-tests.tsx | Active flag |
| 2 | `Billing.EnableStripeSandbox` | Stripe sandbox mode | shouldUseStripeSandbox.ts | Yes — useShouldUseStripeSandbox-tests.ts (6 tests) | All branches covered |

---

## Entity Flags

| # | Flag | Controls | Where Used | Tested? |
|---|------|----------|-----------|---------|
| 1 | `shouldEnableStripeSandboxForPractice` | Per-practice Stripe sandbox | shouldUseStripeSandbox.ts | Yes — useShouldUseStripeSandbox-tests.ts |

---

## Detailed Findings & Actions

### SHOW_NEW_BILLING_MEZZ_REVAMP — Conditional Cleanup

**Status:** Still active in code

**Usage:**
- `BillingSettingsContainer.tsx` — Routes to V2 contact info section when ON
- `InvoiceDetailsContainer.tsx` — Routes to V2 invoice view when ON
- Enables V2 modals: EditBillingContactInfoModal, AddPaymentMethodModalV2, etc.

**Current test coverage:**
- billing-settings-v2-tests.ts (25 tests) — Always tests with flag ON
- billing-settings-page-tests.ts (35 tests) — Always tests with flag OFF (V1)

**If fully rolled out (100%):**
- Delete billing-settings-page-tests.ts (1,254 lines, V1 only)
- Delete V1 components (~600 lines)
- Keep billing-settings-v2-tests.ts only

**If still running:**
- Maintain both test suites
- Add experiment branch tests (ON/OFF) to unit tests

**Action:** Check AB platform for rollout status. If unknown, assume still running and keep both.

---

### BILLING_PAGE_ENABLE_IFRAME_DEPRECATION — Likely Dead

**Status:** Referenced but not tested

**Usage:**
- `BillingSettingsContainer.tsx` (lines ~200-210)
- No unit tests
- No Cypress tests
- Not found in any beforeEach or experiment setup

**Investigation:** Is this experiment:
1. **Concluded/deprecated?** → Delete the code (5 min cleanup)
2. **Still running?** → Add tests for both ON/OFF branches (1 hour)
3. **Fully ON?** → Remove the branch, simplify code (30 min)

**Action:** Search AB platform or Slack for recent mentions. Likely dead code.

---

### BILLING_PAGE_BREAKDOWN_PAID_VS_FREE — Well Tested

**Status:** Active, excellent test coverage

**Coverage:**
- 4 unit tests (FpbInvoiceView-tests.tsx)
  - ON + >= Jan 2026
  - ON + < Jan 2026 (date guard blocks)
  - OFF
  - Edge cases
- 2 Cypress tests (invoice-details-page-tests.ts)
  - ON display
  - OFF display

**Action:** No changes needed. Model for future experiments.

---

### Billing.MinimumPaymentMethodLimit — Well Tested

**Status:** Active, covered

**Coverage:**
- EditMonthlyLimitModal-tests.tsx (3 tests)
- EditMonthlyLimitModalV2-tests.tsx (11 tests)
- Tests check both minimum enforcement and validation error

**Action:** No changes needed.

---

### Billing.EnableStripeSandbox — Well Tested

**Status:** Active, all branches covered

**Coverage:**
- useShouldUseStripeSandbox-tests.ts (6 tests)
- Tests all 4 boolean combinations:
  1. Feature flag ON + entity flag ON → true
  2. Feature flag ON + entity flag OFF → false
  3. Feature flag OFF + entity flag ON → false
  4. Feature flag OFF + entity flag OFF → false

**Action:** No changes needed.

---

## Summary: Flag Cleanup Roadmap

| Flag | Status | Action | Effort | Urgency |
|------|--------|--------|--------|---------|
| `SHOW_NEW_BILLING_MEZZ_REVAMP` | Unknown | Check rollout status | 15 min | High |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | Likely dead | Audit in AB platform | 30 min | High |
| `SHOW_NEW_INVOICE_DETAILS_PAGE` | Deleted | ✓ Already done (a88b14cba6) | Done | — |
| `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | Active, tested | ✓ No action | — | — |
| `Billing.MinimumPaymentMethodLimit` | Active, tested | ✓ No action | — | — |
| `Billing.EnableStripeSandbox` | Active, tested | ✓ No action | — | — |

**Total estimated effort: ~45 minutes**

---

## Recommendations

1. **This week:** Check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout status. If 100%, schedule cleanup.
2. **This week:** Search for `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` in AB platform/Slack. If dead, delete code.
3. **Next sprint:** If V1 experiment is fully rolled out, delete all V1 code + tests (~2,364 lines).
4. **Ongoing:** When adding new feature flags, always include unit + Cypress tests (see `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` as model).

