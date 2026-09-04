# sandbox — Billing E2E (L5) Inventory

**Repo:** `/Users/vishesh.luthra/sandbox` (Playwright, runs against production `https://www.zocdoc.com/`)
**Analyzed revision:** working tree at `dac52b65a3ae89cd756c3951e58ae3fec0ce3b1d` (branch `fix/billing-stripe-payment-element`)
**`origin/main` at time of analysis:** `4bb607cc942b03c067d5755eb8192ebfaf27d227`
**Level:** all tests below are **L5 `e2e`** — real Chromium driving deployed production. No mixed-level files in scope.

## Branch / working-tree caveat (read before ticketing)

Two layers of "not on main" here:

1. `dac52b65 fix: repoint billing add-payment-method helpers at Stripe Payment Element` is **committed but only on `fix/billing-stripe-payment-element`, not on `origin/main` (`4bb607cc`)**. It touches only `playwright/support/billing.ts` (`148 insertions, 167 deletions`, per `git show --stat dac52b65`). Its own commit message states both billing specs "had been failing since 2026-09-02 on selectors for that old markup" — so **on `main` today, all 4 billing tests below are red.**
2. `playwright/support/billing.ts` additionally has **uncommitted working-tree edits** (`git status`: ` M playwright/support/billing.ts`, `git diff --stat`: `14 insertions, 13 deletions`) that replace two hand-rolled `Date.now()` polling loops in `connectStripeTestBank` with `expect.toPass()`. Untracked `playwright.headed.config.ts` also exists (self-described "Not for CI and not to be committed", `playwright.headed.config.ts:1-2`).

Everything below reflects the **working tree**, i.e. including both (1) and (2).

## Files in scope

| File | Tests | Billing tests | Level |
|---|---|---|---|
| `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts` | 2 | 2 | L5 |
| `/Users/vishesh.luthra/sandbox/playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts` | 3 | 2 | L5 |
| **Total** | **5** | **4** | |

Search performed: `grep -ril -E 'billing|invoice|payment|stripe|creditcard|credit-card|\bach\b|cardNumber' playwright/` → 13 hits. Files with *incidental* billing-word matches only, **not** billing coverage (verified by reading each hit):

| File | Match | Why not in scope |
|---|---|---|
| `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/rbac-user-roles-flow.spec.ts:245-590` | `RBAC SMOKE - Billing User` | Tests the *Billing role's* page access, not billing functionality. Asserts `sidebar-settings-billing` reachability/absence only. |
| `playwright/BU/Provider/Retention/Provider-Success/Pages/large-practice-smoke-page.spec.ts:40` | `{ name: "Billing", path: "/provider/config/settings/billing?practiceId=..." }` | Smoke-loads the billing URL as one of N pages. No billing assertions. |
| `playwright/BU/Marketplace/Booking/Flows/patient-appointments-flow.spec.ts:174-201` | `how-billing-works`, `appointment-details-page-v2-billing-option-*` | Patient-side insurance/EOB links. Not provider billing. |
| `playwright/BU/Marketplace/Patient-Acquisition/Flows/criticalTests-{listing,practice}Page-flow.spec.ts` | `"requires self-payment"` copy | Patient-side self-pay messaging. |
| `playwright/BU/Practice-Solutions/Branded-Directory/Flows/intake-flow.spec.ts:404,468` | `// Billing & insurance` comment | Intake form section label. |
| `playwright/fixtures/default_experiments_list.json` | `billing_upgraded_add_payment_method_flow`, `spo_billing_*` | Fixture data, not a test. |
| `playwright/support/index.ts:79-90` | re-exports `./billing` | Barrel file. |
| `playwright/support/billing.ts` | — | Helper module; documented in `support-helpers.md`. |

