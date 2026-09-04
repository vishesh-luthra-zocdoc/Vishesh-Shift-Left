# Billing Coverage: `sandbox` vs `provider-fe-monorepo/apps/settings/e2e`

**sandbox revision analyzed:** working tree at `dac52b65a3ae89cd756c3951e58ae3fec0ce3b1d` (branch `fix/billing-stripe-payment-element`); `origin/main` at `4bb607cc942b03c067d5755eb8192ebfaf27d227`
**monorepo source:** read-only snapshot `/tmp/slv3/snapshots/provider-fe-monorepo/apps/settings/e2e/` (NOT `~/provider-fe-monorepo`, which is stale). **UNVERIFIED —** the snapshot carries no git metadata, so I cannot record a monorepo SHA. Obtaining one requires the snapshot's provenance from the orchestrator.
**Level:** both sides are Playwright browser tests → both **L5 `e2e`** under the v3 taxonomy. They are *not* the same kind of L5, and that difference drives the whole recommendation.

## The environment difference (the crux)

| | sandbox | monorepo `apps/settings/e2e` |
|---|---|---|
| Target | Deployed **production**, `baseURL: "https://www.zocdoc.com/"` | Locally served app. **UNVERIFIED —** no Playwright config in the snapshot (`apps/settings/` contains only `e2e/` and `src/`), so I cannot cite the `baseURL`/`webServer`. Verified indirectly: specs import mocks from `../../src/server/controllers/practiceBillingSettingsPage/mocks`, i.e. the app's own source tree. |
| Evidence | `playwright.config.ts:23` | `billing-settings-page.spec.ts:14` |
| Data | Real production practices. 3 real test accounts. | `practiceId = '<test-practice-id>'` hardcoded, resolved entirely from `mockPracticeBillingSettingsViewModel`. |
| Backend | **Real.** Every billing write hits the real API. | **Fully stubbed.** Every route `page.route`-fulfilled: `GET_BILLING_SETTINGS_PATH`, `SET_DEFAULT_PAYMENT_METHOD_PATH`, `DELETE_PAYMENT_METHOD_PATH`, `SAVE_PAYMENT_METHOD_ATTRIBUTES_PATH`, `UPDATE_BILLING_EMAIL_PATH`, `UPDATE_PRIMARY_BUSINESS_ADDRESS_PATH`, `BILL_SUMMARY_PATH`, `SETUP_INTENT_PATH`, `PAYMENT_METHOD_V2_PATH`, recovery paths (`billing-settings-page-commands.ts:192-346`). Its header states every Cypress passthrough was ported to a full stub because "no real body was produced downstream" (`:1-16`). |
| Stripe | **Real Stripe.** Real Payment Element iframe, real Financial Connections OAuth against Stripe's `"Test (OAuth)"` sandbox institution. `support/billing.ts:239-242, 276-278` both say "no mocking". | **Faked out.** `SHOULD_MOCK_STRIPE=true` cookie in every billing spec's `beforeEach`; the element is replaced by a single Zocdoc-owned `mock-stripe-payment-input` (`billing-settings-payment-element.spec.ts:36-40, 52`). Stripe's SDK is never exercised. |
| Clock | Real. | `page.clock.install({time: new Date('2026-04-15')})` / `'2026-02-15'` (`billing-settings-page.spec.ts:23, 56`) to force bills into the past. |
| Side effects | **Destructive on real practices.** Cards created/deleted, defaults changed, rollovers reordered, billing email rewritten. | **None.** |
| Cost of a run | Minutes; Stripe-dependent; flaky by construction. | Fast, hermetic. |
| Failure meaning | "Production is broken **or** Stripe changed its DOM **or** the shared account drifted." | "This app's rendering/wiring against a fixed contract is broken." |

Only **sandbox** can catch a broken deployment, a real Stripe integration break, a bad backend contract, or an environment/config regression. Only the **monorepo** can cheaply cover branches, error states and edge-case data, because it can dictate the response.

