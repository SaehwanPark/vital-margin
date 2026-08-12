# Visual and Audio Enhancement Roadmap

**Status:** Active GUI delivery queue
**Reviewed:** 2026-08-02
**Code baseline:** v0.14.12
**Owner:** repository agents and maintainers

## Current technical checkpoint

The bounded GUI-first presentation baseline is complete through v0.14.11.
Future work remains conditional on a reproducible evidence gap; this checkpoint
does not establish human comprehension, lived accessibility, legal clearance,
calibration, balance, or policy validity.

This is the current visual/audio work queue for the host-backed GUI. It replaces
the former completion diary with a small set of executable tracks. The Rust
simulation, MCP adapter, CLI reference interface, and shared host action surface
remain the factual authority. This document describes presentation work only;
it does not authorize a runtime schema, save-format, simulation, or browser-scope
change.

## Current implemented baseline

- `src/bin/vital-margin-gui.rs` starts a loopback Axum host; the host owns session
  truth, action validation/order, transitions, history, replay, debriefs, and
  durable checkpoint discovery/restoration.
- The GUI presents `stabilization-v1`, `competitive-regional-v1`, and
  `regional-affiliation-v1` through Setup/Brief/Decide/Resolve/Review task
  workspaces.
- `gui/host-adapter.mjs` and `gui/app.mjs` consume typed host projections,
  campaign coverage, action catalogs, validation, resolution, history/replay,
  checkpoint references, and save-artifact downloads.
- Presentation state is reversible and browser-local: navigation, selection,
  drafts, disclosure, focus, animation pacing, audio, and preferences. The
  browser never decides legality, formulas, effects, persistence, replay, or
  hidden state.
- Text-first, non-color, mute, reduced-motion, scaling, missing-data, and
  failure fallbacks are part of the contract. Unverified visual/audio assets are
  excluded and replaced by registered generic fallbacks.
- The shared current-task rail labels terminal host sessions as final-debrief
  review and resets that label on a nonterminal load.
- Visible consequence links expose existing timing and replay-hash context;
  missing values remain explicitly unavailable. Committed-effect links expose
  existing signed deltas and keep malformed values unavailable. Visible
  institutional response items remain target-free and host-sourced, with the
  approved reported-status token reused for emphasis.
- AI-agent playtest captures retain host-reported history/hash evidence after a
  committed visible-envelope refresh; the analyzer keeps missing history as a
  revision finding.
- Chromium evergreen desktop is the default end-user target. The Codex in-app
  browser is a development inspection surface. Firefox, WebKit/Safari, mobile,
  legacy browsers, and real-device certification are deferred and non-certified.

## Delivery policy

Each queue item is an agent-executable technical slice. An agent may advance an
item when source, tests, and evidence satisfy its entry/exit criteria. No item
requires a human participant, approval, sign-off, or scheduled usability study to
continue technical work. Optional external feedback may be recorded separately,
but it is not a promotion gate.

Automated evidence can establish route/schema compatibility, deterministic
presentation contracts, accessibility-equivalent presence, asset provenance
metadata, replay safety, and default-browser smoke behavior. It cannot establish
human learning, lived accessibility, legal clearance, policy validity, balance,
calibration, or resemblance. Those claims remain explicitly unestablished.

## Ranked active queue

### 1. Workspace task quality

**Purpose:** Make the Setup/Brief/Decide/Resolve/Review progression legible for
all three campaigns without duplicating simulation rules.

**Entry criteria:** The host action catalog and campaign coverage are current;
the workspace can recover a durable checkpoint; the current contract tests pass.

**Agent steps:** Inspect the route DTOs and workspace state; implement one bounded
presentation improvement; preserve host ordering and actor-visible disclosure;
add or update deterministic contract tests; capture a Chromium or Codex browser
smoke artifact when the change affects layout or interaction.

**Exit criteria:** All supported campaigns retain a complete task path; refresh,
back/forward, retry, mute, reduced-motion, keyboard/focus, and text fallbacks
remain safe; future workspace navigation is disabled until its existing
host/session handoff event; no browser-owned mutation or hidden-state leak is
introduced; the focused tests and documentation currentness checker pass.

### 2. Consequence legibility

**Purpose:** Show sources, effects, uncertainty, actor reactions, and replay
context without turning private true state into player information.

**Entry criteria:** A concrete actor-visible gap is named against an existing
projection or debrief surface; the relevant history/replay field is identified.

**Agent steps:** Trace the source/effect DTO from deterministic transition to host
projection; add only the smallest presentation or copy change; provide written
and non-color equivalents; add a regression fixture for stale, missing, and
invalid data.

