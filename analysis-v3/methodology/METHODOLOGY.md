# Methodology — v3

**Run date:** 2026-09-04
**Prior runs:** v1 (2026-04-14), v2 (2026-04-23)
**Scope:** billing test coverage across every repository owned or materially touched by the
Provider Billing team.

---

## What changed in the approach

v1 and v2 answered "how many tests are there, and which components lack one". That was the right
first question, but it produced a plan that could not survive a framework change — and a framework
change is exactly what happened. Cypress was deleted from `provider-fe-monorepo` between v2 and
v3, which invalidated v2's entire shift-left plan.

v3 changes three things:

1. **Tests are segregated by level, not by folder.** See
   [`KINDS-OF-TEST.md`](KINDS-OF-TEST.md). Classification is by what a test actually
   does, not by which directory it sits in or what the team calls it.
2. **Scope covers all three team-owned repos**, not just the frontend monorepo. v1/v2 treated the backend as a
   footnote and never looked at the `provider-billing` service at all.
3. **Every gap is written as a ticket-ready file**, one per ticket, with acceptance criteria and
   verification. See [`../gaps/TICKET-TEMPLATE.md`](../gaps/TICKET-TEMPLATE.md). v1/v2 produced
   prose findings that then had to be re-read and re-scoped before anyone could act on them.

## Repositories in scope

Scope is **pre-release tests in team-owned repos**. The QA-owned `sandbox` repo (Playwright against
production `zocdoc.com`) is post-release and out of scope — it is analyzed separately. Where a
`sandbox` observation explains a monorepo gap it is cited as evidence, but no `sandbox` gap is filed
here.

| Repo | What it holds | Levels present |
|---|---|---|
| `provider-fe-monorepo` | Billing Settings UI (`apps/settings`), shared payment components (`shared/core`) | unit, component, browser |
| `zocdoc_web` | Billing monolith — bill generation, charges, Stripe, chargebacks, tax | unit, API contract, browser |
| `provider-billing` | Provider Billing service (.NET) — Web API, lambdas, cron jobs | unit, integration, API contract |

## Repositories considered and excluded

Determined by searching the `Zocdoc` GitHub org for `billing`, `payment`, `invoice`, `stripe`, and
`revenue`, then inspecting each candidate's tree for a test suite.

| Repo | Last activity | Why excluded |
|---|---|---|
| `billing-redesign` | 2026-04-03 | Design prototype. No test suite. |
| `billing-org-level` | 2026-04-21 | Design prototype. No test suite. |
| `billing-org-level-v1-2` | 2026-08-24 | Design prototype (`dist/` of generated components). No test suite. |
| `billing-collab` | 2026-09-02 | Explicitly non-production: POCs, helper scripts, bastion setup. |
| `Billing` | 2023-01-28 | Dead. |
| `billing_landscape` | 2021-10-06 | Dead. |
| `billing-2026-h2-estimates` | 2026-07-24 | Planning documents. |
| `zvs-video-visits` | 2026-09-03 | Has payments code, but ZVS-owned, not Provider Billing. Out of team scope — revisit if ownership changes. |

## Revisions analyzed

Recording these matters: a finding is only true as of a revision, and two of these repos could not
be refreshed.

| Repo | Revision analyzed | Date | Freshness |
|---|---|---|---|
| `provider-fe-monorepo` | `dd9e4952a6` (`origin/main`) | 2026-09-03 | Current |
| `zocdoc_web` | see `../inventory/zocdoc_web/` | — | See note below |
| `provider-billing` | see `../inventory/provider-billing/` | — | See note below |

**Snapshot technique.** The local `provider-fe-monorepo` working tree was 550 commits behind
`origin/main`, so analyzing it directly would have produced findings about deleted code — which is
precisely the error that would have made v3 as stale as v2. Instead the billing subtrees were
exported from `origin/main` with `git archive` into a scratch snapshot and analyzed there. The
same care applies to any repo whose working tree is not level with its remote.

## How the analysis was produced

Parallel agents, one per repo-and-level slice, each working from a fixed revision against a shared
conventions document that defines the kinds of test, the evidence requirements, and the prohibition on
unverified claims. Findings were then cross-referenced centrally to produce the gap list, the
shift-left plan, and the diff against v2.

Cross-references performed:

1. Source file → does a test exist, at which level? (finds uncovered code)
2. Same behaviour asserted at two levels? (finds redundancy — the shift-left and delete candidates)
3. E2E test → does it mock its backend? (finds tests paying browser-test cost for component-test confidence)
4. v2 finding → still true at v3 revision? (finds what the team actually fixed, and what v2 got wrong)
5. Monorepo billing DOM → the `data-test` attributes the downstream production suite depends on
   (finds implicit cross-repo coupling with no CI signal — recorded as context, not filed as a
   ticket, since the remedy is CI wiring rather than a test)

## Evidence standard

Every claim carries a `file:line`, a verbatim `describe`/`it` title, or a commit SHA. Counts are
exact; anything inferred is labelled **(estimate)** with the basis stated. Anything that could not
be confirmed is written as `UNVERIFIED` rather than asserted, because these documents become Jira
tickets and a fabricated line becomes a ticket that wastes a sprint.

## Known limitations

1. **Coverage percentages are not reported.** No coverage tooling was executed as part of this
   analysis; counts are derived from reading test files. A test existing is not proof that it
   asserts anything useful — where a test looked weak it is noted, but this analysis measures
   presence and level, not assertion quality.
2. **Runtime figures are estimates** unless taken from a real CI run, and are labelled as such.
3. **Local checkouts could not be refreshed.** The agentic sandbox denies writes to their `.git`
   directories, so `git fetch` failed. Findings were taken from remote snapshots instead; see
   [`REVISIONS.md`](REVISIONS.md).
4. **Assertion quality and flakiness are out of scope.** Both matter and both deserve their own
   pass; mixing them into a coverage inventory would have made this one unreadable.
