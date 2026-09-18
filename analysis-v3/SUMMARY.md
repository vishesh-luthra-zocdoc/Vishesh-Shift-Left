# Billing Test Analysis — Executive Summary (v3)

**Date:** 2026-09-04
**Scope:** pre-release automated tests in the three team-owned repos — `provider-fe-monorepo`
(Settings billing), `provider-billing` (.NET service), `zocdoc_web` (monolith billing). The QA-owned
`sandbox` repo is **not** in scope.
**Prior Analysis:** v1 (2026-04-14), v2 (2026-04-23)
**Drift since v2:** ~4.5 months. `provider-fe-monorepo` moved 550 commits; Cypress was removed
monorepo-wide and the billing specs were rewritten in Playwright.
**Jira:** epic [BILL-746](https://zocdoc.atlassian.net/browse/BILL-746) holds **24** issues — the 21
from this analysis plus 3 that pre-date it (see *Epic contents* below)

---

## How to read this

This page is the whole analysis. Read the numbered list in **What Needs Attention** — it is ordered
P0 → P3, and each item names the file, the problem, the test level, and its Jira ticket. Then use
**Recommended Next Steps** to pick what to do first. Everything else is detail:

| If you want to… | Read |
|---|---|
| Work the tickets | [`gaps/BACKLOG.md`](gaps/BACKLOG.md) — same items with links and sequencing |
| Read one gap in full | `gaps/tickets/FE-0NN-*.md` (13 frontend tickets) |
| Check my work before trusting it | [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md) |
| See what the team already fixed | [`ALREADY-FIXED.md`](ALREADY-FIXED.md) |
| Know what v2 got wrong | [`V2-VALIDATION.md`](V2-VALIDATION.md) |

### Epic contents — what the 24 issues under BILL-746 are

| Group | Count | Keys |
|---|---|---|
| From this analysis (v3) | 20 | BILL-1193–1205, 1211, 1212, 1214, 1217–1220 |
| From this analysis, hygiene not coverage | 1 | BILL-1216 — item 21 below |
| Pre-dating v3, filed by QA | 3 | BILL-747 *(open)*, BILL-748 *(closed)*, BILL-962 *(closed)* |

The two closed ones are the revenue-calculator work credited under *What's Working Well*.
BILL-747 ("make monolith invoice generation testable") is still open and overlaps item 10.

Three more v3 tickets were filed and then **deleted as out of scope** — BILL-1206, BILL-1213,
BILL-1215. Their findings are preserved under "Dropped from scope" in
[`gaps/BACKLOG.md`](gaps/BACKLOG.md).

**Already moving:** item 3 ([BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195)) and item 6
([BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197)) are **In Progress** — the cheapest P0 and
the empty L4 row. Check with the assignees before starting either.

**The five test levels**, used throughout. They are labels for *how much of the system a test starts
up* — not for which folder it lives in:

| Level | Plain English | Example in your code | Speed |
|---|---|---|---|
| **L1 — unit** | One function on its own | testing `formatDate` | milliseconds |
| **L2 — component** | One screen on its own | testing `EditMonthlyLimitModal` | milliseconds |
| **L3 — integration** | A few pieces wired together | modal + real provider tree | ~seconds |
| **L4 — api** | The API returns the fields the page expects | *(you have none)* | ~1 second |
| **L5 — e2e** | A real browser clicking through billing | Playwright billing specs | 5–120 seconds |

Lower is better whenever it catches the same bug: faster, runs on every PR, easier to debug.

---

## The Big Picture

**Two facts drive almost every item below.**

1. **Nothing checks that the billing API and the billing page agree on the data.** That is the zero
   in the L4 row. A backend field rename passes all 856 other frontend tests and breaks the billing
   page in front of providers.
2. **All 63 browser tests fake the backend.** A fake Stripe.js is installed for the whole E2E
   directory (`apps/settings/e2e/fixtures.ts:32`) and all 13 endpoints are stubbed. They pay a
   browser boot (5–120s each, on **one** CI worker) to prove what a component test proves.

**Progress since v2** — real, and credited in [`ALREADY-FIXED.md`](ALREADY-FIXED.md):
- The revenue-calculator P0 is **closed** (BILL-748 + BILL-962, 34 tests, correct assertions).
- v2's biggest cleanup shipped: `billing-settings-page-tests.ts` 1,254 → 179 lines, then deleted.
- 505 lines of dead V1 calculator code removed alongside the tests — the right pattern.
- Moving the Stripe mock out of production code is **in progress** (`dd9e4952a6`).

**What we looked at — `provider-fe-monorepo` billing:**

| Level | Files | Tests |
|---|---|---|
| L1 unit | 34 | 224 |
| L2 component | 45 | 515 |
| L2 hooks | 9 | 47 |
| L3 integration | 2 | 70 |
| **L4 api** | **0** | **0** |
| L5 e2e | 7 | 63 |

| | Count |
|---|---|
| Billing source files | 152 |
| …with some coverage | 88 |
| …with **no coverage at all** | **13** |
| REST endpoints consumed by the UI | 13 |
| …with a contract test | **0** |
| E2E tests that mock their entire backend | **63 of 63** |
| E2E tests kept alive only for pixel measurements | 3 |

`provider-billing`: 5 test projects, ~70 L3 integration tests (**may not execute — see limitations**).
`zocdoc_web`: billing Selenium + unit tests; 15 test files opted out of the coverage gate.

## What's Working Well

- **The money test that matters is done right.** `YearlyValueCalcModalV2-tests.tsx:224` hardcodes
  `$327` with the arithmetic worked out by hand in the comment. Change the formula, the test fails.
  That is the pattern the rest of the backlog should copy.
- **V2 Mezzanine components are well covered at L2** — modals, hooks, and sections all have
  component tests, and they run in milliseconds.
- **Test count grew substantially** since v2: 365 → 856 unit + component tests.
- **The team deletes dead code with its tests**, not tests alone (`b5cc093d71`, −505 lines).
- **`provider-billing` has a real L3 layer** — integration tests against LocalStack, which is the
  right level for a queue-driven service.

## What Needs Attention

Twenty coverage findings, numbered continuously, plus one hygiene item (21) that is not coverage
work. Each names the level it belongs at and its Jira ticket.

### P0 — Critical (can corrupt money or provider-facing data)

1. **Real Stripe card entry is untested at every level** — `apps/settings/e2e/fixtures.ts:32`
   installs a fake Stripe.js directory-wide. Nothing anywhere proves a real Payment Element mounts,
   accepts a card, or handles a decline. A Stripe.js bump, a bad publishable key, or a CSP change
   breaks card entry in production with all 63 tests green. **L5** · 1d ·
   [FE-001](gaps/tickets/FE-001-real-stripe-payment-element-untested.md) ·
   [BILL-1193](https://zocdoc.atlassian.net/browse/BILL-1193)

2. **The monthly-limit test cannot fail** — `EditMonthlyLimitModalV2-tests.tsx:129` computes its
   expected value with `getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500'`, the
   same expression the source under test uses. If the source default were wrong, the test computes
   the same wrong value and passes. `maximumMonthlyLimit = 500000`
   (`utils/schemaBuilder.ts:101`) is asserted **nowhere**. **L1** · 45m ·
   [FE-002](gaps/tickets/FE-002-monthly-limit-tautological-test.md) ·
   [BILL-1194](https://zocdoc.atlassian.net/browse/BILL-1194)

3. **`invoiceHelpers.ts` has zero tests** — three exported pure functions (`formatDate`,
   `getLastDayOfMonth`, `capitalizeStatus`) used by both invoice views. Date-formatting bugs show
   wrong invoice dates to providers. Raised as v2's P0 #2; still open. **L1** · 45m ·
   [FE-003](gaps/tickets/FE-003-invoice-helpers-untested.md) ·
   [BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195)

4. **Stripe webhook deduplication is untested and bypassed** — idempotency is disabled in production
   and all four dedup tests are commented out. A replayed webhook could double-charge a provider.
   **L3** · 1d · [BILL-1211](https://zocdoc.atlassian.net/browse/BILL-1211) *(`provider-billing`)*

5. **Prorated subscription day-count is untested, and the source says the math is wrong** — the
   comment in the monolith flags the calculation as incorrect and no test pins the behaviour either
   way. **L1** · 4h · [BILL-1217](https://zocdoc.atlassian.net/browse/BILL-1217) *(`zocdoc_web`)*

### P1 — High Priority (real user-visible failure, or material CI cost)

6. **Zero API contract tests** — not thin, **zero**. No MSW, no `nock`. The frontend mocks what it
   *believes* each of the 13 endpoints returns and nobody checks that belief. This is the empty L4
   row. **L4** · 1d · [FE-005](gaps/tickets/FE-005-zero-api-contract-tests.md) ·
   [BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197)

7. **Six E2E tests are one fixture change away from testing nothing** — every assertion sits inside
   `if (mock.find(...))`. If the fixture stops matching, they pass while asserting nothing. Fix this
   before trusting any E2E result, including the ones below. **L5** · 2h ·
   [FE-004](gaps/tickets/FE-004-conditional-assertions-green-noops.md) ·
   [BILL-1196](https://zocdoc.atlassian.net/browse/BILL-1196)

8. **The ACH / bank-account path has no E2E coverage** — `mockAchInfo` exists, but no spec ever
   selects the option that renders it. **L5** · 4h ·
   [FE-006](gaps/tickets/FE-006-ach-no-e2e-coverage.md) ·
   [BILL-1198](https://zocdoc.atlassian.net/browse/BILL-1198)

9. **Tax amounts in `ProcessorGenerateChargeGroupsTest` are asserted tautologically** — same
   cannot-fail pattern as item 2, applied to tax. **L1** · 2h ·
   [BILL-1218](https://zocdoc.atlassian.net/browse/BILL-1218) *(`zocdoc_web`)*

10. **The bill generator has no active tests** — its only test fixture is `[Ignore]`d, so the class
    that produces bills is entirely unexercised. **L3** · 1d ·
    [BILL-1219](https://zocdoc.atlassian.net/browse/BILL-1219) *(`zocdoc_web`)*

### P2 — Medium (meaningful gap, low blast radius)

11. **19 browser tests should be component tests** — they mock everything, so moving them down loses
    no confidence and runs roughly 100× faster. Land each L2 test *before* removing its L5
    counterpart. **L2** · 1d · [FE-009](gaps/tickets/FE-009-shift-19-e2e-tests-to-component-level.md) ·
    [BILL-1201](https://zocdoc.atlassian.net/browse/BILL-1201)

12. **39 browser tests duplicate named component tests** — delete them, but **do this last** (see
    the sequencing warning). **L5** · 1d ·
    [FE-010](gaps/tickets/FE-010-delete-39-redundant-e2e-tests.md) ·
    [BILL-1202](https://zocdoc.atlassian.net/browse/BILL-1202)

13. **One empty E2E test and four intra-suite duplicates** — delete. Zero coverage risk. **L5** ·
    45m · [FE-007](gaps/tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) ·
    [BILL-1199](https://zocdoc.atlassian.net/browse/BILL-1199)

14. **Three pixel assertions keep browser tests alive purely for layout** (`height === 68`,
    `scrollTop === 0`, `boundingBox()` ordering — the last from a real design fix, `ad433d2bee`).
    Move them to visual regression; do **not** delete them. **L5** · 4h ·
    [FE-008](gaps/tickets/FE-008-move-geometry-assertions-to-visual-regression.md) ·
    [BILL-1200](https://zocdoc.atlassian.net/browse/BILL-1200)

15. **`LegacyInvoiceView` coverage is thin on a now-unconditional path** — it renders for every
    non-FPB invoice. **Do not delete it**; v2 said to, and v2 was wrong. **L2** · 2h ·
    [FE-012](gaps/tickets/FE-012-legacy-invoice-view-coverage.md) ·
    [BILL-1204](https://zocdoc.atlassian.net/browse/BILL-1204)

16. **`BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` still carries test branches** — ramp state can't be
    read from code. Determine it, then remove the dead branches. **L2** · 2h ·
    [FE-011](gaps/tickets/FE-011-investigate-iframe-deprecation-flag.md) ·
    [BILL-1203](https://zocdoc.atlassian.net/browse/BILL-1203)

17. **`ActualCost = 0` is hardcoded in the appointment event processor** with no test pinning it.
    **L1** · 2h · [BILL-1212](https://zocdoc.atlassian.net/browse/BILL-1212) *(`provider-billing`)*

18. **The billing-export Generate stage has no integration test** — Gather and Enrich each have one;
    Generate, the stage that produces the output, does not. **L3** · 4h ·
    [BILL-1214](https://zocdoc.atlassian.net/browse/BILL-1214) *(`provider-billing`)*

### P3 — Low (polish)

19. **13 billing source files have no tests at all** — the tail of the coverage list. **L2** · 1d ·
    [FE-013](gaps/tickets/FE-013-thirteen-source-files-with-no-coverage.md) ·
    [BILL-1205](https://zocdoc.atlassian.net/browse/BILL-1205)

20. **15 billing test files are exempt from the coverage gate** — so this is the one part of the
    billing tree where the real coverage number is unknown, and it's the same tree that holds items
    5, 9, and 10. The question is not "why is the gate off", it's **"which billing code is therefore
    untested?"** The deliverable is a list of untested code, not a config change. **L1** · 4h ·
    [BILL-1220](https://zocdoc.atlassian.net/browse/BILL-1220) *(`zocdoc_web`)*

21. **Three `provider-billing` test projects are named for a level they don't test at** — e.g. a
    project called *integration* holding unit tests. **This is repo structure, not test coverage** —
    no bug ships from a misnamed folder. Kept as hygiene so the L-level counts mean what they say;
    schedule it whenever, or never. **n/a** · 2h ·
    [BILL-1216](https://zocdoc.atlassian.net/browse/BILL-1216) *(`provider-billing`)*

## Recommended Next Steps

| # | Action | Effort | What It Fixes |
|---|---|---|---|
| 1 | Add unit tests for `invoiceHelpers.ts` (item 3) | 45 min | Cheapest P0 — pure functions, no mocking |
| 2 | Hardcode the monthly-limit boundaries (item 2) | 45 min | Turns a test that *cannot fail* into one that can |
| 3 | Delete the empty test + 4 duplicates (item 13) | 45 min | 5 tests gone, zero coverage risk |
| 4 | Un-nest the six `if (mock.find(...))` assertions (item 7) | 2 hours | Makes the E2E suite tell the truth before you act on it |
| 5 | Add one real-Stripe Payment Element test (item 1) | 1 day | The revenue path. Worth more than the whole 39-test deletion |
| 6 | Add contract tests for the 13 billing endpoints (item 6) | 1 day | Fills the empty L4 row — backend renames start failing in CI |
| 7 | Cover Stripe webhook dedup (item 4) | 1 day | Double-charge risk in `provider-billing` |
| 8 | Test prorated day-count + tax amounts (items 5, 9) | 6 hours | Two monetary calculations in the monolith |
| 9 | Then the E2E reduction, in order: items 14 → 11 → 12 | ~2.5 days | ~58 fewer browser tests at the same confidence |
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
Findings: items 4, 17, 18. Its ~70 L3 integration tests are the right level for a queue-driven
service, but see the limitation below about whether they run.

**`zocdoc_web`** — billing lives in the monolith alongside Selenium tests. Findings: items 5, 9, 10,
20. Two of the four are monetary calculations with either no test or a tautological one.

**Both are Jira-only.** The per-ticket write-ups and the inventories for these two repos were never
committed here — the Jira ticket is the only detail that exists for those eight items.

## Notable Deltas from v2 (2026-04-23)

| Change | Impact | Notes |
|---|---|---|
| Cypress removed monorepo-wide; billing ported to Playwright | E2E **grew 32%** (2,302 → 3,049 lines) | `0561a881ee`, 2026-07-06. The port was the cheapest moment to shift left; it wasn't taken |
| `SHOW_NEW_BILLING_MEZZ_REVAMP` torn down | −1,080 test lines | `d5317c99b6`. v2's top cleanup, done |
| Revenue calculator tested | +34 tests | BILL-748, BILL-962. Was the standing P0 |
| Billing payment code extracted to `shared/core` | Coverage now spans an app/shared boundary | Boundary didn't exist in v2 |
| `billing_payment_element_flow` torn down | Payment Element is the only path now | `70a384854e`, 2026-09-02 — broke a downstream suite |
| v2's P0 #1 re-checked | **Wrong** | `LegacyInvoiceView` is live code |
| `provider-billing` + `zocdoc_web` brought into scope | +8 items (7 coverage, 1 hygiene) | Neither was in v1/v2 |
| Unit + component tests | 365 → 856 | Real growth |
| API contract tests | 0 → 0 | Unchanged, and now measured |

## Key Feature Flags Under Review

| Flag | Status | Action |
|---|---|---|
| `SHOW_NEW_INVOICE_DETAILS_PAGE` | Torn down (`a88b14cba6`) | **No deletion.** It made `LegacyInvoiceView` permanent — item 15 |
| `SHOW_NEW_BILLING_MEZZ_REVAMP` | Torn down (`d5317c99b6`) | Done — v2's cleanup landed |
| `billing_payment_element_flow` | Torn down (`70a384854e`, 2026-09-02) | Cautionary: broke a downstream suite with monorepo CI green |
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | **Still unverified** | Determine ramp state, then remove test branches — item 16 |
| `Billing.MinimumPaymentMethodLimit` | Active | Its only assertion is a tautology — item 2 |
| `SHOULD_MOCK_STRIPE` (test cookie) | Being removed from production code | Team is on it (`dd9e4952a6`); don't open a competing ticket |

## Honest limitations

- **`provider-billing`'s ~70 L3 integration tests may never run.** They skip themselves when
  LocalStack is unavailable and nobody confirmed LocalStack is provisioned in CI. If it isn't, that
  whole layer reports success without executing. Five minutes on the pipeline config before trusting
  the L3 count.
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

## Deeper Dives

- **All 21 tickets with sequencing and Jira keys** → [`gaps/BACKLOG.md`](gaps/BACKLOG.md)
- **What tests exist today, per level?** → [`inventory/provider-fe-monorepo/`](inventory/provider-fe-monorepo/)
- **How do I check these claims myself?** → [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md)
- **What did the team already fix?** → [`ALREADY-FIXED.md`](ALREADY-FIXED.md)
- **Which v2 callouts survived?** → [`V2-VALIDATION.md`](V2-VALIDATION.md)
- **Is the E2E reduction plan safe?** → [`shift-left/E2E-PLAN-JUDGMENT.md`](shift-left/E2E-PLAN-JUDGMENT.md)
- **What do L1–L5 mean precisely?** → [`methodology/TEST-LEVEL-TAXONOMY.md`](methodology/TEST-LEVEL-TAXONOMY.md)
- **How was this produced?** → [`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md)
