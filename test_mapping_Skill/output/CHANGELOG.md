# Test Mapping Changelog

One entry per generation run, newest on top. Test identity key is
`<repo-relative-path>::<TestName>[ (CaseName)]`.

## 2026-09-18 — initial mapping

First run — no prior mapping existed in this output directory, so every file below is new.
Subsequent runs will diff against the `commit:` recorded in each mapping's
`<!-- test-mapping-meta -->` header and list Added / Removed / Renamed / Modified / Line shifts.

| Mapping | Repo | Branch | Commit | Type | Test files | Rows |
|---|---|---|---|---|---:|---:|
| [`provider-billing-api-test-mapping.md`](provider-billing-api-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | api | 5 | 97 |
| [`provider-billing-cron-test-mapping.md`](provider-billing-cron-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | cron | 21 | 228 |
| [`provider-billing-integration-test-mapping.md`](provider-billing-integration-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | integration | 13 | 88 |
| [`provider-billing-unit-test-mapping.md`](provider-billing-unit-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | unit | 33 | 350 |
| [`provider-fe-monorepo-playwright-billing-test-mapping.md`](provider-fe-monorepo-playwright-billing-test-mapping.md) | `Zocdoc/provider-fe-monorepo` | `main` | `9b3c308d21` | playwright | 7 | 60 |
| [`provider-fe-monorepo-unit-billing-test-mapping.md`](provider-fe-monorepo-unit-billing-test-mapping.md) | `Zocdoc/provider-fe-monorepo` | `main` | `9b3c308d21` | unit | 82 | 1033 |
| [`zocdoc_web-api-billing-test-mapping.md`](zocdoc_web-api-billing-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `fb4a8bd7b9` | api | 10 | 62 |
| [`zocdoc_web-cron-billing-test-mapping.md`](zocdoc_web-cron-billing-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `fb4a8bd7b9` | cron | 9 | 30 |
| [`zocdoc_web-integration-billing-test-mapping.md`](zocdoc_web-integration-billing-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `fb4a8bd7b9` | integration | 18 | 319 |
| [`zocdoc_web-selenium-billing-test-mapping.md`](zocdoc_web-selenium-billing-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `fb4a8bd7b9` | selenium | 27 | 149 |
| [`zocdoc_web-unit-billing-test-mapping.md`](zocdoc_web-unit-billing-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `fb4a8bd7b9` | unit | 196 | 2291 |
| **Total** | | | | | **421** | **4707** |

### Scope note

QA-team-owned E2E suites are **out of scope** by request: the `sandbox` repo (Cypress/Playwright
against production) and `playwright-qa`. Only dev-owned test suites are mapped, plus the
`zocdoc_web` Selenium billing tests, which the repo owner asked to include.

### Row counts vs declared tests

Rows expand parametrized cases: one row per `[TestCase]` / `[InlineData]` / `it.each` entry,
all sharing their parent method's declaration line. So rows > declared test blocks. Verified
declared-block counts: `provider-billing` 702 methods, `provider-fe-monorepo` billing 821
`it`/`test` blocks + 60 Playwright tests, `zocdoc_web` billing 2,323 methods.

