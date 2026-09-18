# Billing Test Mappings

**Generated:** 2026-09-18 · **Skill:** `test-mapping` (Shift-Left)

Flat, SHA-pinned mappings of every billing test in the dev-owned repos. Each row carries the
test's name, what it tests, its concrete steps, a one-line summary, its level/scope, and a
permalink to the exact declaration line.

**4,707 rows across 421 test files in 3 repos.**

## Mappings

### `Zocdoc/provider-billing`

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`provider-billing-api-test-mapping.md`](provider-billing-api-test-mapping.md) | L4 api | 5 | 97 | `main` @ `166621f1c8` |
| [`provider-billing-cron-test-mapping.md`](provider-billing-cron-test-mapping.md) | L1 unit (cron) | 21 | 228 | `main` @ `166621f1c8` |
| [`provider-billing-integration-test-mapping.md`](provider-billing-integration-test-mapping.md) | L3 integration | 13 | 88 | `main` @ `166621f1c8` |
| [`provider-billing-unit-test-mapping.md`](provider-billing-unit-test-mapping.md) | L1/L2 unit + component | 33 | 350 | `main` @ `166621f1c8` |

### `Zocdoc/provider-fe-monorepo`

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`provider-fe-monorepo-playwright-billing-test-mapping.md`](provider-fe-monorepo-playwright-billing-test-mapping.md) | L5 e2e (Playwright) | 7 | 60 | `main` @ `9b3c308d21` |
| [`provider-fe-monorepo-unit-billing-test-mapping.md`](provider-fe-monorepo-unit-billing-test-mapping.md) | L1/L2 unit + component | 82 | 1033 | `main` @ `9b3c308d21` |

### `Zocdoc/zocdoc_web`

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`zocdoc_web-api-billing-test-mapping.md`](zocdoc_web-api-billing-test-mapping.md) | L4 api | 10 | 62 | `master` @ `fb4a8bd7b9` |
| [`zocdoc_web-cron-billing-test-mapping.md`](zocdoc_web-cron-billing-test-mapping.md) | L1 unit (cron) | 9 | 30 | `master` @ `fb4a8bd7b9` |
| [`zocdoc_web-integration-billing-test-mapping.md`](zocdoc_web-integration-billing-test-mapping.md) | L3 integration | 18 | 319 | `master` @ `fb4a8bd7b9` |
| [`zocdoc_web-selenium-billing-test-mapping.md`](zocdoc_web-selenium-billing-test-mapping.md) | L5 e2e (Selenium) | 27 | 149 | `master` @ `fb4a8bd7b9` |
| [`zocdoc_web-unit-billing-test-mapping.md`](zocdoc_web-unit-billing-test-mapping.md) | L1/L2 unit + component | 196 | 2291 | `master` @ `fb4a8bd7b9` |

## What is NOT here

- **`sandbox`** (QA-owned Cypress/Playwright vs production) — excluded by request.
- **`playwright-qa`** (QA-owned) — excluded by request.
- Assertion *quality* and flakiness. A mapped row proves a test exists and what it touches,
  not that it asserts anything useful. The Scope column flags conditional assertions and
  fully-mocked suites where the body shows it.

## Revisions

| Repo | Branch | Commit | Note |
|---|---|---|---|
| `provider-billing` | `main` | `166621f1c8` | matches `origin/main` at generation time |
| `provider-fe-monorepo` | `main` | `9b3c308d21` | local HEAD, 1 commit behind `origin/main` |
| `zocdoc_web` | `master` | `fb4a8bd7b9` | local HEAD, **1,161 commits behind** `origin/master` — see the note in each `zocdoc_web` mapping |

## Regenerating

Extractors and the renderer live in [`../scripts/`](../scripts/). Both extractors were
validated per-file against an independent attribute/block counter before rendering; the C#
extractor matches on all 260 `zocdoc_web` billing files and all 72 `provider-billing` files,
and the JS extractor matches `it`/`test` grep counts exactly (821 blocks / 82 files).