**Exit criteria:** The display is causally traceable to an existing host field;
history remains append-only; private rival actions and resolved inputs stay
hidden; fallback copy identifies unavailable information; automated contract and
replay checks pass.

### 3. Registered visual/audio signals

**Purpose:** Improve emphasis, pacing, and consequence feedback with safe,
reproducible assets.

**Entry criteria:** The signal has a named actor-visible purpose, a text or
visible equivalent, and an asset-registry/provenance record or a generic fallback
plan.

**Agent steps:** Extend the asset registry and contract; validate license fields,
hashes, dimensions, codecs, SVG safety, and release inclusion; wire the signal
behind mute/reduced-motion and missing-asset fallbacks; update generated credits
only through their generator.

**Exit criteria:** `scripts/validate_assets.py`, security/release checks, contract
audits, and focused GUI tests pass. Uncertain identity, resemblance, provenance,
license, or generation metadata fails closed to exclusion and fallback. No human
approval is represented as technical completion.

### 4. Default-browser hardening

**Purpose:** Keep the supported Chromium evergreen desktop path reliable as GUI
modules evolve.

**Entry criteria:** A reproducible Chromium-targeted defect or compatibility
assumption is identified in the current code or smoke fixture.

**Agent steps:** Reproduce with the loopback host, patch standards-based code,
add a deterministic fixture or smoke assertion, and verify the same path in the
Codex in-app browser when available.

**Exit criteria:** The default path passes the browser compatibility and device
performance checks without adding a new engine requirement. Firefox,
WebKit/Safari, mobile, legacy, and real-device work remains explicitly deferred;
historical smoke evidence is not a certification gate.

### 5. Agent-native validation and revision

**Purpose:** Make every GUI change reviewable by future agents without a human
stop gate.

**Entry criteria:** The change has a bounded claim, affected source/route/schema
list, and a stated evidence limit.

**Agent steps:** Run focused documentation, contract, asset, browser-default, and
Rust checks; compare generated/current references with source; inspect the diff
for stale future claims; record evidence and unresolved limits in the handoff.

**Exit criteria:** The checker classifies changed Markdown correctly; all required
technical checks pass; the handoff names changed-file groups, evidence limits,
deferred scopes, and any unresolved risk. A human study may be proposed as
external follow-up but never blocks this queue.

## Technical completion evidence

The following checks are the normal evidence set for a presentation slice:

```text
python3 scripts/check_documentation_currentness.py
python3 scripts/check_documentation_links.py
python3 scripts/check_browser_compatibility.py
python3 scripts/check_device_performance.py
python3 scripts/validate_assets.py
python3 scripts/verify_asset_release.py --check
python3 scripts/generate_asset_credits.py --check
python3 scripts/audit_visual_audio_contract.py
python3 -m unittest discover -s tests
```

Evidence is technical and bounded. Passing checks do not prove human
comprehension, learning, comfort, accessibility in lived use, legal clearance,
calibration, balance, or policy validity.

## Phase 9: Asset and presentation technical closure

The former diary's completed technical baseline is preserved here as a compact
reference. These entries record automation, not human legal or human review
completion; they establish technical policy conformance only. Legal clearance
and lived-use review remain external, optional, and unestablished.

Status: Complete in v0.12.78
Status: Complete in v0.12.79
Status: Complete in v0.12.80
Status: Complete in v0.12.81
Status: Complete in v0.12.82
Status: Complete in v0.12.83
Status: Complete in v0.12.84

- [x] License allowlist encoded in validation.
- [x] License denylist encoded in validation.
- [x] Attribution text generated.
- [x] Source URLs archived where practical.
- [x] Retrieval dates present.
- [x] Original licenses saved or referenced.
- [x] Modification descriptions present.
- [x] Approval status required.
- [x] Third-party notices generated.
- [x] Release package includes credits.
- [x] In-game credits accessible.
- [x] Automated license policy audit completed before release;
- [x] SVG scripts and external references rejected.
- [x] Embedded raster images reviewed.
- [x] External fonts rejected.
- [x] Unexpected metadata stripped.
- [x] Audio codec validation implemented.
- [x] File-size limits enforced.
- [x] Dimension limits enforced.
- [x] Hashes verified in CI.
- [x] Release build reproducibility checked.
- [x] Asset loading failures degrade gracefully.

Technical closure references: `scripts/validate_assets.py`,
`scripts/validate_asset_security.py`, `scripts/verify_asset_release.py`,
`scripts/sanitize_svg_metadata.py`, `assets/ASSET_RELEASE_MANIFEST.json`, and
`assets/THIRD_PARTY_NOTICES.md`.

