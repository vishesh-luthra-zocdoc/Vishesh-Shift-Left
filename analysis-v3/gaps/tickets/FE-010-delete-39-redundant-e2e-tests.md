# FE-010 — Delete 39 E2E tests already covered by named L2 tests

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Chore |
| Priority | P2 |
| Test level | L5 e2e |
| Action | delete |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — E2E suite |
| Estimate | 1d |
| Labels | shift-left, e2e, cleanup |
| Evidence revision | `dd9e4952a6` |

## Summary
Thirty-nine billing E2E tests assert behaviour that a **named, existing** L2 test already asserts.
Delete them. This is the largest single CI-cost reduction in the backlog — and the one with the most
sequencing risk, so it goes last.

## Current state
39 of 63 tests carry the verdict `delete-redundant`, each with its covering L2 test cited by file and
verbatim `it` title in
[`../../analysis-scratch/e2e-shift-left-candidates.md`](../../analysis-scratch/e2e-shift-left-candidates.md).

**Zero** tests were classified `delete-suspected` — the category reserved for "looks redundant but I
cannot cite the cover." Every deletion here has a named replacement.

Citations were spot-checked rather than trusted wholesale:

| Cited covering test | Verified at |
|---|---|
| `it('calls setDefaultPaymentMethod API on "Set as default" click')` | `PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-tests.tsx:605` |
| `it('opens EditMonthlyLimitModal on "Set limit" click')` | same file, `:801` |

## Why this matters
Pure cost. 39 browser tests on a **serial** CI job (`playwright.config.ts:14`) at up to 60 s each.
No correctness gain — and that is the point of doing it last: the benefit is cheap CI, so it must
never be bought at the price of real coverage.

## Tests being removed
39 tests. Each row in the scratch file gives: source spec, line, and the covering L2 test's file and
`it` title. **The PR description must reproduce that mapping in full** so a reviewer can check any
row without re-deriving it.

Split into per-spec PRs, not one 39-test deletion:

| PR | Spec | Approx. count |
|---|---|---|
| 1 | `billing-settings-v2.spec.ts` | largest share |
| 2 | `billing-invoice-summary.spec.ts` | |
| 3 | `billing-pricing-v2.spec.ts` | |
| 4 | `billing-settings-page.spec.ts` + `invoice-details-page.spec.ts` | remainder |

Take exact counts from the scratch file at execution time — they shift as FE-004/FE-007/FE-009 land.

## Acceptance criteria
- [ ] Before deleting each test, **run its cited L2 covering test and confirm it passes.** A cited
      test that does not exist or does not pass blocks that row — downgrade it to `investigate`
      rather than deleting.
- [ ] The full source → covering-test mapping appears in the PR description.
- [ ] No row is deleted on the basis of "looks similar." Only cited rows.
- [ ] Verification: `yarn playwright test apps/settings/e2e/PracticeSettingsPages/` and
      `yarn test .../billingSettings` both pass.

## Files
| Path | Change |
|---|---|
| `apps/settings/e2e/PracticeSettingsPages/*.spec.ts` | change — remove 39 tests |

## Out of scope
Removing the E2E infrastructure, fixtures, or page objects. Even a much smaller suite needs them, and
`billing-settings-page-commands.ts` (562 lines) plus the 2 page objects (231 lines) should be pruned
in a separate pass once the final suite shape is known.

## Blocked by
**FE-001, FE-008, FE-009 — all three.** This is the last step of the plan, deliberately.

## Verification
```
yarn playwright test apps/settings/e2e/PracticeSettingsPages/
yarn test apps/settings/src/pages/settingsPages/billingSettings
```

## Notes
**Read this before starting.** Executing FE-007 + FE-009 + FE-010 in isolation leaves the billing
E2E suite with essentially **one** test exercising a multi-page journey
(`payment-recovery.spec.ts:96`). Every individual verdict is correct and the aggregate is still a
worse suite — cheaper, but blind to whether the page wires itself together at all.

That is why FE-001 is P0 and this is P2 despite being the biggest line-count win. Sequencing is the
whole ticket. See [`../../shift-left/E2E-PLAN-JUDGMENT.md`](../../shift-left/E2E-PLAN-JUDGMENT.md).
