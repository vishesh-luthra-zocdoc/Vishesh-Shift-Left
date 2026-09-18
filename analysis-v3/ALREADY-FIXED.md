# Already Fixed — Credit Where It's Due

**Purpose:** v1 and v2 raised gaps. Some were closed by the team before v3 ran. This file records
them so v3 does not re-raise closed work, and so the analysis is honest about progress rather than
presenting a static wall of complaints.

Everything here is verified against `provider-fe-monorepo` git history. SHAs are real and
re-checkable.

---

## 1. The revenue calculator P0 — FIXED, and fixed well

**What was wrong:** `YearlyValueCalcModal` — the "what could Zocdoc be worth to you per year"
estimator on the Pricing tab — computed a dollar figure shown to providers and had **no tests on the
arithmetic or the input validation**. A wrong number here is a wrong revenue promise to a customer.

**How it was fixed — two tickets, six days apart:**

| Ticket | Commit | Date | What landed |
|---|---|---|---|
| **BILL-748** | `b5cc093d71` (#11364) | 2026-07-17 | `steps-tests.ts` created (+162). Also deleted the dead V1 modal — `index.tsx`, `StepContent.tsx`, `ResultContent.tsx`, `Common.ts`, stories (−505 lines). |
| **BILL-962** | `89f5111df0` (#11382) | 2026-07-23 | `YearlyValueCalcModalV2-tests.tsx` (+124) and `ResultContentV2-tests.tsx` (+73) created, `steps-tests.ts` extended (+19). |

**Coverage now, at `dd9e4952a6`:**

| Test file | Lines | Tests |
|---|---|---|
| `__tests__/YearlyValueCalcModalV2-tests.tsx` | 556 | 26 |
| `__tests__/steps-tests.ts` | 181 | 6 |
| `__tests__/ResultContentV2-tests.tsx` | 73 | 2 |
| **Total** | **810** | **34** |

All 34 are **component** tests (jsdom render, no browser) — the correct level. Runtime is
milliseconds, not minutes.

### Why this fix is the model for the rest of the backlog

The money assertion is **not a tautology**. `YearlyValueCalcModalV2-tests.tsx:206-225`:

```ts
// showUps=7, reimbursements=245, patientReturns=45,
// patientsPerYear=2, followUpReimbursement=247
// result = (7/10) * (245 + 2 * 247 * (45/100))
//        = 0.7 * (245 + 222.3)
//        = 0.7 * 467.3 = 327.11
expect(resultText).toBe('$327');
```

The expected value is **worked out by hand in the comment and hardcoded**. If someone changes the
formula in `YearlyValueCalcModalV2.tsx:48 calculateResult()`, this test fails. That is what a money
test is supposed to do.

Compare this to the anti-pattern still live in the same codebase —
`EditMonthlyLimitModalV2-tests.tsx:129-133` computes its expected value using *the same expression
the source under test uses* (`getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500'`).
If the source default were wrong, the test computes the identical wrong value and passes. It cannot
fail for the reason it exists.

**Same team, same file tree, two months apart — one test can catch a money bug and the other cannot.**
That is the single clearest illustration of what v3's backlog is for. `FE-002` in the gap list is
"make the monthly-limit test look like the yearly-calculator test."

> Note on the ticket number: you remembered this as BILL-196. BILL-196 (`66dd3a81f7`, #10350,
> `feat(BILL-196): mezzify revenue calculator modal`) is the *feature* commit that mezzified the
> modal — plausibly where the bug entered. The **tests** came from BILL-748 and BILL-962.

---

## 2. v2's biggest single recommendation — FIXED

v2's largest cleanup item was "`billing-settings-page-tests.ts` is 1,254 lines and may be redundant;
check the `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout."

v2's line count was **exactly right** (verified: `git show b730e8aafb:...` → 1254), and v2's
hypothesis was right too — it *was* the flag rollout.

What actually happened, commit by commit:

| When | Commit | Effect |
|---|---|---|
| 2026-05-13 | `d5317c99b6` (#10712, BILL-663) — tear down `SHOW_NEW_BILLING_MEZZ_REVAMP` | **−1,080 lines**, 1,254 → 175. The old-billing test branches became unreachable the moment the flag went, and were removed with it. |
| May–Jul | assorted | drifted 175 → 179 |
| 2026-07-06 | Cypress → Playwright port | file **deleted**; its remaining coverage moved to the Playwright specs |

So the reduction was not a generic cleanup — it was the flag teardown v2 told the team to go look at.
The file no longer exists.

**Closed. Not re-raised in v3.**

---

## 3. Dead V1 code removal — FIXED (partially, and this is the caveat)

`b5cc093d71` deleted 505 lines of dead V1 `YearlyValueCalcModal` code alongside adding the tests —
the right pattern: delete the dead branch and cover the live one in the same change.

**But:** v2's #1 P0 claimed `LegacyInvoiceView` was similarly dead and should be deleted. It is
**not** dead — it is imported at `InvoiceDetailsContainer.tsx:16` and rendered at `:201`. See
[`V2-VALIDATION.md`](V2-VALIDATION.md). The team was right not to act on that one.

---

## 4. Production code reading a test-only cookie — IN PROGRESS

`SHOULD_MOCK_STRIPE` is a test cookie that **production components branch on**
(`CreditCardFormContentV2.tsx:52`, `AchFormContentV2.tsx:69`). The most recent commit on `main` —
`dd9e4952a6` (#12074) `refactor(billing): move the Stripe.js mock out of production code` — is the
team fixing exactly this.

**v3 does not open a competing ticket.** It reinforces the direction and notes the consequence for
the E2E suite: while that cookie is honoured, the green E2E path executes code real users never run.

---

## 5. Other verified test work since v2

| Commit | Date | What |
|---|---|---|
| `f1ca5f7d09` (#11463) | 2026-07-28 | BILL-976 — multi-month mock scenario + grouping tests for payment recovery |
| `d1fb0c10ab` (#11303) | 2026-07-09 | BILL-843 — card-entry stories + E2E for both pay-now routes |
| `b226948a1f` (#11590) | 2026-08-10 | BILL-1073 — `latestDeclineAtUtc` on the recovery summary |
| `ad433d2bee` (#11628) | 2026-08-11 | BILL-1097 — toast vertical padding matched to design spec |

`ad433d2bee` is worth flagging: it is the origin of the toast-geometry assertion
(`height === 68`) that is currently the **sole reason** an E2E test is kept alive. A real design bug
was fixed, but the regression guard landed at the browser level where it costs a browser boot. v3 recommends moving
it to visual regression rather than deleting it — see
[`shift-left/E2E-PLAN-JUDGMENT.md`](shift-left/E2E-PLAN-JUDGMENT.md) Phase 2.

---

## Scorecard

| Item | Raised in | Status |
|---|---|---|
| `YearlyValueCalcModal` untested money math | v1/v2 era P0 | ✅ **Fixed** (BILL-748, BILL-962) — 34 tests, non-tautological |
| `billing-settings-page-tests.ts` 1,254 lines | v2 P2 #6 | ✅ **Fixed** — `d5317c99b6` flag teardown cut it to 175; file deleted in the Jul 6 Playwright port |
| Dead V1 calculator code | v2 (general) | ✅ **Fixed** — 505 lines removed |
| Stripe mock in production code | not raised | 🔄 **In progress** by the team (`dd9e4952a6`) |
| `LegacyInvoiceView` "dead code" | v2 P0 #1 | ❌ **Was never a real gap** — v2 was wrong, correctly not acted on |
| `invoiceHelpers.ts` untested | v2 P0 #2 | ⬜ Still open → v3 ticket |
| `schemaBuilder.ts` tautological test | v2 P1 #3 | ⬜ Still open, **worse than v2 thought** → v3 ticket |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | v2 #5 | ⬜ Still unverified → v3 `investigate` ticket |
| Shift-left the E2E suite | v2 plan | ⬜ Not done; suite **grew 32%** in the Playwright port |
