# GUI executive desktop and adapter reference

**Current status (v0.14.12):** The loopback Axum host is the active GUI surface
for all three campaigns. The host owns actions, transitions, history/replay,
debriefs, and durable checkpoint discovery/restoration; this browser client is
presentation-only. The shared task rail labels terminal sessions as
final-debrief review and resets on a nonterminal load. Chromium evergreen desktop
is the default end-user target;
visible consequence links retain host timing and replay-hash context with
written fallbacks, show existing committed-effect deltas, and carry visible
institutional response items with the registered reported-status token.
Playtest captures retain host-reported history/hash evidence after committed
visible-envelope refreshes; missing history remains a recoverable evidence
finding.
The current bounded GUI-first technical checkpoint is complete; future changes
remain evidence-gated.
Codex in-app browser inspection is development evidence. Firefox,
WebKit/Safari, mobile, and legacy browsers are deferred and non-certified.

## Authority and presentation state

The loopback host is authoritative for simulation state and transitions; the
browser renders actor-visible projections and text/accessibility fallbacks.

## Players: use the live GUI host

From the repository root, run:

```bash
cargo run --bin vital-margin-gui
```

Keep the process running and open the printed loopback URL. The live GUI
supports `competitive-regional-v1`, `stabilization-v1`, and
`regional-affiliation-v1`. Complete instructions and
troubleshooting are in [`docs/guides/gui-how-to-play.md`](../docs/guides/gui-how-to-play.md).

The host-owned `campaign-coverage-v1` read is available for all three campaign
IDs. All campaigns use the same `Actions` card surface: competitive play drafts
a `Monthly plan`, while stabilization and regional affiliation commit one
decision directly. Competitive validation and submit remain host-authoritative;
the coverage companion panel is read-only after normal start/load and accepted
refreshes. Coverage does not reveal private rival state or add browser
simulation authority, and a failed companion read does not block the actions.

Opening `gui/index.html` directly or through a generic static server intentionally
shows fixture/demo mode; it cannot start a live scenario by itself.

## Task workspace and progressive disclosure

The shell presents one task workspace at a time: Setup, Brief, Decide, Resolve,
and Review. Header metrics, source-linked signals, uncertainty, host status,
costs, and written equivalents remain rendered from the existing host envelopes;
navigation changes presentation state only. Future workspace navigation is
disabled until the existing host/session handoff event unlocks it; Setup and
already-unlocked workspaces remain available for review. Start/load and refreshed nonterminal
sessions open Brief, accepted submissions open Resolve, and terminal sessions
open Review. The current task strip exposes the primary handoff and keeps the
full first-session sequence behind an accessible disclosure.

Long collections use host order and bounded defaults (three signals/actors/
processes, six actions, and five history rows). A visible total and a
“Show remaining” disclosure retain the rest without local ranking. The regional
board is full-width on supported tablet/desktop layouts and moves behind a
native disclosure below 768px, where entity cards remain the default review
surface. Settings, audio, credits, and advanced session controls live in a
keyboard-safe utility dialog; selected entities and visual-token explanations
use the same contextual drawer with text fallbacks.

This redesign is technically verified by static, host-contract, loading, and
offline checks. Human cognitive-load, clarity, consequence-comprehension, and
lived-accessibility outcomes remain unestablished; optional external feedback
does not gate technical GUI progression. Unverified artwork remains excluded in
favor of generic registered fallbacks.

## Unified Actions workspace

Open **Actions** to see each host-provided action once. Cards start collapsed;
open one card at a time, enter only the shown parameters, and use **Details**
for host timing, rules, uncertainty, cost, canonical template, and source.
Missing details are shown as unavailable rather than inferred.

Competitive sessions place the draft beside the cards in **Monthly plan**.
Use **Add**, **Revise**, **Save**, and **Remove** as needed; any edit requires
**Check plan** again before **Commit month** becomes available. Stabilization and
regional-affiliation sessions use the same cards with **Commit decision**.
Rejected submissions keep the expanded card and entered values; every
submission still uses the canonical command path.

