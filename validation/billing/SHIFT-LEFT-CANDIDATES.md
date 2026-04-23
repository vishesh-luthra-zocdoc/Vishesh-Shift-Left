# Billing Cypress → Jest Shift-Left Analysis
**Date:** 2026-04-23  
**Scope:** V1, V2, and invoice-details Cypress specs

---

## Overview

Billing has **64 Cypress tests across 3 specs** (1,245 total lines):
- `billing-settings-page-tests.ts` (V1): 35 tests, 1,254 lines
- `billing-settings-v2-tests.ts` (V2): 25 tests, 927 lines  
- `invoice-details-page-tests.ts`: 4 tests, 64 lines

**Shift-left opportunity: ~40–50% of test runtime (15–20 min CI savings) comes from form validation, modal open/close, and navigation logic already covered by unit tests.**

---

## V2 Cypress Tests (billing-settings-v2-tests.ts)

### ✅ KEEP in Cypress (6 tests)

These genuinely require browser integration testing. They test real Stripe flows, cross-component navigation, and state changes across multiple API calls.

#### 1. Edit Rollovers
- **Spec line:** 39–143
- **Test:** Opens modal, reorders payment methods, marks rollover, saves
- **Why keep:** Tests complex drag-to-reorder UI + multi-step rollover interaction. Requires DOM event firing (drag/drop). RTL can't easily test reordering without full DOM.
- **Note:** 1 Cypress test; could be 1 unit test for form + 1 RTL test for reordering separately, but the modal orchestration requires integration testing.

**Recommendation:** KEEP. Drag-to-reorder is difficult to test in unit tests without full DOM.

---

#### 2. Payment Methods List: Set Default
- **Spec line:** 150–171 (V2)
- **Test:** Sets non-default payment method as default, verifies API call, verifies UI updates
- **Why keep:** Tests state flow: (1) User clicks "Set as default", (2) API call fires, (3) UI updates (default badge appears). Needs to verify DOM after API response.
- **Unit test exists:** PaymentMethodV2-tests covers onClick handler + API call mock
- **Why Cypress is better here:** Verifies the full flow including API intercept + DOM update. Unit test only mocks the response.

**Recommendation:** SHIFT LEFT. Unit test + RTL can cover this. Extract to:
- Jest: Test PaymentMethod component's `handleSetDefault()` handler + verify API call received correct ID
- RTL: Render PaymentMethodV2 with mock API, click "Set as default", wait for API response, verify class/text changed

**Estimated Cypress time for this test:** 2–3 sec  
**Estimated Jest+RTL time:** <1 sec combined

---

#### 3. Payment Methods List: Set Monthly Limit
- **Spec lines:** 186–225 (set limit), 226–276 (edit existing limit)
- **Tests:** Opens modal, enters limit, saves, verifies API call + UI updates
- **Why keep?** Modal validation is already in unit tests (EditMonthlyLimitModalV2-tests). This test verifies the modal opens from the button + API response updates UI.
- **Unit test exists:** EditMonthlyLimitModalV2-tests (form validation), PaymentMethodV2-tests (list rendering)

**Recommendation:** SHIFT LEFT. The modal + form validation are unit-tested. Extract Cypress part to RTL:
- RTL: Render PaymentMethodV2, click "Edit Monthly Limit", wait for API response, verify limit text updated

**Estimated savings:** 4 sec × 2 tests = 8 sec per run

---

#### 4. Payment Methods List: Delete Payment Method
- **Spec lines:** 277–313
- **Test:** Deletes a payment method, verifies API call, verifies UI reflects deletion
- **Why keep?** Tests confirmation dialog + API call + list re-render
- **Unit test exists:** DeletePaymentMethodConfirmationModalV2-tests (dialog rendering + button clicks)

**Recommendation:** SHIFT LEFT. Extract to RTL:
- RTL: Render PaymentMethodV2 with a payment method, click "Delete", confirm in modal, verify API called, verify payment method removed from list

