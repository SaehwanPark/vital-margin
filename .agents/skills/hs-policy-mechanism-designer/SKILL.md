---
name: hs-policy-mechanism-designer
description: Design project-specific actors, strategic interactions, observations, scenarios, and debrief hooks for the health-policy strategy game.
---

# HS Policy Mechanism Designer

## When to Use

- Use this skill when designing a simulation mechanism, actor framework,
  strategic interaction, policy lifecycle, scenario, vertical slice, or
  educational debrief artifact for this repository.
- Use it after evidence mapping when the mechanism depends on contested
  health-policy or institutional assumptions.
- Do not use it for generic Rust architecture, generic CLI design, or broad
  framework building disconnected from a concrete slice.

## Required Inputs

- User request and current roadmap phase.
- `_workspace/01_evidence_map.md` when evidence or assumptions are involved.
- Canonical docs and the harness team spec.
- Any existing mechanism, scenario, or code files that the request touches.

## Workflow

1. Define the smallest useful slice: actors, setting, turn length, player role,
   included mechanisms, and explicit exclusions.
2. Specify true state, actor beliefs, observations, reported measures, and any
   delays, bias, missingness, or revisions.
3. Define commands, validation failures, legitimate unfavorable outcomes, events,
   attributed effects, and next-state updates.
4. For each strategic interaction, record participants, feasible actions,
   private information, outside options, payoff categories, decision procedure,
   and rationale output.
5. Add educational hooks: decision log, causal explanation, counterfactual or
   sensitivity prompt, and debrief questions.
6. Check whether the design supports deterministic replay by moving randomness
   and measurement noise into explicit resolved inputs.

## Outputs

Write `_workspace/02_mechanism_design.md` with these sections:

- `Goal and Roadmap Phase`
- `Slice Boundary`
- `Actors and Authority`
- `State, Beliefs, and Observations`
- `Commands, Events, and Effects`
- `Strategic Interaction`
- `Assumptions and Parameters`
- `Educational Debrief Hooks`
- `Determinism and Replay Notes`
- `Open Questions`

## Validation

- The design can be tested in a narrow vertical slice.
- It does not require solving a global equilibrium or modeling the whole US
  healthcare system.
- It distinguishes invalid operations from modeled outcomes such as failed
  negotiations, strikes, or political opposition.
- It preserves multiple defensible strategies rather than encoding one hidden
  optimal path.

## References

- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/vital-margin/team-spec.md`