---

## Table 1 — sandbox vs the same-named `billing-settings-page.spec.ts` (as scoped)

sandbox side: `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` (2 tests) plus its duplicate in `Account-User-Setup/Flows/billing-user-flow.spec.ts:87-451` (2 tests).
monorepo side: `PracticeSettingsPages/billing-settings-page.spec.ts` — **7 tests** in 2 describes (`:20`, `:52`).

| # | Journey / assertion | sandbox? | monorepo `billing-settings-page.spec.ts`? | Verdict |
|---|---|---|---|---|
| 1 | Billing settings page renders its container without an error state | Yes — `billing-settings-container` visible (`:73-75`) | Yes — `selectors.billingSettingsPage.view` = `billing-settings-container` exists (`:138`, `selectors.ts:34`) | **duplicate** (only genuine overlap; same testid asserted on both sides) |
| 2 | Error page shown when `practiceId` is empty | No | Yes — `shows error if practice id not passed` (`:35-41`), asserts `error-state-text` | **monorepo-only** |
| 3 | Error page shown when the billing-settings fetch fails | No | Yes — `shows error if fetch billing settings fails` (`:43-49`), via `doesBillingSettingsFetchFail: true` | **monorepo-only** |
| 4 | Billing completion modal survives `businessAddress.address1 = null` | No | Yes (`:123-140`) | **monorepo-only** |
| 5 | …`city = null` | No | Yes (`:142-159`) | **monorepo-only** |
| 6 | …`state = null` | No | Yes (`:161-178`) | **monorepo-only** |
| 7 | …`zipCode = null` | No | Yes (`:180-197`) | **monorepo-only** |
| 8 | …`practiceBillingEmail = null` | No | Yes (`:199-213`) | **monorepo-only** |
| 9 | Navigate inbox → sidebar Settings → Billing, land on `/provider/config/settings/billing` | Yes (`:61-64`) | No — visits the page directly | **sandbox-only** |
| 10 | Add a credit card end to end (real Stripe Payment Element, card tokenized and persisted) | Yes (`:88-93`; `billing.ts:279-298`) | No | **sandbox-only** |
| 11 | Add an ACH method via real Stripe Financial Connections OAuth | Yes (`:95-100`; `billing.ts:243-264`) | No | **sandbox-only** |
| 12 | Set a monthly limit ($5000) on a payment method | Yes (`:102-122`) | No | **sandbox-only** |
| 13 | Edit an existing monthly limit ($5000 → $10000) | Yes (`:124-139`) | No | **sandbox-only** |
| 14 | Remove a monthly limit | Yes (`:141-151`) | No | **sandbox-only** |
| 15 | Set a payment method as default | Yes (`:153-159`) | No | **sandbox-only** |
| 16 | Enable rollover on a payment method | Yes (`:161-179`) | No | **sandbox-only** |
| 17 | Reorder rollover priority (move up) | Yes (`:181-189`) | No | **sandbox-only** |
| 18 | Disable rollover | Yes (`:191-206`) | No | **sandbox-only** |
| 19 | Delete a payment method (confirmation modal, count decrements) | Yes (`:220-237`, `:364-377`) | No | **sandbox-only** |
| 20 | Open an invoice from `bill-row`, assert `fpb-invoice-view`, `amount-due-row`, PDF button enabled, footer link | Yes (`:239-256`) | No | **sandbox-only** |
| 21 | "Back to Billing" returns to the settings page | Yes (`:258-269`) | No | **sandbox-only** |
| 22 | Billing contact info section labels + Edit link | Yes (`:258-269`) | No | **sandbox-only** |
| 23 | Edit-contact-info modal field set + accessible names + Cancel | Yes (`:271-303`) | No | **sandbox-only** |
| 24 | Change the billing email and see it persist | Yes (`:305-317`) | No | **sandbox-only** |
| 25 | Pricing tab renders `free-products-card` + `pricing-contact-us` | Yes (`:331-339`) | No | **sandbox-only** |
| 26 | Payment/Pricing tab strip visible with correct labels | Yes (`:76-79`) | No | **sandbox-only** |

