# Orchestrator Judgment — The Monorepo E2E Shift-Left Plan

**Repo:** `provider-fe-monorepo` @ `dd9e4952a6`
**Underlying data:** [`../analysis-scratch/e2e-shift-left-candidates.md`](../analysis-scratch/e2e-shift-left-candidates.md)

The per-test classification is sound and its citations are real — I independently verified a sample
(see [Verification](#verification-performed) below). But the aggregate recommendation needs a
guard rail before it becomes tickets, and that guard rail is the point of this file.

---

## The raw recommendation

| Verdict | Count | Share |
|---|---|---|
| `keep-e2e` | 5 | 7.9% |
| `shift-to-L2` | 19 | 30.2% |
| `delete-redundant` | 39 | 61.9% |
| `shift-to-L1` / `shift-to-L3` / `delete-suspected` | 0 | — |
| **Total** | **63** | |

Taken literally: delete 39 tests, move 19 down to L2, keep 5.

## Why the raw number is defensible

Every one of the 63 tests **mocks its entire backend** — 13 REST endpoints stubbed, auth stubbed,
`/login/*` deliberately 500'd, and Stripe.js replaced by a fake installed unconditionally for every
test in the directory (`e2e/fixtures.ts:32`). Nothing in this suite talks to a real dependency.

That means the suite currently provides **no integration confidence to lose**. It pays L5 cost —
browser boot, page load, 60 s timeouts, serial execution on CI
(`apps/settings/playwright.config.ts:13-14`: `retries: isCI ? 1 : 0`, `workers: isCI ? 1 :
undefined`) — for assertions a jsdom render could make in milliseconds. Deleting a mocked browser
test that duplicates a named L2 test genuinely loses nothing.

## Why it should not be executed as stated

**The `keep-e2e` floor is too thin, and it is thin in the wrong way.** Of the 5 kept:

| Test | Kept because | Is that integration value? |
|---|---|---|
| `billing-invoice-summary.spec.ts:297` | Reads `boundingBox()` y-coordinates to assert row ordering | No — layout geometry |
| `payment-recovery.spec.ts:156` | Asserts real toast geometry (`overflow === 0`, `height === 68`) | No — layout geometry |
| `payment-recovery.spec.ts:233` | Asserts `scrollTop === 0` when content overflows (BILL-1083) | No — layout geometry |
| `payment-recovery.spec.ts:96` | Full money-recovery journey across a page transition | **Yes** |
| `billing-settings-payment-element.spec.ts:44` | Add-payment-method submit flow | Partly — but the agent notes its assertions *are* duplicated by `AddPaymentMethodElementModal-tests.tsx` |

So after the shift-left, **one test** (`payment-recovery.spec.ts:96`) would exercise a multi-page
billing journey, and three of the five survivors are really visual-regression assertions wearing
E2E clothing. Nothing would verify that the billing settings page loads, wires its components
together, and survives a real data payload.

That is a worse suite than the one we started with, even though it is cheaper and every individual
verdict was correct. The plan optimises each test in isolation and degrades the whole.

## Recommended sequencing

Do not ship this as one "delete 39 tests" ticket. Three ordered phases:

**Phase 1 — free wins, no coverage risk (do first, independently).**
The subset that costs nothing to remove because it asserts nothing or is self-evidently duplicated:
- `billing-settings-v2.spec.ts:175` — **verified empty body**, zero assertions, title copy-pasted
  from `:56`. Deleting it cannot reduce coverage.
- The 6 tests whose assertions are entirely wrapped in `if (mock.find(...))`
  (`:191, :241, :288, :349, :425, :759`) — one fixture edit turns these into green no-ops, so they
  are worse than absent: they report success without testing. Fix or delete.
- The 4 intra-suite duplicates (6.3% of the suite).

**Phase 2 — establish the floor before removing anything else.**
Add the integration coverage that does not exist today, at the right level:
- One genuine L5 smoke: billing settings page loads against a **real** backend and a **real**
  Stripe Payment Element mounts. Nothing at any level proves this today — see the uncovered-journey
  finding below.
- Promote the three geometry assertions out of the functional suite. Layout/visual assertions
  belong in a visual-regression check, not mixed into functional E2E where they are the sole
  justification for keeping a test alive.

**Phase 3 — execute the bulk deletion and the 19 L2 shifts.**
Only after Phase 2 lands. Each L2 shift ticket must land the L2 test **before** removing the E2E
test, in that order, not the reverse.

## The gap that dominates everything above

**Adding a payment method against a real Stripe and a real backend is untested at every level.**
Nothing in the monorepo proves a real Payment Element mounts, validates a card, handles a decline
or 3DS, or that a saved method persists. A Stripe.js version bump, a publishable-key
misconfiguration, or a CSP change breaks card entry in production **with all 63 tests green**.

Two related holes:
- **ACH / bank-account add has zero E2E coverage.** `mockAchInfo` exists, but the one option that
  renders it is never selected by any spec.
- **The recovery charge is stubbed to success**, so no test at any level proves money moved.

Closing this is worth more than the entire 39-test deletion. The deletion saves CI minutes; this
prevents a revenue-path outage. Ticket priority is set accordingly.

## Verification performed

I spot-checked the highest-risk claims rather than trusting the classification wholesale, because a
wrong `delete-redundant` silently removes real coverage:

| Claim | Result |
|---|---|
| `billing-settings-v2.spec.ts:175` has an empty body | **Confirmed** — `:175-179` is a lone `setUpRoutesAndVisitBillingPage(page, practiceId, {})` call, no assertions |
| Cited covering test `PaymentMethodV2-tests.tsx` `it('calls setDefaultPaymentMethod API on "Set as default" click')` exists | **Confirmed** — `PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-tests.tsx:605` |
| Cited covering test `it('opens EditMonthlyLimitModal on "Set limit" click')` exists | **Confirmed** — same file, `:801` |

Citations are real and re-checkable, and zero verdicts were `delete-suspected`, which is the
category reserved for uncitable claims. The classification can be trusted at row level.

**One residual caveat that applies to the whole `delete-redundant` set:** the covering L2 tests
prove a component *fires* an API call. They do not prove the page wires that component to anything.
For any single test that distinction is immaterial; across 39 deletions it is exactly the erosion
Phase 2 exists to prevent.
