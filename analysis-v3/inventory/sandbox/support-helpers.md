# sandbox — `playwright/support/billing.ts` Support-Helper Inventory

**Repo:** `/Users/vishesh.luthra/sandbox`
**Analyzed revision:** working tree at `dac52b65a3ae89cd756c3951e58ae3fec0ce3b1d` (branch `fix/billing-stripe-payment-element`)
**`origin/main` at time of analysis:** `4bb607cc942b03c067d5755eb8192ebfaf27d227`
**File:** `/Users/vishesh.luthra/sandbox/playwright/support/billing.ts` — 365 lines, 18 top-level declarations (10 exported, 8 module-private)
**Level:** not a test. Supports **L5 `e2e`** only.

## State of this file

| Layer | Status | Evidence |
|---|---|---|
| `dac52b65` "repoint billing add-payment-method helpers at Stripe Payment Element" | Committed, **branch only — not on `origin/main` (`4bb607cc`)**. Sole file touched: this one. `148 insertions, 167 deletions`. | `git show --stat dac52b65` |
| Working-tree edits on top | **Uncommitted.** `14 insertions, 13 deletions`, all inside `connectStripeTestBank` (`:201-226`). Replaces two hand-rolled `Date.now()` deadline loops with `expect(...).toPass()`; behavior equivalent, failure messages better. | `git status` → ` M playwright/support/billing.ts`; `git diff --stat` |

Per the `dac52b65` commit message: *"Both billing specs had been failing since 2026-09-02 on selectors for that old markup."* So on `main` today this helper module is pointed at markup that no longer exists, and all 4 billing E2E tests are red. Neither spec file was edited by `dac52b65` — the public signatures were held stable deliberately (*"Public signatures are unchanged, so neither spec needed editing"*).

Re-export barrel: `playwright/support/index.ts:79-90` re-exports 10 of the 10 exported symbols. Consumers import from `../../../../../support`, never from `./billing` directly.

---

## Exported helpers (10)

| # | Symbol | Lines | Kind | Used by |
|---|---|---|---|---|
| 1 | `ADDED_CREDIT_CARD_LAST4` = `"4242"` | `:8` | const | both specs |
| 2 | `ADDED_ACH_ACCOUNT_LAST4` = `"6789"` | `:9` | const | both specs; also internally at `:203`, `:260` |
| 3 | `listPaymentMethodIds(page)` | `:14-18` | async | **neither spec** — internal only (`:248`, `:284`), though exported and re-exported |
| 4 | `paymentMethodRowById(page, id)` | `:36-40` | Locator factory | both specs |
| 5 | `rolloverRowById(page, id)` | `:44-48` | Locator factory | both specs |
| 6 | `saveModalAndClose(modal, clickSave)` | `:55-69` | async | both specs |
| 7 | `reloadPaymentMethods(page, expectedIds)` | `:78-89` | async | both specs |
| 8 | `addAchPaymentMethodV2(page, accountHolderEmail, accountHolderName?)` | `:243-264` | async → `Promise<string>` (new method id) | both specs |
| 9 | `addCreditCardV2(page, overrides?)` | `:279-298` | async → `Promise<string>` (new method id) | both specs |
| 10 | `cleanupBillingState(page, canonicalBillingEmail?)` | `:305-365` | async | both specs |

Call-site map (`S` = `Provider-Billing/Pages/billing-settings-page.spec.ts`, `F` = `Account-User-Setup/Flows/billing-user-flow.spec.ts`):

