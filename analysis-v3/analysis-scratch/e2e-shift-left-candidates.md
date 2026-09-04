# provider-fe-monorepo — Billing E2E Shift-Left Candidates

| Field | Value |
|---|---|
| Repo | `provider-fe-monorepo` |
| Revision analyzed | `dd9e4952a6` (`origin/main`, 2026-09-03) |
| Snapshot path | `/tmp/slv3/snapshots/provider-fe-monorepo/` |
| Tests classified | 63 (every `test()` in the 7 billing specs under `apps/settings/e2e/`) |
| Companion files | [`../inventory/provider-fe-monorepo/e2e-L5.md`](../inventory/provider-fe-monorepo/e2e-L5.md), [`../inventory/provider-fe-monorepo/e2e-infrastructure.md`](../inventory/provider-fe-monorepo/e2e-infrastructure.md) |

## Tally

| Verdict | Count | Share |
|---|---|---|
| `keep-e2e` | 5 | 7.9% |
| `shift-to-L2` | 19 | 30.2% |
| `shift-to-L1` | 0 | 0% |
| `shift-to-L3` | 0 | 0% |
| `delete-redundant` | 39 | 61.9% |
| `delete-suspected` | 0 | 0% |
| **Total** | **63** | |

Per spec:

| Spec | Tests | keep-e2e | shift-to-L2 | delete-redundant |
|---|---|---|---|---|
| `billing-settings-page.spec.ts` | 7 | 0 | 7 | 0 |
| `billing-settings-v2.spec.ts` | 16 | 0 | 5 | 11 |
| `billing-settings-payment-element.spec.ts` | 4 | 1 | 1 | 2 |
| `billing-invoice-summary.spec.ts` | 20 | 1 | 5 | 14 |
| `billing-pricing-v2.spec.ts` | 11 | 0 | 1 | 10 |
| `invoice-details-page.spec.ts` | 1 | 0 | 0 | 1 |
| `payment-recovery.spec.ts` | 4 | 3 | 0 | 1 |

`invoice-details-page.spec.ts` reaches zero tests and the file is deleted.
`billing-pricing-v2.spec.ts` reaches zero tests once its one shift lands, and the file is deleted.

## Why `shift-to-L3` is zero, and `shift-to-L1` too

- **No `shift-to-L3`.** L3 requires real collaborators across a real boundary. None of these 63
  tests has a real collaborator to preserve — every backend call is `route.fulfill`ed
  (`billing-settings-page-commands.ts:188-359`) and Stripe is a hand-written fake
  (`fixtures.ts:32`). There is nothing to move down *to* L3; the integration these tests would need
  does not exist yet at any level. That absence is the P0 gap, not a shift-left target.
- **No `shift-to-L1`.** Every candidate asserts on rendered output (text, element presence, form
  state), so L2 is the lowest level that can still prove it. The two tests whose *logic* is pure
  (setup-intent reuse semantics) already have L1 coverage and so are `delete-redundant`, not
  `shift-to-L1`.

## Sequencing constraint — read before acting on the deletes

