# SBX-002 — Make the billing specs safe to run in parallel (or enforce serialization)

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Bug |
| Priority | P1 |
| Test level | L5 e2e |
| Action | investigate |
| Repo | sandbox |
| Area | Provider-Billing — production E2E |
| Estimate | 4h |
| Labels | e2e, flakiness, test-isolation |
| Evidence revision | `eef9429d` (`origin/main`) |

## Summary
The billing specs all operate on the same production practice and mutate its payment methods, so
parallel workers delete each other's cards mid-test. Today this is survived by remembering to pass
`--workers=1`. Make the constraint enforced by the code, not by tribal knowledge.

## Context
`sandbox` runs against **production**. The billing specs add and remove real payment methods on a
real test practice, and call `cleanupBillingState()` to reset that practice to a baseline. Cleanup is
destructive and global to the practice.

## Current state
- Both billing specs authenticate as the same test account and operate on the same practice.
- Both call `cleanupBillingState(page, <billing email>)`, which removes payment methods for that
  practice.
- Playwright's default is parallel execution. Nothing in the specs declares
  `test.describe.configure({ mode: 'serial' })` or otherwise prevents two workers from running
  billing tests concurrently.
- The working practice is to pass `--workers=1` manually. That is a habit, not a guarantee — CI or a
  teammate running the suite without the flag hits the race.

## Why this matters
Two failure modes, and the second is worse:
1. **Flaky failures** — worker A deletes the card worker B just added; B fails on a missing element.
   Noisy but visible.
2. **False confidence** — a cleanup racing an assertion can leave a test passing for the wrong
   reason, or leave the production practice in a dirty state that makes the *next* run fail. Because
   this is production, the mess persists between runs.

Flaky billing E2E is also how teams learn to ignore billing E2E, which costs more than the flakes.

## Decision rule
Investigate which of these applies, then act:

| Finding | Action |
|---|---|
| The specs genuinely must share one practice | Enforce serialization **in code** — `test.describe.configure({ mode: 'serial' })` and/or a Playwright project-level `workers: 1` for the billing directory. Remove reliance on the CLI flag. |
| Separate test practices can be provisioned per spec | Give each spec its own practice/account. This is the better outcome — it restores parallelism and removes the shared-state class of bug entirely. |
| Cleanup can be scoped to only what the test created | Make `cleanupBillingState` remove only the payment methods that test added, rather than resetting the whole practice. |

## Acceptance criteria
- [ ] Determine whether additional billing test practices can be provisioned. Record the answer on
      the ticket — this is the deliverable.
- [ ] Implement whichever branch of the decision rule applies.
- [ ] The constraint is enforced by code or config, **not** by remembering a CLI flag. Running
      `npx playwright test <billing dir> --project=chromium` with default workers must be safe.
- [ ] Document the shared-practice constraint in `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md`
      so the next person does not rediscover it.
- [ ] Verification: run the billing specs with default workers, repeated — see below.

## Files
| Path | Change |
|---|---|
| `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | change — serialization or new practice |
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | change — same |
| `playwright/support/billing.ts` | change — scope `cleanupBillingState` if that branch is taken |
| `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` | change — document the constraint |

## Out of scope
Deduplicating the specs — that is SBX-001. Do SBX-001 first; it removes two of the racing tests and
may shrink this problem.

## Verification
```
npx playwright test playwright/BU/Provider/Acquisition/Provider-Billing/ --project=chromium --repeat-each=3
```
Run **without** `--workers=1`. Passing three times with default workers = the race is fixed rather
than avoided.

## Notes
Depends on SBX-001. Sequence: dedupe, then fix isolation on what remains.