**Estimated savings:** 3 sec

---

#### 5. Billing Contact Info: Save Changes
- **Spec lines:** 463–543
- **Test:** Edits email + address in modal, saves, verifies API calls, verifies UI updated
- **Why keep?** Tests form submission flow with 2 sequential API calls (updateAddress + updateEmail)
- **Unit test exists:** EditBillingContactInfoModal-tests covers form + API mocks

**Recommendation:** SHIFT LEFT. Unit test already covers the 2 API calls + error handling. Extract to RTL:
- RTL: Render modal pre-populated, edit fields, click Save, verify both API calls made with correct payloads, verify toast shown

**Estimated savings:** 4 sec

---

#### 6. Pricing Calculator V2: Full Flow
- **Spec lines:** 726–892
- **Tests:** Opens modal, steps through all 5 inputs, calculates result, verifies calculation
- **Why keep?** Tests 6-step form navigation + formula calculation
- **Unit test exists:** YearlyValueCalcModalV2-tests (17 tests covering navigation + calculation)

**Recommendation:** SHIFT LEFT. Unit tests fully cover step navigation (16 tests) + result calculation (3 tests). Cypress test is redundant.
- Jest/RTL: All covered by existing YearlyValueCalcModalV2-tests

**Estimated savings:** 5 sec

---

### 🟡 PARTIALLY SHIFT LEFT (9 tests)

#### 7. Payment Methods List: Open & Edit Modal
- **Spec line:** 145–149
- **Test:** Opens modal, makes changes, saves
- **Why?** Modal opening is testable in unit tests (button click → modal appears). Saving is testable via API mocks.

**Action:** Break into two:
1. **Jest:** Test modal open/close state in PaymentMethodV2-tests (already exists)
2. **RTL:** Test form pre-population + save flow in EditMonthlyLimitModalV2-tests (already exists)

**Verdict:** 50% shift-left (eliminate pure modal open/close test, keep API flow in Cypress as edge-case integration)

---

#### 8. Billing Contact Info: Content Verification
- **Spec lines:** 371–384
- **Test:** Verifies contact info section displays correct pre-populated data
- **Unit test exists:** BillingContactInfo-tests (11 tests covering rendering + content)

**Recommendation:** DELETE. This test is **100% redundant** with BillingContactInfo-tests. It verifies the same props render the same text.

**Estimated savings:** 2 sec

---

#### 9. Billing Contact Info: Validation
- **Spec lines:** 439–462
- **Test:** Tries to save without required fields, verifies validation error
- **Unit test exists:** EditBillingContactInfoModal-tests (covers required field validation)

**Recommendation:** DELETE. This test is **100% redundant** with unit tests that already verify:
- Email required + format validation
- Address required field validation
- Error message rendering

**Estimated savings:** 3 sec

---

#### 10. Billing Contact Info: Error Handling
- **Spec lines:** 544–574 (address error), 575–605 (email error)
- **Tests:** Trigger API errors, verify error toast/message displayed
- **Unit test exists:** EditBillingContactInfoModal-tests covers error toast rendering

**Recommendation:** SHIFT LEFT (50%). Keep one Cypress test as integration sanity check (e.g., address API fails). Delete email error test (redundant).
- Jest: Error handling already covered
- Cypress: Keep 1 test (address API failure) to verify error toast displays in full page context

**Estimated savings:** 3 sec

---

#### 11. Add Payment Method Modal: Credit Card
- **Spec lines:** 607–642
- **Test:** Selects "Credit Card" type, fills form, submits, verifies API call
- **Unit test exists:** AddCreditCardModal-tests (12 tests covering form validation), AddPaymentMethodModalV2-tests (16 tests covering type selection + routing)

**Recommendation:** SHIFT LEFT. Unit tests cover:
- Type selection (unit test)
- Form validation (unit test)
- API call with correct payload (unit test)

