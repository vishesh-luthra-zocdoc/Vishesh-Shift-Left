# provider-fe-monorepo — Billing API Endpoint Coverage

**Analyzed revision:** `provider-fe-monorepo` @ `origin/main` `dd9e4952a6` (2026-09-03)
**Snapshot:** `/tmp/slv3/snapshots/provider-fe-monorepo/` — no `package.json`, no `node_modules`. That matters here:
`@zocdoc/billing-monolith-api-client` is a **generated** client and its source is not in the snapshot, so the paths
for client-owned operations are not readable from the client itself. Where I give a path for one of those, the
evidence is the app's own mirror of it — the `UriTemplate` in `config/routes.ts` plus the Express mount in the dev
server (`app.ts` / `server.ts`), and in two cases the Playwright route glob. Anything I could not corroborate that
way is marked `UNVERIFIED`.

## How billing calls leave the browser — two mechanisms

| Mechanism | Where the URL lives | Who uses it |
|---|---|---|
| `TemplatedUrl` + `executeRequestIncludeCredentials` (fetchHelperV2) | `apps/settings/src/config/routes.ts` | 8 functions in `apps/settings/.../billingSettings/apiCalls.ts` |
| Generated `@zocdoc/billing-monolith-api-client` | Owned by the client package; mirrored as `UriTemplate`s so the dev server can stand in — see the comment at `routes.ts:671-672` ("The generated client owns these paths at runtime; the templates exist only so the dev server can mock the same reads") and `apps/provider-home-webapp/src/config/routes.ts:93-95,99-101,106-108` | 6 functions in `apiCalls.ts`, 4 modules in `shared/core/src/billing`, 1 in `apps/provider-home-webapp/src/apis/recoveryApi.ts` |

One endpoint uses neither: the invoice PDF URL is a **hardcoded string literal** at
`InvoiceDetailsContainer.tsx:171` (`/api/provider/v1/invoices?year=…&month=…`), while the
`GET_INVOICE_PDF_DOWNLOAD_URL` template at `routes.ts:681` is referenced only by the dev server
(`apps/settings/src/server/app.ts:145,1562`). Source and template can drift silently.

## Coverage legend

- **Unit** — a `describe` in a Jest unit test that asserts the request built and/or the response mapped, with the
  transport (`fetchHelperV2` or the generated client) `jest.mock`ed.
- **Component** — a component/hook test that reaches the call site but `jest.mock`s the client module, so it asserts *that*
  the function was called (and with what), never the wire format.
- **Integration** — a real-boundary test. **There are none.** See `integration-tests.md`: no MSW, no `nock`, no in-memory HTTP.
- **API contract** — an HTTP-contract test. **There are none (0 files).**

## Endpoints defined with `TemplatedUrl` (8)

| # | Method + URL pattern | Template defined at | Client function | Unit | Component | Integration |
|---|---|---|---|---|---|---|
| 1 | `GET /api/rest/provider/v1/settings/billing/{practiceId}` | `routes.ts:562` | `fetchPracticeBillingSettings` (`apiCalls.ts:116`, method `:128`) | Yes — `describe('fetchPracticeBillingSettings')` in `apiCalls-tests.ts:56` | Indirect — `usePracticeBillingSettings-tests.ts` (4 blocks) mocks `apiCalls` | None |
| 2 | `POST /api/rest/provider/v1/settings/billing/{practiceId}/{paymentMethodId}/setDefaultPaymentMethod` | `routes.ts:566` | `setDefaultPaymentMethod` (`:146`, `:164`) | Yes — `describe('setDefaultPaymentMethod')` `apiCalls-tests.ts:261` | Yes — `PaymentMethodV2-tests.tsx` `describe('API calls')` (:604), `apiCalls` mocked | None |
| 3 | `DELETE /api/rest/provider/v1/settings/billing/{practiceId}/{paymentMethodId}` | `routes.ts:570` | `deletePaymentMethod` (`:174`, `:192`) | Yes — `describe('deletePaymentMethod')` `apiCalls-tests.ts:285` | Yes — `PaymentMethodV2-tests.tsx` `describe('API calls')`; `DeletePaymentMethodConfirmationModalV2-tests.tsx` covers only the confirmation UI | None |
| 4 | `PUT /api/rest/provider/v1/settings/billing/{practiceId}/billingEmail` | `routes.ts:581` | `updatePracticeBillingEmail` (`:202`, `:218`) | Yes — `describe('updatePracticeBillingEmail')` `apiCalls-tests.ts:309` | **Weak** — `EditBillingEmailModal-tests.tsx` has 2 blocks, both under `describe('billing email validation')`; no save assertion | None |
| 5 | `PUT /api/rest/provider/v1/settings/billing/{practiceId}/primaryBusinessAddress` | `routes.ts:585` | `updatePrimaryBusinessAddress` (`:229`, `:245`) | Yes — `describe('updatePrimaryBusinessAddress')` `apiCalls-tests.ts:339` | **Weak** — `EditBusinessAddressModal-tests.tsx` (9 blocks) is entirely field validation; no save assertion | None |
| 6 | `POST /api/rest/provider/v1/settings/billing/{practiceId}/{providerId}/{paymentMethodId}/setPaymentMethod` | `routes.ts:591` | `setDefaultPaymentMethodForProvider` (`:260`, `:279`) | Yes — `describe('setDefaultPaymentMethodForProvider')` `apiCalls-tests.ts:384` | Yes — `PaymentMethodsPerProviderModal-tests.tsx` (21 blocks), `apiCalls` mocked | None |
| 7 | `POST /api/rest/provider/v1/settings/billing/{practiceId}/savePaymentMethodAttributes` | `routes.ts:610` | `savePaymentMethodAttributes` (`:289`, `:313`) | Yes — `describe('savePaymentMethodAttributes')` `apiCalls-tests.ts:488` | Yes — `EditBillingContactInfoModal-tests.tsx` (12 blocks) incl. `describe('save toast')`, `apiCalls` mocked | None |
| 8 | `POST /spo-provider/v1/management/{practiceId}/pay-now` | `routes.ts:577` — carries `// TODO(BILL-826): placeholder route for the M2 batch-charge ("pay now") endpoint … The real route + BatchProcessorResult response shape are mentor pre-work and not yet finalized` | `triggerPayNow` (`:426`, `:446`) | **Thin** — `triggerPayNow-tests.ts`, 2 declared blocks | Indirect — `PayNowModal-tests.tsx` mocks `apiCalls` (:160) and `resolvePaymentOutcome-tests.ts` mocks it too | None |

