# Summary — What's Actually Missing

Plain language. Technical detail is one click away in each linked ticket.

**New here? Read [`START-HERE.md`](START-HERE.md) instead** — it's one page and it tells you what to
test, at what priority, and what to do first. This file is the same findings in prose.

**Scope:** pre-release tests in team-owned repos (`provider-fe-monorepo`, `provider-billing`,
`zocdoc_web`). The QA-owned `sandbox` repo is out of scope.

---

## The four things that matter

### 1. Adding a payment method is untested against a real Stripe — at every level
All 63 frontend billing E2E tests install a **fake Stripe.js** for the whole directory
(`apps/settings/e2e/fixtures.ts:32`). All 13 backend endpoints are stubbed. Nothing, anywhere, proves
a real Payment Element mounts, validates a card, or handles a decline.

A Stripe.js bump, a bad publishable key, or a CSP change breaks card entry in production **with all
63 tests green**. ACH has no E2E coverage at all — `mockAchInfo` exists but no spec ever selects the
option that renders it. → **[FE-001](gaps/tickets/FE-001-real-stripe-payment-element-untested.md)**,
**[FE-006](gaps/tickets/FE-006-ach-no-e2e-coverage.md)**

### 2. There are zero API contract tests
Not thin — **zero**. No MSW, no `nock`, nothing. The frontend mocks what it *believes* each endpoint
returns, and nobody checks that belief against the real services.

When a backend renames a field, **nothing in the frontend fails.** 856 unit/component tests and 63
E2E tests all stay green; the break surfaces on the billing page in front of providers.
→ **[FE-005](gaps/tickets/FE-005-zero-api-contract-tests.md)**

### 3. The E2E suite does L2 work at L5 cost
63 tests, 3,173 lines, and CI runs them on **one worker** (`playwright.config.ts:14`) at up to 60s
each. Every single one mocks its whole backend — so there is no integration confidence to lose.

Of the 5 tests worth keeping, **3 are kept only for pixel measurements** (`height === 68`,
`scrollTop === 0`, `boundingBox()` ordering). Exactly **one** test exercises a multi-page journey.

Six more tests wrap all their assertions in `if (mock.find(...))` — one fixture change turns them into
green no-ops that report success while testing nothing.
→ **[FE-004](gaps/tickets/FE-004-conditional-assertions-green-noops.md)**,
**[FE-007](gaps/tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md)**–**[FE-010](gaps/tickets/FE-010-delete-39-redundant-e2e-tests.md)**

### 4. A flag teardown in one repo silently broke another repo
2026-09-02: `70a384854e` tore down `billing_payment_element_flow` in `provider-fe-monorepo`, changing
the payment DOM. The downstream Playwright suite that targets that DOM against production went red
the same day. Fixed downstream 2026-09-04 (`eef9429d`, #2593) — but nothing was fixed in the
monorepo, which is where the change originated.

**The monorepo's own CI stayed green**, because it mocks Stripe and cannot see real payment DOM.
Nothing made the breaking change fail where it was made: no canary, no shared selector contract, no
ownership link. **The fix for this is monorepo-side**, which is why it's in scope here. It will
recur on the next teardown — and **[FE-011](gaps/tickets/FE-011-investigate-iframe-deprecation-flag.md)**
is a pending teardown of exactly that kind.

**No ticket is filed for this.** The fix is a CI tripwire, and this analysis covers tests, not CI
wiring — see "Dropped from scope" in [`gaps/BACKLOG.md`](gaps/BACKLOG.md). The *test* that would have
caught this break in the monorepo is **[FE-001](gaps/tickets/FE-001-real-stripe-payment-element-untested.md)**,
which is filed. It's recorded here because it explains why FE-001 is worth more than its estimate
suggests.

---

## The one-line version of the whole analysis

Two tests in the same folder, two months apart:

```ts
// YearlyValueCalcModalV2-tests.tsx:224  — CAN catch a money bug
// result = (7/10) * (245 + 2*247*(45/100)) = 327.11
expect(resultText).toBe('$327');          // ← worked out by hand

// EditMonthlyLimitModalV2-tests.tsx:129  — CANNOT catch a money bug
const minimumMonthlyLimit = parseInt(
  getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500');
                                          // ← the source's own expression
```

The second computes its expectation using **the exact code it is testing**. If the source default were
wrong, the test computes the same wrong value and passes. It cannot fail for the reason it exists.
`maximumMonthlyLimit = 500000` is asserted **nowhere**.
→ **[FE-002](gaps/tickets/FE-002-monthly-limit-tautological-test.md)**

## What the team already fixed

Credit where due — see [`ALREADY-FIXED.md`](ALREADY-FIXED.md):

- **The revenue-calculator P0 is closed.** BILL-748 + BILL-962 added **34 tests**, and the money
  assertion is the good non-tautological kind. (Not BILL-196 — that was the feature commit.)
- **v2's biggest recommendation shipped:** `billing-settings-page-tests.ts` went 1,254 → 179 lines.
- **505 lines of dead V1 calculator code removed** alongside the tests — the right pattern.
- **In progress:** moving the Stripe mock out of production code (`dd9e4952a6`).

## One warning

**Do not execute v2's #1 P0.** It says delete `LegacyInvoiceView` as dead code. It is **live** —
imported at `InvoiceDetailsContainer.tsx:16`, rendered at `:201`. The commit v2 blamed never touched
it; removing that flag made the legacy branch **permanent, not dead**. Executing it breaks invoice
rendering for providers. → [`V2-VALIDATION.md`](V2-VALIDATION.md),
**[FE-012](gaps/tickets/FE-012-legacy-invoice-view-coverage.md)**

## By the numbers — `provider-fe-monorepo` billing

| Level | Files | Tests |
|---|---|---|
| L1 unit | 34 | 224 |
| L2 component | 45 | 515 |
| L2 hooks | 9 | 47 |
| L3 integration | 2 | 70 |
| **L4 api** | **0** | **0** |
| L5 e2e | 7 | 63 |

152 source files · 88 with coverage · 64 with no direct test · **13 with no coverage at all**


## Where to start Monday

| Ticket | Est. | Why |
|---|---|---|
| [FE-003](gaps/tickets/FE-003-invoice-helpers-untested.md) | 45m | Pure functions, no mocking. Cheapest P0. |
| [FE-002](gaps/tickets/FE-002-monthly-limit-tautological-test.md) | 45m | Turns a test that can't fail into one that can. |
| [FE-007](gaps/tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) | 45m | Deletes 5 tests, zero coverage risk. |

Then **FE-001** — it is worth more than the entire 39-test deletion. The deletion saves CI minutes;
FE-001 prevents a revenue-path outage.
