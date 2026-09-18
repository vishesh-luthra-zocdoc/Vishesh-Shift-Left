# v3 Gap Backlog

**20 tickets, all filed in Jira project BILL** — 13 with a write-up here, 7 in Jira only. Read
[`../START-HERE.md`](../START-HERE.md) first — it says what to test and in what order in one page.
This file is the full index with links to both the local write-up and the Jira ticket.

**Scope:** pre-release tests in team-owned repos — `provider-fe-monorepo`, `provider-billing`,
`zocdoc_web`. The QA-owned `sandbox` repo is out of scope and handled separately.

Before working these, spot-check the findings with
[`../VERIFY-THIS-FIRST.md`](../VERIFY-THIS-FIRST.md) — ten minutes of copy-pasteable commands
against the highest-risk claims.

Ticket shape is defined by [`TICKET-TEMPLATE.md`](TICKET-TEMPLATE.md).

**On the `FE-*` / `PB-*` / `WEB-*` prefixes:** they're just repo handles — `FE` =
`provider-fe-monorepo`, `PB` = `provider-billing`, `WEB` = `zocdoc_web`. The
`FE-*` rows have a full write-up in [`tickets/`](tickets/); the `PB-*` and `WEB-*` rows
exist only as Jira tickets — the backend write-ups and inventories were never committed here.

---

## By priority

### P0 — untested logic that can corrupt money or provider-facing data

