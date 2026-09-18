# Verified History — What Actually Happened Between v2 and v3

Every line here was verified against `~/provider-fe-monorepo` git history. Commit SHAs are real
and re-checkable. This file exists because v2's recommendations were written against a codebase
that then changed underneath them, and it matters to know *which* recommendations the team acted
on versus which were made irrelevant by something else.

---

## The billing E2E timeline

| Date | Commit | What happened |
|---|---|---|
| 2026-04-23 | `b730e8aafb` (tree at v2 run) | v2 analysis snapshot. `billing-settings-page-tests.ts` = **1,254 lines** — v2's figure is confirmed exactly right. |
| Apr 23 → Jul 6 | — | That same file shrank **1,254 → 179 lines** (−1,075). See "v2's biggest recommendation" below. |
| 2026-07-06 | `0561a881ee` (#11242) | **The billing Cypress → Playwright migration.** `test(settings): migrate PracticeSettingsPages + Sync feature E2E to Playwright`. |
| 2026-09-02 | `70a384854e` (#12032) | `refactor(settings): tear down billing_payment_element_flow`. Deleted `billing-settings-v2-upgraded-stripe.spec.ts`; Payment Element became the only path. |
| 2026-09-03 | `dd9e4952a6` (#12074) | `refactor(billing): move the Stripe.js mock out of production code`. The v3 analysis revision. |
| (later) | `e44f4ff75f` | `chore: remove cypress e2e infra monorepo-wide (jsplat-759)`. Removed the *remaining framework scaffolding*, not the billing specs. |

**Correction to my own earlier statement:** I initially attributed the billing Cypress removal to
`e44f4ff75f`. That commit removed the leftover Cypress *infrastructure* monorepo-wide. The billing
specs themselves were migrated two months earlier in `0561a881ee`. The distinction matters: the
migration was a deliberate, reviewed port (#11242), not a side effect of an infra cleanup.

## v2's biggest recommendation: the team did it

v2 said "check `SHOW_NEW_BILLING_MEZZ_REVAMP` rollout — may allow deleting 1,254 lines of V1
Cypress spec", and flagged it as the single largest cleanup on the table.

**That cleanup happened.** `billing-settings-page-tests.ts` went from 1,254 lines (Apr 23) to 179
lines with 7 `it` blocks by the time of the migration (Jul 6) — a 1,075-line reduction, before the
Playwright port even started. v2 called this correctly and someone acted on it. It is closed, and
v3 should not re-raise it.

## The Cypress → Playwright migration did not shrink the suite — it grew it 32%

Measured across all billing files in `0561a881ee`:

| | Cypress (before) | Playwright (after) | Δ |
|---|---|---|---|
| `billing-settings-page` spec | 179 | 214 | +35 |
| `billing-settings-v2` spec | 893 | 1,132 | +239 |
| `billing-invoice-summary` spec | 203 | 269 | +66 |
| `billing-pricing-v2` spec | 234 | 292 | +58 |
| `billing-settings-v2-upgraded-stripe` spec | 278 | 361 | +83 |
| `invoice-details-page` spec | 42 | 58 | +16 |
| `billing-settings-page-commands` | 343 | 538 | +195 |
| `EditBillingContactInfoModalPageObject` | 130 | 185 | +55 |
| **Total** | **2,302** | **3,049** | **+747 (+32%)** |

A framework migration is the cheapest moment to drop coverage that shouldn't be at L5 — the tests
are already being rewritten line by line. That opportunity was not taken; the suite was ported
faithfully and grew. This is why v3's shift-left backlog is large: the debt was carried forward
intact and then added to.

## Current billing E2E state at `dd9e4952a6` (verified counts)

| Spec | Tests | Lines |
|---|---|---|
| `billing-invoice-summary.spec.ts` | 20 | 348 |
| `billing-settings-v2.spec.ts` | 16 | 1,032 |
| `billing-pricing-v2.spec.ts` | 11 | 292 |
| `billing-settings-page.spec.ts` | 7 | 214 |
| `billing-settings-payment-element.spec.ts` | 4 | 143 |
| `payment-recovery.spec.ts` | 4 | 291 |
| `invoice-details-page.spec.ts` | 1 | 60 |
| **7 specs** | **63** | **2,380** |
| plus `billing-settings-page-commands.ts` | — | 562 |
| plus 2 page objects | — | 231 |
| **Total billing E2E footprint** | **63 tests** | **3,173 lines** |

## Cross-repo root cause: a monorepo change that could not fail in the monorepo

`70a384854e` (2026-09-02) tore down the `billing_payment_element_flow` flag in
`provider-fe-monorepo`, making the Stripe Payment Element the only code path and changing the
rendered DOM. The downstream Playwright billing specs that target that DOM on production went red the
same day. They were repointed downstream on 2026-09-04 (`eef9429d`, #2593) — as of `dac52b65` that
fix was still on a branch, not yet on `origin/main` `4bb607cc`.

This is the structural finding, not the incident: **monorepo CI could not fail on a monorepo change**,
because it mocks Stripe entirely and cannot see real payment DOM. The break surfaced in a different
repo, on a different workflow, and was diagnosed by hand. Nothing was changed in the monorepo, so it
will recur on the next teardown. The fix (X-001) is monorepo-side, which is why it is in scope here
even though the red suite was not.

## Corrections to subagent findings

| Claim | Status | Evidence |
|---|---|---|
| "`SHOULD_MOCK_STRIPE` is set by 6 specs and consumed nowhere" | **Wrong — it is consumed by production code** | `AddPaymentMethodModalV2/CreditCardFormContentV2.tsx:52` and `AddPaymentMethodModalV2/AchFormContentV2.tsx:69` both read it. The agent's snapshot did include these files. |
| "1,254 lines — UNVERIFIED, no `.git` in snapshot" | **Verified correct** | `git show b730e8aafb:…/billing-settings-page-tests.ts \| wc -l` → 1254 |
| "File header claims a port of a 19-test Cypress spec; 16 exist — UNVERIFIED" | Partially resolved | The pre-migration Cypress `billing-settings-v2-tests.ts` was 893 lines. Exact `it` count at `0561a881ee^` still worth confirming if the discrepancy matters. |
| "Runtime 10–16 min serial (estimate)" | Basis now confirmed | `apps/settings/playwright.config.ts:13-14` sets `retries: isCI ? 1 : 0` and `workers: isCI ? 1 : undefined` — CI genuinely runs these **serially**, so the serial estimate is the CI-relevant one. |

### The `SHOULD_MOCK_STRIPE` finding is more interesting than the agent's version

It is not dead config. Production components read a test-only cookie and branch on it, which means
the E2E suite's green path executes a code path that real users never take. The most recent commit
on the branch — `dd9e4952a6` `move the Stripe.js mock out of production code` — is the team already
working on exactly this. v3 should reinforce that direction rather than open a competing ticket.