## Endpoints owned by the generated client (10)

| # | Method + URL pattern | Path evidence | Client function | Unit | Component | Integration |
|---|---|---|---|---|---|---|
| 9 | `GET /billing-monolith-api/v1/bill/{bill_id}/summary` | `routes.ts:667`; dev mount `app.ts:1547`; Playwright glob `e2e/…/billing-settings-page-commands.ts:172` | `fetchInvoiceDetails` → `apiClient.getBillSummary` (`apiCalls.ts:39,43`) | Yes — `describe('fetchInvoiceDetails')` `apiCalls-tests.ts:192` | Indirect — `InvoiceDetailsContainer-tests.tsx` (17 blocks) mocks `../apiCalls` **and** `v2/FpbInvoiceView` | None |
| 10 | `GET /billing-monolith-api/v1/practice/{practiceId}/recovery` | `routes.ts:673`; `provider-home-webapp/src/config/routes.ts:95`; dev mounts `app.ts:1552`, `server.ts:545-546`; Playwright glob `:184` | `fetchRecovery` (`apiCalls.ts:65,69`) **and** `apps/provider-home-webapp/src/apis/recoveryApi.ts:22` — two independent callers | Yes, twice — `describe('fetchRecovery')` `apiCalls-tests.ts:82` and `recoveryApi-tests.ts:24` (3 blocks) | Indirect — `useRecoverySummary-tests.ts` (9), `useRecoveryStatusSummary.test.ts` (7) | None |
| 11 | `GET /billing-monolith-api/v1/practice/{practiceId}/recovery/balance-detail` | `routes.ts:677`; dev mount `app.ts:1557`; Playwright glob `:186` | `fetchRecoveryBalanceDetail` (`apiCalls.ts:92,96`) | Yes — `describe('fetchRecoveryBalanceDetail')` `apiCalls-tests.ts:142` | **Thin** — `useRecoveryBalanceDetail-tests.ts`, 3 blocks | None |
| 12 | `POST /billing-monolith-api/v1/practice/{practiceId}/setup-intents` | dev mount `app.ts:1481`; Playwright glob `:177` | `createSetupIntentV2` → `apiClient.createSetupIntent` (`apiCalls.ts:323,325`) | **NONE — no `describe` for it in `apiCalls-tests.ts`** | None that reaches it — `CreditCardFormContentV2-tests.tsx` (2 blocks, ZIP only) and `AchFormContentV2-handleConnectBank-tests.tsx` both mock `apiCalls` | None |
| 13 | `POST /billing-monolith-api/v1/practice/{practiceId}/setup-intents/{setupIntentId}/prepare` | dev mount `app.ts:1496` | `prepareSetupIntentV2` → `apiClient.prepareSetupIntent` (`apiCalls.ts:402,407`) | **NONE — no `describe`** | None — only `AchFormContentV2` calls it (`:27,93,183`), and its test mocks `apiCalls` | None |
| 14 | `POST /billing-monolith-api/v1/practice/{practiceId}/payment-methods` | dev mount `app.ts:1491`; Playwright glob `:181` | `addPaymentMethodV3` → `apiClient.addPaymentMethod` (`apiCalls.ts:359,365`) | Yes — `describe('addPaymentMethodV3')` `apiCalls-tests.ts:416` | Indirect — `PayNowModal.tsx:23,199,260` calls it; `PayNowModal-tests.tsx` mocks `apiCalls` | None |
| 15 | `POST /billing-monolith-api/v1/practice/{practiceId}/setup-intents~withCustomer` | `provider-home-webapp/src/config/routes.ts:109`; dev mounts `app.ts:1486`, `server.ts:623-624`; Playwright glob `:179` | `shared/core/src/billing/createSetupIntentWithCustomer.ts:10` | Yes — `createSetupIntentWithCustomer-tests.ts` (4 blocks): 200 mapping, 400 → `errorMessage`, other non-200 → throw | Indirect — `useConfirmPaymentSetup-tests.tsx` (11) mocks the module; `AddPaymentMethodElementModal-tests.tsx` mocks it too | None |
| 16 | `POST /billing-monolith-api/v1/practice/{practiceId}/payment-methods` (core caller) | `provider-home-webapp/src/config/routes.ts:113`; dev mounts `app.ts:1491`, `server.ts:645-646` | `shared/core/src/billing/addPaymentMethod.ts:15` | Yes — `addPaymentMethod-tests.ts` (7 blocks) incl. `SAVE_FAILED_MESSAGE` | Indirect — `AddPaymentMethodElementModal-tests.tsx` mocks it | None. **Two client functions target the same path** (#14 legacy, #16 unified); neither test knows about the other |
| 17 | `GET /billing-monolith-api/v1/practice/{practiceId}/billing-address` | `provider-home-webapp/src/config/routes.ts:103`; dev mount `server.ts:568-569` | `shared/core/src/billing/getBillingAddress.ts:17` | **NONE — no test file for the module** | Only as a mock — `useBillingAddressPrefill-tests.ts` mocks `../getBillingAddress`; `AddPaymentMethodElementModal-tests.tsx` mocks it | None |
| 18 | `PUT /billing-monolith-api/v1/practice/{practiceId}/billing-address` | `provider-home-webapp/src/config/routes.ts:103`; dev mount `server.ts:594-595` | `shared/core/src/billing/updateBillingAddress.ts:21` | **NONE** | **NONE** — mocked in `AddPaymentMethodElementModal-tests.tsx`, reached by no test | None |
| 19 | `PUT` practice SKU mapping — UNVERIFIED path | Owned by a different generated client (`providerSetupClient.updatePracticeSkuMapping`, `apps/provider-home-webapp/src/pages/homepage/controller.ts:311`). `controller.ts` is outside the billing scope list, so I did not resolve its route | `skuService.updateSkus` → `updatePracticeSkuMapping` | Yes, at the service layer — `skuService-test.ts` (16 blocks) mocks `pages/homepage/controller` | Indirect | None |

## Endpoint reached without a template or a client (1)

| # | Method + URL | Where built | Coverage |
|---|---|---|---|
| 20 | `GET /api/provider/v1/invoices?year={y}&month={m}` | **Hardcoded literal** at `InvoiceDetailsContainer.tsx:171`. The `GET_INVOICE_PDF_DOWNLOAD_URL` template (`routes.ts:681`) is used only by the dev server (`app.ts:145,1562`) | component-level only — `InvoiceDetailsContainer-tests.tsx` `describe('PDF URL Generation')` (:483) asserts the exact strings at `:573`, `:614`, `:655` (`…?year=2025&month=9`, `month=1`, `month=12`). No unit test, no integration test |

## Endpoints with no coverage at any level

| Endpoint | Client function | Risk |
|---|---|---|
| `POST /billing-monolith-api/v1/practice/{practiceId}/setup-intents` | `createSetupIntentV2` (`apiCalls.ts:323`) | Creates the Stripe SetupIntent for legacy card/ACH entry — the first step of the **Pay Now declined-card recovery flow**. No `describe`, and every call site mocks it |
| `POST /billing-monolith-api/v1/practice/{practiceId}/setup-intents/{setupIntentId}/prepare` | `prepareSetupIntentV2` (`apiCalls.ts:402`) | ACH / Financial Connections preparation step. No `describe`, single call site, mocked there |
| `GET /billing-monolith-api/v1/practice/{practiceId}/billing-address` | `shared/core/.../getBillingAddress.ts` | Prefills the billing address in the unified Payment Element modal. No test file; the module's own JSDoc notes the values are returned unvalidated, and `billingAddressSchema-tests.ts` covers only the write-side schema |
| `PUT /billing-monolith-api/v1/practice/{practiceId}/billing-address` | `shared/core/.../updateBillingAddress.ts` | **Writes** the practice's billing address. Zero tests at any level — the only file that names it does so to `jest.mock` it |
| Every endpoint above at **Integration/API contract** | all 20 | No test in the repo asserts a billing request/response against a real HTTP layer |

## Candidate Gaps

| # | What's missing | Level | Path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| API-1 | `updateBillingAddress.ts` has **zero tests at any level** and `getBillingAddress.ts` has none either | Unit | `shared/core/src/billing/updateBillingAddress.ts`, `getBillingAddress.ts` | A write of the practice's billing address with no test; the read feeds Stripe's address collection. Both are new code from the Payment Element extraction | S | **P0** |
| API-2 | No `describe` for `createSetupIntentV2` or `prepareSetupIntentV2` — 2 of 14 `apiCalls.ts` functions, both on the Pay Now recovery path | Unit | `apps/settings/.../__tests__/apiCalls-tests.ts`; `apiCalls.ts:323,402` | The other 11 request-builders all have one; these two gate a practice's ability to replace a declined card | S | **P0** |
| API-3 | No integration test/API contract tier at all: 20 endpoints verified only against self-authored mocks | Integration | whole scope; `apps/settings/src/config/routes.ts:562-683`, `apiCalls.ts`, `shared/core/src/billing/billingApiClient.ts` | Route-template typos, method changes, and response-shape drift are invisible below the browser level. MSW once + one suite per client module would cover all 20 | M setup, S each | **P0** |
| API-4 | `POST /spo-provider/v1/management/{practiceId}/pay-now` is still a **placeholder route** per `routes.ts:577` (`TODO(BILL-826)`), tested by 2 declared blocks | Unit/Integration | `routes.ts:577`, `apiCalls.ts:426`, `__tests__/triggerPayNow-tests.ts` | This is the batch-charge call. If the route and `BatchProcessorResult` shape are not final, the code and its 2 tests are both provisional and will silently mismatch the real endpoint | S | **P1** |
| API-5 | Two client functions POST to the same `…/payment-methods` path (`addPaymentMethodV3` in `apiCalls.ts:359`, core `addPaymentMethod.ts:15`) with separate tests and no shared contract | Unit | those two files | Divergent request bodies / error handling for one endpoint; a backend change must be found twice | S | **P1** |
| API-6 | The invoice PDF URL is hardcoded at the call site while a template for it exists | Unit | `InvoiceDetailsContainer.tsx:171`, `routes.ts:681` | The component test asserts the literal, so source and template can drift with a green suite. Use the template and assert via it | XS | P2 |
| API-7 | Save paths for billing email and business address have unit-level request tests but no component-test assertion that the modal actually calls them | Component | `__tests__/EditBillingEmailModal-tests.tsx` (2 blocks), `__tests__/EditBusinessAddressModal-tests.tsx` (9 blocks, all validation) | Both modals could stop saving and their suites would stay green | S | P2 |
| API-8 | `fetchRecovery` is implemented twice (`apiCalls.ts:65`, `provider-home-webapp/src/apis/recoveryApi.ts:22`) against one endpoint, each with its own unit test and different error policies | Unit | those two files | Duplicate transport for the same read; `recoveryApi.ts`'s JSDoc documents a never-404 contract that the settings copy does not encode | S | P2 |

## Level Summary

| Level | Billing test files | Declared blocks | Endpoints with coverage at this level |
|---|---|---|---|
| unit | 34 | 224 | 15 of 20 (endpoints 1-11, 14-16, 19) |
| component | 45 | 515 | 12 of 20, all with the client module mocked (endpoints 1-3, 6, 7, 9-11, 14-16, 20) |
| Hook hook render | 9 | 47 | 5 of 20 (1, 10, 11, 17-as-mock, 19) |
| **integration** | 2 | 70 | **0 of 20** |
| **API contract** | **0** | **0** | **0 of 20** |
| Total non-E2E billing | **90** | **856** | — |

**Endpoint totals:** 20 billing endpoints reached from this repo — 8 via `TemplatedUrl`, 10 via the generated
billing-monolith client (1 of those with an UNVERIFIED path, #19), 1 hardcoded, 1 (`…/payment-methods`) reached by two
different client functions and counted once per caller (#14, #16). **4 endpoints have no coverage at any level;
20 of 20 have no coverage above the component level.**
