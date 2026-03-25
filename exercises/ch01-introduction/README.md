# Chapter 1: Introduction — Exercise

## "Define Your Architecture"

Apply Chapter 1's four dimensions of architecture to both projects.

## Deliverables

For **each** project (SaaS Platform + Fintech System):

### 1. Architecture Definition Document (30pts)
Cover all 4 dimensions:
- **Architecture style** — initial thoughts (monolith? microservices? modular monolith? etc.)
- **Architecture characteristics** — which "-ilities" matter most and why
- **Logical components** — initial high-level breakdown
- **Architecture decisions** — initial constraints and rules

### 2. ADR-001: "Why we chose [initial style]" (25pts)
Write an Architecture Decision Record:
- **Context** — what problem/situation drives the decision
- **Decision** — what you chose
- **Trade-offs** — what you gain vs. sacrifice
- **Consequences** — what changes because of this

### 3. Self-Assessment (20pts)
Rate yourself 1-5 on each architect expectation:
1. Make Architecture Decisions
2. Continually Analyze the Architecture
3. Keep Current with Latest Trends
4. Ensure Compliance with Decisions
5. Understand Diverse Technologies
6. Know the Business Domain
7. Possess Interpersonal Skills
8. Understand and Navigate Politics

Include a brief improvement plan for your 3 lowest-scored areas.

### 4. C4 Level 1 — Context Diagram (25pts)
Draw a Context diagram for each project showing:
- Your system (center box)
- External users/actors
- External systems it interacts with
- Relationships and data flows

## File Structure

```
exercises/ch01-introduction/
  saas-platform/
    architecture-definition.md
    adr-001-initial-style.md
    context-diagram.md          (Mermaid or ASCII)
  fintech-system/
    architecture-definition.md
    adr-001-initial-style.md
    context-diagram.md          (Mermaid or ASCII)
  self-assessment.md            (shared — covers both projects)
```

## Rubric

| Criteria | Points |
|----------|--------|
| Architecture definition completeness (4 dimensions, both projects) | 30 |
| ADR quality (trade-offs, context, consequences) | 25 |
| Self-assessment honesty + improvement plan | 20 |
| Diagram clarity | 25 |
| **Total** | **100** |

## Tips
- There are no wrong answers at this stage — it's about thinking through the dimensions
- Be honest in your self-assessment; this is your baseline
- For the C4 Context diagram, focus on boundaries — what's inside vs. outside your system
- Reference the Laws of Software Architecture: "Everything is a trade-off"

## Grade

> Grade will be added after peer-review evaluation.
