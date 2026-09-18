# Kinds of test

**Short version, if you only want the labels:**

| Kind of test | What it means | Example from billing |
|---|---|---|
| **Unit test** | One function on its own | `formatDate` in `invoiceHelpers.ts` |
| **Component test** | One screen on its own | `EditMonthlyLimitModal` |
| **Integration test** | A few real pieces wired together | modal + real provider tree, or a LocalStack test |
| **API contract test** | The API returns the fields the page expects | *(billing has none)* |
| **Browser test** | A real browser clicking through billing | the Playwright billing specs |

A cheaper kind of test is better whenever it can catch the same bug: faster, runs on every PR, easier to debug. The
rest of this file is the exact decision procedure used to classify each test.

---

**This is the spine of the v3 analysis.** v1 and v2 counted "unit tests" and "E2E tests" and
nothing else. That hid two things: most of what the frontend calls a unit test is really a
component-render test, and most of what the monolith calls an integration test is really a
browser test. You cannot plan a shift-left if tests are mislabelled, because
"make it a cheaper test" has no defined destination.

Every test in this analysis is assigned exactly one of five kinds.

---

## The five kinds

| Kind of test | Label | Definition | Runs in | Typical runtime |
|---|---|---|---|---|
| **Unit** | `unit` | One function or module in isolation. No component render, no HTTP, no DB, no browser. | Process | < 10 ms |
| **Component** | `component` | Renders one component in isolation. Props and data hooks mocked. | Process (jsdom) | 10–200 ms |
| **Integration** | `integration` | Two or more real collaborators across a real boundary — real DB, in-memory HTTP pipeline, LocalStack, MSW-backed fetching, real context/provider tree. No browser. | Process + local infra | 0.1–5 s |
| **API contract** | `api` | Exercises an HTTP surface and asserts the request/response contract: status, schema, headers, error shape. | In-memory host or deployed endpoint | 0.1–2 s |
| **Browser** | `e2e` | Real browser driving a running application. Playwright, Selenium/WebDriver. | Browser + environment | 5–120 s |

## How to decide which kind a test is

Ask these in order. The first "yes" wins.

1. **Is a browser involved?** → **Browser**, regardless of what the folder is called.
2. **Is it asserting on an HTTP request/response contract?** → **API contract**.
3. **Does it touch real infrastructure (DB, LocalStack, in-memory host) or wire together 2+ real
   collaborators?** → **Integration**.
4. **Does it call `render()` on a component?** → **Component**.
5. **Otherwise** → **Unit**.

## Classification rules that matter here

- **A file under `__tests__/` is not automatically a unit test.** In `provider-fe-monorepo`, the majority
  of `*-tests.tsx` files render components and are therefore **component tests**. This is the single biggest
  correction v3 makes to v1/v2's numbers.
- **Selenium tests are browser tests, not "integration" tests.** `zocdoc_web`'s `BillingTests` and `StripeTests`
  drive a browser. v1 catalogued them under "Selenium integration tests" and that framing led to
  the wrong conclusion about where their coverage should move.
- **A browser test that mocks its entire backend is not really a browser test.** It pays browser-test cost
  (browser boot, page load, flake) for component-test confidence. These are the highest-value shift-left
  targets and are flagged individually.
- **Files mixing two kinds are a defect.** A single file containing both unit and component tests cannot be
  run selectively in CI — you can't have a fast pre-commit tier if the fast tests are trapped
  in a file with slow ones. These are called out where found.

## Why the kind of test determines the ticket

The kind of test is not a label for tidiness. It determines cost, so it determines priority:

| Kind of test | Cost of one test | Failure diagnosis | Flake risk |
|---|---|---|---|
| Unit | Negligible | Points at one function | None |
| Component | Very low | Points at one component | Very low |
| Integration | Low–moderate | Points at a boundary | Low |
| API contract | Low–moderate | Points at a contract | Low |
| Browser | High | "Something on the page broke" | High |

A missing unit test is cheap to add and should be added immediately. A missing browser test is expensive and
needs to be justified against what it uniquely proves. Every ticket in `gaps/tickets/` names the kind of test
it targets for exactly this reason.

## The shift-left verdicts

Tests are classified with one of these verdicts in [`../shift-left/E2E-TEST-BY-TEST.md`](../shift-left/E2E-TEST-BY-TEST.md):

| Verdict | Meaning |
|---|---|
| `keep-e2e` | Genuinely needs a browser and a real backend. Correct where it is. |
| `shift-to-integration` | Needs real collaborators, but not a browser. |
| `shift-to-component` | Pure render/interaction/validation assertion. |
| `shift-to-unit` | Pure logic or formatting assertion. |
| `delete-redundant` | Already asserted by a named cheaper test. The covering test is cited. |
| `delete-suspected` | Looks redundant but the covering test could not be named. Needs a human check before deletion. |

`delete-redundant` requires citing the test that covers it. If it can't be cited, it is
`delete-suspected` instead. This distinction exists so nobody deletes coverage on the strength
of an unverified claim.

## Target shape

The current distribution is in [`../SUMMARY.md`](../SUMMARY.md); the reasoning behind the
proposed E2E reduction is in
[`../shift-left/E2E-PLAN-JUDGMENT.md`](../shift-left/E2E-PLAN-JUDGMENT.md). The goal is not a fixed
ratio — it is that each test is the **cheapest kind that can still prove what it needs to
prove**.
