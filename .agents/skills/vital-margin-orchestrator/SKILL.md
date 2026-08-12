---
name: vital-margin-orchestrator
description: Route Vital Margin work through repo-specific research, simulation design, presentation contracts, implementation, and domain-QA handoffs without duplicating global skills.
---

# Vital Margin Orchestrator

## When to Use

- Use this skill for substantial work in this repository that touches research,
  conceptual design, scenario design, simulation mechanics, educational
  debriefing, or deterministic replay boundaries.
- Use it when a request should follow the roadmap phases or preserve `_workspace/`
  handoff artifacts.
- Use it for substantial visual/audio roadmap work that must preserve
  actor-visible presentation and asset-governance boundaries.
- Do not use it for generic Rust formatting, generic code review, release
  preparation, or branch management. Use global skills for those.

## Required Inputs

- User request.
- Current repository state.
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.
- Team spec: `docs/harness/vital-margin/team-spec.md`.
- `docs/visual_audio_enhancement_roadmap.md` when presentation is in scope.

## Workflow

1. Read the canonical docs before shaping project-specific work.
2. Classify the request by roadmap phase, track, and output type. Use the
   simulation track for mechanisms and scenarios, and the presentation track
   for GUI, visual, audio, animation, or asset work:
   research, conceptual model, game design, technical prototype, vertical slice,
   validation, release, or post-release expansion.
3. Write `_workspace/00_input/request-summary.md` for substantial tasks. Include
   scope, non-goals, sources, expected files, validation target, and whether
   generic global skills are needed.
4. Route only to the repo-local specialists needed by the track:
   - simulation/domain: `hs-policy-evidence-mapper`,
     `hs-policy-mechanism-designer`, and `hs-policy-domain-qa`;
   - presentation: `hs-presentation-contract-designer` before substantial
     production and `hs-presentation-domain-qa` after production.
   Use both QA skills only when a presentation change also alters simulation
   mechanisms, domain claims, or educational scoring.
5. For generic implementation quality, use global skills rather than creating
   local duplicates.
6. Treat roadmap items as sequencing guidance, not authorization. Do not
   promote or implement a milestone beyond the user's bounded request. Advance
   bounded technical slices from automated evidence; participant studies,
   approvals, and human review are optional external feedback, never routine
   stop gates.
7. Preserve handoff files named in the team spec when the task spans more than
   one phase.
8. Finish with a concise handoff that lists changed files, verification, known
   limits, and next phase dependencies.

## Outputs

- `_workspace/00_input/request-summary.md` for substantial scoped work.
- `_workspace/final/handoff.md` when a durable handoff is useful.
- Updated repository files requested by the user.

## Validation

- Local skill names must not duplicate global skill names.
- The task must not silently skip canonical docs when project-specific judgment
  is required.
- Any broad feature request must be narrowed to the current roadmap phase unless
  the user explicitly asks for future-facing design.
- Presentation work must trace semantic output to actor-visible sources and
  preserve mute, reduced-motion, missing-asset, and unknown-data fallbacks.
- Presentation progression must record agent-executable entry/exit criteria,
  evidence artifacts, and claim limits. Uncertain assets fail closed to a
  registered generic fallback.
- Code-producing tasks must run focused verification such as `cargo fmt` and
  `cargo test` when Rust files are changed.

## References

- `docs/harness/vital-margin/team-spec.md`
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