**Verdict on the scoped comparison: not duplicates.** 1 of 26 rows overlaps, and it is the weakest possible assertion ("the page rendered"). The two files share a filename and a page under test; they share essentially no coverage. The monorepo file is a **null-data / error-state** suite; the sandbox file is a **happy-path mutation** suite.

---

## Table 2 — sandbox vs the monorepo's *sibling* billing specs (where the real duplication is)

Table 1 answers the question as posed, but it would be misleading on its own. `PracticeSettingsPages/` contains **7 billing spec files, 63 tests total**, and the sandbox journeys are duplicated almost step-for-step by the siblings — not by the same-named file.

| File | Tests |
|---|---|
| `billing-settings-page.spec.ts` | 7 |
| `billing-settings-v2.spec.ts` | 16 |
| `billing-invoice-summary.spec.ts` | 20 |
| `billing-pricing-v2.spec.ts` | 11 |
| `billing-settings-payment-element.spec.ts` | 4 |
| `payment-recovery.spec.ts` | 4 |
| `invoice-details-page.spec.ts` | 1 |
| **Total** | **63** |

| # | sandbox journey | monorepo sibling covering it | Verdict |
|---|---|---|---|
| 10 | Add a credit card (submit → setup intent → payment method saved) | `billing-settings-payment-element.spec.ts:44-61` `submits the unified form and saves a payment method`; `:30-41` `renders the unified form with no type-picker` | **duplicate at the mock level.** sandbox uniquely covers *real Stripe*; the monorepo covers the *form wiring*. |
| 11 | Add ACH via Financial Connections | none (Stripe is mocked to one input) | **sandbox-only** |
| 12–14 | Set / edit / remove monthly limit | `billing-settings-v2.spec.ts:228` `sets a monthly limit for a payment method without a limit`; `:278` `edits an existing monthly limit for a payment method` | **duplicate** (remove-limit: monorepo coverage not found → **sandbox-only**) |
| 15 | Set default payment method | `billing-settings-v2.spec.ts:181` `sets a non-default payment method as default`; `:745` `sets default payment method for a provider in the "See by provider" modal` | **duplicate** |
| 16–18 | Enable / reorder / disable rollover | `billing-settings-v2.spec.ts:56` `opens modal, makes changes to modal and verifies results` (in `describe('Edit rollovers')` `:55`) | **duplicate** |
| 19 | Delete a payment method | `billing-settings-v2.spec.ts:341` `deletes a non-default payment method` | **duplicate** |
| 22–24 | Contact info content, modal fields, save billing email | `billing-settings-v2.spec.ts:459` `verifies billing contact info has the correct content`, `:474` `prepopulates contact info fields`, `:524` `requires required fields`, `:561` `saves changes to contact info` | **duplicate**, and the monorepo goes further (required-field validation) |
| 20 | Invoice view: amount due, PDF button, footer link, bill selection | `billing-invoice-summary.spec.ts:146` `should display amount due row`, `:172` `should render PDF button when PDF is available`, `:155` `should display footer with Eastern Time note and billing link`, `:193` `should show checkmark on the currently selected bill` | **duplicate**, and the monorepo is far more granular (20 tests) |
| 21 | "Back to Billing" link | `billing-invoice-summary.spec.ts:250` `should display "Back to Billing" link`, `:256` `should have a clickable "Back to Billing" link` | **duplicate** |
| 25–26 | Pricing tab / tab strip | `billing-pricing-v2.spec.ts:185` `renders V2 pricing tab` + 10 more, incl. `:225` `shows V2 marketplace card when enrolled in marketplace` | **duplicate**, and the monorepo asserts the `marketplace-card` that sandbox explicitly declines to assert (`billing-user-flow.spec.ts:405-411`) |
| 9 | Sidebar navigation into billing | none found | **sandbox-only** |
| — | Error states: update-address failure, update-email failure | `billing-settings-v2.spec.ts:659`, `:704` | **monorepo-only** |
| — | Add-payment-method **failure recovery**: reuse a confirmed method after a failure; re-run the flow when details are edited after a failure | `billing-settings-payment-element.spec.ts:63`, `:105` | **monorepo-only** — and this is the gap sandbox's own retry helper papers over (`support/billing.ts:91-115`) |
| — | Payment recovery / "Pay Now": banner → review → pay, update-only mode, overflow layout, banner copy | `payment-recovery.spec.ts:96, 156, 233, 276` | **monorepo-only** |
| — | Pricing calculator V2 walkthrough + close | `billing-settings-v2.spec.ts:838`, `:989` | **monorepo-only** |
| — | Invoice formatting: SPO asterisk, taxes/fees line items, credits, healthcare-platforms row pre/post cutoff, booking-source ordering | `billing-invoice-summary.spec.ts:82, 92, 138, 271, 286, 297` | **monorepo-only** |

