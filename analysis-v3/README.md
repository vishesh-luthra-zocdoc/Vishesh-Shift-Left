# Billing Shift-Left Gap Analysis — v3

**Run date:** 2026-09-04 · **Prior runs:** v1 (2026-04-14), v2 (2026-04-23)
**Jira project:** BILL

Test coverage across every repository the Provider Billing team owns or materially touches, segregated
by **test level** (unit / component / integration / api / e2e), with every gap written as a
ready-to-file ticket.

---

## Start here

| If you want to… | Read |
|---|---|
| **File the tickets** | [`gaps/BACKLOG.md`](gaps/BACKLOG.md) — 18 tickets by priority, with sequencing |
| **Check my work before trusting it** | [`VERIFY-THIS-FIRST.md`](VERIFY-THIS-FIRST.md) — 10 min of copy-pasteable commands |
| **See what the team already fixed** | [`ALREADY-FIXED.md`](ALREADY-FIXED.md) |
| **Know what v2 got wrong** | [`V2-VALIDATION.md`](V2-VALIDATION.md) — **v2's #1 P0 is wrong, do not execute it** |
| **Understand the level taxonomy** | [`methodology/TEST-LEVEL-TAXONOMY.md`](methodology/TEST-LEVEL-TAXONOMY.md) |
| **Know how this was produced** | [`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md) |

## What's new in v3

1. **Tests are segregated by level, not by folder.** Classification is by what a test actually *does*.
   A browser test that mocks its entire backend is paying L5 cost for L2 confidence, whatever
   directory it lives in.
2. **All four repos**, not just the frontend. `provider-billing` — an entire .NET service with five
   test projects — was never in v1/v2 scope.
3. **Every gap is a ticket file**, with acceptance criteria, test cases, and a verification command.
   v1/v2 produced prose that had to be re-scoped before anyone could act.
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
| `sandbox` | `eef9429d` (`origin/main`) | 2026-09-04 |

**The staleness mattered:** `provider-billing`'s test projects were renamed and restructured between
June and September. Reading a local checkout would have described projects that no longer exist.

## Structure

```
analysis-v3/
├── README.md                  ← you are here
├── SUMMARY.md                 ← the findings in plain language
├── VERIFY-THIS-FIRST.md       ← spot-check the risky claims yourself
├── ALREADY-FIXED.md           ← what the team closed since v2
├── V2-VALIDATION.md           ← every v2 callout, re-checked
├── gaps/
│   ├── BACKLOG.md             ← the ticket index, by priority
│   ├── TICKET-TEMPLATE.md     ← the contract every ticket follows
│   └── tickets/               ← 18 self-contained ticket files
├── inventory/                 ← what tests exist, per repo, per level
├── shift-left/                ← the E2E reduction plan and its guard rails
└── methodology/               ← taxonomy, method, verified history
```

## Status

The frontend, `sandbox`, and cross-repo analysis is **complete and independently verified**.
Backend inventories (`zocdoc_web`, `provider-billing`) are in progress; `WEB-*` and `PB-*` tickets
land in a follow-up commit.

## Honest limitations

- **No coverage tooling was run.** Counts come from reading test files. A test existing is not proof
  it asserts anything useful.
- **Runtime figures are estimates** unless labelled otherwise. The serial-CI *basis* is confirmed.
- **Assertion quality and flakiness are out of scope**, except where specifically called out
  (FE-002, FE-004).
- Anything unconfirmable is written `UNVERIFIED — <what's needed>` rather than asserted.
