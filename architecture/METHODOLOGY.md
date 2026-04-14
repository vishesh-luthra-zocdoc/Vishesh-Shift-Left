# Methodology

## Approach

This analysis was produced using a multi-agent pattern: independent agents running in parallel to scan different aspects of the codebase, followed by a synthesis phase to cross-reference findings and identify gaps.

## Why Multi-Agent?

The billing domain spans 70+ source files, 25+ test files, and 3 Cypress spec files across multiple directories. A single sequential scan would be slow and risk missing cross-cutting concerns (e.g., an API endpoint defined in `routes.ts`, implemented in `apiCalls.ts`, tested in `apiCalls-tests.ts`, AND intercepted in Cypress commands). Parallel agents each build a complete picture of their domain, then findings are cross-referenced.

## Tools Used

- **Claude Code** — AI-assisted code exploration and analysis
- **Glob/Grep** — File pattern matching and content search across the monorepo
- **Git** — Version control and commit history analysis
- **tmux** — Terminal multiplexing for parallel agent execution

## Analysis Phases

See [AGENT-TEAM-OPERATIONS-LOG.md](AGENT-TEAM-OPERATIONS-LOG.md) for detailed phase breakdown and timing.

## Scope

- **In scope:** All billing-related code in `provider-fe-monorepo`, specifically:
  - `apps/settings/src/pages/settingsPages/billingSettings/` (main billing area)
  - `apps/settings/cypress/e2e/PracticeSettingsPages/billing-*` and `invoice-*` (Cypress tests)
  - `apps/settings/src/config/routes.ts` (billing endpoint definitions)
  - `apps/settings/src/types/practiceBillingSettingsTypes.ts` (type definitions)
  - `apps/settings/src/server/controllers/practiceBillingSettingsPage/` (server mocks)
  - `apps/provider-home-webapp/src/` (SKU-related billing code)
- **Out of scope:** Backend billing services, billing monolith, Stripe dashboard configuration
