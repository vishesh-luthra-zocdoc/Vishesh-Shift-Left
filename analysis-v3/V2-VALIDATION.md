# v2 Callout Validation

Every actionable v2 callout, re-checked against `provider-fe-monorepo` @ `dd9e4952a6` (2026-09-03).
This is the file to read if you are about to act on anything in `analysis-v2/`.

**Headline: do not execute v2's P0 #1. It is wrong, and executing it deletes live coverage of a
live code path.**

---

## v2 P0 #1 — "Delete `LegacyInvoiceView` and its tests" — ❌ WRONG

**What v2 said:**
> `LegacyInvoiceView.tsx` + `LegacyInvoiceView-tests.tsx` … ~320 src + ~120 test.
> Commit **a88b14cba6** `chore(billing): tear down show_new_invoice_details_page feature flag`.
> **Action:** these tests reference a flag that no longer exists — they are safe to delete now.

v2 ranked this its #1 P0 and its top "Recommended Next Step" (30 min, "removes 120+ dead test lines").

**What is actually true:**

| Claim | Reality | Evidence |
|---|---|---|
| The component is dead | **Alive.** Imported and rendered on the non-FPB invoice path. | `InvoiceDetailsContainer.tsx:16` (import), `:201` (render) |
| The files are gone / removable | **Both still present on `main`.** `LegacyInvoiceView.tsx` is ~10 KB. | `git ls-tree origin/main` lists `LegacyInvoiceView.tsx` and `__tests__/LegacyInvoiceView-tests.tsx` |
| `a88b14cba6` tore it down | **That commit never touched it.** | `a88b14cba6` changed 6 files (+8/−44): `billing-settings-page-commands.ts`, `ab/experiments.ts`, `BillingSettingsContainer.tsx`, `BillsContainer.tsx`, `BillingSettingsContainer-tests.tsx`, `settingsExperimentsType.ts`. Neither `LegacyInvoiceView*` nor `InvoiceDetailsContainer.tsx` appears. |

**What `a88b14cba6` really did:** removed the `show_new_invoice_details_page` *experiment plumbing*
from `BillingSettingsContainer` and `BillsContainer`. The flag went away. The legacy view it once
gated did not — it became unconditionally reachable for non-FPB invoices.

**How the error happened:** v2 reasoned "flag torn down → the branch it gated is dead → the tests
for that branch are dead." The middle step was assumed, not checked. Removing a flag can just as
easily make a branch *permanent* as delete it, and here it made it permanent.

**Consequence had it shipped:** deleting `LegacyInvoiceView.tsx` breaks the non-FPB invoice render
for providers. Deleting only the test file silently strips the sole dedicated coverage from a live,
now-unconditional path.

**v3 action:** no deletion ticket. `LegacyInvoiceView` is live code; the correct question is whether
its coverage is adequate, not whether to remove it. This is also why v3 requires every `delete`
ticket to name the test that still covers the behaviour, and why an uncitable claim is downgraded to
`investigate` instead of asserted.

---

## v2 P0 #2 — `invoiceHelpers.ts` has no tests — ✅ STILL OPEN

Still untested at `dd9e4952a6`. v2 estimated 45 minutes; that remains right. Carried into v3 as a
P0 `add-coverage` ticket.

## v2 P1 #3 — `schemaBuilder.ts` tested only indirectly — ✅ STILL OPEN, AND WORSE THAN v2 THOUGHT

Still no direct tests. v2 counted 7 yup schemas; there are **5** at this revision.

The new finding is the more serious one. The single flag-related assertion that does exist is a
**tautology**: `EditMonthlyLimitModalV2-tests.tsx:129-133` computes its expected value with

```ts
const minimumMonthlyLimit = parseInt(
    getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500',
);
```

— the *same expression the source under test uses*. If the source's default were wrong, the test
would compute the identical wrong value and pass. It cannot fail for the reason it exists.
`maximumMonthlyLimit = 500000` (`utils/schemaBuilder.ts:101`) is asserted nowhere.