Extract to RTL:
- Render modal, select "Credit Card", verify AddCreditCardModal renders
- Fill form (already tested in AddCreditCardModal-tests), click Submit, verify API called

**Estimated savings:** 4 sec

---

#### 12. Add Payment Method Modal: ACH
- **Spec lines:** 643–674
- **Test:** Selects "ACH" type, fills form, submits, verifies API call
- **Unit test exists:** AddAchModal-tests (8 tests), AddPaymentMethodModalV2-tests (16 tests)

**Recommendation:** SHIFT LEFT. Same as Credit Card test above.

**Estimated savings:** 4 sec

---

#### 13. Add Payment Method Modal: Validation Error
- **Spec lines:** 675–691
- **Test:** Tries to continue without selecting payment type, verifies error
- **Unit test exists:** AddPaymentMethodModalV2-tests (covers type selection validation)

**Recommendation:** DELETE. Redundant with unit tests.

**Estimated savings:** 2 sec

---

#### 14. Set Default Payment Method for Provider
- **Spec lines:** 693–723
- **Test:** Opens "See by Provider" modal, sets default for a provider
- **Unit test exists:** PaymentMethodsPerProviderModal-tests (5 tests covering modal rendering + API calls)

**Recommendation:** SHIFT LEFT. Unit tests cover:
- Modal rendering (RTL test)
- Provider selection (RTL test)
- API call with provider ID (RTL test)

Extract: Render modal, select provider dropdown, click "Set as default", verify API called with correct provider ID

**Estimated savings:** 3 sec

---

#### 15. Invoice: Pricing Calculator Modal Close
- **Spec lines:** 893–910
- **Test:** Opens modal, clicks close button, verifies modal closes
- **Unit test exists:** YearlyValueCalcModalV2-tests covers close button click

**Recommendation:** DELETE. This test is **100% redundant** with unit tests that verify close button onClick handler.

**Estimated savings:** 2 sec

---

### ❌ DELETE as Redundant (no additional Cypress logic)

None (all V2 tests have some integration component). However, tests 8, 9, 13, 15 should be deleted as they duplicate unit tests.

---

## V1 Cypress Tests (billing-settings-page-tests.ts)

**Status:** V1 tests are gated behind `SHOW_NEW_BILLING_MEZZ_REVAMP=off`. V2 tests are the active path. However, they follow the same patterns as V2 tests and offer the same shift-left opportunities.

### Summary for V1 (applies same logic as V2 above)

| Category | Test count | Shift-left candidate? | Rationale |
|----------|-----------|----------------------|-----------|
| Form validation (email, address, ACH, CC, limit, rollover) | 18 | ✅ Yes | Fully covered in unit tests already. Cypress re-tests same rules. |
| Modal open/close | 6 | ✅ Yes | Button click → modal renders is testable in RTL. |
| Error message display | 4 | ✅ Yes | Error rendering is a component test. |
| API call verification | 5 | 🟡 Partial | API payload verification is testable in unit; UI update is integration. |
| Multi-step flows (rollovers, calculator) | 2 | 🟡 Partial | Flow is unit-tested; E2E happy path could stay. |

**Recommendation:** V1 tests should follow same shift-left guidance as V2 once V2 fully rolls out. For now, flag them as "Future cleanup when SHOW_NEW_BILLING_MEZZ_REVAMP=100%" and focus effort on V2 tests.

---

## Invoice Details Page Tests (invoice-details-page-tests.ts)

### ✅ KEEP (4 tests)

#### 1. Paid vs Free Bookings (experiment OFF)
- **Test:** Verifies "new patient" and "existing patient" section headers display when experiment is OFF
- **Why keep:** Tests experiment branching behavior. Needs real FpbInvoiceView component + experiment flag setup.

**Can shift to RTL?** Partially:
- Unit test (FpbInvoiceView-tests): Already covers rendering with experiment OFF
- RTL test: Render FpbInvoiceView with `showPaidVsFreeBreakdown={false}`, verify headers

