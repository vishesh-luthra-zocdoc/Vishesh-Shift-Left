# provider-fe-monorepo — L5 `e2e` Billing Inventory

| Field | Value |
|---|---|
| Repo | `provider-fe-monorepo` |
| Revision analyzed | `dd9e4952a6` (`origin/main`, 2026-09-03) |
| Snapshot path | `/tmp/slv3/snapshots/provider-fe-monorepo/` |
| Level | L5 `e2e` (Playwright) — see caveat in [Level caveat](#level-caveat) |
| Suite root | `apps/settings/e2e/` |
| Billing specs | 7 |
| Billing L5 tests | **63** |

Cypress no longer exists anywhere in this tree — `find . -iname '*cypress*'` returns zero files at
this revision. Every billing spec is Playwright. Several ported specs retain a file-header comment
naming their Cypress predecessor (e.g. `billing-settings-page-commands.ts:2`,
`billing-settings-v2.spec.ts:2-3`), which is the only remaining trace.

---

## Level caveat

All 63 tests drive a real Chromium browser against a running `apps/settings` Next-style server, so
by the taxonomy's rule 1 ("is a browser involved? → L5") they are all L5.

**But every backend response they consume is stubbed in-process by `page.route` + `route.fulfill`.**
No test in this set reaches a real billing API, a real database, or `js.stripe.com`. The full stub
table lives in `apps/settings/e2e/PracticeSettingsPages/billing-settings-page-commands.ts:188-359`
and the suite-wide fallbacks in `apps/settings/e2e/fixtures.ts:34-113`. Stripe.js itself is replaced
by a hand-written fake installed via `page.addInitScript` in `fixtures.ts:32`
(`shared/core/src/testing/installStripeJsFake.ts`).

The commands file states this explicitly at `billing-settings-page-commands.ts:5-9`:

> every response was either a fixed status or one of the imported mock constants, so a full stub is
> equivalent and avoids a live proxy dependency

Consequence: these tests pay L5 cost (browser boot, page load, flake) for what is, in confidence
terms, an L2/L3 multi-component-tree assertion. Per-test detail is in
[`e2e-infrastructure.md`](e2e-infrastructure.md) and
[`../../analysis-scratch/e2e-shift-left-candidates.md`](../../analysis-scratch/e2e-shift-left-candidates.md).

---

## Spec 1 — `apps/settings/e2e/PracticeSettingsPages/billing-settings-page.spec.ts`

| Field | Value |
|---|---|
| Tests | 7 |
| LOC | 214 |
| `describe` blocks | 2 (both top-level, siblings — no nesting) |

### Describe structure
```
test.describe('billing settings page')                          # :20  — 2 tests
test.describe('billing settings page - tabs and pricing features') # :52 — 5 tests
```

### Test titles (verbatim)
| # | Line | Describe | Title |
|---|---|---|---|
| 1 | :35 | `billing settings page` | `shows error if practice id not passed` |
| 2 | :43 | `billing settings page` | `shows error if fetch billing settings fails` |
| 3 | :123 | `billing settings page - tabs and pricing features` | `showing completion modal - does not error on null address1` |
| 4 | :142 | same | `showing completion modal - does not error on null city` |
| 5 | :161 | same | `showing completion modal - does not error on null state` |
| 6 | :180 | same | `showing completion modal - does not error on null zipCode` |
| 7 | :199 | same | `showing completion modal - does not error on null businessEmail` |

### User journey
Two unrelated journeys in one file:
1. **Error surfaces** — provider lands on `/provider/config/settings/billing` with no `practiceId`,
   or the settings fetch 400s; asserts the error page renders (`selectors.errorPage`).
2. **BillingCompletionModal null-safety** — first-visit modal renders without crashing when
   individual `businessAddress` fields or `practiceBillingEmail` are `null`. Tests 3–7 are the same
   test five times with a different field nulled; all assert only
   `verifyElemExists(billingSettingsPage.view)` + `verifyElemDoesNotExist(errorPage)`.

### Flags / experiment overrides
Set by `setUpRoutesAndVisitBillingPage` defaults (`billing-settings-page-commands.ts:86-99`):

| Experiment const | Assignment |
|---|---|
| `BILLING_PROVIDER_REPOSITIONING` | `on` (default) |
| `BILLING_UPDATED_CALCULATOR_COPY` | `off` (default) |
| `PAY_NOW_ENABLED` | `off` (default) |

Cookies: `SHOULD_MOCK_STRIPE=true` (:25-32, :58-65). **Note (SUPERSEDED — see orchestrator correction below): this cookie name appeared nowhere in the
snapshot's application source** — `grep -rn SHOULD_MOCK_STRIPE` matches only the seven spec files.
`UNVERIFIED —` whether it is read by app code outside the snapshot subtree, or is now dead. Stripe
faking is actually achieved by `installStripeJsFake` in `fixtures.ts:32`, unconditionally.

Clock: `page.clock.install({ time: '2026-04-15' })` (:23) / `'2026-02-15'` (:56).

### Network mocked / intercepted
All of `setUpRoutes` (see [Shared stub table](#shared-stub-table)), plus, inline at :71-120:
- `**/provider/v1/gql` → `getSkuMappings` (one `MarketPlace`/`Selected`/`NotActivated` SKU + one
  `NotStarted` Insurance task), `getEntityFlags` → `[]`, else `route.fallback()`.

Also `givenNavbarInfo` + `mockBootstrappedUserInfo` cookies for the empty-practice case (:36-37).

### Page objects
None. Uses `selectors.errorPage` and `selectors.billingSettingsPage.view` directly.

---

## Spec 2 — `apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts`

| Field | Value |
|---|---|
| Tests | 16 |
| LOC | 1,032 |
| `describe` blocks | 6 (1 outer + 5 nested) |

The file header (`:2-3`) says it is the port of `cypress/e2e/PracticeSettingsPages/billing-settings-v2-tests.ts`
**"(19 tests)"** but contains 16 `test()` blocks. Three tests are unaccounted for. `UNVERIFIED —`
resolving this needs `git show e44f4ff75f^:apps/settings/cypress/e2e/PracticeSettingsPages/billing-settings-v2-tests.ts`;
the snapshot has no `.git`.

### Describe structure
```
test.describe('billing settings page V2')                              # :41
├── test.describe('Edit rollovers')                                    # :55   — 1 test
├── test.describe('Payment methods list')                              # :174  — 5 tests
├── (bare)                                                             # :403  — 1 test
├── test.describe('Billing contact info')                              # :458  — 5 tests
├── (bare)                                                             # :704  — 1 test
├── test.describe('Set default payment method for provider')           # :744  — 1 test
└── test.describe('Pricing calculator V2')                             # :783  — 2 tests
```

### Test titles (verbatim)
| # | Line | Describe path | Title |
|---|---|---|---|
| 1 | :56 | `billing settings page V2 > Edit rollovers` | `opens modal, makes changes to modal and verifies results` |
| 2 | :175 | `billing settings page V2 > Payment methods list` | `opens modal, makes changes to modal and verifies results` |
| 3 | :181 | same | `sets a non-default payment method as default` |
| 4 | :228 | same | `sets a monthly limit for a payment method without a limit` |
| 5 | :278 | same | `edits an existing monthly limit for a payment method` |
| 6 | :341 | same | `deletes a non-default payment method` |
| 7 | :403 | `billing settings page V2` | `verifies payment methods list has the correct content` |
| 8 | :459 | `... > Billing contact info` | `verifies billing contact info has the correct content` |
| 9 | :474 | same | `prepopulates contact info fields` |
| 10 | :524 | same | `requires required fields` |
| 11 | :561 | same | `saves changes to contact info` |
| 12 | :659 | same | `displays an error message when updating primary business address fails` |
| 13 | :704 | `billing settings page V2` | `displays an error message when updating billing email fails` |
| 14 | :745 | `... > Set default payment method for provider` | `sets default payment method for a provider in the "See by provider" modal` |
| 15 | :838 | `... > Pricing calculator V2` | `opens V2 pricing calculator modal, steps through all inputs, and verifies calculated result` |
| 16 | :989 | same | `closes V2 pricing calculator modal when close button is clicked` |

### Defects found in this file
1. **Test 2 (`:175-179`) has an empty body.** It calls
   `setUpRoutesAndVisitBillingPage(page, practiceId, {})` and nothing else — zero assertions. Its
   title is a verbatim copy of test 1's title, so it is almost certainly a copy-paste leftover. It
   burns a full browser+page-load and can only fail on a page crash.
2. **Six tests wrap their entire body in `if (...)` on mock lookup.** Tests 3, 4, 5, 6, 7, 14 do
   `const x = mock...paymentMethods.find(pred); if (x) { ...all assertions... }`. If the mock
   fixture (`apps/settings/src/server/controllers/practiceBillingSettingsPage/mocks.ts:11`) ever
   stops satisfying the predicate, these tests **pass while asserting nothing**. Evidence: :191,
   :241, :288, :349, :425, :759.

### User journeys
- V2 payment-method row lifecycle: set-as-default, set/edit monthly limit, delete (with confirm
  modal), rollover ordering.
- Billing contact info (business address + billing email) read, prepopulate, validate, save,
  and both failure branches.
- Per-provider default payment method via the "See by provider" modal.
- V2 yearly-value pricing calculator: 5-step wizard, back navigation, result (`327`), start-over.

### Flags / experiment overrides
| Experiment | Value | Where |
|---|---|---|
| `BILLING_PROVIDER_REPOSITIONING` | `on` (default) | commands :88-91 |
| `BILLING_UPDATED_CALCULATOR_COPY` | `off` default; **`on`** for tests 15 & 16 | :842, :993 |
| `PAY_NOW_ENABLED` | `off` (default) | commands :96-98 |

Cookies: `SHOULD_MOCK_STRIPE=true` (:44-51); `has_seen_billing_completion_modal=true` +
matching `localStorage` key via `hideBillingCompletionModal` (:52). No `page.clock` in this file.

### Network mocked / intercepted
- Full `setUpRoutes` stub table.
- `**/provider/v1/gql` inline in the `Pricing calculator V2` `beforeEach` (:787-835):
  `getSkuMappings` → one `MarketPlace`/`Selected`/**`Activated`** SKU, no tasks;
  `getEntityFlags` → `[]`.
- `EditBillingContactInfoModalPageObject.interceptSubmitPrimaryBusinessAddress` /
  `interceptSubmitBillingEmail` re-stub `PUT .../primaryBusinessAddress` and `PUT .../billingEmail`
  per test with an explicit status (200 for test 11; 500 for tests 12, 13).

### Page objects used
- `pageObjects/BillingSettingsPagePageObject.ts` → `billingSettingsPagePageObject.verifyContactInfo`
- `pageObjects/EditBillingContactInfoModalPageObject.ts` → `editBillingContactInfoModalPageObject`
  (14 methods used)

---

## Spec 3 — `apps/settings/e2e/PracticeSettingsPages/billing-settings-payment-element.spec.ts`

| Field | Value |
|---|---|
| Tests | 4 |
| LOC | 143 |
| `describe` blocks | 1 |

### Describe structure
```
test.describe('Add Payment Method — Unified PaymentElement flow')  # :19 — 4 tests
```

### Test titles (verbatim)
| # | Line | Title |
|---|---|---|
| 1 | :30 | `renders the unified form with no type-picker` |
| 2 | :44 | `submits the unified form and saves a payment method` |
| 3 | :63 | `reuses the confirmed payment method when saving again after a failure` |
| 4 | :105 | `runs the full flow again when the payment details are edited after a failure` |

### User journey
Provider clicks **Add payment method** on the billing page and gets the unified Stripe
PaymentElement modal (no card-vs-ACH type picker). Covers: render shape (no type picker), happy-path
save, and the two setup-intent-reuse branches after a save failure — retry with unchanged details
must reuse the confirmed payment method (1 setup-intent, 2 payment-method POSTs), whereas editing
the details must re-run confirmation (2 setup-intents).

### Flags / experiment overrides
| Experiment | Value | Where |
|---|---|---|
| `BILLING_PROVIDER_REPOSITIONING` | **`off`** (explicit override, all 4 tests) | :25-28 |
| `BILLING_UPDATED_CALCULATOR_COPY` | `off` (default) | commands :92-95 |
| `PAY_NOW_ENABLED` | `off` (default) | commands :96-98 |

Cookies: `has_seen_billing_completion_modal` via `hideBillingCompletionModal` (:22).
**No `SHOULD_MOCK_STRIPE` cookie and no `page.clock`** — unlike the other six specs.

### Network mocked / intercepted
- Full `setUpRoutes` stub table, notably:
  - `POST **/billing-monolith-api/v1/practice/*/setup-intents` → `200 {client_secret: 'seti_mock_secret_123'}`
    (commands :330-344)
  - `POST **/billing-monolith-api/v1/practice/*/payment-methods` → `200 {payment_method_info: mockCreditCardInfo}`
    (commands :346-358)
- Tests 3 & 4 override `POST /payment-methods` → **400** via `mockPostRoute` (:82, :120).
- Tests 3 & 4 attach a `page.on('request')` listener to **count** POSTs to `/setup-intents` and
  `/payment-methods` (:70-80, :111-118) — this is a request-contract assertion (`toHaveLength(1)` /
  `toHaveLength(2)`), i.e. L4-shaped logic executed in a browser.

### Page objects
None.

---

## Spec 4 — `apps/settings/e2e/PracticeSettingsPages/billing-invoice-summary.spec.ts`

| Field | Value |
|---|---|
| Tests | 20 |
| LOC | 348 |
| `describe` blocks | 8 (1 outer + 7 nested) |

### Describe structure
```
test.describe('billing invoice summary page')                        # :45
├── test.describe('Formatting for items')                            # :73   — 8 tests
├── test.describe('Button for PDF')                                  # :171  — 1 test
├── test.describe('Navigation to left (Billing history sidebar)')    # :186  — 3 tests
├── test.describe('General formatting for hover states / tags')      # :211  — 3 tests
├── test.describe('Back to Billing link')                            # :249  — 2 tests
├── test.describe('Healthcare platforms row')                        # :270  — 2 tests
└── test.describe('Booking source breakdown (API-driven)')           # :296  — 1 test
```

### Test titles (verbatim)
| # | Line | Describe | Title |
|---|---|---|---|
| 1 | :74 | `Formatting for items` | `should display invoice title in "Month Year" format` |
| 2 | :82 | same | `should display "Sponsored Results fees*" with asterisk` |
| 3 | :92 | same | `should display collapsible taxes and fees section with line items` |
| 4 | :107 | same | `should display collapsible marketplace bookings with paid and free breakdown` |
| 5 | :129 | same | `should display "Total" label with correct amount` |
| 6 | :138 | same | `should display "Zocdoc credits" when credits are applied` |
| 7 | :146 | same | `should display amount due row` |
| 8 | :155 | same | `should display footer with Eastern Time note and billing link` |
| 9 | :172 | `Button for PDF` | `should render PDF button when PDF is available` |
| 10 | :187 | `Navigation to left (Billing history sidebar)` | `should display "Invoices" as sidebar title` |
| 11 | :193 | same | `should show checkmark on the currently selected bill` |
| 12 | :203 | same | `should list multiple bills in the sidebar` |
| 13 | :212 | `General formatting for hover states / tags` | `should display "Paid" status tag on paid bills` |
| 14 | :222 | same | `should display status tags on sidebar bills with correct text` |
| 15 | :235 | same | `should show checkmark on the selected bill row in the sidebar` |
| 16 | :250 | `Back to Billing link` | `should display "Back to Billing" link` |
| 17 | :256 | same | `should have a clickable "Back to Billing" link` |
| 18 | :271 | `Healthcare platforms row` | `shows "{count} from Healthcare platforms" for a post-cutoff bill` |
| 19 | :286 | same | `does not show the Healthcare platforms row for a pre-cutoff bill` |
| 20 | :297 | `Booking source breakdown (API-driven)` | `renders the new source rows with their values and correct order` |

### User journey
Provider opens the billing page, clicks the **Jan 2026** bill row, lands on the FPB invoice summary
(`navigateToInvoiceSummary`, :60-71 — identical setup for all 20 tests) and reads the invoice: title,
Sponsored Results line, collapsible taxes-and-fees, collapsible marketplace bookings, total, Zocdoc
credits, amount due, footer, PDF button, sidebar bill list with status tags and selection checkmark,
Back-to-Billing link. Tests 18 & 20 swap in an August-2026 bill (`augustBillSummaryResponse`, :30-43)
to get past the `FpbInvoiceView` booking-period cutoff and render the API-driven booking-source rows.

### Notable weak assertions
- Tests 11 and 15 assert the same thing two ways: `bill-selected-check` is visible (:198-200) vs a
  `bill-row:has(bill-selected-check)` is visible (:240-245).
- Tests 12 and 14 assert only `toBeGreaterThanOrEqual(2)` / `(1)` on a count. Test 14's own comment
  says the mock has Paid / PartiallyPaid / Unpaid, but the assertion never checks the text.
- Test 17 asserts `toBeAttached()` on a filtered locator — "clickable" is never exercised.
- Test 9 asserts the PDF button is visible and contains "PDF". **Nothing clicks it**; no download
  is asserted anywhere in the L5 suite.

### Flags / experiment overrides
Defaults only (`BILLING_PROVIDER_REPOSITIONING=on`, `BILLING_UPDATED_CALCULATOR_COPY=off`,
`PAY_NOW_ENABLED=off`). Cookie `SHOULD_MOCK_STRIPE=true` (:50-57).
Clock: `page.clock.install({ time: '2026-04-15' })` (:48).
Test 19 additionally sets `mockUserInfo` with `is_internal_user: false` via `givenIsInternalUser`
(:289).

### Network mocked / intercepted
- Full `setUpRoutes` stub table. `GET **/billing-monolith-api/v1/bill/*/summary` returns
  `mockBillSummaryResponse` (commands :316-328), overridden per test via the
  `billSummaryResponse` option for tests 18 and 20.
- No inline `page.route` in this file; it inherits `fixtures.ts` fallbacks only.

### Page objects
None.

### Test data
`mockBillSummaryResponse` (`apps/settings/src/server/controllers/practiceBillingSettingsPage/mocks.ts:398`)
and `mockBookingSourceBreakdown`
(`apps/settings/src/pages/settingsPages/billingSettings/fixtures/bookingSourceBreakdownFixtures.ts`) —
both are **production source files**, not `e2e/` fixtures. Hard-coded expected amounts: `$8,570.00`
(:135), `$50.00` / `$30.00` (:313, :320).

---

## Spec 5 — `apps/settings/e2e/PracticeSettingsPages/billing-pricing-v2.spec.ts`

| Field | Value |
|---|---|
| Tests | 11 |
| LOC | 292 |
| `describe` blocks | 1 |

### Describe structure
```
test.describe('billing settings page - V2 pricing tab (BILL-193)')  # :170 — 11 tests
```

### Test titles (verbatim)
| # | Line | Title |
|---|---|---|
| 1 | :185 | `renders V2 pricing tab` |
| 2 | :190 | `shows FAQs section on V2 pricing tab` |
| 3 | :195 | `FAQ items expand and collapse on click` |
| 4 | :225 | `shows V2 marketplace card when enrolled in marketplace` |
| 5 | :234 | `opens price by provider modal when "View price by provider" link is clicked` |
| 6 | :245 | `shows bookable presence card` |
| 7 | :250 | `shows marketplace card when marketplace SKU is selected but not activated` |
| 8 | :258 | `shows FAQs when marketplace SKU is selected but not activated` |
| 9 | :265 | `does not show FAQs section when no SKUs are selected` |
| 10 | :274 | `shows the 5th FAQ about controlling monthly spend` |
| 11 | :284 | `shows the FAQ about what bookings are charged for` |

### User journey
Provider opens `/provider/config/settings/billing#pricing` and reads the V2 pricing tab: marketplace
price card, bookable-presence card, price-by-provider modal, FAQ accordion, and the not-enrolled
empty state. Three setup variants differ only in the `getSkuMappings` payload
(`visitV2PricingTab` :23-81 = Marketplace+Intake Activated; `visitV2PricingTabInactiveMarketplace`
:83-131 = Marketplace Selected/NotActivated; `visitV2PricingTabEmpty` :133-168 = `skuMappings: []`).

Each setup calls `setUpRoutesAndVisitBillingPage` and then **immediately navigates again** to
`pricingUrl` (:79-80) — two full page loads per test, 22 loads for the file.

### Flags / experiment overrides
Defaults (`BILLING_PROVIDER_REPOSITIONING=on`, `BILLING_UPDATED_CALCULATOR_COPY=off`,
`PAY_NOW_ENABLED=off`). Cookies: `SHOULD_MOCK_STRIPE=true` (:174-181),
`has_seen_billing_completion_modal` (:182). Clock: `'2026-02-15'` (:172).
Viewport 1200×900 (:173) — the only billing spec that is not 1000×1000.

Entity flag: `getEntityFlags` → `['IsCreatedViaRepositionFlow']` in all three setups (:71, :121, :158).

### Network mocked / intercepted
- Full `setUpRoutes` stub table.
- `**/provider/v1/gql` → `getSkuMappings` (per-variant payload), `getEntityFlags` →
  `['IsCreatedViaRepositionFlow']`, else `route.fallback()`.

### Page objects
None. Uses `selectors.billingSettingsPage.pricingTabV2` (aliased `pricingV2Selectors`, :20).

---

## Spec 6 — `apps/settings/e2e/PracticeSettingsPages/invoice-details-page.spec.ts`

| Field | Value |
|---|---|
| Tests | 1 |
| LOC | 60 |
| `describe` blocks | 1 |

### Describe structure
```
test.describe('invoice details page')  # :17 — 1 test
```

### Test title (verbatim)
| # | Line | Title |
|---|---|---|
| 1 | :33 | `should display marketplace bookings section with paid and free breakdown` |

### User journey
Identical navigation to spec 4: billing page → click **Jan 2026** bill → expand
`marketplace-bookings-header`. Asserts the header total `$3,132.00`, then `56 Paid bookings` /
`$3,132.00` and `48 Free bookings` / `$0.00` in the body.

This is a stricter version of spec 4 test 4 (`should display collapsible marketplace bookings with
paid and free breakdown`, `billing-invoice-summary.spec.ts:107`), which asserts only that the
strings `Paid bookings` and `Free bookings` appear. Same URL, same click, same fixture, same
section. See the shift-left sheet for the verdict.

### Flags / experiment overrides
Defaults. `SHOULD_MOCK_STRIPE=true` (:23-30). Clock `'2026-02-15'` (:21).
`givenIsInternalUser(page, false)` (:36).

### Network mocked / intercepted
Full `setUpRoutes` stub table only; no inline routes.

### Page objects
None.

---

## Spec 7 — `apps/settings/e2e/PracticeSettingsPages/payment-recovery.spec.ts`

| Field | Value |
|---|---|
| Tests | 4 |
| LOC | 291 |
| `describe` blocks | 1 |

This spec was **not** in the assigned file list but is a billing spec by any reading: it lives in
`PracticeSettingsPages/`, imports `billing-settings-page-commands`, and drives the billing page's
payment-recovery banner and Pay-Now modal.

### Describe structure
```
test.describe('payment recovery - Pay Now flow')  # :31 — 4 tests
```

### Test titles (verbatim)
| # | Line | Title |
|---|---|---|
| 1 | :96 | `banner -> review -> pay -> single success outcome banner` |
| 2 | :156 | `update-only mode: banner -> Update -> new card persists immediately, no charge, confirmation shown` |
| 3 | :233 | `opens the modal at the top when the review step overflows` |
| 4 | :276 | `renders the banner headline and sub-line without decline codes` |

### User journey
Failed-payment recovery. Test 1 is the legacy stage-then-charge happy path: recovery banner CTA →
`pay-now-modal` → failed-payments list keyed `failed-payments-month-2026-06-method-1` →
`pay-now-submit` → `POST /pay-now` → modal closes → `recovery-outcome-banner` with
`data-variant="single.success"`. Test 2 is the BILL-971 update-only path: no charge affordances,
per-row **Update** opens card entry, fills the V2 credit-card form, setup-intent + payment-method
round-trip, stays on review, closing raises a toast (`"We'll retry the charge the next business
day."`) and suppresses the banner until `localStorage` is cleared and the page reloaded. Test 3 is a
layout regression (BILL-1083: modal must open at `scrollTop === 0` when the review step overflows a
600px-high viewport). Test 4 asserts banner copy names the card (`on Visa ending in 1234`) and never
leaks raw Stripe decline codes (`card_declined`, `insufficient_funds`).

This file documents its own level discipline at :23-30 and :221-232 — it states that decline /
HTTP-error branches deliberately live in the `PayNowModal` + `usePaymentRecoveryFlow` RTL suites, and
that test 3 is here only because jsdom has no layout. It is the only billing spec in the repo that
reasons explicitly about the pyramid.

### Flags / experiment overrides
| Experiment | Test 1 | Test 2 | Test 3 | Test 4 |
|---|---|---|---|---|
| `PAYMENT_RECOVERY_EXPERIENCE` | `on` | `on` | `on` | `on` |
| `REVIEW_AND_PAY_CTA` | `on` | `on` | `on` | — |
| `PAY_NOW_ENABLED` | **`on`** | **`off`** (explicit) | `off` (default) | `off` (default) |
| `BILLING_PROVIDER_REPOSITIONING` | `on` (default) | `on` | `on` | `on` |
| `BILLING_UPDATED_CALCULATOR_COPY` | `off` (default) | `off` | `off` | `off` |

Cookie `SHOULD_MOCK_STRIPE=true` (:34-41). No `page.clock`. Test 3 sets viewport 1000×600 (:241);
others inherit 1000×1000 (:33). Test 3 uses `recoveryScenario: 5` (:246); others default to
scenario 1 (commands :220).

### Network mocked / intercepted
- Full `setUpRoutes` stub table.
- `GET **/billing-monolith-api/v1/practice/*/recovery` → `getMockRecoveryResponse(scenario)`
  (commands :222-231)
- `GET **/billing-monolith-api/v1/practice/*/recovery/balance-detail` →
  `getMockRecoveryBalanceDetailResponse(scenario)` (commands :233-244)
- `**/provider/v1/gql` inline (:45-72): `getSkuMappings` → empty `skuMappings`, `getEntityFlags` → `[]`
- `POST **/spo-provider/v1/management/*/pay-now` → `200 {succeeded_count: 1, remaining_failures: 0}`
  (:78-93) — **the charge itself is stubbed**

### Page objects
None. Uses raw `data-test` strings throughout.

---

## Summary table

| Spec | Tests | LOC |
|---|---|---|
| `billing-invoice-summary.spec.ts` | 20 | 348 |
| `billing-settings-v2.spec.ts` | 16 | 1,032 |
| `billing-pricing-v2.spec.ts` | 11 | 292 |
| `billing-settings-page.spec.ts` | 7 | 214 |
| `billing-settings-payment-element.spec.ts` | 4 | 143 |
| `payment-recovery.spec.ts` | 4 | 291 |
| `invoice-details-page.spec.ts` | 1 | 60 |
| **Total (specs)** | **63** | **2,380** |
| `billing-settings-page-commands.ts` (support) | 0 | 562 |
| `selectors.ts` (support, shared with `create-staff-page-v2`) | 0 | 200 |
| `pageObjects/EditBillingContactInfoModalPageObject.ts` | 0 | 185 |
| `pageObjects/BillingSettingsPagePageObject.ts` | 0 | 46 |
| `pageObjects/PageObject.ts` | 0 | 18 |
| **Total incl. billing support code** | **63** | **3,391** |

Ratio: **1.9 lines of support code per line of spec logic in `billing-settings-v2.spec.ts`'s
neighbourhood**, and 63 tests across 3,391 lines = 54 LOC per test.

---

## Shared stub table

Registered by `setUpRoutes` (`billing-settings-page-commands.ts:188-359`) for **every** billing test.

| Path glob | Method | Stubbed response | Line |
|---|---|---|---|
| `/api/rest/provider/v1/settings/billing/*` | GET | `mockPracticeBillingSettingsViewModel` (or `customResponse`); `400` if `doesBillingSettingsFetchFail` | :192-214 |
| `.../recovery` | GET | `getMockRecoveryResponse(n)` — only when `enablePaymentRecovery` | :222-231 |
| `.../recovery/balance-detail` | GET | `getMockRecoveryBalanceDetailResponse(n)` — only when `enablePaymentRecovery` | :233-244 |
| `.../billing/*/*/setDefaultPaymentMethod` | POST | `204` (or `500`) | :247-256 |
| `.../billing/*/*` | DELETE | `204` (or `500`) | :258-267 |
| `.../billing/*/*/*/setPaymentMethod` | POST | `204` (or `500`) | :269-281 |
| `.../billing/*/billingEmail` | PUT | `204` (or `500`) | :283-292 |
| `.../billing/*/primaryBusinessAddress` | PUT | `204` (or `500`) | :294-303 |
| `.../billing/*/savePaymentMethodAttributes` | POST | `204` (or `500`) | :305-314 |
| `**/billing-monolith-api/v1/bill/*/summary` | any | `mockBillSummaryResponse` (or `400`) | :316-328 |
| `**/billing-monolith-api/v1/practice/*/setup-intents` | POST | `{client_secret: 'seti_mock_secret_123'}` | :330-343 |
| `**/billing-monolith-api/v1/practice/*/setup-intents~withCustomer` | POST | same | :344 |
| `**/billing-monolith-api/v1/practice/*/payment-methods` | POST | `{payment_method_info: mockCreditCardInfo}` | :346-358 |

Plus the `fixtures.ts` suite-wide fallbacks: `GET **/login/*` → `500` (:34-41),
`POST **/provider/v1/gql` → fixed org / `{data:{}}` (:43-81), `**/auth/checksession` (:83-89),
`**/auth/touchsession` (:91-97), `**/auth/user/v1/refresh` (:99-105),
`POST **/phi-ab/v1/assignments` → `route.continue()` (:107-113).

`setupNewAbExperiments` (`helpers.ts:828-860`) additionally stubs
`GET **/phi-ab/v1/www/experiments*` → `200` and `POST **/phi-ab/v1/assignments` → `201`. Note
`fixtures.ts:107` registers a `route.continue()` for the same POST path; Playwright runs the
**most-recently-registered** matching handler first, and `setupNewAbExperiments` is invoked from
`setUpRoutesAndVisitBillingPage` (commands :115) after the fixture, so the `201` stub wins for
billing tests. The fixture's `route.continue()` is therefore unreachable for the billing suite.

---

## Specific Findings

### 1. Are the V1 and V2 billing settings specs both still present, and do they duplicate each other?

**Both are present. They do not duplicate each other. The real duplication is elsewhere.**

| Spec | Tests | LOC |
|---|---|---|
| `billing-settings-page.spec.ts` ("V1") | 7 | 214 |
| `billing-settings-v2.spec.ts` ("V2") | 16 | 1,032 |

Overlap between these two files: **0 shared test titles, 0 overlapping assertions.** They have been
carved into disjoint responsibilities:

- `billing-settings-page.spec.ts` now holds **only** two error surfaces (missing `practiceId`,
  settings fetch 400) and five `BillingCompletionModal` null-field smoke tests. It asserts nothing
  about payment methods, contact info, or pricing.
- `billing-settings-v2.spec.ts` holds every feature test for the V2 payment-method list, contact
  info, per-provider defaults, and the V2 calculator.

The "V1 / V2" naming is misleading: `_v2` refers to the **V2 UI components**
(`payment-method-row-v2`, `pricingTabV2`), not to a second generation of the same suite. There is no
V1-vs-V2 redundancy to reclaim here.

Where duplication **does** exist:

| Pair | Overlap | Evidence |
|---|---|---|
| `invoice-details-page.spec.ts:33` vs `billing-invoice-summary.spec.ts:107` | Same navigation, same section, same fixture. The former is a strict superset (asserts exact `$3,132.00` / `56` / `48`); the latter asserts only that the labels appear. **1 of 1 tests in `invoice-details-page.spec.ts` is redundant.** | both expand `marketplace-bookings-header` after `clickBillByDate(page, 'Jan 2026')` |
| `billing-settings-v2.spec.ts` `Pricing calculator V2` (2 tests, :838, :989) vs `billing-pricing-v2.spec.ts` (11 tests) | Both render the V2 pricing tab through the same `getSkuMappings` stub shape. `billing-pricing-v2.spec.ts:185` (`renders V2 pricing tab`) re-asserts `pricingTabV2.view`, which `billing-settings-v2.spec.ts:848-850` already asserts as a precondition. **2 tests overlap on tab-render setup**; the calculator wizard itself is unique to `billing-settings-v2.spec.ts`. | :846-850 vs :186-187 |
| `billing-invoice-summary.spec.ts:193` vs `:235` | Two tests, one behaviour (`bill-selected-check` visible). | :198-200 vs :240-245 |

Quantified: **4 of 63 billing L5 tests (6.3%) are intra-suite duplicates** — 1 (`invoice-details-page`),
2 (pricing-tab render), 1 (`bill-selected-check`).

### 2. `billing-settings-page.spec.ts` — 1,254 Cypress lines → what now?

**214 lines. A 1,040-line (83%) reduction in that one file — but the suite as a whole grew.**

| | Lines | Tests |
|---|---|---|
| `billing-settings-page.spec.ts` — Cypress (per v2 analysis, not independently verifiable here) | 1,254 | UNVERIFIED |
| `billing-settings-page.spec.ts` — Playwright at `dd9e4952a6` | **214** | 7 |

The file did not shrink by deleting coverage; it shrank by **redistribution**. Three destinations
absorbed the content:

1. **Support extraction** — 562 lines moved into `billing-settings-page-commands.ts` (the
   `setUpRoutes` stub table, `waitFor*` helpers, `clickBillByDate`, `setMonthlyLimitInModal`,
   `openEditRolloversModal`, …) plus 200 lines of `selectors.ts` and 249 lines of page objects.
   This support code is shared by all seven billing specs, so its cost is amortized rather than
   removed.
2. **New sibling specs** — `billing-invoice-summary.spec.ts` (348), `billing-pricing-v2.spec.ts`
   (292), `payment-recovery.spec.ts` (291), `billing-settings-payment-element.spec.ts` (143),
   `invoice-details-page.spec.ts` (60) did not exist as separate Cypress files with these names.
3. **Genuine downward migration** — the file's own remaining tests are the residue that could not
   move: error pages and null-field crash smoke tests.

Net: the **billing L5 footprint grew** from a single 1,254-line file to 2,380 spec lines + 1,011
support lines = **3,391 lines / 63 tests**. Caveat: `UNVERIFIED —` I cannot compare the pre-deletion
Cypress totals across all billing files, only the one line count quoted from the v2 analysis. To
verify, `git show e44f4ff75f^ --stat -- apps/settings/cypress/e2e/PracticeSettingsPages/` in a full
clone.

### 3. What does `billing-settings-payment-element.spec.ts` cover, and is the Stripe Payment Element actually exercised or mocked?

**Coverage:** 4 tests over the unified Stripe PaymentElement add-payment-method modal —
(a) the modal renders one unified form with no card-vs-ACH type picker, (b) a happy-path save
round-trips `POST /setup-intents` then `POST /payment-methods` and shows "Payment method added",
(c) after a 400 on `/payment-methods`, retrying with **unchanged** details reuses the already-confirmed
payment method (setup-intent POST count stays at 1 while payment-method POSTs reach 2), and
(d) after a 400, **editing** the details re-runs confirmation (setup-intent POST count reaches 2).

**The Payment Element is entirely mocked. There is no Stripe iframe and no request to Stripe.**

Evidence chain:
1. `apps/settings/e2e/fixtures.ts:32` — `await page.addInitScript(installStripeJsFake)` runs for
   **every** test in `apps/settings/e2e`, unconditionally, before any app code.
2. `shared/core/src/testing/installStripeJsFake.ts:21-129` assigns a hand-written object to
   `window.Stripe`. Its own docstring (:1-20) states: *"`@stripe/stripe-js`'s loader resolves with an
   existing `window.Stripe` rather than injecting its script tag, so nothing is requested from
   js.stripe.com and no publishable key is needed."*
3. The fake's `mount()` (:31-54) appends a plain
   `<input data-test="mock-stripe-<type>-input">` to the target node. It is not an iframe. The spec
   drives exactly that element: `type(page, 'mock-stripe-payment-input', 'test')` (:52, :86, :124).
4. `confirmSetup` (:113-119) is a stub that **always** resolves
   `{setupIntent: {status: 'succeeded', payment_method: 'pm_fake_unified'}}`. No card is validated,
   no 3DS is possible, no Stripe error branch can occur.
5. `POST /setup-intents` is stubbed to return a literal `client_secret: 'seti_mock_secret_123'`
   (`billing-settings-page-commands.ts:337-339`) — a string Stripe would reject.

What these 4 tests genuinely prove: the app's own **client-side state machine** around confirmation
reuse (the `useConfirmPaymentSetup` invalidate-on-change contract) and the request sequence it
emits. What they cannot prove: card validation, declines, 3DS, ACH microdeposits, Stripe error
mapping, real `client_secret` handling, or that the Element renders at all in a real browser.

The same contract is already asserted at L2/L1 without a browser:
`shared/core/src/billing/__tests__/useConfirmPaymentSetup-tests.tsx:163`
(`it('reuses the confirmed payment method on retry without a second intent')`) and `:176`
(`it('confirms again once the entered details change')`); plus
`shared/core/src/components/AddPaymentMethodModal/__tests__/AddPaymentMethodElementModal-tests.tsx:239`
(`it('invalidates the confirmed payment method when the details change')`) and `:141`
(`it('renders the modal shell around the payment element fields')`).

**This is the sharpest shift-left finding in the L5 billing suite: a spec named for Stripe's Payment
Element never touches Stripe, and its four behaviours are each already covered by a named RTL test.**

### 4. Total billing E2E test count and estimated runtime

**Count: 63 tests across 7 spec files** (exact — every `test()` block enumerated above).

**Runtime: 10–16 minutes serial (estimate).** Basis, stated because this figure is inferred:

- No CI configuration, `playwright.config.ts`, or CI log exists in the snapshot
  (`find . -name 'playwright*.config.*'` → zero results; the snapshot contains only
  `apps/settings/e2e/`, `apps/settings/src/`, `apps/spo-webapp/src/`,
  `apps/provider-home-webapp/src/`, `shared/core/src/`). No recorded runtime is available.
- Every test performs at least one full `page.goto` gated on
  `expect(global-loading-spinner).toHaveCount(0, {timeout: 10000})` (`helpers.ts:614-628`).
  `billing-pricing-v2.spec.ts` performs **two** page loads per test (:79-80), i.e. 22 loads for 11
  tests.
- Total page loads across the suite: 63 baseline + 11 extra from `billing-pricing-v2.spec.ts` + 1
  reload in `payment-recovery.spec.ts:220` = **75 (estimate)**.
- Assuming 6–12s per test (mocked responses are instant, so cost is browser context + page load +
  React hydration + the ~5s of interaction in the heavier modal/wizard tests), 63 × 6–12s ≈
  **6.3–12.6 min**, plus fixed worker startup → **10–16 min serial (estimate)**.
- **Wall-clock will be far lower.** Because every test stubs its own backend and shares no mutable
  state, these specs are safely parallel — unlike the `sandbox` billing specs, which share one real
  practice and must run `--workers=1`. At 4 workers this suite is ~3–4 min (estimate).
- `UNVERIFIED —` an exact figure requires a CI run (`yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-*.spec.ts payment-recovery.spec.ts --reporter=json`)
  or a TeamCity build log.

For contrast, the 63 L5 tests' nearest lower-level equivalents run in-process: the billing L2/L1
suites under `apps/settings/src/pages/settingsPages/billingSettings/__tests__/` and
`shared/core/src/billing/__tests__/` are jsdom Jest files (10–200 ms/test per the taxonomy), so the
same behaviours cost roughly **two orders of magnitude less** at L2.

---

## Candidate Gaps

Billing user journeys with **no** L5 coverage at this revision. Each row is verified by searching
the seven billing specs for the relevant affordance.

| # | Missing journey | Correct level | File(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| 1 | **Add ACH / bank account end-to-end.** Zero L5 coverage. `grep -in 'ach\|bank\|routing' PracticeSettingsPages/*.spec.ts` matches only the word `beforeEach`. `mockAchInfo` exists (`mocks.ts:143`) but is only injected into a **read** list via `getPaymentMethodsWithoutRollovers` (commands :203-208) — no spec sets that option. L2 exists (`AchFormContentV2-handleConnectBank-tests.tsx`, `AchFormContentV2-schema-tests.ts`) but nothing proves the ACH branch of the unified PaymentElement modal reaches a save. | L5 e2e (add) — the microdeposit/bank-connect handoff cannot be asserted in jsdom | new spec under `apps/settings/e2e/PracticeSettingsPages/`; subject `shared/core/src/components/AddPaymentMethodModal/` | ACH is the cheapest rail for large practices. A broken ACH add means the practice cannot pay at all and lands in collections. Money-critical. | 1d | **P0** |
| 2 | **Add a card against real Stripe.** All 4 payment-element tests run on `installStripeJsFake`; `confirmSetup` always succeeds (`installStripeJsFake.ts:113-119`). Nothing anywhere in this repo proves a real Stripe Element mounts, validates a card, or that a real `client_secret` is consumed. | L5 e2e (add) against Stripe test mode | new spec; subject `shared/core/src/billing/useConfirmPaymentSetup.ts`, `getBillingStripePromise.ts` | A Stripe.js major-version bump, a publishable-key misconfiguration, or a CSP change breaks card entry in production and **every existing test still passes** — the fake has no dependency on Stripe at all. Money-critical. | 1d | **P0** |
| 3 | **Payment failure → recovery → successful re-charge with a real charge.** `payment-recovery.spec.ts:78-93` stubs `POST /pay-now` to `{succeeded_count: 1, remaining_failures: 0}`. No test observes a real decline, a partial success (`remaining_failures > 0`), or the multi-method outcome variants. `deriveOutcome`/`resolvePaymentOutcome` are L1-covered, but the wiring to a real charge is not covered at any level. | L4 api (charge contract) + L5 e2e (one real recovery happy path) | `apps/settings/e2e/PracticeSettingsPages/payment-recovery.spec.ts`; subject `.../billingSettings/PaymentRecovery/` | The recovery flow exists specifically to un-break failed money collection. A stubbed 200 proves the UI renders a success banner, not that the provider was charged. | 1d | **P0** |
| 4 | **Invoice PDF download.** `billing-invoice-summary.spec.ts:172-183` asserts the button is visible and says "PDF". Nothing clicks it; no `page.waitForEvent('download')` exists in any billing spec (`grep -in download PracticeSettingsPages/*.spec.ts` → 1 match, the selector name). Fetch-and-download logic is L2-covered in `v2/__tests__/FpbInvoiceView-tests.tsx:386` (`it('fetches the PDF url and downloads on clicking "PDF" (flag on, happy path)')`) with a mocked fetch. | L5 e2e (add) — a real download needs a real browser + real object storage URL | `apps/settings/e2e/PracticeSettingsPages/billing-invoice-summary.spec.ts` | A provider who cannot download an invoice cannot submit it to their accountant or dispute a charge. A broken/expired signed URL is invisible to every current test. | 4h | **P1** |
| 5 | **Bookings CSV download.** `FpbInvoiceView-tests.tsx:354` (`it('fetches the CSV url and downloads on clicking "Bookings CSV"')`) and `:659` in `InvoiceDetailsContainer-tests.tsx` cover it at L2 behind the BILL-1135 flag. **Zero L5 coverage**; the flag is never set in any e2e spec. | L5 e2e (add) — same real-URL argument as #4 | `apps/settings/e2e/PracticeSettingsPages/billing-invoice-summary.spec.ts` | Same blast radius as #4; the CSV is how practices reconcile bookings against charges. | 3h | **P1** |
| 6 | **Monthly limit change actually constrains spend.** `billing-settings-v2.spec.ts:228` / `:278` set a limit against a `204`-stubbed `savePaymentMethodAttributes` and assert only the on-screen label. Nothing verifies the limit was persisted with the value sent, and both tests are inside an `if (paymentMethodWithLimit)` guard (:241, :288) so they can silently pass while asserting nothing. | L4 api (persist contract) — the UI part is already L2-covered by `EditMonthlyLimitModalV2-tests.tsx` | subject `.../billingSettings/apiCalls.ts`; existing L2 at `__tests__/EditMonthlyLimitModalV2-tests.tsx` | A monthly limit is a hard cap on what Zocdoc may charge a practice. Silently dropping it overcharges the provider — direct money corruption. | 4h | **P0** |
| 7 | **`SHOULD_MOCK_STRIPE` cookie may be dead.** ~~(RETRACTED — it is consumed by production code; see orchestrator correction in this file.)~~ Set by 6 of 7 billing specs but matched nowhere in the snapshot's application source. If dead, 6 specs carry a misleading 8-line `addCookies` block implying Stripe behaviour is being toggled when `installStripeJsFake` already faked it unconditionally. | investigate | `billing-settings-page.spec.ts:25`, `billing-settings-v2.spec.ts:44`, `billing-invoice-summary.spec.ts:50`, `billing-pricing-v2.spec.ts:174`, `invoice-details-page.spec.ts:23`, `payment-recovery.spec.ts:34` | Not a coverage gap, but a correctness gap in the tests: a reader will believe Stripe is conditionally mocked. Decision rule: if no consumer exists outside the snapshot subtree, delete the cookie from all 6 specs. | 1h | P2 |
| 8 | **Empty test with zero assertions.** `billing-settings-v2.spec.ts:175-179` — title duplicates the sibling at `:56`; body is a single `setUpRoutesAndVisitBillingPage` call. Costs a full browser page load and can only fail on a page crash. | delete | `billing-settings-v2.spec.ts:175` | An always-green test in a money-critical suite is worse than no test: it inflates the count and implies coverage that does not exist. | 15m | P1 |
| 9 | **Six tests guarded by `if (mock.find(...))`.** `billing-settings-v2.spec.ts` tests at :181, :228, :278, :341, :403, :745 wrap every assertion in `if (found) { ... }` (:191, :241, :288, :349, :425, :759). A fixture change makes them pass vacuously. | investigate / fix | `billing-settings-v2.spec.ts` | Six of the sixteen tests in the payment-method suite can silently stop asserting. Replace with a hard `expect(found).toBeDefined()` before the block. | 1h | P1 |


---

## Orchestrator Correction — `SHOULD_MOCK_STRIPE`

**CORRECTED BY ORCHESTRATOR (verified against full repo at `dd9e4952a6`):** this cookie is NOT dead. It is read by production code at `apps/settings/src/pages/settingsPages/billingSettings/AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:52` and `.../AddPaymentMethodModalV2/AchFormContentV2.tsx:69`. The real finding is worse than dead config: production components branch on a test-only cookie, so the E2E suite's green path executes a code path real users never take. Commit `dd9e4952a6` (`move the Stripe.js mock out of production code`) is the team already addressing this — reinforce that work, do not open a competing ticket. See `../../methodology/VERIFIED-HISTORY.md`.
