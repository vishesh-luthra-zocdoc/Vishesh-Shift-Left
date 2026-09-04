# FE-011 — Determine the `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` ramp state and remove its test branches

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P2 |
| Test level | L2 component |
| Action | investigate |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — feature flag cleanup |
| Estimate | 2h |
| Labels | shift-left, test-coverage, feature-flag, cleanup |
| Evidence revision | `dd9e4952a6` |

## Summary
`BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` reads like a fully-ramped kill switch that still carries
test branches on both sides. Confirm its ramp state, then delete the dead side — or leave it alone if
it is still live.

## Context
Billing Settings previously rendered payment entry in an iframe. This flag gates the deprecation of
that approach. Flags that are fully ramped but not torn down leave tests asserting both branches, and
the dead branch's tests are pure maintenance cost that also obscure which path actually ships.

## Current state
**Unresolved, and deliberately not asserted.** Ramp state cannot be determined from the code alone —
`apps/settings/src/ab/` was outside the analysis snapshot, so the flag's configuration was never read.

Raised by v2 as callout #5. Still unverified at `dd9e4952a6`, three months later.

## Why this matters
Two possibilities with opposite correct actions, which is exactly why this is an `investigate` and not
a `delete`:
- **Fully ramped** → the tests for the iframe path assert behaviour no user experiences. They are
  maintenance cost and a misleading signal.
- **Still ramping** → the tests are load-bearing and deleting them removes live coverage.

v2's #1 P0 made precisely this mistake in the other direction — it assumed a flag teardown had killed
a code path, and the path was actually made **permanent**. See [`../../V2-VALIDATION.md`](../../V2-VALIDATION.md).
That error is the reason this ticket exists in this form.

## Decision rule
| Finding | Action |
|---|---|
| Flag is fully ramped (100%) and the iframe path is unreachable | Tear down the flag; delete the iframe-path tests and the dead source. Cite the removed path in the PR. |
| Flag is fully ramped but the gated path became **unconditional** rather than dead | **Do not delete.** Remove the flag plumbing only, and confirm the now-permanent path has adequate coverage. This is the v2 failure mode. |
| Flag is still ramping or is an active kill switch | Leave both branches and their tests. Close this ticket with the ramp state recorded so it is not re-investigated. |

## Acceptance criteria
- [ ] Read the actual flag configuration (`apps/settings/src/ab/`, plus the AB tooling / experiment
      dashboard) and record the ramp percentage and whether it is a kill switch.
- [ ] Trace whether the gated code path is **unreachable** or merely **unconditional**. State which,
      with `file:line` evidence.
- [ ] Apply the matching branch of the decision rule.
- [ ] Record the ramp state on the ticket regardless of outcome — the answer is the deliverable.
- [ ] Verification: `yarn test .../billingSettings` passes; if source was removed, the app still builds.

## Files
| Path | Change |
|---|---|
| `apps/settings/src/ab/` | read only — the flag configuration (not previously analyzed) |
| `apps/settings/src/pages/settingsPages/billingSettings/**` | change — only if the teardown branch applies |

## Out of scope
Other billing flags. `SHOW_NEW_BILLING_MEZZ_REVAMP` and `billing_payment_element_flow` are already
torn down (`70a384854e`); `SHOULD_MOCK_STRIPE` is being handled by `dd9e4952a6`.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings
```
Plus a build if source was removed.

## Notes
Do **X-001 first.** This is a pending flag teardown of exactly the kind that broke the `sandbox`
suite on 2026-09-02. Landing the cross-repo tripwire before this teardown is the whole point of X-001.