Technical closure did not establish human legal clearance or human review
completion. Assets with unresolved provenance remain excluded.

## Phase 10: Future extension boundary

The active queue above supersedes speculative phase diaries. Any future phase
must first name its actor-visible contract, deterministic source fields,
automated exit checks, and evidence limits. Human feedback, if sought, is
external context rather than a technical stop gate.

## Deferred and excluded work

- Firefox, WebKit/Safari, mobile, legacy browsers, and real-device certification.
- Networked or multi-user GUI hosting and browser-owned persistence.
- New campaigns, simulation mechanisms, asset identity/resemblance claims, or
  audio/visual expansion without a bounded contract and registry entry.
- Human-subject studies, classroom outcomes, policy forecasting, calibration,
  balance certification, and legal-quality conclusions as promotion gates.

## Source links

- [`docs/roadmap.md`](roadmap.md) — project-wide current position and queue.
- [`ARCHITECTURE.md`](../ARCHITECTURE.md) — code and authority boundaries.
- [`gui/README.md`](../gui/README.md) — GUI technical reference.
- [`docs/validation/playtesting.md`](validation/playtesting.md) — agent evidence
  protocol and claim limits.
- [`docs/decision-records/0014-ai-native-gui-and-browser-boundary.md`](decision-records/0014-ai-native-gui-and-browser-boundary.md) — current governance decision.

## Historical technical evidence index (non-gating)

The following compact labels preserve source-bound references used by older
technical evidence validators. They are point-in-time evidence identifiers, not
active Future work, human stop gates, browser certification tasks, or release
requirements. The ranked queue above is authoritative for current progression.

## Vertical-slice sprint

- [x] Integrate the board with live competitive-session data.
- [x] Link facilities and reports.
- [x] Implement visible project progression.
- [x] Implement first-month consequence presentation.
- [x] Add adaptive planning and pressure music states.

## 8. Final Program Rule

Historical technical closure remains bounded by host authority, actor-visible
projections, deterministic replay, generic fallbacks, and explicit human-evidence
limits. It does not promote structured DTOs or a new runtime surface.

## Milestone 10.1:

- [x] Three systems visible.
- [x] Facilities visually distinct.
- [x] Institutional identity consistent.
- [x] Facility selection works.
- [x] Uncertainty rendering works.
- [x] Project overlay works.
- [x] Pressure overlay works.
- [x] Rival observation timing respected.
- [x] Briefing uses semantic container.
- [x] Action queue uses semantic container.
- [x] Reports use actor-family identities.
- [x] Metrics use appropriate visualizations.
- [x] Source and status labels remain visible.
- [x] Month sequence implemented.
- [x] Critical event prioritization works.
- [x] Map and reports update coherently.
- [x] Skip behavior works.
- [x] Reduced-motion behavior works.
- [x] Replay is deterministic.
- [x] UI cues refined.
- [x] Environmental ambience available.
- [x] Adaptive music transition works.
- [x] Priority and cooldown manager works.
- [x] Full mute works.
- [x] Cues-only mode works.
- [x] Text equivalents remain available.
- [x] Every asset registered.
- [x] Every asset hashed.
- [x] Every license policy check passes; human legal review remains external.
- [x] Credits generated.
- [x] AI metadata complete where applicable.

## Milestone 10.2:

- [x] Test protocol written.
- [x] First-session tasks defined.
- [x] Recognition tasks defined.
- [x] Consequence-tracing tasks defined.
- [x] Accessibility tasks defined.
- [ ] Audio preference feedback collected.
- [ ] Quantitative ratings collected.
- [ ] Qualitative interviews completed.
- [ ] Findings classified as defect, preference, or scope expansion.
- [x] Revision log created.
- [ ] Go/no-go decision recorded.

The `phase10.2-audio-preference-review-packet.json` and its preparation note
record technical audio preference/listening review packet prepared. Optional
external feedback remains outside technical promotion.

# Phase 11:

## Milestone 11.1:

