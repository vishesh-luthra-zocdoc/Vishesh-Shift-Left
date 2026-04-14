# Detailed Test Catalog — Every Billing Test

A line-by-line catalog of every unit test and Cypress test case in the billing domain.

---

## Unit Tests

### 1. billingDateUtils-tests.ts
**Path:** `apps/settings/src/pages/settingsPages/billingSettings/utils/__tests__/billingDateUtils-tests.ts`
**Tests:** 12 | **Type:** Business logic (date utilities)

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | Formats date "Dec 2019" correctly | Abbreviation expansion |
| 2 | Formats date "December 2019" correctly | Full month passthrough |
| 3 | Formats date "Oct 1, 2025 - Oct 31, 2025" correctly | Date range → month/year |
| 4 | Formats date "April 1, 2022 - April 30, 2022" correctly | Date range with full month |
| 5 | returns fallback when billDate missing | Undefined input |
| 6 | returns fallback when billDate invalid | Invalid date string |
| 7 | formats month/year in UTC to avoid TZ shift | UTC parsing |
| 8 | returns false for "Dec 2025" | Past invoice detection |
| 9 | returns true for "Jan 2026" | Future invoice detection |
| 10 | returns true for "Feb 2026" | Future invoice detection |
| 11 | returns true for "Jan 1, 2026 - Jan 31, 2026" | Date range future detection |
| 12 | returns false for "not-a-date" | Invalid date handling |

---

### 2. AddAchModal-tests.tsx
**Path:** `apps/settings/src/pages/settingsPages/billingSettings/__tests__/AddAchModal-tests.tsx`
**Tests:** 8 | **Type:** Form validation

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | account holder name - does not allow empty value | Required field |
| 2 | bank name - does not allow empty value | Required field |
| 3 | routing number - does not allow empty value | Required field |
| 4 | routing number - does not allow non-digit values | Digits only |
| 5 | routing number - does not allow less than 9 digits | Min length |
| 6 | routing number - does not allow more than 9 digits | Max length |
| 7 | account number - does not allow empty value | Required field |
| 8 | account number - does not allow non-digit values | Digits only |

---

### 3. AddCreditCardModal-tests.tsx
**Path:** `apps/settings/src/pages/settingsPages/billingSettings/__tests__/AddCreditCardModal-tests.tsx`
**Tests:** 12 | **Type:** Form validation + Stripe integration

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | name on card - does not allow empty value | Required field |
| 2 | address line 1 - does not allow empty value | Required field |
| 3 | address line 1 - does not allow value longer than 150 chars | Max length |
| 4 | address line 2 - does not allow value longer than 150 chars | Max length |
| 5 | city - does not allow empty value | Required field |
| 6 | city - does not allow value longer than 50 chars | Max length |
| 7 | zip code - does not allow empty value | Required field |
| 8 | zip code - does not allow non-digit values | Digits only |
| 9 | zip code - does not allow value shorter than 5 chars | Min length |
| 10 | zip code - does not allow value longer than 5 chars | Max length |
| 11 | uses sandbox Stripe key when hook returns true | Stripe sandbox |
| 12 | uses regular Stripe key when hook returns false | Stripe production |

---

### 4. BillingContactInfo-tests.tsx
**Path:** `apps/settings/src/pages/settingsPages/billingSettings/__tests__/BillingContactInfo-tests.tsx`
**Tests:** 11 | **Type:** Component rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | renders section with correct title | Title display |
| 2 | displays business address correctly | Multi-line address |
| 3 | handles missing address2 gracefully | Null address2 |
| 4 | displays billing email when provided | Email display |
| 5 | shows "Not specified" when billing email is empty | Empty email fallback |
| 6 | renders section with correct data-test attribute | Accessibility |
| 7 | displays subsection titles correctly | Subheading text |
| 8 | handles empty address1 gracefully | Empty string |
| 9 | handles empty city, state, zipCode gracefully | Multiple empty fields |
| 10 | shows edit button when user can edit | Permission: canEdit=true |
| 11 | does not show edit button when user cannot edit | Permission: canEdit=false |

---

### 5. BillingSettingsContainer-tests.tsx
**Tests:** 4 | **Type:** Component integration

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should show both tabs when marketplace is not selected | Tab visibility (no SKUs) |
| 2 | should show tabs when marketplace is selected | Tab visibility (with SKUs) |
| 3 | should show coachmark when user from home | Coachmark step 1 |
| 4 | should show coachmark step 2 when user has no payments | Coachmark step 2 |

---

### 6. EditBillingEmailModal-tests.tsx
**Tests:** 2 | **Type:** Form validation

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | does not allow empty value | Required field |
| 2 | does not allow invalid emails | Email format |

---

### 7. EditBusinessAddressModal-tests.tsx
**Tests:** 8 | **Type:** Form validation

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | address line 1 - does not allow empty value | Required |
| 2 | address line 1 - does not allow value longer than 150 chars | Max length |
| 3 | address line 2 - does not allow value longer than 150 chars | Max length |
| 4 | city - does not allow empty value | Required |
| 5 | city - does not allow value longer than 50 chars | Max length |
| 6 | zip code - does not allow empty value | Required |
| 7 | zip code - does not allow non-digit values | Digits only |
| 8 | zip code - does not allow value shorter/longer than 5 chars | Exact length |