Adjacent-but-separate money surface, **not** counted: `playwright/support/spend-management.ts` drives real `PUT/DELETE .../spend-management/budget` and `spend-lock` calls (`spend-management.ts:26-62`). That is SPO ad spend, not provider billing, but it is a second real-money-adjacent write surface in this repo.

---

## 1. `playwright/BU/Provider/Acquisition/Provider-Billing/Pages/billing-settings-page.spec.ts`

- **Suite nesting:** `test.describe("/provider/billing")` (`:29`) → `test.describe("Modify billing settings")` (`:30`)
- **Test count: 2.** `test.step` count in file: **24**.
- **Level:** L5 `e2e`.

### Test titles (verbatim)

| # | Line | Title |
|---|---|---|
| 1 | `:52` | `Manage billing settings: layout, payment methods, invoice, contact info, and pricing` |
| 2 | `:342` | `Add and remove a credit card payment method` |

### Test 1 — journey (20 `test.step`s, in order)

`:60` Navigate to billing settings → `:67` Clean up billing state → `:72` Verify billing page structure → `:88` Add a credit card payment method → `:95` Add an ACH payment method → `:102` Set a $5000 monthly limit on the ACH method → `:124` Edit the ACH method's monthly limit to $10000 → `:141` Remove the ACH method's monthly limit → `:153` Set the credit card as the default payment method → `:161` Enable rollover on the ACH method → `:181` Move the ACH method up in rollover priority → `:191` Disable rollover on the added card and ACH methods → `:208` Restore the original default payment method → `:220` Delete the added credit card and ACH methods → `:239` Re-navigate to billing and view invoice → `:258` Back to billing and verify contact info → `:271` Verify edit billing contact info modal → `:305` Edit billing email to automation address → `:319` Restore billing email to original → `:331` Verify the Pricing tab content

Entry path: `page.goto("/provider/inbox/pt_mI_Rr6ZArUeQedbfQXXpJh")` (`:61`) → click `sidebar-settings` → `sidebar-settings-billing` → assert URL `/provider/config/settings/billing` (`:62-64`).

### Test 2 — journey (4 `test.step`s)

`:345` Navigate to billing settings → `:352` Clean up billing state → `:357` Add a credit card payment method → `:364` Delete the credit card payment method. Same inbox→sidebar entry path (`:346-349`).

### Environment / setup (`beforeEach`, `:31-50`)

| Aspect | Value | Evidence |
|---|---|---|
| Viewport | `setViewport(page, "macbook-15")` | `:32` |
| Network stubs | `stubNetworkCalls(page)` — stubs telemetry only (`eventslogger/v2/logevents`, `eventslogging/v1/event`, `api2.branch.io`) | `:33`; `support/network.ts:3-23` |
| AB overrides | `setAbOverrides(context)` → writes `testAbSystemOverrides` cookie from `loadAbOverrides()` default map | `:34`; `support/ab.ts:42-56` |
| Frontend experiment mock | `page.route("**/phi-ab/v1/www/experiments*")` fulfilled with `playwright/fixtures/default_experiments_list.json` (1516 `experiment_id` entries), which pins `{"assignment":"on","experiment_id":"billing_upgraded_add_payment_method_flow"}` | `:23`, `:42-49`; fixture |
| Auth | `loginByAPI(request, context, BILLING_EMAIL, <password literal>)` → real `POST /accounts/v2/authentication/authenticate-password` | `:35`; `support/auth.ts:108-123` |
| Test account | `BILLING_EMAIL = "<test-account-email>"` (`:27`) — reused as login **and** billing-contact email **and** ACH account-holder email | `:27`, `:35`, `:69`, `:97`, `:325` |
| Credential storage | **Hardcoded plaintext literal at `:35`** (value redacted here). No env var, no fixture, no secret store. | `:35` |
| localStorage seeding | `has_seen_billing_completion_modal`, `has_seen_detabbed_inbox_page_tutorial` = `"true"` | `:37-40` |
| Practice under test | `pt_mI_Rr6ZArUeQedbfQXXpJh` (inbox id in the nav URL) | `:61` |
| Extra AB header | none set in this spec (no `ZD-Experiment-Overrides`) | grep: absent |

