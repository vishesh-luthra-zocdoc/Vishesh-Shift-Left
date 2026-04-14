# Agent Topology

## Hierarchy

```
Orchestrator (Main Agent)
├── Phase 1: Discovery (4 agents, parallel)
│   ├── Agent 1: Source File Discovery
│   ├── Agent 2: Unit Test Cataloging
│   ├── Agent 3: Cypress E2E Cataloging
│   └── Agent 4: API Endpoint Mapping
└── Phase 2: Synthesis (Orchestrator)
    ├── Cross-reference source ↔ tests
    ├── Identify untested components
    ├── Flag obsolete/redundant tests
    └── Produce final reports
```

## Agent Responsibilities

### Agent 1: Source File Discovery
- **Input:** Monorepo root
- **Search patterns:** `billing`, `invoice`, `payment`, `bill`, `pricing`, `sku`, `credit`, `ach`, `stripe`
- **Output:** Complete inventory of 70 source files with file type, business logic classification, feature flags, and API endpoint references
- **Scope:** All `apps/` and `shared/` directories

### Agent 2: Unit Test Cataloging
- **Input:** Monorepo test directories (`__tests__/`)
- **Output:** 25 test files, ~265+ test cases with exact `describe`/`it` block names, mock inventory, and coverage classification
- **Depth:** Read every test file fully, categorize each test (validation, rendering, API, business logic)

### Agent 3: Cypress E2E Cataloging
- **Input:** `apps/settings/cypress/`
- **Output:** 3 spec files, 31 test cases, custom commands, page objects, selectors, fixtures
- **Depth:** Full spec reading, intercept mapping, experiment configuration extraction

### Agent 4: API Endpoint Mapping
- **Input:** Route definitions, API client code, server handlers
- **Output:** 11 REST endpoints with URL patterns, HTTP methods, source locations, test coverage mapping (unit + Cypress intercepts)
- **Depth:** Traced each endpoint from route definition → client function → server handler → test coverage

## Cross-Reference Matrix

The synthesis phase cross-references all 4 agent outputs to answer:
1. Which source files have unit tests? (Agent 1 × Agent 2)
2. Which source files have Cypress tests? (Agent 1 × Agent 3)
3. Which API endpoints are tested in both unit and E2E? (Agent 4 × Agent 2 × Agent 3)
4. Which components have zero test coverage? (Agent 1 - Agent 2 - Agent 3)
