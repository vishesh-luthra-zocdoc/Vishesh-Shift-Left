# FE-013 — Add coverage for the 13 billing source files with no tests at all

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P3 |
| Kind of test | Component test |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — uncovered components |
| Estimate | 1d |
| Labels | shift-left, test-coverage, component |
| Evidence revision | `dd9e4952a6` |

## Summary
Thirteen billing source files have neither direct nor indirect test coverage. Most are
presentational, which is why this is P3 — but "no coverage at all" should be a deliberate choice, not
an accident.

## Context
The billing area has **152 source files**. 88 have some coverage; 64 have no direct test; of those,
**13 have no coverage of any kind** — not even incidental coverage via a parent component's test.

## Current state
| Metric | Count |
|---|---|
| Billing source files | 152 |
| With some coverage | 88 |
| No **direct** test | 64 |
| **No coverage at all (direct or indirect)** | **13** |

The 13 are enumerated in
[`../../inventory/provider-fe-monorepo/source-components.md`](../../inventory/provider-fe-monorepo/source-components.md).

This list was **14** during analysis and corrected down to 13: `PriceByProviderModal.tsx` does have
indirect coverage via `PricingInformationV2-tests.tsx:215`. Re-derive the list at execution time
rather than trusting a three-week-old count.

## Why this matters
Low blast radius — these are mostly presentational, and a broken presentational component is usually
visible immediately. The real cost is that they are invisible to every refactor: a rename or prop
change cannot be validated by the suite, so changes here rely entirely on manual checking.

Any file among the 13 that formats or displays a **monetary value** is not P3 — pull it into its own
P1 ticket instead of handling it here.

## Acceptance criteria
- [ ] Re-derive the uncovered list at `HEAD` and record it on the ticket. Do not work from the stale list.
- [ ] Triage each file into: **money/logic** (split out to a higher-priority ticket),
      **presentational** (cover here), or **intentionally untested** (document why and close).
- [ ] Each presentational file gets a component render test asserting it renders and displays its key props.
- [ ] Any money formatting uses **hardcoded** expected values (see FE-002).
- [ ] Verification: `yarn test .../billingSettings` passes with 13 fewer wholly-uncovered files.

## Test cases to write
Per file, minimum:

| # | Scenario | Expected |
|---|---|---|
| 1 | Render with typical props | Renders without throwing; key content present |
| 2 | Render with empty/missing optional props | Documented fallback; no crash |
| 3 | If it takes a callback | Callback fires on the expected interaction |

## Files
| Path | Change |
|---|---|
| 13 files listed in `inventory/provider-fe-monorepo/source-components.md` | read only — subjects under test |
| Corresponding `__tests__/*-tests.tsx` | **create** — up to 13 files |

## Out of scope
The other 51 files that lack a *direct* test but have indirect coverage. Lower value; revisit only if
a specific one causes a bug.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings
```

## Notes
Good first ticket for someone new to the billing area — small, independent, no sequencing
dependencies. Split into 2–3 PRs rather than one 13-file change.
