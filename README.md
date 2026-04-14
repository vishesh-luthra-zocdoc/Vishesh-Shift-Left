# Shift-Left Test Analysis

**Owner:** Vishesh Luthra (Provider Billing Team)
**Generated:** 2026-04-14
**Scope:** Billing domain across `provider-fe-monorepo` + `zocdoc_web` monolith

## What This Is

A comprehensive test coverage gap analysis for billing-related features across two repos:
- **provider-fe-monorepo** — Frontend unit tests (Jest) and Cypress E2E tests
- **zocdoc_web** — Backend Selenium integration tests (bill generation, payments, Stripe, chargebacks, churn)

The goal is to identify missing tests, outdated tests, and shift-left opportunities — moving test coverage from slow E2E/Selenium tests to faster unit tests where possible.

## Repository Structure

```
├── architecture/                     # How this analysis was produced
│   ├── AGENT-TEAM-OPERATIONS-LOG.md  # Agent deployment phases & timing
│   ├── METHODOLOGY.md               # Approach and tools used
│   └── AGENT-TOPOLOGY.md            # Agent hierarchy and responsibilities
├── analysis/
│   └── billing/
│       ├── SUMMARY.md               # START HERE — executive summary
│       ├── inventory/               # Current state mapping
│       │   ├── MASTER-INVENTORY.md  # Test count breakdown
│       │   ├── DETAILED-TEST-CATALOG.md  # Every test with purpose
│       │   ├── components.md        # Component-to-test map
│       │   ├── cypress-e2e-tests.md # Cypress spec catalog
│       │   ├── api-endpoint-coverage.md  # REST endpoint coverage
│       │   └── selenium-tests.md   # Monolith Selenium tests (zocdoc_web)
│       └── gaps/                    # Findings & action items
│           ├── GAPS.md              # Missing test coverage (P0-P3)
│           ├── OBSOLETE.md          # Dead/outdated tests
│           └── feature-flag-audit.md # Experiment cleanup candidates
```

## How to Read

1. Start with **[analysis/billing/SUMMARY.md](analysis/billing/SUMMARY.md)** for the executive overview
2. Dive into **inventory/** for detailed maps of what exists
3. Review **gaps/** for prioritized action items
4. See **architecture/** to understand how the analysis was produced

## Key Stats

| Metric | Count |
|--------|-------|
| Source components analyzed | 70 |
| Unit test files | 25 |
| Unit test cases | ~265+ |
| Cypress E2E spec files | 3 |
| Cypress E2E test cases | 31 |
| REST API endpoints | 11 |
| Components with NO tests | 12 |
| P0 gaps identified | 2 |
| P1 gaps identified | 4 |
| Selenium tests (zocdoc_web) | 76 |
| Selenium tests to keep | 38 |
| Selenium tests to remove | 38 |
| Lines of potentially obsolete tests | ~1,200+ |