This raises v3's priority for `schemaBuilder.ts` above v2's: the gap is not "indirect coverage,
would be nice to firm up", it is "a monetary boundary guarded by a test that cannot detect a
regression."

## v2 P1 #4 — `AddPaymentMethodModal` (V1) untested — ⚠️ SUPERSEDED

The V1/V2 framing is obsolete. Payment-method entry has since been reorganised around the unified
Payment Element in `shared/core`. v3 replaces this callout with the seam gap below.

## v2 P2/P3 — presentational components (`BusinessAddress`, `BillingEmail`, `BillStatusLabel`) — ✅ STILL OPEN, STILL P3

Unchanged and still correctly low priority.

## v2 P2 #6 — "`billing-settings-page-tests.ts` (1,254 lines) may be redundant" — ✅ CORRECT, AND DONE

v2's line count was exactly right (verified: 1,254 at `b730e8aafb`). The cleanup happened — the file
was **1,254 → 179 lines** by 2026-07-06, before the Playwright port. Closed. Not re-raised.

## v2 #5 — audit `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` — 🔶 STILL OPEN, UNVERIFIED

Still unresolved. It reads like a fully-ramped kill switch still carrying test branches, but ramp
state cannot be determined from code (`apps/settings/src/ab/` was outside the analysis snapshot).
Carried into v3 as an `investigate` ticket with an explicit decision rule rather than an assertion.

## v2's shift-left plan — ⚠️ OBSOLETE IN FORM, DIRECTIONALLY RIGHT

v2's per-test Cypress→Jest classification targets a framework that no longer exists: the billing
specs were ported to Playwright in `0561a881ee` (2026-07-06, #11242) and Cypress was removed.

v2's *direction* was right and its warning was prescient — it flagged that Cypress was growing
faster than unit coverage (+210% vs +38%) and that "shift-left pressure is increasing, not
decreasing." That trend continued: the migration **grew** billing E2E 32% (2,302 → 3,049 lines).
The rewrite was the cheapest possible moment to drop browser tests that didn't need a browser, and it
wasn't taken.

---

## Scorecard

| v2 callout | Verdict |
|---|---|
| P0 #1 `LegacyInvoiceView` deletion | ❌ **Wrong — do not execute** |
| P0 #2 `invoiceHelpers.ts` | ✅ Still open, correctly flagged |
| P1 #3 `schemaBuilder.ts` | ✅ Still open, under-prioritised by v2 |
| P1 #4 `AddPaymentMethodModal` V1 | ⚠️ Superseded by the core extraction |
| P2 #6 V1 Cypress spec redundancy | ✅ Correct, and resolved by the team |
| P2/P3 presentational components | ✅ Still open, correctly low priority |
| #5 `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` | 🔶 Still open, still unverified |
| Shift-left plan | ⚠️ Obsolete in form, right in direction |

**One wrong out of eight, but it was v2's top-priority item** — and the failure mode is the
dangerous direction: it recommended *removing* something on an unverified inference. Gaps that turn
out to be non-gaps cost a little wasted effort; deletions that turn out to be live code cost an
outage. Hence v3's citation rule for every `delete` ticket.

## What v2 could not have known

Not errors — the codebase moved after v2 ran. Recorded so the delta is attributable:

- Cypress removed monorepo-wide; billing specs ported to Playwright (`0561a881ee`, 2026-07-06).
- Billing payment code extracted into `shared/core`, splitting coverage across an app/shared
  boundary that did not exist in v2.
- `billing_payment_element_flow` torn down (`70a384854e`, 2026-09-02), deleting
  `billing-settings-v2-upgraded-stripe.spec.ts` and making Payment Element the only path.
- `provider-billing` — a whole service repo with five test projects — was never in v1/v2 scope.
