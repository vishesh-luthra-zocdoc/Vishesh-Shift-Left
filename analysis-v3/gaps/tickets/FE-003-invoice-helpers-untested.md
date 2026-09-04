# FE-003 — Add unit tests for `invoiceHelpers.ts`

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P0 |
| Test level | L1 unit |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — invoice formatting |
| Estimate | 45m |
| Labels | shift-left, test-coverage, unit, money-math |
| Evidence revision | `dd9e4952a6` |

## Summary
`invoiceHelpers.ts` formats and derives the invoice figures providers read, and has no tests. This
ticket adds direct unit tests, starting with anything that touches an amount or a date.

## Context
Billing Settings shows providers their invoices — amounts due, statuses, dates, and line items.
`invoiceHelpers.ts` holds the pure functions that shape that data for display. Pure functions with
money in them are the cheapest possible thing to test and among the most damaging to get wrong.

## Current state
**No test file exists.** There is no
`pages/settingsPages/billingSettings/__tests__/invoiceHelpers-tests.ts`, and no other test imports
the module directly — any coverage it has is incidental, via components that happen to call it.

Raised by v2 as its P0 #2 with a 45-minute estimate. Re-verified still untested at `dd9e4952a6`.

## Why this matters
A formatting or rounding error here shows a provider the wrong amount owed. Nothing fails; the
number is simply wrong on screen. Providers dispute invoices, support escalates, and trust in
billing accuracy erodes — the most expensive kind of billing bug because it is silent.

## Acceptance criteria
- [ ] Create `apps/settings/src/pages/settingsPages/billingSettings/__tests__/invoiceHelpers-tests.ts`.
- [ ] Every exported function in `invoiceHelpers.ts` has at least one direct test.
- [ ] Every function returning or formatting a monetary value asserts a **hardcoded expected string
      or number** — never a value recomputed with the source's own expression (see FE-002).
- [ ] Edge cases covered: zero, negative (credits/refunds), very large amounts, and `null`/
      `undefined` inputs.
- [ ] Verification: `yarn test .../billingSettings/__tests__/invoiceHelpers-tests.ts` passes.

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | A normal positive amount | Correct hardcoded currency string |
| 2 | Zero | `$0` / `$0.00` per the source's convention — assert the literal |
| 3 | A negative amount (credit or refund) | Correctly signed, not silently absolute |
| 4 | A large amount requiring separators | Comma-grouped correctly |
| 5 | A fractional amount | Rounds per the documented convention, asserted literally |
| 6 | `null` / `undefined` / missing field | Documented fallback, no throw |

> Fill the exact function names and expectations while reading the file — the shape above is the
> requirement, not a guess at the API.

## Files
| Path | Change |
|---|---|
| `apps/settings/src/pages/settingsPages/billingSettings/invoiceHelpers.ts` | read only — subject under test |
| `apps/settings/src/pages/settingsPages/billingSettings/__tests__/invoiceHelpers-tests.ts` | **create** |

## Out of scope
Refactoring `invoiceHelpers.ts`. If a function is hard to test, note it on the ticket rather than
restructuring production code here.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings/__tests__/invoiceHelpers-tests.ts
```
Passing = every export has a direct test and money assertions use literals.

## Notes
Carried forward from v2 P0 #2, unchanged and still correct. This is the cheapest P0 in the backlog —
pure functions, no mocking, no async.
