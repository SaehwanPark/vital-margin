---
name: hs-policy-domain-qa
description: Review Vital Margin artifacts for project-specific simulation, policy, education, scope, and determinism risks.
---

# Health-Policy Domain QA

## When to Use

- Use this skill to review mechanism ledgers, scenario specs, policy claims,
  and educational debrief logic against domain evidence and project guardrails.
- Use it to protect determinism, explicit stochastic inputs, and partial
  observability.
- Do not use it for generic Rust style or release bookkeeping. Use global skills
  for those.

## Required Inputs

- Draft artifact or code under review.
- Canonical docs and `docs/harness/vital-margin/team-spec.md`.
- Verification output when code changed.

## Workflow

1. Compare the artifact to the original request and roadmap phase.
2. Check project-specific risks:
   scope expansion, false precision, normative opacity, strategic opacity,
   educational opacity, premature frameworking, and replay instability.
3. Verify that state, beliefs, observations, actor utility, social welfare, and
   educational evaluation remain distinct where relevant.
4. Check deterministic boundaries: no hidden randomness, wall-clock dependency,
   global mutable state, or unresolved stochastic behavior inside core
   transitions.
5. Return one status:
   `pass` when the artifact is ready, `fix` when targeted revision is enough, or
   `redo` when the direction conflicts with the project.

## Outputs

Write `_workspace/03_domain_qa.md` with these sections:

- `Status`
- `Reviewed Inputs`
- `Findings`
- `Required Fixes`
- `Residual Risks`
- `Verification Evidence`

## Validation

- Findings cite file paths or handoff sections.
- QA does not repeat generic code review that belongs to global skills.
- A `pass` still records residual uncertainty when evidence, calibration, or
  educational validation is incomplete.

## References

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/vital-margin/team-spec.md`
