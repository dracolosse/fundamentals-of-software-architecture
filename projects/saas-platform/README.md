# SaaS Platform — Architecture Project

## Brief

Design and evolve the architecture for a **multi-tenant SaaS application** throughout the 30-week program.

## Domain

A B2B SaaS platform providing project management and collaboration tools. Key concerns:
- **Multi-tenancy:** Data isolation, tenant-specific configuration
- **Scalability:** Handle growing number of tenants and users
- **API design:** RESTful APIs, webhooks, integrations
- **Billing:** Subscription tiers, usage-based pricing

## Evolution Path

| Chapters | Focus |
|----------|-------|
| Ch 1-4 | Define requirements, identify architectural characteristics |
| Ch 5-8 | Component design, modularity analysis, fitness functions |
| Ch 9-14 | Compare monolith vs service-based, ADR for chosen style |
| Ch 15-18 | Add event-driven features, evaluate microservices migration |
| Ch 19 | Final architecture style justification |
| Ch 20-27 | Patterns, risk analysis, team topology, complete documentation |

## Directories

- `adrs/` — Architecture Decision Records
- `diagrams/` — C4, component, sequence diagrams
- `docs/` — Architecture docs, trade-off analyses
- `src/` — Code implementations (when applicable)
