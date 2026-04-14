# Selenium Integration Tests — Billing Domain (zocdoc_web Monolith)

These tests live in `zocdoc_web` (the monolith), NOT in provider-fe-monorepo. They test backend billing logic: bill generation, payment processing via Stripe, chargebacks, churn workflows, credits, refunds, and RBAC.

**Source:** [Billing - Shift Left Test Mapping spreadsheet](https://docs.google.com/spreadsheets/d/1IVIf_Q0F-j8t8B1ECI1qDp3HBGLag1EN6JzNISWuK5I/edit?gid=0#gid=0)
**Triage by:** Vishesh + Vaisly

---

## Summary

| Metric | Count |
|--------|-------|
| Total test files | 14 |
| Total tests | 76 |
| Keep ("Yes") | 38 |
| Remove ("No") | 38 |
| Helpers (support methods) | 8 |

---

## Triage Results at a Glance

| Test File | Total | Keep | Remove | What It Tests |
|-----------|-------|------|--------|---------------|
| PracticeBillingSettingsImplTests.cs | 3 | 3 | 0 | API auth (401/200 by role) |
| PracticeBillingSettingsControllerTest.cs | 7 | 7 | 0 | RBAC, FGA flags, CSR access |
| BillCreationScenarioTests.cs | 13 | 2 | 11 | Bill generation scenarios |
| BillGeneratorScenarioTests.cs | 8 | 3 | 5 | Test helpers for bill generation |
| ChargeBackScenarioTests.cs | 2 | 2 | 0 | Chargeback processing |
| ChurnScenarioTests.cs | 16 | 1 | 15 | Churn billing workflows |
| ContractTermChangeScenarioTests.cs | 6 | 0 | 6 | Contract term change billing |
| CreditScenarioTests.cs | 9 | 9 | 0 | Credit application scenarios |
| DocSwapScenarioTests.cs | 1 | 0 | 1 | Doctor swap credits |
| DoctorsNotToProcessScenarioTests.cs | 5 | 3 | 2 | Save-a-Doc, locked docs, zero bills |
| PayTheBillScenarioTests.cs | 8 | 8 | 0 | ACH/CC payments, multi-PM |
| PriceOverrideScenarioTests.cs | 2 | 0 | 2 | Price override billing |
| ProcessorCardScenarioTests.cs | 9 | 9 | 0 | Card validation (declined, fraud, brands) |
| ProcessorRefundScenarioTests.cs | 3 | 2 | 1 | Full/partial refunds |
| TrialScenarioTests.cs | 2 | 0 | 2 | Free trial / concession billing |

---

## Detailed Breakdown by File

### PracticeBillingSettingsImplTests.cs — KEEP ALL (3/3)

These verify API auth for the billing settings endpoint. Simple, fast, important.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | GetTask_ReturnsUnauthorized | No auth header → 401 |
| 2 | Yes | GetTask_ReturnsOK_WithCsrDeveloperRole | CsrDeveloper role → 200 + correct task data |
| 3 | Yes | GetTask_ReturnsOK_WithOnboardingRole | OnboardingTaskFrameworkReadWrite role → 200 |

---

### PracticeBillingSettingsControllerTest.cs — KEEP ALL (7/7)

These test RBAC and FGA authorization for all billing endpoints. Critical for security.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | CallEndpoints_GivenUserRole_ReturnsForbiddenIfRoleNowAllowed | RBAC enforcement — forbidden roles get 403 |
| 2 | Yes | CallEndpoints_GivenCsrUser_ReturnsOK | CSR can access all billing endpoints |
| 3 | Yes | PracticeAuth_ReturnsCorrectResponse_GivenFgaFlagsAreSet | FGA authorization flags work |
| 4 | Yes | PracticeAuth_WithAuditOnlyFlag_UsesRbacResult | Audit-only flag uses RBAC |
| 5 | Yes | PracticeAuth_FgaResultNotUsed_WhenAuthorizationAuditPercentageSetToZero | FGA ignored when audit % = 0 |
| 6 | Yes | PracticeAuth_CsrUserSucceeds_EvenWhenFgaFlagsAreSetAndFgaFails | CSR bypasses FGA |
| 7 | Yes | SetBillingEmail_SucceedsWithUpdateTaskStatus_Flag_On | Email update + task status flag |

---

### BillCreationScenarioTests.cs — KEEP 2 / REMOVE 11

Most bill creation scenarios are for legacy billing flows that are no longer active. Only the Net Payments tests are still relevant.

| # | Keep? | Test Name | Why Keep/Remove |
|---|-------|-----------|-----------------|
| 1 | No | GeneratesMonthlyBill | Legacy monthly billing — no longer active |
| 2 | No | GeneratesAnnualBill | Legacy annual billing |
| 3 | No | GeneratesBillForAdditionalProfessional | Legacy billing seeding |
| 4 | No | GeneratesMonthlyProrataBill | Legacy prorated billing |
| 5 | No | ForAnnualPracticeDoesntGenerateBillInNonRenewalMonth | Legacy annual renewal |
| 6 | No | ForMultiAnnualPracticeDoesntGenerateBillInNonRenewalYear | Legacy multi-year |
| 7 | No | DoesNotGenerateMonthlyBillForNonActivatedProfessional | Legacy activation flow |
| 8 | No | NoneActive_DoesNotGenerateMonthlyBill | Legacy activation |
| 9 | No | SomeInactive_GeneratesMonthlyBillWithCorrectBillItems | Legacy activation |
| 10 | No | ExistingBillNewInactive_DoesNotCreateNewBillItem | Legacy activation |
| 11 | No | WhenProfessionalIsLocked_GeneratesMonthlyBill | Legacy locked billing |
| 12 | **Yes** | **NetPaymentsNotEnabled** | **Active — verifies immediate processing when net payments off** |
| 13 | **Yes** | **NetPaymentsEnabled** | **Active — verifies delayed charge date (DoNotProcessUntilDate)** |

---

### BillGeneratorScenarioTests.cs — KEEP 3 / REMOVE 5

Helpers for bill creation tests. Keep the ones used by active tests.

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | Yes | SetupTest | Used by all active tests |
| 2 | Yes | DoGeneratorScenarioTestSetup | Used by all active tests |
| 3 | No | ChangeContract | Only used by removed contract tests |
| 4 | Yes | MarkBillAsPaid | Used by credit and payment tests |
| 5 | Yes | AssertCorrectChargesHappenedInStripe | Used by payment tests |
| 6 | No | LockProfessional | Only used by removed lock tests |
| 7 | No | GetBillSubscriptionDates | Only used by removed prorata tests |
| 8 | No | GetProrataPriceForSubscription | Only used by removed prorata tests |

---

### ChargeBackScenarioTests.cs — KEEP ALL (2/2)

Chargebacks are still active. Both tests needed.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | ProcessBillWithChargeback_SingleProvider | Single-provider chargeback processing |
| 2 | Yes | ProcessBillWithChargeback_MultiProfProvider | Multi-professional chargeback processing |

---

### ChurnScenarioTests.cs — KEEP 1 / REMOVE 15

Almost all churn scenarios are for legacy billing. Only the FPBAD/Bisquick reset test is still relevant.

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1-15 | No | ChurnScenario_* (15 tests) | Legacy churn billing — no longer active |
| 16 | **Yes** | **LocalPracticeBackFromChurn_ForcedOntoBisquick** | **Active — FPBAD reset + tier adjustment** |

---

### ContractTermChangeScenarioTests.cs — REMOVE ALL (0/6)

All contract term change tests are for legacy billing flows.

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1-6 | No | ContractTermChangeScenarioTests_* | Legacy contract change billing |

---

### CreditScenarioTests.cs — KEEP ALL (9/9)

Credit application is still active. All scenarios needed.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | CreditLessThanBillTotalForSinglePractice | Partial credit |
| 2 | Yes | CreditEqualToBillTotal | Full credit ($0 bill) |
| 3 | Yes | SpoCreditWithNoSpoDebits | SPO credit without debits |
| 4 | Yes | SpoDebitWithSubscriptionCredit | SPO debit + subscription credit |
| 5 | Yes | SpoCreditWithSpoDebits | SPO credit + debits |
| 6 | Yes | CreditLessThanBillTotalForMuliplePractice | Multi-practice credit |
| 7 | Yes | CreditEqualToBillTotal_AgreementChange | Credit + contract change |
| 8 | Yes | CreditsOnDifferentPaymentMethodsOnUnprocessedBill | Multi-PM credits |
| 9 | Yes | CreditsNotPromotedToNextBill | Credits don't carry over |

---

### DocSwapScenarioTests.cs — REMOVE (0/1)

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | No | DocSwapCredit_IsAutomaticallyApplied_MultipleTimes | Legacy doc swap flow |

---

### DoctorsNotToProcessScenarioTests.cs — KEEP 3 / REMOVE 2

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | **Yes** | **DocInSaveADocIsNotChargedBase** | **Active — Save-a-Doc billing skip** |
| 2 | No | DocInSaveADocIsNotChargedAfterChurn | Legacy churn |
| 3 | No | DocLockedIsCharged | Legacy locked billing |
| 4 | **Yes** | **DocInSaveADocIsNotChargedOtherDocsAreCharged** | **Active — partial billing** |
| 5 | **Yes** | **ZeroDollarBillIsNotCharged** | **Active — $0 bill handling** |

---

### PayTheBillScenarioTests.cs — KEEP ALL (8/8)

Payment processing is core functionality. All tests needed.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | PaysViaAch | Single-provider ACH |
| 2 | Yes | PaysViaAchMultiDoc | Multi-professional ACH |
| 3 | Yes | PaysViaCreditCard | Single-provider CC |
| 4 | Yes | PaysViaCreditCardForMultipleProfessionals | Multi-professional CC |
| 5 | Yes | WithNonAgreementItemWhileInChurnQueue_SPOItemStillCharged | SPO billing during churn |
| 6 | Yes | WithNonAgreementItemWhenChurned_ItDoesCharge | SPO billing after churn |
| 7 | Yes | WithMultiProWhenOneChurned_ChargesForAllButChurned | Partial billing |
| 8 | Yes | PaysViaCreditCardDifferentPaymentMethods | Multi-PM (AmEx + Visa) |

---

### PriceOverrideScenarioTests.cs — REMOVE ALL (0/2)

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | No | SingleProfessional_CreatesCorrectBill | Legacy price override |
| 2 | No | MultipleProfessional_CreatesCorrectBill | Legacy price override |

---

### ProcessorCardScenarioTests.cs — KEEP ALL (9/9)

Card validation is critical. Tests all card brands + edge cases.

| # | Keep? | Test Name | What It Tests |
|---|-------|-----------|---------------|
| 1 | Yes | DeclinedCard | Declined card handling |
| 2 | Yes | FraudulentCard | Fraud detection |
| 3 | Yes | GoodVisaCard | Visa processing |
| 4 | Yes | GoodAmexCard | AmEx processing |
| 5 | Yes | GoodMasterCard | MasterCard processing |
| 6 | Yes | GoodDiscoverCard | Discover processing |
| 7 | Yes | OneGoodAndOneBadCard | Mixed card scenario |
| 8 | Yes | MoreCardsThanProfessionals | Extra cards handling |
| 9 | Yes | CreateProfessionalAndAttemptToCharge | Helper for above |

---

### ProcessorRefundScenarioTests.cs — KEEP 2 / REMOVE 1

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | Yes | IssueFullRefund | Active — full refund flow |
| 2 | Yes | IssuePartialRefund | Active — partial refund flow |
| 3 | No | WhenIssuingRefundOnSubscriptionBillItemTransaction | Legacy subscription refund |

---

### TrialScenarioTests.cs — REMOVE ALL (0/2)

| # | Keep? | Test Name | Why |
|---|-------|-----------|-----|
| 1 | No | ProfessionalOnFreeTrial_CreatesZeroDollarBill | Legacy trial billing |
| 2 | No | ProfessionalOnConcessionPrice_CreatesCorrectBill | Legacy concession pricing |

---

## Action Items

### Tests to Remove (38 tests)

These are legacy billing flows no longer active. Removing them will:
- Speed up the Selenium test suite
- Reduce maintenance burden
- Remove false confidence from tests that exercise dead code paths

**Biggest wins:**
- ChurnScenarioTests.cs — 15 tests removed (only 1 kept)
- BillCreationScenarioTests.cs — 11 tests removed (only 2 kept)
- ContractTermChangeScenarioTests.cs — 6 tests removed (all)

### Tests to Keep (38 tests)

These test active billing flows:
- **RBAC/Auth** (10 tests) — API access control
- **Payment processing** (8 tests) — ACH/CC payments via Stripe
- **Card validation** (9 tests) — All card brands + edge cases
- **Credits** (9 tests) — Credit application scenarios
- **Chargebacks** (2 tests) — Dispute handling
- **Refunds** (2 tests) — Full/partial refunds
- **Net payments** (2 tests) — Delayed processing
- **Save-a-Doc** (3 tests) — Queue billing behavior
- **Churn (FPBAD)** (1 test) — Bisquick reset

### Shift-Left Candidates

Some "Keep" tests could potentially be shifted from Selenium to faster integration tests:
- RBAC tests (PracticeBillingSettingsControllerTest) → could be unit/integration tests
- Card validation tests → could test Stripe token handling without full browser automation