**Net:** of sandbox's ~26 distinct billing assertions/journeys, **roughly 20 are already covered at the mock level in the monorepo**, in more granular form. Sandbox's genuinely unique value reduces to a small set: real Stripe card tokenization, real Financial Connections ACH linking, real backend persistence of payment-method attributes, real invoice data, and the sidebar navigation path.

---

## Which repo SHOULD own what

The rule that falls out of the environment table: **the monorepo owns everything a mock can decide; sandbox owns only what requires the real deployment and the real third party.** Sandbox's cost per test is not just runtime — it is a destructive write on a shared production practice (`support/billing.ts:305-365` deletes payment methods before every test). Every assertion that a mock could have made is paying that cost for nothing.

### Move to the monorepo (delete from sandbox)

| Journey | Target level | Why |
|---|---|---|
| Page structure / tab labels / contact-info section copy (`billing-settings-page.spec.ts:72-86, 258-269`) | **L2 `component`** in the monorepo | Pure rendering against a fixed view model. Already largely covered by `billing-settings-v2.spec.ts:459-474`. Needs zero backend. |
| Edit-contact-info modal field set, accessible names, Cancel behavior (`:271-303`) | **L2 `component`** | Form-shape assertions. The spec's own comment already points at a monorepo issue (`provider-fe-monorepo#11928`) — the assertion belongs where the component lives. |
| Monthly-limit set/edit/remove modal mechanics (`:102-151`) | **L3 `integration`** (monorepo, MSW/route-stubbed) | Duplicated by `billing-settings-v2.spec.ts:228, 278`. Sandbox adds nothing but a real 500-prone write (see `support/billing.ts:71-77`). |
| Rollover enable/reorder/disable modal mechanics (`:161-206`) | **L3** | Duplicated by `billing-settings-v2.spec.ts:56`. |
| Set-default and delete-method modal mechanics (`:153-159, 220-237`) | **L3** | Duplicated by `billing-settings-v2.spec.ts:181, 341`. |
| Invoice view field presence, PDF-button enabled, footer link (`:239-256`) | **L3** | Duplicated far more thoroughly by `billing-invoice-summary.spec.ts` (20 tests). Sandbox's version additionally *depends on the shared production practice having invoices*, which is a flake source unrelated to the code. |
| Pricing tab content (`:331-339`) | **L3** | Duplicated by `billing-pricing-v2.spec.ts` (11 tests), which also asserts the `marketplace-card` sandbox skips. |

### Keep in sandbox (irreplaceable)