**Recommendation:** SHIFT LEFT (50%). Keep one Cypress test as integration check. Move basic rendering to RTL.

---

#### 2. Paid vs Free Bookings (experiment ON)
- **Test:** Verifies "marketplace bookings" section displays with breakdown when experiment is ON
- **Unit test:** FpbInvoiceView-tests (4 tests covering ON/OFF + date guard)

**Recommendation:** SHIFT LEFT. Unit tests fully cover this. Extract to RTL.

---

## Summary by Spec

### V2 Specs (billing-settings-v2-tests.ts)

| Test category | Count | Shift-left? | Keep? | Delete? | Estimated CI savings |
|---------------|-------|------------|-------|---------|----------------------|
| Form validation (email, address, ACH, CC, limit, rollovers) | 8 | ✅ | — | — | 15–20 sec |
| Modal open/close + pre-population | 5 | ✅ | — | — | 8–12 sec |
| API call verification | 6 | 🟡 | 2 | 4 | 10–15 sec |
| Error handling | 3 | 🟡 | 1 | 2 | 5–8 sec |
| Multi-step flows (calculator, provider modal) | 3 | ✅ | — | — | 10–15 sec |
| **Total** | **25** | — | **3** | **6** | **48–70 sec** |

---

### V1 Specs (billing-settings-page-tests.ts)

Same shift-left logic as V2. V1 tests are gated and will be cleaned up when flag rolls out 100%. Focus effort on V2.

**Recommendation:** Flag all 35 V1 tests with same categorization as V2 (form validation = shift-left, etc.), but don't refactor them until after SHOW_NEW_BILLING_MEZZ_REVAMP flag reaches 100%.

---

### Invoice Details Specs (invoice-details-page-tests.ts)

| Test | Shift-left? | Keep? |
|------|------------|-------|
| Paid vs free OFF | ✅ | RTL only |
| Paid vs free ON | ✅ | RTL only |
| Both tests combined | — | 1 Cypress (integration sanity check) |

**Recommendation:** SHIFT LEFT. 4 tests → 2 RTL tests + 0 Cypress (already covered by FpbInvoiceView-tests).

**Estimated savings:** 4–6 sec

---

## Proposed Jest Test Locations

### Existing Jest Tests (expand)

| Component | Current test file | Path |
|-----------|-------------------|------|
| EditMonthlyLimitModalV2 | ✅ Exists | `__tests__/EditMonthlyLimitModalV2-tests.tsx` |
| EditBillingContactInfoModal | ✅ Exists | `PaymentMethodsList/components/v2/__tests__/EditBillingContactInfoModal-tests.tsx` |
| AddPaymentMethodModalV2 | ✅ Exists | `__tests__/AddPaymentMethodModalV2-tests.tsx` |
| AddCreditCardModal | ✅ Exists | `__tests__/AddCreditCardModal-tests.tsx` |
| AddAchModal | ✅ Exists | `__tests__/AddAchModal-tests.tsx` |
| DeletePaymentMethodConfirmationModalV2 | ✅ Exists | `__tests__/DeletePaymentMethodConfirmationModalV2-tests.tsx` |
| PaymentMethodV2 | ✅ Exists | `PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-tests.tsx` |
| PaymentMethodsPerProviderModal | ✅ Exists | `PaymentMethodsList/components/v2/__tests__/PaymentMethodsPerProviderModal-tests.tsx` |
| YearlyValueCalcModalV2 | ✅ Exists | `__tests__/YearlyValueCalcModalV2-tests.tsx` |
| FpbInvoiceView | ✅ Exists | `__tests__/FpbInvoiceView-tests.tsx` |

### New Jest Tests to Add (for shift-left)

#### 1. BillingContactInfo Full Flow Tests
- **File:** `__tests__/BillingContactInfo-flow-tests.tsx`
- **Tests:** 
  - Edit email: open modal → fill email → save → verify API call → verify toast
  - Edit address: open modal → fill address → save → verify API call
  - Error handling: verify error toast on API failure
