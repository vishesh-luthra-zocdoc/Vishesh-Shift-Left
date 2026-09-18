# Billing Test Gap Analysis — v3

**Date:** 2026-09-04 · **Prior runs:** v1 (2026-04-14), v2 (2026-04-23) · **Jira project:** BILL

**Scope:** pre-release tests in team-owned repos — `provider-fe-monorepo`, `provider-billing`,
`zocdoc_web`. The QA-owned `sandbox` repo is handled separately and is **not** in this analysis.

---

## Read this page. Everything else is detail you can skip.

| If you want to… | Go to |
|---|---|
| See what to fix and in what order | [The list](#what-needs-testing-by-priority), below |
| File tickets | [`gaps/BACKLOG.md`](gaps/BACKLOG.md) |
| Read one gap in full | `gaps/tickets/<ID>.md` |
| Check my work before trusting it | [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md) |
| See what the team already fixed | [`ALREADY-FIXED.md`](ALREADY-FIXED.md) |
| Know what v2 got wrong | [`V2-VALIDATION.md`](V2-VALIDATION.md) |

---

## What the test levels mean

Every test in this analysis is tagged with one of five levels. They are just labels for **how much
of the system a test starts up**:

| Level | Plain English | Example from your code | Speed |
|---|---|---|---|
| **L1 — unit** | One function on its own | testing `formatDate` | milliseconds |
| **L2 — component** | One screen on its own | testing `EditMonthlyLimitModal` | milliseconds |
| **L3 — integration** | A few pieces wired together | modal + real provider tree | ~seconds |
| **L4 — api** | The billing API returns the fields the page expects | *(you have none)* | ~1 second |
| **L5 — e2e** | A real browser clicking through billing | Playwright billing specs | 5–120 seconds |

Lower is better when it can catch the same bug: faster, runs on every PR, easier to debug.

## Where billing stands today

`provider-fe-monorepo`:

| Level | Files | Tests |
|---|---|---|
| L1 unit | 34 | 224 |
| L2 component | 54 | 562 |
| L3 integration | 2 | 70 |
| **L4 api** | **0** | **0** |
| L5 e2e | 7 | 63 |

152 source files · 88 with coverage · **13 with no coverage at all**

## The two sentences that matter

**1. Nothing checks that the billing API and the billing page agree on the data.** That's the zero
row. A backend field rename passes all 856 other tests and breaks the billing page in front of
providers.

**2. All 63 browser tests fake the backend.** They cost a browser boot (5–120s each, on one CI
worker) and prove only what a component test proves. Most should be component tests; a few should be
real.

Everything below follows from those two.

---

## What needs testing, by priority

### P0 — can corrupt money or provider-facing data

| ID | What needs testing | Level | Est. |
|---|---|---|---|
| [FE-001](gaps/tickets/FE-001-real-stripe-payment-element-untested.md) | That a **real** Stripe Payment Element mounts and accepts a card. All 63 E2E tests install a fake Stripe, so a Stripe.js bump breaks card entry in production with everything green. | L5 | 1d |
| [FE-002](gaps/tickets/FE-002-monthly-limit-tautological-test.md) | The monthly payment limit boundaries. The existing test computes its expected value using the same code it tests — it **cannot fail**. `maximumMonthlyLimit = 500000` is asserted nowhere. | L1 | 45m |
| [FE-003](gaps/tickets/FE-003-invoice-helpers-untested.md) | `invoiceHelpers.ts` — `formatDate`, `getLastDayOfMonth`, `capitalizeStatus`. Three pure functions, zero tests. Raised in v2, still open. | L1 | 45m |
| PB-001 → [BILL-1211](https://zocdoc.atlassian.net/browse/BILL-1211) | Stripe webhook deduplication. Idempotency is bypassed in production and all four dedup tests are commented out — a replayed webhook could double-charge. | L3 | 1d |
| WEB-001 → [BILL-1217](https://zocdoc.atlassian.net/browse/BILL-1217) | Prorated subscription day-count. Untested, and the source's own comment says the math is wrong. | L1 | 4h |

### P1 — real user-visible failure, or material CI cost

| ID | What needs testing | Level | Est. |
|---|---|---|---|
| [FE-005](gaps/tickets/FE-005-zero-api-contract-tests.md) | That the billing endpoints return what the UI expects. **Zero** contract tests exist — no MSW, no nock. This is the empty L4 row. | L4 | 1d |
| [FE-004](gaps/tickets/FE-004-conditional-assertions-green-noops.md) | Six E2E tests wrap every assertion in `if (mock.find(...))`. One fixture change turns them into green tests that check nothing. Fix before trusting any E2E result. | L5 | 2h |
| [FE-006](gaps/tickets/FE-006-ach-no-e2e-coverage.md) | The ACH / bank-account payment path. `mockAchInfo` exists but no test ever selects the option that renders it. | L5 | 4h |
| WEB-002 → [BILL-1218](https://zocdoc.atlassian.net/browse/BILL-1218) | Tax amounts in `ProcessorGenerateChargeGroupsTest` — same cannot-fail pattern as FE-002, on tax. | L1 | 2h |
| WEB-003 → [BILL-1219](https://zocdoc.atlassian.net/browse/BILL-1219) | The bill generator. Its only test fixture is `[Ignore]`d, so it has no active tests at all. | L3 | 1d |

### P2 — meaningful, low blast radius

| ID | What needs testing | Level | Est. |
|---|---|---|---|
| [FE-009](gaps/tickets/FE-009-shift-19-e2e-tests-to-component-level.md) | 19 browser tests that mock everything — move them to component tests. Same coverage, ~100× faster. | L2 | 1d |
| [FE-010](gaps/tickets/FE-010-delete-39-redundant-e2e-tests.md) | 39 browser tests already covered by named component tests — delete. Do this **last**. | L5 | 1d |
| [FE-007](gaps/tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) | One empty test and four duplicates — delete. Zero coverage risk. | L5 | 45m |
| [FE-008](gaps/tickets/FE-008-move-geometry-assertions-to-visual-regression.md) | Three pixel assertions (`height === 68`) that keep browser tests alive purely for layout. Move to visual regression, don't delete. | L5 | 4h |
| [FE-012](gaps/tickets/FE-012-legacy-invoice-view-coverage.md) | `LegacyInvoiceView` coverage — it now renders unconditionally. **Do not delete it** (v2 said to; v2 was wrong). | L2 | 2h |
| [FE-011](gaps/tickets/FE-011-investigate-iframe-deprecation-flag.md) | `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` ramp state, then remove its dead test branches. | L2 | 2h |
| PB-002 → [BILL-1212](https://zocdoc.atlassian.net/browse/BILL-1212) | The hardcoded `ActualCost = 0` in the appointment event processor. | L1 | 2h |
| PB-004 → [BILL-1214](https://zocdoc.atlassian.net/browse/BILL-1214) | The billing-export **Generate** stage. Gather and Enrich each have an integration test; Generate has none. | L3 | 4h |

### P3 — polish

| ID | What needs testing | Level | Est. |
|---|---|---|---|
| [FE-013](gaps/tickets/FE-013-thirteen-source-files-with-no-coverage.md) | The 13 billing source files with no tests at all. | L2 | 1d |
| WEB-004 → [BILL-1220](https://zocdoc.atlassian.net/browse/BILL-1220) | What the 15 billing test files that opted out of the coverage gate actually leave uncovered. The output is a list of untested billing code, not a config change. | L1 | 4h |

---

## Start here Monday

| Ticket | Est. | Why this one |
|---|---|---|
| FE-003 | 45m | Pure functions, no mocking. Cheapest P0. |
| FE-002 | 45m | Turns a test that can't fail into one that can. |
| FE-007 | 45m | Deletes 5 tests, zero risk. |

Then **FE-001**. It's worth more than the entire 39-test deletion — the deletion saves CI minutes,
FE-001 prevents a revenue-path outage.

## One order that matters

Don't delete browser tests before adding the real one. Run FE-007 + FE-009 + FE-010 without FE-001
and billing ends up with essentially **one** test that exercises a multi-page journey — every
individual call correct, suite worse overall.

```
FE-004  (make the suite tell the truth — 6 tests pass vacuously today)
   ↓
FE-001  (add the one real test) · FE-008 (relocate pixel assertions)
   ↓
FE-007  (free wins) → FE-009 (move 19 down) → FE-010 (bulk delete, last)
```

`FE-001` before `FE-011` — FE-011 is a flag teardown of the same kind that changed the payment DOM on
2026-09-02 and broke a downstream suite while monorepo CI stayed green. FE-001 is the test that would
have caught it here.

Everything else is independent. Start any of it today.

## One warning

**Do not execute v2's #1 P0.** It says delete `LegacyInvoiceView` as dead code. It is **live** —
imported at `InvoiceDetailsContainer.tsx:16`, rendered at `:201`. Removing that flag made the legacy
branch permanent, not dead. Details in [`V2-VALIDATION.md`](V2-VALIDATION.md).

## Honest limitations

- **`provider-billing`'s 70 integration tests may never run.** They skip themselves when LocalStack
  is unavailable, and nobody confirmed LocalStack is provisioned in CI. If it isn't, that whole L3
  layer is reporting success without executing. Worth five minutes on the pipeline config before
  trusting the L3 numbers below.
- **PB-\* and WEB-\* rows link to Jira, not to files here.** Those tickets were filed from the
  backend analysis, but the per-ticket write-ups and the `provider-billing` / `zocdoc_web`
  inventories were never committed. The Jira ticket is the only detail that exists for them today.
- **No coverage tooling was run.** Counts come from reading test files. A test existing is not proof
  it asserts anything useful.
- **Runtime figures are estimates** unless labelled otherwise.
- Anything unconfirmable is written `UNVERIFIED — <what's needed>` rather than asserted.
- Findings are true as of `provider-fe-monorepo` `dd9e4952a6`, `provider-billing` `84318e3d5c`,
  `zocdoc_web` `8742b5072da` (2026-09-03/04).