The collapsed **Technical controls** disclosure is available only in static or
demo mode. Live host play keeps legal-command and free-form CLI controls hidden;
the host remains the source of legality, cost, uncertainty, and transitions.

## SVG rendering proof

Open `gui/svg-proof.html` directly or through a static server to inspect the
Phase 1.2 deterministic SVG fixture. It uses `scene.mjs` and the selected
Variant A vocabulary, exposes institution/facility selection through keyboard
reachable SVG controls, and includes explicit generic/uncertain fallbacks. The
proof page is fixture-only: it does not load a host, submit a command, or create
simulation state.

## Riverside identity proof — shared health-system kits

Open `gui/identity-proof.html` directly or through a static server to inspect
the Phase 2.1 fictional Riverside, Northlake, and Summit identity kits. It
shows the selected source and release mark, monochrome treatment, compact
marker, facility sign, report header, text badge, audio motif reference, and
generic fallback. The proof is fixture-only and does not load host state or
change a session.

## Actor-family language proof

Open `gui/actor-family-proof.html` directly or through a static server to
inspect the shared Phase 2.2 fictional payer, regulator, labor, employer,
community, board, policy coalition, and independent-provider language. It
shows each family’s glyph, report-frame pattern, written notification style,
optional identity-sonic tag, visible source, and generic fallback. The proof is
fixture-only and does not load host state or change a session.

## Facility component proof

Open `gui/facility-proof.html` directly or through a static server to inspect
the Phase 3.1 fictional general-hospital base, patient-tower,
emergency-department, ambulatory-center, specialty-center, rural-clinic,
administrative-headquarters, parking-structure, utility-plant,
research-education-building, construction-crane, and undeveloped-parcel
components. It
shows the selected compact release derivative, seven composable layers, visible
layer sources, written equivalents, non-color patterns, and generic facility
fallback. The proof is fixture-only and does not load host state or change a
session.

## Regional map grid contract

`map-environment.mjs` defines the fixture-only 24px regional map grid and
deterministic cell coordinates used by later map/environment slices. The grid
is symbolic: coordinates organize relationships and attention without asserting
real-world distance or geography.

`map-tiles.mjs` adds the fixture-only symbolic road tile set used by later
intersection and district slices. Horizontal, vertical, and quarter-curve
segments have written orientation labels and a generic fallback; they do not
assert real-world road geometry or travel time.

`map-districts.mjs` adds the fixture-only symbolic district tile set with
commercial, residential, employer-center, and government tokens. Each token
has a non-color pattern and generic fallback; it does not assert real-world
land use, population, ownership, zoning, travel time, or jurisdiction.

`map-parcels.mjs` adds the fixture-only symbolic facility and undeveloped-land
parcel tokens on the shared grid. Each token has a non-color pattern and
generic fallback; it does not assert ownership, availability, development
potential, land value, zoning, geography, or future use.

`map-relationships.mjs` adds fixture-only peer, service, policy, and uncertain
relationship-line styles with non-color patterns, no arrowheads, and a generic
fallback. The styles do not infer hidden intent, causality, strength, direction,
distance, or future outcome.

`map-service-areas.mjs` adds fixture-only primary, shared, and coordinated
service-area overlays with symbolic contour/fill patterns, no metric encoding,
and a generic fallback. The overlays do not establish real-world catchment,
distance, travel time, population, access, jurisdiction, or performance.

`map-uncertainty.mjs` adds fixture-only stale, missing, and revised
visible-information overlays with non-color patterns, no severity encoding,
static reduced-motion behavior, and a generic fallback. The overlays do not
quantify hidden risk, severity, probability, truth, or future outcome.

`map-event-markers.mjs` adds fixture-only policy, workforce, community, and
project event-marker categories with stable glyph/shape labels, no severity or
priority encoding, static reduced-motion behavior, and a generic fallback.
`map-environment-proof.html` composes the shared map vocabulary and documents
compact, standard, and wide target layouts, keyboard order, bounded zoom, and
bounded pan. Coordinates and controls remain symbolic local presentation state;
they do not assert geography, distance, travel time, ownership, jurisdiction,
or host/session behavior.

## Operational overlay proof

