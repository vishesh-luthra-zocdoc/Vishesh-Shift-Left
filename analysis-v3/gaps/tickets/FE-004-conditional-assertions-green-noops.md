# FE-004 — Fix six E2E tests whose assertions are entirely inside `if (mock.find(...))`

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Bug |
| Priority | P1 |
| Kind of test | Browser test |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — E2E suite integrity |
| Estimate | 2h |
| Labels | shift-left, test-coverage, e2e, false-green |
| Evidence revision | `dd9e4952a6` |

## Summary
Six tests in `billing-settings-v2.spec.ts` wrap every assertion in `if (mock.find(...))`. If the
lookup returns `undefined`, the test passes having asserted nothing. This ticket makes them fail
loudly instead.

## Current state
`apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts` — six tests at lines
**`:191`, `:241`, `:288`, `:349`, `:425`, `:759`** guard their assertions behind a `mock.find(...)`
lookup on fixture data. No `expect` runs on the miss path, and nothing asserts the lookup succeeded.

## Why this matters
A test that cannot fail is worse than a missing test: a missing test is visible in a coverage gap,
while this reports success. One fixture rename turns all six green-and-empty, and the next person to
read the suite sees six passing tests covering behaviour nobody is checking.

These six sit in the same suite the team is about to shrink (FE-009, FE-010). Deciding what to delete
based on a suite containing silent no-ops means deleting the wrong things.

## Acceptance criteria
- [ ] For each of the six tests, either:
      **(a)** assert the fixture lookup succeeded before using it (e.g. `expect(found).toBeDefined()`)
      so a fixture change fails the test, or
      **(b)** delete the test if its assertions are already covered at the component level — citing the covering test
      by file and `it` title, per the `delete` rule.
- [ ] No `expect` in these specs remains reachable only inside an unasserted conditional.
- [ ] A deliberate fixture rename causes a **failure**, not a pass. Record this check on the ticket.
- [ ] Verification: `yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts` passes, and the sabotage check above fails.

## Test cases to write
Not new tests — repairs. One row per site:

| # | Location | Action |
|---|---|---|
| 1 | `billing-settings-v2.spec.ts:191` | Assert lookup, or delete citing component-test cover |
| 2 | `billing-settings-v2.spec.ts:241` | Assert lookup, or delete citing component-test cover |
| 3 | `billing-settings-v2.spec.ts:288` | Assert lookup, or delete citing component-test cover |
| 4 | `billing-settings-v2.spec.ts:349` | Assert lookup, or delete citing component-test cover |
| 5 | `billing-settings-v2.spec.ts:425` | Assert lookup, or delete citing component-test cover |
| 6 | `billing-settings-v2.spec.ts:759` | Assert lookup, or delete citing component-test cover |

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts` | change — 6 sites |

## Out of scope
Shifting these tests to the component level (FE-009) or deleting the redundant bulk (FE-010). This ticket only makes
the suite tell the truth so those decisions rest on real signal.

## Verification
```
yarn playwright test apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts
```
Then sabotage-check: rename the fixture key the `find` depends on. Before this ticket the suite stays
green; after, it must fail.

## Notes
Do this **before** FE-009/FE-010. It is cheap and it changes what those tickets should conclude.
