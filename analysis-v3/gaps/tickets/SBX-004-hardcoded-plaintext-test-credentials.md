# SBX-004 — Move hardcoded plaintext test-account passwords out of the billing specs

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Bug |
| Priority | P1 |
| Test level | L5 e2e |
| Action | add-coverage |
| Repo | sandbox |
| Area | Provider-Billing — credential handling |
| Estimate | 2h |
| Labels | e2e, security, credentials |
| Evidence revision | `eef9429d` (`origin/main`) |

## Summary
The billing specs authenticate using passwords written as plaintext string literals in the spec files
and committed to git. Move them to environment variables or the repo's secret mechanism.

> Deliberately not reproduced here: this ticket names locations, not values.

## Context
`sandbox` logs into production `zocdoc.com` as real test accounts. Login helpers take an email and a
password; both are currently supplied as literals in the spec source.

## Current state
Plaintext password literals appear at:

| File | Locations |
|---|---|
| `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | 1 occurrence, in the `beforeEach` `loginByAPI` call |
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | 2 occurrences, in `loginByUI` / `loginByAPI` calls |

These are committed to git history and are readable by anyone with repo access, in every past
revision.

## Why this matters
These credentials authenticate against **production**. Even limited test accounts can read
provider-side production screens — including, in one spec, an appointment report (see SBX-003).
Plaintext-in-git means rotation requires a commit, exposure cannot be undone from history, and access
is scoped to "everyone who can read the repo" rather than "CI and the people who need it."

Priority is P1 rather than P0 because these are test accounts in a private repo, not customer or
admin credentials. It is a real problem, not an emergency.

## Acceptance criteria
- [ ] All password literals removed from spec source; credentials read from environment variables
      (or the mechanism the repo already uses — check for an existing pattern before inventing one).
- [ ] Local runs documented: which variables to set, and where to obtain the values. Add to
      `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` or the repo README.
- [ ] CI supplies the variables via its secret store.
- [ ] A missing variable fails with a clear, actionable message rather than a confusing login failure.
- [ ] Passwords **rotated** after the change — removing a value from `HEAD` does not remove it from
      history, so the old value must be assumed compromised.
- [ ] Verification: the billing specs pass with the variables set, and fail with a clear message when unset.

## Test cases to write
| # | Scenario | Expected |
|---|---|---|
| 1 | Required env vars set | Specs authenticate and pass |
| 2 | A required env var missing | Clear error naming the missing variable; no confusing timeout |
| 3 | `git grep` for the old literals | No hits in `HEAD` |

## Files
| Path | Change |
|---|---|
| `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | change — 1 credential |
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | change — 2 credentials |
| `playwright/support/auth.ts` | read only — confirm the helper signature; add validation if that is the right home |
| `playwright/BU/Provider/Acquisition/Provider-Billing/OWNERSHIP.md` | change — document required variables |

## Out of scope
- Other specs in the repo. Audit them, and open a repo-wide follow-up if the pattern is widespread —
  do not expand this ticket.
- Purging git history. Rotation is the practical mitigation; history rewriting on a shared repo is a
  separate decision.

## Verification
```
npx playwright test playwright/BU/Provider/Acquisition/Provider-Billing/ --project=chromium --workers=1
```
Then unset one variable and confirm the failure message names it. Then `git grep` the old literals in
`HEAD` and confirm no hits.

## Notes
Do this alongside SBX-001. Deduplication removes one of the three credential sites for free.