---

### 8. EditMonthlyLimitModal-tests.tsx
**Tests:** 3 | **Type:** Form validation

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | does not allow non-numbers | Numeric validation |
| 2 | does not allow floats | Whole number only |
| 3 | does not allow values less than minimum limit | Feature flag minimum |

---

### 9. EditRolloversModal-tests.tsx
**Tests:** 2 | **Type:** Business logic validation

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | shows validation error when limit set and rollover is not | Rollover required |
| 2 | shows validation error when limit set for last rollover | Last rollover restriction |

---

### 10. FeaturedProviderSection-tests.tsx
**Tests:** 7 | **Type:** Component rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should render single featured provider fee inline | Single provider |
| 2 | should render nothing when no fees provided | Empty array |
| 3 | should render nothing when fees is undefined | Undefined |
| 4 | should render multiple fees as collapsible | Multi-provider |
| 5 | should expand/collapse multiple featured provider fees | Interaction |
| 6 | should display credit card info when provided | Payment method |
| 7 | should sort providers alphabetically when expanded | Sorting |

---

### 11. FpbInvoiceView-tests.tsx
**Tests:** 22 | **Type:** Component rendering + A/B testing

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should render PDF download link when available | PDF link |
| 2 | should not show PDF message when first bill | First bill edge case |
| 3 | should show download link when PDF available on first bill | First bill + PDF |
| 4 | should show disabled download link when isPdfAvailable but no URL | Disabled state |
| 5 | should not show link when isPdfAvailable but no URL on first bill | Hidden link |
| 6 | should render help text with link | Help link |
| 7 | should render total cost | Total display |
| 8 | should render applied credits | Credit display |
| 9 | should render total cost after credit | Cost after credit |
| 10 | should render payments with date and card | Payment details |
| 11 | should render payments without credits | No credits |
| 12 | should render amount due | Amount due |
| 13 | should show thank you message when Paid | Paid status |
| 14 | should not show thank you when not Paid | Unpaid status |
| 15 | should show excess credit message | Credit balance |
| 16 | should not show excess credit when not latest | Restriction |
| 17 | should not render back button when onBack not provided | Optional back |
| 18 | should render sponsored results charge | SPO charge |
| 19 | paid vs free breakdown when date >= 1/1/2026 | Experiment + date guard |
| 20 | no breakdown when date before 1/1/2026 even with flag | Date guard |
| 21 | paid vs free breakdown when date is exactly 1/1/2026 | Boundary date |
| 22 | paid vs free for pre-2026 when date guard off | Flag override |

---

### 12. InvoiceDetailsContainer-tests.tsx
**Tests:** 9 | **Type:** Component integration + routing

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should show loading state | Loading spinner |
| 2 | should show error state when fetch fails | Error display |
| 3 | should render FpbInvoiceView for FPB after Feb 2019 | FPB routing |
| 4 | should render LegacyInvoiceView for non-FPB | Legacy routing |
| 5 | should render Legacy for FPB before Feb 2019 | Historical routing |
| 6 | should use query string billId when prop not provided | Query param fallback |
| 7 | should route to FPB when isFeePerBooking and after Feb 2019 | Routing condition |
| 8 | should route to Legacy when not isFeePerBooking | Routing condition |
| 9 | should generate correct PDF URL | PDF URL generation |

---

### 13. LegacyInvoiceView-tests.tsx
**Tests:** 12 | **Type:** Component rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should render invoice table with correct headers | Table headers |
| 2 | should render all line items | Line items |
| 3 | should render totals correctly | Total calculation |
| 4 | should show timezone disclaimer for FPB items | Disclaimer |
| 5 | should not show disclaimer for non-FPB | Conditional |
| 6 | should show thank you for paid items | Thank you message |
| 7 | should not show thank you for unpaid | Conditional |
| 8 | should render Sales Tax Learn More link | Help link |
| 9 | should not render back button when not provided | Optional |
| 10 | should handle empty line items | Edge case |
| 11 | should show invoice title and trigger print | Print handler |
| 12 | should open print URL in new tab | Window.open + print |

---

### 14. LicenseFeeSection-tests.tsx
**Tests:** 5 | **Type:** Component rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | should render annual license fee | Fee display |
| 2 | should expand/collapse license fee details | Interaction |
| 3 | should display date range | Date range |
| 4 | should display credit card info | Payment method |
| 5 | should not display sales tax when zero | Conditional |

---

### 15. PatientBookingsSection-tests.tsx
**Tests:** 7 | **Type:** Component rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | multi providers as collapsible | Multi-provider UI |
| 2 | single provider inline | Single provider |
| 3 | expand/collapse | Interaction |
| 4 | zero bookings | Empty state |
| 5 | zero bookings when undefined | Undefined input |
| 6 | credit card info | Payment method |
| 7 | sort alphabetically | Sorting |

---