Open `gui/operational-overlay-proof.html` directly or through a static server
to inspect the twelve Phase 3.3 operational overlay contracts. It shows each
visible source, non-color pattern, written equivalent, reduced-motion rule, and
a deterministic simultaneous-overlay stack with explicit overflow count. The
proof is fixture-only and does not infer severity, intent, causality, future
outcomes, or host/session state.

## Static regional-board proof

Open `gui/regional-board-proof.html` directly or through a static server to
inspect the Phase 4.1 host-shaped regional board. `regional-board.mjs` maps a
recorded `competitive-regional-world-v1` envelope into the existing SVG
identity, facility, status, overlay, source, and missingness vocabulary. The
proof keeps institution/facility selection local, shows generic fallbacks, and
preserves keyboard and written equivalents. It is fixture-only: it does not
load a host, submit a command, create simulation state, or assert real
geography.

The main `index.html` mounts the same SVG board beside the existing semantic map
and detail panels. `app.mjs` routes board, report, and semantic-list focus
through one local selected-entity state; the host DTO remains authoritative for
all visible values and future transitions.

## Visible consequence linkage

`consequence-links.mjs` projects actor-visible regional signals/processes and
host-committed resolution effects into deterministic, source-linked list items.
Public rival signals retain their observed month and private-detail boundary;
resolution effects without a host target remain targetless. The main page links
reports to entities, entities to related reports/consequences, and consequence
items back to board focus using local keyboard controls. Replay helpers preserve
turn/state-hash sequence entries without rewriting current host history.

## Semantic information-container proof

Open `semantic-container-proof.html` directly or through a static server to
inspect the Phase 5.1 board packet, operations ledger, intelligence report,
regulatory letter, project sheet, news wire, executive action queue, and
after-action report contracts. The proof toggles compact/expanded variants and
keeps headings, markers, source/status language, exact visible text, responsive
reflow, print output, and reduced-motion behavior inspectable. It is fixture-only
and does not load a host, submit a command, create simulation state, or consume
hidden data.

`semantic-containers.mjs` is a presentation catalog; its structural distinctions
do not imply severity, priority, causality, authority, or outcome.

## Metric and trend visualization proof

Open `metric-visualization-proof.html` directly or through a static server to
inspect the Phase 5.2 sparkline, month-over-month delta, capacity bar, staffing
composition, project progress, payer-mix, trust/legitimacy trend, and visible
uncertainty interval contracts. The proof keeps exact values, source/status,
uncertainty, and missingness in text; it also exposes large-text, print, and
reduced-motion behavior. A deterministic SVG snapshot guards the fixture
output. It is fixture-only and does not load a host, submit a command, create
simulation state, or consume hidden data.

`metric-visualizations.mjs` is an opt-in adapter: the live GUI renders a visual
only when an actor-visible metric descriptor supplies `visualization_kind` and
its corresponding values. It never converts absent fields into trends or
percentages.

## Motion specification proof

Open `motion-proof.html` directly or through a static server to inspect the
Phase 6.1 focus, report-arrival, month-transition, project, public-rival,
status, metric-delta, and relationship-line motion contracts. The proof shows
deterministic replay order, reduced-motion replacements, interruption results,
simultaneous-animation limits, and a declared local frame budget without
starting timers or animations. It is fixture-only and does not load a host,
submit a command, create simulation state, or consume hidden data.

`motion-catalog.mjs` is a policy/planning catalog for later motion
implementation; it never owns focus, commands, transitions, randomness,
history, hashes, replay authority, or debrief facts.

## Audio direction proof

Open `gui/audio-proof.html` directly or through a static server to inspect the
Phase 1.3 generated Web Audio direction candidates. It documents loudness,
peak, duration, loop, and ducking targets and exposes visible source/text
equivalents beside confirmation, rejection, report, identity, ambience,
pressure, and environmental previews. The proof is fixture-only: it does not
load a host, change a session, or replace the live audio client.

## Audio cue refinement proof

Open `gui/audio-cue-proof.html` directly or through a static server to inspect
the Phase 7.1 contract for all 16 existing interface and event cues. Each row
shows semantic purpose, priority, duration, normalized recipe target, peak
ceiling, cooldown, visible trigger source, text equivalent, and a distinct
cue label. The page is fixture-only and does not load a host, use hidden state,
or play recorded audio.

