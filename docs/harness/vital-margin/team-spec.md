# Vital Margin Agent Harness

## Domain Summary

This project is a playable Rust strategy simulation with a reference CLI,
bounded MCP adapter, and active host-backed loopback GUI for all three
campaigns. AI-native validation is the default technical progression path. The
player leads a fictional nonprofit US health system
under financial, clinical, regulatory, political, labor, market, and
educational constraints.

The harness exists to keep agent work aligned with the canonical project docs:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`

Core project constraints:

- model strategic systems, not isolated decisions
- preserve meaningful tradeoffs and multiple defensible strategies
- keep actor utility distinct from social welfare and educational scoring
- make mechanisms, assumptions, observations, decisions, and causality inspectable
- keep the simulation core deterministic, with stochasticity resolved at explicit
  boundaries before transition evaluation
- distinguish true state, beliefs, observations, and reported measurements
- preserve immutable snapshots and append-only history
- build narrow vertical slices before general frameworks

## Non-Duplication Contract

This repo-local harness must not duplicate global agent skills. It only adds
project-specific routing, domain checks, and artifact contracts.

Use global skills for these generic responsibilities:

| Global capability | Do not create local duplicate for |
| --- | --- |
| `fp-developer` | functional-first implementation style, pure core logic, typed boundaries |
| `code-reviewer` | general bug, security, performance, and maintainability review |
| `code-commenter` | general commenting style and comment quality |
| `spec-driven-developer` | generic spec, architecture, and changelog synchronization workflow |
| `plan-designer` | generic implementation-plan shaping |
| `preferred-workflow` | branch, commit, PR, and review-loop workflow |
| `release-preparer` | public release packaging and publication readiness |
| `harness` | creating or revising this harness architecture |
| `end-user-xp-improver` | generic user workflow, usability, accessibility, and recovery design |

Repo-local skills are allowed only when the request depends on health-policy
simulation semantics, the roadmap phase gates, actor and mechanism modeling,
educational debriefing, deterministic replay, actor-visible presentation, or
project-specific visual/audio asset governance as defined by this project.

## Chosen Architecture

Pattern: Pipeline with an Expert Pool and producer/automated-evidence checkpoints.

Reason: the roadmap requires ordered work. Research and assumptions feed
conceptual design; conceptual design feeds game and educational design; those
feed the deterministic technical prototype; implementation is checked against
domain, reproducibility, and educational criteria. Technical checks are the
progression mechanism; human studies, approvals, and sign-offs are optional
external feedback rather than routine stop gates.

The orchestrator selects the simulation/domain track, presentation track, or
both. Each track has a producer and an explicit project-specific reviewer.
Parallel work is allowed only for bounded read-heavy or non-overlapping slices
that share the same input snapshot and write separate `_workspace/` artifacts
before synthesis.

## Roles

| Role | Responsibility | Reusable skill | Writes |
| --- | --- | --- | --- |
| Orchestrator | Route work through the phase pipeline and preserve handoffs | `.agents/skills/vital-margin-orchestrator/SKILL.md` | `_workspace/00_input/request-summary.md`, `_workspace/final/handoff.md` |
| Evidence Mapper | Convert research and precedent material into assumptions, mechanisms, and unresolved questions | `.agents/skills/hs-policy-evidence-mapper/SKILL.md` | `_workspace/01_evidence_map.md` |
| Mechanism Designer | Shape actor, policy, scenario, and causal mechanics for the first vertical slice | `.agents/skills/hs-policy-mechanism-designer/SKILL.md` | `_workspace/02_mechanism_design.md` |
| Domain QA Reviewer | Review proposed work against project-specific risks and phase gates | `.agents/skills/hs-policy-domain-qa/SKILL.md` | `_workspace/03_domain_qa.md` |
| Presentation Contract Designer | Define actor-visible visual, audio, consequence, fallback, and asset contracts | `.agents/skills/hs-presentation-contract-designer/SKILL.md` | `_workspace/02_presentation_contract.md` |
| Presentation Domain QA Reviewer | Review presentation work for information leaks, false causality, inaccessible meaning, provenance gaps, and replay-boundary drift | `.agents/skills/hs-presentation-domain-qa/SKILL.md` | `_workspace/03_presentation_qa.md` |

Generic implementation and code review are intentionally not local roles. When
Rust code is changed, use the relevant global skills alongside the local domain
QA checks. A local QA `pass` establishes only bounded technical conformance and
must state human-evidence and legal-review limits.

## Phase Order

### Phase 0: Request Framing

- Input sources: user request, README, canonical docs, current repository state.
- Actions: identify roadmap phase, scope, expected output, and whether code,
  documentation, research, or scenario design is in scope.
- Output files: `_workspace/00_input/request-summary.md`.
- Completion criteria: the task has an explicit phase, non-goals, and validation
  target.

### Phase 1: Evidence and Assumptions

- Input sources: canonical docs, cited literature or user-provided sources,
  existing assumptions and mechanism notes.
- Actions: map claims to mechanisms, actor incentives, evidence quality,
  uncertainty, and unresolved normative choices.
- Output files: `_workspace/01_evidence_map.md`.
- Completion criteria: assumptions are visible, contested points are not silently
  resolved, and every proposed mechanism has a source or is labeled abstraction.

### Phase 2: Mechanism and Scenario Design

- Input sources: request summary, evidence map, roadmap phase, design principles.
- Actions: define the smallest actor set, action vocabulary, state boundary,
  observation model, strategic interaction, causal effects, and debrief outputs.
- Output files: `_workspace/02_mechanism_design.md`.
- Completion criteria: design can be prototyped as a narrow slice and does not
  require a general framework before proving gameplay value.

### Phase 2P: Presentation Contract Design

- Trigger: GUI, visual, audio, animation, consequence-presentation, or asset
  work is explicitly in scope.
- Input sources: request summary, visual/audio roadmap, current host and browser
  contracts, relevant asset governance, and design principles.
- Actions: define player questions, actor-visible source ledger, semantic
  vocabulary, accessibility equivalents, fallbacks, authority/replay boundaries,
  provenance requirements, and evidence limits.
- Output files: `_workspace/02_presentation_contract.md`.
- Completion criteria: the slice can be produced without hidden-state leakage,
  local outcome inference, inaccessible meaning, or unregistered assets.

### Phase 3: Implementation or Document Production

- Input sources: mechanism design or presentation contract, plus existing docs,
  assets, browser files, or Rust code as applicable.
- Actions: produce the requested artifact. For code, use global implementation
  skills where relevant and keep I/O, randomness, persistence, and terminal
  rendering outside the deterministic transition core.
- Output files: requested repository files plus any phase-specific notes.
- Completion criteria: changes preserve the repo's boundaries and include
  focused verification.

### Phase 4: Domain QA

- Input sources: original request, canonical docs, produced artifacts, test
  output, and prior phase handoffs.
- Actions: check scope, deterministic replay assumptions, state/observation
  separation, actor utility versus welfare separation, assumption visibility,
  educational value, and first-slice fit.
- Output files: `_workspace/03_domain_qa.md`.
- Completion criteria: review returns `pass`, `fix`, or `redo` with evidence.

### Phase 4P: Presentation Domain QA

- Trigger: project-specific GUI, visual, audio, animation, or asset work was
  produced.
- Input sources: original request, presentation contract, produced artifacts,
  host projection/history contracts, registries, and verification output.
- Actions: trace visible and audible meaning to authorized actor-visible data;
  audit causality, accessibility equivalents, fallbacks, provenance, rights,
  browser authority, and replay isolation.
- Output files: `_workspace/03_presentation_qa.md`.
- Completion criteria: automated/agent review returns `pass`, `fix`, or `redo`
  with evidence and explicit human-evaluation and legal-review limits. Human
  evaluation is optional follow-up, not a promotion gate.

### Phase 5: Final Handoff

- Input sources: produced artifact, verification output, and the applicable
  domain or presentation QA result.
- Actions: summarize changed files, validation performed, known limitations, and
  next phase dependencies.
- Output files: `_workspace/final/handoff.md` when the task is substantial.
- Completion criteria: another contributor can continue without reconstructing
  the reasoning from chat history.

## Handoff Files

| From | To | File | Purpose |
| --- | --- | --- | --- |
| Orchestrator | Evidence Mapper | `_workspace/00_input/request-summary.md` | Defines phase, scope, sources, and non-goals |
| Evidence Mapper | Mechanism Designer | `_workspace/01_evidence_map.md` | Preserves assumptions, evidence, abstractions, and unresolved questions |
| Mechanism Designer | Implementer or Writer | `_workspace/02_mechanism_design.md` | Gives the smallest coherent design surface to build or document |
| Implementer or Writer | Domain QA Reviewer | Changed files and `_workspace/02_mechanism_design.md` | Lets QA compare output against intent and project principles |
| Domain QA Reviewer | Orchestrator | `_workspace/03_domain_qa.md` | Records pass/fix/redo status and project-specific risks |
| Presentation Contract Designer | Implementer, Writer, or Asset Producer | `_workspace/02_presentation_contract.md` | Defines authorized sources, semantics, fallbacks, provenance, and evidence limits |
| Implementer, Writer, or Asset Producer | Presentation Domain QA Reviewer | Changed files and `_workspace/02_presentation_contract.md` | Lets QA compare presentation output against its actor-visible contract |
| Presentation Domain QA Reviewer | Orchestrator | `_workspace/03_presentation_qa.md` | Records pass/fix/redo status and presentation-specific risks |
| Orchestrator | Contributor | `_workspace/final/handoff.md` | Captures final result, tests, and follow-up dependencies |

## Artifact Naming

Use deterministic names:

- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- `_workspace/02_mechanism_design.md`
- `_workspace/02_presentation_contract.md`
- `_workspace/03_domain_qa.md`
- `_workspace/03_presentation_qa.md`
- `_workspace/final/handoff.md`
- `_workspace/research/{topic-slug}.md` for bounded research branches
- `_workspace/experiments/{run}/results.tsv` only for explicit autonomous
  experiment loops

## Failure Policy

- Missing canonical docs: stop and report the missing file before generating
  project-specific design or implementation.
- Missing external evidence: label the mechanism as a design abstraction and
  add an unresolved evidence question instead of fabricating certainty.
- Scope pressure: defer broad mechanisms unless they are necessary for the
  current roadmap phase or first vertical slice.
- Reviewer status `fix`: make targeted revisions, then rerun the applicable
  automated/agent QA checks. Human review is not required to continue.
- Reviewer status `redo`: return to the relevant evidence, mechanism, or
  presentation-contract phase and preserve the failed artifact for comparison.
- Presentation scope without authorization: document the proposed contract or
  harness only when requested; do not create assets or start a roadmap milestone.
- Missing or conflicting asset rights: exclude the asset from release, preserve
  the source record for audit, and use a registered generic fallback.
- Conflicting domain assumptions: document both positions and choose the
  narrower reversible abstraction for the current slice.

## Validation Checks

- Every generated `SKILL.md` has YAML frontmatter with `name` and `description`.
- Local skill names are prefixed with `hs-` and do not reuse global skill names.
- The harness does not define generic Rust, code review, comment, release, or
  spec-maintenance roles.
- Handoff paths in skills and team spec match exactly.
- Proposed mechanisms distinguish invalid operations from unfavorable modeled
  outcomes.
- Proposed scenarios include decision logs, causal explanation, and debrief
  hooks when gameplay or education is in scope.
- Presentation semantics trace to actor-visible host sources or committed
  history, and unknown values have explicit fallbacks.
- Meaningful visual/audio assets have accessibility equivalents, registry
  records, provenance, license basis, hashes, and approval state.

## Test Scenarios

### Normal Flow

Request: "Design the first payer-provider negotiation slice."

Expected outputs:

- `_workspace/00_input/request-summary.md` identifies Phase 3 or 5 depending on
  requested depth.
- `_workspace/01_evidence_map.md` separates evidence-backed assumptions from
  abstractions.
- `_workspace/02_mechanism_design.md` defines actors, information, feasible
  actions, outside options, effects, and debrief hooks.
- `_workspace/03_domain_qa.md` checks deterministic inputs, actor-specific
  observations, and educational explanation.

### Failure Flow

Failure point: the request asks for national-scale US policy modeling before the
vertical slice.

Expected behavior:

- The orchestrator records the request as out of current scope.
- The mechanism designer narrows to one regional market or one policy process.
- Domain QA returns `fix` or `redo` if the artifact still requires a broad
  framework or unsupported forecasting claim.

### Presentation Normal Flow

Request: "Add a visible staffing-pressure treatment to the regional board."

Expected outputs:

- `_workspace/00_input/request-summary.md` names the authorized milestone and
  rejects unrelated roadmap expansion.
- `_workspace/02_presentation_contract.md` maps staffing-pressure semantics to
  actor-visible host fields, including observation timing and unknown state.
- The contract defines text/symbol, reduced-motion, muted, and missing-asset
  behavior before implementation.
- `_workspace/03_presentation_qa.md` traces the implementation to those sources
  and records provenance plus evidence limits.

### Presentation Failure Flow

Failure point: a proposed music state derives urgency from private rival intent
or true-state deterioration not present in the actor-visible projection.

Expected behavior:

- The contract designer rejects the hidden source and selects a visible signal
  or non-informational ambience.
- Presentation QA returns `redo` if the hidden-state classifier remains.
- Muted play and visible text remain strategically complete.