- [x] Facility asset coverage complete.
- [x] Current supported operational-overlay coverage complete. Evidence:
- [x] Current 24-month competitive facility placement/use read continuity
- [x] Actor-family coverage complete.
- [x] Event cue coverage complete.
- [x] Music-state coverage complete.
- [x] History view updated.
- [x] Current competitive terminal debrief view covered. Evidence:
- [x] Current in-memory host checkpoint visual continuity covered. Evidence:
- [x] Current explicit durable competitive host checkpoint recovery covered.
- [x] Current competitive full-campaign host checkpoint continuation covered.
- [x] Current full stabilization host checkpoint continuation covered.
- [x] Current full regional-affiliation host checkpoint continuation covered.
- [x] Current cross-campaign latest-checkpoint identity covered. Evidence:
- [x] Current full-campaign host audio-state coverage covered. Evidence:
- [x] Current full-campaign host history/replay continuity covered. Evidence:
- [x] Current full-campaign coverage renderer continuity covered. Evidence:
- [x] Current full-campaign coverage transport continuity covered. Evidence:
- [x] Current explicit durable stabilization host checkpoint recovery covered.
- [x] Current explicit durable regional-affiliation host checkpoint recovery covered.
- [x] Current live replay visual continuity covered. Evidence:
- [x] Current local replay playback over visible host rows covered. Evidence:
- [x] Unknown content fallbacks tested.
- [x] Current tracked visual/audio asset-registry coverage is 100%. Evidence:
- [x] Current supported screenshot-surface contract passes. Evidence:
- [x] Current full-campaign local-browser screenshot inspection recorded.
- [x] Current persisted 1024x768 full-campaign raster evidence recorded.
- [x] Current persisted terminal raster state correction recorded. Evidence:

## Milestone 11.2:

This historical boundary had no current promotion effect; the GUI-first queue
supersedes it.

## Historical gate markers (non-gating)

- [ ] Prompt and seed recorded.
- [ ] Crop and release derivative completed.
- [ ] Identity consistency reviewed.
- [ ] Real-person resemblance reviewed.
- [ ] Anatomy and artifact review completed.
- [ ] No protected marks present.
- [ ] Registry entry approved.
- [ ] Small-size rendering tested.
- [ ] Grayscale rendering tested.
- [ ] Audio preference feedback collected.
- [ ] Quantitative ratings collected.
- [ ] Qualitative interviews completed.
- [ ] Findings classified as defect, preference, or scope expansion.
- [ ] Go/no-go decision recorded.
- [ ] Educational usability reviewed.
- [ ] First-session workflow complete.
- [ ] Competitive campaign coverage complete.
- [ ] No real institution accidentally represented.
- [ ] No public-figure resemblance remains.
- [ ] No unsupported clinical implication introduced.
- [ ] AI-generation metadata complete.
- [ ] Debrief visuals reviewed.
- [ ] Complete asset provenance review.
- [ ] Run structured first-time-user evaluation.
- [ ] Record revision decisions.
- [ ] Approve or reject expansion to full campaign coverage.

The historical browser/device marker is retained as evidence scope only:
coverage, durable persistence, cross-browser/device certification, and human
educational/accessibility gates remain open in the old audit artifact. Current
policy instead supports Chromium evergreen desktop and explicitly defers other
engines; no human gate blocks technical progression.

Historical audit marker: coverage, durable persistence, cross-browser/device
certification, and human educational/accessibility gates remain open.

## Current technical evidence references

- `scripts/validate_asset_security.py`
- `scripts/sanitize_svg_metadata.py`
- `assets/ASSET_RELEASE_MANIFEST.json`
- `assets/THIRD_PARTY_NOTICES.md`
- `phase10.2-audio-preference-review-packet.json`
- `Current technical audio preference/listening review packet prepared`
- `phase13.1-ai-preview-provenance-review-packet.json`
- `docs/evaluation/phase13.1-ai-generation-metadata-boundary.json`
- `technical AI-preview provenance/human-review packet prepared`
- `actual model identity, immutable revision, sampler, and seed remain `unverified-preview`/`pending`; human-review gates remain open`
- `[x] Attribution complete. Evidence: current repository-owned attribution`
- `[ ] No unsupported clinical implication introduced.`
- `[x] Current GUI source/content wording scan completed.`
- `bounded repository-owned source/content wording check`
- `[x] Current technical competitive campaign boundary documented.`
- `[x] Current competitive full-campaign technical review packet prepared.`
- `[ ] First-session workflow complete.`
- `[x] Current technical first-session path documented and recoverable.`
- `[x] Current technical first-session path documented and recoverable.`
- `[x] Current technical first-session review packet prepared.`
- `[x] Current first-session technical review packet prepared.`
- `phase13.1-first-session-review-packet.json`
- `participant-ready technical packet; pending human evidence remains optional`
- `[x] No hidden-state leak found.`
- `[ ] Debrief visuals reviewed.`
- `[x] Current technical debrief visual review packet prepared.`
- `[x] Current technical debrief visual presentation contract documented.`
