# SBX-001 — Deduplicate the two sandbox billing specs (~75% identical)

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Chore |
| Priority | P1 |
| Test level | L5 e2e |
| Action | delete |
| Repo | sandbox |
| Area | Provider-Billing — production E2E |
| Estimate | 2h |
| Labels | shift-left, e2e, cleanup, duplication |
| Evidence revision | `eef9429d` (`origin/main`) |

## Summary
`billing-user-flow.spec.ts` contains a 365-line block that duplicates almost all of
`billing-settings-page.spec.ts` — same two test titles, ~75% identical body. In a billing suite of
only **5 tests**, two are redundant copies. Consolidate to one.

## Context
The `sandbox` repo runs Playwright against **production** `zocdoc.com` with real test accounts. It is
the only place a real backend and a real Stripe are exercised, which makes its small test budget
disproportionately valuable — and duplication disproportionately wasteful.

## Current state
Two specs, 5 tests total:

| Spec | Tests | Lines |
|---|---|---|
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | 3 | 451 |
| `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | 2 | 380 |

**The duplication:** `billing-user-flow.spec.ts:87-451` and `billing-settings-page.spec.ts:29-380`
contain identically-titled tests:
- `"Manage billing settings: layout, payment methods, invoice, contact info, and pricing"`
- `"Add and remove a credit card payment method"`

Diffing the two blocks (365 vs 352 lines) yields only **90 diff lines** — roughly 75% identical. The
differences are incidental, not behavioural:

| Difference | `billing-user-flow.spec.ts` | `billing-settings-page.spec.ts` |
|---|---|---|
| Viewport | `macbook-16` | `macbook-15` |
| Login | `loginByUI` | `loginByAPI` |
| Navigation | direct `page.goto("/provider/config/settings/billing")` | goto inbox, then click sidebar |
| Cleanup ordering | after setup steps | inside a dedicated "Clean up billing state" step |
| Extra cookie | sets `zd_global_nav_coachmark_shown` | — |

## Why this matters
Every duplicated test doubles the cost of the most expensive tests we own: real browser, real
production backend, real Stripe, serialized (see SBX-002). It also doubles the maintenance surface —
when the monorepo changed the payment DOM on 2026-09-02, **both** copies had to be repaired.

Worse, the duplication hides how thin the real coverage is: "5 billing tests against production"
sounds reasonable; **3 distinct journeys** is the truth.

## Tests being removed
| # | Remove | Keep | Rationale |
|---|---|---|---|
| 1 | `billing-user-flow.spec.ts` "Manage billing settings: layout, payment methods…" | the copy in `billing-settings-page.spec.ts` | Identical title and ~75% identical body. Keeper uses `loginByAPI` (faster, less flaky than `loginByUI`) and lives under `Provider-Billing/`, matching the BU ownership hierarchy. |
| 2 | `billing-user-flow.spec.ts` "Add and remove a credit card payment method" | the copy in `billing-settings-page.spec.ts` | Same. |

`billing-user-flow.spec.ts` retains its genuinely distinct first test,
`"Billing user can navigate to appointment report and view patient data (PROVPERF-2665)"`.

## Acceptance criteria
- [ ] Before deleting, diff the two blocks and confirm **every** assertion in the removed copy exists
      in the keeper. Port any assertion unique to the removed copy (e.g. the `macbook-16` viewport
      case, if that resolution is deliberately covered) rather than losing it.
- [ ] `billing-user-flow.spec.ts:87-451` removed; the file keeps only the appointment-report test.
- [ ] The kept spec still passes against production.
- [ ] Confirm the removed copy's navigation path (direct `goto` to `/provider/config/settings/billing`)
      is either covered by the keeper's sidebar-click path or explicitly deemed redundant — note which.
- [ ] Verification: `npx playwright test playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts --project=chromium --workers=1` passes.

## Files
| Path | Change |
|---|---|
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | change — remove the duplicated describe block (`:87-451`) |
| `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | read only — the keeper |
| `playwright/support/billing.ts` | read only — shared helpers, unaffected |

## Out of scope
The appointment-report test in `billing-user-flow.spec.ts` — different feature, different owner. See
SBX-003 for a separate concern about it.

## Verification
```
npx playwright test playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts --project=chromium --workers=1
```
`--workers=1` is required — see SBX-002.

## Notes
Whichever copy is kept, the file placement should follow the BU hierarchy in `CLAUDE.md`:
billing-settings coverage belongs under `Provider/Acquisition/Provider-Billing/`, not under
`Account-User-Setup/`.