The live audio panel exposes `Full audio` and `Cues only`. Cues-only suppresses
music and ambience while retaining interface/event cues and their visible/text
equivalents. Mute, unavailable browser audio, reduced notifications, and focus
loss remain complete presentation fallbacks.

## Environmental ambience library proof

Open `gui/ambience-proof.html` directly or through a static server to inspect
the Phase 7.2 executive office, hospital lobby, hospital campus exterior,
construction site, boardroom, press/policy event, and regional city bed
contracts. Each row exposes generation/license/hash basis, explicit no-release-
file derivative status, noise floor, reviewed seamless loop, loudness/peak
targets, no-speech/music/name/alarm constraints, and written/reduced-audio
fallbacks. The fixture is dependency-free and does not load recorded audio,
host state, hidden state, or network resources.

`ambience-contract.mjs` is the pure runtime catalog. The optional live client
keeps the regional city bed as the only default ambience selection; explicit
setting selection remains a presentation contract and never changes simulation
or replay state.

## Adaptive music stem proof

Open `gui/music-stem-proof.html` directly or through a static server to inspect
the Phase 7.3 menu/planning, stable operations, pressure, regulatory scrutiny,
competitive escalation, affiliation/negotiation, and debrief states. Each row
shows the five stem roles, visible trigger, bounded loop/crossfade metadata,
written equivalent, and fallback. The proof is fixture-only and does not load
host state, hidden data, network resources, or recorded audio.

`music-stem-contract.mjs` is the pure visible-state catalog and replay-sequence
planner. The live panel keeps music optional, exposes `Music only mute`, and
continues to support full mute and cues-only mode without removing written
context.

## Audio priority and fatigue proof

Open `gui/audio-priority-proof.html` directly or through a static server to
inspect the Phase 7.4 fixed priority order, one-critical-per-batch rule,
routine aggregation, queue cap, simultaneous transient-voice bound, bounded
ducking, local preference boundary, and written equivalents. The proof is
fixture-only and does not load host state, submit a command, play audio, or use
network resources.

`audio-priority-contract.mjs` plans visible cue batches deterministically.
`audio.mjs` dispatches at most one transient cue voice, suppresses repeats,
ducks ambience for major/critical cues and music for critical cues, and stores
only explicit local audio preferences when browser storage is available. All
reports, sources, status text, and controls remain available when sound is
queued, aggregated, ducked, muted, reduced, unsupported, or interrupted.

## Local generation workflow proof

The generation and portrait proof pages below are historical fixture and
asset-admission references, not active GUI technical promotion gates. Their
separate external-review fields protect candidate asset release claims; an incomplete
candidate remains excluded and the registered generic fallback is used, while
technical GUI work continues.

Open `gui/generation-workflow-proof.html` directly or through a static server
to inspect the Phase 8.1 approved-model scope, generation metadata contract,
prompt template, external-review boundary, fail-closed release gate,
and empty manifest. The proof is contributor-facing and fixture-only: it does not load
model weights, run inference, create an asset, call a hosted service, or use
network resources.

`scripts/capture_generation_metadata.py` captures prompts, negative prompts,
seeds, settings, source/release hashes, post-processing, accessibility, and
review metadata from a local request. `scripts/validate_generation_metadata.py`
rejects unknown models/licenses, missing or mismatched hashes, incomplete
human-review metadata, unapproved release records, and invalid visual/audio
registry bridges from release. A rejected candidate remains out of the runtime
registry; future technical work uses the written equivalent and generic
fallback.

## Fictional actor portrait proof

Open `gui/portrait-workflow-proof.html` directly or through a static server to
inspect the Phase 8.2 seven-role portrait contract, identity-only meaning,
small-size/grayscale checks, generic actor-marker fallback, and all seven
preserved preview candidates. Every preview is explicitly unverified and is
outside the runtime GUI, visual asset registry, release directory, and
generation manifest because the preview tool does not expose the approved
local model revision or actual seed. `scripts/validate_generation_metadata.py`
enforces the exact role set, preview hash/dimension/path boundary, and blocks
candidate asset promotion until approved model/seed provenance and portrait
review fields are complete; it does not block technical GUI progression.

