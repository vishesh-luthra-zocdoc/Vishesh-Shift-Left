# Test-Level Taxonomy

**Short version, if you only want the labels:**

| Level | What it means | Example from billing |
|---|---|---|
| **L1 — unit** | One function on its own | `formatDate` in `invoiceHelpers.ts` |
| **L2 — component** | One screen on its own | `EditMonthlyLimitModal` |
| **L3 — integration** | A few real pieces wired together | modal + real provider tree, or a LocalStack test |
| **L4 — api** | The API returns the fields the page expects | *(billing has none)* |
| **L5 — e2e** | A real browser clicking through billing | the Playwright billing specs |

Lower is better whenever it can catch the same bug: faster, runs on every PR, easier to debug. The
rest of this file is the exact decision procedure used to classify each test.

---

**This is the spine of the v3 analysis.** v1 and v2 counted "unit tests" and "E2E tests" and
nothing else. That hid two things: most of what the frontend calls a unit test is really a
component-render test, and most of what the monolith calls an integration test is really a
browser test. You cannot plan a shift-left if the levels are mislabelled, because
"move it down a level" has no defined destination.

Every test in this analysis is assigned exactly one of five levels.

---

## The five levels

| Level | Label | Definition | Runs in | Typical runtime |
|---|---|---|---|---|
| **L1** | `unit` | One function or module in isolation. No component render, no HTTP, no DB, no browser. | Process | < 10 ms |
| **L2** | `component` | Renders one component in isolation. Props and data hooks mocked. | Process (jsdom) | 10–200 ms |
| **L3** | `integration` | Two or more real collaborators across a real boundary — real DB, in-memory HTTP pipeline, LocalStack, MSW-backed fetching, real context/provider tree. No browser. | Process + local infra | 0.1–5 s |
| **L4** | `api` | Exercises an HTTP surface and asserts the request/response contract: status, schema, headers, error shape. | In-memory host or deployed endpoint | 0.1–2 s |
| **L5** | `e2e` | Real browser driving a running application. Playwright, Selenium/WebDriver. | Browser + environment | 5–120 s |

## How to decide the level

Ask these in order. The first "yes" wins.

1. **Is a browser involved?** → **L5**, regardless of what the folder is called.
2. **Is it asserting on an HTTP request/response contract?** → **L4**.
3. **Does it touch real infrastructure (DB, LocalStack, in-memory host) or wire together 2+ real
   collaborators?** → **L3**.
4. **Does it call `render()` on a component?** → **L2**.
5. **Otherwise** → **L1**.

## Classification rules that matter here

- **A file under `__tests__/` is not automatically L1.** In `provider-fe-monorepo`, the majority
  of `*-tests.tsx` files render components and are therefore **L2**. This is the single biggest
  correction v3 makes to v1/v2's numbers.
- **Selenium tests are L5, not "integration".** `zocdoc_web`'s `BillingTests` and `StripeTests`
  drive a browser. v1 catalogued them under "Selenium integration tests" and that framing led to
  the wrong conclusion about where their coverage should move.
- **A browser test that mocks its entire backend is not really an L5.** It pays L5 cost
  (browser boot, page load, flake) for L2 confidence. These are the highest-value shift-left
  targets and are flagged individually.
- **Mixed-level files are a defect.** A single file containing both L1 and L2 tests cannot be
  run selectively in CI — you can't have a fast pre-commit tier if the fast tests are trapped
  in a file with slow ones. These are called out where found.

## Why the level determines the ticket

The level is not a label for tidiness. It determines cost, so it determines priority:

| Level | Cost of one test | Failure diagnosis | Flake risk |
|---|---|---|---|
| L1 | Negligible | Points at one function | None |
| L2 | Very low | Points at one component | Very low |
| L3 | Low–moderate | Points at a boundary | Low |
| L4 | Low–moderate | Points at a contract | Low |
| L5 | High | "Something on the page broke" | High |

A gap at L1 is cheap to close and should be closed immediately. A gap at L5 is expensive and
needs to be justified against what it uniquely proves. Every ticket in `gaps/tickets/` names its
target level for exactly this reason.

## The shift-left verdicts

Tests are classified with one of these verdicts in `shift-left/SHIFT-LEFT-PLAN.md`:

| Verdict | Meaning |
|---|---|
| `keep-e2e` | Genuinely needs a browser and a real backend. Correct where it is. |
| `shift-to-L3` | Needs real collaborators, but not a browser. |
| `shift-to-L2` | Pure render/interaction/validation assertion. |
| `shift-to-L1` | Pure logic or formatting assertion. |
| `delete-redundant` | Already asserted by a named lower-level test. The covering test is cited. |
| `delete-suspected` | Looks redundant but the covering test could not be named. Needs a human check before deletion. |

`delete-redundant` requires citing the test that covers it. If it can't be cited, it is
`delete-suspected` instead. This distinction exists so nobody deletes coverage on the strength
of an unverified claim.

## Target shape

The current distribution is in [`../START-HERE.md`](../START-HERE.md); the reasoning behind the
proposed E2E reduction is in
[`../shift-left/E2E-PLAN-JUDGMENT.md`](../shift-left/E2E-PLAN-JUDGMENT.md). The goal is not a fixed
ratio — it is that each test sits at the **lowest level that can still prove what it needs to
prove**.