| Helper | S | F |
|---|---|---|
| `addCreditCardV2` | `:90`, `:359` | `:154`, `:430` |
| `addAchPaymentMethodV2` | `:97` | `:161` |
| `cleanupBillingState` | `:69`, `:354` | `:149`, `:425` |
| `reloadPaymentMethods` | `:106`, `:165` | `:170`, `:229` |
| `saveModalAndClose` | `:117`, `:134`, `:147`, `:176`, `:186`, `:203` | `:181`, `:198`, `:211`, `:240`, `:250`, `:267` |
| `paymentMethodRowById` | `:92`, `:99`, `:107`, `:125`, `:142`, `:154`, `:225`, `:235`, `:361`, `:366`, `:376` | `:156`, `:163`, `:171`, `:189`, `:206`, `:218`, `:289`, `:299`, `:432`, `:437`, `:447` |
| `rolloverRowById` | `:173`, `:185`, `:197` | `:237`, `:249`, `:261` |
| `ADDED_CREDIT_CARD_LAST4` | `:92`, `:361` | `:156`, `:432` |
| `ADDED_ACH_ACCOUNT_LAST4` | `:99` | `:163` |
| `listPaymentMethodIds` | — | — |

## Module-private helpers (8)

| Symbol | Lines | Purpose |
|---|---|---|
| `waitForNewPaymentMethodId(page, idsBefore)` | `:22-31` | Polls until exactly one *new* method id appears; returns it. 15s budget. |
| `saveAddPaymentMethodWithRetry(page, addModal, timeout)` | `:91-115` | Clicks Save up to 3×, racing modal-detach against the error banner. |
| `paymentElementFrame(page)` | `:134-136` | Resolves Stripe's Payment Element iframe. **This is the load-bearing change in `dac52b65`.** |
| `selectPaymentMethodTab(element, "card" \| "us_bank_account")` | `:141-150` | Clicks a Payment Element tab until it reports `aria-selected="true"`. 45s budget. |
| `fillStripeInput(input, value)` | `:154-162` | `fill()`, verify digits landed, fall back to `pressSequentially` at 80ms/key. |
| `advanceFinancialConnections(fc)` | `:181-194` | Finds the newest visible+enabled advance control in Stripe's FC modal and clicks it. |
| `connectStripeTestBank(page)` | `:201-226` | Walks Stripe's hosted Financial Connections flow to link the `••••6789` sandbox account. |
| `openAddPaymentMethodModal(page)` | `:230-237` | Opens our modal, asserts the charge disclaimer, waits for the Payment Element wrapper. |

## Module-level constants

| Constant | Value | Line |
|---|---|---|
| `STRIPE_FC_IFRAME` | `'iframe[src*="linked-accounts-inner"]'` | `:118` |
| `CHARGE_DISCLAIMER_COPY` | `"Your use of a paid Zocdoc service authorizes Zocdoc to charge your practice"` | `:121` |
| `STRIPE_TEST_BANK` | `"Test (OAuth)"` | `:124` |
| `FC_ADVANCE_BUTTONS` | `[/^Agree and continue$/i, /^Continue\b/i, /^Not now$/i, /^Finish without saving$/i, /^Done$/i]` | `:168-174` |
| `CREDIT_CARD_DEFAULTS` | `{cardNumber:"4242424242424242", expiry:"1240", cvc:"123", zipCode:"10012", country:"US"}` — Stripe's public "success" test card, not a credential | `:268-274` |

---

## DOM contract — current (post-`dac52b65`)

### Zocdoc-owned `data-test` ids

