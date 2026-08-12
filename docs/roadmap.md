# Vital Margin Roadmap

**Status:** Canonical current direction
**Reviewed:** 2026-08-02
**Code baseline:** v0.14.12

This roadmap is the short current queue. Historical phase plans, release
journals, and evidence packets remain in `docs/history/`, `_workspace/`, and
versioned evaluation artifacts. They are evidence of what was considered or
verified at a point in time, not current promotion gates.

## Current position

The deterministic Rust core, CLI/reference interface, MCP adapter, and three
campaign paths are implemented. The loopback Axum GUI is the active product
focus: it presents stabilization, competitive regional-market, and regional-
affiliation campaigns through a shared Setup/Brief/Decide/Resolve/Review
workspace. The host owns validation, action ordering, transitions, history,
replay, debriefs, checkpoint discovery, and durable restoration. The browser
owns reversible presentation state only. Future workspace tabs remain disabled
until their existing host/session handoff event makes the visible task ready;
Setup and prior workspaces remain reviewable. The current-task rail switches to
final-debrief wording when the host reports a terminal session.
Visible consequence links now show existing timing and replay-hash context with
written unavailable fallbacks; committed-effect links also show existing signed
deltas with explicit malformed-data wording; the same panel now carries
host-reported visible institutional responses without inferred targets; these
cards reuse the approved reported-status token.
AI-agent playtest captures now retain host-reported history/hash evidence after
a committed visible-envelope refresh; missing history remains an explicit
analyzer finding rather than an inferred commit.

The current release is technically playable but is not a calibrated forecast,
measured learning intervention, lived-accessibility result, legal clearance,
policy validation, or balance certification. Those claims remain unestablished;
their uncertainty does not block technical GUI progress.

## Current technical checkpoint

The bounded GUI-first baseline is complete through v0.14.11: workspace task
handoffs, consequence timing/delta/response legibility, registered response
signals, Chromium-safe token insertion, and complete playtest history evidence
all satisfy their current automated exit checks. This closes the present
technical checkpoint without claiming human usability, learning, lived
accessibility, legal clearance, calibration, or policy validity.

Future work remains gap-gated. A new slice requires a reproducible AI-agent
trace, authoring failure, debrief mismatch, domain-QA finding, accessibility-mode
failure, or release-check finding; absent that evidence, no broader feature or
browser-support expansion is promoted.

## Development sequence

| Completed foundation | Current focus | Deferred boundary |
| --- | --- | --- |
| Deterministic transitions and explicit stochastic inputs | GUI task-workspace quality | Non-default browsers |
| True state vs actor observations | Consequence and causal legibility | Network/multi-user hosting |
| CLI, MCP, replay/history, and durable checkpoints | Registered visual/audio signals | New campaigns or simulation rules |
| Three campaign runtime coverage | Chromium evergreen hardening | Mobile, legacy, WebKit/Safari, Firefox |

## GUI-first queue

The queue is ordered by actor-visible value and bounded technical risk. Each item
has agent-executable entry and exit criteria; no item requires a human participant,
approval, sign-off, or review meeting to advance.

### 1. Workspace task quality

Trace the existing host action catalog, campaign coverage, and checkpoint
references into the Setup/Brief/Decide/Resolve/Review shell. Improve one bounded
interaction at a time while preserving all three campaign paths, host ordering,
keyboard/focus behavior, retry/refresh safety, mute/reduced-motion behavior, and
text-first fallbacks.

Technical exit: focused GUI and host-boundary tests, documentation currentness,
and a default-browser or Codex smoke artifact pass; no browser-owned legality,
effects, persistence, or replay logic is introduced.

### 2. Consequence visualization

Make source/effect summaries, uncertainty, actor reactions, and replay context
legible from existing actor-visible projections. Every new emphasis has a written
and non-color equivalent and handles stale, missing, and invalid data.

Technical exit: the displayed claim is traceable to a host field, append-only
history remains intact, private or resolved inputs stay hidden, and contract and
replay checks pass.

### 3. Registered visual/audio assets

Add only assets with a named presentation purpose, registry entry, provenance,
license fields, hashes, safety metadata, and a generic fallback. Generated credits
and notices continue to come from their generators.

Technical exit: asset, security, release, and presentation-contract checks pass;
uncertain identity, resemblance, provenance, licensing, or generation metadata is
excluded automatically. Automated checks do not establish human legal clearance
or lived-use quality.

### 4. Default-browser hardening

Keep the Chromium evergreen desktop path reliable using standards-based modules,
loopback smoke tests, and deterministic fixtures. The Codex in-app browser is a
development inspection surface. Firefox, WebKit/Safari, mobile, legacy browsers,
and real-device certification are deferred and non-certified.

Technical exit: the default browser checks pass without expanding browser scope;
historical cross-engine evidence cannot create a current certification gate.

### 5. AI-native validation

For every slice, an agent records the bounded claim, affected source/routes/
schemas, automated checks, evidence artifact, and unresolved evidence limits.
Agents may revise or stop on a reproducible technical failure; human studies or
approval are optional external feedback, never routine stop gates.

Technical exit: changed Markdown is classified by the currentness checker, all
required checks pass, and the handoff reports changed-file groups, deferred scope,
and claims that remain unestablished.

## Evidence and claim boundaries

Normal technical evidence includes documentation links/currentness, route and
schema contract tests, replay/history checks, asset validation and release
verification, Chromium-targeted compatibility/performance checks, and the Rust
suite. These checks can establish implementation and traceability properties.

They cannot establish human learning, classroom effectiveness, human comfort or
lived accessibility, legal clearance, policy validity, calibration, balance,
optimality, or resemblance. External research and participant feedback may be
added as separate evidence, but never as a prerequisite for the technical queue.

## Historical phase index

Phases 0–8 established governance, research/design artifacts, deterministic
architecture, vertical slices, campaign coverage, reproducible tooling, and
release documentation. Their accepted decisions and evidence remain preserved
in the ADRs, changelog, history tree, and versioned workspace records.

The old post-release Phase 9 expansion list is superseded by the GUI-first queue
above. A future runtime or browser expansion requires a new bounded proposal and
ADR; it does not become active merely because an old phase document mentions it.

## Source of truth

- [`SPEC.md`](../SPEC.md) — Past/Present/Future state index.
- [`ARCHITECTURE.md`](../ARCHITECTURE.md) — code and authority boundaries.
- [`visual_audio_enhancement_roadmap.md`](visual_audio_enhancement_roadmap.md) —
  detailed presentation queue and technical closure baseline.
- [`docs/README.md`](README.md) — document classes and authority rules.
- [`docs/decision-records/0014-ai-native-gui-and-browser-boundary.md`](decision-records/0014-ai-native-gui-and-browser-boundary.md) — current AI-native and browser decision.
