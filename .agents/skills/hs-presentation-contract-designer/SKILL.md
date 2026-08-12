---
name: hs-presentation-contract-designer
description: Define actor-visible visual, audio, asset, and consequence-presentation contracts for Vital Margin before implementation.
---

# HS Presentation Contract Designer

## When to Use

- Use this skill for project-specific GUI, regional-board, institutional
  identity, facility, report, animation, audio-cue, or asset-system work.
- Use it when presentation must preserve actor-visible information, causal
  legibility, deterministic replay boundaries, accessibility equivalents, and
  asset provenance.
- Do not use it to authorize a roadmap milestone, generate assets, implement
  generic UI code, or replace a general UX/accessibility skill.

## Required Inputs

- Original request and explicit scope authorization.
- `docs/visual_audio_enhancement_roadmap.md` and the current project state.
- Relevant host projection, observation, history, and browser presentation
  contracts.
- Existing asset registries, credits, policies, and tests when assets or audio
  are in scope.
- `_workspace/00_input/request-summary.md` for substantial work.

## Workflow

1. Confirm the named roadmap milestone or bounded presentation outcome. Treat
   roadmap text as guidance, not permission to start unrequested work.
2. State the player question the presentation should answer and the strategic,
   institutional, or causal relationship it should make easier to perceive.
3. Create a source ledger for every semantic element: host field or committed
   history source, observation timing, missing/unknown state, and prohibited
   client inference. Never derive severity, intent, or future outcomes locally.
4. Define the visual, motion, and audio vocabulary. Give each meaningful signal
   a stable semantic role and require text, symbol, or visible-state equivalents
   so color, motion, and sound are never the sole channel.
5. Specify fallbacks for missing data, missing assets, muted or unsupported
   audio, reduced motion, text scaling, and interrupted loading.
6. Record authority and replay boundaries: browser state remains reversible and
   presentation-only; commands, outcomes, history, hashes, and replay remain
   host-owned unless a separately approved architecture change says otherwise.
7. Define provenance and release requirements for each new or modified asset,
   including source/generation metadata, license basis, hashes, modifications,
   attribution, and approval state.
8. Name focused contract tests, optional external feedback, and evidence limits.
   Automated checks are the technical progression mechanism; do not equate them
   with human usability, lived accessibility, learning, calibration, or policy
   validity.

## Outputs

Write `_workspace/02_presentation_contract.md` with these sections:

- `Goal and Authorization`
- `Player Questions and Consequences`
- `Actor-Visible Source Ledger`
- `Visual, Motion, and Audio Semantics`
- `Accessibility and Fallbacks`
- `Authority, History, and Replay Boundaries`
- `Asset Provenance and Release Requirements`
- `Verification and Evidence Limits`
- `Non-Goals and Open Questions`

## Validation

- Every semantic presentation element has an actor-visible source or is labeled
  decorative and non-informational.
- Unknown, delayed, and unavailable information have explicit representations.
- No visual or audio cue leaks private intent, true-state deterioration, or a
  future outcome.
- Meaning survives mute, missing assets, reduced motion, and non-color use.
- The contract does not copy or closely imitate proprietary game assets.
- The requested slice can be implemented without creating a second simulation
  or legality engine in the browser.
- The contract has agent-executable entry/exit criteria and no required human
  participant, approval, or review stop gate.

## References

- `docs/visual_audio_enhancement_roadmap.md`
- `docs/design_principles.md`
- `ARCHITECTURE.md`
- `docs/harness/vital-margin/team-spec.md`
- `LESSONS.md`
