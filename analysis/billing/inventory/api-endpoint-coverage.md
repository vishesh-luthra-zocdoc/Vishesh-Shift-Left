# API Endpoint Coverage Map

Every REST endpoint used by billing, and whether it's tested.

---

## REST Endpoints

| # | Endpoint | Method | Unit Test | Cypress Intercept | Verdict |
|---|----------|--------|-----------|-------------------|---------|
| 1 | `/api/rest/provider/v1/settings/billing/{practiceId}` | GET | fetchPracticeBillingSettings (2 tests) | @getPracticeBillingSettings | Fully covered |
| 2 | `.../{practiceId}/{paymentMethodId}/setDefaultPaymentMethod` | POST | setDefaultPaymentMethod (2 tests) | @postSetDefaultPaymentMethod | Fully covered |
| 3 | `.../{practiceId}/{paymentMethodId}` | DELETE | deletePaymentMethod (2 tests) | @deletePaymentMethod | Fully covered |
| 4 | `.../{practiceId}/billingEmail` | PUT | updatePracticeBillingEmail (2 tests) | @putUpdateBillingEmail | Fully covered |
| 5 | `.../{practiceId}/primaryBusinessAddress` | PUT | updatePrimaryBusinessAddress (3 tests) | @putUpdatePrimaryBusinessAddress | Fully covered |
| 6 | `.../{practiceId}/{providerId}/{paymentMethodId}/setPaymentMethod` | POST | setDefaultPaymentMethodForProvider (2 tests) | @postSetDefaultPaymentMethodForProvider | Fully covered |
| 7 | `.../{practiceId}/addCreditCard` | POST | addCreditCard (3 tests) | @postAddCreditCard | Fully covered |
| 8 | `.../{practiceId}/addAch` | POST | addAch (3 tests) | @postAddAch | Fully covered |
| 9 | `.../{practiceId}/savePaymentMethodAttributes` | POST | savePaymentMethodAttributes (2 tests) | @postSavePaymentMethodAttributes | Fully covered |
| 10 | `/billing-monolith-api/v1/bill/{bill_id}/summary` | GET | fetchInvoiceDetails (4 tests) | @getBillSummary | Fully covered |
| 11 | `/api/provider/v1/invoices` (PDF download) | GET | -- | -- | **GAP: No tests** |

**Score: 10/11 endpoints fully covered (91%)**

---

## API Client Functions

All defined in `apps/settings/src/pages/settingsPages/billingSettings/apiCalls.ts`:

| # | Function | Unit Tests | Error Handling Tested? |
|---|----------|------------|----------------------|
| 1 | `fetchPracticeBillingSettings` | 2 | Yes (API error) |
| 2 | `fetchInvoiceDetails` | 4 | Yes (non-200, exception, snake_case) |
| 3 | `setDefaultPaymentMethod` | 2 | Yes |
| 4 | `deletePaymentMethod` | 2 | Yes |
| 5 | `updatePracticeBillingEmail` | 2 | Yes |
| 6 | `updatePrimaryBusinessAddress` | 3 | Yes (including 400 error message) |
| 7 | `setDefaultPaymentMethodForProvider` | 2 | Yes |
| 8 | `addCreditCard` | 3 | Yes (API error + error in response) |
| 9 | `addAch` | 3 | Yes (API error + error in response) |
| 10 | `savePaymentMethodAttributes` | 2 | Yes |

**Score: 10/10 functions tested (100%)**

---

## GraphQL

| Query | Used By | Tested? | Notes |
|-------|---------|---------|-------|
| `getCostPlans` | PricingInformation, BillingSettingsContainer | Mocked in PricingTab-tests + BillingSettingsContainer-tests | Not tested for actual data shape |
| `getSkuMappings` | PricingInformation | -- | **GAP: No tests** |

---

## Key Types (for reference)

The main data types flowing through these endpoints:

```
PracticeBillingSettingsViewModelType
├── practiceId: string
├── practiceName: string
├── practiceBillingEmail: string
├── canEdit: boolean
├── paymentMethods: PaymentMethodInfo[]
│   ├── id, description, cardType, isDefault
│   ├── monthlyDollarLimit: number | null
│   └── rolloverOrder: number | null
├── providersWithPaymentMethods: ProviderWithPaymentMethodInfo[]
├── businessAddress: BusinessAddressInfo
└── bills: BillInfo[]
    ├── invoiceName, invoiceUrl
    └── status: 'Paid' | 'PartiallyPaid' | 'Unpaid'
```
