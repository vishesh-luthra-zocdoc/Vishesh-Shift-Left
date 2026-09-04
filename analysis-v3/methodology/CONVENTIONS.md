# v3 Analysis Conventions — READ BEFORE WRITING ANYTHING

## Test-Level Taxonomy (MANDATORY — use these exact labels)

Every test you catalogue MUST be assigned exactly one level. The whole point of v3
is that v1/v2 lumped "unit tests" together with component-render tests and called
Selenium "integration". Do not repeat that.

| Level | Label | Definition | Decides it |
|---|---|---|---|
| L1 | `unit` | One function/module in isolation. No React render, no HTTP, no DB, no browser. Pure logic, schemas, formatters, reducers, C# classes with all deps mocked. | Does it render a component or touch a boundary? If no → L1. |
| L2 | `component` | Renders ONE component in isolation (RTL/`render()`), props and hooks mocked. Fast, in-process, no real network. | Uses `render()`/`screen` but mocks its data layer → L2. |
| L3 | `integration` | Multiple real units together across a real boundary: real DB, real in-memory HTTP pipeline, LocalStack, MSW-backed fetching, multi-component tree with a real provider/context. No browser. | Real infra or 2+ real collaborators, still no browser → L3. |
| L4 | `api` | Exercises an HTTP surface and asserts the request/response contract (status, schema, headers). In-memory host or deployed endpoint. | Asserting on an HTTP contract → L4. |
| L5 | `e2e` | Real browser driving a running app in a real environment. Playwright, Selenium/WebDriver. | Browser involved → L5. |

Notes:
- A Jest file under `__tests__/` is NOT automatically L1. Read it. Most `*-tests.tsx` in
  this monorepo are **L2 component**, not L1 unit. Classify per `describe`/`it` block if a
  single file mixes levels, and say so.
- zocdoc_web `BillingTests`/`StripeTests` drive a browser → those are **L5 e2e**, even though
  v1 called them "Selenium integration". Call that out explicitly as a v1/v2 misclassification.
- If a file mixes levels, report it as `mixed` with a per-level breakdown, and flag it as a
  structural problem (mixed-level files can't be run selectively in CI).

## Output rules

- Write plain GitHub-flavored Markdown. Tables over prose.
- EVERY factual claim needs evidence: `path/to/file.ts:123`, a `describe`/`it` name, or a commit SHA.
- Give exact counts, never "~several". If you estimate, label it **(estimate)** and say why.
- Never invent a test, file, ticket ID, or SHA. If you cannot verify something, write
  `UNVERIFIED —` and state what you'd need. This document set will be turned into Jira
  tickets; a fabricated line becomes a bogus ticket someone wastes a sprint on.
- Record the exact git revision you analyzed at the top of every file you write.
- Keep it technical but readable. No hype, no "comprehensive"/"robust" filler.

## Gap → ticket rule

If you find a coverage gap, do NOT write the ticket yourself. Append a row to your file's
`## Candidate Gaps` section with: what's missing, correct test level, file path(s),
why it matters, rough effort, and your suggested priority (P0–P3). The orchestrator turns
these into ticket files. P0 = untested logic that can corrupt money/data. P3 = polish.
