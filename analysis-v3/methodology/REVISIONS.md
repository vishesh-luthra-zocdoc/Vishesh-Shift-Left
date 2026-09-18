# Snapshot Revisions

Snapshots are content exports and carry no git metadata. This file is the authoritative record.

| Snapshot dir | Repo | Revision | Ref | Date |
|---|---|---|---|---|
| `provider-fe-monorepo/` | Zocdoc/provider-fe-monorepo | `dd9e4952a6` | `origin/main` | 2026-09-03 |
| `provider-billing/` | Zocdoc/provider-billing | `84318e3d5c` | `main` (GitHub API) | 2026-09-03 |
| `zocdoc_web/` | Zocdoc/zocdoc_web | `8742b5072da` | `master` (GitHub API) | 2026-09-04 |

The QA-owned `sandbox` repo is out of scope for this analysis. Where its 2026-09-02 breakage is cited
as evidence for X-001, the reference revisions are `dac52b65` (branch
`fix/billing-stripe-payment-element`) and `origin/main` at `4bb607cc`, both 2026-09-04.

## Why snapshots, not the local checkouts

The local checkouts were badly stale and the agentic sandbox denies writes to their `.git` dirs, so
`git fetch` fails. Analyzing them would have produced findings about deleted code:

| Repo | Local checkout | Current remote | Drift |
|---|---|---|---|
| provider-fe-monorepo | 550 commits behind | `dd9e4952a6` | ~7 weeks |
| zocdoc_web | `580b2defeb6` (Jun 16) | `8742b5072da` (Sep 4) | ~11 weeks |
| provider-billing | `77a08ce` (Jun 15) | `84318e3d5c` (Sep 3) | ~11 weeks |

`provider-fe-monorepo` was exported with `git archive` from a locally-present fresh `origin/main`
ref. `zocdoc_web` and `provider-billing` were fetched via the GitHub REST API (`gh api`), which
needs no local write access — this is what unblocked them.

**The staleness mattered.** `provider-billing`'s test projects were renamed and restructured
between June and September (`ProviderBilling.*Tests` → `UnitTests`/`IntegrationTests`/`ApiTests`,
plus new `SmokeTests` and `BillingExportCron.UnitTests`). An analysis of the June checkout would
have described test projects that no longer exist.