| ID | Title | Level | Action | Est. | Jira |
|---|---|---|---|---|---|
| [FE-001](tickets/FE-001-real-stripe-payment-element-untested.md) | Add an integration test that a real Stripe Payment Element mounts and accepts a card | L5 e2e | add-coverage | 1d | [BILL-1193](https://zocdoc.atlassian.net/browse/BILL-1193) |
| [FE-002](tickets/FE-002-monthly-limit-tautological-test.md) | Replace the tautological monthly-limit assertion with hardcoded boundary values | L1 unit | add-coverage | 45m | [BILL-1194](https://zocdoc.atlassian.net/browse/BILL-1194) |
| [FE-003](tickets/FE-003-invoice-helpers-untested.md) | Add unit tests for `invoiceHelpers.ts` | L1 unit | add-coverage | 45m | [BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195) |
| PB-001 | Stripe webhook idempotency is bypassed in production and all four dedup tests are commented out | L3 integration | add-coverage | 1d | [BILL-1211](https://zocdoc.atlassian.net/browse/BILL-1211) |
| WEB-001 | Prorated subscription day-count is untested, and the source comment says the math is wrong | L1 unit | add-coverage | 4h | [BILL-1217](https://zocdoc.atlassian.net/browse/BILL-1217) |

### P1 — real user-visible failure mode, or material CI cost

| ID | Title | Level | Action | Est. | Jira |
|---|---|---|---|---|---|
| [FE-005](tickets/FE-005-zero-api-contract-tests.md) | Add API contract tests for the billing endpoints the UI consumes | L4 api | add-coverage | 1d | [BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197) |
| [FE-004](tickets/FE-004-conditional-assertions-green-noops.md) | Fix six E2E tests whose assertions are entirely inside `if (mock.find(...))` | L5 e2e | add-coverage | 2h | [BILL-1196](https://zocdoc.atlassian.net/browse/BILL-1196) |
| [FE-006](tickets/FE-006-ach-no-e2e-coverage.md) | Add coverage for the ACH / bank-account add-payment-method path | L5 e2e | add-coverage | 4h | [BILL-1198](https://zocdoc.atlassian.net/browse/BILL-1198) |
| WEB-002 | Replace the tautological tax assertion in `ProcessorGenerateChargeGroupsTest` with hardcoded amounts | L1 unit | add-coverage | 2h | [BILL-1218](https://zocdoc.atlassian.net/browse/BILL-1218) |
| WEB-003 | The bill generator has no active tests — its only fixture is `[Ignore]`d | L3 integration | add-coverage | 1d | [BILL-1219](https://zocdoc.atlassian.net/browse/BILL-1219) |

### P2 — meaningful gap, low blast radius

| ID | Title | Level | Action | Est. | Jira |
|---|---|---|---|---|---|
| [FE-009](tickets/FE-009-shift-19-e2e-tests-to-component-level.md) | Shift 19 mocked E2E tests down to L2 component tests | L2 component | shift-left | 1d | [BILL-1201](https://zocdoc.atlassian.net/browse/BILL-1201) |
| [FE-010](tickets/FE-010-delete-39-redundant-e2e-tests.md) | Delete 39 E2E tests already covered by named L2 tests | L5 e2e | delete | 1d | [BILL-1202](https://zocdoc.atlassian.net/browse/BILL-1202) |
| [FE-007](tickets/FE-007-delete-empty-and-duplicate-e2e-tests.md) | Delete the empty E2E test and the four intra-suite duplicates | L5 e2e | delete | 45m | [BILL-1199](https://zocdoc.atlassian.net/browse/BILL-1199) |
| [FE-008](tickets/FE-008-move-geometry-assertions-to-visual-regression.md) | Move the three layout-geometry assertions out of the functional E2E suite | L5 e2e | shift-left | 4h | [BILL-1200](https://zocdoc.atlassian.net/browse/BILL-1200) |
| [FE-012](tickets/FE-012-legacy-invoice-view-coverage.md) | Assess coverage of `LegacyInvoiceView`, now that it renders unconditionally — **do not delete it** | L2 component | investigate | 2h | [BILL-1204](https://zocdoc.atlassian.net/browse/BILL-1204) |
| [FE-011](tickets/FE-011-investigate-iframe-deprecation-flag.md) | Determine the `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` ramp state and remove its test branches | L2 component | investigate | 2h | [BILL-1203](https://zocdoc.atlassian.net/browse/BILL-1203) |
| PB-002 | Cover the hardcoded `ActualCost = 0` in the appointment event processor | L1 unit | add-coverage | 2h | [BILL-1212](https://zocdoc.atlassian.net/browse/BILL-1212) |
| PB-004 | Add an integration test for the billing-export **Generate** stage (Gather and Enrich have one) | L3 integration | add-coverage | 4h | [BILL-1214](https://zocdoc.atlassian.net/browse/BILL-1214) |

### P3 — polish

| ID | Title | Level | Action | Est. | Jira |
|---|---|---|---|---|---|
| [FE-013](tickets/FE-013-thirteen-source-files-with-no-coverage.md) | Add coverage for the 13 billing source files with no tests at all | L2 component | add-coverage | 1d | [BILL-1205](https://zocdoc.atlassian.net/browse/BILL-1205) |
| WEB-004 | Establish what the 15 gate-exempt billing test files actually leave uncovered | L1 unit | investigate | 4h | [BILL-1220](https://zocdoc.atlassian.net/browse/BILL-1220) |

---

## Sequencing — read this before starting the E2E work

The shift-left tickets are **ordered on purpose**. Running FE-007 + FE-009 + FE-010 without FE-001
leaves the billing E2E suite with essentially **one** test exercising a multi-page journey. Every
individual verdict would be correct and the suite would still be worse: cheaper, and blind to whether
the page wires itself together at all.

```
FE-004  (make the suite tell the truth — 6 tests currently pass vacuously)
   ↓
FE-001  (establish the floor — the ONLY real-dependency test)
FE-008  (relocate geometry assertions so it's clear what needs a browser)
   ↓
FE-007  (free wins — empty test + 4 duplicates)
   ↓
FE-009  (shift 19 down to L2 — each L2 test lands BEFORE its E2E counterpart is removed)
   ↓
FE-010  (bulk delete 39 — last, deliberately)
```

`FE-001` should land before `FE-011`. FE-011 is a flag teardown of the same kind that changed the
payment DOM on 2026-09-02 — monorepo CI stayed green because it mocks Stripe, and a downstream suite
went red instead. FE-001 is the test that would catch it in this repo.

## Independent, no sequencing

`FE-002`, `FE-003`, `FE-005`, `FE-012`, `FE-013`, and every `PB-*` and `WEB-*` ticket. Start any of
these today.

## Fastest value

| Ticket | Est. | Why |
|---|---|---|
| FE-003 | 45m | Pure functions, no mocking, no async. Cheapest P0 in the backlog. |
| FE-002 | 45m | Converts a test that *cannot fail* into one that can. |
| FE-007 | 45m | Deletes 5 tests with zero coverage risk. |

Then **FE-001** — it's worth more than the entire 39-test deletion. The deletion saves CI minutes;
FE-001 prevents a revenue-path outage.

## Jira key mapping

| Local ID | Jira key | Repo |
|---|---|---|
| FE-001 | [BILL-1193](https://zocdoc.atlassian.net/browse/BILL-1193) | `provider-fe-monorepo` |
| FE-002 | [BILL-1194](https://zocdoc.atlassian.net/browse/BILL-1194) | `provider-fe-monorepo` |
| FE-003 | [BILL-1195](https://zocdoc.atlassian.net/browse/BILL-1195) | `provider-fe-monorepo` |
| FE-004 | [BILL-1196](https://zocdoc.atlassian.net/browse/BILL-1196) | `provider-fe-monorepo` |
| FE-005 | [BILL-1197](https://zocdoc.atlassian.net/browse/BILL-1197) | `provider-fe-monorepo` |
| FE-006 | [BILL-1198](https://zocdoc.atlassian.net/browse/BILL-1198) | `provider-fe-monorepo` |
| FE-007 | [BILL-1199](https://zocdoc.atlassian.net/browse/BILL-1199) | `provider-fe-monorepo` |
| FE-008 | [BILL-1200](https://zocdoc.atlassian.net/browse/BILL-1200) | `provider-fe-monorepo` |
| FE-009 | [BILL-1201](https://zocdoc.atlassian.net/browse/BILL-1201) | `provider-fe-monorepo` |
| FE-010 | [BILL-1202](https://zocdoc.atlassian.net/browse/BILL-1202) | `provider-fe-monorepo` |
| FE-011 | [BILL-1203](https://zocdoc.atlassian.net/browse/BILL-1203) | `provider-fe-monorepo` |
| FE-012 | [BILL-1204](https://zocdoc.atlassian.net/browse/BILL-1204) | `provider-fe-monorepo` |
| FE-013 | [BILL-1205](https://zocdoc.atlassian.net/browse/BILL-1205) | `provider-fe-monorepo` |
| PB-001 | [BILL-1211](https://zocdoc.atlassian.net/browse/BILL-1211) | `provider-billing` |
| PB-002 | [BILL-1212](https://zocdoc.atlassian.net/browse/BILL-1212) | `provider-billing` |
| PB-004 | [BILL-1214](https://zocdoc.atlassian.net/browse/BILL-1214) | `provider-billing` |
| WEB-001 | [BILL-1217](https://zocdoc.atlassian.net/browse/BILL-1217) | `zocdoc_web` |
| WEB-002 | [BILL-1218](https://zocdoc.atlassian.net/browse/BILL-1218) | `zocdoc_web` |
| WEB-003 | [BILL-1219](https://zocdoc.atlassian.net/browse/BILL-1219) | `zocdoc_web` |
| WEB-004 | [BILL-1220](https://zocdoc.atlassian.net/browse/BILL-1220) | `zocdoc_web` |

## Dropped from scope

This analysis answers three questions: **what isn't being checked, what's stale, and what has no
tests at all.** Four tickets were filed that answered a different question — they described
infrastructure, CI wiring, or file organisation. All four are deleted in Jira. The findings behind
them are real and are recorded here so they aren't lost, but they are not test-coverage work and
don't belong in a team's sprint backlog under this program.

| Was | Finding | Why it's out | Whose it is |
|---|---|---|---|
| PB-003 / BILL-1213 | The post-deploy smoke test is a bare `Assert.Pass` | Runs after release; this analysis is pre-release only | Deploy pipeline owner |
| PB-005 / BILL-1215 | LocalStack integration tests `Assert.Ignore` when LocalStack is down | The fix is CI environment detection, not a test | CI / pipeline owner — **but see the caveat below** |
| PB-006 / BILL-1216 | Three test projects named for a level they don't test at | File organisation. Its own write-up conceded no bug ships from a misnamed folder | `provider-billing` team, as hygiene |
| X-001 / BILL-1206 | No signal fails in the monorepo when a billing DOM change breaks a downstream suite | A CI tripwire, not a test. FE-001 is the test that covers this risk | Whoever owns the monorepo CI config |

**One caveat worth carrying forward from PB-005:** nobody confirmed that `provider-billing`'s 70 L3
integration tests actually execute in CI. If LocalStack isn't provisioned there, they skip silently
and that entire layer has never run. That *is* a coverage question — it's recorded in the limitations
of [`../START-HERE.md`](../START-HERE.md) rather than as a ticket, because the answer is a
five-minute look at the pipeline, not a sprint item.