39 deletes plus 19 downward moves would remove 58 of 63 browser tests from the billing path. Every
delete cites a named lower-level test that asserts the same thing, so **no assertion is lost** — but
browser-level confidence is not what these tests were providing in the first place (see
[`e2e-infrastructure.md#tests-that-mock-their-whole-backend`](../inventory/provider-fe-monorepo/e2e-infrastructure.md#tests-that-mock-their-whole-backend):
61 of 63 assert nothing that requires a browser, and 0 of 63 reach a real backend).

The correct order is:

1. **First** land the P0 additions — a real-backend smoke tier and a real-Stripe add-card test
   (gaps I1, I2 in `e2e-infrastructure.md`; gaps 1, 2, 3 in `e2e-L5.md`). These are net-new
   confidence that today does not exist at any level.
2. **Then** execute the deletes. Doing it in this order means billing integration coverage goes up
   before browser-test volume goes down.

Executing step 2 without step 1 would be defensible on the evidence but leaves the billing page with
almost no browser coverage during the gap. Recommend not splitting them across sprints.

---

## `billing-settings-page.spec.ts` (7 tests)

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `billing-settings-page.spec.ts:35` | `shows error if practice id not passed` | shift-to-L2 | Asserts `selectors.errorPage` renders when the `practiceId` query param is absent. No backend, no browser API involved — a container render with an empty param. | `apps/settings/src/pages/settingsPages/billingSettings/__tests__/BillingSettingsContainer-tests.tsx` (extend) |
| `billing-settings-page.spec.ts:43` | `shows error if fetch billing settings fails` | shift-to-L2 | The failure is produced by a stub returning 400 (`billing-settings-page-commands.ts:192-214`), so nothing real fails. Mocking the same rejection at the data hook proves the identical branch. | `apps/settings/src/pages/settingsPages/billingSettings/__tests__/BillingSettingsContainer-tests.tsx` (extend) |
| `billing-settings-page.spec.ts:123` | `showing completion modal - does not error on null address1` | shift-to-L2 | Pure null-prop crash-safety: spreads `mockPracticeBillingSettingsViewModel` with one field nulled and asserts the view rendered and the error page did not. A jsdom render with the same prop proves it. | new/extended `__tests__` for the BillingCompletionModal, as a single `it.each` over the 5 nullable fields |
| `billing-settings-page.spec.ts:142` | `showing completion modal - does not error on null city` | shift-to-L2 | Same as above, `city` nulled. Collapses into the same `it.each`. | same `it.each` |
| `billing-settings-page.spec.ts:161` | `showing completion modal - does not error on null state` | shift-to-L2 | Same as above, `state` nulled. | same `it.each` |
| `billing-settings-page.spec.ts:180` | `showing completion modal - does not error on null zipCode` | shift-to-L2 | Same as above, `zipCode` nulled. | same `it.each` |
| `billing-settings-page.spec.ts:199` | `showing completion modal - does not error on null businessEmail` | shift-to-L2 | Same as above, `businessEmail` nulled. | same `it.each` |

Net effect: 7 browser tests, each costing a full page load, become one parameterised jsdom test.
`UNVERIFIED —` whether a `BillingCompletionModal` L2 test file already exists; the snapshot search
covered `billingSettings/__tests__/` but I did not enumerate every file there. Confirm before
creating a new file.

---

## `billing-settings-v2.spec.ts` (16 tests)

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `billing-settings-v2.spec.ts:56` | `opens modal, makes changes to modal and verifies results` (Edit rollovers) | shift-to-L2 | The modal half is already covered: `EditRolloversModalV2-tests.tsx` `it('reorder moves items up')`, `it('calls API and onPaymentMethodsChange on successful save')`, `it('shows "Rollover settings saved" toast on successful save')`. The uncovered half is the page-level list re-rendering in the new order after save — that belongs in the list component's own suite, not a browser. | `apps/settings/src/pages/settingsPages/billingSettings/PaymentMethodsList/__tests__/PaymentMethodsListV2-tests.tsx` (extend with a post-save reorder assertion) |
| `billing-settings-v2.spec.ts:175` | `opens modal, makes changes to modal and verifies results` (Payment methods list) | delete-redundant | **The body has zero assertions** — it is a single `setUpRoutesAndVisitBillingPage(page, practiceId, {})` call (:175-179). Deleting it cannot reduce coverage because it asserts nothing; no covering test is needed. Its title is a verbatim copy of `:56`, so it is a copy-paste leftover. | delete outright |
| `billing-settings-v2.spec.ts:181` | `sets a non-default payment method as default` | delete-redundant | Covered by `PaymentMethodV2-tests.tsx` `it('calls setDefaultPaymentMethod API on "Set as default" click')` and `PaymentMethodsListV2-tests.tsx` `it('calls parent onSetDefaultPaymentMethod and shows "Default payment method updated" toast when set-default is triggered')`. The E2E's API call is stubbed 204 (`commands:247-256`), so it proves nothing extra. Also currently guarded by `if (nonDefaultPaymentMethod)` at :191. | already covered — delete |
| `billing-settings-v2.spec.ts:228` | `sets a monthly limit for a payment method without a limit` | delete-redundant | Covered by `PaymentMethodV2-tests.tsx` `it('opens EditMonthlyLimitModal on "Set limit" click')` plus `EditMonthlyLimitModalV2-tests.tsx` `it('calls API and onPaymentMethodsChange when value changes with rollovers set')`. Guarded at :241. Note the *persistence contract* is a separate P0 gap (L4), not served by this test either. | already covered — delete; add the L4 persist test per `e2e-L5.md` gap 6 |
| `billing-settings-v2.spec.ts:278` | `edits an existing monthly limit for a payment method` | delete-redundant | Covered by `EditMonthlyLimitModalV2-tests.tsx` `it('calls API and onPaymentMethodsChange when value changes with rollovers set')` and `PaymentMethodV2-tests.tsx` `it('shows monthly limit when present')`. Guarded at :288. | already covered — delete |
| `billing-settings-v2.spec.ts:341` | `deletes a non-default payment method` | delete-redundant | Covered by `DeletePaymentMethodConfirmationModalV2-tests.tsx` `it('calls handleDelete and closes modal on Delete click')` and `PaymentMethodV2-tests.tsx` `it('calls deletePaymentMethod API when delete is confirmed')`. The DELETE is stubbed 204 (`commands:258-267`). Guarded at :349. | already covered — delete |
| `billing-settings-v2.spec.ts:403` | `verifies payment methods list has the correct content` | delete-redundant | Pure content assertion, covered by `PaymentMethodsListV2-tests.tsx` `it('renders payment methods list')` plus `PaymentMethodV2-tests.tsx` `it('displays default tag when payment method is default')` and `it('shows monthly limit when present')`. Both levels read the same `mocks.ts` constants, so the expected strings are identical. Guarded at :425. | already covered — delete |
| `billing-settings-v2.spec.ts:459` | `verifies billing contact info has the correct content` | delete-redundant | Covered by `BillingContactInfo-tests.tsx` `it('displays business address correctly (address1, address2, city/state/zip)')` and `it('displays billing email when provided')`. This test's only mechanism is the `verifyContactInfo` page-object method, which asserts the same two strings. | already covered — delete (and `BillingSettingsPagePageObject.ts` becomes unused) |
| `billing-settings-v2.spec.ts:474` | `prepopulates contact info fields` | delete-redundant | Covered by `EditBillingContactInfoModal-tests.tsx` `it('prepopulates form fields with existing values')`. | already covered — delete |
| `billing-settings-v2.spec.ts:524` | `requires required fields` | delete-redundant | Form validation with no network. Covered by `EditBillingContactInfoModal-tests.tsx` `it('shows error when address1 is cleared')` and its sibling required-field cases. | already covered — delete |
| `billing-settings-v2.spec.ts:561` | `saves changes to contact info` | delete-redundant | Covered by `EditBillingContactInfoModal-tests.tsx` `it('shows "Contact info saved" toast when both updates succeed')` and `it('allows selecting a state via the DropdownSingle mock')`. Both PUTs are stubbed 204 in the E2E. | already covered — delete |
| `billing-settings-v2.spec.ts:659` | `displays an error message when updating primary business address fails` | shift-to-L2 | The nearest L2 is `EditBillingContactInfoModal-tests.tsx` `it('does not show toast when updatePrimaryBusinessAddress returns hasError: true')`, which asserts toast *suppression* rather than the inline error string this test checks. Not a clean delete — extend the L2 to assert the error message, then drop the E2E. | `.../PaymentMethodsList/components/v2/__tests__/EditBillingContactInfoModal-tests.tsx` (extend) |
| `billing-settings-v2.spec.ts:704` | `displays an error message when updating billing email fails` | shift-to-L2 | Same reasoning as the row above, for the billing-email PUT. The failure is a stubbed 500, so nothing real is being exercised. | `.../v2/__tests__/EditBillingContactInfoModal-tests.tsx` (extend) |
| `billing-settings-v2.spec.ts:745` | `sets default payment method for a provider in the "See by provider" modal` | shift-to-L2 | Modal opening is covered by `PaymentMethodsListV2-tests.tsx` `it('opens PaymentMethodsPerProviderModal on "See by provider" click')`, but the per-provider set-default call is not covered by any test I could name. Move the interaction into the per-provider modal's own suite rather than deleting. Currently guarded at :759. | `.../PaymentMethodsList/__tests__/` — extend `PaymentMethodsListV2-tests.tsx` or add a `PaymentMethodsPerProviderModal` suite |
| `billing-settings-v2.spec.ts:838` | `opens V2 pricing calculator modal, steps through all inputs, and verifies calculated result` | delete-redundant | Covered by `YearlyValueCalcModalV2-tests.tsx` `it('navigates through all 5 steps and shows the Calculate button on the last step')`, `it('displays the correct calculated result')`, `it('resets to step 1 when Start over is clicked')`, `it('clears all form values after start over')`. The E2E's `'327'` assertion and the Start-over reset are both in that list. | already covered — delete |
| `billing-settings-v2.spec.ts:989` | `closes V2 pricing calculator modal when close button is clicked` | shift-to-L2 | Modal dismissal — no covering L2 title captured. Trivial to assert in the modal's existing suite; not worth a browser and a `getSkuMappings` stub. | `.../__tests__/YearlyValueCalcModalV2-tests.tsx` (extend) |

---

## `billing-settings-payment-element.spec.ts` (4 tests)

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `billing-settings-payment-element.spec.ts:30` | `renders the unified form with no type-picker` | shift-to-L2 | The positive half is covered by `AddPaymentMethodElementModal-tests.tsx` `it('renders the modal shell around the payment element fields')` and `PaymentElementFields-tests.tsx` `it('renders the Stripe element')`. The unique half — `[data-test="payment-method-type-credit-card"]` having count 0 when `billingProviderRepositioning` is off — is an absence assertion best placed beside the existing modal tests. | `shared/core/src/components/AddPaymentMethodModal/__tests__/AddPaymentMethodElementModal-tests.tsx` (extend), or `apps/settings/.../__tests__/AddPaymentMethodModalV2-tests.tsx` |
| `billing-settings-payment-element.spec.ts:44` | `submits the unified form and saves a payment method` | keep-e2e | Its assertions *are* duplicated by `AddPaymentMethodElementModal-tests.tsx` `it('confirms the setup then saves the confirmed payment method')`. But this is the **only** browser test on the add-a-card path — the single journey by which a practice becomes payable. Deleting it leaves that path with zero browser coverage. Keep the test and **rewire it to Stripe test mode** per `e2e-infrastructure.md` gap I2 so it starts proving something the L2 cannot. This is the one place where the conservative call is to keep despite provable redundancy. | keep at L5; rework to drop `installStripeJsFake` and hit a real setup intent |
| `billing-settings-payment-element.spec.ts:63` | `reuses the confirmed payment method when saving again after a failure` | delete-redundant | Covered at L1 by `shared/core/src/billing/__tests__/useConfirmPaymentSetup-tests.tsx` `it('reuses the confirmed payment method on retry without a second intent')`. The E2E proves it by counting POSTs via a `page.on('request')` listener (:70-80) against stubbed endpoints — an HTTP-contract assertion executed in a browser for no reason, since the hook test asserts the same invariant directly. | already covered — delete |
| `billing-settings-payment-element.spec.ts:105` | `runs the full flow again when the payment details are edited after a failure` | delete-redundant | Covered at L1 by `useConfirmPaymentSetup-tests.tsx` `it('confirms again once the entered details change')` and at L2 by `AddPaymentMethodElementModal-tests.tsx` `it('invalidates the confirmed payment method when the details change')`. | already covered — delete |

---

## `billing-invoice-summary.spec.ts` (20 tests)

All L2 citations below are in
`apps/settings/src/pages/settingsPages/billingSettings/.../v2/__tests__/FpbInvoiceView-tests.tsx`
unless another file is named. Both levels read the same `mockBillSummaryResponse`
(`mocks.ts:398`), so the expected values are identical by construction.

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `billing-invoice-summary.spec.ts:74` | `should display invoice title in "Month Year" format` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render title in "Month Year" format')` — same format assertion, same fixture. | already covered — delete |
| `billing-invoice-summary.spec.ts:82` | `should display "Sponsored Results fees*" with asterisk` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render sponsored results charge with asterisk')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:92` | `should display collapsible taxes and fees section with line items` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render taxes and fees section with grouped license fees')` plus `TaxesAndFeesSection-tests.tsx` `it('should render "Taxes and fees" header with total amount')` and `it('should expand to show license fee details')` — the expand interaction included. | already covered — delete |
| `billing-invoice-summary.spec.ts:107` | `should display collapsible marketplace bookings with paid and free breakdown` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should display a breakdown of paid and free bookings when invoice date is >= 1/1/2026')`, which asserts the amounts this test only checks for label presence. | already covered — delete |
| `billing-invoice-summary.spec.ts:129` | `should display "Total" label with correct amount` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render total label')`. The hard-coded `$8,570.00` (:135) derives from the same fixture the L2 uses. | already covered — delete |
| `billing-invoice-summary.spec.ts:138` | `should display "Zocdoc credits" when credits are applied` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render applied credits with "Zocdoc credits" label')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:146` | `should display amount due row` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render amount due')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:155` | `should display footer with Eastern Time note and billing link` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render footer text with billing link')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:172` | `should render PDF button when PDF is available` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('should render PDF button when available')`. This test never clicks the button, so it adds nothing over the L2. The *download* is a separate uncovered journey (`e2e-L5.md` gap 4), not something this test provides. | already covered — delete; add the download test per gap 4 |
| `billing-invoice-summary.spec.ts:187` | `should display "Invoices" as sidebar title` | delete-redundant | `BillsContainer-tests.tsx` `it('renders the "Invoices" heading')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:193` | `should show checkmark on the currently selected bill` | delete-redundant | `BillsContainer-tests.tsx` `it('marks the correct bill as selected')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:203` | `should list multiple bills in the sidebar` | shift-to-L2 | Asserts only `toBeGreaterThanOrEqual(2)` on a row count — a weak assertion with no named L2 equivalent. Move it into the sidebar component's suite and assert the actual expected row set rather than a floor. | `.../__tests__/BillsContainer-tests.tsx` (extend) |
| `billing-invoice-summary.spec.ts:212` | `should display "Paid" status tag on paid bills` | shift-to-L2 | Status-tag rendering from a fixture field. No named L2 covers the tag text, so this is a move rather than a delete. Pure render — no browser needed. | `.../__tests__/BillsContainer-tests.tsx` (extend) |
| `billing-invoice-summary.spec.ts:222` | `should display status tags on sidebar bills with correct text` | shift-to-L2 | The title says "with correct text" but the assertion is `toBeGreaterThanOrEqual(1)` on a count and never checks any text — the test does not do what it claims. Rewrite at L2 asserting the Paid / PartiallyPaid / Unpaid strings the fixture actually contains. | `.../__tests__/BillsContainer-tests.tsx` (rewrite) |
| `billing-invoice-summary.spec.ts:235` | `should show checkmark on the selected bill row in the sidebar` | delete-redundant | Duplicate of the sibling at `billing-invoice-summary.spec.ts:193` (`should show checkmark on the currently selected bill`) — same behaviour, expressed as `bill-row:has(bill-selected-check)` instead of the check alone. Also covered by `BillsContainer-tests.tsx` `it('marks the correct bill as selected')`. | already covered — delete |
| `billing-invoice-summary.spec.ts:250` | `should display "Back to Billing" link` | shift-to-L2 | Link presence and label. No named L2 equivalent captured, so move rather than delete. Nothing browser-specific. | `.../v2/__tests__/FpbInvoiceView-tests.tsx` (extend) |
| `billing-invoice-summary.spec.ts:256` | `should have a clickable "Back to Billing" link` | delete-redundant | Covered by the sibling at `billing-invoice-summary.spec.ts:250` (`should display "Back to Billing" link`) — this test asserts `toBeAttached()` on the same locator and **never clicks**, so "clickable" is not exercised and the two tests are identical in effect. | already covered by the sibling — delete |
| `billing-invoice-summary.spec.ts:271` | `shows "{count} from Healthcare platforms" for a post-cutoff bill` | delete-redundant | `FpbInvoiceView-tests.tsx` `it('renders "{count} from Healthcare platforms" with $0.00 when count > 0')` and `it('renders the row for the August 2026 bill, whose bookings are July's')` — the L2 covers both the row and the August cutoff case this test constructs `augustBillSummaryResponse` for. | already covered — delete |
| `billing-invoice-summary.spec.ts:286` | `does not show the Healthcare platforms row for a pre-cutoff bill` | shift-to-L2 | The negative pre-cutoff case is not among the `FpbInvoiceView-tests.tsx` titles I could name, so it is a move, not a delete. It is a date-boundary branch on a fixture — ideal L2. | `.../v2/__tests__/FpbInvoiceView-tests.tsx` (extend with the pre-cutoff case) |
| `billing-invoice-summary.spec.ts:297` | `renders the new source rows with their values and correct order` | keep-e2e | The only test in this file that needs a real browser: it reads `boundingBox()` y-coordinates to assert visual ordering (sponsored above google above website above taxes). `FpbInvoiceView-tests.tsx` `it('renders the new rows after Sponsored Results and in source order')` covers **DOM** order, which a CSS `order`/`flex-direction` change could silently diverge from. jsdom has no layout, so the visual guarantee is only observable here. | keep at L5 |

---

## `billing-pricing-v2.spec.ts` (11 tests)

All L2 citations are in
`apps/settings/src/pages/settingsPages/billingSettings/__tests__/PricingInformationV2-tests.tsx`
unless otherwise named. Every test in this spec renders the pricing tab against a stubbed
`getSkuMappings` payload — precisely the input the L2 suite passes as a prop.

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `billing-pricing-v2.spec.ts:185` | `renders V2 pricing tab` | shift-to-L2 | A bare smoke assertion on `pricingTabV2.view`. `PricingTab-tests.tsx` exists but I could not name an `it` asserting exactly this, so it is a move rather than a delete. Note it also duplicates the precondition already asserted at `billing-settings-v2.spec.ts:848-850`. | `.../__tests__/PricingTab-tests.tsx` (confirm/extend) |
| `billing-pricing-v2.spec.ts:190` | `shows FAQs section on V2 pricing tab` | delete-redundant | `PricingInformationV2-tests.tsx` `it('shows 5 FAQ items')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:195` | `FAQ items expand and collapse on click` | delete-redundant | `PricingInformationV2-tests.tsx` `it('expands FAQ answer on click')` — an accordion toggle is a standard RTL interaction, nothing browser-specific. | already covered — delete |
| `billing-pricing-v2.spec.ts:225` | `shows V2 marketplace card when enrolled in marketplace` | delete-redundant | `PricingInformationV2-tests.tsx` `it('renders marketplace card when enrolled in marketplace')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:234` | `opens price by provider modal when "View price by provider" link is clicked` | delete-redundant | `PricingInformationV2-tests.tsx` `it('opens PriceByProviderModal when "View price by provider" is clicked')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:245` | `shows bookable presence card` | delete-redundant | `PricingInformationV2-tests.tsx` `it('renders bookable presence card when enrolled in marketplace')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:250` | `shows marketplace card when marketplace SKU is selected but not activated` | delete-redundant | `PricingInformationV2-tests.tsx` `it('renders marketplace card when marketplace SKU is selected but not activated')` — the L2 takes the same SKU state as a prop that this spec builds a whole `getSkuMappings` stub and second page load to produce. | already covered — delete |
| `billing-pricing-v2.spec.ts:258` | `shows FAQs when marketplace SKU is selected but not activated` | delete-redundant | `PricingInformationV2-tests.tsx` `it('renders FAQs when marketplace SKU is selected but not activated')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:265` | `does not show FAQs section when no SKUs are selected` | delete-redundant | `PricingInformationV2-tests.tsx` `it('does not render FAQs section when practiceEnrollments is empty')` and `it('shows empty state text when not enrolled in marketplace')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:274` | `shows the 5th FAQ about controlling monthly spend` | delete-redundant | `PricingInformationV2-tests.tsx` `it('includes the new 5th FAQ about controlling monthly spend')`. | already covered — delete |
| `billing-pricing-v2.spec.ts:284` | `shows the FAQ about what bookings are charged for` | delete-redundant | `PricingInformationV2-tests.tsx` `it('includes FAQ about what bookings are charged for')`. | already covered — delete |

This is the single clearest shift-left target in the repo: 11 browser tests and 22 page loads
(the spec navigates twice per test, :79-80) asserting static marketing copy and accordion toggles
that `PricingInformationV2-tests.tsx` already asserts in-process. Once the one `shift-to-L2` lands
the file is empty and is deleted, along with its three `getSkuMappings` setup helpers (:23-168, 146
lines of support code).

---

## `invoice-details-page.spec.ts` (1 test)

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `invoice-details-page.spec.ts:33` | `should display marketplace bookings section with paid and free breakdown` | delete-redundant | Covered twice over. At L5 by `billing-invoice-summary.spec.ts:107` (`should display collapsible marketplace bookings with paid and free breakdown`) — same URL, same `clickBillByDate(page, 'Jan 2026')`, same fixture, same section. At L2 by `FpbInvoiceView-tests.tsx` `it('should display a breakdown of paid and free bookings when invoice date is >= 1/1/2026')`, which asserts the same amounts. The only thing this test adds over its L5 sibling is exact-value strictness, and the L2 already has that. | already covered — delete the whole file |

Deleting this test empties `invoice-details-page.spec.ts` (60 LOC). If the exact-value strictness is
considered worth preserving, fold it into the `FpbInvoiceView-tests.tsx` case rather than keeping a
browser test for it.

---

## `payment-recovery.spec.ts` (4 tests)

The highest keep rate in the suite (3 of 4), and not by accident: this is the only billing spec whose
header reasons explicitly about levels (:23-30) and whose one layout test justifies itself in a
docstring (:221-232). It is the model the other six specs should follow.

| spec | test title | verdict | reason | proposed target |
|---|---|---|---|---|
| `payment-recovery.spec.ts:96` | `banner -> review -> pay -> single success outcome banner` | keep-e2e | The only test that stitches the whole money-recovery journey across a page transition: recovery banner CTA, Pay Now modal, submitted charge, then the outcome banner rendering `data-variant="single.success"` back on the billing page. Every individual hop has L2 coverage (`BillingSettingsContainer-tests.tsx` `it('shows the recovery banner under the Payment tab')`, `it('opens the Pay Now modal when the CTA is clicked and showReviewAndPayCta is true')`; `RecoveryStatusBanner-tests.tsx` `it('fires onStartRecovery exactly once when the CTA is clicked')`; `PayNowModal-tests.tsx` `it('starts on the review step')`) but nothing else asserts the stitch. Caveat: `POST /pay-now` is stubbed to success (:78-93), so it currently proves the UI sequence, not that money moved — upgrade per `e2e-L5.md` gap 3. | keep at L5; rework to hit a real `/pay-now` in a deployed environment |
| `payment-recovery.spec.ts:156` | `update-only mode: banner -> Update -> new card persists immediately, no charge, confirmation shown` | keep-e2e | Two assertions here are browser-only: the toast's real geometry (`overflow === 0`, `height === 68`) and the banner's suppression surviving a `localStorage` clear plus a full page reload. Neither is observable in jsdom. The modal-behaviour half **is** L2-covered (`PayNowModal-tests.tsx` `it('Update persists the new card immediately as the replacement, fires no charge, and reports it up')`, `it('hides the "Pay now" button and "Use different payment method" link, keeping the review list')`; `BillingSettingsContainer-tests.tsx` `it('splices the persisted card into the payment-methods list in place of the method it replaced, with no page-level confirmation')`) and the E2E should be trimmed to the two browser-only assertions rather than re-walking the modal. | keep at L5; trim the L2-duplicated middle |
| `payment-recovery.spec.ts:233` | `opens the modal at the top when the review step overflows` | keep-e2e | BILL-1083. Asserts `scrollTop === 0` after `expect.poll` confirms the content actually overflows a 1000x600 viewport. The spec's own docstring (:221-232) states the case correctly: jsdom has no layout, so `ReviewStep-tests.tsx` `it('takes focus on mount without scrolling the modal content')` can only assert the mechanism (`preventScroll`), never the resulting scroll position. This is the textbook justified L5. | keep at L5 |
| `payment-recovery.spec.ts:276` | `renders the banner headline and sub-line without decline codes` | delete-redundant | Static copy assertion on the banner plus a negative check that raw Stripe codes do not leak. Covered by `RecoveryStatusBanner-tests.tsx` `it('renders the single-failure headline, context, and CTA')`; the code-leak negative belongs beside it in the same suite. No page navigation or layout involved. | already covered — delete; add the decline-code negative assertion to `RecoveryStatusBanner-tests.tsx` if not already present |

---

## Cost impact (estimate)

| | Now | After |
|---|---|---|
| Billing L5 tests | 63 | 5 |
| Billing L5 page loads | 75 (estimate) | 6 (estimate) |
| Billing L5 spec LOC | 2,380 | ~450 (estimate) |
| Billing L5 support LOC | 1,990 | ~1,100 (estimate — `selectors.ts` and `helpers.ts` are shared with non-billing specs and stay) |
| Serial billing L5 runtime | 10–16 min (estimate) | 1–2 min (estimate) |
| New L2/L1 tests to add or extend | — | 19 moves, collapsible to ~12 test bodies (the 5 null-field tests become one `it.each`) |

Basis for the runtime figures and their limitations are stated in
[`e2e-L5.md#4-total-billing-e2e-test-count-and-estimated-runtime`](../inventory/provider-fe-monorepo/e2e-L5.md#4-total-billing-e2e-test-count-and-estimated-runtime).
`UNVERIFIED —` no CI artifact or `playwright.config.ts` exists in the snapshot, so none of these
timings are measured.

Support code that becomes dead once the deletes land, and should be removed in the same change:

| Path | Why |
|---|---|
| `pageObjects/BillingSettingsPagePageObject.ts` (46 LOC) | its only method `verifyContactInfo` is used solely by `billing-settings-v2.spec.ts:459` and `:561`, both deleted |
| `pageObjects/EditBillingContactInfoModalPageObject.ts` (185 LOC) | used only by the five `Billing contact info` tests; two shift to L2, three are deleted |
| `billing-pricing-v2.spec.ts:23-168` | the three `visitV2PricingTab*` helpers die with the file |
| `getPaymentMethodsWithoutRollovers` (`commands:203-208`) | already unused by every spec today — see `e2e-infrastructure.md` gap I7 |

---

## Candidate Gaps

Journey-level gaps are in
[`e2e-L5.md#candidate-gaps`](../inventory/provider-fe-monorepo/e2e-L5.md#candidate-gaps) (9 rows) and
infrastructure gaps in
[`e2e-infrastructure.md#candidate-gaps--infrastructure`](../inventory/provider-fe-monorepo/e2e-infrastructure.md#candidate-gaps--infrastructure)
(9 rows). These are specific to executing this shift-left plan.

| # | Missing / needed | Correct test level | File(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| S1 | **Execute the 39 deletes and 19 moves, gated behind the P0 additions.** Ordering is load-bearing: land the real-backend smoke tier and real-Stripe add-card test first (`e2e-L5.md` gaps 1-3, `e2e-infrastructure.md` gaps I1-I2), then delete. | L2 (destination) / delete | the 7 specs listed above; destinations named per row | 58 of 63 browser tests assert nothing a browser is required for. Executing the plan cuts serial billing L5 runtime from 10-16 min to 1-2 min (estimate) and removes ~900 LOC of support code, with every removed assertion re-homed to a named lower-level test. Doing it in the wrong order leaves the billing page briefly with almost no browser coverage. | 3d, splittable per spec | **P1** |
| S2 | **`billing-pricing-v2.spec.ts` can be deleted almost wholesale** (10 of 11 tests cited to `PricingInformationV2-tests.tsx`), plus 146 LOC of setup helpers and 22 page loads. Independently actionable, no dependency on the P0 work, because it asserts only static copy and accordion state. | delete + 1 L2 move | `apps/settings/e2e/PracticeSettingsPages/billing-pricing-v2.spec.ts`; `.../__tests__/PricingTab-tests.tsx` | The single largest cost reduction available for the least risk in this analysis: no money path, no integration, every assertion already duplicated at L2 with a named `it`. Good first ticket to prove the approach. | 4h | **P1** |
| S3 | **Adopt `payment-recovery.spec.ts`'s level-discipline docstring convention across the other six specs.** That file states which branches deliberately live in RTL suites (:23-30) and justifies its one layout test (:221-232); no other billing spec explains why it is at L5. | convention / docs | the 6 other billing specs under `apps/settings/e2e/PracticeSettingsPages/` | Without this, the suite re-accretes L2-shaped browser tests as soon as the cleanup ships — which is exactly how it reached 63. Requiring a one-line "why L5" per describe makes the next reviewer able to reject a misplaced test. | 2h | P2 |
| S4 | **Confirm the two `UNVERIFIED` L2 destinations before writing the moves**: whether a `BillingCompletionModal` L2 suite exists (destination for the 5 null-field tests) and whether `PricingTab-tests.tsx` contains a tab-render assertion (destination for `billing-pricing-v2.spec.ts:185`). | investigate | `apps/settings/src/pages/settingsPages/billingSettings/__tests__/` | Two of the 19 moves have destinations I could not confirm in the snapshot. Decision rule: if the suite exists, extend it; if not, create it. Cheap to settle but it blocks writing those two tickets accurately. | 30m | P2 |
