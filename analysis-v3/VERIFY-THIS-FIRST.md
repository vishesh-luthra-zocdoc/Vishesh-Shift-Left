# Verify This First — 10-Minute Spot-Check

You should not take this analysis on faith, and you don't have to. Below are the claims that, if
wrong, would waste the most of your team's time — each with a command that confirms or refutes it
in seconds.

**Run these from `~/provider-fe-monorepo`.** They read `origin/main` directly, so they do not depend
on your local checkout being fresh (it is 550 commits behind).

If any command's output disagrees with the "Expected" column, **stop and tell me** — that ticket is
wrong and I'll pull it.

---

## 1. The most dangerous claim: v2's #1 P0 is wrong, do not delete `LegacyInvoiceView`

If I'm wrong here, we *should* delete it and I'm blocking a valid cleanup. If I'm right and you
execute v2, you break invoice rendering for providers.

```bash
git show origin/main:apps/settings/src/pages/settingsPages/billingSettings/InvoiceDetailsContainer.tsx \
  | grep -n "LegacyInvoiceView"
```
**Expected:** two hits — an `import` around line 16 and a render around line 201. That means the
component is **live**, not dead.

```bash
git show --stat --format="%s" a88b14cba6 | head -12
```
**Expected:** 6 files changed, and **no** `LegacyInvoiceView` or `InvoiceDetailsContainer.tsx` among
them. v2 cited this commit as the teardown that killed the component. It never touched it.

---

## 2. FE-002: the monthly-limit test really is a tautology

This is a P0 that says an existing green test is worthless. Strong claim, easy to check.

```bash
git show origin/main:apps/settings/src/pages/settingsPages/billingSettings/__tests__/EditMonthlyLimitModalV2-tests.tsx \
  | sed -n '125,140p'
```
**Expected:** the test computes `minimumMonthlyLimit` with
`parseInt(getFeatureFlagVariant('Billing.MinimumPaymentMethodLimit') || '500')` — the same
expression as the source. Then confirm the source uses it too:

```bash
git show origin/main:apps/settings/src/pages/settingsPages/billingSettings/utils/schemaBuilder.ts \
  | grep -n "MinimumPaymentMethodLimit\|maximumMonthlyLimit\|500000"
```
**Expected:** the source reads the same flag with the same `|| '500'` default, and
`maximumMonthlyLimit = 500000` appears. Both sides matching = the test cannot fail. Also confirm
nothing asserts the maximum:

```bash
git grep -n "500000" origin/main -- "*billingSettings*__tests__*"
```
**Expected:** **no output.** The maximum monetary boundary is asserted nowhere.

---

## 3. FE-003: `invoiceHelpers.ts` genuinely has no tests

```bash
git ls-tree -r origin/main --name-only | grep -i "invoiceHelpers"
```
**Expected:** exactly one file — the source. No `invoiceHelpers-tests.ts`.

---

## 4. FE-001: the entire E2E suite mocks Stripe, so it cannot catch a real Stripe break

This justifies the top-priority ticket in the backlog.

```bash
git show origin/main:apps/settings/e2e/fixtures.ts | grep -n "installStripeJsFake"
```
**Expected:** it is called in the shared fixture (~line 32), i.e. applied to **every** spec in the
directory, not opted into per-test.

```bash
git grep -n "SHOULD_MOCK_STRIPE" origin/main -- "apps/settings/src/**"
```
**Expected:** hits in `CreditCardFormContentV2.tsx` (~:52) and `AchFormContentV2.tsx` (~:69) —
**production** files. Production code branching on a test cookie is the finding.

---

## 5. FE-004: six E2E tests wrap all their assertions in a conditional

These report success without testing anything if a fixture changes.

```bash
git show origin/main:apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts \
  | grep -n "if (mock"
```
**Expected:** ~6 hits. Every assertion inside those blocks is skipped when the `find` returns
undefined — a green no-op.

```bash
git show origin/main:apps/settings/e2e/PracticeSettingsPages/billing-settings-v2.spec.ts \
  | sed -n '173,181p'
```
**Expected:** a test whose body is a single `setUpRoutesAndVisitBillingPage(...)` call with **zero
assertions**, and whose title is copy-pasted from an earlier test. Deleting it cannot reduce coverage.

---

## 6. The CI cost claim behind the whole shift-left plan

```bash
git show origin/main:apps/settings/playwright.config.ts | sed -n '1,20p'
```
**Expected:** `retries: isCI ? 1 : 0`, `workers: isCI ? 1 : undefined`, `timeout: 60000`. Despite
`fullyParallel: true`, CI runs **one worker** — so these 63 browser tests run serially. That is the
cost being paid for assertions jsdom could make in milliseconds.

---

## 7. The good news is real too — the yearly calculator fix

```bash
git show origin/main:apps/settings/src/pages/settingsPages/billingSettings/__tests__/YearlyValueCalcModalV2-tests.tsx \
  | sed -n '204,226p'
```
**Expected:** the expected result `'$327'` is **hardcoded**, with the arithmetic worked out by hand in
a comment above it. This is the pattern FE-002 asks us to copy. Landed by **BILL-748**
(`b5cc093d71`) and **BILL-962** (`89f5111df0`) — not BILL-196, which was the feature commit.

---

## What I could not verify, and said so

Honesty about the edges, so you know where the analysis is soft:

| Claim | Status |
|---|---|
| `BILLING_PAGE_ENABLE_IFRAME_DEPRECATION` ramp state | **Unverifiable from code.** `apps/settings/src/ab/` was outside the snapshot. This is an `investigate` ticket with a decision rule, not an assertion. |
| Runtime minutes for the E2E suite | **Estimate.** No real CI run was measured. The serial-execution *basis* is confirmed (item 6); the minute figure is not. |
| Coverage percentages | **Not reported at all.** No coverage tooling was run. Counts come from reading files. |
| Assertion quality across the suite | **Out of scope**, except where noted (FE-002, FE-004). A test existing is not proof it asserts anything useful. |

## How to tell me it's wrong

Per ticket, one of: **"good"**, **"wrong — <what>"**, or **"not now"**. I'll pull or fix before
anything reaches Jira. Nothing has been written to Jira and nothing will be until you say so.
