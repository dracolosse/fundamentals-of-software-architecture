# Fintech System — Architecture Project

## Brief

Design and evolve the architecture for a **payment processing and compliance system** throughout the 30-week program.

## Domain

A financial technology platform handling payments, regulatory compliance, and financial reporting. Key concerns:
- **Reliability:** Zero-downtime, exactly-once processing
- **Compliance:** PCI-DSS, KYC/AML, audit trails
- **Security:** Encryption at rest/transit, access control, fraud detection
- **Data consistency:** ACID transactions, event sourcing for audit

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
