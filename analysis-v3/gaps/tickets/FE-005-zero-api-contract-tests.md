# FE-005 — Add API contract tests for the billing endpoints the UI consumes

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P1 |
| Test level | L4 api |
| Action | add-coverage |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — API contracts |
| Estimate | 1d |
| Labels | shift-left, test-coverage, api, contract |
| Evidence revision | `dd9e4952a6` |

## Summary
Billing has **zero** L4 API-contract tests. Every mock in the repo encodes what the frontend
*believes* the backend returns, and nothing verifies that belief. This ticket introduces a contract
layer for the highest-traffic billing endpoints.

## Context
Billing Settings calls 13 REST endpoints. Their shapes are hand-written into E2E route stubs
(`apps/settings/e2e/fixtures.ts`) and into L2 component mocks. Those two sets of assumptions are
maintained separately, by hand, and neither is checked against the real services (`zocdoc_web`,
`provider-billing`).

## Current state
- **L4 test count for billing: 0.** Verified by inventory across 90 non-E2E billing test files
  (L1 34 files / 224 tests, L2 45 / 515, L2-hooks 9 / 47, L3 2 / 70, **L4 0**).
- No MSW. No `nock`. No recorded-fixture or schema-validation harness anywhere in the billing tree.
- E2E stubs all 13 endpoints inline, so the browser suite validates the frontend against the
  frontend's own assumptions.

## Why this matters
When a backend team renames a field, changes a nullability, or alters an enum, **nothing in this repo
fails**. The mocks keep returning the old shape and all 63 E2E tests plus 856 unit/component tests
stay green. The break surfaces in production, on the billing page, in front of providers.

This is the structural reason the suite's green signal is weaker than its size suggests: 856 tests
and none of them touch a real contract.

## Acceptance criteria
- [ ] Choose and document the mechanism: MSW with schema validation, or contract tests generated
      from the services' OpenAPI specs. Record the choice and why in the PR description.
- [ ] Cover at minimum the endpoints behind: payment methods list, add payment method, monthly limit
      update, invoice list, invoice detail.
- [ ] Each contract test asserts **response shape** — required fields, types, nullability, enum
      values — not business behaviour.
- [ ] Contract definitions are shared with the E2E fixtures so a single source of truth drives both,
      rather than a second hand-maintained copy.
- [ ] A deliberate field rename in the contract fails the suite. Record this check.
- [ ] Verification: `yarn test` on the new contract directory passes.

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | Payment methods list response | Matches contract: required fields present, correct types |
| 2 | Payment methods list, empty | Empty collection valid, not `null`, no throw |
| 3 | Add payment method success | Response shape matches contract |
| 4 | Add payment method error | Error shape matches contract; UI-consumed error field present |
| 5 | Monthly limit update | Request *and* response shapes both asserted |
| 6 | Invoice list + invoice detail | Shapes match, including nullable/optional fields |
| 7 | Contract drift: rename a required field | Suite **fails** |

## Files
| Path | Change |
|---|---|
| `apps/settings/src/pages/settingsPages/billingSettings/__contracts__/` | **create** — new contract test directory |
| `apps/settings/e2e/fixtures.ts` | change — source stub shapes from the shared contracts |
| `package.json` | change — add MSW or the chosen harness, if not already present |

## Out of scope
- Contract tests for non-billing endpoints. Establish the pattern in billing first.
- Consumer-driven contract publication (e.g. Pact broker) — a follow-up if this proves valuable.
- Backend-side verification. See the `provider-billing` and `zocdoc_web` tickets.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings/__contracts__
```
Passing = shapes asserted. Then rename a required field in one contract; the suite must fail.

## Notes
Pairs with FE-001. FE-001 proves the browser can talk to a real Stripe; this proves the app agrees
with its own backends. Together they are the integration confidence the current suite lacks entirely.
