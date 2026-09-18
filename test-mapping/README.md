# Test Mapping

**Generated:** 2026-09-18 · **Skill:** `test-mapping`

Flat, SHA-pinned mappings of every billing test in the dev-owned repos. Each row carries the
test's name, what it tests, its concrete steps, a one-line summary, its L1–L5 scope, and a
permalink to the exact declaration line at a pinned commit.

**4,939 rows across 440 test files in 3 repos.**

## Repos

| Repo | Mappings | Test files | Rows |
|---|---|---:|---:|
| [`provider-billing/`](provider-billing/) | api, integration, unit | 72 | 763 |
| [`provider-fe-monorepo/`](provider-fe-monorepo/) | e2e, unit | 89 | 1093 |
| [`zocdoc_web/`](zocdoc_web/) | api, e2e, integration, unit | 279 | 3083 |
| **Total** | | **440** | **4939** |

### [`provider-billing/`](provider-billing/)

`Zocdoc/provider-billing` — The billing service — .NET. All five test projects under `tests/` are mapped: `UnitTests` and `BillingExportCron.UnitTests` (both in the unit mapping), `IntegrationTests`, `ApiTests`, and `SmokeTests` (one service-reachability test, in the api mapping).

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`api-test-mapping.md`](provider-billing/api-test-mapping.md) | L4 api | 5 | 97 | `main` @ `166621f1c8` |
| [`integration-test-mapping.md`](provider-billing/integration-test-mapping.md) | L3 integration | 13 | 88 | `main` @ `166621f1c8` |
| [`unit-test-mapping.md`](provider-billing/unit-test-mapping.md) | L1/L2 unit + component | 54 | 578 | `main` @ `166621f1c8` |

### [`provider-fe-monorepo/`](provider-fe-monorepo/)

`Zocdoc/provider-fe-monorepo` — Provider-facing frontend monorepo. Scoped to billing surfaces by path (billing settings, payment recovery, payment-method components), not by filename keyword — keyword scoping pulled in unrelated SPO and provider-photo tests.

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`e2e-test-mapping.md`](provider-fe-monorepo/e2e-test-mapping.md) | L5 e2e | 7 | 60 | `main` @ `9b3c308d21` |
| [`unit-test-mapping.md`](provider-fe-monorepo/unit-test-mapping.md) | L1/L2 unit + component | 82 | 1033 | `main` @ `9b3c308d21` |

### [`zocdoc_web/`](zocdoc_web/)

`Zocdoc/zocdoc_web` — The C#/.NET monolith. Scoped to 17 billing test directories spanning `Billing/`, `ZocBill/`, the billing APIs, Zocron tasks, CSR, and the Selenium billing suites.

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`api-test-mapping.md`](zocdoc_web/api-test-mapping.md) | L4 api | 22 | 144 | `master` @ `b306dc12f4` |
| [`e2e-test-mapping.md`](zocdoc_web/e2e-test-mapping.md) | L5 e2e | 26 | 147 | `master` @ `b306dc12f4` |
| [`integration-test-mapping.md`](zocdoc_web/integration-test-mapping.md) | L3 integration | 20 | 381 | `master` @ `b306dc12f4` |
| [`unit-test-mapping.md`](zocdoc_web/unit-test-mapping.md) | L1/L2 unit + component | 211 | 2411 | `master` @ `b306dc12f4` |

## How mappings are split

One file per **test level**, not per suite or per tool:

| File | Level | What lands here |
|---|---|---|
| `unit-test-mapping.md` | L1 / L2 | Isolated logic with mocked collaborators. Component tests that render UI are marked **L2 component**. Cron/scheduled-task handler tests live here too, marked **L1 unit (cron handler)** — they are unit tests of a job, not a separate level. |
| `integration-test-mapping.md` | L3 | Crosses a real boundary — SQL persistence, multi-collaborator flows. |
| `api-test-mapping.md` | L4 | Asserts HTTP request/response contracts. |
| `e2e-test-mapping.md` | L5 | Drives a real browser. The tool (Playwright or Selenium) is named in the document title, not the filename. |

## Reading a mapping

One table per test file, `#` numbered continuously through the document. Columns:

| Column | Meaning |
|---|---|
| **Test Name** | The declared test method / `it` block. Parametrized cases get one row each. |
| **What It Tests** | Fixture or suite context plus the humanized test name. |
| **Steps** | Concrete actions read out of the body — mocks, HTTP verbs and routes, UI actions, assertions. |
| **Summary** | One line, including the assertion count. |
| **Scope** | L1–L5 level, the unit under test, and flags: `[Ignore]`, `skipped`, `.only`, `retry-on-fail`, `CI-gated`, combinatorial `[Values]`, and `CONDITIONAL assertion — can pass as a no-op`. |
| **Source Code** | Permalink to the declaration line at the pinned full SHA. |

## What is NOT here

- **`sandbox`** (QA-owned Cypress/Playwright vs production) — excluded by request.
- **`playwright-qa`** (QA-owned) — excluded by request.
- Assertion *quality* and flakiness. A mapped row proves a test exists and what it touches, not
  that it asserts anything useful. The Scope column flags conditional assertions and
  fully-mocked suites where the body shows it.

## Revisions

| Repo | Branch | Commit | Note |
|---|---|---|---|
| `provider-billing` | `main` | `166621f1c8` | matches `origin/main` at generation time |
| `provider-fe-monorepo` | `main` | `9b3c308d21` | local HEAD, 1 commit behind `origin/main` |
| `zocdoc_web` | `master` | `b306dc12f4` | current `origin/master` tip (2026-09-18) |

See [`CHANGELOG.md`](CHANGELOG.md) for per-run diffs and verification notes.

## Regenerating

Extractors and the renderer live in [`tools/`](tools/). Both extractors are validated
per-file against an independent method/block counter before rendering: the C# extractor matches
on all 279 `zocdoc_web` billing files and all 72 `provider-billing` files, and the JS extractor
matches `it`/`test` grep counts exactly (821 blocks / 82 files).