Open `portrait-review-proof.html` to inspect the seven per-role external-review
packets, explicit pending evidence, written equivalents,
generic fallbacks, and candidate release-boundary rule. The worksheet is
contributor/release-only; it does not perform human review or add portrait
authority to the runtime GUI.

## Developers: adapter contracts

This is a dependency-free browser surface over typed actor-visible MCP
presentation, action, and resolution contracts plus optional generated audio.
For static integration work, open `gui/index.html` through a static file server and
provide a live or recorded read-only adapter:

```js
window.HsMgtGameReadOnlyAdapter = {
  sessionId: "session-1",
  async startSession({ campaign, seed, difficulty }) {},
  async getPresentation(sessionId) {
    // Call get_presentation or return a recorded envelope with the same schema.
  },
  async getRegionalWorld(sessionId) {},
  async getCampaignCoverage(sessionId) {},
};
```

The read-only client expects `schema_version: "competitive-read-only-v1"` and
renders the typed `session`, `resources`, `observation`, `institutions`,
`pending_effects`, `history`, `latest_transition`, and `replay` fields. It can
consume live MCP output or a recorded envelope without knowing which source
provided it. The demo envelope is display fixture data, not a second simulation
state, and remains available when no read-only adapter is configured.

For the Phase 3/4 action and resolution path, inject a separate host adapter with
`getPresentation`, `getActionCatalog`, `validateTurn`, and `submitTurn`. The
page then renders forms from the host action catalog, keeps draft rows locally,
and submits only an unchanged batch that the host marked valid:

```js
window.HsMgtGameActionAdapter = {
  sessionId: "session-1",
  async startSession({ campaign, seed, difficulty }) {},
  async getPresentation(sessionId) {},
  async getRegionalWorld(sessionId) {},
  async getHistory(sessionId) {},
  async getReplay(sessionId) {},
  async saveSession(sessionId) {},
  async loadSession(sessionId) {},
  async getActionCatalog(sessionId) {},
  async validateTurn(sessionId, commandText) {},
  async getResolution(sessionId, turn) {},
  async endSession(sessionId) {},
  async submitTurn(commandText) {},
  async getCampaignCoverage(sessionId) {},
};
```

`createReadOnlyClient` never calls `submitTurn`. The action-builder path is
enabled only when `HsMgtGameActionAdapter` is supplied; it submits only an
unchanged host-validated batch. The legacy `createThinClient` and
`HsMgtGameAdapter.submitTurn` export remain available for compatibility with
the earlier thin-client proof, but are not wired into the Phase 3/4 page.
Host/core code remains authoritative for commands, transitions, randomness,
history, hashes, and debriefs.

After a successful action submission, `getResolution(sessionId, turn)` may
return `schema_version: "competitive-resolution-v1"`. The page renders the
eight host-sourced resolution steps, before/after operating/resource values,
direct committed effects, and state hash. Play, pause, skip, review, and a
historical-turn read are local presentation controls; `getResolution` never
advances the session. Text remains in the DOM when paused or reduced motion is
enabled.

The live resolution envelope may also include `audio_cue_ids`, an additive
host-shaped list of existing event-cue catalog IDs derived from committed,
actor-visible data. The page honors that list, including an explicit empty
list; envelopes from older adapters that omit the field use the existing
visible-only `visibleEventCues` classifier. Cue playback remains optional and
the catalog's written equivalents remain the meaning-bearing fallback.

The same live resolution envelope may include `music_state_id`, one of the
existing music-stem catalog states selected from committed visible context.
The page uses a valid non-empty state when present and otherwise keeps the
visible-only music classifier. Music remains optional atmospheric support;
written resolution and status text remain complete when muted or unavailable.

When supplied, `getHistory(sessionId)` returns
`schema_version: "competitive-history-v1"` with the host's immutable
transition summaries, aligned transition count, and state hashes. The page
validates and renders this dedicated read through the existing text-first
history view; unsupported, malformed, or failed reads preserve the current
history and report a recoverable adapter error. The route never submits a
turn, regenerates replay data, or creates save/load state.

