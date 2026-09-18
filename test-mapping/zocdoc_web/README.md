# zocdoc_web — Billing Test Mapping

`Zocdoc/zocdoc_web` — The C#/.NET monolith. Scoped to 17 billing test directories spanning `Billing/`, `ZocBill/`, the billing APIs, Zocron tasks, CSR, and the Selenium billing suites.

**3,083 rows across 279 test files.**

| Mapping | Level | Test files | Rows | Revision |
|---|---|---:|---:|---|
| [`api-test-mapping.md`](api-test-mapping.md) | L4 api | 22 | 144 | `master` @ `b306dc12f4` |
| [`cron-test-mapping.md`](cron-test-mapping.md) | L1 unit (cron) | 9 | 30 | `master` @ `b306dc12f4` |
| [`integration-test-mapping.md`](integration-test-mapping.md) | L3 integration | 20 | 381 | `master` @ `b306dc12f4` |
| [`selenium-test-mapping.md`](selenium-test-mapping.md) | L5 e2e (Selenium) | 26 | 147 | `master` @ `b306dc12f4` |
| [`unit-test-mapping.md`](unit-test-mapping.md) | L1/L2 unit + component | 202 | 2381 | `master` @ `b306dc12f4` |

Each mapping opens with a `<!-- test-mapping-meta -->` header recording the repo, branch,
commit and test type it was generated from. Links are pinned to the full SHA and will not
drift.

← [All repos](../README.md) · [Changelog](../CHANGELOG.md)

