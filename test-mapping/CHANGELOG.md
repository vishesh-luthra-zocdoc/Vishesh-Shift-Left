# Test Mapping Changelog

Newest entry on top. Test identity key is `<repo-relative-path>::<Class>.<TestName>`.

## 2026-09-18 — one file per test level; `scripts/` → `tools/`

Reorganized so each repo folder holds exactly one mapping per **test level**. No test content
changed — 4,939 rows across 440 files, same as the previous run.

**`cron-test-mapping.md` is gone, folded into `unit-test-mapping.md`.** Cron was never a test
level; those files held L1 unit tests whose subject happened to be a scheduled job, so listing
them beside `unit` / `integration` / `api` implied a level that does not exist. Every folded row
keeps **`L1 unit (cron handler)`** in its Scope column, so the subset is still filterable:

| Repo | Cron suite folded in | Tests | Unit mapping now |
|---|---|---:|---|
| `provider-billing` | `tests/BillingExportCron.UnitTests` | 228 | 350 → **578** rows |
| `zocdoc_web` | `Zocron/Zocron.Tasks.Tests/Billing` | 30 | 2,381 → **2,411** rows |

Worth knowing: 43 of the `provider-billing` cron tests drive a real in-memory EF context and are
flagged as such in Scope. They sit closest to the L1/L3 boundary and are the ones to look at first
if this split gets revisited.

**`playwright-` / `selenium-` → `e2e-test-mapping.md`.** Same reasoning: the filename now names the
level, and the tool is named in the document title and intro. Both files keep their tool-specific
Scope notes — Selenium rows say *drives a real browser; slow and order-sensitive*, Playwright rows
say *no real backend or Stripe*.

**`scripts/` → `tools/`.** The extractors, renderer, `awk` baseline and two scope files are
tooling for regenerating the mappings, not deliverables; the old name sat at the same level as the
repo folders and read like content.

Resulting layout:

| Mapping | Repo | Branch | Commit | Level | Test files | Rows |
|---|---|---|---|---|---:|---:|
| [`provider-billing/api`](provider-billing/api-test-mapping.md) | `provider-billing` | `main` | `166621f1c8` | L4 api | 5 | 97 |
| [`provider-billing/integration`](provider-billing/integration-test-mapping.md) | `provider-billing` | `main` | `166621f1c8` | L3 integration | 13 | 88 |
| [`provider-billing/unit`](provider-billing/unit-test-mapping.md) | `provider-billing` | `main` | `166621f1c8` | L1/L2 unit | 54 | 578 |
| [`provider-fe-monorepo/e2e`](provider-fe-monorepo/e2e-test-mapping.md) | `provider-fe-monorepo` | `main` | `9b3c308d21` | L5 e2e | 7 | 60 |
| [`provider-fe-monorepo/unit`](provider-fe-monorepo/unit-test-mapping.md) | `provider-fe-monorepo` | `main` | `9b3c308d21` | L1/L2 unit | 82 | 1033 |
| [`zocdoc_web/api`](zocdoc_web/api-test-mapping.md) | `zocdoc_web` | `master` | `b306dc12f4` | L4 api | 22 | 144 |
| [`zocdoc_web/e2e`](zocdoc_web/e2e-test-mapping.md) | `zocdoc_web` | `master` | `b306dc12f4` | L5 e2e | 26 | 147 |
| [`zocdoc_web/integration`](zocdoc_web/integration-test-mapping.md) | `zocdoc_web` | `master` | `b306dc12f4` | L3 integration | 20 | 381 |
| [`zocdoc_web/unit`](zocdoc_web/unit-test-mapping.md) | `zocdoc_web` | `master` | `b306dc12f4` | L1/L2 unit | 211 | 2411 |
| **Total** | | | | | **440** | **4939** |

## 2026-09-18 — re-map `zocdoc_web` against current `origin/master`

The five `zocdoc_web` mappings were regenerated from `origin/master` at `b306dc12f4`
(2026-09-18, current tip), replacing the first run pinned to `fb4a8bd7b9`, which was 1,161
commits behind. The `provider-billing` and `provider-fe-monorepo` mappings are unchanged.

**Across all five `zocdoc_web` suites:**

- **367 tests added**, **124 removed**, **7 reclassified**
- **726 line-shifted** (same test, moved declaration line)
- Test files 260 → **279** (+27 / −8)
- Total tests 2323 → **2566**