When supplied, `getReplay(sessionId)` returns
`schema_version: "competitive-replay-v1"` with the same immutable summaries,
seed, transition count, and latest visible state hash. The page validates the
alignment and renders the existing history/replay list. **Previous row**,
**Next row**, **Play replay**, and **Pause replay** move a local written cursor
over those rows and show the selected command, optional visible observation,
events/effects, and state hash. Failure preserves the current list and cursor;
an empty replay disables movement with an explicit written state. Historical
committed resolution review remains the separate host-read
`getResolution(sessionId, turn)` path. The host verifies competitive history
deterministically before returning the replay projection; the browser still
does not regenerate or simulate replay data.

When supplied, `saveSession(sessionId)` and `loadSession(sessionId)` return
`schema_version: "competitive-save-v1"` with `saved`/`loaded` operation,
identity, committed count, and latest visible hash. The live page exposes
explicit Save host checkpoint and Restore host checkpoint controls, and
requests an autosave after each accepted campaign decision. Autosave uses the
same host-only checkpoint route and reports success or failure in written
status; it never rolls back a committed transition. Restore
uses the existing host read path to refresh presentation, action catalog,
history, replay, and regional-world views; failed operations preserve the
current view. The loopback GUI host also writes an explicit competitive,
stabilization, or regional-affiliation checkpoint to its application-config
save path, wrapping the existing `CompetitiveSessionSave`, `SessionSave`, or
`AffiliationReplayArtifact` artifact with the opaque session ID. Each explicit
checkpoint is written to a separate host-owned file in a sibling
`.checkpoints` archive keyed by that opaque ID; older single-file checkpoints
remain loadable as a migration fallback. `GET /api/v1/checkpoints` and the
**Find saved checkpoints** control expose only validated session metadata
(campaign, opaque ID, seed, transition count, and archive/legacy source); an
entry fills the existing ID field but never loads automatically. After a host
restart, a browser refresh may request the existing host `loadSession` route
once after an unknown live-session read, then repeat the same actor-visible
reads. Manual loads do not trigger that durable hydration path; transient
refresh failures preserve the stored opaque ID for retry, while confirmed
unknown sessions clear it. The browser never serializes or loads the save artifact; invalid
checkpoint files are omitted from discovery. An explicit Download host save
request is the only path that transfers validated bytes to the user's file
download.

Each discovered entry can export a deterministic `gui-checkpoint-reference-v1`
JSON file, and the Saved checkpoints panel can import one. A reference contains
only the discovery metadata and fills the existing opaque session-ID control;
it never loads automatically, writes browser storage, or carries host save
contents, history, hashes, resolved inputs, or true state. The host still
validates the current checkpoint when the user chooses Load or Restore.

Each validated discovered entry also exposes **Download host save**. The host
revalidates the selected archive or legacy checkpoint and serves the existing
save bytes as an attachment; the browser only performs the user-requested
download and does not serialize, parse, load, or store the artifact as game
state. A failed download leaves the current session active and reports a
written recovery message.

When supplied, `getRegionalWorld(sessionId)` returns
`schema_version: "competitive-regional-world-v1"`. The page renders a
schematic identity map, visible demand/access/process overlays, owned facility
detail, and lagged public rival signals. Map selection and navigation are local
presentation state; rival private detail remains explicitly unavailable.

When supplied, `endSession(sessionId)` returns
`schema_version: "competitive-end-session-v1"`. The host terminal response
contains the immutable transition summaries, replay seed/count/latest hash, and
host-authored debrief lines. The page renders those fields as a final
text-first history/debrief view, disables further action, and does not retry or
recreate a terminated session. A failed end-session request leaves the current
presentation active. Optional debrief music is atmospheric only; written
history, hashes, and debrief text remain complete when audio is muted.

