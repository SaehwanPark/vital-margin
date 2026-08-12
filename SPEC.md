# Project Specification

This is the concise spec-driven-development index for Vital Margin.
It records what is true, what is being changed, and what is
intentionally deferred. Detailed release history remains in `CHANGELOG.md`,
dated findings remain under `docs/history/` and `_workspace/`, and architectural
decisions remain in `docs/decision-records/`.

Canonical product and domain direction lives in:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/visual_audio_enhancement_roadmap.md`

## Spec maintenance rule

Keep `Present` small. Every active item must state `Done`, `Not Yet Done`, and
`Deferred / Non-Goals`. Move completed slices to `Past` after verification;
never use `SPEC.md` as a per-commit journal.

## Past

### Project foundation and deterministic simulation

- Rust CLI, deterministic state transitions, explicit stochastic inputs,
  actor-specific observations, immutable history, replay verification, and
  state hashes are implemented and tested.
- Stabilization, competitive regional-market, and regional-affiliation
  campaigns are implemented with scenario selection and educational debriefs.
- The MCP adapter exposes bounded agent playtesting and typed actor-visible
  reads, validation, resolution, history, replay, and debrief surfaces.
- Campaign persistence includes host checkpoints, per-session archives,
  discovery, opaque checkpoint references, save-artifact download, recovery,
  and deterministic continuation for all three GUI campaigns.

### GUI and presentation baseline

- The dependency-free browser client is served by a loopback Axum host and
  remains a thin presentation layer over the Rust/MCP contracts.
- The GUI supports all three campaigns, progressive Setup/Brief/Decide/
  Resolve/Review workspaces, host-ordered contextual actions, direct and
  competitive decision flows, visible consequence/resolution views, history,
  replay, debrief, settings, reduced motion, text scaling, mute/audio
  fallbacks, and checkpoint recovery.
- Visual/audio catalogs, asset registries, credits, release hashes, loading and
  offline policies, and missing-content fallbacks are machine-checked.
- Chromium evergreen desktop is the active supported target. Codex in-app
  browser inspection is development evidence. Firefox, WebKit/Safari, mobile,
  and legacy browsers remain deferred.

Historical boundary note: Phase 0 acceptance does not promote structured DTOs;
later GUI DTOs are promoted only through the current host contracts and ADRs.
Historical phase labels retained for evidence indexing: Phase 1 static executive desktop; Phases 8–9 remain sequentially gated; those labels are not current
promotion gates and remain future work only in their dated evidence records.

### GUI-focused documentation and SDD alignment (v0.14.3)

- Maintained Markdown was classified and aligned with the implemented
  three-campaign loopback GUI, deterministic host boundary, AI-native
  progression rules, and Chromium-default browser policy.
- Root SDD files were compacted into current-state indexes; release journals,
  historical reports, accepted ADR bodies, generated credits, and versioned
  workspace evidence remain preserved in their source roles.
- A repository-wide currentness checker, focused tests, and CI command now
  enforce document roles, current GUI facts, browser scope, and human-evidence
  claim limits.

### Progressive workspace navigation gating (v0.14.4)

- Future GUI workspaces are disabled until the existing host/session event
  unlocks their visible task handoff; Setup and already-unlocked workspaces
  remain reviewable.
- Native disabled semantics, written requirements, and event-order regression
  tests protect keyboard/focus and presentation-only authority boundaries;
  session-boundary resets prevent stale terminal tabs from carrying forward.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-support boundary changed.

### Terminal task handoff (v0.14.5)

- The shared first-session task rail now renders an explicit final-debrief
  state when an existing host terminal signal or end-session result moves the
  workspace to Review.
- A nonterminal session load clears the terminal task state; no terminality is
  inferred from local turn counts or hidden presentation content.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-support boundary changed.

### Consequence timing and replay context (v0.14.6)

- Visible consequence links render existing observed-month/turn and replay
  state-hash context with deterministic unavailable fallbacks.
- Source labels, target focus, information boundaries, and private-state
  exclusions remain unchanged; no causal certainty or future outcome is added.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-support boundary changed.

### Committed effect delta legibility (v0.14.7)

- Committed-effect consequence links render the existing host delta as signed
  text, with an explicit unavailable fallback for malformed or missing values.
- Regional signals and visible processes remain delta-free; timing, replay-hash,
  source, target focus, information boundaries, and private-state exclusions
  remain unchanged.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-support boundary changed.

### Visible institutional response links (v0.14.8)

- Existing response-step items are projected as target-free, delta-free
  consequence links with host source and replay context.
- Absent response steps produce no fabricated card; present empty or malformed
  items use written unavailable detail while private actor intent remains hidden.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-support boundary changed.

### Registered response status token (v0.14.9)

- Visible response links reuse the approved runtime `status-reported` token
  with its existing label, symbol, tooltip, source, and written equivalent.
- Effects, regional signals, processes, response text, focus, and information
  boundaries remain unchanged; no new asset or audio provenance is added.
- No host route/schema, simulation, persistence, replay, or browser-support
  boundary changed.

### Browser-safe response token insertion (v0.14.10)

- Response-token headings keep the normal `prepend` path and use a deterministic
  `insertBefore` fallback when the DOM helper is unavailable.
- Content, token semantics, focus, accessibility equivalents, source/replay,
  and browser scope remain unchanged; no new engine is certified.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  campaign boundary changed.

### Playtest history evidence closure (v0.14.11)

- The visible-envelope recorder path is regression-tested to preserve a
  host-reported transition turn, state hash, and transition count after a
  committed decision refresh.
- The stabilization first-decision matrix capture now includes its committed
  history observation; the analyzer still reports `command_without_history`
  when a capture omits that evidence.
- No host route/schema, simulation, persistence, replay, asset, audio, or
  browser-authority boundary changed.

## Present

The documentation baseline and the bounded GUI-first technical checkpoint are
complete through v0.14.11. Present work is limited to gap-gated refinement from
the Future queue below; each item advances through agent-executable evidence and
automated/domain QA rather than a human stop gate.

The checkpoint does not establish human usability, learning, lived
accessibility, legal clearance, calibration, balance, policy validity, or
non-default browser/device support.

## Future

Future work is promoted only when an AI-agent trace, authoring failure,
debrief mismatch, domain-QA finding, accessibility-mode failure, or release
check identifies a bounded unmet need.

### 1. GUI task-workspace quality

Refine Setup/Brief/Decide/Resolve/Review sequencing, action-card density,
focus/recovery behavior, large text, reduced motion, and three-campaign wording
using host-backed DOM/transport tests and AI-agent task traces.

### 2. Actor-visible consequence legibility

Improve map, facility, process, resolution, history, and debrief relationships
only from existing actor-visible fields or a separately justified host
projection. Do not infer private intent, true-state severity, or causal
certainty in the browser.

### 3. Registered visual/audio production

Add only assets or audio that answer a strategic or explanatory question, have
machine-readable provenance and hashes, preserve text/mute/reduced-motion
fallbacks, and fail closed to generic presentation when metadata is incomplete.

### 4. Default-browser release hardening

Maintain Chromium evergreen desktop and loopback source-checkout evidence,
offline/loading policy, performance proxy, and deterministic GUI smoke coverage.
Do not promote non-default browser or device support without a separately
authorized decision.

### 5. Agent-native validation and revision

Run reproducible profiles across campaigns, seeds, action paths, failure
recovery, keyboard, large-text, reduced-motion, and audio-off modes. Use
technical/domain/presentation QA to prioritize revisions. Keep human-learning,
legal, calibration, and policy-validity claims explicitly unestablished.

## Promotion rules

Before a Future item becomes Present, record the concrete evidence gap, the
smallest artifact or behavior to change, source/authority boundaries,
verification commands, and non-goals. A passing automated check may close a
technical contract; it may not be described as human outcome evidence.

## Deferred / non-goals

- Network multiplayer, remote hosting, browser-owned simulation state, GUI-only
  rules, general visual editors, patient/interior simulation, and broad model
  generalization.
- Firefox, WebKit/Safari, mobile, legacy-browser, and real-device certification.
- Human usability, learning, classroom effectiveness, lived accessibility,
  legal clearance, empirical calibration, balance, and policy validity claims.
- Unregistered, unverifiable, or resemblance-risk assets in the runtime release.
