# FE-012 — Assess coverage of `LegacyInvoiceView`, now that it renders unconditionally

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Task |
| Priority | P2 |
| Test level | L2 component |
| Action | investigate |
| Repo | provider-fe-monorepo |
| Area | Billing Settings — invoice details |
| Estimate | 2h |
| Labels | test-coverage, component, flag-cleanup |
| Evidence revision | `dd9e4952a6` |

## Summary
`LegacyInvoiceView` was assumed dead and slated for deletion. It is **live** — and since its gating
flag was removed it now renders unconditionally for non-FPB invoices. Confirm its coverage is
adequate for a permanent path.

> **Do not delete this component.** See below.

## Context
Invoice details render through either a newer view or `LegacyInvoiceView`, historically gated by
`show_new_invoice_details_page`. That flag's plumbing was removed in `a88b14cba6`.

## Current state
The component is **alive and reachable**:
- Imported at `InvoiceDetailsContainer.tsx:16`
- Rendered at `InvoiceDetailsContainer.tsx:201`
- Both `LegacyInvoiceView.tsx` (~10 KB) and `__tests__/LegacyInvoiceView-tests.tsx` are present on `main`

**v2 got this wrong and it is worth recording why.** v2 ranked "delete `LegacyInvoiceView` and its
tests" as its #1 P0 and top recommended next step, citing `a88b14cba6` as the teardown. That commit
changed 6 files (+8/−44) — `billing-settings-page-commands.ts`, `ab/experiments.ts`,
`BillingSettingsContainer.tsx`, `BillsContainer.tsx`, `BillingSettingsContainer-tests.tsx`,
`settingsExperimentsType.ts` — and **touched neither `LegacyInvoiceView*` nor
`InvoiceDetailsContainer.tsx`**.

Removing the flag made the legacy branch **unconditional, not dead**. Had v2's recommendation
shipped, it would have broken non-FPB invoice rendering for providers.

## Why this matters
The real question is not deletion but adequacy. A path that used to be one arm of an experiment is now
the permanent path for a class of invoices, and its coverage was sized for the former situation.
Providers reading invoices through this view see real amounts.

## Decision rule
| Finding | Action |
|---|---|
| Existing `LegacyInvoiceView-tests.tsx` covers the render paths and money formatting | Close with evidence. No work needed. |
| Coverage is thin for a now-permanent path | Extend the L2 tests. Prioritise anything displaying an amount, date, or status. |
| The component is genuinely unreachable (contradicting the above) | Prove it with the reachability trace, **then** delete with a `delete` ticket citing the evidence. Do not act on inference. |

## Acceptance criteria
- [ ] Determine which invoices route to `LegacyInvoiceView` vs the newer view, with `file:line`
      evidence from `InvoiceDetailsContainer.tsx`.
- [ ] Enumerate what `__tests__/LegacyInvoiceView-tests.tsx` currently asserts.
- [ ] Identify uncovered render paths and monetary formatting, and close the gaps.
- [ ] Any money assertion added uses **hardcoded** expected values (see FE-002).
- [ ] Verification: `yarn test .../__tests__/LegacyInvoiceView-tests.tsx` passes.

## Files
| Path | Change |
|---|---|
| `apps/settings/src/pages/settingsPages/billingSettings/InvoiceDetailsContainer.tsx` | read only — `:16`, `:201` |
| `.../LegacyInvoiceView.tsx` | read only — subject under test |
| `.../__tests__/LegacyInvoiceView-tests.tsx` | change — extend if thin |

## Out of scope
Migrating non-FPB invoices onto the newer view. A product decision, not a test one.

## Verification
```
yarn test apps/settings/src/pages/settingsPages/billingSettings/__tests__/LegacyInvoiceView-tests.tsx
```

## Notes
This ticket exists mainly so v2's wrong P0 is not executed by someone reading the old analysis. If
you only read one thing here: **the component is live.**
