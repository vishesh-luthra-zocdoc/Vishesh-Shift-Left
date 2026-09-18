# X-001 — Make a billing DOM change fail in the repo that made it

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Story |
| Priority | P0 |
| Test level | L5 e2e |
| Action | add-coverage |
| Repo | `provider-fe-monorepo` (the fix lands here) |
| Area | Billing — cross-repo test contract |
| Estimate | 1d |
| Labels | qa-shift-left, e2e, test-coverage |
| Evidence revision | `provider-fe-monorepo` `dd9e4952a6` |

## Summary
A feature-flag teardown in `provider-fe-monorepo` changed the billing DOM. The downstream Playwright
suite that drives that DOM on production went red the same day, while monorepo CI stayed green. This
ticket adds the missing signal **in the monorepo**, so the next teardown fails where it's made.

**Scope note:** the downstream suite is QA-owned and out of scope for this analysis. This ticket is
in scope because the entire deliverable is monorepo-side — a monorepo change should not be able to
break the billing DOM without failing monorepo CI, regardless of who runs tests downstream.

## Context
`provider-fe-monorepo` builds the Billing Settings UI. A downstream Playwright suite runs against the
deployed result on production, selecting elements by `data-test` attributes. The coupling is real but
entirely implicit: no shared package, no contract, no CI signal.

## Current state — the incident, verified
| Date | Repo | Event |
|---|---|---|
| 2026-09-02 | `provider-fe-monorepo` | `70a384854e` (#12032) `refactor(settings): tear down billing_payment_element_flow`. Made the Stripe Payment Element the only path; **changed the rendered DOM**. Also deleted `billing-settings-v2-upgraded-stripe.spec.ts`. |
| 2026-09-02 | downstream | The Playwright billing specs that target that DOM on production went red. |
| 2026-09-04 | downstream | Selectors repointed: `eef9429d` (#2593) `fix: repoint billing add-payment-method helpers at Stripe Payment Element`. Nothing changed in the monorepo. |

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

- [ ] **Option A (preferred): a declared selector contract.** The `data-test` attributes anything
      downstream depends on are declared in one place in `provider-fe-monorepo`. Removing or renaming
      one fails the monorepo's own build or tests.
- [ ] **Option B: a post-deploy canary.** A minimal billing smoke runs automatically after a
      monorepo settings deploy and alerts the billing channel on failure. Catches the break in
      minutes rather than by chance. Needs the QA repo owner's agreement on where it runs.
- [ ] **Option C: a codeowners tripwire.** Changes to billing components or their `data-test`
      attributes require review from the downstream billing test owner. Cheapest, weakest — a
      fallback if A and B are blocked.
- [ ] Whichever is chosen: **prove it works** by reverting `70a384854e` locally (or simulating an
      equivalent `data-test` rename) and confirming the mechanism fires.
- [ ] The set of `data-test` attributes treated as a public contract is written down in the billing
      area of `provider-fe-monorepo`, so a future author knows which ones are load-bearing.

## Test cases to write
| # | Scenario | Expected |
|---|---|---|
| 1 | Rename a `data-test` attribute the downstream suite depends on | Monorepo CI fails (A) or canary alerts (B) |
| 2 | Tear down a billing feature flag that changes payment DOM | Same |
| 3 | A DOM change nothing downstream depends on | **No** false alarm |

Case 3 matters as much as case 1. A tripwire that fires on every DOM change gets disabled within a
month.

## Files
| Path | Change |
|---|---|
| `provider-fe-monorepo` — billing components | change — declare the selector contract (Option A) |
| `provider-fe-monorepo` — CI config | change — contract check or canary wiring |
| `provider-fe-monorepo` — billing README / ownership doc | change — record which selectors are load-bearing |

Downstream repo changes, if any are needed to consume the contract, are the QA repo owner's to make
and are tracked separately.

## Out of scope
Extending the mechanism beyond billing. Prove it on billing — the area with a known, dated incident —
then generalize if it earns its keep.

## Verification
Simulate the break (revert `70a384854e` or rename a depended-on `data-test`) and confirm the
mechanism fires **in the repo making the change**. That last part is the whole point: a signal that
only appears downstream is what we already have.

## Notes
- Relates to FE-001: if the monorepo had one E2E test using a **real** Stripe Element, this specific
  break would likely have been caught in-repo. FE-001 and this ticket attack the same gap from two
  directions, and both are worth doing.
- FE-011 (`BILLING_PAGE_ENABLE_IFRAME_DEPRECATION`) is a **pending teardown** of exactly the kind
  that caused this incident. Landing X-001 before FE-011 is the natural order.
- Option B needs a conversation with the QA repo owner before it's picked; Option A does not.
