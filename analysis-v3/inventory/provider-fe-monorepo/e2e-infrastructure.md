# provider-fe-monorepo — E2E Test Infrastructure (`apps/settings/e2e/`)

| Field | Value |
|---|---|
| Repo | `provider-fe-monorepo` |
| Revision analyzed | `dd9e4952a6` (`origin/main`, 2026-09-03) |
| Snapshot path | `/tmp/slv3/snapshots/provider-fe-monorepo/` |
| Framework | Playwright (Cypress deleted monorepo-wide in `e44f4ff75f`, jsplat-759) |
| Support LOC (billing-relevant) | 1,990 |

**Headline finding: nothing in this suite talks to a real backend.** Every HTTP call the application
makes during a billing E2E test is intercepted and fulfilled in-process, Stripe.js is replaced by a
hand-written fake, and authentication is bypassed by stubbing the session endpoints while `/login/*`
is deliberately made to return `500`. All 63 billing tests are therefore flagged under
[Tests that mock their whole backend](#tests-that-mock-their-whole-backend) — which is all of them.

---

## File map

| Path (relative to `apps/settings/e2e/`) | LOC | Role |
|---|---|---|
| `fixtures.ts` | 119 | Extended `test` fixture — Stripe fake + suite-wide network stubs |
| `helpers.ts` | 860 | Selector builders, assertions, navigation, cookie bootstrap, AB stubs |
| `PracticeSettingsPages/billing-settings-page-commands.ts` | 562 | Billing route stub table + `waitFor*` + billing UI actions |
| `PracticeSettingsPages/selectors.ts` | 200 | `data-test` string tree (shared with the staff-page specs) |
| `PracticeSettingsPages/pageObjects/PageObject.ts` | 18 | Abstract base |
| `PracticeSettingsPages/pageObjects/BillingSettingsPagePageObject.ts` | 46 | Contact-info assertion |
| `PracticeSettingsPages/pageObjects/EditBillingContactInfoModalPageObject.ts` | 185 | Contact-info modal driver |
| **Total** | **1,990** | |

Non-billing specs sharing this infrastructure: `PracticeUsersPage/*.spec.ts`,
`ConsolidatedProvidersAndStaffPage/*.spec.ts`. Their "Billing" string matches are permission-role
labels (`Billing` as a staff role), **not** billing functionality — checked and excluded from the
billing inventory.

---

## `fixtures.ts` — the mandatory entry point

Every billing spec imports `{ test, expect }` from `../fixtures` (verified in all 7 files). The
fixture is `base.extend({ page: async ({ page }, use) => {...} })`, so its setup runs for every test
before any spec code.

| Line | What it installs | Effect |
|---|---|---|
| :27-31 | `page.addInitScript` setting cookie `zd_global_nav_coachmark_shown=true` | suppresses the nav coachmark overlay |
| **:32** | `page.addInitScript(installStripeJsFake)` | **replaces `window.Stripe` before app code runs — unconditional, every test** |
| :34-41 | `page.route('**/login/*')` GET → `500` after a 200 ms delay | login is deliberately broken so the app never redirects to a real IdP |
| :43-81 | `page.route('**/provider/v1/gql')` POST → `getPracticeOrg` / `getPracticeLocations` fixed payloads, else `{data:{}}` | GraphQL never leaves the process |
| :83-89 | `**/auth/checksession` → `200 {Redirect:false, Timeout:9999}` | session always valid |
| :91-97 | `**/auth/touchsession` → same | session never expires |
| :99-105 | `**/auth/user/v1/refresh` → `200 {expiry_in_seconds:9999}` | token refresh never fails |
| :107-113 | `**/phi-ab/v1/assignments` → `route.continue()` | later overridden — see note below |

The file's own docstring (:1-14) states specs import from here "so they inherit the same fallback
network stubs every Cypress spec received", listing the login-500 / gql / assignments trio.

**Dead handler.** `fixtures.ts:107` registers `route.continue()` for `POST **/phi-ab/v1/assignments`,
but `setupNewAbExperiments` (`helpers.ts:828-860`) registers a `201` stub on the same pattern later,
and Playwright evaluates handlers most-recently-registered first. Since
`setUpRoutesAndVisitBillingPage` always calls `setupNewAbExperiments`
(`billing-settings-page-commands.ts:115`), the fixture handler is unreachable for every billing test.
Low severity, but it means a reader cannot tell from `fixtures.ts` whether AB assignments are real.

---

## Authentication and session strategy

**There is no authentication.** No login is performed, no credential is supplied, no session cookie
from a real IdP is used.

| Concern | How it is handled | Evidence |
|---|---|---|
| Login | `GET **/login/*` stubbed to `500` | `fixtures.ts:34-41` |
| Session validity | `checksession` / `touchsession` stubbed valid for 9999s | `fixtures.ts:83-97` |
| Token refresh | stubbed to `200` | `fixtures.ts:99-105` |
| User identity | cookie `mockUserInfo`, read by app bootstrap | `helpers.ts` `givenIsInternalUser`, `mockBootstrappedUserInfo` |
| Practice identity | cookie `mockPracticeDetails` + a `practiceId` query param | `helpers.ts` `overridePracticeDetails`; specs pass `practiceId` into the URL |
| Navbar / org | cookie `mockNavbarInfo` + gql `getPracticeOrg` stub | `helpers.ts` `givenNavbarInfo`; `fixtures.ts:43-81` |

Consequence: **zero coverage of auth-adjacent billing failures** — an expired session mid-payment, a
403 from the billing API for a user lacking the Billing role, or a cross-practice authorization
mistake. All three are plausible production bugs and all three are invisible to this suite. (Not
listed as a billing gap below because auth is another team's surface; noted here for the
orchestrator.)

---

## Bootstrap-by-cookie mechanism (and its ordering trap)

Application state is injected by writing cookies that `src/utils/localhostBootstrapSetup` reads
**at page load**. Therefore every `given*` helper must be called **before** navigation, or it has no
effect.

| Helper | Cookie written | Purpose |
|---|---|---|
| `givenFeatureFlags` | `mockFlagContent` | feature flags |
| `givenNavbarInfo` | `mockNavbarInfo` | navbar payload |
| `givenIsInternalUser` | `mockUserInfo` (`is_internal_user`) | internal-user gating |
| `overridePracticeDetails` | `mockPracticeDetails` | practice fields |
| `mockBootstrappedUserInfo` | `mockUserInfo` | full user object |
| `hideBillingCompletionModal` | `has_seen_billing_completion_modal` + matching `localStorage` | suppress first-visit modal |
| `showBillingCompletionModal` | inverse of the above | force the modal |

`COOKIE_DOMAIN` is derived from `process.env.PLAYWRIGHT_BASE_URL` falling back to
`http://localhost:3000` (`helpers.ts:18`), so this suite is designed to run against a locally served
app, not a deployed environment.

This is a fragile contract with no enforcement: nothing fails loudly if a spec calls
`givenIsInternalUser` after `visitWithTimeout` — the assertion simply exercises the default. It is a
latent source of silently-wrong tests.

### `SHOULD_MOCK_STRIPE` — set by 6 specs, and consumed by PRODUCTION code

**CORRECTED BY ORCHESTRATOR (verified against full repo at `dd9e4952a6`):** this cookie is NOT dead. It is read by production code at `apps/settings/src/pages/settingsPages/billingSettings/AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:52` and `.../AddPaymentMethodModalV2/AchFormContentV2.tsx:69`. The real finding is worse than dead config: production components branch on a test-only cookie, so the E2E suite's green path executes a code path real users never take. Commit `dd9e4952a6` (`move the Stripe.js mock out of production code`) is the team already addressing this — reinforce that work, do not open a competing ticket. See `../../methodology/VERIFIED-HISTORY.md`.


Six of seven billing specs write cookie `SHOULD_MOCK_STRIPE=true`
(`billing-settings-page.spec.ts:25` and `:58`, `billing-settings-v2.spec.ts:44`,
`billing-invoice-summary.spec.ts:50`, `billing-pricing-v2.spec.ts:174`,
`invoice-details-page.spec.ts:23`, `payment-recovery.spec.ts:34`). A recursive grep for the string
across the snapshot matches **only those spec files** — no application source reads it.

`UNVERIFIED —` whether a consumer exists outside the exported subtrees (the snapshot contains only
`apps/settings/e2e/`, `apps/settings/src/`, `apps/spo-webapp/src/`, `apps/provider-home-webapp/src/`,
`shared/core/src/`). To settle it: `grep -rn SHOULD_MOCK_STRIPE` in a full clone at `dd9e4952a6`.

Either way it is misleading: Stripe is faked unconditionally by `fixtures.ts:32`, so the cookie
cannot be what makes mocking happen, and `billing-settings-payment-element.spec.ts` — the one spec
whose entire subject is Stripe — does **not** set it and is faked all the same.

---

## Network mocking — the full picture

Three layers stack, all in-process:

```
fixtures.ts               login / gql / auth×3 / phi-ab            (every test in apps/settings/e2e)
  └─ setUpRoutes          13 billing REST + billing-monolith paths (every billing test)
       └─ per-spec routes  provider/v1/gql SKU payloads, /pay-now  (5 of 7 specs)
            └─ per-test    mockPostRoute overrides to 400/500       (5 tests)
```

### Layer 2 — `setUpRoutes` (`billing-settings-page-commands.ts:188-359`)

Full path/status table is in [`e2e-L5.md`](e2e-L5.md#shared-stub-table). Thirteen endpoints, every
one `route.fulfill`ed. Notable literal payloads:

| Stub | Value | Line |
|---|---|---|
| `POST .../setup-intents` | `{ client_secret: 'seti_mock_secret_123' }` | :337-339 |
| `POST .../payment-methods` | `{ payment_method_info: mockCreditCardInfo, error: undefined }` | :350-353 |
| `GET .../bill/*/summary` | `mockBillSummaryResponse` | :318-320 |
| `GET .../settings/billing/*` | `mockPracticeBillingSettingsViewModel` | :196-199 |
| `POST .../pay-now` | `{ succeeded_count: 1, remaining_failures: 0 }` (in `payment-recovery.spec.ts:78-93`) | spec-local |

The file states the rationale at :5-9 — the Cypress version proxied these through a `:9000` mock
server that itself produced only fixed statuses or the same mock constants, so a full stub was judged
equivalent. **That reasoning is sound about the port, and it is also the proof that the pre-migration
Cypress suite was equally backend-free.** This is not a regression introduced by the migration; it
is a pre-existing property that the migration made explicit and easy to read.

### Layer 3/4 — per-spec and per-test overrides

| Spec | Extra routes |
|---|---|
| `billing-settings-page.spec.ts:71-120` | `provider/v1/gql` → `getSkuMappings` (Selected/NotActivated + Insurance NotStarted), `getEntityFlags` `[]` |
| `billing-settings-v2.spec.ts:787-835` | same shape, SKU `Activated` |
| `billing-pricing-v2.spec.ts:23-168` | three variants: both-Activated / Marketplace-NotActivated / `skuMappings: []`; `getEntityFlags` `['IsCreatedViaRepositionFlow']` |
| `payment-recovery.spec.ts:45-93` | empty SKUs; `POST **/spo-provider/v1/management/*/pay-now` → success |
| `billing-settings-payment-element.spec.ts:82,120` | `mockPostRoute(page, '/payment-methods', 400)` |
| `billing-settings-v2.spec.ts` (via page object) | `PUT primaryBusinessAddress` / `PUT billingEmail` with explicit 200/500 |

### The `route.fallback()` discipline

Spec-local gql handlers end in `route.fallback()` rather than `route.fulfill` on the default branch
(`billing-settings-page.spec.ts:118`, `billing-pricing-v2.spec.ts:77`, `payment-recovery.spec.ts:70`),
which correctly hands unmatched operations back to the `fixtures.ts` handler. This is the right
pattern and is applied consistently.

---

## Stripe: `installStripeJsFake`

`shared/core/src/testing/installStripeJsFake.ts` (130 LOC) — installed by `fixtures.ts:32` for every
test.

| Aspect | Reality | Line |
|---|---|---|
| Loader defeat | assigns `window.Stripe` so `@stripe/stripe-js`'s loader resolves with the existing global and never injects its `<script>` — "nothing is requested from js.stripe.com and no publishable key is needed" | :1-20 (docstring) |
| Element rendering | `mount()` appends a plain `<input data-test="mock-stripe-<type>-input">`. **Not an iframe.** | :31-54 |
| `createToken` | always `{ token: { id: 'tok_fake' } }` | :~95 |
| `createPaymentMethod` | always `{ paymentMethod: { id: 'pm_fake' } }` | :~102 |
| `confirmCardPayment` | always `{ paymentIntent: { status: 'succeeded' } }` | :~108 |
| `confirmSetup` | always `{ setupIntent: { status: 'succeeded', payment_method: 'pm_fake_unified' } }` | :113-119 |
| Version reporting | constructor carries `version: 'dahlia'` | :~25 |

**No Stripe failure path is reachable in any E2E test.** No declined card, no `card_declined` error
mapping, no 3DS challenge, no ACH microdeposit handoff, no invalid-`client_secret` handling, and no
evidence that a real Element mounts. Because the fake has no dependency on Stripe at all, a Stripe.js
major-version bump, a publishable-key misconfiguration, or a CSP change that breaks card entry in
production leaves every one of these 63 tests green. Recorded as a P0 gap in
[`e2e-L5.md#candidate-gaps`](e2e-L5.md#candidate-gaps) row 2.

---

## Commands / helpers

### `billing-settings-page-commands.ts` (562 LOC)

Three groups.

**1. Setup and options.**

`SetUpRoutesArgs`: `doesBillingSettingsFetchFail`, `doesBillSummaryFetchFail`,
`doesPageHttpRequestFail`, `getPaymentMethodsWithoutRollovers`, `fromHomepage`, `customResponse`,
`enablePaymentRecovery`, `recoveryScenario`, `billSummaryResponse`.

`SetUpRoutesAndVisitBillingPageOptions` adds: `showBillingCompletionModal`,
`billingProviderRepositioning?: 'on'|'off'` (default `'on'`), `billingUpdatedCalculatorCopy`
(default `'off'`), `enableReviewAndPayCta`, `payNowEnabled?: 'on'|'off'` (default `'off'`, BILL-971).

Note `getPaymentMethodsWithoutRollovers` injects `mockAchInfo` into the payment-method list, but
**no spec sets it** — so the one path that would render an ACH row is never taken.

**2. The `waitFor*` family — the ported `cy.wait('@alias')` idiom.**

`waitForGetPracticeBillingSettings`, `waitForSetDefaultPaymentMethod`, `waitForDeletePaymentMethod`,
`waitForSetDefaultPaymentMethodForProvider`, `waitForUpdateBillingEmail`,
`waitForUpdatePrimaryBusinessAddress`, `waitForSavePaymentMethodAttributes`, `waitForBillSummary`,
`waitForSetupIntent`, `waitForPaymentMethodV2`.

Each returns a `page.waitForResponse` promise that must be **armed before** the triggering click —
Cypress's alias model allowed arming after the fact; Playwright does not. Specs follow this
correctly (e.g. `payment-recovery.spec.ts` arms `waitForPostResponse(page, '/pay-now')` before
clicking `pay-now-submit`). This is the single most important migration idiom in the suite and it is
applied consistently.

**3. UI actions.** `selectValueInDropdown`, `clickBillByDate`, `openPaymentMethodMoreMenu`,
`setMonthlyLimitInModal`, `openSeeByProviderModal`, `saveModalAndWait`, `openEditRolloversModal`,
`hideBillingCompletionModal`, `showBillingCompletionModal`.

### `helpers.ts` (860 LOC)

| Function | Behaviour | Note |
|---|---|---|
| `dataTest(sel, opts)` | builds `[data-test="…"]`, optional `*=` / `^=` / `$=` | |
| `getElem` | `scrollIntoViewIfNeeded()` then falls back to `toBeAttached()` | **the fallback weakens assertions**: an element that cannot be scrolled to still passes |
| `getElemWithoutScrollingIntoView` | no scroll — required by the BILL-1083 scroll test | `payment-recovery.spec.ts:233` |
| `visitWithTimeout` | `goto(waitUntil:'domcontentloaded')`, 10 s, then asserts `global-loading-spinner` count 0 | :614-628; the implicit per-test cost driver |
| `mockPostRoute(page, pattern, status)` | matches `**${pattern}` on POST, fulfils with `status` | |
| `waitForPostResponse(page, pattern)` | arms a POST response wait | |
| `setupNewAbExperiments(page, experiments)` | stubs `GET **/phi-ab/v1/www/experiments*` → 200 and `POST **/phi-ab/v1/assignments` → **201** | :828-860; the 201 is load-bearing — a 200 makes the client silently fall back to all-experiments-OFF |

The `setupNewAbExperiments` 201 requirement is a genuine sharp edge: an experiment override that
silently degrades to OFF would make a flag-on test assert the flag-off UI and still pass. It is
correct here, but nothing prevents regression.

---

## Page objects

Three files, 249 LOC. A Playwright-adapted Page Object pattern: methods take `page: Page`
explicitly because there is no ambient `cy`.

### `PageObject.ts` (18 LOC)
Abstract base: constructor takes `pageSelector`; `isAtPage(page)` delegates to `verifyElemVisible`.

### `BillingSettingsPagePageObject.ts` (46 LOC)
Instance `billingSettingsPagePageObject = new BillingSettingsPagePageObject('billing-settings-container')`.
Exactly one method: `verifyContactInfo(page, businessAddress, billingEmail)`. Used by
`billing-settings-v2.spec.ts` tests 8 and 11.

### `EditBillingContactInfoModalPageObject.ts` (185 LOC)
Instance selector `'edit-billing-contact-info-modal'`. Field union
`'address1'|'address2'|'city'|'state'|'zip-code'|'billing-email'`.

Methods: `getFormErrorMessage`, `getSaveButton`, `formIsInvalid` / `formIsValid` (assert save-button
disabled/enabled), `typeInField`, `selectDropdownOption`, `clearField`, `getErrorMessageForField`,
`getInputField`, `getDropdownField`, `interceptSubmitPrimaryBusinessAddress`,
`waitForSubmitPrimaryBusinessAddress`, `interceptSubmitBillingEmail`, `waitForSubmitBillingEmail`.

Two implementation details worth recording:

1. **Per-`Page` `WeakMap` for armed waits.** Two module-level `WeakMap<Page, Promise<Response>>`
   store the armed response promises keyed by `Page`, so parallel workers sharing the module-level
   singleton do not collide. This is the correct fix for the singleton-page-object-plus-parallelism
   hazard and is worth copying elsewhere.
2. **`fulfillStatus` resolves `statusCode ?? status ?? 200`** and documents that the Cypress original
   was inconsistent about which key callers passed. Defensive, but it means a typo'd key silently
   yields `200` instead of the intended `500` — a failure-path test could pass for the wrong reason.

No page object exists for: the add-payment-method modal, the Pay Now modal, the pricing tab, the
invoice summary, the rollovers modal, or the monthly-limit modal. Those five specs use raw
`data-test` strings or `selectors.ts` lookups directly, so the pattern is applied to 1 of 7 modals.

---

## Test data strategy

**Test data comes from production application source, not from `e2e/` fixtures.**

| Import | Source file | Used by |
|---|---|---|
| `mockPracticeBillingSettingsViewModel` | `apps/settings/src/server/controllers/practiceBillingSettingsPage/mocks.ts:11` | commands (default settings response), `billing-settings-page.spec.ts` (spread + null a field), `billing-settings-v2.spec.ts` (`.find()` predicates) |
| `mockCreditCardInfo` | same file, `:124` | commands `/payment-methods` stub |
| `mockDefaultCreditCardInfo` | same file, `:133` | list fixtures |
| `mockAchInfo` | same file, `:143` | `getPaymentMethodsWithoutRollovers` only — **never activated by a spec** |
| `mockBillSummaryResponse` | same file, `:398` | commands `/bill/*/summary` stub; spread into `augustBillSummaryResponse` |
| `mockBookingSourceBreakdown` | `apps/settings/src/pages/settingsPages/billingSettings/fixtures/bookingSourceBreakdownFixtures.ts` | `billing-invoice-summary.spec.ts:30-43` |
| `getMockRecoveryResponse(n)`, `getMockRecoveryBalanceDetailResponse(n)` | billing recovery mocks under `src/` | commands `:222-244` |
| `PracticeBillingSettingsViewModelType` | `src/` types | spec type annotations |

Three consequences:

1. **Coupling.** A developer editing `src/server/controllers/practiceBillingSettingsPage/mocks.ts`
   for a local-dev reason changes what 63 E2E tests assert against, with no signal that they did.
2. **Vacuous-pass risk.** `billing-settings-v2.spec.ts` derives its subjects by predicate
   (`paymentMethods.find(pm => !pm.isDefault)`) and then wraps every assertion in `if (found)`
   (:191, :241, :288, :349, :425, :759). A mock edit that breaks the predicate turns six tests into
   no-ops that still report green.
3. **Duplicated expectations.** Amounts are also hard-coded in specs (`$8,570.00`
   `billing-invoice-summary.spec.ts:135`; `$3,132.00` / `56` / `48` in `invoice-details-page.spec.ts`;
   `'327'` in `billing-settings-v2.spec.ts:~980`; `$50.00` / `$30.00` at :313, :320), so a fixture
   change breaks the spec at an assertion rather than at the data.

The same `mocks.ts` constants are also imported by the L2 suites, which is why several L5 assertions
are byte-identical to L2 ones — it makes the redundancy in
[`../../shift-left/E2E-TEST-BY-TEST.md`](../../shift-left/E2E-TEST-BY-TEST.md)
easy to establish, since both levels assert the same numbers from the same source.

There is **no** database seeding, no API-driven setup, no test-account provisioning, and no cleanup —
because there is no shared state to clean. (Contrast `sandbox`, which drives production, shares one
real practice across billing specs, and must run `--workers=1`.)

---

## Tests that mock their whole backend

Per the taxonomy: *"A browser test that mocks its entire backend is not really an L5. It pays L5 cost
for L2 confidence. These are the highest-value shift-left targets and are flagged individually."*

**All 63 billing E2E tests qualify.** Flagging each individually would reproduce the full test list,
so the flag is recorded structurally — the mechanism is suite-wide and unconditional, not per-test:

| Layer | Applies to | Cannot be opted out of |
|---|---|---|
| `fixtures.ts:32` Stripe fake | all 63 | correct — no spec can restore real Stripe |
| `fixtures.ts:34-113` auth/login/gql stubs | all 63 | correct |
| `setUpRoutes` 13-endpoint table | all 63 (every spec calls `setUpRoutesAndVisitBillingPage`) | correct |

Per-spec confirmation that no real backend call survives:

| Spec | Tests | Real backend calls | Only-in-a-browser justification |
|---|---|---|---|
| `billing-settings-page.spec.ts` | 7 | 0 | none — error page + null-field renders are pure L2 |
| `billing-settings-v2.spec.ts` | 16 | 0 | none — every behaviour has a named L2 counterpart |
| `billing-settings-payment-element.spec.ts` | 4 | 0 | none — Stripe itself is faked; retry semantics are L1-covered |
| `billing-invoice-summary.spec.ts` | 20 | 0 | 1 (test 20, `boundingBox()` y-ordering — jsdom has no layout) |
| `billing-pricing-v2.spec.ts` | 11 | 0 | none |
| `invoice-details-page.spec.ts` | 1 | 0 | none |
| `payment-recovery.spec.ts` | 4 | 0 | 1 (test 3, BILL-1083 `scrollTop` — self-documented as browser-only at :221-232) |

**Only 2 of 63 tests assert something a browser is strictly required for** (real layout: element
y-ordering and modal scroll position). The remaining 61 assert text content, element presence, form
validation, and request sequencing — all reproducible in jsdom, and in most cases already reproduced
there. Per-test verdicts are in
[`../../shift-left/E2E-TEST-BY-TEST.md`](../../shift-left/E2E-TEST-BY-TEST.md).

`payment-recovery.spec.ts` is the one spec that reasons about this explicitly: its header (:23-30)
states that decline and HTTP-error branches deliberately live in the `PayNowModal` +
`usePaymentRecoveryFlow` RTL suites, and :221-232 justifies its single layout test. **That docstring
is the model the other six specs should follow.**

---

## Structural issues in the infrastructure

| # | Issue | Evidence | Impact |
|---|---|---|---|
| 1 | `getElem`'s `toBeAttached()` fallback | `helpers.ts` `getElem` | an element present but unreachable (zero-size, behind an overlay, `display:none` ancestor) passes a "verify visible" call |
| 2 | `fulfillStatus`'s `?? 200` default | `EditBillingContactInfoModalPageObject.ts` | a mistyped option key silently turns a failure-path test into a happy-path test |
| 3 | Unreachable `phi-ab/assignments` handler | `fixtures.ts:107` vs `helpers.ts:828-860` | misleading — reader cannot tell AB assignments are stubbed |
| 4 | `SHOULD_MOCK_STRIPE` cookie with no located consumer | 6 specs; no `src/` match | implies conditional Stripe mocking that does not exist |
| 5 | Page Object pattern applied to 1 of 7 modals | only `EditBillingContactInfoModal` | inconsistent; the other six specs hard-code `data-test` strings |
| 6 | Production `src/` mocks used as E2E fixtures | `mocks.ts` imports in all specs | an unrelated local-dev edit silently changes 63 E2E assertions |
| 7 | Cookie-bootstrap ordering is unenforced | `helpers.ts` `given*` family | a `given*` call placed after navigation silently no-ops |
| 8 | `billing-pricing-v2.spec.ts` double-navigates | :79-80 | 22 page loads for 11 tests; ~2× the necessary runtime for that file |
| 9 | `selectors.ts` is shared with non-billing specs | 200 LOC, also used by staff-page specs | a billing selector rename risks unrelated spec breakage |

---

## Candidate Gaps — infrastructure

Coverage gaps in the billing journeys themselves are in
[`e2e-L5.md#candidate-gaps`](e2e-L5.md#candidate-gaps) (9 rows). These are infrastructure-level.

| # | Missing / wrong | Correct level | File(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| I1 | **No E2E runs against a real backend at any level.** There is no smoke tier: not one test proves the billing page can load real settings, render a real bill, or persist a real payment method. The 13-endpoint stub table means a breaking change to any billing API contract (renamed field, changed enum, new required property) ships with all 63 tests green. | L4 api (contract tests against the real endpoints) **plus** a 2–3 test L5 smoke tier against a deployed environment | new: `apps/settings/e2e/` smoke spec; contract subjects `apps/settings/src/server/controllers/practiceBillingSettingsPage/` | This is the load-bearing risk of the whole suite. Every existing test asserts the frontend agrees with a fixture that the frontend team wrote. Nothing asserts the frontend agrees with the backend. A field rename in the billing monolith is undetectable until production. Money-critical. | 2d (split: 1d contract, 1d smoke) | **P0** |
| I2 | **Stripe is faked with no real-integration test anywhere.** `fixtures.ts:32` is unconditional; `installStripeJsFake.ts:113-119` makes `confirmSetup` always succeed. No test can exercise a decline, 3DS, or a real Element mount. | L5 e2e against Stripe test mode | `apps/settings/e2e/fixtures.ts:32`; `shared/core/src/testing/installStripeJsFake.ts`; subject `shared/core/src/billing/getBillingStripePromise.ts` | Duplicate of `e2e-L5.md` gap 2, restated here because the cause is infrastructural: the fake is installed by the shared fixture, so no spec can opt out even if someone wanted to. Fixing this requires a fixture change, not a spec change. | 1d | **P0** |
| I3 | **Six tests can pass while asserting nothing** because assertions sit inside `if (mock.find(...))`. | fix existing L5 | `billing-settings-v2.spec.ts:191, 241, 288, 349, 425, 759` | Six of sixteen payment-method tests are one fixture edit away from being no-ops that report green, in a suite whose subject is how a practice is charged. Add `expect(found).toBeDefined()` before each block. | 1h | **P1** |
| I4 | **E2E specs import production `src/` mocks as fixtures.** No boundary, no ownership signal, no test that guards the mock's shape. | restructure | `apps/settings/src/server/controllers/practiceBillingSettingsPage/mocks.ts` → new `apps/settings/e2e/fixtures/billing/` | An engineer editing a local-dev mock cannot know they are changing 63 E2E assertions; the file gives no indication it is test infrastructure. Move (or re-export behind an `e2e/fixtures` module) so the coupling is explicit. | 4h | P2 |
| I5 | **`getElem` silently downgrades visibility to attachment.** | fix helper | `helpers.ts` `getElem` | Assertions across the whole suite are weaker than they read. An invoice total hidden behind a modal, or a CTA rendered at zero height, passes. Split into `getVisibleElem` (strict) and keep the lenient variant opt-in. | 3h | P2 |
| I6 | **`fulfillStatus`'s `?? 200` masks mistyped failure-path options.** | fix helper | `EditBillingContactInfoModalPageObject.ts` | The two error-path tests (`billing-settings-v2.spec.ts:659`, `:704`) depend on a 500 arriving. If the option key is ever mistyped the tests assert the success path and still pass. Require the status explicitly. | 1h | P2 |
| I7 | **No spec exercises `getPaymentMethodsWithoutRollovers`**, the only option that puts `mockAchInfo` into the payment-method list. | add L5 or delete option | `billing-settings-page-commands.ts:203-208`; `mocks.ts:143` | Either dead support code (delete it) or the missing ACH-row coverage from `e2e-L5.md` gap 1 (use it). Decision rule: if ACH rows must render distinctly from cards, write the test; if not, delete the option and `mockAchInfo`'s E2E path. | 2h | P2 |
| I8 | **Unreachable `fixtures.ts:107` route handler** and an **unlocated `SHOULD_MOCK_STRIPE` cookie** set by 6 specs. | investigate / cleanup | `fixtures.ts:107`; the 6 spec sites listed above | Both make the suite read as if it does something it does not (pass through AB assignments; conditionally mock Stripe). Decision rule: confirm no consumer in a full clone, then delete both. | 1h | P3 |
| I9 | **`billing-pricing-v2.spec.ts` loads the page twice per test.** | fix existing L5 | `billing-pricing-v2.spec.ts:79-80` | 11 wasted page loads (~1–2 min of CI per run, estimate). Navigate straight to `#pricing` in one `goto` instead of visiting the billing page and then re-navigating. | 1h | P3 |