| Journey | Why only sandbox can do it |
|---|---|
| Add a credit card through the **real** Stripe Payment Element and confirm it persists (`support/billing.ts:279-298`) | The monorepo swaps the element for `mock-stripe-payment-input` (`billing-settings-payment-element.spec.ts:36-40`). Only sandbox would have caught the DOM change behind `dac52b65`. |
| Add ACH through **real** Stripe Financial Connections OAuth (`support/billing.ts:243-264`) | No mock can validate a live OAuth handoff and a real bank-account token. |
| Backend persistence of payment-method attributes across a **real page reload** (`support/billing.ts:78-89`; `billing-user-flow.spec.ts:304-310`) | This is precisely where `savePaymentMethodAttributes`'s whole-set-or-500 behavior lives — mocks cannot reproduce it. |
| Sidebar navigation into billing from the inbox/dashboard shell (`billing-settings-page.spec.ts:61-64`) | Cross-app navigation through the deployed provider shell; the monorepo serves `apps/settings` alone. |
| One thin post-deploy smoke: billing page loads, real bills render, real default method shows | Deployment/config health. Non-mutating, so it can run in parallel without the serialization problem. |

### Target shape

Sandbox billing should go from **4 tests (2 distinct, ~26 assertions, ~20 destructive writes, run twice)** to **2 tests**:

1. `billing add-payment-method — real Stripe (card + ACH)` — add each method, assert it persisted after a reload, delete it. Its only job is proving the real Stripe integration and the real backend write. Must live in `Provider-Billing/Flows/` (which does not exist yet), with `mode: "serial"`, `retries: 0`, and a comment naming the shared-practice constraint.
2. `billing settings — production smoke` — non-mutating: page loads, bills render, default method present, Pricing tab renders. Safe to parallelize.

Everything else moves to `provider-fe-monorepo` as L2/L3, where most of it **already exists**. And the duplicate block at `billing-user-flow.spec.ts:87-451` should be deleted outright — it re-runs the same production mutations for one extra assertion.

---

## Candidate Gaps

| # | What's missing | Correct test level | File path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| C1 | ~20 of sandbox's ~26 billing assertions are already covered at mock level in `provider-fe-monorepo` `billing-settings-v2` / `billing-invoice-summary` / `billing-pricing-v2` / `billing-settings-payment-element`. Sandbox pays for them with destructive production writes on a shared practice. | L5 → delete; already L3 in monorepo | `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts`; `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts:87-451` | Every removed assertion removes a real mutation from a shared production billing account and cuts a flake source. Net coverage loss ≈ 0 because the monorepo equivalents exist. | M | **P1** |
| C2 | Nobody owns the split. Neither repo documents which side owns which billing journey; `Provider-Billing/OWNERSHIP.md` scopes the *feature* (`#practice-billing-team`, Jira `BILL`) but says nothing about test-level placement. | — (process) | `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` | Without a written rule, both suites keep growing toward each other. This is how sandbox ended up re-testing modal copy against production. | S | **P1** |
| C3 | Real Stripe is exercised **only** in sandbox, and only inside the two heavyweight all-in-one tests. `dac52b65` shows a Stripe DOM change took both billing tests down for ~2 days with a selector timeout as the only signal. | L5 | `/Users/vishesh.luthra/sandbox/playwright/support/billing.ts:118-226` | The single most valuable thing this repo does for billing has no dedicated, fast, clearly-named test. Split the real-Stripe add flows into their own small spec so a Stripe break is unambiguous and isolated from the rest. | M | **P1** |
| C4 | Add-payment-method **failure** paths (reuse a confirmed method after a failure; re-run the flow when details are edited after a failure) exist in the monorepo (`billing-settings-payment-element.spec.ts:63, 105`) but there is no equivalent against real Stripe/real backend — and sandbox's `saveAddPaymentMethodWithRetry` actively retries *past* such failures. | L5 (thin) + L4 for the backend contract | `/Users/vishesh.luthra/sandbox/playwright/support/billing.ts:91-115` | Double-charging or orphaning a Stripe payment method on retry is a money bug. Sandbox's retry loop would mask exactly that. | M | **P1** |
| C5 | Payment recovery / "Pay Now" (`payment-recovery.spec.ts:96-276`) — the flow where a provider actually **pays money** — is covered only against mocks. Nothing exercises it against real Stripe or the real backend. | L5 (real-Stripe smoke) + L4 | none in sandbox | This is the highest-value money path in the billing surface and it has zero real-environment coverage in either repo. Needs an explicit decision on whether a production test is acceptable here. | L | **P1** |
| C6 | Pricing-tab `marketplace-card` is asserted in the monorepo (`billing-pricing-v2.spec.ts:225`) but deliberately **not** in sandbox, with an in-code note that enterprise practices render Pricing without it (`billing-user-flow.spec.ts:405-411`). Nobody reconciled the two. | L5 / L3 | `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts:401-412` | Either production has a real enterprise-practice bug the mocked suite cannot see, or sandbox's test account is misconfigured. Both need answering; today the divergence is a comment. | S | **P2** |
| C7 | Invoice **content** correctness (SPO asterisk, taxes/fees line items, Zocdoc credits, healthcare-platforms row, booking-source ordering) is asserted only against mock bodies. Sandbox reads real invoices but asserts only that four elements are visible. | L3 (monorepo, keep) + one L5 real-data shape check | `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts:239-256` | A real invoice whose totals are wrong passes both suites: the monorepo asserts against a mock that is correct by construction, sandbox asserts only element presence. | M | **P1** |
| C8 | The monorepo snapshot has no recorded revision, so this comparison cannot be reproduced. | — (process) | `/tmp/slv3/snapshots/provider-fe-monorepo/` | A comparison that can't be re-run becomes stale silently and the resulting tickets can't be verified. Record the monorepo SHA alongside the snapshot. | S | **P2** |