When supplied, `getCampaignCoverage(sessionId)` returns
`schema_version: "campaign-coverage-v1"` for all three campaigns. The loopback
launcher exposes this read; stabilization and regional-affiliation use it as
their primary action surface, while competitive sessions retain their richer
presentation/action catalog and may use the coverage envelope as a companion.
The projection keeps each campaign's
briefing, visible metrics, actor signals, process status, decision forms,
immutable history, replay metadata, and host-provided debrief distinct.
Decision forms substitute only host-provided parameter values into the host
command template; the existing `submitTurn` path remains the only mutation
path. Host rejection is shown as a recoverable error and does not fabricate a
local transition.

The same envelope may include an optional `audio` projection with
host-supplied `music_state_id` and `audio_cue_ids`. The browser accepts only
IDs already present in `AUDIO_CATALOG`; an explicit empty cue list suppresses
campaign cues, while omitted audio metadata preserves the older visible-state
and regional-milestone fallback. Audio remains optional and the written
campaign surface is complete without it.

Committed stabilization and regional-affiliation history entries may also
include optional actor-visible observation lines from before the corresponding
command. The browser presents them in a native written disclosure; older
entries without the field and competitive history remain valid.

For reproducible interface-task traces, inject an optional recorder from
`playtest.mjs` into any client. It emits `schema_version: "gui-playtest-v1"`
with declared campaign/role/task metadata, allowlisted onboarding/settings/
recovery/command/validation/audio/history/hash/semantic-snapshot events, and
separate evidence lanes. It never stores raw adapter payloads, true state,
resolved inputs, effect queues, private rival actions, hidden DOM payloads, or
model hidden reasoning:

```js
import { createPlaytestRecorder } from "./playtest.mjs";

const recorder = createPlaytestRecorder({
  metadata: {
    campaign: "stabilization-v1",
    role: "first-time",
    task: "complete-first-decision",
    interface_mode: "browser-adapter",
    accessibility_mode: "reduced-motion",
    capture_method: "semantic-recorder",
  },
});
const client = HsMgtGui.createReadOnlyClient({ recorder });
recorder.attach(document);
await client.load();
console.log(recorder.toJSON());
```

Run the deterministic diagnostic over a capture with
`python3 scripts/diagnose_gui_playtests.py capture.json`. The protocol records
interface-task evidence only; it does not score strategies or establish human
usability, accessibility, learning, engagement, calibration, balance, or policy
validity.

For repeated declared captures, run the Phase 9 comparison with
`python3 scripts/analyze_gui_playtests.py tests/fixtures/gui_playtest_matrix`.
The analysis preserves campaign/role/task/seed/accessibility distinctions and
emits only deterministic evidence-gap/recovery hypotheses plus explicit limits;
it never changes the GUI, simulation, or host history.

Phase 2/3/4/5/6/7/8/10/11/12/13 review checklist:

- load a live or recorded envelope and observe the loading-to-loaded state;
- locate typed cash, AP, political capital, trust, and session metadata;
- inspect current observation, observed player capacity/facility metrics, and
  public market/information-gap signals;
- follow a pending process and monthly result back to its typed source;
- inspect committed transitions and state hashes without changing the turn;
- exercise empty, missing, unsupported-schema, and adapter-error states; and
- verify that the read-only path does not expose or call command submission.
- with the action adapter, add/revise/remove drafts, validate through the host,
  and confirm submit is unavailable until validation passes.
- after a committed submit, locate all eight resolution steps and compare the
  before/after snapshots without treating differences as inferred causality;
- pause, skip, review a historical committed turn, and enable reduced motion;
  confirm text remains complete and no session transition occurs.
- enable optional audio, exercise independent channels, mute, focus loss, and
  reduced notifications; confirm the same visual/text result remains complete.
- load the regional-world projection, select each public/owned entity, switch
  overlays, follow navigation links, and confirm public-signal lag and missing
  private detail remain labeled.
- load stabilization and regional-affiliation campaign coverage, confirm their
  distinct role/stage/briefing/metric/actor/process surfaces, and commit one
  unified action-card decision through the canonical host path.
- exercise a rejected campaign command, confirm the error is recoverable, and
  verify history/replay/debrief output remains host-sourced.
- open onboarding/settings, toggle reduced motion and written equivalents,
  activate retry after an adapter failure, attach a `gui-playtest-v1` recorder,
  and verify semantic snapshots contain only allowlisted visible controls.