### Support helpers called

From `../../../../../support` (`:3-20`): `loginByAPI`, `stubNetworkCalls`, `setAbOverrides`, `setViewport`, `clickByDataTest`, `waitForURLMatch`, `scrollAndClick`, `cleanupBillingState`, `saveModalAndClose`, `reloadPaymentMethods`, `addAchPaymentMethodV2`, `addCreditCardV2`, `paymentMethodRowById`, `rolloverRowById`, `ADDED_CREDIT_CARD_LAST4`, `ADDED_ACH_ACCOUNT_LAST4`. Fixture import: `{ test, expect }` from `../../../../../support/fixtures` (`:21`) — conforms to the `CLAUDE.md` rule.

---

## 2. `playwright/BU/Provider/Acquisition/Account-User-Setup/Flows/billing-user-flow.spec.ts`

- **Test count: 3** (1 non-billing + 2 billing). `test.step` count in file: **24**.
- **Level:** L5 `e2e`.
- **Structural problem:** this one file mixes two unrelated features under two unrelated accounts — an appointment-report RBAC test and a full duplicate of the billing-settings suite. It also sits under `Account-User-Setup/`, not `Provider-Billing/`, so a `Provider-Billing`-scoped CI slice (`./run-playwright.sh "BU/Provider/Acquisition/Provider-Billing"`) will silently miss half the repo's billing coverage.

### Test titles (verbatim)

| # | Line | Title | Billing? |
|---|---|---|---|
| 1 | `:59` | `Billing user can navigate to appointment report and view patient data (PROVPERF-2665)` | No — Performance/appointment-report page, tested *as* a Billing-role user |
| 2 | `:119` | `Manage billing settings: layout, payment methods, invoice, contact info, and pricing` | Yes |
| 3 | `:414` | `Add and remove a credit card payment method` | Yes |

Note: titles of tests 2 and 3 are **byte-identical** to tests 1 and 2 of `billing-settings-page.spec.ts`, inside an identically-named `describe` nest (`test.describe("/provider/billing")` `:87` → `test.describe("Modify billing settings")` `:88`). `-g "Manage billing settings..."` therefore selects both.

### Describe block A — `Billing user can access appointment report and see patient data` (`:32`)

| Aspect | Value | Evidence |
|---|---|---|
| Viewport | `macbook-15` | `:34` |
| Auth | `loginByAPI(..., "<test-account-email-2>", <password literal>)` | `:37` |
| Cookies | `has_seen_invite_coachmark_v2=true` | `:38-45` |
| Init script | overrides `window.open` to same-tab navigation | `:46-51` |
| Entry | `goto https://www.zocdoc.com/practice/pt_gpAP793H-UyGE6HiNwy7ox/dashboard` (`PRACTICE_ID`, `:25`) | `:52-54` |
| Journey (test 1) | Waits on `GetAppointmentReport` GraphQL op at `/provider/v1/gql`, asserts 200; asserts `provider-filter`, `patient-type-filter`, appointments table, patient column header, and that row 1 matches `/DOB\s+\d{1,2}\/\d{1,2}\/\d{4}/` | `:60-84` |
| Helpers | `loginByAPI`, `stubNetworkCalls`, `setAbOverrides`, `setViewport`, `providerSidebarSubmenuNavigation` | `:3-22`, `:70` |
| PHI note | asserts a real patient DOB pattern is rendered on production. It matches a *shape*, not a value, so no PHI is written into the repo — but failure artifacts (`trace: "retain-on-failure"`, `screenshot`, `video`, `playwright.config.ts:29-31`) will capture real patient rows. | `:83`, `playwright.config.ts:29-31` |

### Describe block B — `/provider/billing` › `Modify billing settings` (`:87-88`)

