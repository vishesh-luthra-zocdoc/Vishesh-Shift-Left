# zocdoc_web — Billing Cron (Zocron) Test Mapping

<!-- test-mapping-meta
repo: Zocdoc/zocdoc_web
branch: master
commit: b306dc12f4a767a1462028a2dba66dcb8cae2134
generated: 2026-09-18
test-type: cron
-->
> Source: Zocdoc/zocdoc_web @ `b306dc12f4` · branch `master` · generated 2026-09-18


**Suite:** `Zocron/Zocron.Tasks.Tests/Billing` — scheduled billing task handlers.

> **Revision note:** mapped from `origin/master` at `b306dc12f4` (2026-09-18), the current tip. Links are pinned to this full SHA and will not drift.


**9 test files · 30 mapped rows**


---

## Zocron/Zocron.Tasks.Tests/Billing/AddBillProcessorSimulationResultToQueueTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 1 | `DoTaskTest (true)` | AddBillProcessorSimulationResultToQueueTests: Do Task Test — case: true | Assert Moq Verify | Do Task Test. 2 assertions. | L1 unit (cron handler). In scope: `AddBillProcessorSimulationResultToQueueTests`. | [L18](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/AddBillProcessorSimulationResultToQueueTests.cs#L18) |
| 2 | `DoTaskTest (false)` | AddBillProcessorSimulationResultToQueueTests: Do Task Test — case: false | Assert Moq Verify | Do Task Test. 2 assertions. | L1 unit (cron handler). In scope: `AddBillProcessorSimulationResultToQueueTests`. | [L18](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/AddBillProcessorSimulationResultToQueueTests.cs#L18) |

---

## Zocron/Zocron.Tasks.Tests/Billing/ApplyFutureTierChangesTaskTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 3 | `DoTask_ExpectedFlow` | ApplyFutureTierChangesTaskTests: Do Task — Expected Flow | Assert Moq Verify | Do Task — Expected Flow. 4 assertions. | L1 unit (cron handler). In scope: `ApplyFutureTierChangesTaskTests`. | [L50](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/ApplyFutureTierChangesTaskTests.cs#L50) |
| 4 | `DoTask_Exception` | ApplyFutureTierChangesTaskTests: Do Task — Exception | Assert Moq Verify | Do Task — Exception. 1 assertion. | L1 unit (cron handler). In scope: `ApplyFutureTierChangesTaskTests`. asserts the throw path. | [L73](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/ApplyFutureTierChangesTaskTests.cs#L73) |

---

## Zocron/Zocron.Tasks.Tests/Billing/BillGeneratorTaskActionTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 5 | `DoTaskTest` | BillGeneratorTaskActionTests: Do Task Test | Assert Moq Verify | Do Task Test. 2 assertions. | L1 unit (cron handler). In scope: `BillGeneratorTaskActionTests`. combinatorial [Values]. | [L18](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillGeneratorTaskActionTests.cs#L18) |

---

## Zocron/Zocron.Tasks.Tests/Billing/BillingErrorSenderTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 6 | `SendsOneEmailPerNonDevOwner` | BillingErrorSenderTests: Sends One Email Per Non Dev Owner | Assert Moq Verify | Sends One Email Per Non Dev Owner. 1 assertion. | L1 unit (cron handler). In scope: `BillingErrorSenderTests`. retry-on-fail. | [L50](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingErrorSenderTests.cs#L50) |
| 7 | `DoNotSendErrorsToBillingDevs` | BillingErrorSenderTests: Do Not Send Errors To Billing Devs | Execute test body | Do Not Send Errors To Billing Devs. | L1 unit (cron handler). In scope: `BillingErrorSenderTests`. retry-on-fail. | [L74](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingErrorSenderTests.cs#L74) |
| 8 | `DoesNotSendIgnorableErrors` | BillingErrorSenderTests: Does Not Send Ignorable Errors | Execute test body | Does Not Send Ignorable Errors. | L1 unit (cron handler). In scope: `BillingErrorSenderTests`. retry-on-fail. | [L92](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingErrorSenderTests.cs#L92) |
| 9 | `IfNoErrorsExist_NoEmailIsSent` | BillingErrorSenderTests: If No Errors Exist — No Email Is Sent | Execute test body | If No Errors Exist — No Email Is Sent. | L1 unit (cron handler). In scope: `BillingErrorSenderTests`. retry-on-fail. | [L111](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingErrorSenderTests.cs#L111) |

---

## Zocron/Zocron.Tasks.Tests/Billing/BillingJobWrapperTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 10 | `RunJob_AlertsForDevOwnedErrors` | BillingJobWrapperTests: Run Job — Alerts For Dev Owned Errors | Execute test body | Run Job — Alerts For Dev Owned Errors. | L1 unit (cron handler). In scope: `BillingJobWrapperTests`. | [L37](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingJobWrapperTests.cs#L37) |
| 11 | `RunJob_DoesNotAlertForNonDevOwnedErrors` | BillingJobWrapperTests: Run Job — Does Not Alert For Non Dev Owned Errors | Execute test body | Run Job — Does Not Alert For Non Dev Owned Errors. | L1 unit (cron handler). In scope: `BillingJobWrapperTests`. | [L49](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingJobWrapperTests.cs#L49) |
| 12 | `RunJob_CreatesAndAlertsFatalErrorWhenJobThrowsUncaughtException` | BillingJobWrapperTests: Run Job — Creates And Alerts Fatal Error When Job Throws Uncaught Exception | Assert FluentAssertions HaveCount | Run Job — Creates And Alerts Fatal Error When Job Throws Uncaught Exception. 2 assertions. | L1 unit (cron handler). In scope: `BillingJobWrapperTests`. asserts the throw path. | [L59](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingJobWrapperTests.cs#L59) |

---

## Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 13 | `GetLatestRunLogForTask_ValidTaskId` | BillingZocronSqlPersistenceTests: Get Latest Run Log For Task — Valid Task Id | Assert Assert.That | Get Latest Run Log For Task — Valid Task Id. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronSqlPersistenceTests`. retry-on-fail. | [L48](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs#L48) |
| 14 | `GetLatestRunLogForTask_InvalidTaskId` | BillingZocronSqlPersistenceTests: Get Latest Run Log For Task — Invalid Task Id | Execute test body | Get Latest Run Log For Task — Invalid Task Id. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronSqlPersistenceTests`. retry-on-fail. | [L65](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs#L65) |
| 15 | `CreateRunLogEntryForTask_ValidTaskId` | BillingZocronSqlPersistenceTests: Create Run Log Entry For Task — Valid Task Id | Assert Assert.That | Create Run Log Entry For Task — Valid Task Id. 4 assertions. | L1 unit (cron handler). In scope: `BillingZocronSqlPersistenceTests`. retry-on-fail. | [L72](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs#L72) |
| 16 | `CreateRunLogEntryForTask_invalidTaskId` | BillingZocronSqlPersistenceTests: Create Run Log Entry For Task — invalid Task Id | Assert Assert.Throws | Create Run Log Entry For Task — invalid Task Id. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronSqlPersistenceTests`. retry-on-fail; asserts the throw path. | [L110](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs#L110) |
| 17 | `ZocronTaskTypeEnum_MatchesZocronTaskTypeRef` | BillingZocronSqlPersistenceTests: Zocron Task Type Enum — Matches Zocron Task Type Ref | Assert Assert.AreEqual | Zocron Task Type Enum — Matches Zocron Task Type Ref. 2 assertions. | L1 unit (cron handler). In scope: `BillingZocronSqlPersistenceTests`. retry-on-fail. | [L121](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronSqlPersistenceTests.cs#L121) |

---

## Zocron/Zocron.Tasks.Tests/Billing/BillingZocronTaskHelperTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 18 | `ShouldTaskRun` | BillingZocronTaskHelperTests: Task Run | Assert Assert.AreEqual | Task Run. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronTaskHelperTests`. | [L51](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronTaskHelperTests.cs#L51) |
| 19 | `ShouldMonthlyTaskRun` | BillingZocronTaskHelperTests: Monthly Task Run | Assert Assert.AreEqual | Monthly Task Run. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronTaskHelperTests`. | [L78](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronTaskHelperTests.cs#L78) |
| 20 | `IsFirstOfMonth` | BillingZocronTaskHelperTests: Is First Of Month | Assert FluentAssertions Be | Is First Of Month. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronTaskHelperTests`. | [L116](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronTaskHelperTests.cs#L116) |
| 21 | `IsFirstOfMonth_And_ShouldMonthlyTaskRun` | BillingZocronTaskHelperTests: Is First Of Month — And — Should Monthly Task Run | Assert Assert.AreEqual | Is First Of Month — And — Should Monthly Task Run. 1 assertion. | L1 unit (cron handler). In scope: `BillingZocronTaskHelperTests`. | [L125](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/BillingZocronTaskHelperTests.cs#L125) |

---

## Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 22 | `DoTask_GetAllViolations_NoNewViolations (0)` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — No New Violations — case: 0 | Assert Moq Verify | Do Task — Get All Violations — No New Violations. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L40](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L40) |
| 23 | `DoTask_GetAllViolations_NoNewViolations (3)` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — No New Violations — case: 3 | Assert Moq Verify | Do Task — Get All Violations — No New Violations. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L40](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L40) |
| 24 | `DoTask_GetAllViolations_AllViolationsAreNew` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — All Violations Are New | Assert Moq Verify | Do Task — Get All Violations — All Violations Are New. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L64](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L64) |
| 25 | `DoTask_GetAllViolations_NewAndExistingViolations (3, 3)` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — New And Existing Violations — case: 3, 3 | Assert Moq Verify | Do Task — Get All Violations — New And Existing Violations. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L87](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L87) |
| 26 | `DoTask_GetAllViolations_NewAndExistingViolations (3, 0)` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — New And Existing Violations — case: 3, 0 | Assert Moq Verify | Do Task — Get All Violations — New And Existing Violations. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L87](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L87) |
| 27 | `DoTask_GetAllViolations_NewAndExistingViolations (0, 3)` | VerifyBillingDataIntegrityTests: Do Task — Get All Violations — New And Existing Violations — case: 0, 3 | Assert Moq Verify | Do Task — Get All Violations — New And Existing Violations. 2 assertions. | L1 unit (cron handler). In scope: `VerifyBillingDataIntegrityTests`. | [L87](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/VerifyBillingDataIntegrityTests.cs#L87) |

---

## Zocron/Zocron.Tasks.Tests/Billing/ZocMonAccountingDataTests.cs

| # | Test Name | What It Tests | Steps | Summary | Scope | Source Code |
|---|-----------|---------------|-------|---------|-------|-------------|
| 28 | `DoTask_JustWorks` | ZocMonAccountingDataTests: Do Task — Just Works | Execute test body | Do Task — Just Works. | L1 unit (cron handler). In scope: `ZocMonAccountingDataTests`. | [L57](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/ZocMonAccountingDataTests.cs#L57) |
| 29 | `DoTask_TooManyDeliberateOmissionsTotalCount_Throws` | ZocMonAccountingDataTests: Do Task — Too Many Deliberate Omissions Total Count — Throws | Assert Assert.Throws | Do Task — Too Many Deliberate Omissions Total Count — Throws. 1 assertion. | L1 unit (cron handler). In scope: `ZocMonAccountingDataTests`. asserts the throw path. | [L63](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/ZocMonAccountingDataTests.cs#L63) |
| 30 | `DoTask_TooManyDeliberateOmissionsAddedTodayCount_Throws` | ZocMonAccountingDataTests: Do Task — Too Many Deliberate Omissions Added Today Count — Throws | Assert Assert.Throws | Do Task — Too Many Deliberate Omissions Added Today Count — Throws. 1 assertion. | L1 unit (cron handler). In scope: `ZocMonAccountingDataTests`. asserts the throw path. | [L79](https://github.com/Zocdoc/zocdoc_web/blob/b306dc12f4a767a1462028a2dba66dcb8cae2134/Zocron/Zocron.Tasks.Tests/Billing/ZocMonAccountingDataTests.cs#L79) |