---

## Level Summary

| Level | Label | sandbox billing tests | monorepo `PracticeSettingsPages` billing tests | Notes |
|---|---|---|---|---|
| L1 | `unit` | 0 | 0 (none in `e2e/`) | Monorepo unit/component tests live outside `e2e/` and are out of this file's scope. |
| L2 | `component` | 0 | 0 | Several monorepo E2E tests *behave* like L2 (fully mocked single-page render) but run in a browser, so per CONVENTIONS they are L5. Flagged as a misplacement, not reclassified. |
| L3 | `integration` | 0 | 0 | — |
| L4 | `api` | 0 | 0 | The `savePaymentMethodAttributes` whole-set-or-500 contract (`support/billing.ts:71-77`) is untested at L4 on both sides. |
| L5 | `e2e` | **4** | **63** | sandbox: real production + real Stripe. monorepo: locally served + fully mocked backend + mocked Stripe. |

| Comparison metric | Exact value |
|---|---|
| sandbox billing spec files / tests | 2 / 4 (2 distinct after de-duplication) |
| monorepo billing spec files / tests in `PracticeSettingsPages/` | 7 / 63 |
| Same-named file comparison (Table 1) rows | 26 |
| — `duplicate` | 1 |
| — `sandbox-only` | 18 |
| — `monorepo-only` | 7 |
| Sibling-spec comparison (Table 2): sandbox journeys duplicated at mock level | ~20 of ~26 **(estimate** — "journey" granularity differs between a sandbox `test.step` and a monorepo `test()`, so the mapping is 1-to-many; counted as steps with a named monorepo counterpart**)** |
| sandbox journeys with no monorepo counterpart | 4 (real-Stripe card add, real-Stripe ACH add, real backend persistence across reload, sidebar navigation) |
| Monorepo billing specs mocking Stripe via `SHOULD_MOCK_STRIPE` | 6 of 7 (`billing-settings-payment-element.spec.ts` uses `mock-stripe-payment-input` without the cookie) |
