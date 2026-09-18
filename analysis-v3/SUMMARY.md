# Billing Test Analysis — v3

**Date:** 2026-09-04
**Scope:** pre-release automated tests in the three team-owned repos — `provider-fe-monorepo`
(Settings billing), `provider-billing` (.NET service), `zocdoc_web` (monolith billing). The QA-owned
`sandbox` repo is **not** in scope.
**Prior analysis:** v1 (2026-04-14), v2 (2026-04-23)
**Drift since v2:** ~4.5 months. `provider-fe-monorepo` moved 550 commits; Cypress was removed
monorepo-wide and the billing specs were rewritten in Playwright.
**Jira:** epic [BILL-746](https://zocdoc.atlassian.net/browse/BILL-746) holds **24** issues — the 21
from this analysis plus 3 that pre-date it.

This is a prioritized list of missing test coverage. Every item names the file, says what kind of
test exists today (if any), and says what to write.

---

## Where to go

| If you want to… | Read |
|---|---|
| Work the tickets | [`gaps/BACKLOG.md`](gaps/BACKLOG.md) — same items with Jira keys and sequencing |
| Read one gap in full | `gaps/tickets/FE-0NN-*.md` (13 frontend tickets) |
| Check my work before trusting it | [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md) |
| See what the team already fixed | [`ALREADY-FIXED.md`](ALREADY-FIXED.md) |
| Know what v2 got wrong | [`V2-VALIDATION.md`](V2-VALIDATION.md) |
| See which of the 63 browser tests goes where | [`shift-left/E2E-TEST-BY-TEST.md`](shift-left/E2E-TEST-BY-TEST.md) |

**Epic contents.** 20 coverage items from v3 (BILL-1193–1205, 1211, 1212, 1214, 1217–1220), 1 hygiene
item from v3 (BILL-1216 — item 21), and 3 that pre-date v3 and were filed by QA: BILL-747 *(open,
overlaps item 10)*, BILL-748 and BILL-962 *(both closed — the revenue-calculator work credited
below)*. Three more v3 tickets were filed and then **deleted as out of scope** — BILL-1206,
BILL-1213, BILL-1215; their findings are preserved under "Dropped from scope" in
[`gaps/BACKLOG.md`](gaps/BACKLOG.md).

**Already moving:** item 3 ([BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195)) and item 6
([BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197)) are **In Progress**. Check with the
assignees before starting either.

---

## The big picture

**Two facts drive almost every item below.**

1. **Nothing checks that the billing API and the billing page agree on the data.** There are no API
   contract tests at all. A backend field rename passes all 856 other frontend tests and breaks the
   billing page in front of providers.
2. **All 63 browser tests fake the backend.** A fake Stripe.js is installed for the whole E2E
   directory (`apps/settings/e2e/fixtures.ts:32`) and all 13 endpoints are stubbed. They pay a
   browser boot (5–120s each, on **one** CI worker) to prove what a component test proves.

**What exists today — `provider-fe-monorepo` billing:**

| Kind of test | Files | Tests |
|---|---|---|
| Unit tests (one function on its own) | 34 | 224 |
| Component tests (one screen on its own) | 45 | 515 |
| Hook tests (a component test for a hook) | 9 | 47 |
| Integration tests (a few pieces wired together) | 2 | 70 |
| **API contract tests** (the API returns what the page expects) | **0** | **0** |
| Browser tests (Playwright, a real browser clicking through) | 7 | 63 |

| | Count |
|---|---|
| Billing source files | 152 |
| …with some coverage | 88 |
| …with **no coverage at all** | **13** |
| REST endpoints consumed by the UI | 13 |
| …with a contract test | **0** |
| Browser tests that mock their entire backend | **63 of 63** |
| Browser tests kept alive only for pixel measurements | 3 |

`provider-billing`: 5 test projects, ~70 integration tests (**may not execute — see limitations**).
`zocdoc_web`: billing Selenium + unit tests; 15 test files opted out of the coverage gate.

A unit or component test is preferable to a browser test whenever it catches the same bug: faster,
runs on every PR, easier to debug.

## What's working well

- **The money test that matters is done right.** `YearlyValueCalcModalV2-tests.tsx:224` hardcodes
  `$327` with the arithmetic worked out by hand in the comment. Change the formula, the test fails.
  That is the pattern the rest of the backlog should copy.
- **V2 Mezzanine components have good component tests** — modals, hooks, and sections are all
  covered, and they run in milliseconds.
- **Test count grew substantially** since v2: 365 → 856 unit + component tests.
- **The team deletes dead code with its tests**, not tests alone (`b5cc093d71`, −505 lines).
- **`provider-billing` has a real integration layer** — tests against LocalStack, which is the right
  level for a queue-driven service.

---

# Test Coverage Gaps — Billing (2026-09-04)

Twenty coverage findings, numbered continuously across the priority sections, plus one hygiene item
(21) that is not coverage work.

---

## P0 — Critical (money or provider-facing data, with no test)

### 1. Real Stripe card entry — untested at every level

**File:** `apps/settings/e2e/fixtures.ts:32` (the fake), `AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:52`

**What it does:** The Payment Element is how a practice adds a credit card. Since
`70a384854e` (2026-09-02) tore down `billing_payment_element_flow`, it is the **only** path — there
is no fallback if it breaks.

**Current testing:** None that uses real Stripe. `fixtures.ts:32` installs a fake Stripe.js
unconditionally for the whole E2E directory, all 13 endpoints are stubbed, and `/login/*` is
deliberately 500'd. Component tests render in jsdom, where a Stripe iframe cannot mount. Production
code even branches on a test-only cookie, `SHOULD_MOCK_STRIPE`, at
`CreditCardFormContentV2.tsx:52` and `AchFormContentV2.tsx:69`.

**Why it matters:** A Stripe.js version bump, a bad publishable key, or a CSP change breaks card
entry in production **with all 63 browser tests green**. This is the revenue path, and nothing
anywhere proves a real Payment Element mounts, accepts a card, or handles a decline.

**Test plan:** Create `apps/settings/e2e/PracticeSettingsPages/billing-payment-element-real.spec.ts`
— a browser test that opts out of the fake.
- Card `4242 4242 4242 4242` → the payment method saves
- Declined card `4000 0000 0000 0002` → the error is shown to the user
- Empty Element → submit is blocked
- Note: `a633542cab` (#11400) already points test practices at a Stripe sandbox, so the plumbing exists

**Effort:** 1 day
**Risk if not fixed:** High (silent breakage of the only card-entry path)
· [FE-001](gaps/tickets/FE-001-real-stripe-payment-element-untested.md) · [BILL-1193](https://zocdoc.atlassian.net/browse/BILL-1193)

---

### 2. EditMonthlyLimitModalV2-tests.tsx — the monthly-limit test cannot fail

**File:** `__tests__/EditMonthlyLimitModalV2-tests.tsx:129-133`, `utils/schemaBuilder.ts:101`

**Current testing:** A component test exists, but it computes its own expected value with the same
expression the source under test uses:

```ts
const minimumMonthlyLimit = parseInt(
    getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500',
);
```

If the source default were wrong, the test computes the same wrong value and passes. The upper bound,
`maximumMonthlyLimit = 500000` (`utils/schemaBuilder.ts:101`), is asserted **nowhere**.
`schemaBuilder.ts` holds 5 yup schemas and has **no unit test file at all**.

**Why it matters:** This is the validation that stops a practice from setting a payment limit that is
too low to cover their bills, or absurdly high. The test that supposedly guards it cannot fail.

**Test plan:** Create `utils/__tests__/schemaBuilder-tests.ts` with **hardcoded** boundaries:
- 499 → invalid; 500 → valid
- Flag set to `'750'`: 600 → invalid; 750 → valid
- 500000 → valid; 500001 → invalid
- 0, negative, and non-numeric → invalid
- Sanity check: change the source default 500 → 400 and confirm the new tests fail

Contrast `YearlyValueCalcModalV2-tests.tsx:206-225`, which asserts a hand-computed `'$327'` — that is
the pattern to copy.

**Effort:** 45 minutes
**Risk if not fixed:** Medium (a wrong limit is accepted or a valid one rejected, silently)
· [FE-002](gaps/tickets/FE-002-monthly-limit-tautological-test.md) · [BILL-1194](https://zocdoc.atlassian.net/browse/BILL-1194)

---

### 3. invoiceHelpers.ts — 3 exported functions, zero tests

**File:** `apps/settings/src/pages/settingsPages/billingSettings/invoiceHelpers.ts`

| Function | What It Does | Usage |
|---|---|---|
| `formatDate` | Converts YYYY-MM-DD to "Mon DD, YYYY" | FpbInvoiceView, v2/FpbInvoiceView |
| `getLastDayOfMonth` | Returns the last day of a given month | InvoiceDetailsContainer |
| `capitalizeStatus` | Normalizes bill status strings | FpbInvoiceView |

**Current testing:** **No test file exists.** Not a unit test, not a component test. Raised as v2's
P0 #2 in April and re-verified still untested in September.

**Why it matters:** Date-formatting bugs show providers the wrong invoice dates. These are pure
functions — trivial to test, and used by both invoice views.

**Test plan:**
- `formatDate`: known inputs → expected outputs (e.g. `"2026-04-23"` → `"Apr 23, 2026"`); null/undefined input
- `getLastDayOfMonth`: each month, plus a leap-year February
- `capitalizeStatus`: status normalization (e.g. `"pending"` → `"Pending"`), plus an unexpected value

**Effort:** 45 minutes
**Risk if not fixed:** Medium (formatting bugs are subtle but provider-visible)
· [FE-003](gaps/tickets/FE-003-invoice-helpers-untested.md) · [BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195) — **In Progress**

---

### 4. StripeWebhookHandler.cs — idempotency is bypassed in production and all four tests are commented out

**File:** `src/ProviderBilling.Lambda/StripeWebhookHandler.cs` · repo `provider-billing`

**What it does:** Receives Stripe webhook events via SQS. SQS delivery is at-least-once, and Stripe
events can additionally be replayed from the Stripe Dashboard — one click, available to support. The
`IWebhookEventDeduplicator` exists specifically to make repeat delivery safe.

**Current testing:** The deduplicator is injected but **never called** — the `ExistsAsync` check
(`:55`) and the `MarkAsDoneAsync` write (`:57`) are commented out, and `#pragma warning disable
CS9113` (`:25`) silences the compiler telling you the dependency is unused. A comment at `:60` says
outright: *"While this is bypassed the lambda is NOT idempotent."* And in
`tests/UnitTests/StripeWebhookHandlerTests.cs` the mock is still constructed, but **every assertion
on it is inside a comment block** (`:102`, `:109`, `:112`, `:131`, `:135`).

**Why it matters:** A redelivered `charge.succeeded` processed twice can double-apply a payment to a
provider. The production code says in its own comment that it isn't idempotent, and the test suite is
green. That combination is the worst case: the risk is known, written down, and invisible to CI.

**Test plan:**
- Restore the four commented-out tests; confirm the test **count** goes up, not just that it's green
- Same event ID delivered twice → exactly one state change
- Successful event → `MarkAsDoneAsync` called once
- Failed event → `MarkAsDoneAsync` **not** called, so it stays retryable
- Restore the call sites and delete the `#pragma` and the "NOT idempotent" comment
- Find out *why* it was commented out before restoring — if the original blocker still applies, that blocker becomes the ticket

**Effort:** 1 day
**Risk if not fixed:** High (double-charging a provider)
· [BILL-1211](https://zocdoc.atlassian.net/browse/BILL-1211)

---

### 5. Prorated subscription day-count — untested, and the source comment says the math is wrong

**File:** `zocdoc_web` monolith, subscription proration

**Current testing:** No unit test pins the behaviour either way.

**Why it matters:** The source carries a comment flagging the calculation as incorrect. So either the
math is wrong and providers are billed the wrong prorated amount, or the comment is stale and
misleading — and no test tells you which.

**Test plan:**
- Hardcoded expected amounts for a mid-month start, a mid-month cancel, and a full month
- Month-length edge cases (28/29/30/31 days)
- Resolve the comment: fix the math and test the fix, or delete the comment and pin current behaviour

**Effort:** 4 hours
**Risk if not fixed:** High (wrong money on a provider invoice)
· [BILL-1217](https://zocdoc.atlassian.net/browse/BILL-1217)

---

## P1 — High Priority (real user-visible failure, or material CI cost)

### 6. Zero API contract tests across 13 billing endpoints

**File:** new directory `__contracts__/` · repo `provider-fe-monorepo`

**Current testing:** **None — not thin, zero.** Verified across 90 non-E2E billing test files: no
MSW, no `nock`, nothing that checks a real response shape. Every test mocks what the frontend
*believes* each endpoint returns, and nobody checks that belief against the API.

**Why it matters:** A backend field rename passes all 856 frontend tests and breaks the billing page
in front of providers. This is the single largest structural hole in the analysis.

**Test plan:** Create `__contracts__/` covering, at minimum:
- Payment methods list
- Add payment method
- Monthly limit update
- Invoice list
- Invoice detail
- Acceptance check: rename a required field in the contract fixture → the suite must fail

**Effort:** 1 day
**Risk if not fixed:** High (provider-facing breakage from a routine backend change)
· [FE-005](gaps/tickets/FE-005-zero-api-contract-tests.md) · [BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197) — **In Progress**

---

### 7. billing-settings-v2.spec.ts — six browser tests are one fixture change away from testing nothing

**File:** `apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts` at
`:191`, `:241`, `:288`, `:349`, `:425`, `:759`

**Current testing:** Six browser tests exist and pass. Every assertion in them sits inside
`if (mock.find(...))`. If the fixture stops matching, the `if` is false, the test asserts nothing,
and it still reports green.

**Why it matters:** Fix this **before trusting any other browser-test result**, including the shift
and delete decisions in items 11–13. Right now six of the 63 are green no-ops.

**Test plan:**
- Add `expect(found).toBeDefined()` before each conditional, or delete the test outright where a component test already covers it
- Sabotage check: rename the fixture key and confirm each of the six fails

**Effort:** 2 hours
**Risk if not fixed:** Medium (false confidence, and it corrupts the E2E-reduction decisions)
· [FE-004](gaps/tickets/FE-004-conditional-assertions-green-noops.md) · [BILL-1196](https://zocdoc.atlassian.net/browse/BILL-1196)

---

### 8. ACH / bank-account payment — no coverage at any level

**File:** `AddPaymentMethodModalV2/AchFormContentV2.tsx:69`, target spec
`billing-settings-payment-element.spec.ts`

**What it does:** Lets a practice pay by bank account instead of card, including a Financial
Connections OAuth handoff to their bank.

**Current testing:** `mockAchInfo` exists in the E2E fixtures, but **no spec ever selects the option
that renders it**, so the fixture is dead. `AchFormContentV2.tsx:69` reads the `SHOULD_MOCK_STRIPE`
cookie. The Financial Connections OAuth flow is untested at every level.

**Why it matters:** ACH is a live payment method. A break here means a practice cannot pay, and
nothing in CI would say so.

**Test plan:**
- Select the bank-account option → the ACH form renders (works against the existing mocks)
- Submit valid bank details → the payment method saves
- Validation errors on bad details
- OAuth handoff to the bank, and the return leg — these two need item 1 first

**Effort:** 4 hours
**Risk if not fixed:** Medium-High (a whole payment method unexercised)
· [FE-006](gaps/tickets/FE-006-ach-no-e2e-coverage.md) · [BILL-1198](https://zocdoc.atlassian.net/browse/BILL-1198)

---

### 9. ProcessorGenerateChargeGroupsTest — tax amounts asserted tautologically

**File:** `ProcessorGenerateChargeGroupsTest` · repo `zocdoc_web`

**Current testing:** A unit test exists, and it computes the expected tax with the same expression as
the source. Same cannot-fail pattern as item 2, applied to tax.

**Why it matters:** Tax on a provider charge. If the calculation is wrong, the test is wrong in the
same direction and stays green.

**Test plan:**
- Replace the computed expectation with hardcoded amounts for two or three known rate/subtotal pairs
- Include a zero-tax case and a rounding case (half-cent)
- Sanity check: perturb the source rate and confirm the tests fail

**Effort:** 2 hours
**Risk if not fixed:** Medium-High (wrong tax on a provider charge, undetected)
· [BILL-1218](https://zocdoc.atlassian.net/browse/BILL-1218)

---

### 10. Bill generator — its only test fixture is `[Ignore]`d, so it has no active tests

**File:** bill generator + its `[Ignore]`d fixture · repo `zocdoc_web`

**Current testing:** A test fixture exists and is annotated `[Ignore]`. Nothing runs. The class that
produces bills is entirely unexercised.

**Why it matters:** This is the code that generates what providers are billed. Note that
**BILL-747** ("Make monolith invoice generation testable and add integration tests") is an open QA
ticket covering the same ground — reconcile with it rather than duplicating it.

**Test plan:**
- Establish why it is ignored (usually a missing harness or a slow dependency); that answer scopes the rest
- Re-enable with integration coverage: seeded inputs → hardcoded expected bill lines
- At least one case per bill line type, plus a zero-line case

**Effort:** 1 day
**Risk if not fixed:** High (the bill-producing path has no active test)
· [BILL-1219](https://zocdoc.atlassian.net/browse/BILL-1219)

---

## P2 — Medium (meaningful gap, low blast radius)

### 11. 19 browser tests that should be component tests

**File:** `billing-settings-v2.spec.ts`, `billing-invoice-summary.spec.ts`, `billing-pricing-v2.spec.ts`,
`billing-settings-page.spec.ts`, `invoice-details-page.spec.ts`

**Current testing:** Browser tests that mock every dependency — so they are paying a 5–120s browser
boot for what a millisecond component test proves. Full per-test classification is in
[`shift-left/E2E-TEST-BY-TEST.md`](shift-left/E2E-TEST-BY-TEST.md).

**Why it matters:** ~100× slower for the same confidence, on a **single** CI worker
(`playwright.config.ts:14`, `workers: isCI ? 1 : undefined`).

**Test plan:** Four batches, and in each one the new component test lands **before** the browser test
is removed:
- A: `billing-settings-v2.spec.ts` → `PaymentMethodsList` / `PaymentMethodV2`
- B: `billing-invoice-summary.spec.ts` → invoice summary components
- C: `billing-pricing-v2.spec.ts` → `PricingInformationV2` / `PricingTab`
- D: `billing-settings-page.spec.ts` + `invoice-details-page.spec.ts` → the containers

**Effort:** 1 day
**Risk if not fixed:** Low (cost, not correctness)
· [FE-009](gaps/tickets/FE-009-shift-19-e2e-tests-to-component-level.md) · [BILL-1201](https://zocdoc.atlassian.net/browse/BILL-1201)

---

### 12. 39 browser tests that duplicate a named component test

**File:** the five billing specs · repo `provider-fe-monorepo`

**Current testing:** Each of the 39 has a **named** component test covering the same behaviour —
citations spot-checked, e.g. `it('calls setDefaultPaymentMethod API on "Set as default" click')` at
`PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-tests.tsx:605`, and
`it('opens EditMonthlyLimitModal on "Set limit" click')` in the same file at `:801`.

**Why it matters:** Pure duplication. But **do this last** — see the sequencing note below. Deleting
these before item 1 exists leaves billing with essentially one test that exercises a multi-page
journey.

**Test plan:**
- Split into 4 PRs, one per spec, so a mistake is easy to revert
- For each deletion, the covering component test is named in the PR description
- Run the full suite after each PR

**Effort:** 1 day
**Risk if not fixed:** Low (cost, not correctness)
· [FE-010](gaps/tickets/FE-010-delete-39-redundant-e2e-tests.md) · [BILL-1202](https://zocdoc.atlassian.net/browse/BILL-1202)

---

### 13. billing-settings-v2.spec.ts:175 — one empty browser test, plus four duplicates

**File:** `apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts:175-179`

**Current testing:** The test at `:175` has a **verified empty body** — one
`setUpRoutesAndVisitBillingPage(page, practiceId, {})` call and no assertions at all. Its title is
copy-pasted from the test at `:56`. Four more tests duplicate others inside the same suite (4 of 63,
6.3%).

**Why it matters:** Zero coverage risk to delete, and it removes 5 tests from a serial suite. This is
the free win.

**Test plan:**
- Delete `:175-179`
- Delete the four intra-suite duplicates, naming the surviving test for each
- Confirm the suite count drops by exactly 5

**Effort:** 45 minutes
**Risk if not fixed:** Low
· [FE-007](gaps/tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) · [BILL-1199](https://zocdoc.atlassian.net/browse/BILL-1199)

---

### 14. Three pixel assertions keep browser tests alive purely for layout

**File:** `billing-invoice-summary.spec.ts:297`, `payment-recovery.spec.ts:156`, `payment-recovery.spec.ts:233`

| Assertion | What it checks |
|---|---|
| `boundingBox()` y-coordinates | Invoice row ordering |
| `overflow === 0`, `height === 68` | Payment-recovery banner does not clip |
| `scrollTop === 0` | Page opens at the top (BILL-1083) |

**Current testing:** Functional browser tests that assert geometry. The `height === 68` traces to
`ad433d2bee` (#11628, BILL-1097) — **a real design fix**, so the assertion is protecting something.

**Why it matters:** 3 of the 5 tests marked `keep-e2e` are kept only for geometry. That hides the
real question of what actually needs a browser. **Do not delete these** — relocate them.

**Test plan:**
- Move the three assertions to visual-regression coverage
- Leave the functional assertions in the browser suite
- Re-mark the `keep-e2e` set afterwards, so it reflects tests kept for behaviour rather than pixels

**Effort:** 4 hours
**Risk if not fixed:** Low (but it distorts every other E2E decision)
· [FE-008](gaps/tickets/FE-008-move-geometry-assertions-to-visual-regression.md) · [BILL-1200](https://zocdoc.atlassian.net/browse/BILL-1200)

---

### 15. LegacyInvoiceView — thin coverage on a path that is now unconditional

**File:** `LegacyInvoiceView.tsx` (~10KB), imported at `InvoiceDetailsContainer.tsx:16`, rendered at `:201`

**What it does:** Renders every non-FPB invoice. Removing the
`SHOW_NEW_INVOICE_DETAILS_PAGE` flag did not delete this branch — it made it **permanent**.

**Current testing:** A component test file exists and is thin relative to a path that now always
renders.

**Why it matters:** **Do not delete this file.** v2's #1 P0 said to, blaming commit `a88b14cba6` —
that commit changed 6 files (+8/−44) and touched neither `LegacyInvoiceView*` nor
`InvoiceDetailsContainer.tsx`. Executing v2's recommendation breaks invoice rendering for providers.

**Test plan:**
- Assess the existing component test against what now always renders
- Add cases for the invoice states that reach this view in production
- Record in the ticket that the file is live, so the v2 recommendation isn't re-derived later

**Effort:** 2 hours
**Risk if not fixed:** Medium (a permanent render path with thin coverage)
· [FE-012](gaps/tickets/FE-012-legacy-invoice-view-coverage.md) · [BILL-1204](https://zocdoc.atlassian.net/browse/BILL-1204)

---

### 16. BILLING_PAGE_ENABLE_IFRAME_DEPRECATION — ramp state unknown, test branches still present

**File:** `apps/settings/src/ab/` (outside the snapshot that was analysed)

**Current testing:** Component tests still carry branches for both sides of the flag. Whether either
branch is dead cannot be determined from code — the ramp state is a runtime value.

**Why it matters:** Raised as v2's callout #5 and unverified for 3 months. Also note the v2 failure
mode from item 15: **removing a flag can make a branch permanent rather than dead**, so read the ramp
before deleting anything.

**Test plan:** Determine the ramp state, then apply one of:
- Fully ramped on → delete the off-branch tests and the off-branch code
- Fully ramped off → the feature is unshipped; decide whether to keep it at all
- Partially ramped → both branches are live; keep both sets of tests and record the ramp in the ticket

**Effort:** 2 hours
**Risk if not fixed:** Low
· [FE-011](gaps/tickets/FE-011-investigate-iframe-deprecation-flag.md) · [BILL-1203](https://zocdoc.atlassian.net/browse/BILL-1203)

---

### 17. Handler.cs:251 — `ActualCost = 0` is hardcoded with nothing asserting it

**File:** `src/ProviderBilling.AppointmentEventProcessorLambda/Handler.cs:251` · repo `provider-billing`

**What it does:** Persists the billing projection of each appointment. `ActualCost` is the field that
would carry what the appointment costs the provider. It is written as a literal `0`, unconditionally,
in a 352-line handler.

**Current testing:** No test asserts this value — not that it is `0` deliberately, nor what it should
be otherwise.

**Why it matters:** Almost every other monetary field in this service is a pass-through
(`StripeEventProcessor.cs:85` does `AmountCents = charge.Amount`). This is the one place a monetary
field is *originated*. Either `0` is a deliberate placeholder — in which case it's undocumented and a
future author may "fix" it into something wrong — or it's an unfinished stub and every appointment is
persisted with no cost attribution.

**Test plan:**
- Determine who consumes `ActualCost` from this service, and whether any consumer needs it non-zero. **This answer is the deliverable.**
- If `0` is correct: assert `ActualCost == 0` with a comment naming the system that owns the real value
- If it's an unfinished stub and the real value is available here: compute it and test against hardcoded amounts
- If the real value isn't available here: document that, assert `0` meanwhile, open a follow-up for whoever owns the missing input

**Effort:** 2 hours
**Risk if not fixed:** Medium (an originated money value guarded by nothing)
· [BILL-1212](https://zocdoc.atlassian.net/browse/BILL-1212)

---

### 18. Billing-export Generate stage — no integration test, while Gather and Enrich have one

**File:** `src/ProviderBilling.BillingExportCron/BillingExportGenerateService.cs` (181 lines) · repo `provider-billing`

**What it does:** The terminal stage of the billing-export cron. Composes rows via `CsvRowMapper`,
writes the file via `CsvFileWriter`, and uploads to S3 (`:38`, `:43` fail fast when
`BillingExport__S3Bucket` is unset). This is the file providers actually receive.

**Current testing:** `tests/IntegrationTests/BillingExportTests/` has
`BillingExportGatherIntegrationTests.cs` and `BillingExportEnrichIntegrationTests.cs` — but **no**
`BillingExportGenerateIntegrationTests.cs`. Generate's only coverage is a unit test
(`BillingExportGenerateServiceTests.cs`) that mocks its dependencies. The pieces it wires together
*are* well unit-tested (`CsvRowMapperTests.cs` covers the PII-obfuscation paths) — leave those alone.

**Why it matters:** The two stages that only read and transform data have integration coverage. The
one stage that produces the provider-facing artifact and pushes it to S3 does not. A misconfigured
bucket, a permissions change, or a path/naming regression is caught by nothing above the mocked level
— and the failure gets noticed by the recipient rather than by us.

**Test plan:** Create `BillingExportGenerateIntegrationTests.cs`, reusing the existing
`BillingExportTestHostBuilder` and `DbHelper` (do not build a second harness):
- Seeded appointments, non-obfuscated → CSV content matches a hardcoded header + rows
- Seeded appointments, obfuscated → patient names masked **in the produced file**, not just in the mapper's own test
- Zero matching appointments → whichever behaviour is intended (empty file with header, or no file), asserted
- S3 upload attempted with the expected bucket and key
- `BillingExport__S3Bucket` unset → the explicit failure at `:43`, with no partial upload

**Effort:** 4 hours
**Risk if not fixed:** Medium-High (a wrong, empty, or missing provider-facing export)
· [BILL-1214](https://zocdoc.atlassian.net/browse/BILL-1214)

---

## P3 — Low (polish)

### 19. 13 billing source files with no coverage at all

**File:** enumerated in [`inventory/provider-fe-monorepo/source-components.md`](inventory/provider-fe-monorepo/source-components.md)

**Current testing:** Of 152 billing source files, 88 have some coverage and 64 have no *direct* test;
of those, **13 have no coverage at all** — not directly, not indirectly through another component's
test. (Was 14; `PriceByProviderModal.tsx` was corrected out after finding indirect coverage at
`PricingInformationV2-tests.tsx:215`.)

**Why it matters:** The tail of the coverage list. Low individual risk, but it's the honest bottom of
the pyramid.

**Test plan:**
- Work the list in the inventory file, cheapest first
- A component test per file: renders, handles its empty state, handles its primary interaction
- Skip anything that turns out to be dead code — and delete that instead, with a note

**Effort:** 1 day
**Risk if not fixed:** Low
· [FE-013](gaps/tickets/FE-013-thirteen-source-files-with-no-coverage.md) · [BILL-1205](https://zocdoc.atlassian.net/browse/BILL-1205)

---

### 20. 15 billing test files are exempt from the coverage gate — so what do they leave untested?

**File:** the 15 gate-exempt billing test files · repo `zocdoc_web`

**Current testing:** Unknown, and that is the finding. These files opted out of the coverage gate, so
this is the one part of the billing tree where the real coverage number isn't known — and it is the
same tree that holds items 5, 9, and 10.

**Why it matters:** The question is **not** "why is the gate off". Re-enabling the gate is explicitly
**not** the goal — that's a config change, not test coverage. The question is *which billing code is
therefore untested*.

**Test plan:**
- For each of the 15 files, establish what billing code it covers
- Produce a list of billing code left uncovered — **that list is the deliverable**
- Feed anything material on that list back into this backlog as its own ticket

**Effort:** 4 hours
**Risk if not fixed:** Low (but it's a known unknown sitting next to three P0/P1 items)
· [BILL-1220](https://zocdoc.atlassian.net/browse/BILL-1220)

---

## Hygiene — not test coverage

### 21. Three `provider-billing` test projects are named for something they don't test

**File:** `tests/IntegrationTests/HandlerTests.cs`, two SQLite-backed files under `tests/IntegrationTests/` · repo `provider-billing`

| Project / file | Named | Actually is |
|---|---|---|
| `tests/IntegrationTests/HandlerTests.cs` | integration | a **unit test** — mocks every dependency, crosses no boundary |
| Two files under `tests/IntegrationTests` | integration against MySQL | integration against **SQLite** — a different engine from production |

**Why it matters:** **This is repo structure, not test coverage** — no bug ships because a folder is
misnamed, which is why it sits outside the priority list and outside the effort total. It's kept
because the counts in this analysis are read off those project names, so wrong names make the counts
misleading. The SQLite case is the one with real risk attached: collation, date handling, and
strictness all differ from MySQL, so those two files prove less than their location implies.

**Test plan:**
- Move `HandlerTests.cs` to the unit project, or justify in writing why it belongs where it is
- Run the two SQLite files against MySQL, or rename them to state the engine and record the limitation
- Delete or document the empty `src/ProviderBilling.CronJobs` project
- Verification: `dotnet test` passes with the **same total test count** as before — relabelling must not lose a test

**Effort:** 2 hours
**Risk if not fixed:** Low (decision quality only)
· [BILL-1216](https://zocdoc.atlassian.net/browse/BILL-1216)

---

## Recommended next steps

| # | Action | Effort | What It Fixes |
|---|---|---|---|
| 1 | Add unit tests for `invoiceHelpers.ts` (item 3) | 45 min | Cheapest P0 — pure functions, no mocking |
| 2 | Hardcode the monthly-limit boundaries (item 2) | 45 min | Turns a test that *cannot fail* into one that can |
| 3 | Delete the empty test + 4 duplicates (item 13) | 45 min | 5 tests gone, zero coverage risk |
| 4 | Un-nest the six `if (mock.find(...))` assertions (item 7) | 2 hours | Makes the browser suite tell the truth before you act on it |
| 5 | Add one real-Stripe Payment Element test (item 1) | 1 day | The revenue path. Worth more than the whole 39-test deletion |
| 6 | Add contract tests for the 13 billing endpoints (item 6) | 1 day | Backend renames start failing in CI instead of in production |
| 7 | Cover Stripe webhook dedup (item 4) | 1 day | Double-charge risk in `provider-billing` |
| 8 | Test prorated day-count + tax amounts (items 5, 9) | 6 hours | Two monetary calculations in the monolith |
| 9 | Then the browser-test reduction, in order: items 14 → 11 → 12 | ~2.5 days | ~58 fewer browser tests at the same confidence |
| 10 | The remainder (items 10, 15–20) | ~3 days | Backfill |
| — | Item 21 (renaming test projects) | 2 hours | Nothing test-wise. Hygiene only — not part of the total |

**Total estimated effort: ~11 days.** The first four rows are **~4 hours** and are worth doing this
week regardless of what else gets scheduled.

### One order that matters

Do **not** delete browser tests before adding the real one. Running items 13 + 11 + 12 without item 1
leaves billing with essentially **one** test that exercises a multi-page journey. Every individual
call would be correct and the suite would still be worse.

```
item 7   (make the suite tell the truth — 6 tests pass vacuously today)
   ↓
item 1   (add the one real test) · item 14 (relocate the pixel assertions)
   ↓
item 13  (free wins) → item 11 (move 19 down) → item 12 (bulk delete, last)
```

Item 1 should also land before item 16. Item 16 is a flag teardown of the same kind that changed the
payment DOM on 2026-09-02 (`70a384854e`) and broke a downstream Playwright suite while monorepo CI
stayed green — because monorepo CI mocks Stripe. Item 1 is the test that would catch it here.

Everything else is independent. Start any of it today.

## One warning

**Do not execute v2's #1 P0.** It says delete `LegacyInvoiceView` as dead code. It is **live** —
imported at `InvoiceDetailsContainer.tsx:16`, rendered at `:201`. The commit v2 blamed
(`a88b14cba6`) never touched it; removing that flag made the legacy branch **permanent, not dead**.
Executing it breaks invoice rendering for providers. → [`V2-VALIDATION.md`](V2-VALIDATION.md)

## Backend repos (new in v3)

**`provider-billing`** — never in v1/v2 scope. An entire .NET service with five test projects.
Findings: items 4, 17, 18, plus hygiene item 21.

**`zocdoc_web`** — billing lives in the monolith alongside Selenium tests. Findings: items 5, 9, 10,
20. Two of those four are monetary calculations with either no test or a tautological one.

**Both are Jira-only.** The per-ticket write-ups and the inventories for these two repos were never
committed here — the Jira ticket is the only detail that exists for those eight items.

## Notable deltas from v2 (2026-04-23)

| Change | Impact | Notes |
|---|---|---|
| Cypress removed monorepo-wide; billing ported to Playwright | Browser suite **grew 32%** (2,302 → 3,049 lines) | `0561a881ee`, 2026-07-06. The port was the cheapest moment to shift left; it wasn't taken |
| `SHOW_NEW_BILLING_MEZZ_REVAMP` torn down | −1,080 test lines | `d5317c99b6`. v2's top cleanup, done |
| Revenue calculator tested | +34 tests | BILL-748, BILL-962. Was the standing P0 |
| Billing payment code extracted to `shared/core` | Coverage now spans an app/shared boundary | Boundary didn't exist in v2 |
| `billing_payment_element_flow` torn down | Payment Element is the only path now | `70a384854e`, 2026-09-02 — broke a downstream suite |
| v2's P0 #1 re-checked | **Wrong** | `LegacyInvoiceView` is live code |
| `provider-billing` + `zocdoc_web` brought into scope | +8 items (7 coverage, 1 hygiene) | Neither was in v1/v2 |
| Unit + component tests | 365 → 856 | Real growth |
| API contract tests | 0 → 0 | Unchanged, and now measured |

## Key feature flags under review

| Flag | Status | Action |
|---|---|---|
| `SHOW_NEW_INVOICE_DETAILS_PAGE` | Torn down (`a88b14cba6`) | **No deletion.** It made `LegacyInvoiceView` permanent — item 15 |
| `SHOW_NEW_BILLING_MEZZ_REVAMP` | Torn down (`d5317c99b6`) | Done — v2's cleanup landed |
| `billing_payment_element_flow` | Torn down (`70a384854e`, 2026-09-02) | Cautionary: broke a downstream suite with monorepo CI green |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | **Still unverified** | Determine ramp state, then remove the dead branches — item 16 |
| `Billing.MinimumPaymentMethodLimit` | Active | Its only assertion is a tautology — item 2 |
| `SHOULD_MOCK_STRIPE` (test cookie) | Being removed from production code | Team is on it (`dd9e4952a6`); don't open a competing ticket |

## Honest limitations

- **`provider-billing`'s ~70 integration tests may never run.** They skip themselves when LocalStack
  is unavailable and nobody confirmed LocalStack is provisioned in CI. If it isn't, that whole layer
  reports success without executing. Five minutes on the pipeline config before trusting the count.
- **`provider-billing` and `zocdoc_web` findings exist only as Jira tickets** — no write-ups or
  inventories were committed here for those eight items.
- **No coverage tooling was run.** Counts come from reading test files. A test existing is not proof
  it asserts anything useful.
- **Runtime figures are estimates** unless labelled otherwise; the serial-CI basis is confirmed
  (`playwright.config.ts:14`).
- **Assertion quality and flakiness are out of scope** except where called out (items 2, 7, 9).
- Anything unconfirmable is written `UNVERIFIED — <what's needed>` rather than asserted.
- Findings are true as of `provider-fe-monorepo` `dd9e4952a6`, `provider-billing` `84318e3d5c`,
  `zocdoc_web` `8742b5072da` (2026-09-03/04).

## Deeper dives

- **All 21 tickets with sequencing and Jira keys** → [`gaps/BACKLOG.md`](gaps/BACKLOG.md)
- **What tests exist today** → [`inventory/provider-fe-monorepo/`](inventory/provider-fe-monorepo/)
- **How do I check these claims myself?** → [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md)
- **What did the team already fix?** → [`ALREADY-FIXED.md`](ALREADY-FIXED.md)
- **Which v2 callouts survived?** → [`V2-VALIDATION.md`](V2-VALIDATION.md)
- **Is the browser-test reduction plan safe?** → [`shift-left/E2E-PLAN-JUDGMENT.md`](shift-left/E2E-PLAN-JUDGMENT.md)
- **Which of the 63 browser tests goes where?** → [`shift-left/E2E-TEST-BY-TEST.md`](shift-left/E2E-TEST-BY-TEST.md)
- **How was this produced?** → [`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md)
