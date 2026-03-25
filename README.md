# Fundamentals of Software Architecture — Learning Program

A structured 30-week learning program based on **"Fundamentals of Software Architecture"** (2nd Edition, 2025) by Mark Richards & Neal Ford.

## Program Structure

| Part | Chapters | Duration | Exam |
|------|----------|----------|------|
| **I. Foundations** | Ch 1-8: Thinking, Modularity, Characteristics, Components | Weeks 1-8 | Exam 1 (Week 9) |
| **II. Architecture Styles** | Ch 9-19: Layered, Monolith, Pipeline, Microkernel, Service-Based, Event-Driven, Space-Based, SOA, Microservices | Weeks 10-20 | Exam 2 (Week 21) |
| **III. Techniques & Soft Skills** | Ch 20-27: Patterns, ADRs, Risk, Diagramming, Teams, Leadership, Intersections | Weeks 22-29 | Exam 3 Final (Week 30) |

## Weekly Format

- **Session 1 (Theory):** Read chapter, concept quiz, spaced repetition review
- **Session 2 (Practice):** Exercise implementation, peer-review simulation, journal entry

## Grading

| Grade | Score | Description |
|-------|-------|-------------|
| A | 90-100 | Excellent — SA-cert ready |
| B | 80-89 | Good — solid understanding |
| C | 70-79 | Adequate — needs reinforcement |
| D | 60-69 | Below expectations — revisit |
| F | <60 | Fail — must redo |

**GPA:** Exercises (40%) + Exams (40%) + Journal & Katas (20%)

## Repository Structure

```
projects/          Two evolving architecture projects (SaaS + Fintech)
exercises/         Chapter exercises with briefs, solutions, grades
katas/             Architecture kata sessions
exams/             Three exams (Foundations, Styles, Final)
journal/           Weekly architect's journal
spaced-repetition/ Review quiz history
tools/             sa-learn CLI for Notion progress tracking
```

## Projects

### SaaS Platform
Multi-tenant SaaS application — evolves through each chapter applying new architectural concepts. Focus: scalability, multi-tenancy, API design.

### Fintech System
Payment processing and compliance system — parallel evolution with different trade-offs. Focus: reliability, compliance, security, data consistency.

## Progress

> Progress tracked via `sa-learn progress` CLI command and Notion dashboard.

## Setup

```bash
# Install CLI dependencies
cd tools && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Configure Notion token
cp .env.example .env  # Add your NOTION_TOKEN

# Setup Notion workspace
./tools/sa-learn.sh setup

# Shell alias (add to .zshrc)
alias sa-learn="/path/to/fundamentals-of-software-architecture/tools/sa-learn.sh"
```