| Aspect | Value | Evidence |
|---|---|---|
| Viewport | `macbook-16` (**differs** from the other spec's `macbook-15`) | `:90` |
| Network stubs | `stubNetworkCalls(page)` | `:91` |
| AB overrides | `setAbOverrides(context)` | `:92` |
| Frontend experiment mock | same `**/phi-ab/v1/www/experiments*` → `default_experiments_list.json` route | `:26`, `:108-115` |
| Cookies | `zd_global_nav_coachmark_shown=true` | `:93-100` |
| localStorage | `has_seen_billing_completion_modal`, `has_seen_detabbed_inbox_page_tutorial` | `:102-105` |
| Auth | `loginByUI(page, BILLING_USER_EMAIL, <password literal>)` — real sign-in **through the UI**, unlike the other spec's API login | `:117`; `support/auth.ts:66-76` |
| Test account | `BILLING_USER_EMAIL = "<teammate-test-account-email>"` (`:30`) — a **different** account and a **different domain** from block A's `<test-account-email-2>` (`:37`) and from the other spec's `<test-account-email>` | `:30`, `:37` |
| Credential storage | **Hardcoded plaintext literals at `:37` and `:117`** (values redacted). No env var / fixture. | `:37`, `:117` |
| Practice under test | Not stated. Block B never sets a practice; it relies on whatever practice `<teammate-test-account-email>` lands on. `PRACTICE_ID` (`:25`) is used only by block A. **UNVERIFIED** — resolving which practice this is requires querying the account, which cannot be done from the repo. |

### Test 2 (`:119`) — journey (20 `test.step`s)

`:127` Navigate to billing settings (direct `goto /provider/config/settings/billing`, `:128`) → `:132` Verify billing page structure → `:148` **Reset billing state to baseline** → `:152` Add a credit card payment method → `:159` Add an ACH payment method → `:166` Set a $5000 monthly limit on the ACH method → `:188` Edit the ACH method's monthly limit to $10000 → `:205` Remove the ACH method's monthly limit → `:217` Set the credit card as the default payment method → `:225` Enable rollover on the ACH method → `:245` Move the ACH method up in rollover priority → `:255` Disable rollover on the added card and ACH methods → `:272` Restore the original default payment method → `:284` Delete the added credit card and ACH methods → `:303` Re-navigate to billing and view invoice → `:328` Back to billing and verify contact info → `:341` Verify edit billing contact info modal → `:375` Edit billing email to automation address → `:389` Restore billing email to original → `:401` Verify the Pricing tab content

### Test 3 (`:414`) — journey (4 `test.step`s)

`:417` Navigate to billing settings (sidebar path, unlike test 2's direct `goto`) → `:423` Reset billing state to baseline → `:428` Add a credit card payment method → `:435` Delete the credit card payment method.

### Support helpers called

`loginByAPI`, `loginByUI`, `stubNetworkCalls`, `setAbOverrides`, `setViewport`, `waitForURLMatch`, `scrollAndClick`, `clickByDataTest`, `providerSidebarSubmenuNavigation`, `addAchPaymentMethodV2`, `addCreditCardV2`, `cleanupBillingState`, `saveModalAndClose`, `reloadPaymentMethods`, `paymentMethodRowById`, `rolloverRowById`, `ADDED_CREDIT_CARD_LAST4`, `ADDED_ACH_ACCOUNT_LAST4` (`:3-22`). `{ test, expect }` from `../../../../../support/fixtures` (`:23`).

---

## Internal duplication (sandbox vs sandbox)

Block B of `billing-user-flow.spec.ts` is a near-verbatim copy of the whole of `billing-settings-page.spec.ts`.

Measured: extracting the `/provider/billing` describe from each (`billing-settings-page.spec.ts:29-380` = 352 lines; `billing-user-flow.spec.ts:87-451` = 365 lines) and diffing gives **63 differing lines** — i.e. ~82% of the block is byte-identical, including comments. Substantive differences, exhaustively:

| Difference | `billing-settings-page.spec.ts` | `billing-user-flow.spec.ts` |
|---|---|---|
| Auth method | `loginByAPI` (`:35`) | `loginByUI` (`:117`) |
| Account | `<test-account-email>` (`:27`) | `<teammate-test-account-email>` (`:30`) |
| Viewport | `macbook-15` (`:32`) | `macbook-16` (`:90`) |
| Cookie | none extra | `zd_global_nav_coachmark_shown` (`:93`) |
| Test-2 entry | inbox → sidebar (`:61-64`) | direct `goto` (`:128`) |
| Step ordering | cleanup **before** structure assertions (`:67`, `:72`) | cleanup **after** (`:132`, `:148`) |
| Invoice step | no reload (`:239-256`) | `page.reload({waitUntil:"domcontentloaded"})` first, to prove deletions persisted server-side (`:304-310`) |
| Pricing step | asserts `free-products-card` + `pricing-contact-us` (`:337-338`) | same, plus a comment documenting a suspected product bug: enterprise practices render Pricing without `marketplace-card` (`:405-411`) |

The two blocks therefore run the same ~20 destructive production mutations twice per suite run, roughly doubling the money-surface write volume and the wall-clock cost for one extra assertion (persistence-after-reload) and one extra login path.

---

## Money-critical / blast-radius assessment

Everything in `Modify billing settings` is a **real write against a real production practice**, with no mock in the payment path. Explicitly:

| Mutation | Real? | Evidence |
|---|---|---|
| Tokenize a card in Stripe and attach it to the practice | Yes — Stripe test card `4242…4242` driven through Stripe's live Payment Element iframe | `support/billing.ts:268-298`; `"Fills Stripe's Payment Element card fields directly (no mocking)"` `billing.ts:276-278` |
| Link a bank account via Stripe Financial Connections OAuth | Yes — Stripe sandbox institution `"Test (OAuth)"`, "through the real OAuth flow (no mocking)" | `billing.ts:124`, `201-226`, `239-264` |
| Set / edit / remove a payment method monthly limit ($5000 → $10000 → none) | Yes — `savePaymentMethodAttributes` | spec `:102-151`; `billing.ts:71-89` |
| Change which payment method is **default** | Yes | spec `:153-159`, `:208-218` |
| Enable / reorder / disable **rollover** payment methods | Yes | spec `:161-206` |
| **Delete** payment methods | Yes, and pre-emptively: `cleanupBillingState` deletes rows until only 2 remain | spec `:220-237`; `billing.ts:318-336` |
| Change the practice's **billing email** to `<billing-automation-email>` | Yes, then restores it | spec `:305-329` |
| Download-invoice-PDF button | Assert-enabled only; not clicked | spec `:250-251` |

Blast radius:

1. **`cleanupBillingState` is unconditionally destructive on entry, not on exit.** It deletes payment methods down to 2 (`billing.ts:318-336`), rewrites the default (`:306-316`), rewrites rollover state (`:338-348`) and rewrites the billing email (`:350-364`) — before any assertion runs. Its own comment says this is deliberate so it self-heals from prior crashes (`:300-304`). Consequence: **any human or process that adds a payment method to one of these three accounts loses it on the next suite run**, with no confirmation prompt and no record of what was deleted.
2. **`retries: 2`** (`playwright.config.ts:10`) means a mid-test failure re-runs the whole destructive sequence up to 3×. There is no `test.describe.configure({ retries: 0 })` on either billing describe, unlike `practice-locations-page.spec.ts:1027,1177` which explicitly sets `retries: 0` for exactly this reason ("retries: 2 from the config would be catastrophic here").
3. **Restore steps are best-effort and unguarded.** `"Restore the original default payment method"` (`:208`) sets the default to whatever is currently row 0 — not to whatever it was before the test. If the pre-test default was not row 0, the test leaves the practice with a *different* default payment method than it found. Similarly the billing email is restored only if the test reaches `:319`; a timeout at `:331` (Pricing tab) leaves the practice's billing email as `<billing-automation-email>` until the next run's cleanup notices.
4. **Real invoices are read, not synthesized.** `bill-row` / `fpb-invoice-view` / `amount-due-row` (`:244-249`) assert against this practice's actual production invoices. If the account is ever billed a real amount, the test asserts on real financial data; if it has no bills, `expect(billRows.first()).toBeAttached()` fails for a reason unrelated to the code under test.
5. **Third-party dependency in the hot path.** Both add flows depend on Stripe's hosted UI — `iframe[src*="linked-accounts-inner"]` (`billing.ts:118`), Stripe's own `#card-tab` / `#payment-numberInput` ids, and copy-matched buttons in Stripe's Financial Connections modal (`billing.ts:168-174`). Any Stripe UI change breaks the suite with no product regression, and vice versa. `dac52b65` is that exact failure mode having already happened once.

---

## Serialization constraint: documented or tribal?

The user's own memory note (`~/.claude/.../memory/billing-specs-share-one-practice.md`, per the index entry "Billing specs share one practice — parallel workers make them delete each other's cards; use `--workers=1`") records a hard operational constraint. **In the repository itself, that constraint is nowhere.** Verified:

| Where you'd document it | Present? | Evidence |
|---|---|---|
| `playwright.config.ts` `workers` key | **Absent.** Only `fullyParallel: false` is set. | `playwright.config.ts:11`; `grep -n workers playwright.config.ts` → no match |
| `test.describe.configure({ mode: "serial" })` on either billing describe | **Absent.** Six other specs in the repo do use it (`user-management-page.spec.ts:17`, `appointment-mgmt-user-flow.spec.ts:1139`, `practice-locations-page.spec.ts:1027,1177`, `calendar-page.spec.ts:146`, `intake-flow.spec.ts:183`) — so the idiom exists and was simply not applied to billing. | repo-wide grep for `serial` |
| `--workers` in `run-playwright.sh` / `run-playwright-impacted.sh` / `package.json` | **Absent.** CI runs bare `npx playwright test --project=chromium` (`run-playwright.sh:21`). | `grep -rn -- '--workers'` → no match anywhere outside `node_modules` |
| `README.md` | **No mention of billing, workers, serial or parallel at all.** | `grep -n -i -E 'billing\|workers\|serial\|parallel' README.md` → no match |
| `CLAUDE.md` | Documents `--repeat-each`, headed mode, and the BU hierarchy. **No `--workers`, no billing note.** | `CLAUDE.md:11-44, 87-103` |
| Comment in either billing spec or in `support/billing.ts` | **Absent.** The comments do warn about *shared-account* pollution (`billing-settings-page.spec.ts:25-27, 57-58`; `billing.ts:4-9, 300-304`) but never say "run with one worker". | file reads |

**Finding.** `fullyParallel: false` only serializes tests *within* a file; Playwright still distributes *files* across workers, and with no `workers` setting it defaults to half the machine's logical cores. So `billing-settings-page.spec.ts` and `billing-user-flow.spec.ts` will be picked up by two different workers on any full-suite run, and both call the destructive `cleanupBillingState`. The repo also has no `process.env.CI` guard — `run-playwright.sh:11` sets `DEPLOY_ENV=ci`, not `CI`, so Playwright's own CI heuristics never fire. The one thing standing between these two specs and mutual card deletion today is that they log in as **different** accounts (`<test-account-email>` vs `<teammate-test-account-email>`). Whether those two accounts resolve to the same *practice* is **UNVERIFIED** from the repo — that requires querying the accounts. If they do, the collision is live and undocumented. Either way, the mitigation currently exists only as a flag one engineer remembers to type.

---

## Candidate Gaps

| # | What's missing | Correct level | File path(s) | Why it matters | Effort | Priority |
|---|---|---|---|---|---|---|
| G1 | Billing suite's `--workers=1` / same-practice serialization requirement is documented nowhere in the repo — not in `playwright.config.ts`, the run scripts, `README.md`, `CLAUDE.md`, or a code comment. A full-suite run schedules the two billing spec files on separate workers, both of which delete payment methods on entry. | L5 | `playwright.config.ts:11`, `run-playwright.sh:21`, both billing specs | A destructive-write constraint that lives only in tribal knowledge will be violated by the next person who runs the suite or wires up a new CI job. Fix is cheap: `test.describe.configure({ mode: "serial" })` plus a comment, or move both billing describes into one file. | S | **P0** |
| G2 | `retries: 2` applies to both billing tests, so a mid-sequence failure replays ~20 real production billing mutations up to 3×. `practice-locations-page.spec.ts:1027,1177` already sets `retries: 0` for exactly this hazard; billing does not. | L5 | `playwright.config.ts:10`; `billing-settings-page.spec.ts:30`; `billing-user-flow.spec.ts:88` | Amplifies every write in the money path 3× and multiplies the window in which the practice sits in a half-mutated state. | S | **P0** |
| G3 | Test-account passwords are hardcoded plaintext literals in three places in tracked spec files. | L5 | `billing-settings-page.spec.ts:35`; `billing-user-flow.spec.ts:37,117` | Credentials for accounts that can mutate production billing state are committed to git. Should be env vars resolved in `support/auth.ts`. | S | **P1** |
| G4 | ~82% of `billing-user-flow.spec.ts:87-451` duplicates `billing-settings-page.spec.ts` (63 differing lines out of ~352), including identical `describe` and `test` titles. | L5 | both files | Doubles production billing writes and suite runtime; identical titles break `-g` selection and confuse Jira/Xray reporting (`playwright/jira-reporter/`). Collapse to one spec plus a thin second case for the extra `loginByUI` + reload-persistence assertions. | M | **P1** |
| G5 | No negative-path coverage anywhere: declined card, invalid card number, expired card, failed ACH micro-deposit/verification, `savePaymentMethodAttributes` 500, delete-last-payment-method, delete-the-default-method. Every existing test is a happy path. `support/billing.ts:91-115` and `:55-69` exist purely to *retry past* server errors rather than assert them. | L5 (some better as L2/L3 in the monorepo) | `Provider-Billing/Pages/` | Payment-method failure handling is what actually costs money when it breaks. Right now a regression that makes every card decline would still pass this suite as long as Stripe's happy path works. | M | **P1** |
| G6 | `Provider-Billing/` has **no `Flows/` directory at all** and `Pages/` still carries the placeholder `.gitkeep` from the folder-scaffolding commit `9f5d06df`. All of the BU's actual multi-step flow coverage lives in another team's folder (`Account-User-Setup/Flows/`). | L5 | `playwright/BU/Provider/Acquisition/Provider-Billing/` | A CI slice scoped to `BU/Provider/Acquisition/Provider-Billing` (the documented pattern, `run-playwright.sh:8`) runs 2 of the repo's 4 billing tests. Ownership routing in `OWNERSHIP.md` (`Slack: #practice-billing-team`, `Jira: BILL`) does not reach the other 2. | S | **P1** |
| G7 | `download-invoice-pdf-button` is asserted visible+enabled but never clicked; the invoice PDF is never generated or validated. `OWNERSHIP.md` lists "invoice PDF" as an owned surface. | L5 | `billing-settings-page.spec.ts:250-251`; `billing-user-flow.spec.ts:320-321` | An invoice PDF that renders blank or 500s is invisible to this suite. | S | **P2** |
| G8 | Pricing-tab assertions stop at `free-products-card` + `pricing-contact-us`. `marketplace-card` (the *paid* product section) is deliberately unasserted, with an in-code note calling it a suspected product bug on enterprise practices. | L5 | `billing-user-flow.spec.ts:405-411`; `billing-settings-page.spec.ts:331-339` | A known-suspicious product behavior is being worked around in the test rather than filed. Needs a product decision, then either an assertion or a documented exclusion. | S | **P2** |
| G9 | `cleanupBillingState` restores the default payment method to *row 0*, not to the method that was actually default before the test. | L5 | `billing.ts:306-316`; `billing-settings-page.spec.ts:208-218` | Silently leaves the shared production practice with a different default payment method than it started with. That is the method a real charge would hit. | S | **P2** |
| G10 | No test asserts that a payment method is ever actually **charged**, nor that a monthly limit or rollover order is honored at charge time. Coverage stops at "the UI persisted the setting". `OWNERSHIP.md` scope includes "billing zocrons" and "AAA (pricing/booking processor)". | L4 / L3 (not L5) | none exist | The settings tested here exist only to control real charges. The charge-side behavior they configure is entirely untested at any level in this repo. Belongs in a backend contract/integration suite, not in browser E2E. | L | **P1** |
| G11 | `billing-user-flow.spec.ts` mixes an appointment-report RBAC test with the billing-settings suite in one file under `Account-User-Setup/`. | L5 | `billing-user-flow.spec.ts:32-85` vs `:87-451` | Can't run billing selectively; ownership of the file is ambiguous between two teams' `OWNERSHIP.md`. | S | **P2** |
| G12 | The `dac52b65` Stripe-Payment-Element repair is unmerged, so billing E2E is red on `main`, and `support/billing.ts` carries further uncommitted edits on top. | L5 | `playwright/support/billing.ts` | Until merged there is effectively **zero** working billing E2E on `main`. Merge and confirm green. | S | **P0** |

---

## Level Summary

| Level | Label | Billing test count (sandbox) | Files | Notes |
|---|---|---|---|---|
| L1 | `unit` | 0 | — | No unit tests in this repo by design. |
| L2 | `component` | 0 | — | — |
| L3 | `integration` | 0 | — | — |
| L4 | `api` | 0 | — | `loginByAPI` (`support/auth.ts:108`) and `spend-management.ts` make HTTP calls, but as setup, not as asserted contracts. The one status assertion in scope (`billing-user-flow.spec.ts:71`, `GetAppointmentReport` = 200) is inside an L5 browser test and is not billing. |
| L5 | `e2e` | **4** | 2 | `billing-settings-page.spec.ts` (2), `billing-user-flow.spec.ts` (2 of its 3). |
| — | **Total billing tests** | **4** | **2** | Of which ~2 are duplicates of the other 2 (see Internal duplication). Effective distinct billing journeys: **2**. |

Supporting counts:

| Metric | Exact value | Evidence |
|---|---|---|
| Billing spec files | 2 | file list above |
| `test()` blocks in those files | 5 | `grep -c` per file: 2 + 3 |
| Billing-specific `test()` blocks | 4 | 1 of the 3 in `billing-user-flow.spec.ts` is appointment-report |
| Distinct non-duplicated billing journeys | 2 | "manage billing settings" + "add/remove a credit card" |
| `test.step()` blocks | 48 (24 per file) | `grep -c 'test.step('` |
| Exported helpers in `support/billing.ts` | 10 | see `support-helpers.md` |
| Test accounts used | 3 (`<test-account-email>`, `<test-account-email-2>`, `<teammate-test-account-email>`) | `:27`; `:37`; `:30` |
| Files in `Provider-Billing/` | 3 tracked (`OWNERSHIP.md`, `Pages/.gitkeep`, `Pages/billing-settings-page.spec.ts`) | `git ls-files` |
| `Flows/` dirs under `Provider-Billing/` | 0 | `ls` → no such directory |
