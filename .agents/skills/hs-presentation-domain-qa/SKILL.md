---
name: hs-presentation-domain-qa
description: Review Vital Margin visual, audio, GUI, and asset work for information-boundary, causality, accessibility, provenance, and replay risks.
---

# HS Presentation Domain QA

## When to Use

- Use this skill after project-specific visual, audio, GUI, animation, or asset
  work is produced and before treating the slice as ready.
- Use it for presentation-only changes and alongside `hs-policy-domain-qa` when
  simulation mechanisms, domain claims, or educational scoring also change.
- Do not use it as a substitute for generic code review, browser testing,
  design critique, legal advice, or lived accessibility evaluation.

## Required Inputs

- Original request and `_workspace/00_input/request-summary.md`.
- Produced artifact or changed files.
- `_workspace/02_presentation_contract.md` when the work is substantial.
- Relevant host projections, history/replay contracts, asset registries,
  credits, policies, and verification output.
- Canonical docs, the visual/audio roadmap, and the harness team spec.

## Workflow

1. Compare the result with the request, explicit authorization, presentation
   contract, and named roadmap milestone. Flag unrequested milestone promotion
   and run the documented automated evidence set.
2. Trace every meaningful visual, motion, and audio signal to actor-visible host
   data or committed history. Check observation timing, missingness, and safe
   unknown fallbacks; reject client-inferred severity, intent, or outcomes.
3. Verify that causal presentation distinguishes committed effects from local
   comparisons and does not rewrite immutable history or imply unsupported
   causality.
4. Check project-specific accessibility equivalence: meaning remains available
   without color, motion, or audio; reduced-motion, mute, scaling, keyboard, and
   recovery paths retain the complete decision-relevant content.
5. Audit new assets for stable IDs, registry coverage, source/generation method,
   license basis, hashes, modifications, attribution, approval, safe SVG or
   metadata handling, and generic fallbacks. Flag imitation of proprietary games
   or unintended resemblance to real institutions or people.
6. Confirm presentation state never enters commands, transition evaluation,
   stochastic inputs, state hashes, or authoritative replay. Verify graceful
   behavior when data, assets, audio, or browser capabilities are unavailable.
7. Return `pass`, `fix`, or `redo`. A `pass` must still state evidence limits.
   Agents may revise and re-run the checks; optional human or legal feedback is
   recorded as a limit or follow-up, not a technical stop gate.

## Outputs

Write `_workspace/03_presentation_qa.md` with these sections:

- `Status`
- `Reviewed Inputs and Authorization`
- `Information and Causality Findings`
- `Accessibility and Fallback Findings`
- `Provenance and Rights Findings`
- `Authority and Replay Findings`
- `Required Fixes`
- `Residual Risks and Evidence Limits`
- `Verification Evidence`

## Validation

- Findings cite file paths, registry IDs, tests, or contract sections.
- Review separates blocking defects from human-evaluation or legal-review gaps.
- Generic implementation findings are handed to the appropriate global skill
  instead of being duplicated here.
- Approval means only that the bounded project contract passed; it does not
  establish usability, learning, calibration, balance, or policy validity.
- Asset uncertainty fails closed to exclusion and a registered generic fallback;
  no reviewer is asked to guess provenance, identity, resemblance, or rights.

## References

- `docs/visual_audio_enhancement_roadmap.md`
- `docs/design_principles.md`
- `ARCHITECTURE.md`
- `docs/harness/vital-margin/team-spec.md`
- `LESSONS.md`