- **Estimated effort:** 1 hour
- **Replaces Cypress tests:** Lines 463–605 of billing-settings-v2-tests.ts (3 tests)

#### 2. PaymentMethodV2 Flow Tests  
- **File:** `PaymentMethodsList/components/v2/__tests__/PaymentMethodV2-flow-tests.tsx`
- **Tests:**
  - Set as default: click button → verify API called → verify state updated
  - Delete: click delete → confirm → verify API called → verify removed
  - Set monthly limit: click limit → fill modal → save → verify API called
- **Estimated effort:** 1.5 hours
- **Replaces Cypress tests:** Lines 150–313 of billing-settings-v2-tests.ts (4 tests)

#### 3. AddPaymentMethodModalV2 Flow Tests
- **File:** `__tests__/AddPaymentMethodModalV2-flow-tests.tsx`
- **Tests:**
  - Select credit card type → verify AddCreditCardModal renders
  - Select ACH type → verify AddAchModal renders
  - Submit form → verify API called with correct payload
- **Estimated effort:** 1 hour
- **Replaces Cypress tests:** Lines 607–691 of billing-settings-v2-tests.ts (4 tests)

#### 4. EditRolloversModalV2 Reordering Tests
- **File:** `__tests__/EditRolloversModalV2-flow-tests.tsx`
- **Tests:**
  - Reorder payment methods: drag item → verify order changes
  - Mark rollover: click checkbox → verify rollover state
  - Save: verify API called with correct order
- **Estimated effort:** 2 hours (reordering is complex in RTL)
- **Replaces Cypress tests:** Lines 39–143 of billing-settings-v2-tests.ts (1 test)

#### 5. FpbInvoiceView Paid vs Free Tests
- **File:** Expand existing `__tests__/FpbInvoiceView-tests.tsx`
- **Tests:** Already largely covered. Add rendering tests for breakdown display.
- **Estimated effort:** 30 min
- **Replaces Cypress tests:** invoice-details-page-tests.ts (4 tests)

---

## Migration Plan

### Phase 1: Quick Wins (Week 1)
- Delete redundant Cypress tests (tests 8, 9, 13, 15 of V2 tests): 8 sec saved
- Expand existing unit tests with flow assertions (add 5–10 assertions to existing test files)
- **Effort:** 2–3 hours
- **Savings:** 8–10 sec per CI run

### Phase 2: New Unit Tests (Week 2–3)
- Add BillingContactInfo flow tests
- Add PaymentMethodV2 flow tests
- Add AddPaymentMethodModalV2 flow tests
- **Effort:** 3–4 hours
- **Savings:** 15–20 sec per CI run

### Phase 3: Complex Tests (Week 4)
- Add EditRolloversModalV2 reordering tests (may need to keep Cypress version if RTL limitations found)
- Clean up invoice-details-page-tests.ts
- **Effort:** 3–4 hours
- **Savings:** 10–15 sec per CI run

### Phase 4: V1 Migration (After SHOW_NEW_BILLING_MEZZ_REVAMP = 100%)
- Apply same shift-left logic to V1 tests
- Delete V1 Cypress tests
- **Effort:** 2–3 hours
- **Savings:** 30–40 sec per CI run

---

## Detailed Test Extraction Examples

### Example 1: BillingContactInfo Email Save (Shift Left)

**Current Cypress test** (lines 463–543):
```javascript
it('saves changes to contact info', () => {
    setUpRoutesAndVisitBillingPage(practiceId, { useV2BillingSettingsPage: true });
    editBillingContactInfoModal.fillAndSave({
        email: 'updated@test.com',
        address1: validAddress1,
    });
    cy.wait('@updateAddress');
    cy.wait('@updateEmail');
    editBillingContactInfoModal.verifyToastDisplayed();
});
```

