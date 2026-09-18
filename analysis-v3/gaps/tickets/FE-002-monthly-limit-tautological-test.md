# FE-002 — Replace the tautological monthly-limit assertion with hardcoded boundary values

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Bug |
| Priority | P0 |
| Kind of test | Unit test |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — monthly payment limit validation |
| Estimate | 45m |
| Labels | shift-left, test-coverage, unit, money-math |
| Evidence revision | `dd9e4952a6` |

## Summary
The only test guarding the minimum monthly payment limit computes its expected value using the same
expression as the code under test, so it cannot fail. The maximum limit is asserted nowhere. This
ticket replaces both with hardcoded boundary assertions.

## Context
`utils/schemaBuilder.ts` builds the yup validation schemas for Billing Settings forms, including the
monthly payment limit a provider sets to cap what Zocdoc charges them. The minimum is driven by a
feature flag (`Billing.MinimumPaymentMethodLimit`, defaulting to `500`); the maximum is hardcoded at
`500000`.

## Current state
`utils/schemaBuilder.ts` has **no direct tests** (5 yup schemas, all covered only indirectly).

The one flag-related assertion that exists is a tautology —
`__tests__/EditMonthlyLimitModalV2-tests.tsx:129-133`:

```ts
const minimumMonthlyLimit = parseInt(
    getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500',
);
```

That is **the same expression the source under test uses**. If the source's default were changed to
a wrong value, the test would compute the identical wrong value and pass. It cannot fail for the
reason it exists.

`maximumMonthlyLimit = 500000` (`utils/schemaBuilder.ts:101`) is asserted **nowhere**.

## Why this matters
These are monetary boundaries on how much Zocdoc can charge a provider. A regression that drops the
minimum to `0` or lifts the maximum lets a provider set a limit that either blocks all billing or
permits an unbounded charge — and the current test suite stays green either way.

This is not a hypothetical style complaint: a green test on a money boundary is worse than no test,
because it stops anyone from looking.

Contrast with `YearlyValueCalcModalV2-tests.tsx:206-225`, which asserts `'$327'` worked out by hand
and *would* catch a formula change. Same folder, same team. That is the standard this ticket applies.

## Acceptance criteria
- [ ] Create `utils/__tests__/schemaBuilder-tests.ts` with direct tests for the monthly-limit schema.
- [ ] The minimum boundary is asserted with a **literal** `500` — no call to `getFeatureFlagVariant`
      in the expectation.
- [ ] A flag-override case asserts a literal overridden minimum (e.g. flag returns `'750'` → `750`
      is the boundary), proving the flag is actually read.
- [ ] The maximum boundary `500000` is asserted with a literal.
- [ ] `EditMonthlyLimitModalV2-tests.tsx:129-133` no longer derives its expectation from the source's
      own expression.
- [ ] Verification: `yarn test apps/settings/src/pages/settingsPages/billingSettings/utils` passes.

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | Limit `499`, flag unset | Invalid — below the `500` minimum |
| 2 | Limit `500`, flag unset | Valid — boundary inclusive |
| 3 | Flag returns `'750'`; limit `600` | Invalid — proves the flag is read, not ignored |
| 4 | Flag returns `'750'`; limit `750` | Valid |
| 5 | Limit `500000` | Valid — boundary inclusive |
| 6 | Limit `500001` | Invalid — above the maximum |
| 7 | Limit `0` / negative / non-numeric | Invalid |

## Files
| Path | Change |
|---|---|
| `apps/settings/src/pages/settingsPages/billingSettings/utils/schemaBuilder.ts` | read only — subject under test |
| `apps/settings/src/pages/settingsPages/billingSettings/utils/__tests__/schemaBuilder-tests.ts` | **create** |
| `apps/settings/src/pages/settingsPages/billingSettings/__tests__/EditMonthlyLimitModalV2-tests.tsx` | change — de-tautologise `:129-133` |

## Out of scope
The other 4 yup schemas in `schemaBuilder.ts`. Worth covering, but this ticket is scoped to the
monetary boundary. Open a P2 follow-up for the rest.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings/utils
```
Passing = boundaries asserted against literals. Sanity check: temporarily change the source default
from `500` to `400`; the new tests must **fail**. The old test did not.

## Notes
v2 raised `schemaBuilder.ts` as P1 "tested only indirectly". v3 raises it to P0 — the tautology
finding is materially worse than "indirect coverage". v2 also counted 7 schemas; there are **5** at
this revision.
