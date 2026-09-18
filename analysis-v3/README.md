# Billing Shift-Left Gap Analysis — v3

**Run date:** 2026-09-04 · **Prior runs:** v1 (2026-04-14), v2 (2026-04-23)
**Jira:** project BILL, epic [BILL-746](https://zocdoc.atlassian.net/browse/BILL-746)

**→ [`SUMMARY.md`](SUMMARY.md) is the analysis.** One page: what needs testing, at what priority,
at what test level, and what to do first. Everything else in this folder is supporting detail for it.

**Scope:** pre-release automated tests in the repos the Provider Billing team owns or materially
touches — `provider-fe-monorepo`, `provider-billing`, `zocdoc_web`. The QA-owned `sandbox` repo is
**not** in scope; it's handled separately.

This analysis answers three questions and nothing else: **what isn't being checked, what's stale,
and what has no tests at all.** CI wiring, deploy pipelines, and file organisation are out of scope.

---

## Where to go

| If you want to… | Read |
|---|---|
| **Understand the whole thing** | [`SUMMARY.md`](SUMMARY.md) — 20 numbered findings, P0 → P3, with effort |
| **File or work the tickets** | [`gaps/BACKLOG.md`](gaps/BACKLOG.md) — the same items with Jira keys and sequencing |
| **Read one gap in full** | [`gaps/tickets/`](gaps/tickets/) — 13 self-contained frontend tickets |
| **Check my work before trusting it** | [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md) — 10 min of copy-pasteable commands |
| **See what the team already fixed** | [`ALREADY-FIXED.md`](ALREADY-FIXED.md) |
| **Know what v2 got wrong** | [`V2-VALIDATION.md`](V2-VALIDATION.md) — **v2's #1 P0 is wrong, do not execute it** |
| **Understand the L1–L5 labels** | [`methodology/TEST-LEVEL-TAXONOMY.md`](methodology/TEST-LEVEL-TAXONOMY.md) |
| **Know how this was produced** | [`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md) |

## What's new in v3

1. **Tests are grouped by what they actually do, not by folder.** A browser test that mocks its
   entire backend is paying L5 cost for L2 confidence, whatever directory it lives in. The five
   levels (L1 unit → L5 e2e) are explained in plain terms at the top of [`SUMMARY.md`](SUMMARY.md).
2. **All three team-owned repos**, not just the frontend. `provider-billing` — an entire .NET
   service with five test projects — was never in v1/v2 scope.
3. **Frontend gaps are full ticket files**, with acceptance criteria, test cases, and a verification
   command. v1/v2 produced prose that had to be re-scoped before anyone could act.
4. **v2's callouts were re-validated.** One of eight was wrong — and it was v2's top-priority item,
   recommending deletion of live code.

## Revisions analyzed

Findings are only true as of a revision. Local checkouts were **not** used — `provider-fe-monorepo`
was 550 commits behind, which is exactly the error that made v2 stale. Snapshots were exported from
each remote's tip.

| Repo | Revision | Date |
|---|---|---|
| `provider-fe-monorepo` | `dd9e4952a6` (`origin/main`) | 2026-09-03 |
| `provider-billing` | `84318e3d5c` (`main`) | 2026-09-03 |
| `zocdoc_web` | `8742b5072da` (`master`) | 2026-09-04 |

**The staleness mattered:** `provider-billing`'s test projects were renamed and restructured between
June and September. Reading a local checkout would have described projects that no longer exist.

## Structure

```
analysis-v3/
├── SUMMARY.md                 ← read this. The whole analysis, one page.
├── README.md                  ← you are here (scope, revisions, structure)
├── VERIFY-THIS-FIRST.md       ← spot-check the risky claims yourself
├── ALREADY-FIXED.md           ← what the team closed since v2
├── V2-VALIDATION.md           ← every v2 callout, re-checked
├── gaps/
│   ├── BACKLOG.md             ← the ticket index, by priority, with Jira keys
│   ├── TICKET-TEMPLATE.md     ← the contract every ticket follows
│   └── tickets/               ← 13 self-contained frontend ticket files
├── inventory/                 ← what tests exist, per repo, per level
├── shift-left/                ← the E2E reduction plan and its guard rails
└── methodology/               ← taxonomy, method, verified history
```

## Honest limitations

- **Three filed tickets were withdrawn as out of scope** (BILL-1206, BILL-1213, BILL-1215) — they
  described CI wiring or deploy checks rather than test coverage, and are deleted in Jira. See
  "Dropped from scope" in [`gaps/BACKLOG.md`](gaps/BACKLOG.md), which records the findings so they
  aren't lost. One more (BILL-1216) is kept but flagged as hygiene, not coverage.
- **`provider-billing`'s ~70 L3 integration tests may not execute in CI** — they skip when LocalStack
  is unavailable and provisioning was never confirmed. Treat the L3 count as unverified.
- **`provider-billing` and `zocdoc_web` findings exist only in Jira.** Their per-ticket write-ups and
  inventories were never committed here. The Jira ticket is the only detail for those seven items.
- **No coverage tooling was run.** Counts come from reading test files. A test existing is not proof
  it asserts anything useful.
- **Runtime figures are estimates** unless labelled otherwise. The serial-CI *basis* is confirmed.
- **Assertion quality and flakiness are out of scope**, except where specifically called out
  (FE-002, FE-004).
- Anything unconfirmable is written `UNVERIFIED — <what's needed>` rather than asserted.