- run the deterministic diagnostic on the capture twice and confirm failure
  classes and evidence lanes are stable.
- use the skip link or presentation navigation to reach briefing, actions,
  resolution, and debrief without pointer input;
- switch Standard/Large text size and confirm the local setting is reflected
  without changing host commands or session data;
- open the status-language legend and confirm each status has text plus a
  non-color symbol/pattern cue;
- hide optional cue explanations and confirm written results, observations,
  history, resolution, and debrief remain visible.
- start `competitive-regional-v1` through an adapter that maps to the existing
  host session-start operation, confirm the returned session ID loads typed
  presentation, then load an existing session ID;
- exercise missing start capability, malformed session envelopes, invalid seed,
  and failed replacement loads without losing the current rendered session or
  calling command submission.
- follow the competitive first-session rail from start/load through visible
  inspection, two local drafts, host validation, unchanged submission,
  resolution, and refreshed presentation; confirm it reaches Continue only
  after both host reads succeed;
- start stabilization or regional affiliation and confirm the rail changes to
  campaign coverage: inspect, choose an action card, review the refreshed
  stage, and continue only after canonical host submission succeeds;
- revise or remove a draft after validation and confirm the rail returns to its
  draft/validation handoff without limiting the existing draft controls; reject
  a host operation and confirm the current session and path remain recoverable.

This checklist is a technical/interface-task proxy, not human usability or
lived-accessibility evidence.

Visual identity and marker tokens come from the project-generated
`visual-catalog-v1` in `visual.mjs`; they label visible systems, facilities,
overlays, and processes while preserving source/status text. Unknown identities
and categories use explicit generic fallbacks. The registry and credits are
`visual-catalog.json` and `ASSET_CREDITS.md`.

Asset audit: zero downloaded assets, external fonts, network calls, or image/audio
files. CSS, HTML, JavaScript, generated visual glyphs, and generated Web Audio
recipes are the complete surface. The typed projection contains no true-world state, resolved stochastic
inputs, private rival actions, or client-side cost formula. Phase 5 audio, Phase 6
regional-world projection, and Phase 7 campaign coverage are optional,
visible-only, registry-recorded, and presentation-only; Phase 8 capture and
diagnostics plus Phase 9 comparison are optional, allowlisted, and
 presentation/test evidence only. Phase 10 accessibility behavior is local
presentation state and does not establish human accessibility. Phase 11
session launch/load is an optional host adapter boundary and does not create
local session state. Phase 12 visual identity/marker lookup is a generated,
visible-only vocabulary and does not create host facts or local game state. Phase
13 first-session continuity is a local text-first stage projection; it does not
create a host payload, client-side legality/outcome rule, transition, or local
simulation state. The competitive seven-stage rail and the campaign-coverage
five-stage rail both report presentation handoffs only. Phase 6.2 first-month resolution sequencing is a pure local
storyboard over the host-owned `competitive-resolution-v1` envelope. It renders
every committed stage immediately, annotates display-only priority and
board/report/metric synchronization targets, aligns optional cues to visible
stages, and exposes native advance, skip, pause, and review controls. Skip and
reduced motion alter only local emphasis; they retain all written reports and
effects. The sequence planner has no transition, randomness, network, history,
hash, or hidden-state authority.
The settings panel's Low-distraction mode is also local presentation state: it
temporarily enforces reduced motion, Large text, written cue explanations,
muted audio, and reduced notifications, then restores the prior local
preferences when disabled. It does not change host commands, validation,
transitions, replay, or simulation state.
Richer causal
overlays, recorded assets, true geography, and broader campaign expansion
require a new bounded proposal.

## In-game asset credits

The settings panel includes an accessible, text-first “Asset credits and
provenance” disclosure. `asset-credits.mjs` is generated from the canonical
`assets/registry/*.json` manifests; `asset-credits-renderer.mjs` renders only
text content, approval/release status, attribution, source, license,
provenance, and written equivalents. It is available before host/session data
loads and uses no network, command, simulation, history, replay, or debrief
authority. The generated module is checked by
`python3 scripts/generate_asset_credits.py --check`.