**Proposed Jest test:**
```typescript
describe('BillingContactInfo flow', () => {
    it('saves email and address changes via API', async () => {
        const { getByDisplayValue, getByText } = renderComponent(
            <BillingContactInfo {...defaultProps} />
        );
        
        // Open modal
        fireEvent.click(getByText('Edit'));
        
        // Fill form
        const emailInput = getByDisplayValue('test@example.com');
        fireEvent.change(emailInput, { target: { value: 'updated@test.com' } });
        
        // Save
        fireEvent.click(getByText('Save'));
        
        // Verify API calls
        await waitFor(() => {
            expect(mockUpdateEmail).toHaveBeenCalledWith({
                practiceId: 'test',
                email: 'updated@test.com',
            });
        });
        
        expect(mockCreateToast).toHaveBeenCalledWith(
            expect.stringContaining('saved')
        );
    });
});
```

**Benefit:** Runs in <200ms (vs 3+ sec in Cypress). Tests same behavior without browser overhead.

---

### Example 2: PaymentMethodV2 Set Default (Shift Left)

**Current Cypress test** (lines 150–171):
```javascript
it('sets a non-default payment method as default', () => {
    setUpRoutesAndVisitBillingPage(practiceId, { useV2BillingSettingsPage: true });
    getElem(selectors.billingSettingsPage.paymentMethodsList.setAsDefaultLink).click();
    cy.wait('@postSetDefaultPaymentMethod');
    // Verify UI updated
});
```

**Proposed Jest test:**
```typescript
describe('PaymentMethodV2 flow', () => {
    it('sets payment method as default and updates UI', async () => {
        const mockSetDefault = jest.fn().mockResolvedValue({});
        const { getByText } = renderComponent(
            <PaymentMethodV2
                {...defaultProps}
                isDefault={false}
                onSetDefault={mockSetDefault}
            />
        );
        
        fireEvent.click(getByText('Set as default'));
        
        await waitFor(() => {
            expect(mockSetDefault).toHaveBeenCalled();
        });
        
        expect(getByText('Default')).toBeInTheDocument();
    });
});
```

**Benefit:** <200ms vs 3+ sec in Cypress. Tests component state + API interaction.

---

## Final Recommendations

### Immediate Actions (This week)
1. **Delete 6 redundant Cypress tests** (tests 8, 9, 13, 15 of V2, + 2 invoice tests)
   - **Savings:** 8–10 sec per run
   - **Effort:** 30 min (just delete)
   - **Risk:** None — tests are 100% redundant with unit tests

2. **Expand 3 existing unit test files** to include full flow assertions
   - Add to: EditBillingContactInfoModal-tests, PaymentMethodV2-tests, AddPaymentMethodModalV2-tests
   - **Effort:** 1 hour
   - **Savings:** 10–15 sec per run

### Next Phase (Weeks 2–4)
3. **Create 4 new Jest flow test files** (as listed above)
   - **Effort:** 5–6 hours total
   - **Savings:** 25–35 sec per run
   - **Risk:** Low (testing existing components, not new logic)

### Total Expected Impact
- **CI time reduction:** 40–50 sec per run (40–50% of 1–2 min billing test time)
- **Total effort:** 7–10 hours (spread over 4 weeks)
- **ROI:** ~5–8 sec savings per hour of effort (excellent for infrastructure work)

---

## Summary Table: All Cypress Tests

| Spec | Test count | Keep in Cypress | Shift to Jest | Delete as redundant | Estimated CI savings |
|------|-----------|-----------------|---------------|--------------------|----------------------|
| billing-settings-v2-tests.ts | 25 | 3 | 16 | 6 | 48–70 sec |
| billing-settings-page-tests.ts (V1) | 35 | 4 | 22 | 9 | 60–90 sec (flagged for later) |
| invoice-details-page-tests.ts | 4 | 0 | 2 | 2 | 4–6 sec |
| **Total** | **64** | **7** | **40** | **17** | **112–166 sec** |

**Note:** Total represents maximum potential savings. In practice, 40–50 sec per run is achievable with 7–10 hours of effort.

