---
name: spec-kit
description: Apply GitHub Spec Kit's pinned specification-driven workflow to define principles, requirements, plans, tasks, implementation, and convergence checks. Use when starting or restructuring non-trivial product or software work that benefits from traceable specs before code.
---

# GitHub Spec Kit

Use the pinned `v0.16.4` source at `full-sources/tools/spec-kit` and the user-local `specify` CLI installed by this repository.

## Setup

```bash
bash scripts/setup_tools.sh spec-kit
specify --version
```

Initialize only after reading the target repository and selecting the correct integration:

```bash
specify check
specify init --here --integration <integration>
```

Review the command's planned writes and preserve existing project instructions. Never overwrite an established constitution, requirements set, or Agent configuration blindly.

## Core workflow

1. **Constitution** — record durable quality, security, testing, UX, and governance principles.
2. **Specify** — define user outcomes, scope, constraints, acceptance criteria, edge cases, and exclusions; avoid prematurely hard-coding implementation choices.
3. **Clarify** — resolve consequential ambiguity with stakeholders rather than inventing facts.
4. **Plan** — choose architecture and technology from repository evidence and constraints.
5. **Tasks** — produce ordered, testable work units with dependencies and parallel-safe boundaries.
6. **Implement** — execute tasks while preserving traceability to the spec and plan.
7. **Converge/verify** — compare code, tests, docs, and behavior to the authoritative artifacts; append remaining gaps instead of declaring completion by intuition.

Depending on the integration, commands appear as `/speckit.*` or `$speckit-*`. Use the syntax generated for the current Agent rather than assuming one host.

## Required evidence

At handoff, identify the constitution/spec/plan/tasks used, the requirements implemented, verification commands and results, deviations approved, and unresolved gaps. Specs guide implementation but never override higher-priority user instructions or observed repository facts.
