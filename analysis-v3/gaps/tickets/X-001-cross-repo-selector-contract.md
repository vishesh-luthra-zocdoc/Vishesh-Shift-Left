# X-001 — Prevent monorepo DOM changes from silently breaking the sandbox suite

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P0 |
| Test level | L5 e2e |
| Action | add-coverage |
| Repo | cross-repo (`provider-fe-monorepo` + `sandbox`) |
| Area | Billing — cross-repo test contract |
| Estimate | 1d |
| Labels | shift-left, e2e, cross-repo, ci |
| Evidence revision | `provider-fe-monorepo` `dd9e4952a6`; `sandbox` `eef9429d` |

## Summary
A feature-flag teardown in `provider-fe-monorepo` changed the billing DOM and broke `sandbox`'s
billing suite the same day, with nothing connecting the two repos. This ticket adds the missing link
so the next teardown is caught before it lands.

## Context
`provider-fe-monorepo` builds the Billing Settings UI. `sandbox` runs Playwright against the deployed
result on production, selecting elements by `data-test` attributes. The coupling between them is real
but entirely implicit: no shared package, no contract, no CI signal.

## Current state — the incident, verified
| Date | Repo | Event |
|---|---|---|
| 2026-09-02 | `provider-fe-monorepo` | `70a384854e` (#12032) `refactor(settings): tear down billing_payment_element_flow`. Made the Stripe Payment Element the only path; **changed the rendered DOM**. Also deleted `billing-settings-v2-upgraded-stripe.spec.ts`. |
| 2026-09-02 | `sandbox` | Billing specs, which target that DOM against production, went red. |
| 2026-09-04 | `sandbox` | Fix merged: `eef9429d` (#2593) `fix: repoint billing add-payment-method helpers at Stripe Payment Element`. |

The monorepo's own E2E suite stayed green throughout — it mocks Stripe entirely
(`apps/settings/e2e/fixtures.ts:32`), so it could not detect a change in real payment DOM.

**Nothing failed in the repo that made the change.** The breakage surfaced in a different repo, owned
by a different workflow, and was diagnosed by hand.

## Why this matters
This is the structural finding of the v3 analysis, not just an incident report. The same mechanism
will fire on the next flag teardown, component rename, or `data-test` change — and billing has
several flags still pending teardown (e.g. `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION`, FE-011).

The failure mode is the dangerous one: the repo making the change gets a green build. Detection is
delayed until someone notices a red suite elsewhere and correlates it manually. In the meantime the
production billing path is unverified.

## Acceptance criteria
Pick **one** primary mechanism — do not build all three:

- [ ] **Option A (preferred): a shared selector contract.** The `data-test` attributes `sandbox`
      depends on are declared in one place that `provider-fe-monorepo` consumes. Removing or renaming
      one fails the monorepo's build or tests, in the monorepo's own CI.
- [ ] **Option B: a post-deploy canary.** A minimal `sandbox` billing smoke runs automatically after
      a monorepo settings deploy, and alerts the billing channel on failure. Catches the break in
      minutes rather than by chance.
- [ ] **Option C: a codeowners tripwire.** Changes to billing components or their `data-test`
      attributes require review from the `sandbox` billing owner. Cheapest, weakest — a fallback if A
      and B are blocked.
- [ ] Whichever is chosen: **prove it works** by reverting `70a384854e` locally (or simulating an
      equivalent `data-test` rename) and confirming the mechanism fires.
- [ ] Cross-repo ownership documented in both places:
      `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` (`sandbox`) and the billing
      area of `provider-fe-monorepo`.

## Test cases to write
| # | Scenario | Expected |
|---|---|---|
| 1 | Rename a `data-test` attribute `sandbox` depends on | Monorepo CI fails (A) or canary alerts (B) |
| 2 | Tear down a billing feature flag that changes payment DOM | Same |
| 3 | A DOM change `sandbox` does **not** depend on | **No** false alarm |

Case 3 matters as much as case 1. A tripwire that fires on every DOM change gets disabled within a
month.

## Files
| Path | Change |
|---|---|
| `provider-fe-monorepo` — billing components | change — consume the shared contract (Option A) |
| `sandbox` — `playwright/support/billing.ts` | change — consume the shared contract |
| CI config in one or both repos | change — canary wiring (Option B) |
| `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` | change — cross-repo ownership |

## Out of scope
Extending the mechanism beyond billing. Prove it on billing — the area with a known, dated incident —
then generalize if it earns its keep.

## Verification
Simulate the break (revert `70a384854e` or rename a depended-on `data-test`) and confirm the
mechanism fires **in the repo making the change**. That last part is the whole point: a signal that
only appears in `sandbox` is what we already have.

## Notes
- Relates to FE-001: if the monorepo had one E2E test using a **real** Stripe Element, this specific
  break would likely have been caught in-repo. FE-001 and this ticket attack the same gap from two
  directions, and both are worth doing.
- FE-011 (`BILLING_PAGE_ENABLE_IFRAME_DEPRECATION`) is a **pending teardown** of exactly the kind
  that caused this incident. Landing X-001 before FE-011 is the natural order.
