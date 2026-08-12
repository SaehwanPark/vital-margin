---
name: hs-policy-evidence-mapper
description: Map health-policy simulation research, precedents, and assumptions into project-specific mechanisms and unresolved questions.
---

# HS Policy Evidence Mapper

## When to Use

- Use this skill when a request asks for research synthesis, precedent review,
  evidence-to-design implications, assumptions, or mechanism justification for
  this game.
- Use it before designing mechanics that depend on health policy, institutions,
  economics, political process, labor, payer-provider behavior, education, or
  validation claims.
- Do not use it for generic literature review outside this project or for
  implementation-only tasks that already have a settled spec.

## Required Inputs

- User request and `_workspace/00_input/request-summary.md` when available.
- Canonical docs in `README.md` and `docs/`.
- Source material supplied by the user or gathered for the task.
- The current roadmap phase and intended downstream artifact.

## Workflow

1. Identify the mechanism, institution, actor, or educational claim being
   supported.
2. Separate source-backed claims from design abstractions, tuning choices, and
   unresolved empirical or normative questions.
3. Record actor incentives, authority, information, constraints, outside
   options, and likely strategic responses.
4. Flag risks from false precision, normative bias, unbounded scope, or
   unsupported forecasting.
5. Translate findings into actionable design implications for the next phase.

## Outputs

Write `_workspace/01_evidence_map.md` with these sections:

- `Scope`
- `Sources Reviewed`
- `Mechanisms and Institutions`
- `Actor Incentives and Information`
- `Assumptions`
- `Unresolved Questions`
- `Design Implications`
- `Risks`

## Validation

- Each major mechanism has a cited source, a project-doc basis, or an explicit
  label as a game abstraction.
- Evidence claims do not imply policy forecasting authority unless validation
  evidence exists.
- The output distinguishes actor utility, organizational success, social welfare,
  and educational evaluation.

## References

- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/vital-margin/team-spec.md`