### 16. PricingTab-tests.tsx
**Tests:** 2 | **Type:** Conditional rendering

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | hide pricing when no SKU selected | Empty SKUs |
| 2 | show pricing when SKUs selected | With SKUs |

---

### 17. SkuTitleMap-tests.ts
**Tests:** 5 | **Type:** Business logic

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | Throws for marketplace SKU | Error case |
| 2 | Returns correct string for Intake | Mapping |
| 3 | Returns correct string for PartnerSyndication | Mapping |
| 4 | Returns correct string for Zvs | Mapping |
| 5 | Returns correct string for Bob | Mapping |

---

### 18. apiCalls-tests.ts
**Tests:** 26 | **Type:** API integration

| # | Function Tested | Tests | Pattern |
|---|----------------|-------|---------|
| 1 | fetchPracticeBillingSettings | 2 | success + error |
| 2 | fetchInvoiceDetails | 4 | success + non-200 + exception + DTO shape |
| 3 | setDefaultPaymentMethod | 2 | success + error |
| 4 | deletePaymentMethod | 2 | success + error |
| 5 | updatePracticeBillingEmail | 2 | success + error |
| 6 | updatePrimaryBusinessAddress | 3 | success + error + 400 message |
| 7 | setDefaultPaymentMethodForProvider | 2 | success + error |
| 8 | addCreditCard | 3 | success + error response + network error |
| 9 | addAch | 3 | success + error response + network error |
| 10 | savePaymentMethodAttributes | 2 | success + error |

---

### 19. usePracticeBillingSettings-tests.ts
**Tests:** 3 | **Type:** Hook integration

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | returns error when practiceId is null | Null guard |
| 2 | returns settings if no error | Success |
| 3 | returns error state on error | Error handling |

---

### 20. useShouldUseStripeSandbox-tests.ts
**Tests:** 6 | **Type:** Business logic

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | returns false when feature flag is off | Flag required |
| 2 | returns false when not test practice | Practice flag required |
| 3 | returns false when entity flag not present | Entity flag required |
| 4 | returns true when all conditions met | All conditions |
| 5 | returns false when not test practice (other conditions met) | Precedence |
| 6 | returns false when flag off (other conditions met) | Precedence |

---

### 21. PaymentMethodsListV2-tests.tsx
**Tests:** 11 | **Type:** Component rendering + interaction

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | renders payment methods list | List rendering |
| 2 | displays empty state | No payment methods |
| 3 | shows title and buttons when canEdit | Edit mode |
| 4 | hides buttons when canEdit false | Read-only |
| 5 | renders "Edit rollovers" link | Link visibility |
| 6 | no "Edit rollovers" link without methods | Conditional |
| 7 | opens AddPaymentMethodModal on "Add" click | Modal trigger |
| 8 | opens EditRolloversModal on "Edit rollovers" | Modal trigger |
| 9 | opens PaymentMethodsPerProviderModal | Modal trigger |
| 10 | renders "See by provider" link | Link visibility |
| 11 | no "See by provider" link without providers | Conditional |

---

### 22. PaymentMethodV2-tests.tsx
**Tests:** 22 | **Type:** Component + API integration

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | renders with correct description | Display |
| 2 | displays default tag | Default indicator |
| 3 | does not display default tag | No indicator |
| 4 | shows monthly limit | Limit display |
| 5 | hides monthly limit when not set | Conditional |
| 6 | opens more menu | Menu interaction |
| 7 | shows "Replace" only for single non-rollover | Menu item visibility |
| 8 | does not show "Replace" for multiple | Menu restriction |
| 9 | disables "Set as default" for default | Disabled state |
| 10 | disables "Set as default" when only one | Disabled state |
| 11 | shows "Edit limit" when limit exists | Menu item |
| 12 | shows "Set limit" when no limit | Menu item |
| 13 | disables "Delete" for default | Disabled state |
| 14 | disables "Delete" when only one | Disabled state |
| 15 | calls setDefault API | API invocation |
| 16 | calls onSetDefault callback on success | Callback |
| 17 | displays error on API failure | Error display |
| 18 | opens AddPaymentMethodModal on "Replace" | Modal trigger |
| 19 | opens DeleteConfirmation on "Delete" | Modal trigger |
| 20 | calls deletePaymentMethod API | API invocation |
| 21 | opens EditMonthlyLimit on "Edit limit" | Modal trigger |
| 22 | clears error on successful operation | State cleanup |

---

### 23. PaymentMethodsPerProviderModal-tests.tsx
**Tests:** 5 | **Type:** Component rendering + interaction

| # | Test Name | What It Checks |
|---|-----------|---------------|
| 1 | renders modal with correct title | Title |
| 2 | displays all providers with avatars | Provider list |
| 3 | default method has "(Default)" in dropdown | Indicator |
| 4 | updates provider payment method on change | Dropdown interaction |
| 5 | displays error on API failure | Error display |

---

### 24-25. SKU Tests (provider-home-webapp)

**skuService-test.ts** — ~25 tests for SKU updates and ClaimYourProfile task status transitions
**skuValidator-tests.ts** — ~20 tests for SKU activation/selection/enrollment status validators

*(These are outside the main billing settings area but relate to billing SKU management)*
