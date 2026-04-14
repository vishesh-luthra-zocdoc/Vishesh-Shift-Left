# Cypress E2E Test Catalog — Billing

All Cypress specs, commands, page objects, and fixtures related to billing.

---

## Spec Files Overview

| File | Lines | Tests | UI Version |
|------|-------|-------|------------|
| billing-settings-page-tests.ts | 1,208 | 33 | V1 (Legacy) |
| billing-settings-v2-tests.ts | 628 | 13 | V2 (Mezzanine) |
| invoice-details-page-tests.ts | 64 | 2 | — |
| **Total** | **1,900** | **48** | |

---

## billing-settings-page-tests.ts (V1)

**1,208 lines** — this is the largest Cypress spec in billing. Tests the legacy UI before the Mezzanine redesign.

### Billing Settings Page (lines 52-952)

| # | Test | What It Does |
|---|------|-------------|
| 1 | shows error if practice id not passed | Error handling — no practiceId |
| 2 | shows error if fetch billing settings fails | Error handling — API failure |
| 3 | shows page if practice id passed | Happy path — page loads with 4 payment methods, 2 providers |
| 4 | shows error if set default payment method fails | Error handling — set default API |
| 5 | sets payment method as default | Happy path — set default + UI update |
| 6 | does not delete if cancelled in dialog | Cancel flow — delete confirmation |
| 7 | deletes payment method if confirmed | Happy path — delete + UI update |
| 8 | shows error if delete fails | Error handling — delete API |
| 9 | sets default payment method for provider | Happy path — per-provider assignment |
| 10 | shows error if set provider payment method fails | Error handling — per-provider API |
| 11 | updates billing email via modal | Happy path — email update flow |
| 12 | shows error if update billing email fails | Error handling — email API |
| 13 | updates primary business address via modal | Happy path — address update (5 fields) |
| 14 | shows error if update business address fails | Error handling — address API |
| 15 | adds ACH account via modal | Happy path — ACH addition (bank name, routing, account) |
| 16 | shows error if add ACH fails | Error handling — ACH API |
| 17 | adds credit card via modal | Happy path — credit card addition (name, card, address) |
| 18 | shows error if add credit card fails | Error handling — credit card API |
| 19 | updates rollovers via modal | Happy path — reorder + mark rollover methods |
| 20 | shows error if update rollovers fails | Error handling — rollover API |
| 21 | sets and removes monthly limit | Happy path — limit CRUD |
| 22 | shows edit rollovers dialog if limit set but no rollovers | Edge case — modal chaining |
| 23 | shows error if update monthly limit fails | Error handling — limit API |

### Tabs & Pricing (lines 954-1208)

| # | Test | What It Does |
|---|------|-------------|
| 24 | shows marketplace enrollments on pricing tab | Pricing tab visibility |
| 25 | shows pricing for providers | Provider pricing expansion |
| 26-30 | completion modal null field handling (5 tests) | Null address1/city/state/zip/email |
| 31 | shows completion modal on DOD completion | Completion modal with empty email |
| 32 | shows FAQ for marketplace users | FAQ visibility |
| 33 | pricing calculator works | 6-step calculator navigation |

---

## billing-settings-v2-tests.ts (V2)

**628 lines** — tests the new Mezzanine UI. All tests run with `SHOW_NEW_BILLING_MEZZ_REVAMP=ON`.

### Edit Rollovers (lines 31-134)

| # | Test | What It Does |
|---|------|-------------|
| 1 | opens modal, makes changes, verifies results | Rollover reordering + checkbox toggle |

### Payment Methods List (lines 136-317)

| # | Test | What It Does |
|---|------|-------------|
| 2 | sets a non-default payment method as default | Set default via more menu |
| 3 | sets a monthly limit (no existing limit) | Set initial limit |
| 4 | edits an existing monthly limit | Edit existing limit |
| 5 | deletes a non-default payment method | Delete with confirmation |

### Content Verification (lines 319-361)

| # | Test | What It Does |
|---|------|-------------|
| 6 | verifies payment methods list content | V2 payment methods display |

### Billing Contact Info (lines 362-593)

| # | Test | What It Does |
|---|------|-------------|
| 7 | verifies billing contact info content | Contact info display |
| 8 | prepopulates contact info fields | Form field prepopulation |
| 9 | requires required fields | Form validation |
| 10 | saves changes to contact info | Address + email update |
| 11 | error when updating address fails | Error handling — address |
| 12 | error when updating email fails | Error handling — email |

### Per-Provider Payment (lines 595-627)

| # | Test | What It Does |
|---|------|-------------|
| 13 | sets payment method for provider in modal | Per-provider assignment via V2 modal |

---

## invoice-details-page-tests.ts

**64 lines** — tests the invoice detail view.

| # | Test | What It Does |
|---|------|-------------|
| 1 | new vs existing bookings (experiment off) | Shows "104 new" + "35 existing" patient bookings |
| 2 | marketplace bookings (experiment on) | Shows "$3,132.00" with "56 Paid" + "48 Free" breakdown |

---

## Custom Commands

Defined in `billing-settings-page-commands.ts`:

| Command | Purpose |
|---------|---------|
| `setUpRoutesAndVisitBillingPage(practiceId, options)` | Sets up all 10 API intercepts + visits billing page |
| `hideBillingCompletionModal()` | Sets cookie/localStorage to suppress modal |
| `showBillingCompletionModal()` | Clears cookie/localStorage to show modal |
| `selectValueInDropdown(wrapper, value, key)` | Selects dropdown option |
| `clickBillByDate(date)` | Clicks invoice by date text |
| `openPaymentMethodMoreMenu(id)` | Opens payment method context menu |
| `setMonthlyLimitInModal(limit)` | Sets monthly limit value |
| `openSeeByProviderModal()` | Opens per-provider modal |
| `saveModalAndWait(alias)` | Saves modal + waits for API |
| `openEditRolloversModal()` | Opens rollover editor |

## Page Objects

| Page Object | Methods |
|-------------|---------|
| BillingSettingsPagePageObject | `verifyContactInfo(address, email)` |
| EditBillingContactInfoModalPageObject | `getInputField`, `typeInField`, `clearField`, `formIsValid`, `interceptSubmit*`, etc. |

## Experiments Configured in Tests

| Experiment | V1 Tests | V2 Tests |
|------------|----------|----------|
| `SHOW_NEW_BILLING_MEZZ_REVAMP` | Not set (defaults to off) | Always ON |
| `SHOW_NEW_INVOICE_DETAILS_PAGE` | Not set | Always ON |
| `BILLING_PAGE_BREAKDOWN_PAID_VS_FREE` | Not set | Toggled on/off per test |
