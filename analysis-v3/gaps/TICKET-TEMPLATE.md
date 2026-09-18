# Ticket Template

Every file in [`tickets/`](tickets/) follows this exact shape. Nothing else goes in that folder.

**The contract:** each ticket file is self-contained and ready to paste into Jira with no extra
thinking. If you open one and still have to go read the code to understand what to do, the ticket
is wrong — fix the ticket, not the reader.

Filenames: `<REPO>-<nnn>-<kebab-slug>.md`, numbered in priority order **within each repo**
(`FE-001` is the highest-priority frontend gap).

| Prefix | Repo |
|---|---|
| `FE` | `provider-fe-monorepo` |
| `WEB` | `zocdoc_web` |
| `PB` | `provider-billing` |

Per-repo prefixes rather than one global sequence, for two reasons: you can tell which repo and
which team a ticket belongs to from the filename alone, and adding a repo later doesn't renumber
tickets you've already created in Jira.

These IDs are **local handles for this analysis only** — they are not Jira keys. Real Jira keys get
written back into [`BACKLOG.md`](BACKLOG.md) after creation, so the mapping stays traceable.

---

## Template

```markdown
# FE-001 — <imperative one-line title, this becomes the Jira Summary>

| Field | Value |
|---|---|
| Jira project | BILL |
| Issue type | Story |
| Priority | P0 \| P1 \| P2 \| P3 |
| Test level | L1 unit \| L2 component \| L3 integration \| L4 api \| L5 e2e |
| Action | add-coverage \| shift-left \| delete \| investigate |
| Repo | provider-fe-monorepo \| zocdoc_web \| provider-billing |
| Area | <e.g. Billing Settings — invoice formatting> |
| Estimate | <e.g. 45m / 2h / 1d> |
| Labels | qa-shift-left, <level>, test-coverage \| cleanup |
| Evidence revision | <commit SHA the finding was verified against> |

## Summary
One or two sentences. What is missing or wrong, and what this ticket delivers.

## Context
Why this code exists and what it does, for someone who has never opened it. Two to four sentences.

## Current state
What coverage exists today, with file:line evidence. If the answer is "none", say none and cite
the source file that is uncovered. If coverage is indirect, name the test that provides it.

## Why this matters
The concrete failure this gap allows. Not "improves quality" — describe the bug that ships.
State the blast radius: who sees it, and whether money or provider-facing data is involved.

## Acceptance criteria
- [ ] Specific, checkable outcomes.
- [ ] Each names the file to create or change.
- [ ] The last one is always a verification step (the command that proves it, e.g. `yarn test <path>`).

## Test cases to write
| # | Input / scenario | Expected |
|---|---|---|
| 1 | ... | ... |

For `shift-left` and `delete` tickets, this section instead lists the tests being moved or
removed, with their current location and their destination.

## Files
| Path | Change |
|---|---|
| `path/to/thing.ts` | read only — subject under test |
| `path/to/__tests__/thing-tests.ts` | **create** |

## Out of scope
What this ticket deliberately does not do. Prevents scope creep and reviewer confusion.

## Verification
The exact command(s) to run, and what passing looks like.

## Notes
Optional. Dependencies on other GAP tickets, rollout gates, staleness caveats, open questions
for the assignee.
```

---

## Field rules

- **Priority** — assigned on failure impact, not effort:
  | | Meaning |
  |---|---|
  | **P0** | Untested logic that can corrupt money, billing data, or provider-facing amounts. Also: tests asserting against code that no longer exists (actively misleading). |
  | **P1** | Untested logic with a real user-visible failure mode, or a shift-left with material CI cost. |
  | **P2** | Meaningful coverage gap, low blast radius. |
  | **P3** | Polish. Presentational components, completeness-only additions. |

- **Action** — `add-coverage` (new tests), `shift-left` (move existing tests down a level),
  `delete` (remove dead or redundant tests), `investigate` (a question must be answered before
  work can be scoped; the deliverable is an answer, not a test).

- **Estimate** — realistic hands-on-keyboard time, excluding review. If it exceeds one day, the
  ticket is too big and must be split.

- **Evidence revision** — the commit SHA the finding was verified against, so a stale finding is
  detectable later. Findings verified against a stale checkout say so in **Notes**.

## Rules that keep these trustworthy

1. **No fabricated evidence.** Every file path, `it` title, and SHA is one that was actually read.
   Anything unverified is written as `UNVERIFIED — <what's needed>` and never silently asserted.
2. **`delete` tickets must cite their replacement.** A ticket that removes coverage names the
   test that still covers the behaviour, or it is downgraded to `investigate`.
3. **`investigate` tickets state their decision rule** — what answer leads to what follow-up
   action — so the outcome is actionable rather than just informational.