| Selector | Used at | Depended-on behavior |
|---|---|---|
| `add-payment-method-button` | `:231` | Opens the add modal |
| `add-payment-method-modal` | `:232` | Modal root; **detachment is the success signal** (`:102`) |
| `add-payment-element-fields` | `:135`, `:235` | Wrapper the Stripe iframe is anchored inside; visible within 30s |
| `add-payment-method-submit` | `:95` | Submit button (**renamed** — was `action-buttons-save`) |
| `add-payment-method-error-message` | `:92` | Failure banner; must clear on click, then re-appear on failure (**renamed** — was `action-buttons-error-message`) |
| `payment-method-more-menu-<id>` | `:16-17`, `:39`, `:310`, `:322`, `:327` | **Carries the method id.** The entire id-based targeting strategy rests on this prefix + suffix format |
| `payment-method-row-v2` | `:38`, `:307`, `:319`, `:321`, `:326`, `:334` | Row container; `.filter({has: more-menu-<id>})` yields exactly 1 |
| `default-payment-method-tooltip` | `:308`, `:314` | Presence == "this row is the default" |
| `set-default-payment-method-` (prefix) | `:311` | Menu action |
| `delete-payment-method-` (prefix) | `:323`, `:329` | Menu action; **`isDisabled()` on it is meaningful** (can't delete the default) — `:324` |
| `payment-method-delete-confirmation-modal` | `:330`, `:333` | Confirm dialog; contains a `Delete` role=button |
| `edit-rollovers-link` | `:339` | Opens rollovers modal |
| `edit-rollovers-modal` | `:340`, `:348` | Modal root |
| `edit-rollovers-payment-method-row` | `:46`, `:342` | Row in rollovers modal |
| `rollover-label` | `:343` | Presence == "rollover enabled on this row" |
| `checkbox-input-container` | `:345` | Clickable wrapper for the (visually hidden) checkbox |
| `billing-settings-container` | `:84` | Page-ready gate |
| `billing-email-value` | `:352`, `:362` | Displays the current billing email |
| `edit-billing-contact-info-link` / `-modal` / `-form-billing-email-input` | `:354`, `:355`, `:357`, `:361` | Contact-info edit path |
| `action-buttons-error-message` | `:56` | Still used, but now **only** by `saveModalAndClose` for the limit/rollover/contact modals — no longer by the add flow |

### Non-`data-test` selectors (fragility hotspots)

| Selector | Line | Owner | Risk |
|---|---|---|---|
| `[id="rollover-checkbox-<id>"]` | `:47` | Zocdoc | DOM `id`, not `data-test`; a refactor to a generated React id silently breaks `rolloverRowById` |
| `iframe:not([aria-hidden="true"])` inside `add-payment-element-fields` | `:135` | Stripe | Assumes exactly one non-`aria-hidden` iframe there. Documented at `:126-133`: Stripe's other frame (bank-search helper) *is* `aria-hidden` |
| `#card-tab` / `#us_bank_account-tab` (built as `` `#${paymentMethodType}-tab` ``) | `:145` | Stripe | Stripe's own element ids, derived from its type names |
| `#payment-numberInput`, `#payment-expiryInput`, `#payment-cvcInput`, `#payment-countryInput`, `#payment-postalCodeInput` | `:288-294` | Stripe | Stripe's own field ids |
| `#payment-emailInput`, `#payment-nameInput`, `#payment-bankInput` | `:252-254` | Stripe | Stripe's own field ids |
| `iframe[src*="linked-accounts-inner"]` | `:118` | Stripe | Substring of Stripe's FC iframe URL |
| `getByRole("menuitem", {name: "Test (OAuth)"})` | `:255` | Stripe | Stripe's sandbox institution display name |
| `getByRole("button", {name: /6789/})` | `:203` | Stripe | Sandbox test-account last-4 as text |
| `getByRole("button", {name: /^Connect account$/i})` | `:215` | Stripe | Stripe's own copy |
| `FC_ADVANCE_BUTTONS` copy regexes | `:168-174` | Stripe | Justified at `:164-167`: Stripe's hosted UI "exposes no test ids we can rely on, and its class names are content-hashed" |
| `getByRole("tabpanel")` contains `6789` | `:260` | Stripe | The only in-form confirmation FC handed an account back |
| `getByRole("button", {name: "Save"/"Cancel"/"Delete"})` | `:332`, `:347`, `:360` | Zocdoc | Copy-matched, not id-matched |
| `page.keyboard.press("Escape")` | `:325` | — | Assumes Escape closes the more-menu |

**14 of the selectors this module depends on belong to Stripe, not Zocdoc.** That is the structural reason `dac52b65` was needed and the reason it will be needed again.

---

## Old vs new DOM contract (what `dac52b65` actually changed)

Reconstructed from `git show dac52b65 -- playwright/support/billing.ts` and `git show dac52b65^:playwright/support/billing.ts`. The public signatures of `addCreditCardV2` and `addAchPaymentMethodV2` are unchanged; everything below is internal.

### Structural shift

| | Old (pre-`dac52b65`) | New (`dac52b65` onward) |
|---|---|---|
| Form architecture | Zocdoc-built form: a **type-picker step** (radio + `Continue`), then Zocdoc inputs for name/address/state, with **three separate Stripe Elements iframes** for card number / expiry / CVC, plus a Zocdoc **ACH mandate checkbox** | **One Stripe Payment Element** in a single iframe hosting a tab strip and *all* fields for both card and bank |
| Field ownership | Split — Stripe owned 3 card fields; Zocdoc owned name, address1, city, state, zip, mandate | Stripe owns **every** field; Zocdoc owns only the modal chrome, the disclaimer, and Submit |
| Iframe resolution | `page.frameLocator('iframe[title="<exact title>"]')` per field (`old :252-261`) | One `FrameLocator` anchored on our own `add-payment-element-fields` wrapper, taking the single non-`aria-hidden` iframe (`:134-136`) |
| Stripe.js readiness | Explicit `waitForStripeReady()` — waited for `iframe[src*="js.stripe.com"]` to attach **and** `typeof window.Stripe === "function"` (`old :128-133`) | **Removed.** Replaced by waiting on `add-payment-element-fields` visibility (`:235`) and the tab reporting `aria-selected` (`:146-149`) |

### Selector-by-selector

| Concern | Old selector | New selector |
|---|---|---|
| Pick "credit card" | `label[for="payment-method-type-credit-card"]` then `addModal` button `Continue` (`old :288-289`) | `#card-tab` inside the element, clicked until `aria-selected="true"` (`:145-149`) |
| Pick "ACH" | `label[for="payment-method-type-ach"]` then `Continue` (`old :208-209`) | `#us_bank_account-tab`, same retry (`:145-149`) |
| Card number | `iframe[title="Secure card number input frame"]` → `input[name="cardnumber"]` (`old :298`) | `#payment-numberInput` (`:288`) |
| Expiry | `iframe[title="Secure expiration date input frame"]` → `input[name="exp-date"]` (`old :299`) | `#payment-expiryInput` (`:289`) |
| CVC | `iframe[title="Secure CVC input frame"]` → `input[name="cvc"]` (`old :300`) | `#payment-cvcInput` (`:290`) |
| Cardholder name | `add-credit-card-v2-form-name-input` (`old :302`) | **Gone** — Payment Element does not collect it |
| Billing address1 / city / zip | `add-credit-card-v2-form-address1-input` / `-city-input` / `-zip-code-input` (`old :303-305`) | Only postal code survives, as Stripe's `#payment-postalCodeInput` (`:294`) |
| State | `add-credit-card-v2-form-state-search-trigger` + keyboard type-ahead + `-state-container` text assert (`old :309-312`) | **Gone** — no state field |
| Country | not handled | `#payment-countryInput` `.selectOption("US")` — **new**, because Stripe preselects country from caller IP and country decides whether a postal-code field renders at all (`:291-293`) |
| ACH account-holder name | `add-ach-v2-form-name-input` (`old :214`) | `#payment-nameInput` (`:253`) |
| ACH account-holder email | `add-ach-v2-form-email-input` (`old :215`) | `#payment-emailInput` (`:252`) |
| Open bank picker | `add-ach-v2-connect-bank`, clicked in a 3-attempt loop re-running `waitForStripeReady` (`old :219-231`) | `#payment-bankInput` → `menuitem` named `"Test (OAuth)"` (`:254-255`) |
| Bank-connected confirmation | `add-ach-v2-bank-connected-flag` visible **and** containing `"Your account is connected"` (`old :235-236`) | Stripe's `tabpanel` containing `6789` (`:260`) — the only in-form signal left |
| ACH mandate | `add-ach-v2-mandate-checkbox-label-text` copy assert, `dispatchEvent("click")` on `-label`, then `toBeChecked()` on `-mandate-checkbox` (`old :237-242`) | **Gone** — no separate mandate control |
| Submit button | `action-buttons-save` (`old :90`) | `add-payment-method-submit` (`:95`) |
| Error banner | `action-buttons-error-message` (`old :87`) | `add-payment-method-error-message` (`:92`) |
| Field-fill helper | `fillStripeCardField(page, frameTitle, inputName, value)` — resolved the frame itself (`old :252-261`) | `fillStripeInput(input, value)` — takes an already-resolved `Locator` (`:154-162`); retry-on-dropped-digits logic is unchanged |

### Copy assertions lost

The old module asserted four pieces of product copy so a silent wording change would fail the test. Three are now unassertable because the markup that carried them no longer exists:

| Copy constant | Old line | Now |
|---|---|---|
| `INSTANT_VERIFICATION_HELP_NOTE` ("Only banks that support instant verification are available…") | `old :116-117`, asserted `old :213` | **Removed** |
| `BANK_CONNECTED_FLAG_COPY` ("Your account is connected") | `old :118`, asserted `old :236` | **Removed** |
| `MANDATE_CHECKBOX_COPY` ("I verify that the bank account I am adding is a business account…") | `old :119-120`, asserted `old :237` | **Removed** |
| `CC_SUPPORTED_TYPES_COPY` ("Supported card types: Visa, Mastercard, American Express, Discover") | `old :123`, asserted `old :293` | **Removed** |
| `CHARGE_DISCLAIMER_COPY` | `old :121`, asserted `old :238` and `old :294` | **Retained** at `:121`, asserted once in `openAddPaymentMethodModal` (`:234`) |

The ACH mandate is the material one: the old test proved a Zocdoc-rendered business-account attestation was displayed and had to be actively accepted before a bank could be saved. Nothing in the new module asserts any mandate text, and nothing asserts that acceptance is required. If the Payment Element still surfaces a mandate, it is now inside Stripe's iframe and unverified; if the rebuild dropped it, this suite would not notice.

### Timing guards added by `dac52b65`

Three, each documented in the commit message and in code:

1. `selectPaymentMethodTab` (`:141-150`) — Stripe mounts tab markup before wiring its click handler, so an early click is silently swallowed and the form silently stays on the default tab. Click until `aria-selected="true"`, 45s budget.
2. `advanceFinancialConnections` (`:181-194`) — Financial Connections stacks screens in the DOM rather than replacing them, so a passed screen leaves its button behind wedged in a disabled "Loading…" state. Walk from the **end** of the button list and require `isVisible() && isEnabled()`.
3. Country pinning (`:291-293`) — pin `US` so the form is identical on a laptop and on CI.

### Additional guard in the uncommitted working-tree diff

`connectStripeTestBank` (`:201-226`): two `while (Date.now() < deadline)` loops with `page.waitForTimeout(2000|1000)` became `expect(async () => {...}).toPass({intervals:[1_000], timeout:...})`. Same 90s and 60s budgets. Two behavior improvements: the old post-connect loop could `return` silently on success but fell through to a bare `expect(...).toHaveCount(0)` on timeout, whereas the new form always reports the iframe that never went away; and `advanceFinancialConnections` is now called only while the target state is absent, so a screen is never clicked past.

---

## Server-side contract encoded in comments (not asserted anywhere)

`support/billing.ts:71-77` documents a real backend behavior discovered by these tests and worked around rather than tested:

> `savePaymentMethodAttributes` rejects (500) any payload whose payment-method set does not exactly equal the practice's persisted set ("Attributes for all payment methods for the practice should be passed").

`reloadPaymentMethods` (`:78-89`) exists solely to work around it, and both specs must call it before the *first* monthly-limit save and again before the *first* rollover save (`billing-settings-page.spec.ts:106,165`; `billing-user-flow.spec.ts:170,229`), with in-spec comments explaining that a stale list poisons the save "for the rest of the run". No test asserts this contract; it is only routed around. That is a genuine L4 API-contract gap.

---

## Candidate Gaps

| # | What's missing | Correct test level | File path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| H1 | `savePaymentMethodAttributes` requires the client to send the practice's **complete** payment-method set or it 500s. This is documented only as a prose comment and worked around by a page reload; nothing asserts it. | **L4 `api`** | `playwright/support/billing.ts:71-89` | A whole-set-or-500 write API on the money path, with no contract test. Any client that sends a partial set silently 500s, and the failure mode ("poisoned for the rest of the run") is exactly what a partial-set bug in production would look like to a provider editing a monthly limit. | M | **P0** |
| H2 | The ACH business-account mandate is no longer asserted at all. The pre-`dac52b65` module asserted the mandate copy, that the checkbox had to be actively clicked, and that it registered as checked (`old :237-242`). | L5, plus L2 for the copy | `playwright/support/billing.ts:239-264` | A compliance attestation on a bank-debit authorization. If the Payment Element rebuild dropped or weakened it, this suite passes anyway. Needs a product answer on where the mandate now lives, then an assertion. | S | **P0** |
| H3 | Three other product-copy assertions were dropped with the rebuild: instant-verification help note, "Your account is connected", supported-card-types list. Only `CHARGE_DISCLAIMER_COPY` survives. | L2 `component` (in `provider-fe-monorepo`), not L5 | `playwright/support/billing.ts:120-121` | Copy assertions are cheap and belong at component level against mocks; they were only in E2E because that was the only suite that existed. Losing them is fine *if* they land in the monorepo — currently they landed nowhere. | S | **P2** |
| H4 | `rolloverRowById` targets `[id="rollover-checkbox-<id>"]` — a raw DOM `id`, the only non-`data-test` Zocdoc selector in the module. | L5 | `playwright/support/billing.ts:44-48` | The repo's own convention is `data-test` (`CLAUDE.md`, "Tests use `data-test` attributes for element selection"). A React-generated-id refactor breaks all six rollover call sites with no product change. Ask the monorepo for `data-test="rollover-row-<id>"`. | S | **P2** |
| H5 | 14 of the selectors this module depends on are Stripe-owned (`#payment-*Input`, `#*-tab`, `iframe[src*=...]`, and 7 copy-matched buttons in Stripe's hosted Financial Connections UI). No canary or contract check warns when Stripe changes them. | L5 | `playwright/support/billing.ts:118-226, 252-294` | This is the documented root cause of `dac52b65`: both billing specs were red from 2026-09-02 and someone had to diagnose it from a selector timeout. A dedicated, fast Stripe-surface canary would name the cause immediately and keep it out of the money-path suite's failure signal. | M | **P2** |
| H6 | `listPaymentMethodIds` is exported and re-exported through `support/index.ts:87` but consumed by no spec. | — | `playwright/support/billing.ts:14-18`; `playwright/support/index.ts:87` | Dead public API; either make it private or document the intended use. | S | **P3** |
| H7 | `dac52b65` is unmerged and this file carries further uncommitted edits, so no billing E2E works on `main`. | L5 | `playwright/support/billing.ts` | Until merged, billing E2E coverage on `main` is 0 working tests. Commit the working-tree `toPass` refactor and merge. | S | **P0** |

---

## Level Summary

| Level | Label | Count | Notes |
|---|---|---|---|
| L1 | `unit` | 0 | No test in this file. |
| L2 | `component` | 0 | — |
| L3 | `integration` | 0 | — |
| L4 | `api` | 0 | One API contract is *documented* here (`:71-77`) and zero are asserted. See H1. |
| L5 | `e2e` | 0 tests; **supports 4** | Consumed by 4 L5 billing tests across 2 spec files. |

| Metric | Exact value |
|---|---|
| Total lines | 365 |
| Top-level declarations | 18 |
| Exported symbols | 10 (8 functions/factories + 2 consts) |
| Module-private functions | 8 |
| Exported but unused by any spec | 1 (`listPaymentMethodIds`) |
| Zocdoc `data-test` ids depended on | 22 |
| Stripe-owned selectors depended on | 14 |
| Non-`data-test` Zocdoc selectors | 1 (`[id="rollover-checkbox-<id>"]`, `:47`) |
| Product-copy assertions: before `dac52b65` → after | 5 → 1 |
| Real (unmocked) third-party flows driven | 2 (Payment Element card entry; Financial Connections OAuth) |