Added/removed/reclassified are computed globally, not per-suite, so a test that moved between
suites is counted once as a reclassification rather than as both an add and a removal.

| Suite | Tests | Test files |
|---|---|---|
| unit | 1816 → **1973** | 196 → **202** |
| integration | 273 → **283** | 18 → **20** |
| api | 60 → **138** | 10 → **22** |
| cron | 26 → **26** | 9 → **9** |
| selenium | 148 → **146** | 27 → **26** |
| **total** | 2323 → **2566** | 260 → **279** |

### Reclassification — a fix to the previous run, not repo churn

**7 tests moved unit → integration.** Two `AppCode.SlowTests` billing files were assigned to the
unit suite in the first run, which was wrong — `Tests/ZocDoc.AppCode.SlowTests/**` crosses a
real boundary and belongs at L3. Both are now in the integration mapping:

- `Tests/ZocDoc.AppCode.SlowTests/Billing/CreditCardTriggerTests.cs`
- `Tests/ZocDoc.AppCode.SlowTests/CS/Billing/PricingOptionTest.cs`

They existed at `fb4a8bd7b9` too, so this is a correction to the earlier mapping's grouping.

### Files removed since the last mapping

- `Billing/BillProcessor/BillingTests/Tests/Charge/ECheckChargeServiceTests.cs`
- `Billing/BillProcessor/BillingTests/Tests/Charge/StripeChargeServiceTest.cs`
- `Billing/BillProcessor/BillingTests/Tests/Charge/StripeSandboxAllowedProvidersTests.cs`
- `Billing/ZocDoc.Billing.Tests/BillingFeatureFlagsTests.cs`
- `Billing/ZocDoc.Billing.Tests/Invoicing/FakeProviderBillingApiCallerTests.cs`
- `Billing/ZocDoc.Billing.Tests/PaymentMethods/PaymentMethodServiceAddPaymentMethodV2Test.cs`
- `Billing/ZocDoc.Billing.Tests/ThirdPartyProcessors/StripeEventSqlPersistenceTest.cs`
- `SeleniumTests/SeleniumTests/Tests/CSR/Billing/ScenarioTests/ChargeBackScenarioTests.cs`

### Files added since the last mapping

27 new test files:

**`Apis/BillingMonolithApi`** — new `*ImplTests` fixtures on the billing monolith API (9):

- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/BillingAddressImplTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/InvoiceSummaryImplTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/PayNowImplTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/PaymentMethodImplAddPaymentMethodErrorTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/PaymentMethodImplBackfillTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/PaymentMethodImplMetricTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/PaymentMethodImplSandboxGuardTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/RecoveryImplTests.cs`
- `Apis/BillingMonolithApi/Zocdoc.BillingMonolithApi.Tests/StripeEventsImplTests.cs`

**`Billing/ZocDoc.Billing.Tests`** — new unit fixtures (recovery, invoicing breakdowns, bill periods) (15):

- `Billing/ZocDoc.Billing.Tests/AppCode/AppCodeBillingServiceTest.cs`
- `Billing/ZocDoc.Billing.Tests/BillProcessing/PayNowTriggerServiceTests.cs`
- `Billing/ZocDoc.Billing.Tests/Bills/BillPeriodTests.cs`
- `Billing/ZocDoc.Billing.Tests/Bills/ChargeWindowTests.cs`
- `Billing/ZocDoc.Billing.Tests/Bills/FindOrCreateFeePerBookingBillConcurrencyTest.cs`
- `Billing/ZocDoc.Billing.Tests/Invoicing/BookingBreakdownFactoryTests.cs`
- `Billing/ZocDoc.Billing.Tests/Invoicing/ProviderBillBookingSourceBreakdownReadSqlPersistenceTests.cs`
- `Billing/ZocDoc.Billing.Tests/Invoicing/ProviderBillBookingSourceBreakdownReaderTests.cs`
- `Billing/ZocDoc.Billing.Tests/Invoicing/ProviderBillBookingSourceBreakdownSqlPersistenceTests.cs`
- `Billing/ZocDoc.Billing.Tests/Onboarding/BillingOnboardingTaskServiceTests.cs`
- `Billing/ZocDoc.Billing.Tests/PaymentMethods/PaymentMethodServiceAddPaymentMethodTest.cs`
- `Billing/ZocDoc.Billing.Tests/PaymentMethods/StripePaymentMethodIdBackfillerTests.cs`
- `Billing/ZocDoc.Billing.Tests/Recovery/BillItemCardMappingServiceTests.cs`
- `Billing/ZocDoc.Billing.Tests/Recovery/RecoveryBalanceShaperTests.cs`
- `Billing/ZocDoc.Billing.Tests/Recovery/RecoveryStatusServiceTests.cs`

**`RestApis`** — practice billing settings controller + serialization (2):

- `RestApis/ZocDoc.RestApis.Tests/PracticeBillingSettings/PracticeBillingInfoResponseSerializationTests.cs`
- `RestApis/ZocDoc.RestApis.Tests/PracticeBillingSettings/PracticeBillingSettingsControllerTests.cs`

**`SeleniumTests`** — API-level billing fixtures (1):

- `SeleniumTests/SeleniumTests/Tests/API/Billing/PayNowApiTests.cs`

### Verification notes

- Line-shifts are real edits above the test declaration, not extraction drift — spot-checked on
  `ObsCreditToAccountingIntegrationTests`, where every test moved down exactly 1 line.
- The extractor was re-validated per-file against the independent `awk` method counter across all
  279 files. One reported diff (`BillingDetailsViewModelTests.cs`, awk 14 vs 15) is a baseline
  limitation — `awk` cannot match `[TestCase (` with a space before the paren — not a miss.
- The L4 classification of `SeleniumTests/.../Tests/API/Billing` was re-verified at this SHA: all
  4 fixtures derive from `BaseZocHttpApiTestFixture` and reference no WebDriver (`Driver`,
  `Browser`, `OpenPage`, `Navigate` all absent). The 5th file in that directory,
  `BillingHttpUtils.cs`, is a `static` helper with no tests and so contributes no rows.

## 2026-09-18 — initial mapping

First run — no prior mapping existed, so every file was new. `zocdoc_web` was pinned to
`fb4a8bd7b9` and is superseded by the entry above (same day). Counts in the table below are
current, i.e. post-re-map.

| Mapping | Repo | Branch | Commit | Type | Test files | Rows |
|---|---|---|---|---|---:|---:|
| [`provider-billing/api`](provider-billing/api-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | api | 5 | 97 |
| [`provider-billing/unit`](provider-billing/unit-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | cron | 21 | 228 |
| [`provider-billing/integration`](provider-billing/integration-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | integration | 13 | 88 |
| [`provider-billing/unit`](provider-billing/unit-test-mapping.md) | `Zocdoc/provider-billing` | `main` | `166621f1c8` | unit | 33 | 350 |
| [`provider-fe-monorepo/e2e`](provider-fe-monorepo/e2e-test-mapping.md) | `Zocdoc/provider-fe-monorepo` | `main` | `9b3c308d21` | playwright | 7 | 60 |
| [`provider-fe-monorepo/unit`](provider-fe-monorepo/unit-test-mapping.md) | `Zocdoc/provider-fe-monorepo` | `main` | `9b3c308d21` | unit | 82 | 1033 |
| [`zocdoc_web/api`](zocdoc_web/api-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `b306dc12f4` | api | 22 | 144 |
| [`zocdoc_web/unit`](zocdoc_web/unit-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `b306dc12f4` | cron | 9 | 30 |
| [`zocdoc_web/integration`](zocdoc_web/integration-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `b306dc12f4` | integration | 20 | 381 |
| [`zocdoc_web/e2e`](zocdoc_web/e2e-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `b306dc12f4` | selenium | 26 | 147 |
| [`zocdoc_web/unit`](zocdoc_web/unit-test-mapping.md) | `Zocdoc/zocdoc_web` | `master` | `b306dc12f4` | unit | 202 | 2381 |
| **Total** | | | | | **440** | **4939** |

### Scope note

QA-team-owned E2E suites are **out of scope** by request: the `sandbox` repo (Cypress/Playwright
against production) and `playwright-qa`. Only dev-owned suites are mapped, plus the `zocdoc_web`
Selenium billing tests, which the repo owner asked to include.

### Row counts vs declared tests

Rows expand parametrized cases: one row per `[TestCase]` / `[InlineData]` / `it.each` entry, all
sharing their parent method's declaration line. So rows > declared test blocks. Verified
declared-block counts: `provider-billing` 702 methods, `provider-fe-monorepo` billing 821
`it`/`test` blocks + 60 Playwright tests, `zocdoc_web` billing 2,566 methods at `b306dc12f4`.

