# Architecture

Last Reviewed: 2026-08-02
Status: Verified against v0.14.12 source and tests

The project is a deterministic Rust simulation with CLI, MCP, and loopback
browser presentation interfaces. The host/core owns simulation truth and
authoritative mutations. The GUI is a thin, dependency-free client that
renders actor-visible projections and keeps only reversible presentation state.

## System shape

```text
scenario/configuration
  -> model and campaign genesis
  -> validated commands + resolved inputs
  -> deterministic transition/effects/history
  -> actor-visible observations and debriefs
  -> CLI, MCP, and loopback GUI projections
```

## Core simulation

`src/model/`, `src/sim/`, `src/competitive/`, `src/affiliation/`, and
`src/scenario/` own typed state, commands, validation, deterministic
transitions, campaign rules, explicit stochastic inputs, events, effects, and
scenario loading. A transition evaluates an immutable prior snapshot plus
validated commands, resolved inputs, and a versioned ruleset. It does not read
wall-clock time, browser state, network state, or hidden global randomness.

True state, actor beliefs/observations, reported measurements, and committed
history remain distinct. Unfavorable outcomes are modeled results; invalid
authority or malformed commands are validation errors.

## History, replay, and debrief

`src/model/history.rs`, `src/model/competitive_history.rs`, `src/replay/`,
`src/artifact/`, and `src/debrief/` preserve append-only transitions,
observation-before-command context, state hashes, replay artifacts, causal
source/effect summaries, and player/instructor debrief boundaries. Presentation
reads cannot rewrite history, generate outcomes, or turn local animation/audio
state into replay state.

## CLI and MCP interfaces

`src/cli/` is the reference text interface for campaign selection, commands,
reports, persistence, and debriefs. `src/mcp/` exposes bounded stdio tools and
typed actor-visible projections, including:

- session start/get/end and host checkpoint save/load;
- competitive presentation, action catalog, validation, resolution, and
  regional-world reads;
- shared `campaign-coverage-v1` reads for all three campaigns;
- history and replay reads; the loopback GUI host additionally owns checkpoint
  discovery, opaque checkpoint references, and host save-artifact download.

MCP and GUI mutation paths delegate to the same host validation and transition
logic. Read projections are non-mutating and must omit true state, resolved
inputs, effect queues, private rival actions, and instructor-only detail unless
the explicit post-run surface authorizes it.

## Loopback GUI host

`src/bin/vital-margin-gui.rs` starts `src/gui_server.rs`, an Axum loopback-only
host. It embeds the current `gui/` module graph and serves same-origin routes
under `/api/v1/`. The host owns `GameSessionStore`, session IDs, campaign
creation, validation, transitions, history, replay, debriefs, checkpoint
discovery, and durable per-session checkpoint archives.

The GUI supports `competitive-regional-v1`, `stabilization-v1`, and
`regional-affiliation-v1`. Its current presentation shell is a progressive
Setup/Brief/Decide/Resolve/Review workspace with host-ordered action cards and
campaign-specific action contracts. The browser owns only navigation,
selection, drafts, disclosure, focus, animation pacing, audio, and local
presentation preferences.

## Browser modules and assets

`gui/host-adapter.mjs` is the transport boundary. `gui/app.mjs` coordinates
session reads, actions, resolution, history/replay, checkpoint recovery, and
presentation state. `gui/workspace.mjs` owns task navigation and acknowledgement
state, including event-unlocked future-workspace navigation while leaving prior
workspaces reviewable. The first-session flow mirrors the existing host terminal
signal with final-debrief wording and resets that local state on nonterminal
loads. Consequence links render only existing timing/hash context with explicit
fallbacks. Other modules render regional-world, semantic containers,
visual/audio
catalogs, motion, and fallbacks.

`assets/` separates source, generated, registry, and release paths. Registry,
license, hash, SVG-safety, credits, loading, offline, and missing-asset checks
are automated. Meaningful visual/audio signals require text or visible
equivalents and may not leak hidden state. Unverifiable assets remain excluded
and use generic fallback presentation.

## Browser support boundary

The default supported target is Chromium evergreen desktop with native ES
modules, `fetch`, SVG, CSS Grid, and optional Web Audio/local storage. The
Codex in-app browser is a development inspection surface. Firefox,
WebKit/Safari, mobile, legacy browsers, and real-device certification are
deferred; existing smoke artifacts remain historical technical evidence and do
not create an active support gate.

## Durable constraints

- Keep core transitions deterministic and stochasticity explicit.
- Preserve true-state, belief, observation, and reported-measurement
  boundaries.
- Keep history append-only and hashes/replays reproducible.
- Keep actor utility distinct from social welfare and educational evaluation.
- Keep browser presentation actor-visible, reversible, and host-authoritative.
- Do not duplicate legality, formulas, transitions, persistence, or replay in
  the browser.
- Require written, non-color, mute, reduced-motion, scaling, missing-data, and
  failure fallbacks for decision-relevant presentation.
- Treat automated and AI-agent evidence as technical/gameplay evidence, not
  proof of human learning, lived accessibility, legal clearance, calibration,
  or policy validity.

## Extension posture

Add a new mechanism, DTO, route, asset family, browser target, or campaign only
after a bounded evidence gap identifies the need. Prefer extending existing
typed host projections and shared presentation primitives. A change that would
alter simulation authority, replay semantics, persistence formats, or public
browser support requires a new ADR and a separate implementation slice.

Historical phase records may say that later interface work “remain future work”;
current implementation status is defined by the verified sections above.
