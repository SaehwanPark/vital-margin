# Lessons Learned

## Keep presentation and symbol naming unified across crate, binaries, and harness

- Context: Transitioning from generic/legacy working titles to "Vital Margin"
  requires aligning display titles, binary targets, crate module paths, agent
  skills, and documentation links simultaneously.
- Risk: Divergent binary names (`hs-mgt-game-gui` vs `vital-margin-gui`) or broken
  harness references cause link validation or automated test failures.
- Resolution: Establish a clear dual rule ("Vital Margin" for human-facing
  display text; `vital-margin` / `vital_margin` for crate, binary, and symbol
  names) and update all links and harnesses atomically.
- Prevention: Run automated documentation link checkers, release metadata
  validators, and full test suites after any rebranding.

## Keep playtest commits paired with host history evidence

- Context: a stabilization playtest fixture recorded an accepted command and
  completion without the host's committed history/hash observation.
- Risk: an agent could mistake a local submission event for a committed
  transition, weakening the strategic-trace evidence lane.
- Resolution: record visible host-envelope history after refresh, keep the
  matrix fixture complete, and retain `command_without_history` as a diagnostic
  when an artifact omits the evidence.
- Prevention: test both the complete capture and the analyzer's missing-history
  finding; never infer commit status from a command event alone.

## Preserve token order when DOM helpers are constrained

- Context: response-token insertion used `Element.prepend`, which is standard in
  the default browser but may be absent in a constrained test DOM.
- Risk: a missing helper could drop the registered token or change the heading
  order while leaving written response content apparently intact.
- Resolution: keep `prepend` for the normal path and fall back to
  `insertBefore(token, firstChild)` with the same node and semantics.
- Prevention: test insertion guards as source contracts while keeping browser
  certification scope explicit.

## Reuse registered visual tokens before adding assets

- Context: response cards needed a category cue, while the approved runtime
  catalog already contained a `reported` status token with text equivalents.
- Risk: adding a new image or audio cue would expand provenance, byte-budget,
  and fallback obligations for no additional host information.
- Resolution: reuse the registered token only for response links and preserve
  its label, symbol, tooltip, source, and written equivalent.
- Prevention: inspect the current catalog and registry before creating new
  assets; treat generic fallbacks as part of the contract.

## Link actor responses without fabricating targets

- Context: host resolution steps already expose visible institutional response
  strings, but consequence links only represented effects.
- Risk: attaching a response to a board entity or metric would imply private
  actor intent, target ownership, or causal severity not present in the DTO.
- Resolution: project only the `responses` step items as target-free,
  delta-free links with host source/replay context and explicit fallbacks.
- Prevention: test absent, empty, malformed, and ordered response steps before
  wiring them into shared consequence rendering.

## Display effect direction from the host field

- Context: committed-effect links already carried a host `delta`, but the
  shared card showed only metric/detail prose.
- Risk: snapshot arithmetic or inferred labels could expose a causal claim or
  silently turn missing data into a direction.
- Resolution: format only strict numeric deltas, write explicit signed text,
  and keep regional links delta-free with a malformed-data fallback.
- Prevention: test positive, negative, zero, missing, and non-primitive values
  before adding emphasis to consequence cards.

## Consequence context must come from link fields

- Context: consequence links already carried observed month, turn, and replay
  state hash, but the renderer showed only detail and source text.
- Risk: adding inferred timing or causal prose would blur actor-visible and
  private-state boundaries.
- Resolution: format only existing link fields and make missing or invalid
  timing/hash values explicitly unavailable.
- Prevention: test both populated and malformed link context before adding
  visual emphasis.

## Terminal review must update the task rail

- Context: an existing host event can move the GUI into terminal Review while
  the browser-local current-task state still describes a monthly action.
- Risk: the visible task rail can contradict the terminal history/debrief
  surface even though the host and workspace controller are correct.
- Resolution: keep terminal task wording as an explicit local flow state, drive
  it only from the host terminal field/end-session envelope, and reset it on
  every nonterminal load.
- Prevention: test terminal rendering and cross-session reset together with
  workspace routing, rather than treating Review visibility as sufficient.

## Keep Read Companions Separate from Mutation Rails

- Context: the competitive GUI already has a validated action rail, while the
  shared campaign-coverage envelope is a richer typed read projection.
- Risk: reusing the coverage campaign loader in a normal competitive session
  would reset drafts and disable the action rail even though no command was
  submitted.
- Resolution: use a companion-only coverage read that renders the existing
  envelope without changing action-client state; treat failures as optional
  read errors and keep host submit authoritative.
- Prevention: name and test read-only companion lifecycles separately from
  campaign loaders that own controls, drafts, validation, or submission.

## Sanitize Shared Coverage History, Not Just Current Observation

- Context: competitive campaign coverage reused a typed transition-summary
  shape and the full competitive debrief while the competitive resolver records
  private rival events, effects, instructor rationales, and true-state deltas
  internally for host/instructor history and review.
- Risk: filtering only current observation fields still let a player infer an
  exact private rival command and its parameters from active coverage history,
  or receive instructor-only rival actions and metric deltas at completion.
- Resolution: map competitive coverage history from the host-owned public-action
  log, keep the player command and state hash, omit raw competitive effects, and
  use a player-safe terminal debrief; add active/private and terminal regressions.
- Prevention: treat every shared projection field—including history, debrief,
  audio inputs, and error text—as an actor-visible boundary. Preserve raw
  transitions only on host-authorized history/replay surfaces.

## Keep Shared Campaign Coverage Read-Only for Competitive Mutation

- Context: competitive presentation already has a richer action-catalog,
  validation, and submit sequence, while stabilization and affiliation use the
  shared campaign-coverage renderer.
- Risk: routing competitive decisions through a second coverage-specific
  submit path would bypass host validation or make the browser a competing
  mutation authority.
- Resolution: extend only the host-owned `campaign-coverage-v1` read projection
  with actor-visible competitive data and canonical catalog decision metadata;
  keep competitive mutation on the existing validated action rail.
- Prevention: test that competitive coverage reads do not advance history,
  exclude true-state/private-rival markers, and leave catalog/validation/
  `submitTurn` as the only competitive mutation path.

## Keep GUI autosave behind the existing host checkpoint boundary

- Context: the loopback GUI already supported explicit host checkpoints for
  competitive, stabilization, and regional-affiliation sessions, but a player
  could commit a decision and stop before saving a restart point.
- Risk: adding browser serialization or a second autosave format would create
  a competing state boundary and could make a failed save look like a failed
  decision.
- Resolution: invoke the existing `saveSession` adapter only after the host
  accepts a decision, report success/failure in the existing live status, reuse
  the approved save-complete cue, and leave the committed session active when
  saving fails. Manual Save/Restore remains an explicit recovery path.
- Prevention: test accepted-response ordering, success metadata/cue, failure
  preservation, all supported campaign paths, blocked adapters, and the
  unchanged opaque-session/host-authority boundary. Treat durable autosave as
  host persistence, not browser state.

## Keep Browser Refresh Recovery as an Opaque Same-Host Handle

- Context: the loopback GUI held the active session ID only in the in-memory
  adapter, so a browser refresh lost the route back to a still-running host
  session even though the host remained authoritative.
- Risk: storing a serialized presentation or simulation snapshot would create a
  second state boundary and could expose or reconstruct information the browser
  is not authorized to own.
- Resolution: retain only the non-empty host-issued session ID in optional
  browser storage, reuse the existing host load path, clear confirmed stale or
  terminal IDs, and preserve IDs for transient failures.
- Prevention: keep storage best-effort and written; test blocked storage,
  unknown-session cleanup, end cleanup, and authority-marker exclusions. Treat
  durable file or cross-process recovery as a separate host persistence design.

## Keep Checkpoint Transfer as a Metadata Reference

- Context: the host-owned checkpoint picker makes durable session IDs
  discoverable, but users may need to move a recovery handle between browser
  sessions.
- Risk: exporting the save wrapper, history, hash, resolved inputs, or true
  state would turn a convenience file into a second client persistence and
  authority boundary.
- Resolution: use a strict `gui-checkpoint-reference-v1` JSON contract with
  only discovery metadata; export is deterministic, import fills the existing
  ID field, and Load/Restore still invokes host validation explicitly.
- Prevention: reject extra keys and save-shaped content, keep import free of
  storage/load side effects, and state that the reference is informational
  until the host accepts it.

## Keep Decision-Time Recovery Host-Sourced and Written

- Context: core stabilization and affiliation transitions already retained the
  actor-visible observation paired with each command, but campaign history
  summaries exposed only command/effect/hash text to the browser.
- Risk: asking players to judge an earlier decision from current or outcome
  text can blur the information boundary and encourage hindsight reasoning.
- Resolution: add an optional summary field populated by existing visible
  formatters and render it as a native written disclosure tied to the committed
  history entry; omit it for competitive summaries and preserve older payloads.
- Prevention: expose only pre-command visible observations, keep hashes and
  commands host-owned, test absent-field compatibility, and keep causal or
  educational claims separate from technical recovery evidence.

## Keep Host Audio Metadata Visible-Only and Optional

- Context: campaign coverage already exposed typed stage, actor, process,
  history, and debrief data, but the browser still had to infer campaign music
  and cues from those visible strings.
- Risk: Browser-side classification can drift from host meaning, while a cue
  list without an explicit empty state can accidentally preserve legacy events
  after the host has intentionally supplied no campaign cue.
- Resolution: Project optional host-sourced music/cue IDs in the existing
  campaign envelope, filter them against the current catalog, distinguish
  omitted metadata from an explicit empty list, and keep written equivalents
  complete when audio is muted or unavailable.
- Prevention: For every new audio projection, bind it to visible host fields,
  use existing approved IDs, test allowlist and empty/omitted behavior, and
  keep human listening/quality claims separate from technical routing evidence.

## Keep Onboarding Rails Aligned with Campaign Authority

- Context: the live GUI gained stabilization and regional-affiliation
  campaign-coverage handoff, but the existing first-session rail still taught
  competitive local drafting and validation.
- Risk: A technically reachable campaign can still mislead a new player if its
  orientation rail describes controls that do not exist for that campaign.
- Resolution: Keep the competitive rail schema unchanged and add a separate
  five-stage campaign-coverage rail driven by successful host reads and writes.
  Rejected decisions do not advance the local presentation stage.
- Prevention: Whenever a new campaign renderer becomes launchable, audit the
  first-session orientation, guidance, and recovery wording for campaign-
  specific controls before calling the technical path complete.

## Keep Low-Power Evidence Explicitly Emulated

- Context: Phase 11.2 required a low-power-device test, but the verification
  environment did not provide a physical low-power device or standalone browser
  binary.
- Risk: Calling a local viewport smoke or wall-clock sample a hardware
  certification would overstate battery, thermal, memory, frame-rate, and
  accessibility evidence.
- Resolution: Define `device-performance-v1` as a reduced-capability proxy,
  record explicit source/DOM/SVG/time limits and local observations, retain
  written/audio-off fallback checks, and fail closed on `real_device: true`.
- Prevention: Keep proxy results and real-device validation as separate gates;
  never infer hardware suitability from a passing static or local smoke report.

## Bind Presentation Labels Only to Explicit Visible Fields

- Context: Phase 11.1 had a twelve-entry operational-overlay catalog, but the
  live host emitted only five category bindings.
- Risk: Filling the catalog by treating raw metrics or inferred context as
  causal labels would leak assumptions into the actor-visible surface and make
  the overlay look more authoritative than its source.
- Resolution: Bind each remaining ID only to an explicit `PlayerObservation`
  field or visible project/market/policy text; keep raw metric rows raw, omit
  absent categories, and retain the generic fallback for unknown IDs.
- Prevention: Require a ledger row, host source string, written equivalent,
  absence test, and authority-marker test for every catalog ID before marking
  current overlay coverage complete.

## Separate Terminal Debrief Coverage from Learning Claims

- Context: The competitive GUI already renders a host terminal envelope with
  history, replay metadata, and debrief lines, but the Phase 11.1 checklist did
  not have a dedicated coverage record.
- Risk: Treating a passing text renderer as evidence of educational usefulness,
  instructor readiness, or human comprehension would overstate what the test
  can establish.
- Resolution: Record exact schema/route/adapter/renderer sources, row/hash
  alignment, failure behavior, and terminal controls in a ledger; keep full
  campaign, instructor, counterfactual, accessibility, and learning gates open.
- Prevention: Every debrief-view closure must name its host source and rendered
  contract separately from human evaluation and educational-effectiveness
  evidence.

## Append to Existing Handoff Artifacts

- Context: The repository keeps durable `_workspace` request, presentation,
  and QA records across roadmap slices.
- Risk: Replacing a tracked handoff while adding a new slice silently erases
  prior evidence and makes the final review incomplete.
- Resolution: Restore the tracked artifact from `HEAD` when an accidental
  replacement occurs, then append a dated/versioned slice section with an
  additive patch.
- Prevention: Inspect `git status` and the tail of every handoff before
  editing; treat existing `_workspace` files as append-only operational state.

## Verify the Embedded GUI Route Graph, Not Only the Source Graph

- Context: The live GUI source graph was complete and loading-policy checked,
  but the loopback Rust host embedded only a subset of those modules.
- Risk: A normal-checkout user could receive the entrypoint while browser module
  requests returned 404, making the nominal offline surface incomplete.
- Resolution: Add explicit embedded routes for every live module, the injected
  host adapter, and catalogs; compare the route table to the loading policy and
  test every current route through the local server.
- Prevention: Treat source closure and delivery closure as separate contracts;
  re-open this evidence when adding a module, catalog, service worker, cache, or
  deployed origin.

## Audit the Live Module Graph Before Adding Loading Machinery

- Context: The live GUI renders the board inline and generates audio locally,
  but Phase 11.2 still called for lazy-loading and preload decisions.
- Risk: Adding a generic loader would increase complexity without a current
  file-backed asset demand, while an unchecked future module or media reference
  could bypass the policy.
- Resolution: Add `loading-policy-v1` for the exact live entrypoint/module set,
  reject media/preload markers and external/escaped sources, and require every
  local entrypoint module to be declared before a future loading exception is
  reviewed.
- Prevention: Reopen the policy with measured browser/cache/device evidence if
  file-backed assets become part of the live surface; do not infer performance
  from a static scan.

## Treat Runtime-Generated Audio as an Explicit Packaging Decision

- Context: The GUI's cues, music stems, and ambience are generated by local
  Web Audio recipes, while Phase 11.2 still required an audio-compression
  review.
- Risk: Leaving the item unchecked makes an intentionally empty release audio
  surface look like an omission; silently adding a codec policy could also
  imply runtime or device evidence that does not exist.
- Resolution: Add `audio-packaging-scope-v1` with a zero-file/zero-byte release
  boundary, enumerate known audio suffixes, require null registry release paths,
  and record `not-applicable-runtime-generated` as the current decision.
- Prevention: Reopen the compression decision in a separate reviewed slice if
  file-backed audio is introduced, with actual codec, decode, accessibility,
  and browser/device evidence.

## Keep Raster Preview Bounds Separate From Release Eligibility

- Context: The repository has seven 1254×1254 generated portrait previews but
  intentionally ships no raster derivative in `assets/release`.
- Risk: Treating preview dimensions or byte limits as release readiness could
  accidentally promote unverified images or imply runtime suitability.
- Resolution: Add a scope report that requires zero release raster files,
  bounds preview files, and rejects release paths/registry IDs while preserving
  the existing generation metadata gate.
- Prevention: Keep future raster optimization/promotion as a separate reviewed
  contract with provenance, accessibility, derivative, and runtime evidence.

## Enumerate Fallback Coverage Against the Registry

- Context: Selected fallback examples passed, but Phase 11.2 requires
  confidence that every current release descriptor degrades safely.
- Risk: A new facility or institution could be registered and rendered without
  an exercised generic fallback, leaving an unavailable asset path blank or
  accidentally authoritative.
- Resolution: Enumerate live facility and identity catalogs in Node, align the
  exact release-path set to the visual registry, and exercise missing, failed,
  malformed, and contradictory availability for every descriptor.
- Prevention: Keep catalog enumeration and registry alignment in the fallback
  gate whenever a release descriptor is added; preserve written equivalents,
  null release paths, and the no-network/no-simulation boundary.

## Optimize Release Derivatives Without Touching Source Semantics

- Context: Phase 11.2 needed an SVG optimization step, while source sheets
  contain reusable design layers and accessible wording that release files
  must preserve.
- Risk: Generic minification can rewrite geometry, style, URL, or text content
  and make registry/manifest hashes silently stale.
- Resolution: Normalize only outer/inter-tag formatting whitespace, compare a
  parsed tag/attribute/meaningful-text projection before and after, require
  idempotence, and refresh release hashes/manifest in the same change.
- Prevention: Keep source and release paths distinct; require a fail-closed
  optimization report and hash checks before any future geometry/style or
  raster/audio optimization.

## Define Packaging Budgets Before Runtime Performance Claims

- Context: Phase 11.2 calls for asset-size, cache, render, decode, memory,
  offline, device, and compatibility work, but the repository currently has a
  small tracked release directory and larger source/preview trees.
- Risk: A broad “performance hardened” label could conflate byte accounting
  with runtime behavior and accidentally include non-release previews.
- Resolution: Define named budgets against explicit `assets/release` roots and
  emit a deterministic report with observed file count, total bytes, and the
  largest file. Keep source references, generated previews, and runtime
  measurements outside the slice.
- Prevention: Require each future optimization or benchmark to declare its
  measured surface, limit, and evidence boundary before changing assets or
  loading behavior.

## Keep Live Checkpoints Host-Owned and Explicitly Ephemeral

- Context: The CLI already has durable save artifacts, while the live GUI
  session store is intentionally in memory and had no save/restore boundary.
- Risk: Letting the browser serialize presentation or history would create a
  second state authority and could make a restored view differ from the host's
  transition hash sequence.
- Resolution: Add one cloned host checkpoint per active session, expose named
  save/load operations, validate operation/count/hash metadata, and refresh all
  visible reads from the host after restore. Keep the checkpoint explicitly
  ephemeral until a separate storage contract exists.
- Prevention: Test rewind and deterministic continuation after restore,
  missing/unknown checkpoints, failed refresh preservation, and the absence of
  browser serialization or simulation calls; keep durable persistence and
  cross-process recovery separate.

## Keep Replay Continuity as Host Metadata, Not Browser Playback

- Context: The live GUI had immutable history and historical-resolution reads,
  but no dedicated replay envelope tying the visible sequence to a latest
  state hash.
- Risk: Adding browser-owned playback or hash calculation would create a
  second replay authority and could make a visually coherent sequence diverge
  from the host's committed history.
- Resolution: Add `competitive-replay-v1` as a read-only projection over
  `GameSessionStore::get_history`, validate seed/count/latest-hash alignment in
  the browser, and render through the existing text-first history surface.
- Prevention: Test empty and committed replay reads, malformed metadata,
  render preservation after a failed refresh, unknown sessions, and the
  absence of transition/simulation calls; keep persistence and replay
  regeneration as separate contracts.

## Keep Dedicated History Reads Non-Mutating

- Context: The live GUI already received history inside presentation and
  terminal envelopes, but it had no dedicated route or adapter for refreshing
  the existing history view.
- Risk: Rebuilding history in the browser or coupling a refresh to a turn
  submission would blur the host's immutable history boundary and could make
  count/hash drift look like a valid visual update.
- Resolution: Add a versioned host `HistoryEnvelope` backed only by
  `GameSessionStore::get_history`, validate transition-count and state-hash
  alignment in the browser, and preserve the current view on failure.
- Prevention: Test empty and committed reads, unknown sessions, malformed
  schemas/counts, and the absence of transition/simulation calls in the
  history handler; keep save/load, replay regeneration, and persistence as
  separate future slices.

## Keep Music-State Priority Explicit and Visible

- Context: The browser already classified music from visible presentation
  values, but live resolution also had a committed transition summary and an
  explicit terminal boundary owned by the host.
- Risk: A browser-only classifier can drift from the committed resolution
  context and can make terminal/debrief state dependent on a later refresh.
- Resolution: Add one host-shaped `music_state_id` using the existing visible
  priority—debrief, regulatory, affiliation, competitive, pressure, then
  stable operations—and make the browser use it only when it is a usable
  string. Legacy and malformed envelopes retain visible classification.
- Prevention: Test priority conflicts and every live-selectable catalog state;
  keep the ID out of simulation state, hashes, history, replay, and debrief
  facts, and preserve written equivalents when audio is unavailable.

## Make Event-Cue Selection Host-Shaped but Presentation-Only

- Context: The live resolution browser already classified event cues from
  visible text, while the host owned the committed transition summary and
  actor-visible before/after snapshots.
- Risk: Keeping the primary classifier in the browser makes cue selection
  harder to audit against the committed transition and can blur the legacy
  envelope boundary.
- Resolution: Add an additive `audio_cue_ids` projection to the host-shaped
  resolution envelope using only visible events, effects, observation text,
  and before/after margins. Honor an explicit empty list and retain the
  browser classifier only when older envelopes omit the field.
- Prevention: Test every supported cue against the catalog, keep cue IDs out
  of simulation state and hashes, and document that cue selection is a
  presentation projection rather than a new authority or event model.

## Keep Terminal Debrief and Replay on One Host Envelope

- Context: The host already generated final debrief text and removed sessions,
  but the live browser had no terminal route and could not show the debrief with
  the history that produced it.
- Risk: Fetching debrief separately or rebuilding history in JavaScript could
  produce a visually plausible but misaligned retrospective and could invite a
  second client-owned terminal state.
- Resolution: Extend one host-authoritative terminal envelope with immutable
  transition summaries and replay metadata, render it text-first, and disable
  post-termination controls only after the host response succeeds.
- Prevention: Assert that history count, latest hash, replay metadata, and
  debrief survive one terminal response; keep failed termination recoverable and
  leave persistence/replay-campaign claims separate.

## Bind Operational Overlays Only From Explicit Visible Conditions

- Context: The fixture operational-overlay catalog existed before the live
  regional-world projection carried category bindings.
- Risk: Mapping every numeric metric to a category would turn presentation
  vocabulary into an unsupported severity or causality classifier.
- Resolution: Add an optional host-shaped binding only for named visible
  conditions, keep raw demand/access/capacity metrics unchanged, and resolve
  unknown IDs through the registered generic overlay.
- Prevention: Keep the source ledger beside the DTO and test both bound and raw
  overlays; do not add a category until the host exposes a direct visible
  condition or committed history source.

## Keep Live Facility Vocabulary Host-Shaped

- Context: The regional board exposed four actor-visible facility groups while
  the visual catalog contained more specific reusable components.
- Risk: Inferring a hidden facility taxonomy or implying that a combined
  emergency/ICU observation is an exact asset match would overstate what the
  player can know.
- Resolution: Add stable component IDs at the host projection boundary, bind
  them through the existing pure catalog, and document `emergency-department`
  as a bounded presentation equivalent. Keep rival facility detail absent and
  use the generic descriptor for unknown content.
- Prevention: Treat component IDs as presentation vocabulary, not simulation
  state; require source/equivalent text and an explicit fallback in tests.

## Keep Campaign Coverage Bounded and Exact

- Context: Phase 11.1 names a broad full-campaign expansion, while the
  repository already contains several pure visual/audio catalogs and a
  bounded first-month path.
- Risk: A checklist or catalog count can imply full campaign coverage even
  when screenshot, continuity, performance, and human-quality evidence is
  absent.
- Resolution: Compare a committed ledger with live module exports, assert
  visible source/equivalent and fallback semantics, and close only the exact
  actor-family/fallback entries supported by the probe.
- Prevention: State catalog scope and open campaign limits beside every
  coverage ledger; keep host/core authority outside presentation evidence.

## Prepare Evaluation Without Fabricating Human Evidence

- Context: Phase 10.1 technical integration was complete, while Phase 10.2
  required first-time-user, accessibility, audio, and consequence-comprehension
  evidence that was not available in the repository.
- Risk: Checking evaluation outcomes or writing plausible participant findings
  would turn a preparation artifact into an unsupported product claim.
- Resolution: Separate stable task/rating definitions from collection, finding
  classification, revision, and go/no-go authorization. Keep the revision log
  empty and prohibit identifying/private data in repository artifacts.
- Prevention: Treat human evidence as an explicit external gate; automated
  tests may verify protocol shape and blank decision state only.

## Bind Integrated Slice Checklists to Live Evidence

- Context: The first-month board, executive, resolution, replay, and audio
  surfaces were implemented across earlier slices, while Phase 10.1 retained
  an unverified feature checklist.
- Symptom: Individual tests can pass while the roadmap loses a cross-surface
  acceptance boundary or quietly gains client authority.
- Resolution: Add one deterministic acceptance ledger that asserts each exact
  technical checklist label, live mount/source marker, first-month stage path,
  visible music sequence, skip behavior, replay/hash surface, and forbidden
  authority markers.
- Prevention: Keep integration evidence separate from Phase 10.2 human
  comprehension, accessibility-quality, audio-fatigue, educational, legal,
  ownership, and review conclusions.

## Keep Roadmap Checklists Bound to Evidence

- Context: Phase 9 technical work was implemented across several slices, but
  the roadmap retained unchecked checklist items and “in progress” evidence
  statuses.
- Symptom: Stale planning text makes complete technical gates look unfinished,
  while blindly checking every item could overclaim legal, quality, or human
  review.
- Resolution: Add a focused regression test for technical evidence closure and
  record automated completion separately from explicit external review gates.
- Prevention: Update checklist status in the same PR as the implementation,
  cite concrete validators/tests/projections, and keep legal, ownership,
  decoder, accessibility, quality, portrait, and human-review limits visible.

## Keep Release Transforms Explicit and Read-Only

- Context: Phase 9.2 needed a way to remove SVG metadata after the release
  security audit began rejecting it, without turning a release check into an
  implicit canonical-asset rewrite.
- Symptom: A metadata audit can identify a problem but cannot provide a safe,
  reproducible derivative operation; an automatic rewrite could silently change
  registry hashes or release manifests.
- Resolution: Validate SVG/XML with the standard library, delete only parsed
  `<metadata>` elements into a new caller-selected derivative under an explicit
  boundary, and keep approved-release checking read-only.
- Prevention: Preserve `<title>`/`<desc>` and all other bytes, reject malformed
  input, symlinked paths, missing inputs, and output collisions, and retain
  legal, accessibility, decoder, quality, ownership, and human-review gates as
  separate evidence requirements.

## Make Human Review Explicit Without Simulating Approval

- Context: After preserving all seven portrait previews, Phase 8.2 still
  required human resemblance, accessibility, artifact, provenance, derivative,
  and registry review.
- Symptom: A boolean checklist or attractive proof can look like approval even
  when no authorized human has reviewed the candidate.
- Resolution: Add one hash-bound review packet per role with explicit gates,
  pending decision, null reviewer/release fields, written equivalents, generic
  fallbacks, and a review-only proof.
- Prevention: Keep automated validation limited to schema, binding, and
  fail-closed mechanics; never mark a gate complete or registry-safe without
  human evidence.

## Keep a Complete Preview Set Explicitly Unreleased

- Context: The second Phase 8.2 slice added the remaining six fictional actor
  portrait candidates after the first rival-system-executive preview.
- Symptom: A partial preview manifest can drift from the canonical role set,
  making a polished candidate look more complete or approved than it is.
- Resolution: Require exactly one hash-bound preview for every canonical role,
  mark the six current-slice targets explicitly, show all candidates in the
  fixture proof, and keep model/seed/review/registry gates pending.
- Prevention: Validate the role set and preview set together, test duplicate and
  missing-role failures, and maintain generic written fallbacks when previews
  are disabled or withheld.

## Keep Portrait Identity Decorative and Provenance Honest

- Context: Phase 8.2 introduced fictional actor portrait work after the local
  generation workflow was available, but the built-in preview path did not
  expose the approved local model revision or actual seed.
- Symptom: A polished portrait can imply real-person identity, score,
  severity, intent, or future outcome, and its appearance can tempt a release
  record to overstate provenance or human review.
- Resolution: Define the full seven-role contract first, preserve the first
  candidate as an explicitly unverified preview with source hash, prompt,
  accessible equivalent, and generic fallback, and keep it outside the asset
  registry, release directory, runtime GUI, and generation manifest.
- Prevention: Treat portraits as optional identity decoration, require
  small-size/grayscale and written-fallback checks, reject unknown model/seed
  provenance, and never substitute automated visual inspection for human
  resemblance, accessibility, legal, or clinical review.

## Make Generation Provenance Fail Closed

- Context: Phase 8.1 needed a local workflow for future fictional visual/audio
  assets without quietly treating a model card or an automated record as full
  legal, quality, accessibility, or human-review clearance.
- Symptom: A generated file can look complete while its model revision,
  prompt, seed, source output, hash, post-processing, accessible equivalent,
  or reviewer decisions are missing or unverifiable.
- Resolution: Keep an approved-model registry and generation manifest separate
  from the existing release asset registries; capture source/release hashes and
  explicit settings; require all review fields and a matching registry bridge
  before approved/release status; leave the manifest empty until an authorized
  asset slice supplies a preserved output.
- Prevention: Treat model-card licensing as a documented basis rather than
  blanket clearance, preserve generic/written fallbacks, reject unknown or
  mismatched records, and keep generation artifacts outside simulation,
  observation, history, replay, and debrief authority.

## Bound Audio Priority and Preserve Written Consequences

- Context: Phase 7.4 needed dense month resolutions to remain readable while
  retaining the existing optional music, ambience, and visible event cues.
- Symptom: Immediate cue playback can stack repeated reports, mask a critical
  consequence with a background layer, and leave preferences inconsistent when
  browser storage is unavailable.
- Resolution: Plan synchronous visible requests with a pure priority contract,
  select one critical cue per batch, aggregate routine requests, cap queue and
  transient voices, duck only background layers with bounded ramps, and persist
  only explicit local audio controls with safe session fallback.
- Prevention: Treat priority as ordering rather than severity, keep all visible
  text/source/status output intact, test fake timers and Web Audio voice bounds,
  and leave host, simulation, history, replay, and debrief authority untouched.

## Keep Music Contextual and Visible-Only

- Context: Phase 7.3 needed adaptive music states without turning harmony into
  a hidden score, moral judgment, or second transition authority.
- Symptom: A classifier can accidentally treat private rival activity,
  resolved inputs, or an unmodeled outcome as a musical cue; layered stems can
  also become unbounded or remove the written context when muted.
- Resolution: Store seven states and five stem roles in one pure contract,
  classify only explicit actor-visible stage/observation/report/process text,
  plan replay sequences from the same visible inputs, cap loop/crossfade
  timings, and expose music-only/full mute plus written fallbacks.
- Prevention: Preserve stable legacy state IDs, leave priority/fatigue/ducking
  to Phase 7.4, keep all stem recipes generated locally, and treat replay
  sequence checks as deterministic technical evidence rather than musical or
  learning validation.

## Keep Ambience Optional and Non-Clinical

- Context: Phase 7.2 needed environmental atmosphere for seven fictional
  settings without turning sound into a second information channel.
- Symptom: An ambience bed can imply geography, urgency, clinical severity, or
  a real institution even when the visible interface does not support that
  claim; repeated or speech-like loops can also interfere with reading.
- Resolution: Store each setting in one deterministic recipe contract with
  provenance, source-hash basis, no-speech/music/name/alarm constraints, noise
  and loudness targets, reviewed seamless-loop metadata, written equivalent,
  reduced-audio behavior, and fallback. Select only the visible regional city
  bed by default.
- Prevention: Keep setting selection explicit and presentation-only, preserve
  cues-only/mute/unavailable behavior, and document that runtime recipes have
  no release hash because no audio file is distributed.

## Put Cue Standards in One Catalog

- Context: Phase 7.1 needed to refine repeated UI/event cues without creating
  a separate uninspectable audio pipeline.
- Symptom: A cue can have a visible source and cooldown yet still drift in
  duration, level, peak, text equivalent, or distinction when each runtime
  entry carries its own partial recipe.
- Resolution: Store the 16 cue contracts in one pure catalog and decorate the
  existing generated Web Audio entries from it. Use one bounded normalization
  gain and expose cues-only mode as a local channel policy.
- Prevention: Keep cue metadata informational rather than clinical, retain
  visible/text equivalents, suppress only music/ambience in cues-only mode, and
  never let audio timestamps or classifications enter host/replay state.

## Sequence Visible Resolution Before Local Pacing

- Context: Phase 6.2 needs a first-month presentation that is easier to follow
  without making browser timing another transition authority.
- Symptom: If a client only inserts or reveals one resolution step at a time,
  skip, reduced motion, an interrupted timer, or a refresh failure can hide a
  committed report or make local order look like causal order.
- Resolution: Normalize the host-owned eight-stage envelope into a pure
  storyboard, render every stage and source immediately, and use local controls
  only to emphasize an existing stage. Unknown stages and missing data retain
  explicit written fallbacks.
- Prevention: Keep priority display-only, map/report/metric synchronization as
  metadata, cue IDs optional, and replay/skip tests focused on text retention;
  never infer severity, causality, or hidden rival state from pacing.

## Specify Motion Before Scheduling Motion

- Context: Phase 6.1 needs consequence animation to aid comprehension without
  letting client timing become a second transition authority.
- Symptom: Unbounded animation can block input, reveal hidden information,
  reorder replay, or make reduced-motion users lose the written consequence.
- Resolution: Define each category’s semantic purpose, timing, replacement,
  interruption, replay, input, and load rules in one pure catalog; prove the
  policy with planned events rather than timers.
- Prevention: Keep motion supplementary, keep exact text in the DOM, cap
  simultaneous effects, and treat local performance smoke results as budgets
  rather than hardware or usability claims.

## Visualize Supplied Metrics Without Inventing Precision

- Context: Phase 5.2 needs small visuals that make visible constraints easier to
  scan while the model may provide missing, stale, categorical, or uncertain
  values.
- Symptom: Normalizing every metric to a percentage or numeric trend can imply
  precision, comparability, probability, or hidden state that the host did not
  provide.
- Resolution: Use one catalog with per-form precision, uncertainty,
  missingness, exact-text, color-independent, and large-text rules; render only
  when an actor-visible metric descriptor explicitly supplies a visualization.
- Prevention: Keep exact text and source/status beside every SVG, leave missing
  periods visible, use patterns/labels/shapes as equivalents, and snapshot the
  deterministic proof output.

## Differentiate Containers Without Hiding Evidence

- Context: Phase 5.1 needs the executive desktop to distinguish information
  classes while retaining dense source-linked text and accessibility fallbacks.
- Symptom: Color-only panel styling or compact cards can fragment the shared
  grid, imply unsupported priority, or hide exact values at narrow/large-text
  sizes.
- Resolution: Use one catalog for structural header, non-color marker,
  compact/expanded, large-text, narrow-width, print, reduced-motion, and
  source/status rules; apply restrained classes to the existing semantic panels.
- Prevention: Change hierarchy and structure before decoration, keep all text in
  the DOM, and test the proof at compact, expanded, responsive, print, and
  reduced-motion states.

## Link Consequences Only When the Host Names the Target

- Context: Phase 4.2 connects regional reports, board entities, resolution
  effects, and replay review without changing host authority.
- Symptom: A client-side metric/source match can look like a causal or spatial
  link even when the host did not identify the affected actor or facility.
- Resolution: Regional signals/processes use explicit visible entity IDs;
  resolution effects remain targetless unless a host-provided target exists;
  deterministic links retain source, observed month, turn, and state hash.
- Prevention: Treat focus as local navigation, preserve the semantic report
  fallback, and never infer private rival detail, project outcome, causality, or
  target identity from text alone.

## Keep the Semantic Board as the Fallback

- Context: Phase 4.1 integrates a graphical SVG board with an existing typed
  regional-world projection and semantic map/detail panels.
- Symptom: A visual board can look like a replacement surface while dropping
  source labels, missingness, keyboard reachability, or the existing selection
  contract.
- Resolution: Map DTO fields through a pure adapter, mount SVG beside the
  semantic surface, route both paths through one local selection state, and
  preserve explicit status/source/missingness text plus a deterministic SVG
  snapshot.
- Prevention: Treat the graphical board as an additional projection of the
  actor-visible DTO; never let local focus become simulation state or hide the
  semantic fallback.

## Make Overlay Priority Explicitly Non-Semantic

- Context: Phase 3.3 requires deterministic ordering and collision behavior for
  multiple operational overlays while the host remains the authority for
  visible fields and outcomes.
- Symptom: A high display priority or a stacked card can be read as hidden
  urgency, severity, causality, or strategic importance.
- Resolution: Each overlay records `severity_encoding: "none"` and a
  display-only priority rule; bounded layout preserves visible overflow as an
  explicit count and stable-ID tie-breaks.
- Prevention: Treat priority as a rendering constraint, not a model signal;
  keep trigger fields, text equivalents, and unknown fallbacks adjacent to
  every semantic overlay token.

## Complete Symbolic Map Vocabulary Before Board Integration

- Context: Event markers and viewport interaction were the final explicit
  Phase 3.2 map/environment contracts after grid, roads, districts, parcels,
  relationships, service areas, and uncertainty were proven separately.
- Symptom: A board proof can appear complete while missing marker categories,
  target-size behavior, keyboard order, or bounded viewport recovery.
- Resolution: Composed one fixture proof from the shared catalogs, declared
  target viewports and focus order, clamped zoom/pan locally, and kept every
  marker static, text-equivalent, and severity-free.
- Prevention: Close the reusable vocabulary and its interaction contract in
  fixture space before introducing live host projection or custom board logic.

## Keep Uncertainty Status Separate From Hidden Severity

- Context: Uncertainty overlays needed stale, missing, and revised vocabulary
  before live intelligence or consequence rendering was modeled.
- Symptom: Hatching, emphasis, or a “revised” label can imply hidden risk,
  severity, probability, truth, or future outcome that is not visible.
- Resolution: Used deterministic non-color patterns with no severity encoding,
  static reduced-motion behavior, written equivalents, a generic fallback, and
  an explicit information boundary.
- Prevention: Treat uncertainty as an explicit visible information-status field;
  never turn uncertainty styling into an unobserved risk scale.

## Keep Service-Area Overlays Separate From Catchment Claims

- Context: Service-area overlays needed reusable contour vocabulary before
  geographic or operational map semantics were modeled.
- Symptom: A contour, hatch, or “primary area” label can imply catchment,
  distance, travel time, population, access, jurisdiction, or performance that
  is not visible.
- Resolution: Used deterministic symbolic contour/fill patterns with no metric
  or direction encoding, written equivalents, a generic fallback, and an
  explicit information boundary.
- Prevention: Treat service areas as relationship vocabulary until a scenario
  explicitly supplies geographic or operational semantics.

## Keep Relationship Lines From Becoming Causal Claims

- Context: Relationship-line styles needed to distinguish visible categories
  before relationship instances or live map rendering were modeled.
- Symptom: Arrows, line weight, or a “service” label can imply hidden intent,
  causality, strength, direction, distance, or future outcome that is not
  visible.
- Resolution: Used deterministic non-color patterns with round caps, no
  arrowheads, a generic fallback, written equivalents, and an explicit
  information boundary.
- Prevention: Keep relationship style vocabulary non-directional; permit
  direction or causal meaning only when an actor-visible instance contract
  explicitly supplies it.

## Keep Parcel Tokens Separate From Ownership and Future Use

- Context: The parcel system needed reusable facility and undeveloped-land
  placement vocabulary before projects or overlays were modeled.
- Symptom: A parcel boundary, footprint, or open-area mark can imply ownership,
  availability, development potential, land value, zoning, geography, or
  future use that is not visible.
- Resolution: Used deterministic symbolic parcel tokens with non-color
  patterns, written equivalents, a generic fallback, and an explicit
  non-claim boundary.
- Prevention: Treat parcels as placement vocabulary until a scenario explicitly
  supplies ownership, land-use, or project semantics.

## Keep District Tokens Separate From Land-Use Claims

- Context: The district tile set needed reusable commercial, residential,
  employer-center, and government vocabulary before parcels or overlays were
  modeled.
- Symptom: A district label, block pattern, or civic mark can imply real-world
  land use, population, ownership, zoning, travel time, or jurisdiction that
  is not visible.
- Resolution: Used deterministic symbolic district tokens with non-color
  patterns, written equivalents, a generic fallback, and an explicit
  non-geographic boundary.
- Prevention: Treat districts as presentation vocabulary until a scenario
  explicitly supplies geographic or institutional semantics.

## Keep Road Tokens Separate From Travel Claims

- Context: The road tile set needed reusable segments before intersections and
  districts were modeled.
- Symptom: Orientation, centerlines, or a road label can imply travel time,
  traffic, capacity, jurisdiction, or real-world geometry that is not visible.
- Resolution: Used deterministic symbolic path tokens with written roles and a
  generic fallback, plus an explicit non-geographic boundary.
- Prevention: Treat roads as presentation vocabulary until scenarios provide
  geographic or operational semantics explicitly.

## Make Symbolic Map Coordinates Explicit

- Context: Phase 3.2 needed a reusable map coordinate system before adding
  roads, districts, or relationships.
- Symptom: A grid can quietly suggest real distance, jurisdiction, travel time,
  or geographic truth if its meaning is not stated.
- Resolution: Defined a deterministic 24px fixture grid with named coordinates,
  a pure conversion helper, and an explicit non-geographic disclaimer.
- Prevention: Treat map placement as presentation vocabulary until a scenario
  explicitly supplies geographic semantics.

## Keep Parcel Boundaries From Becoming Future-Use Claims

- Context: The undeveloped-parcel component needed to organize a board without
  asserting what the land will become or who controls it.
- Symptom: A parcel boundary or “undeveloped” label can imply development
  potential, ownership, availability, or a forecast that is not visible.
- Resolution: Used a dashed boundary as a type-only cue and tested explicit
  non-claim wording for potential, ownership, and future use.
- Prevention: Keep land vocabulary symbolic and route future projects through
  visible project and uncertainty layers only.

## Keep Construction Cues Separate From Project Status

- Context: The construction-crane component needed a recognizable boom and
  tower while project status is supplied by a separate visible layer.
- Symptom: A crane can be read as proof that work is active, complete, funded,
  or successful even when no such field is present.
- Resolution: Used the crane as a type-only cue and tested explicit non-claim
  wording for project status and completion.
- Prevention: Keep base geometry descriptive and make project meaning explicit
  through the shared project and uncertainty layers.

## Keep Education Symbols From Becoming Outcome Claims

- Context: The research-and-education-building component needed a recognizable
  wing-and-tower form while research and education outcomes are not encoded by
  a fixture shape.
- Symptom: A tower, building name, or study-like geometry can be read as proof
  of research quality, educational effect, or capacity that is not visible.
- Resolution: Used the geometry as a type-only cue and tested explicit
  non-claim wording for research, education, and capacity.
- Prevention: Keep institutional building cues descriptive and route outcome
  meaning through visible status layers with written equivalents.

## Keep Infrastructure Symbols From Becoming Reliability Claims

- Context: The utility-plant component needed a recognizable pipe-and-tank
  silhouette while reliability, safety, and service are not encoded by a
  fixture shape.
- Symptom: Pipes, tanks, or a plant label can be read as operational assurance
  or risk evidence that is not an actor-visible field.
- Resolution: Used the infrastructure geometry as a type-only cue and tested
  explicit non-claim wording for reliability, safety, and service.
- Prevention: Keep support-infrastructure illustrations descriptive and route
  operational meaning through visible layers with written equivalents.

## Keep Parking Geometry Separate From Availability Claims

- Context: The parking-structure component needed a recognizable stacked-deck
  cue while parking availability and access are not encoded by the fixture.
- Symptom: Deck count, arrows, or a parking label can be read as occupancy,
  accessibility, or service-availability evidence that is not visible state.
- Resolution: Used tier lines and ramps as a type-only cue and tested explicit
  non-claim wording for parking availability and access.
- Prevention: Treat support-facility geometry as vocabulary only; keep capacity,
  pressure, and uncertainty in visible layers with written equivalents.

## Keep Administrative Type Cues From Becoming Authority Claims

- Context: The administrative-headquarters component needed an office-like
  silhouette while the simulation does not expose institutional authority or
  performance from a facility shape.
- Symptom: A stepped office form or headquarters label can imply control,
  legitimacy, effectiveness, or ownership that is not an actor-visible field.
- Resolution: Used the stepped silhouette as a type-only cue and tested explicit
  non-claim wording for authority and performance.
- Prevention: Keep administrative vocabulary tied to visible facility kind and
  require accessible descriptions to state the limit of the cue.

## Avoid Letting “Rural” Become a Geographic Claim

- Context: The rural-clinic component needed a recognizable compact roof cue
  while the roadmap treats geography as symbolic unless modeled explicitly.
- Symptom: A facility label or illustration can imply real distance, access,
  service quality, or community conditions that are not visible fields.
- Resolution: Kept the pitched roof as a type-only cue and tested explicit
  non-claim language for access and quality.
- Prevention: Treat regional/facility descriptors as fictional vocabulary and
  keep geographic meaning in host-provided visible data only.

## Keep Modular Type Cues Distinct Without Expanding Claims

- Context: The specialty center needed a third compact geometry after the
  low-rise ambulatory center and emergency entrance wing.
- Symptom: A stronger shape cue can be mistaken for a claim about clinical
  scope or capacity.
- Resolution: Used a peaked canopy as a type-only marker, with explicit written
  non-claim language and the shared seven-layer boundary.
- Prevention: Vary geometry for recognition while keeping every accessible
  description and layer source tied to visible fields.

## Distinct Geometry Must Keep Type Claims Narrow

- Context: The ambulatory center needed a low-rise visual distinction from the
  general hospital, patient tower, and emergency department.
- Symptom: A compact type cue can accidentally sound like a performance or
  throughput claim when reused in a report or screen-reader description.
- Resolution: Kept the arc silhouette as a type-only cue, retained all written
  layer labels, and tested the explicit non-claim description.
- Prevention: Describe what a facility shape identifies and explicitly state
  what it does not establish before release.

## Keep Facility Type Descriptions Within the Information Boundary

- Context: An emergency-department release description needed to explain its
  entrance-wing shape for non-visual users.
- Symptom: Calling a type silhouette a “capacity cue” could make accessible
  text imply unsupported service performance.
- Resolution: Described the mark as a type cue only and added a regression test
  for the explicit non-claim wording.
- Prevention: Review accessible descriptions for implied facts, not only for
  missing labels or color alternatives.

## Reuse the Layer Contract Across Facility Types

- Context: The patient tower shares consequence layers with the general
  hospital but needs a visibly distinct silhouette.
- Symptom: A second proof page could drift in fallback, source labels, or
  non-color behavior while appearing visually complete.
- Resolution: Extended one catalog/proof selector with the patient tower and
  kept the same seven layer IDs, written equivalents, registry fields, and
  generic fallback.
- Prevention: Add new facility types as data against the established layer
  contract before creating another rendering path.

## Make Facility Layers Composable Before Adding More Buildings

- Context: Phase 3.1 needs many facility types and several visible consequence
  layers without one-off illustrations for every state.
- Symptom: A single finished building illustration can hide missing identity,
  project, pressure, uncertainty, or accessibility contracts.
- Resolution: Proved the general-hospital base as one source/release pair with
  seven named layers, shared grid/color variables, written equivalents, and a
  generic fallback.
- Prevention: Complete the layer contract on one reusable component before
  expanding the library to new facility types.

## Give Actor Families One Shared Vocabulary

- Context: Phase 2.2 needs eight recurring actor families to remain distinct
  across reports and notifications without eight bespoke proof pages.
- Symptom: Independent family assets would make labels, fallbacks, and
  color-independent cues drift between institutional sources.
- Resolution: Stored glyph, frame, notification, optional identity-sonic tag,
  source, and written equivalent in one catalog consumed by one proof page.
- Prevention: Add families as data to the shared language contract, and test
  unknown IDs before promoting any family treatment into runtime UI.

## Finish the Identity Matrix Before Cross-Screen Promotion

- Context: Phase 2.1 spans three recurring systems and the same map, facility,
  report, compact, and audio surfaces.
- Symptom: Promoting one polished system early could make the shared GUI path
  imply incomplete or inconsistent identity coverage.
- Resolution: Kept Riverside, Northlake, and Summit in explicit roadmap lanes,
  completed each through the shared proof, and retained generic fallback.
- Prevention: Close the full identity matrix in fixture space before promoting
  identity assets into live cross-screen rendering.

## Reuse the Surface Contract While Varying Identity Vocabulary

- Context: Northlake needed a distinct kit without creating a second proof
  architecture or weakening the Riverside fallback contract.
- Symptom: Copying a whole proof page per system would allow accessibility,
  provenance, and cross-surface rules to drift.
- Resolution: Added Northlake data/assets to the shared identity catalog and
  selector, while keeping its geometry, palette, labels, and motif distinct.
- Prevention: Reuse the tested surface contract and generic fallback; vary only
  the fictional vocabulary and registry-backed assets.

## Keep Identity Kits Surface-Complete Before Runtime Promotion

- Context: Phase 2.1 requires one fictional system to persist across map,
  facility, report, event, and audio surfaces.
- Symptom: A logo-only asset could look finished while missing monochrome,
  signage, report, compact, fallback, or provenance behavior.
- Resolution: Added a Riverside source/release kit, static cross-surface proof,
  generic fallback, and registry/hash coverage before live GUI integration.
- Prevention: Complete and test every identity surface for each system before
  promoting shared identity tokens into runtime rendering.

## Keep Audio Policy Local Until the Vocabulary Is Accepted

- Context: The direction board needed priority, cooldown, and preference
  behavior before any live audio integration could be justified.
- Symptom: Putting scheduler policy into the live client first could couple
  unreviewed sound semantics to host timing or make muted states incomplete.
- Resolution: Added a fixture-local policy with explicit priority, ducking,
  cooldown, modes, and reduced-audio filtering; every result retains text.
- Prevention: Promote policy to the live client only through a separately
  reviewed host-independent integration slice with calibrated evidence.

## Define Audio Direction Before Adding Playback Policy

- Context: The existing browser audio client had a broad oscillator catalog but
  no reviewed vocabulary for cue contour, ambience, identity, or pressure.
- Symptom: Adding priority or mode behavior first could make a technically
  correct scheduler amplify an unreviewed or hidden-state signal.
- Resolution: Added a fixture-only recipe board with explicit source,
  equivalent, loudness, peak, duration, loop, ducking, and masking targets.
- Prevention: Review and test the semantic sound vocabulary first; add runtime
  priority, cooldown, mute modes, and preferences only in a separate slice.

## Keep Rendering Proofs Fixture-Only Until the Scene Contract Is Stable

- Context: The selected visual direction needed a concrete viability test, but
  the live GUI already has an authoritative host adapter and presentation path.
- Symptom: Integrating a new renderer early could create a parallel scene model,
  hidden-state inference, or browser-owned geography.
- Resolution: Added a pure fixture-driven SVG renderer and keyboard proof page
  with snapshot, fallback, boundary, and performance tests; the live route is
  unchanged.
- Prevention: Prove scene semantics and accessibility equivalents in isolation,
  then promote only a justified host projection in a separate slice.

## Resolve Visual Style Before Building Asset Breadth

- Context: The roadmap offers both map-like and dashboard-like visual paths
  before a renderer or facility library exists.
- Symptom: Choosing an attractive motif without a scored comparison can imply
  unsupported geography or flatten the game into a generic dashboard.
- Resolution: Committed three labeled SVG references, scored strategic clarity,
  accessibility, reuse, tone, and implementation risk, then selected the flat
  institutional direction through an ADR.
- Prevention: Keep rejected variants as evidence, select one vocabulary before
  renderer/facility production, and label schematic layout as non-geographic.

## Put Provenance Checks Before Asset Production

- Context: The visual/audio roadmap separates generated runtime recipes from
  future distributable SVG, raster, and audio files.
- Symptom: A catalog or credits file can look complete while a future release
  file has no stable ID, source hash, license, fallback, or approval record.
- Resolution: Added separated source/generated/release paths, manifests with
  semantic and accessibility metadata, fail-closed hash/license/coverage
  validation, and deterministic credits before adding new production assets.
- Prevention: Treat registry validation and credits freshness as the gate for
  every later asset slice; keep runtime-generated recipes registered even when
  they have no release file.

## Give Presentation Semantics Their Own Contract

- Context: Future visual/audio work needs domain-specific coordination, but the
  existing harness routed all project work through evidence and simulation
  mechanism artifacts.
- Symptom: A GUI or audio task could either skip project boundaries or misuse a
  mechanism design as a presentation specification, obscuring host sources,
  accessibility equivalents, and asset provenance.
- Resolution: Added a selective presentation producer-reviewer track with an
  actor-visible source ledger and a separate presentation QA handoff.
- Prevention: Route presentation work through its own contract; invoke policy
  mechanism design only when simulation semantics or domain claims also change.

## Migrate Document Paths From a Frozen Manifest

- Context: Moving 136 top-level documents affected current guides, historical
  evidence, Markdown links, path strings, Python audits, tests, scenarios, and
  old workspace handoffs.
- Symptom: Direct string replacement updates root-relative paths but breaks
  sibling links inside files that move to different directory depths; assembled
  path constants can also escape ordinary searches.
- Resolution: Classified every source path first, resolved relative Markdown
  links from each file's former location, updated plain references from the same
  manifest, and added a tracked-Markdown link check to CI.
- Prevention: For future documentation moves, freeze an old-to-new manifest,
  migrate relative and plain references separately, search constructed path
  consumers, and run the link checker before broader tests.

## Test the Shipped GUI Transport, Not Only Injected Adapters

- Context: The browser source had complete mocked launch/action contracts, but
  a normal checkout supplied no adapter that a browser could use.
- Symptom: The page rendered demo data while Start reported that a host adapter
  was missing; all focused tests still passed.
- Cause: Tests injected fake adapters and the first-month audit explicitly
  excluded browser transport, while the real Rust host used stdio MCP.
- Resolution: Added a loopback-only GUI host, same-origin adapter, real transport
  test, and player instructions that distinguish live and static modes.
- Prevention: Every player-facing launch control must have one documented
  shipped command and an integration test crossing its real process/transport
  boundary.

Use this file to record practical lessons that would save future contributors or
agents meaningful time. Keep entries factual, concise, and tied to prevention.

## Close Presentation Tracks With Scope-Matched Audits

- Context: After thirteen visual/audio slices, the source and focused tests
  covered the bounded first-month experience, but `SPEC.md` still described it
  as incomplete.
- Symptom: A stale Future heading made it unclear whether another runtime
  feature was required and could encourage unsupported GUI expansion.
- Resolution: Added a deterministic source/test contract audit with explicit
  evidence paths, boundary exclusions, provenance checks, and claim limits;
  then closed only the bounded technical sequence in the active spec.
- Prevention: Before promoting another presentation mechanism, run the audit,
  reconcile phase docs and merge state, and preserve human-evaluation and asset
  production as separate gates.

## Make Graphical Commands Host-Shaped

- Context: Phase 3 needed to remove CLI syntax friction while preserving the
  existing competitive command and transition contracts.
- Symptom: Rebuilding enum lists, numeric bounds, or costs in the browser would
  create a second legality engine and make previews drift from the host.
- Resolution: The host supplies catalog templates and validates the complete
  canonical batch; local draft edits invalidate prior validation, and submit is
  gated on an unchanged valid response.
- Prevention: Keep browser interaction state reversible and presentation-only;
  derive costs and legality from the parser/validator boundary and test invalid
  validation and rejected submission as non-mutating paths.

## Make Static Interfaces Useful Without Making Them Authoritative

- Context: Phase 1 needed to expose finance, workforce, capacity, access, and
  public rival context before live presentation DTOs were justified.
- Symptom: Reusing a raw observation list alone preserved authority but left a
  reviewer searching through CLI-shaped text; adding local rules would create a
  second engine.
- Resolution: Added a display-only fixture, source labels, responsive semantic
  panels, selection-only navigation, and adapter-owned command entry.
- Prevention: Improve information architecture with injected actor-visible data
  first; keep selection and preview state local and reserve validation,
  transition, and outcome logic for the host boundary.

## Keep Resolution Presentation Derived From History

- Context: Phase 4 needed to make one committed competitive month legible after
  graphical action submission without creating a second outcome engine.
- Symptom: A browser timeline could appear causal while silently recomputing
  operations, revealing hidden state, or hiding result text behind animation.
- Resolution: Added a host-derived resolution envelope with actor-visible
  before/after snapshots, committed event/effect source labels, historical hash
  metadata, and local-only pacing. All textual steps are rendered immediately.
- Prevention: Treat resolution as a read of immutable history; label direct
  committed effects separately from presentation comparisons, keep skipped and
  reduced-motion views complete, and never infer a causal graph in the client.

## Make Audio Optional and Source-Traceable

- Context: Phase 5 needed restrained feedback for the visible action/resolution
  loop without turning sound into a hidden score or an asset-governance detour.
- Symptom: Audio can leak private state, make muted play incomplete, fatigue
  repeated sessions, or silently introduce unlicensed files and network paths.
- Resolution: Used generated Web Audio recipes, a visible-only classifier,
  independent channels, focus/reduced-notification/mute fallback, cooldowns,
  recording-sink events, and a registry/credits record with no third-party
  assets.
- Prevention: Keep every cue paired with visible text/status, record provenance
  before adding files, start audio only after a gesture, and treat playback as
  client state that never enters transitions, hashes, or replay history.

## Close Presentation Gates Before Adding DTOs or Assets

- Context: The visual/audio proposal listed a broad GUI, audio, and asset track,
  while the current repository had only an injected-data thin-client proof.
- Symptom: Starting with typed DTOs or decorative assets would blur the host
  authority boundary and make later source gaps harder to audit.
- Resolution: Closed Phase 0 with a source inventory, one-month contract,
  wireframe, visible-only cue catalog, and license policy before implementation.
- Prevention: Treat technology, source ownership, hidden-state exclusions, and
  promotion gates as deliverables before adding presentation runtime code.

## Keep Release Checks Read-Only and Metadata-Scoped

- Context: The final release-readiness queue item called for one lightweight
  quality check before any packaging or publication work.
- Symptom: A release helper can quietly expand into registry, tag, or deployment
  automation and make local verification harder to reproduce.
- Resolution: Added one dependency-free checker for package-version projections,
  documented the same local command, and ran it in CI without touching runtime
  code or external services.
- Prevention: Keep early release checks read-only, compare only documented
  metadata, and require a separate authorized slice for publication workflows.

## Keep Schematic Maps Actor-Visible

- Context: Phase 6 needed a persistent regional view without turning the GUI
  into a second geography or rival-state simulation.
- Symptom: Reusing true system objects for map cards would expose private rival
  operations and make display positions look like unsupported geography.
- Resolution: Added an additive host projection with owned player detail,
  lagged public rival signals, explicit source/missingness fields, and
  deterministic layout slots that the browser treats as presentation only.
- Prevention: Test serialized output for hidden fields, preserve the existing
  observation lag, label public timing, and leave the base presentation intact
  when the optional regional adapter is empty or unavailable.

## Keep Campaign Semantics in Shared UI

- Context: Phase 7 needed one browser route to cover stabilization and regional
  affiliation without turning either campaign into a generic dashboard.
- Symptom: A universal stage or score model would erase stabilization's
  onboarding loop and affiliation's partner, obligation, and stakeholder
  distinctions; local command templates would also create a second legality
  engine.
- Resolution: Added one host-owned `campaign-coverage-v1` envelope with shared
  rendering primitives, campaign-specific stage/actor/process/decision data,
  source labels, and canonical command templates. The browser substitutes only
  host-provided values and treats rejection as a non-mutating recoverable state.
- Prevention: Share presentation structure, not simulation meaning; test each
  campaign's visible distinctions, hidden-field exclusions, command equivalence,
  history/replay continuity, and complete text/audio fallback independently.

## Close Breadth Only With Scope-Matched Evidence

- Context: The breadth queue offered several attractive expansion directions,
  while the current competitive campaign already had multiple bounded tradeoffs.
- Symptom: Treating a broad queue label as permission for a new actor or patient
  model would expand scope without a demonstrated gameplay or learning need.
- Resolution: Audited the existing source boundaries and committed playtest
  artifacts, then removed the queue item while preserving public-payer, patient,
  actor, and equilibrium limits plus a concrete reopening condition.
- Prevention: Inventory implemented mechanisms first; require a concrete
  unexplained gap before adding state, actors, outcomes, or abstractions.

## Keep GUI Proofs Thin and Adapter-Owned

- Context: The GUI Future item called for one surface consuming existing game
  outputs without weakening core inspectability.
- Symptom: A browser prototype could accidentally duplicate command parsing,
  transitions, hidden state, or external asset/network assumptions.
- Resolution: Implemented rendering plus an injected `submitTurn` adapter,
  empty-input checking only, no external assets, and static contract tests; the
  unavailable browser backend was recorded as a verification limit.
- Prevention: Keep GUI state presentation-only, make the server authoritative,
  audit assets/network calls, and separate visual verification limits from user
  usability claims.

## Synchronize Queue Text With Completed Runtime Proposals

- Context: The v0.12.7 affiliation proposal was complete, but the related
  affiliation/acquisition item remained in the Future queue.
- Symptom: A stale queue entry could imply that a new runtime mechanism was
  still required and encourage scope expansion.
- Resolution: Revalidated the six contracts and 9-run/54-stage artifact, then
  removed the queue item while preserving broader acquisition deferral and a
  reopening condition.
- Prevention: After a proposal closes, audit all queue references and either
  remove the completed item or explicitly route it to a new evidence gap.

## Separate Pressure Evidence From Tuning Authorization

- Context: The v0.12.4 review found workforce-capacity counts rising across
  tested difficulty tiers, and v0.12.6 made the typed context visible.
- Symptom: A monotonic simulated signal could be mistaken for a causal balance
  diagnosis or general Expert winnability result.
- Resolution: Closed the queue item only after confirming exact observation
  controls, 15/15 named Expert clearability overlap, source-version limits, and
  no unexplained gap; no runtime values changed.
- Prevention: Treat descriptive pressure as routing evidence, require a new
  unexplained gap for tuning, and preserve clearability and provenance limits.

## Remove Completed Queue Items Without Making Learning Claims

- Context: The v0.12.3 cross-campaign teachability review had already found no
  structural gap, but its Future queue entry remained active text.
- Symptom: Leaving the item in the queue obscured the actual next work, while
  promoting trace coverage as learner evidence would overstate the result.
- Resolution: Added a closure artifact with source-specific coverage, 18 runs,
  270 transitions, and zero gaps; removed the item and recorded a concrete
  reopening condition without changing runtime behavior.
- Prevention: Close queue entries only with scope-matched evidence and preserve
  explicit limits and reopening criteria.

## Reconcile Runtime Proposals Before Adding Another Mechanism

- Context: The v0.12.7 SPEC item called for a separate affiliation runtime
  proposal, while ADR-0010 and the v0.12.0 implementation already supplied
  that boundary.
- Symptom: Treating the queue text as an unimplemented feature would duplicate
  runtime scope and risk expanding the actor model unnecessarily.
- Resolution: Audited source markers and the committed 9-run/54-stage artifact
  across state, observations, resolved inputs, transitions, replay, and debrief;
  closed the queue item as an existing-runtime confirmation with no new code.
- Prevention: Before promoting a Future item, reconcile SPEC, ADRs, runtime
  ownership, and committed evidence; authorize new runtime only for a concrete
  unexplained gap.

## Prove Observation-Only Changes With Immutable Transition Controls

- Context: v0.12.5 identified safe typed workforce fields that were absent from
  the competitive MCP observation.
- Symptom: A presentation fix could appear harmless while accidentally changing
  simulation behavior or actor-visible scope.
- Resolution: Added only formatter lines and a boundary test, then replayed the
  75-run/1,800-transition compatibility matrix against immutable all-tier and
  Expert artifacts; every history and state-hash sequence matched exactly.
- Prevention: For observation-boundary changes, count every rendered trace,
  compare complete histories as well as hashes, and assert excluded hidden
  markers remain absent before considering the gap closed.

## Separate Pressure Signals From Their Decision-Time Context

- Context: The v0.12.4 workforce-capacity signal was visible in operating
  consequences, but the MCP formatter omitted typed staffing and capacity
  counts that could help interpret it before a command.
- Symptom: Trust labels, labor guidance, and debrief attribution were present,
  while the numeric staffing/capacity context was absent from the player view.
- Resolution: Defined an observation-only follow-up from `PlayerObservation` and
  explicitly excluded targets, effective allocations, future hires, and rival
  private state.
- Prevention: Audit typed-vs-rendered fields after identifying a mechanism signal;
  route omissions to the owning presentation boundary before changing balance or
  difficulty values.

## Treat Difficulty Signals as Routing Evidence

- Context: The v0.12.4 review compared existing all-tier and standalone Expert
  artifacts before any difficulty tuning.
- Symptom: Workforce-capacity bottleneck counts rose from 0 Easy to 160 Expert,
  while Normal, Hard, and Expert scripted action counts were identical.
- Resolution: Reported workforce capacity as a candidate visible pressure signal
  and kept it behind a separate design gate; Expert completion remained a
  bounded clearability proxy for named profiles and seeds.
- Prevention: Recompute pressure from committed events/effects, preserve source
  versions, and never translate monotonic simulated counts into causal balance,
  winnability, or human-perceived difficulty claims.

## Compare Evidence Lanes Without Flattening Campaign Semantics

- Context: The v0.12.3 Phase 7 review joined the v0.12.2 affiliation post-fix
  artifact with the approved v0.11.12 competitive teachability capture.
- Symptom: Both lanes expose decision, transition, outcome, and debrief records,
  but their stage/month units and context vocabulary differ.
- Resolution: Used a shared structural audit with source-specific context and
  debrief markers, preserving pinned source versions and reporting 18 runs and
  270 transitions without a new capture.
- Prevention: Normalize only audit metadata. Keep campaign-specific contracts
  explicit, and never turn deterministic trace coverage into a comprehension,
  balance, winnability, or learning claim.

## Isolate Tests That Share User-Scoped Files

- Context: CI ran persistence tests in parallel against the shared
  `competitive_session.save` path.
- Symptom: A delete-idempotency test could remove the file while a round-trip
  test was loading it, producing a missing-file failure that serial tests hid.
- Resolution: Added a test-module mutex around the shared-path tests without
  changing production persistence behavior.
- Prevention: Run the default parallel test command before handoff and isolate
  tests that mutate user-scoped filesystem paths.

## Audit Typed Observations Against Rendered Interfaces

- Context: The v0.12.1 regional-affiliation capture compared the typed
  `AffiliationObservation` with the MCP observation lines used by scripted
  policies.
- Symptom: The runtime retained alternatives, assumptions, and commitments,
  but the player-facing MCP rendering omitted them while the debrief later
  asked the player to compare alternatives.
- Resolution: Recorded the structural gap in v0.12.1, then rendered only the
  existing safe typed fields through the MCP boundary in v0.12.2 without
  changing transitions, rulesets, or replay/hash contracts.
- Prevention: When validating a new campaign, compare the typed observation
  fields with every rendered CLI/MCP surface before making balance or learning
  claims; keep omitted fields as an interface slice rather than leaking hidden
  state into the player view.

## Keep New Campaign Contracts Separate from Competitive Golden Paths

- Context: The regional affiliation slice needed new state, inputs, replay, and
  debrief behavior while the competitive campaign has a frozen seed-42 contract.
- Resolution: Kept affiliation state, canonical hashing, replay artifact version,
  scenario fields, and transition modules campaign-specific; only the campaign
  router and shared interface surfaces were extended.
- Prevention: Before sharing a new field or hash schema, prove that it is truly
  campaign-neutral. Otherwise add a narrow typed boundary and regression-test the
  unchanged golden path.

## Consolidation Design Must Precede Consolidation Runtime

- Context: The next roadmap candidate after the v0.11.12 validation checkpoint
  was regional affiliation/acquisition work.
- Resolution: Narrowed the first slice to one affiliation-first design gate and
  kept acquisition, runtime state, legal outcomes, and transaction finance out
  of scope.
- Prevention: Require evidence mapping, explicit actor/observation boundaries,
  domain QA, and debrief contracts before promoting any consolidation mechanic
  into `SPEC.md` Present or runtime code.

## Current-Code Teachability Captures Should Reuse Policy and Retry Contracts

- Context: The v0.11.12 continuation needed current-code observation and pacing
  evidence after the broader v0.11.11 all-tier matrix.
- Resolution: Reused the historical observation-driven policy and retry-aware
  MCP boundary while adapting only the versioned artifact and audit contract.
- Prevention: Keep historical evidence immutable, preserve rejected-command
  metadata, and use a focused profile/seed matrix when the active question is
  teachability rather than difficulty breadth.

## Re-run the Full Matrix After Difficulty Changes

- Context: The v0.11.9 Expert capture and v0.11.10 source synthesis did not
  establish current all-tier behavior after the v0.11.7 risk-posture and v0.11.8
  rival-resource changes.
- Resolution: Reran the five-profile, three-seed, four-tier matrix on current
  code and audited 1,440 committed months while preserving the Normal hold
  control hash.
- Prevention: Do not infer current all-tier clearability or trajectory behavior
  from a pre-change matrix plus an Expert-only post-change capture.

## Preserve Source-Specific Evidence Contracts

- Context: The v0.11.10 synthesis combined the v0.11.6 strategy audit with the
  v0.11.9 Expert capture, which expose different trace shapes and metadata.
- Resolution: Validated each artifact independently and summarized only shared
  coverage facts without normalizing raw evidence into a new schema.
- Prevention: Treat cross-artifact continuity as a source-boundary audit; do not
  infer causal outcome comparisons or shared fields that a source does not declare.

## Revalidate Expert After Difficulty Surface Changes

- Context: The v0.11.7 and v0.11.8 slices changed AI risk posture and rival
  starting resources, so older Expert clearability evidence no longer covered
  the current difficulty surface.
- Resolution: Ran a fresh Expert-only matrix over five deterministic policy
  lanes and three named seeds while preserving the Normal seed-42 control hash.
- Prevention: Treat difficulty changes as needing post-change clearability
  evidence before claiming Expert remains severe but playable; do not tune
  balance from a completion matrix alone.

## Compare Strategy Traces Across the Latest Frozen Matrix

- Context: The v0.11.6 continuation needed to test whether the v0.11.5
  operating-outcome evidence supported profile-level strategy comparison.
- Resolution: Reused the latest frozen v0.11.4 capture, composed the existing
  observation/debrief contract, and grouped traces by profile, seed, and
  difficulty without launching new sessions or changing runtime behavior.
- Prevention: Treat trajectory and signal-response differences as descriptive
  evidence only; require a concrete unexplained product or domain gap before
  promoting runtime work.

## Re-run Evidence After a Debrief Surface Fix

- Context: The v0.11.2 audit identified 469 operating signal-months with no
  month-specific outcome line, and v0.11.3 added the missing player-owned
  debrief output.
- Resolution: Re-ran the unchanged five-profile, three-seed, four-difficulty
  matrix and audited 1,440 monthly sections instead of treating focused report
  tests as complete evidence.
- Prevention: Keep post-fix matrix validation separate from runtime changes;
  require exact month-level coverage and preserve the golden control hash.

## Render Committed Monthly Outcomes Beside Monthly Decisions

- Context: The v0.11.2 audit found that operating signal-months had complete
  decision and transition attribution but only a global debrief mechanism list.
- Resolution: Render the player-owned operating result from each committed
  transition next state inside its month section, while leaving active
  observations and global attribution separate.
- Prevention: Keep post-run outcome lines explicitly labeled as realized
  game-unit results; do not treat them as decision-time knowledge, calibrated
  dollars, or causal proof.

## Separate Month-Level Debrief Links From Global Attribution

- Context: The v0.11.2 audit found complete decision and transition traces for
  469 operating signal-months, but no month-specific operating-outcome lines in
  the debrief; global attribution summaries appeared in all 60 runs.
- Resolution: Count month-level decision links, month-level outcome links, and
  global attribution summaries as separate evidence dimensions.
- Prevention: Never treat an aggregated debrief mechanism list as proof that a
  specific month’s loss or bottleneck was explained retrospectively.

## Preserve a Golden Control Beside New Policy Matrices

- Context: The v0.11.1 matrix intentionally submits different commands from the
  existing seed-42 competitive preset, so its transition hashes differ.
- Resolution: Run a separate hold-policy control and assert the known month-one
  hash while keeping new policy trajectories in their own evidence artifact.
- Prevention: Do not compare a changed-policy trajectory directly with a golden
  hash; preserve an unchanged control path when validating runtime compatibility.

## Operating Diagnostics Must Separate Traceability From Causality

- Context: The v0.11.1 matrix exposed repeated losses, bottlenecks, and threshold
  crossings across deterministic policy lanes.
- Resolution: Report ranges and candidate signals while explicitly deferring
  causal marginal-effect, dominance, balance, calibration, and learning claims.
- Prevention: Use controlled follow-up evidence before tuning an operating rule
  or promoting a player-facing change.

## Close the Consequence Loop Before Expanding Content

- Context: External review found that competitive cash funded actions but had
  no recurring operating-income source despite extensive capacity and staffing.
- Resolution: Add one aggregate demand-to-volume-to-margin cycle using existing
  state before adding actors, commands, or service lines.
- Prevention: A new operational domain should identify how it changes demand,
  staffed production, revenue, cost, cash, quality, or access; otherwise defer it.

## AI Playtests Do Not Become Human Evidence Through Repetition

- Context: Recruitment and participant-study costs make structured human
  playtests infeasible for the current personal project.
- Resolution: Use bounded MCP AI playtests as the active gameplay-validation
  path and retain a separate funded approval gate for any future human study.
- Prevention: Never translate AI completion, explanation, pacing, or diversity
  into claims about enjoyment, comprehension, cognitive load, or learning.

## Decision-to-Debrief Audits Need Source-Specific Retry Contracts

- Context: Auditing decision-time context, retries, delayed observations,
  outcomes, and debrief framing for v0.10.58 across the v0.10.43, v0.10.50,
  v0.10.51, and v0.10.54–v0.10.56 artifacts.
- Symptom: A shared retry rule treated the v0.10.51 resource-probe artifact as
  incomplete because that source records the pre-submit observation rather than
  an `observation_after_failure` field.
- Resolution: Keep source-specific contracts, accept the declared pre-submit
  observation only when the source also records the expected failure, and treat
  malformed or mismatched retry state as limited evidence.
- Prevention: Do not normalize heterogeneous evidence into a shared schema or
  infer successful recovery from absent fields; preserve each source's declared
  observation and retry boundary.

## Event-Specific Debrief Coverage Is Still Traceability Evidence

- Context: Auditing v0.10.43, v0.10.50, v0.10.51, and v0.10.54–v0.10.56
  artifacts for debrief use in v0.10.57.
- Symptom: A source can contain observations, commands, hashes, and a debrief
  while still appearing to prove more educational value than it does.
- Resolution: Check each source-specific visibility, response,
  follow-through, outcome, and explanation step; preserve missing fields as
  explicit evidence gaps and keep runtime promotion deferred.
- Prevention: Do not infer debrief clarity, comprehension, learning, strategy
  quality, or causal value from event-specific trace continuity alone.

## Response-Conditioned Recovery Is Still Simulated-Policy Evidence

- Context: Testing whether the existing project-limit error surface supports a
  response-conditioned recovery path in v0.10.56.
- Symptom: A scripted policy can branch on a plain error and recover cleanly,
  which may look like evidence that the interface is comprehensible.
- Resolution: Record the allowed observation/error surface, exclude structured
  fields from the recovery branch, preserve rejected-turn and hash continuity,
  and label the result as traceability evidence.
- Prevention: Do not promote validation hints, schema changes, or human-learning
  claims from deterministic simulated-policy recovery alone.

## Missing Structured Hints Need Recovery Evidence Before Promotion

- Context: Narrowing the v0.10.51 concurrent-project trace fact in v0.10.54.
- Symptom: A stable validation code without a structured resource hint can look
  like an interface defect even when the plain error, unchanged turn, visible
  project state, safe retry, and debrief explanation remain available.
- Resolution: Capture the full rejected-turn surface across named seeds and
  separate response-shape evidence from actual repeated decision friction.
- Prevention: Do not promote validation wording or schema changes from field
  asymmetry alone; require a player-facing, instructor-facing, or domain-review
  artifact that demonstrates unexplained recovery failure.

## Cross-Artifact Synthesis Should Preserve Source Boundaries

- Context: Synthesizing the v0.10.50–v0.10.52 Phase 7 evidence chain for
  v0.10.53.
- Symptom: Different artifacts expose different trace shapes, so a synthesis can
  accidentally imply a shared schema or stronger claim than the sources support.
- Resolution: Validate each source using its declared fields, verify only the
  shared control and matrix identities, and report continuity separately from
  product-gap promotion.
- Prevention: Do not normalize heterogeneous evidence into a generalized
  analytics layer or infer causality, strategy quality, learning, or balance
  from a complete continuity check.

## Turn-Level Traces Are Required for Pacing Proxies

- Context: Auditing v0.10.50 observation-driven traces for v0.10.52.
- Symptom: Aggregate action totals hid whether commands were concentrated in
  particular months or spread across the campaign.
- Resolution: Derive action, hold, active-month, and multi-action metrics from
  the recorded turn trace while preserving the raw source artifact.
- Prevention: Treat temporal command concentration as a descriptive pacing or
  action-overload proxy only; do not infer human cognitive burden or promote
  runtime changes without player-facing, instructor-facing, or domain evidence.

## Expected Validation Failures Need Separate Run Status

- Context: Probing cash, action-point, and concurrent-project limits for
  v0.10.51.
- Symptom: A complete campaign can contain validation failures intentionally
  submitted as part of a resource-boundary probe.
- Resolution: Store expected probe failures separately from unexpected failures,
  verify the rejected turn remains unchanged, and record the safe retry that
  advances the campaign.
- Prevention: Do not count intentional probes as final replay failures or infer
  exploit value, balance, or comprehension from their presence alone.

## Zero-Retry Observation Captures Are Compatibility Evidence

- Context: Capturing nine observation-driven Hard competitive runs for v0.10.50.
- Symptom: Complete runs with no validation failures can look like proof that
  the command surface is comprehensible or educationally effective.
- Resolution: Preserve the full observation, legal-hint, command, retry,
  history, hash, and debrief trace, then label zero retries as capture
  compatibility only.
- Prevention: Do not promote command, guidance, difficulty, or debrief changes
  without a concrete player-facing or instructor-facing gap.

## Synthesize Evidence Without Promoting Runtime Work

- Context: Closing the v0.10.45–v0.10.48 competitive teachability evidence
  chain.
- Symptom: Several supported artifacts can look like cumulative justification
  for a runtime change even when each artifact reports only traceability or
  descriptive variation.
- Resolution: Check source continuity and declared evidence dimensions in a
  read-only synthesis, then route runtime promotion only from a concrete gap
  that existing observations, histories, diagnostics, and debriefs cannot
  explain.
- Prevention: Keep source-specific trace shapes and evidence limits visible;
  do not infer causality, strategy value, balance, winnability, or learning
  from a complete chain.

## Separate Visible Monitor Response From Monitor Exposure

- Context: Adding the v0.10.43 rival-information follow-through matrix.
- Symptom: A monitored and unmonitored comparison can show information
  exposure without showing whether a later decision used that information.
- Resolution: Pair monitor-reactive and monitor-ignoring arms with an
  unmonitored control, and record the signal source month beside the exact next
  turn command.
- Prevention: Treat endpoint differences from intentionally different policy
  commands as descriptive only; require actor-visible signal-to-command
  traceability before discussing monitor value or debrief usefulness.

## Evidence Synthesis Must Close Promotion Gates

- Context: Synthesizing the v0.10.39–v0.10.41 consultant-advice evidence chain.
- Symptom: A sequence of successful traceability and simulated-policy captures
  can look like justification for adding a richer advisor system.
- Resolution: Close the chain with an explicit synthesis that separates
  visibility and continuity evidence from advice quality, learning, causality,
  and advisor-market value.
- Prevention: Keep generic decision-support baselines in place until a later
  artifact identifies a concrete teachability or strategy limitation that the
  proposed runtime expansion would solve.

## Pair Advice-Aware Evidence With Hash-Matched Controls

- Context: Adding the v0.10.41 consultant-advice usage matrix.
- Symptom: Advice-aware commands can change cash runway and make an inherited
  scripted command invalid later in the campaign.
- Resolution: Record advice-aware selection and fallback signals separately,
  guard commands using visible resources, and compare advice-ignoring control
  hashes with the prior traceability artifact.
- Prevention: Never infer advice value from endpoint differences when the policy
  itself changed; require exact observation/history/debrief continuity and a
  matching control before interpreting the evidence.

## Build the Local MCP Binary Before Wrapper Evidence Runs

- Context: Adding the v0.10.40 consultant-advice traceability matrix.
- Symptom: The wrapper launched an existing `target/debug/hs-mgt-game-mcp`
  binary, which can be older than the checked-out source and produce misleading
  evidence about current MCP output.
- Prevention: Evidence runners that invoke the local MCP binary must run
  `cargo build --quiet --bin hs-mgt-game-mcp` before starting sessions, then
  record the package version from the same worktree.

## Test Recurring Costs Against Every Scenario Cash Scale

- Context: Evaluating a future in-house advisor market with monthly salaries.
- Symptom: A recurring cost can appear modest against a high-cash exemplary
  scenario while consuming a large share of the default 60-cash campaign, which
  has no general recurring operating-income flow.
- Prevention: Before promoting a recurring-cost mechanic, test its full campaign
  burden against every supported scenario cash scale and document when a
  month-start tick must occur before observation and command validation.

## Separate Future Queue Ranking From Promotion Rules

- Context: Re-ranking `SPEC.md` Future items after several validation and
  proposal-review slices had accumulated.
- Symptom: The Future queue mixed ranked product work, evidence analysis,
  platform support, architecture discipline, and release readiness as if they
  were equivalent next actions.
- Cause: Cross-cutting guardrails and promotion criteria were stored as ranked
  tracks, making it harder to see the next bounded slice.
- Resolution: Move promotion rules and architecture/documentation discipline
  above the ranked queue, then rank only actionable future tracks.
- Prevention: When updating `SPEC.md` Future, keep the ranked list focused on
  promotable work. Put phase gates, evidence requirements, non-goals, and
  architecture freezes in separate guardrail text.

## Expansion Ideas Need Proposal Gates Before SDD Promotion

- Context: Reviewing future difficulty, regional M&A, and GUI expansion ideas
  after the competitive campaign already had substantial validation evidence.
- Symptom: Large attractive features can look ready for implementation because
  the current architecture can plausibly support them.
- Cause: Difficulty tuning, consolidation mechanics, and GUI work each carry
  different evidence, domain, licensing, and architecture risks that should not
  be collapsed into one implementation track.
- Resolution: Add a proposal-review artifact first, then update roadmap and SDD
  Future tracks while keeping runtime behavior unchanged.
- Prevention: For future broad product ideas, write the review gate before
  promoting work into `SPEC.md` Present. Name the smallest slice, evidence
  limits, non-goals, and stop conditions before editing runtime code.

## Preserve Live-Agent Retry and Replacement Metadata

- Context: Adding the v0.10.15 live LLM/sub-agent difficulty gate after the
  v0.10.14 independent reviewer-agent matrix.
- Symptom: A completed replay artifact can look cleaner than the live decision
  process that produced it, especially when delegated runs retry invalid
  commands or one delegated session does not complete.
- Cause: The replay script validates accepted command streams, while the live
  process includes wrapper mistakes, cash-overrun retries, and occasional
  incomplete delegated sessions.
- Resolution: Store `live_validation_retries` and `decision_source` in the
  artifact, and document the replacement Competitive Analyst Normal stream
  explicitly in the findings.
- Prevention: Future live-decision evidence should preserve retry and source
  metadata even when the final replay has zero validation failures.

## Do Not Read Difficulty Effects From Non-Adaptive Policies

- Context: Adding the v0.10.14 independent reviewer-agent live-capture matrix
  after the v0.10.13 static-vs-adaptive comparison.
- Symptom: A Normal/Hard matrix can look like it should explain difficulty
  balance simply because both difficulty labels are present.
- Cause: If the submitted player policy does not branch on difficulty and the
  observed endpoint metrics are identical, the artifact mainly tests policy
  completion and capture workflow, not difficulty pressure.
- Resolution: Label the reviewer-policy artifact as simulated-agent evidence and
  explicitly state that identical Normal/Hard endpoints do not isolate
  difficulty balance.
- Prevention: Future difficulty evidence gates should either use policies that
  intentionally react to difficulty-visible pressure, live month-by-month LLM or
  human decisions, or a separate analysis that explains why the difficulty
  setting is expected to change outcomes.

## Encode Evidence Matrix Coordinates in Run Metadata Before Expanding Diagnostics

- Context: Adding the v0.10.13 static-vs-adaptive live-capture comparison after
  the v0.10.12 difficulty-pressure matrix.
- Symptom: A new comparison axis can look like it requires changes to shared
  diagnostic tooling before the evidence question is answered.
- Cause: Existing live-capture diagnostics already summarize runs by
  `profile_name`; the missing piece was clear per-run variant metadata and
  readable matrix labels.
- Resolution: Add `policy_variant` metadata to the artifact and include variant,
  difficulty, and seed in `profile_name`, preserving the existing diagnostic
  script.
- Prevention: For future Phase 7 evidence matrices, first test whether the new
  axis can be represented in artifact metadata and labels. Change shared
  diagnostics only when repeated evidence work needs aggregation that labels
  cannot support.

## Reuse Existing Playtest Policies for Evidence Slices Before Inventing New Ones

- Context: Adding the v0.10.12 live difficulty-pressure capture slice after the
  v0.10.11 conservative live-capture matrix.
- Symptom: A new evidence slice can look like it needs new scripted command
  policies, which increases validation risk and duplicates prior playtest
  logic.
- Cause: The pressure and difficulty-adaptive policies already existed in
  `scripts/run_automated_playtests.py`; the missing piece was the
  observation-by-observation live capture artifact, not new gameplay behavior.
- Resolution: Reuse the existing automated policies through `play_session` with
  `capture_trace=True`, and fail fast when a run has validation failures or does
  not complete 24 transitions.
- Prevention: For future Phase 7 evidence work, first check existing automated
  policies and diagnostics before adding new policy logic or runtime exports.

## Capture MCP Evidence at the Wrapper Boundary First

- Context: Adding the v0.10.9 live MCP capture evidence slice after v0.10.7
  replayed preplanned sub-agent commands.
- Symptom: It was tempting to treat observation-by-observation evidence as a new
  Rust MCP DTO or runtime export requirement.
- Cause: The existing Python MCP wrapper already receives observations, legal
  command hints, submitted commands, validation failures, transition summaries,
  and debriefs during normal play.
- Resolution: Add optional trace capture to `scripts/play_game.py` and keep the
  Rust MCP interface unchanged.
- Prevention: For future playtest evidence gaps, first check whether the Python
  wrapper can record the needed actor-visible data. Change Rust MCP DTOs only
  when a specific required field is not already crossing the boundary.

## Access-Loop Diagnostics Should Precede Runtime Cooldowns

- Context: The v0.10.1 free-form Hard seed-variation findings showed access-heavy
  operator policies repeatedly issuing public access commitments under persistent
  scrutiny cues.
- Symptom: The repeated commands could be mistaken for a balance problem or a
  need for automatic runtime cooldowns.
- Cause: The operator policies reacted to recurring observation language without
  remembering recent pledges or requiring a high-access threshold before
  pledging again.
- Resolution: The v0.10.2 diagnostic compared unchanged baseline policies
  against cooldown and reported-access-threshold variants. Both variants reduced
  access pledges while completing all sessions, but also changed access and
  community-trust endpoints for access-heavy profiles.
- Prevention: Treat repeated pledge loops as guidance or operator-policy
  diagnostics first. Do not tune pledge effects or add runtime cooldowns without
  stronger human, LLM, or domain-review evidence.

## Post-Guidance Validation Can Change Endpoint Tradeoffs

- Context: The v0.10.4 post-guidance validation compared unchanged free-form
  Hard policies against a guidance-aware variant that suppressed repeated or
  high-access pledges.
- Symptom: Aggregate access pledges fell sharply, but access-heavy profiles also
  ended with lower access and/or community trust.
- Cause: Redirecting repeated pledges toward neutral payer negotiation reduced
  public legitimacy effects while preserving legal command completion.
- Prevention: Treat lower repetitive-command counts as a behavior signal, not
  automatically as an improved gameplay outcome. Document endpoint tradeoffs
  before promoting guidance heuristics into runtime cooldowns, formula tuning,
  or default playtest policies.

## Phase 7 Synthesis Must De-Duplicate Repeated Controls

- Context: The v0.10.5 synthesis combined the v0.10.0-v0.10.4 free-form Hard
  competitive artifacts.
- Symptom: Raw session totals can look stronger than the evidence actually is
  because the same seed/profile baseline matrix is intentionally repeated across
  artifacts as a control.
- Cause: Validation slices reuse baseline policies to compare guidance or
  operator-policy variants. Those repeated controls are useful for regression
  and comparison, but they are not independent player samples.
- Prevention: When synthesizing playtest evidence, report artifact session
  counts and overlap caveats together. Do not use repeated controls to justify
  runtime cooldowns, balance tuning, human-learning claims, or empirical
  calibration.

## Targeted Project Playtests Must Account for Scenario Delays

- Context: Adding the v0.9.7 `project-coverage` automated MCP playtest target.
- Symptom: Early project-heavy policies failed with `concurrent projects 3
  exceed limit 2`, even when commands appeared spaced apart.
- Cause: Scenario mechanics such as CON legal objections can delay project
  completion, so a later project command may overlap with more in-flight work
  than a simple duration count suggests.
- Prevention: For targeted project-command playtests, use minimal divisible
  budgets, keep no more than two plausible concurrent projects including
  scenario delays, and rerun the full target before documenting findings.

## Scripted MCP Policies Must Budget for Long-Run Cash Draws

- Context: Extending competitive scripted playtest policies beyond month 3 for
  v0.9.6.
- Symptom: Early versions of the extended policies failed around months 5, 10,
  12, 19, or 22 with validation errors such as cash required exceeding
  available cash.
- Cause: The validator correctly includes active project monthly draws and
  current command costs. A policy can become invalid many months after an early
  project or recruitment decision if later commands assume cash that no longer
  exists.
- Prevention: When writing scripted 24-month policies, keep project commands
  rare, prefer low-cost direct investments for coverage slices, and rerun the
  full `python3 scripts/run_automated_playtests.py --json-output ...` batch
  before documenting findings.

## Clinical Service Line Expansion Checklist

- Context: Implementing the Ambulatory Surgery Center (ASC) service line in the competitive regional campaign.
- Symptom: Compile-time errors for missing fields/variants or missing match arms, state hash mismatches in integration tests, and display/transition calculation drifts.
- Cause: Clinical service lines touch almost all layers of the game engine (state, observations, commands, parser, autocompletion, resolver, effects engine, AI, display dashboard, scenario loader, state hashing, and test fixtures).
- Prevention: When adding any new clinical service line, ensure you update the following modules in a single consistent change:
  1. **Core Models**: Add capacity field to `HealthSystemState` in `src/model/competitive_world.rs` and enum variants to `InvestDomain`/`ProjectKind` in `src/model/competitive_command.rs`.
  2. **Observations**: Add capacity to `PlayerObservation` in `src/model/campaign.rs` and map it in both `src/sim/observe_ai.rs` and `src/sim/observe_competitive.rs`. Update test fixtures in `src/competitive/fixtures.rs`.
  3. **Effects Engine**: Register the capacity variant in `effects_competitive.rs` (under strike suspension lists and resolution).
  4. **CLI Parser & Autocomplete**: Add parsing rules in `competitive_parse.rs`, register REPL autocompletes (and update completion unit tests) in `repl.rs`, and document commands in `guidance.rs`.
  5. **Resolution Formatting**: Update command string formatters in `resolution.rs` and `debrief/report.rs`.
  6. **Rival AI**: Include the new capacity in target staffing calculations and `InvestDomain` command scoring in `src/actors/ai_player.rs`.
  7. **Genesis & Scenarios**: Initialize the capacity in `src/competitive/genesis.rs` rival templates, and load it from TOML configs in `src/scenario/mod.rs`.
  8. **Simulation & Display Kernels**: Update target staffing formulas, priority greedy allocation loops, strike adjustments, overflow/diversion/deferral rules, and total capacity calculations in both `transition_competitive.rs` and `display/executive_report.rs` in tandem.
  9. **State Hashing**: Bump schema version in `competitive_hash.rs`, append the new capacity to the hashed string format, and update golden test hashes in `tests/golden_competitive_seed42.rs`.


## Exhaustive Enum Match Updates for Command Vocabularies

- Context: Adding the Cardiology service line and CardiologyUnit project kind to the command vocabularies.
- Symptom: Compilation failures on unmatched patterns in `src/competitive/resolution.rs` and `src/debrief/report.rs`.
- Cause: Match expressions on `InvestDomain` and `ProjectKind` enums in serialization and debrief report formatters were not updated to include the new variants.
- Prevention: When extending command or project enums (`InvestDomain`, `ProjectKind`, etc.), perform a global repository search or run `cargo check` early to guarantee that all match arms in serialization wrappers, command-to-string formatters, REPL autocomplete registries, parser modules, and debrief report generators are exhaustively populated.


## Maintain Original Execution Sequence for Dynamic Timeline Events

- Context: Refactoring hardcoded timeline events to run dynamically from parsed scenario TOML.
- Symptom: An integration test for Month 10 strike action failed because a capital project ended up delayed by 4 months (resolve month 19) instead of 3 (resolve month 18).
- Cause: The refactored trigger logic executed dynamic timeline events before ongoing scenario tick effects (such as active nurse strike costs and project delays). Since the timeline event set the strike active flag to `true`, the active nurse strike logic immediately executed and added an extra 1-month delay in the same turn, which differed from the original sequential ordering where the active nurse strike check ran before the Month 10 strike trigger.
- Prevention: When externalizing or dynamically refactoring sequential transition logic, ensure ongoing condition evaluations run *before* event trigger checks in the turn-start phase to match the exact original execution sequence.


## Direct Investment Limits in Tests

- Context: Adding the Intensive Care Unit (ICU) service line with direct investment commands.
- Symptom: A test for direct ICU investment failed validation with `InvestAmountTooHigh { amount: 60, max: 40 }`.
- Cause: The competitive ruleset defines `max_invest_amount = 40` as the maximum allowed direct investment per turn to keep resource consumption bounded.
- Prevention: When writing unit or integration tests that verify capacity expansion, ensure that direct `Invest` commands do not exceed the ruleset's single-turn investment limit (e.g., 40). For larger expansions, split investments across multiple turns or use capital projects (`ProjectKind`).


## Default Capacities in Backward-Compatible Scenarios to Avoid Staffing Deficits

- Context: Adding the Emergency Department (ED) service line with staffing targets to existing scenario models.
- Symptom: Adding default non-zero `emergency_capacity` at genesis/scenario mapping induced turn-1 staffing deficits and access/quality penalties for existing scenarios because start-of-month systems lacked the nurses and physicians to staff the new ED bays.
- Cause: Scenario structures (e.g. `ScenarioSystemState`) mapped and parsed TOML objects. When defaults are hardcoded to positive values for new fields, they apply immediately to old test files/fixtures, altering their operational assumptions and failing regression tests.
- Prevention: Always set new capacity or service-line default parameters to `0` unless scenario-specific data exists. This allows systems to begin without initial staffing deficits, preserving legacy test runs while allowing players to expand into the new service lines in subsequent turns.


## Keep Scenario Briefs Parameter-Complete to Avoid Downstream Gaps

- Context: Drafting the `competitive-exemplary-v1` scenario brief under Track 2.
- Symptom: Initial drafts of the scenario timeline referred to delayed consequences for underfunded EHR projects and nurse staffing ratios, but lacked initial parameters for starting staffing ratios or definitions of EHR project costs, duration, and Action Point requirements in the brief.
- Cause: Scenario authoring sometimes relies on mechanism-design documents or core codebase defaults without reflecting those constraints explicitly in the student/instructor-facing brief.
- Prevention: Every scenario brief must explicitly specify starting parameters, project costs, duration, Action Point requirements, and immediate vs. delayed consequences of events (such as strikes or underfunding) to remain actionable for future scenario developers.

## Post-Milestone SDD Reviews Should Rank, Not Expand

- Context: After the public playable prototype reached v0.2.0, the repo had a
  thorough runnable stabilization slice, a bounded competitive preview, MCP
  playtest evidence, and a long Future backlog.
- Symptom: Future work was specific but still read as a broad menu, making it
  too easy for the next agent to pick platform expansion, balance tuning, or
  new actors before the product risk was re-evaluated.
- Cause: Milestone completion changed the main uncertainty from "can the game
  run end to end?" to "is repeated play explainable, teachable, and strategically
  interesting?"
- Resolution: Keep `SPEC.md` `Present` empty, record the progress-review slice
  as completed, and rank Future tracks so debrief/instructor analysis,
  exemplary scenario authoring, and evidence-confidence work lead runtime
  expansion.
- Prevention: After major runnable milestones, perform an SDD review that
  explicitly names the next risk, ranks Future tracks, and refreshes stale
  companion docs before promoting a new implementation slice.

## End-Session Metrics Belong In Debrief, Not Active Observation

- Context: Closing the v0.1.49 competitive MCP evidence gap by exposing final
  player tradeoff metrics.
- Symptom: Competitive playtest findings could compare commands and hashes but
  could not make outcome-distribution claims.
- Cause: The active MCP observation surface correctly avoids omniscient state,
  but the end-session debrief had not yet summarized the final human-system
  metrics available in committed history.
- Resolution: Add final player tradeoff and resource lines to competitive
  `end_session` debrief only, derived from genesis and final committed human
  system state.
- Prevention: Put post-run analysis metrics in debrief or instructor surfaces,
  not active-play observations, unless a design explicitly changes the actor's
  information boundary.

## Playtest Policies Need Campaign-Stable Detection

- Context: Running the v0.1.49 automated MCP playtest batch after the AI-agent
  validation pivot.
- Symptom: The batch appeared to hang on the first stabilization `submit_turn`.
- Cause: Scripted policies detected stabilization by checking for the Turn 1
  `staffed_beds` legal-command hint. From Turn 2 onward the policies fell into
  the competitive branch, submitted invalid competitive commands to the
  stabilization parser, and retried forever.
- Resolution: Detect stabilization by the MCP legal-command surface shape,
  launch the built stdio MCP binary, and make scripted validation failures raise
  with campaign, turn, command, and error context.
- Prevention: In playtest automation, branch on stable campaign/session
  metadata or legal-command surface shape, not one turn-specific hint. Scripted
  policies should fail fast on validation errors rather than silently retrying.

## SDD Status Drift Needs A Cross-Doc Scan

- Context: Cleaning up `SPEC.md` after competitive preview, scenario-loader, MCP,
  and playtest slices had landed.
- Symptom: `SPEC.md` and `ARCHITECTURE.md` reflected the current runtime, while
  companion docs still described competitive work as design-only, stubbed, or
  planned I1-I8 runtime.
- Cause: Slice completion updated release history faster than older design docs
  that originally framed the implementation sequence.
- Resolution: Refresh `SPEC.md` Future into gated actionable tracks, archive
  displaced completion detail, and scan canonical/companion docs for stale
  status phrases before final verification.
- Prevention: For SDD cleanup PRs, run a targeted `rg` over `SPEC.md`,
  `README.md`, `ARCHITECTURE.md`, and `docs/*.md` for old version numbers,
  "stub", "design only", "runtime deferred", and completed slice names before
  calling the docs aligned.

## Broad Feedback Should Become Gates Before Features

- Context: Translating external assessment into future SDD planning after the
  architecture, MCP interface, scenario loader, and competitive preview already
  existed.
- Symptom: Strong conceptual feedback can invite broad new abstractions,
  diagnostics, scenario tooling, or calibration frameworks before gameplay has
  proved the need.
- Cause: The project can represent sophisticated health-policy simulation, but
  the next risk is whether repeated play is difficult, legible, interesting, and
  teachable.
- Resolution: Convert feedback into falsifiable playtest hypotheses,
  strategy-space diagnostics, debrief QA, canonical-scenario gates, and
  model-confidence labels rather than runtime expansion.
- Prevention: For future SDD planning updates, ask which finding would justify
  implementation. If no playtest, authoring, debrief, or domain-review evidence
  exists, keep the item in Future and label the needed evidence.

## Agent Playtests Need Evidence Labels

- Context: Replacing planned external human playtest recruitment with AI-agent
  and sub-agent playtests.
- Symptom: It is easy for validation language to drift from "agent traces show
  the debrief is inspectable" into "players learned the intended material."
- Cause: Agent runs are reproducible and useful, but they are simulated-player
  evidence rather than human educational measurement.
- Resolution: Added an active agent-playtest protocol, ADR-0009, glossary terms,
  and roadmap language that separate command/gameplay evidence from human
  learning and policy-validation claims.
- Prevention: When adding playtest findings, label the actor type, seed,
  profile or prompt, observations, commands, and evidence limits before making
  follow-up recommendations.

## MCP SDK Schema Derives Need Direct Dependencies

- Context: Adding the first local MCP stdio server with the official `rmcp`
  Rust SDK.
- Symptom: `JsonSchema` derives failed even though the SDK re-exports schema
  helpers.
- Cause: Derive macros resolve the `schemars` crate name directly.
- Resolution: Add `schemars` as a direct dependency and keep MCP DTOs in
  `src/mcp/` instead of adding serialization/schema derives to core model types.
- Prevention: For protocol adapter DTOs, depend directly on the derive macro's
  crate and keep schema-facing structs at the adapter boundary.

## Canonical Docs Define Scope Before Structure

- Context: Initiating the spec-driven-development baseline for an early research
  and design repository.
- Symptom: It would be easy to invent implementation, CI, scenario, or release
  conventions before the roadmap calls for them.
- Cause: The repository already has canonical proposal, roadmap, design
  principles, and harness documents that define durable boundaries and phase
  order.
- Resolution: Root SDD documents were initiated as lightweight indexes and
  boundary records, not as detailed process or architecture commitments.
- Prevention: Before major changes, read `README.md`, `docs/proposal.md`,
  `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/harness/vital-margin/team-spec.md`; document deferred
  conventions instead of filling them in prematurely.

## First Engine Proof Should Stay Scripted

- Context: Replacing the placeholder CLI with the first deterministic
  architecture proof.
- Symptom: It is tempting to add scenario loading, interactive menus, richer
  actor frameworks, or hash libraries immediately.
- Cause: The roadmap asks for vertical slices before broad frameworks, and the
  codebase had no existing architecture to constrain abstractions.
- Resolution: The first proof uses one scripted command, explicit resolved
  inputs, simple integer metrics, deterministic replay, and no dependencies.
- Prevention: Add loaders, modules, dependencies, and broader actor frameworks
  only when a later slice has at least two concrete examples that need the same
  boundary.

## Second Slice Can Still Stay Single-File

- Context: Adding the first state-policy response after the initial
  payer-negotiation proof.
- Symptom: A second command and second actor decision can make a module split
  feel immediately attractive.
- Cause: The design boundary is now visible, but the prototype still has one
  compact transition function and no reusable scenario, CLI, or persistence
  boundary.
- Resolution: The policy response reused the existing command, observation,
  event, effect, history, and replay shapes without adding dependencies or
  modules.
- Prevention: Split modules when reuse or independent testing needs become
  concrete, not merely because a second branch exists in the demo.

## Debriefing Can Start From Committed History

- Context: Adding the first educational debrief to the deterministic demo.
- Symptom: It is tempting to design a general reporting framework, scenario
  schema, or instructor export format before the first debrief exists.
- Cause: The existing transition history already contains observations, actor
  rationales, attributed effects, and final state needed for a useful teaching
  summary.
- Resolution: The first debrief is a deterministic report over committed
  history, with no new dependency, loader, or persistent artifact format.
- Prevention: Add reporting structure only when repeated debrief outputs need a
  shared format or external consumers.

## First Playability Step Can Be Hard-Coded

- Context: Adding the first player-facing CLI choice after the scripted
  deterministic demo and debrief were working.
- Symptom: It is tempting to add a command parser, scenario schema, or save/load
  path as soon as stdin appears.
- Cause: The immediate roadmap need is to test whether different strategic
  paths produce understandable outcomes, not to define durable content formats.
- Resolution: The first playable slice uses three compiled strategy paths and a
  small input boundary that selects among existing deterministic transitions.
- Prevention: Add parsers and scenario loaders only when repeated playable
  content needs external authoring or persistence.

## Seeded Inputs Belong Outside The Transition Core

- Context: Replacing per-path hard-coded `ResolvedInputs` with a seeded
  stochastic input boundary.
- Symptom: It is tempting to call RNG helpers inside `transition()` once
  exogenous variation is needed.
- Cause: The architecture requires stochasticity to be resolved before the
  deterministic core evaluates state changes.
- Resolution: Added `resolve_inputs(seed, prior, ruleset)` with named streams
  and splitmix64 outside `transition()`, then committed resolved inputs into
  history for replay and debrief.
- Prevention: Keep all random draws, measurement noise, and exogenous shocks in
  explicit pre-transition resolution steps; never hide RNG inside the core.

## Third Turn Can Reuse Command And Actor Patterns

- Context: Adding a workforce pressure turn after payer and policy interactions.
- Symptom: A third command and third actor decision can invite a general
  campaign framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `RespondToWorkforcePressure` with a nursing workforce
  representative decision, extended strategy presets with `third_command`, and
  kept everything in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Fourth Turn Can Reuse Coalition Patterns

- Context: Adding a regional access coalition turn after payer, policy, and
  workforce interactions.
- Symptom: A fourth command and fourth actor decision can invite a general
  coalition framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `JoinRegionalAccessCoalition` with a coalition liaison
  decision, extended strategy presets with `fourth_command`, and kept everything
  in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Observation Revisions Can Stay In Briefings

- Context: Adding prior-period access measurement revisions after the coalition
  turn without rewriting committed history.
- Symptom: It is tempting to retroactively edit prior transition observations
  when later data arrives.
- Cause: The architecture requires immutable committed observations while still
  teaching the difference between reported and revised estimates.
- Resolution: Added `access_measurement_revision` to resolved inputs and
  `prior_access_revision` to observations; debrief notes revisions while history
  remains append-only.
- Prevention: Keep revisions as explicit briefing inputs or notes; never mutate
  prior committed transition records.

## Phase 2 Docs Should Constrain Before They Format

- Context: Expanding the system-boundary and ontology draft after the first
  four-turn vertical-slice prototype.
- Symptom: It is tempting to introduce scenario schemas, actor-card templates,
  or parameter ledgers while documenting the conceptual boundary.
- Cause: The roadmap calls for ontology and causal boundaries before broader
  implementation conventions.
- Resolution: The Phase 2 document names actors, authority, observations,
  commands, causal categories, exclusions, and deferred ontology work without
  defining a file format or calibration process.
- Prevention: Use boundary docs to stabilize vocabulary and scope first; create
  loaders, schemas, and ledgers only when a later slice needs executable or
  evidence-backed artifacts.

## Actor And Scenario Docs Should Gate Runtime Expansion

- Context: Continuing from the Phase 2 boundary draft into the first Phase 3
  design artifacts.
- Symptom: It is tempting to add a fifth turn, a new actor, or a scenario
  schema as soon as the current demo has a coherent four-turn loop.
- Cause: The next roadmap need is to clarify actor authority, information,
  objectives, and learning goals before expanding runtime content.
- Resolution: Added an actor-card template and first scenario brief without
  changing Rust behavior, adding a loader, or introducing a runtime schema.
- Prevention: Before adding a strategic actor or scenario mechanism, write the
  actor card and scenario rationale first; only implement when the slice can be
  tested deterministically and explained in debrief.

## Replay Hashing Should Stay Canonical And Bounded

- Context: Adding stable state hashes to the deterministic replay proof.
- Symptom: It is tempting to add a serializer, save format, cryptographic hash
  dependency, or durable replay artifact as soon as hashes appear.
- Cause: The immediate Phase 4 need is drift detection during replay, not
  persistence or tamper-proof storage.
- Resolution: Added a labeled canonical state record and local 64-bit FNV-1a
  hash for committed transition checks without changing gameplay mechanics.
- Prevention: Keep replay hash inputs explicit and versioned; add external
  replay artifacts or stronger hash guarantees only when save/load, analysis,
  or release requirements make them necessary.

## CLI Playability Can Improve Without New Input Semantics

- Context: Adding a starting executive dashboard and strategy previews after
  the replay hash proof.
- Symptom: It is tempting to make the preview step a command parser, forecast
  engine, or per-turn choice system.
- Cause: The first Phase 5 playability need is better pre-run context, while
  the existing compiled strategy paths still provide the bounded behavior under
  test.
- Resolution: Added pure dashboard and commitment-preview helpers derived from
  existing state and `StrategyPlan` values, without changing transitions,
  resolved inputs, actor decisions, or replay hashes.
- Prevention: Keep CLI affordance improvements at the display boundary until
  the scenario action vocabulary justifies interactive per-turn command entry.

## Per-Turn Play Can Reuse Existing Command Shapes

- Context: Adding per-turn interactive command entry after the dashboard preview
  slice.
- Symptom: It is tempting to add a general command grammar, scenario schema, or
  per-turn posture menus before the first interactive loop exists.
- Cause: The four-turn demo already has typed commands, validation, observation
  briefings, actor decisions, and replay hashes that can be driven turn by turn.
- Resolution: Added play-mode selection, pure per-command parsers with
  access-stabilization defaults, executive briefings from observation data only,
  and concise turn summaries while preserving preset strategy paths for
  regression.
- Prevention: Add parsers and posture menus only when repeated playable content
  needs external authoring or more than numeric parameter entry.

## Replay Artifacts Can Stay Human-Readable and Dependency-Free

- Context: Adding deterministic replay artifact export after interactive play.
- Symptom: It is tempting to add JSON crates, cryptographic hashes, or a general
  save/load framework as soon as external replay is mentioned.
- Cause: The committed history already stores commands, resolved inputs, and
  per-turn state hashes needed for verification.
- Resolution: Added a versioned line-oriented `replay-artifact-0.1.15` format
  with pure serialize, deserialize, and verify helpers plus an optional
  post-run export prompt.
- Prevention: Keep artifact formats explicit and versioned; add stronger
  integrity guarantees or mid-run persistence only when analysis or classroom
  workflows require them.

## Competitive Track Justifies Scoped Command Parser

- Context: Designing the competitive regional market campaign with Stata-like CLI.
- Symptom: Earlier lessons deferred general command parsers for the stabilization
  vertical slice, which uses numeric prompts and turn-locked commands.
- Cause: The competitive sketch requires verb+argument entry, help, and
  autocomplete at a scale numeric prompts cannot support.
- Resolution: ADR-0006 limits the parser to the competitive campaign I/O layer
  only; stabilization demo unchanged; parse output is typed commands feeding the
  existing validation and transition boundary.
- Prevention: Do not generalize the REPL to stabilization until a concrete need
  appears; keep parser logic out of `transition()` per ADR-0001.

## Rustyline Helper Types Need Full Trait Set

- Context: Adding competitive verb Tab-autocomplete using `rustyline`.
- Symptom: Compilation fails with trait-bound errors even when a custom
  completer compiles in isolation.
- Cause: In `rustyline`, `Helper` requires `Completer + Hinter + Highlighter +
  Validator` on the same helper type.
- Resolution: Implemented empty/default `Hinter`, `Highlighter`, and `Validator`
  traits on the completer helper struct.
- Prevention: When introducing a new `rustyline` helper, scaffold all required
  helper trait impls first, then add completer logic.

## Scenario Loading Should Start As A Data Boundary

- Context: Adding the first runtime scenario loader after the scenario format
  draft was approved for a narrow slice.
- Symptom: It is tempting to make scenario files own presets, transition logic,
  arbitrary paths, competitive campaigns, or migration policy immediately.
- Cause: The first proven need is to externalize the existing stabilization
  genesis and schedule, not to create a general authoring platform.
- Resolution: Added `scenario-toml-0.1.40` with one bundled
  `stabilization-v1` TOML fixture and validation before fresh runs; transitions,
  replay artifacts, and session saves stayed unchanged.
- Prevention: Extend scenario loading only when playtest or authoring evidence
  identifies a concrete repeated need; keep executable logic out of scenario
  files.

## Interactive Terminal Tests Can Hang Without Stdin Redirection

- Context: Running `cargo test` in a pseudo-terminal (PTY) runner or workspace sandbox.
- Symptom: Tests that read standard input for campaigns (e.g. `competitive_month_loop_runs_three_months_in_non_tty_context`) hang or timeout.
- Cause: `std::io::stdin().is_terminal()` returns `true` inside a PTY, causing the game to block waiting for human command input instead of executing the fallback non-TTY batch.
- Resolution: `stdin_uses_fallback_input()` in `src/cli/io.rs` treats `cfg!(test)` like non-TTY stdin so competitive campaign tests use preset fallback batches instead of rustyline. Stdin redirection (`cargo test < /dev/null`) still works for manual runs.
- Prevention: Route any new CLI stdin prompts through `stdin_uses_fallback_input()` (or equivalent) so unit tests never block on terminal detection inside PTYs.

## Clippy CI Check Prevents Code Quality Decay

- Context: Integrating `cargo clippy --all-targets -- -D warnings` into the CI workflow.
- Symptom: The repository had accumulated 32 clippy errors (including manual prefix stripping, complex type signatures, collapsible ifs) because clippy was not enforced in the pipeline.
- Cause: The original `.github/workflows/ci.yml` only executed `cargo fmt` and `cargo test` without checks for code quality and compiler lints.
- Resolution: Resolved all 32 clippy issues across production and test code, and added a lint checking step to the CI pipeline.
- Prevention: Run `cargo clippy --all-targets -- -D warnings` locally before committing and always include clippy checks in the CI runner to catch lints early.

## Centralize Post-Run Debriefing Logic for Shared CLI/MCP Surface

- Context: Adding instructor-visible summaries and decision quality reviews for stabilization and competitive campaigns.
- Symptom: It is tempting to write separate CLI-only or MCP-only report string formatting functions or duplicate logic between the MCP session handler and the CLI campaign loop.
- Cause: The CLI campaign and MCP session end endpoint need the same structured information. Duplicating code violates modularity and invites drift.
- Resolution: Consolidated both stabilization and competitive campaign debriefing functions (including the new instructor run summaries) into the `src/debrief/report.rs` module. The CLI campaign runner and the MCP session end endpoint call the exact same module functions, sharing the same representations.
- Prevention: Keep all report formatting and debrief generation code in `src/debrief` and have other layers (CLI and MCP) consume it, ensuring a single source of truth for debriefing text.

## write_to_file Scopes and Parameter Mismatch Scrutiny

- Context: Updating workspace pipeline files (`_workspace/*`) under the harness team spec.
- Symptom: `write_to_file` returned a tool error when writing to `_workspace/00_input/request-summary.md` with `ArtifactMetadata` specified.
- Cause: Specifying `ArtifactMetadata` flags the file as an agent artifact,
  which the tool restricts to its configured artifact directory outside the
  repository.
- Resolution: Omit `ArtifactMetadata` entirely when creating or modifying standard workspace and codebase files outside the conversation-specific artifacts directory.
- Prevention: Do not include `ArtifactMetadata` in `write_to_file` arguments unless writing a conversation report/plan directly to the chat artifacts directory.

## Scenario starting parameters should be complete to prevent initial deficits

- Context: Implementing clinical capacity and staffing requirements (nurses, physicians, admins) in the competitive campaign.
- Symptom: A unit test for the nurse staffing deficit failed because workforce trust dropped more than the isolated nurse deficit.
- Cause: The system genesis template initialized administrator counts below their target ratio, creating a starting admin deficit that triggered immediate burnout penalties in turn 0/genesis calculations.
- Prevention: Ensure that all starting staffing headcounts are set to at least their target ratio levels in the genesis template unless a starting deficit is intentionally part of the scenario. In unit tests, explicitly set target counts for all supporting headcounts (like admins) to isolate the testing of a specific deficit (like nurses).

## Competitive Staffing and Capacity Design Safeguards

- Context: Addressing senior code reviewer findings for Track 5 clinical service line capacity and staffing.
- Symptoms: Compounding exponential decay of access/quality metrics; AI players unable to recruit physicians/admins; immediate understaffing penalties due to instant construction vs. delayed recruitment; leaking rival private events in CLI summaries; integer division budget exploits.
- Causes & Resolutions:
  - **In-place Metric Mutation vs. Additive Penalties:** Direct multiplication of state metrics (`access_index`, `quality_index`) by utility ratios compounds exponentially to 0. Resolved by replacing multiplication with a linear monthly additive drop proportional to the staffing deficit severity.
  - **AI Competitor Completeness:** AI players were restricted to `RecruitRole::Nurse`. Resolved by extending AI candidate command generation to check and generate recruitment options for physicians and admins when their counts fall below target ratios.
  - **Physical Capacity Construction Delays:** Instant physical bed expansion paired with delayed nurse recruitment resulted in immediate, unavoidable turn-0 penalties. Resolved by queuing bed capacity additions with a 1-month delay, matching outpatient clinics, allowing players to recruit beforehand.
  - **Rival Event Filtering:** Rival private operational events (burnout, etc.) were displayed to the player. Resolved by filtering player-facing summaries to skip events starting with competitor names.
  - **Budget Division Exploits:** Players could buy projects with non-multiple budgets, under-paying total costs due to integer truncation. Resolved by validating that project budgets must be a multiple of the duration.
- Prevention: Always use additive drops for ongoing penalties, ensure AI player vocabulary handles all roles, keep construction and recruitment delays aligned, maintain observation boundaries in displays, and validate budget divisibility.

## Scenario Deserialization Backward Compatibility & Systems Length Validation

- Context: Implementing competitive scenario loading and validation (Track 1 / Phase 6.2).
- Symptom: Extending the `Scenario` struct with new required fields broke parsing of the existing stabilization scenario TOML file. Also, difficulty selection had to align with the number of systems in the custom file.
- Cause: TOML deserializers using `#[serde(deny_unknown_fields)]` reject input when fields are added unless they are marked optional. Difficulty choice also determines how many AI rival controllers are initialized.
- Resolution: Wrapped all new competitive-specific fields (`initial_market`, `systems`) and existing stabilization-specific fields (`initial_state`, `turn_schedule`, `actor_stubs`) in `Option`. Validated in `validate_stabilization_scenario` and `validate_competitive_scenario` that the required fields for each campaign are present. In the CLI session runner, verified that `systems.len() == 1 + difficulty.k_rivals()` before initializing.
- Prevention: Make all campaign-specific scenario fields optional in the shared deserialization struct and enforce campaign-specific schema requirements during separate validation passes.

## Competitive Campaign Length Extension & Autosave Implementation

- Context: Extending the competitive regional campaign from a 3-month preview to a full 24-month horizon with mid-campaign serialization, autosave, and reload.
- Symptom: Serializing structs with `'static str` references (e.g. `AiProfile`, `Event`, `AttributedEffect`) causes compilation or runtime issues with serde, and simultaneous loop progression requires keeping track of the historical transition chain.
- Cause: Serde cannot directly deserialize `'static str` since it represents memory leaked references. Additionally, resuming a competitive campaign requires restoring both the starting state and all resolved transitions to date.
- Resolution: Derived `Serialize` and `Deserialize` on all competitive types. For structs with `'static str` fields, serialized them as standard strings, and manually leaked them using `Box::leak` on deserialization to reconstruct stable `'static str` references. Bounded campaign execution to 24 months, auto-saved the transition history on early quit (`q`/`quit`) into `.config/hs-mgt-game/competitive_session.save`, and added a resume menu selection to reload it. Finally, enabled exporting the complete `CompetitiveHistory` as a replay JSON file upon campaign completion.
- Prevention: Separate save structures (`session.save` and `competitive_session.save`) to isolate serialization logic. When deserializing lifetime-bound static strings, deserialize into owned strings and use `Box::leak` to construct stable `'static str` references safely. Ensure complete unit/integration tests cover round-trip serialization and delete-on-completion paths.


## Keep Changelog and Versioning Policy Aligned with Repository Rules

- Context: Updating `CHANGELOG.md` to align with the new versioning policy (0.0.1 bump per PR/PR-equivalent change, 0.1 minor bump for major features/milestones with lower digits reset).
- Symptom: Commit history shows versions (like `0.5.0`) merged to `main` in PRs without corresponding entries in `CHANGELOG.md`, causing a mismatch between `Cargo.toml` and the changelog.
- Cause: Developers sometimes bump `Cargo.toml` version during PR development but forget to add the changelog section for that version.
- Resolution: Added the release notes for `0.5.0` (campaign extension, autosave, replay export), bumped the package version to `0.5.1` in both `Cargo.toml` and `CHANGELOG.md` for the alignment change itself, and aligned `docs/reference/versioning-policy.md` to match the exact rules in `AGENTS.md`.
- Prevention: Always check that `CHANGELOG.md` includes the entry for the version in `Cargo.toml` before merging a PR, and perform a `0.0.1` bump for every PR-equivalent change (including changelog/documentation updates).


## Prevent Test Suite and Automated Playtest Hangs / Crashes

- Context: Running standard cargo test and python automated playtests after campaign loop extension.
- Symptom: Test execution blocks indefinitely waiting for stdin in PTY/terminal-like test environments, and automated playtests crash with `IndexError` on turn index >= 4.
- Cause: Directly calling `std::io::IsTerminal::is_terminal(&io::stdin())` inside campaign completion checks bypassing the `stdin_uses_fallback_input()` safeguard, and fixed 3-command arrays in playtest policies when the competitive loop runs for 24 months.
- Resolution: Swapped `is_terminal` checks with `!stdin_uses_fallback_input()` in `src/cli/campaign.rs` and `src/cli/session.rs`. Modified `scripts/run_automated_playtests.py` policy functions to return `"hold"` once turns exceed the defined command sequence.
- Prevention: Never bypass fallback checks with direct terminal state checks in interactive prompt paths. Ensure automated scripts gracefully scale commands when campaign configurations (like loop duration) change.


## Keep Offline Replay Fixtures Up to Date via Integration Tests

- Context: Developing offline diagnostic scripts that parse replay JSON files which match the current Rust models.
- Symptom: Hardcoded offline JSON files quickly become out-of-date and cause parsers to fail when Rust models are updated or serialized keys change.
- Cause: Manually exporting and updating JSON replay files is slow and easily overlooked.
- Resolution: Created an integration test `generate_mock_replay_fixture` under `tests/golden_competitive_seed42.rs` that automatically builds a full 24-month `CompetitiveHistory` and writes it out as a pretty JSON file at `tests/fixtures/mock_replay.json` on every test run.
- Prevention: Leverage standard test runners to dynamically export serialization fixtures to maintain parity between engine structures and diagnostic tool inputs.

## Avoid Shared-File Race Conditions in Parallel Test Runners

- Context: Running standard Rust `cargo test` suites containing tests that read/write/delete shared configuration files in the user's config directory.
- Symptom: Sporadic test failures in `competitive_persistence_write_load_delete_round_trip` with `No such file or directory` errors.
- Cause: Rust tests run in parallel by default. A cleanup step in one test (like `delete_competitive_session_save`) can run concurrently and delete the file written by another test before it gets loaded.
- Resolution: Run the tests sequentially using `cargo test -- --test-threads=1` when verifying shared file interactions.
- Prevention: Avoid writing tests that point to hardcoded global config files; use unique temporary files or directories (e.g. using `tempfile` crate) to isolate test states.


## Differentiate Timeline Decounters from Event Activation Triggers

- Context: Implementing scheduled timeline events with finite durations (like the nurse strike).
- Symptom: Strike duration decremented immediately in the same month-start tick it was activated, reducing a 2-month strike to 1 month on the first turn.
- Cause: Execution of activation logic and time-decay counters within the same sequential tick processing loop without checking if the event was just created.
- Resolution: Guarded the strike decrement logic to run only when the current month is strictly greater than the activation month (`month_index > 10`).
- Prevention: Ensure state decrements or decay steps check that they do not run in the same tick the state is initialized, or guard them with index constraints.


## Exhaustive Match Patterns for Domain Model Enums

- Context: Adding new PledgeType variants to support Workforce pledges.
- Symptom: Rust compilation error (E0004) for non-exhaustive match patterns on PledgeType and CompetitiveCommand.
- Cause: Adding a new enum variant without updating all matching structures in the codebase (e.g., AI command scoring, serialization helpers, and debrief reports).
- Prevention: When introducing new command verbs or enum variants, search the workspace for all pattern matches on that type and explicitly update AI, report generation, and formatting match arms.


## PR Creation under Sandboxed Credentials

- Context: Attempting to automate pull request creation using `gh pr create` inside a sandboxed agent environment.
- Symptom: `gh pr create` fails with exit code 1 and permission errors (`Permission denied for gh command`).
- Cause: The agent's token/environment lacks permissions to execute `gh` pull request operations on GitHub directly.
- Resolution: Push the git branch to the remote origin (`git push -u origin HEAD`) and report the blocker to the user, providing the direct URL to open the PR manually via the GitHub web interface.
- Prevention: Document this limitation and fallback to manual PR creation rather than blocking the handoff flow.


## Sequential Run Target for Persistence Tests

- Context: Running `cargo test` in parallel when tests read or write global configuration states.
- Symptom: Persistence tests such as `competitive_persistence_write_load_delete_round_trip` fail intermittently when run in parallel.
- Cause: Parallel test execution triggers race conditions where a cleanup step in one thread deletes the session file expected by another thread.
- Resolution: Enforce sequential execution for tests interacting with shared files by running them with `cargo test -- --test-threads=1`.


## Query Pending Effect Queue to Enrich Observations

- Context: Deriving rich observations for in-flight operations (like active capital projects).
- Symptom: Dashboard displays generic labels like `1 active project(s)` which hides crucial details (project name, remaining duration, monthly cash drain).
- Cause: Observation mapping relied on the simple count field (`human.resources.active_projects`) rather than inspecting the pending effects queue.
- Resolution: Updated `in_flight_projects_label` in `src/sim/observe_competitive.rs` to query `world.effect_queue` for matching system effects, calculate remaining months, and extract project names and cash draws.
- Prevention: When displaying status of delayed or multi-turn commitments, query the queue containing the details instead of only presenting state accumulator values.
## Hierarchical Staffing Priority Insertion

- Context: Adding the Obstetrics/L&D service line as a second-priority service line after ICU and before Med-Surg/Outpatient.
- Symptom: If priority queues are not kept aligned between the transition simulation (`src/sim/transition_competitive.rs`) and the user dashboard display (`src/cli/display/executive_report.rs`), the dashboard will show incorrect/inconsistent effective capacities compared to the actual state transitions.
- Cause: The simulation uses a hierarchical greedy allocation to distribute nurses and physicians to ICU, Obstetrics, Med-Surg Beds, Outpatient Clinics, and ED in a specific sequence. This sequence must be mirrored exactly in the display formatting code.
- Prevention: Ensure that any change to the hierarchical allocation rules (such as inserting a new service line like Obstetrics) is updated identically in both `apply_staffing_constraints` and the CLI dashboard report renderer.


## Psychiatric ED Boarding Interaction & Testing Constraints

- Context: Implementing Psychiatric Service Line with ED holding boarding and diversion mechanics.
- Symptom: Unit tests failed to trigger the psychiatric ED boarding path because overflow patients were constantly diverted instead of boarded.
- Cause: ICU critical care patients board in the ED unconditionally (even when ED effective capacity is 0), which depletes all available ED bays before psychiatric patients (who board conditionally based on remaining ED bays) are processed. Furthermore, under normal staffing, ED staffing is only possible if higher-priority specialty units (like psychiatric beds) are fully staffed, leaving no psychiatric overflow.
- Resolution: To test psychiatric ED boarding, set starting `staffed_beds` to `0` to prevent ICU boarding, and activate the scenario-specific RNA strike (under a matching `scenario_id` like `exemplary-competitive-v1`) to halve a single psychiatric bed to `0` effective capacity (creating 1 overflow patient) while leaving the ED staffed with positive capacity.
- Prevention: When testing conditional resource-sharing code (like psychiatric ED holding), isolate the target resource by zeroing out higher-priority demands (like Med-Surg staffed beds / ICU) and use scenario strike/event logic to create capacity-staffing mismatches while maintaining positive holding capacity.


## Keep Display and Transition Ratios Aligned for Dashboard Integrity

- Context: Adding the Neurology inpatient service line with capacity, commands, priority staffing allocation, and ED holding boarding/diversion mechanics.
- Symptom: Incorrect or inconsistent effective capacity numbers printed on the REPL dashboard.
- Cause: The logic to calculate effective capacities (including strike-time halving, target nurse/physician/admin ratios, priority allocation queues, and ED boarding math) was updated in the simulation kernel (`src/sim/transition_competitive.rs`) but not in the display formatting engine (`src/cli/display/executive_report.rs`).
- Prevention: Whenever adding or modifying service lines, targets, strike adjustments, or boarding mathematics, modify both the transition simulation kernel and the CLI/REPL display report formatter in tandem. Write exhaustive unit tests verifying the alignment of targets, effective capacities, and ED boarding/diversion outcomes.
## Advice Validation Must Separate Traceability From Advice Quality

- Context: Validating the repaired deterministic consultant baseline after the
  v0.10.39 live observation and history slice.
- Resolution: Capture observations and debriefs at the MCP wrapper boundary,
  assert exact A-D option and month coverage, and preserve submitted commands
  beside the retained options without scoring adherence.
- Prevention: Treat simulated-agent advice traces as evidence of visibility and
  inspectability only. Do not infer learning, advice quality, calibration,
  difficulty value, or advisor-market value from this matrix.

## Compare Information-to-Action Traces Without Claiming Causality

- Context: Synthesizing consultant-advice and rival-monitor evidence into an
  instructor-facing comparison surface.
- Symptom: A visible cue followed by a different command can look like proof
  that the cue improved a decision or outcome.
- Cause: Advice-aware and monitor-reactive policies intentionally submit
  different commands from their controls, while deterministic traces do not
  represent human decision-making.
- Resolution: Compare visibility, response, resource feasibility, operational
  follow-through, realized tradeoffs, and debrief continuity as separate review
  steps. Label endpoint differences and strategy labels as non-causal,
  interpretive evidence.
- Prevention: Keep actor utility, organizational outcomes, social welfare, and
  educational evaluation distinct; require a new concrete gap before changing
  runtime information, difficulty, balance, or advisor mechanics.

## Audit Evidence Coverage Before Promoting Runtime Work

- Context: Continuing the Phase 7 information-to-action comparison after the
  v0.10.44 synthesis.
- Symptom: A comparison surface can appear complete while its supporting
  artifacts use different field names and trace shapes.
- Resolution: Added a small read-only audit that checks visibility, response,
  follow-through, outcome, and explanation coverage across the existing source
  artifacts without launching new sessions or normalizing them into a broader
  schema.
- Prevention: Verify field coverage and deterministic regeneration first; keep
  supported trace fields separate from human clarity, learning, causal value,
  balance, and runtime-promotion claims.

## Treat Expert Completion as a Bounded Clearability Proxy

- Context: Capturing the v0.10.46 Expert completion matrix across four existing
  simulated-policy profiles and seeds 42, 43, and 44.
- Symptom: A complete 24-month run can be read too broadly as proof that Expert
  difficulty is generally winnable or balanced.
- Resolution: Record completion status, validation failures, histories, hashes,
  and debriefs while labeling the result as a bounded clearability proxy for
  the tested policies and seeds.
- Prevention: Do not promote difficulty values, scoring, balance, or runtime
  mechanics from completion alone. Require broader evidence or a concrete
  player-facing explanation gap before changing the simulation.

## Semantic Command Coverage Must Follow Field Coverage

- Context: Continuing Phase 7 evidence review after the v0.10.45 field-coverage
  audit and v0.10.46 Expert completion matrix.
- Symptom: A trace can contain command, history, and debrief fields while still
  leaving the action-specific event/effect relationship untested.
- Resolution: Added a read-only audit that normalizes each submitted command,
  matches it to player-owned event/effect signatures or an explicit neutral
  classification, and verifies the monthly `Player:` debrief record.
- Prevention: Treat semantic command coverage as traceability evidence only;
  do not convert matched event/effect text into causal, decision-quality,
  learning, balance, or policy-validity claims.

## Strategy Signatures Are Descriptive, Not Dominance Evidence

- Context: Continuing Phase 7 validation after the v0.10.47 command-to-effect
  traceability audit.
- Symptom: Different command trajectories can be mistaken for proof that one
  profile or action is strategically superior.
- Resolution: Added a read-only audit that reports normalized action families,
  trajectories, hold rates, first-turn signals, and existing final tradeoffs
  without assigning utility or comparing outcomes causally.
- Prevention: Treat common actions and distinct profiles as descriptive evidence
  only; require a concrete player, instructor, or domain-review gap before
  changing runtime, balance, difficulty, or scoring.

## Pending Project Effects Must Have Observation Coverage

- Context: Extending project-limit recovery evidence to an accepted ASC
  project exposed a mismatch between the active-project counter and the human
  observation text.
- Symptom: `AscCapacity` consumed a concurrency slot and monthly draw but was
  omitted from the `In-flight projects` label because the formatter had no
  matching branch.
- Resolution: Added the missing `AscCapacity` observation branch and a focused
  Rust regression test, then reran the three-seed capture with state-hash
  continuity checks.
- Prevention: When adding a pending project effect, update actor-visible
  formatters and test name, remaining duration, and monthly draw alongside
  validation and transition coverage.

## Operating-Outcome Use Must Preserve Temporal Alignment

- Context: Auditing whether the v0.11.4 operating-result surface connects
  visible prior-month outcomes to later commands and exact debrief results.
- Symptom: A complete current-month debrief line can appear to support a
  response claim even when the observation belongs to the preceding transition
  or when the campaign has already ended.
- Resolution: Compare month-two-plus observations to the preceding committed
  transition, compare debrief results to the current transition, and classify
  final-month signals as expected terminal cases rather than missing responses.
- Prevention: Keep signal-to-command counts descriptive, preserve player/rival
  boundaries, and do not infer causality, strategy quality, or human learning
  from deterministic trace continuity.

## Runtime Proposals Must Freeze the Observation Contract First

- Context: Promoting the v0.11.13 affiliation design gate toward a future
  runtime slice.
- Symptom: A staged institutional mechanic can appear small while silently
  expanding state, actor authority, stochastic inputs, replay, and debrief
  surfaces.
- Resolution: Define the opt-in scenario boundary, minimum state and
  observations, explicit resolved-input categories, and debrief distinctions
  before adding commands or Rust types.
- Prevention: Keep proposal PRs separate from runtime implementation, preserve
  the default campaign golden path, and stop when a design requires a generic
  actor or deal-market framework.

## Phase Roadmaps Need an Explicit Current-State Checkpoint

- Context: Aligning canonical documents after the project had advanced from
  initial research through three playable campaigns and repeated validation.
- Symptom: The roadmap's detailed history was current, but its final
  “Recommended Immediate Next Steps” still directed contributors to begin
  Phase 0–2 setup, making the canonical document contradict the repository.
- Resolution: Added a dated roadmap-position checkpoint and replaced the stale
  startup list with the current evidence-gated Phase 7/8 posture.
- Prevention: Keep durable phase descriptions intact, but review the roadmap's
  current-position and immediate-next-step sections at each documentation or
  release-status alignment change.

## Separate Intended Users From Affordable Validation

- Context: Translating the visual/audio proposal into an implementable SDD plan
  when recruited human testplays were outside the available budget.
- Symptom: Replacing people with agents can accidentally turn an affordable
  development proxy into unsupported claims about human usability, enjoyment,
  accessibility, domain expertise, or learning.
- Resolution: Preserved humans as the intended audience, replaced only the
  testplay method with declared AI roles/tasks/seeds and reproducible UI,
  command, cue, history, replay, screenshot, and semantic captures, and labeled
  every human-experience claim as deferred.
- Prevention: For each validation gate, name both what the affordable method can
  establish and what still requires separately funded work with people.

## Typed Read-Only Projections Must Exclude Commands by Construction

- Context: Promoting the Phase 2 browser fixture to real live/recorded session
  data after Phase 1 exposed the risk of treating a presentation DTO as a
  convenient mirror of simulation state.
- Symptom: A broad session envelope could silently carry legal commands,
  resolved inputs, effect queues, or private rival data into a client that only
  needs to display observations and committed history.
- Resolution: Added a separate versioned `get_presentation` projection that
  selects actor-visible observation/resource fields and committed transition
  summaries, with serialization tests for hidden-field exclusion and no-turn
  mutation.
- Prevention: Keep read-only DTOs separate from action envelopes, derive them
  from existing observation/history sources, and require an explicit Phase 3
  contract before adding graphical command submission.

## Capture Evidence Must Stay Visible and Allowlisted

- Context: Adding the v0.12.24 browser readiness recorder for reproducible
  AI-agent interface tasks without introducing a second simulation state.
- Symptom: A convenient DOM or adapter mirror could leak hidden sections, raw
  payloads, true/private state, or duplicate interaction events into a trace.
- Resolution: Record only declared session/event/evidence fields, blank hidden
  semantic text, deduplicate direct and delegated DOM hooks, and fail closed on
  unknown or forbidden capture fields with deterministic diagnostics.
- Prevention: Keep settings and recovery outside the transition boundary,
  retain visible source/equivalent labels, and classify captures as technical or
  interface-task evidence rather than human usability or learning evidence.

## Rejected Commands Should Not Be Treated as Missing Committed History

- Context: Comparing repeated v0.12.25 GUI playtest captures for the Phase 9
  evaluation/revision gate.
- Symptom: A generic command-without-history rule would flag an intentional
  rejected-command recovery task even though rejection must leave history
  unchanged.
- Resolution: Make the deterministic analyzer context-aware: require history
  evidence after an accepted command, but suppress that finding when the trace
  records an adapter or submission rejection; retain the gap for valid accepted
  command traces.
- Prevention: Interpret event absence with its declared failure context, cite
  the source capture, and keep every revision finding as a bounded hypothesis
  rather than a strategy, human, or policy conclusion.
## Phase 10: Presentation settings must have observable effects

- Context: The visual/audio contract required readable scaling, non-color status
  language, and written equivalents, but the existing `text_equivalents` setting
  was persisted without changing presentation behavior.
- Symptom: A control can appear in a readiness capture while silently doing
  nothing, weakening both user trust and the evidence contract.
- Resolution: Keep local settings narrowly scoped and test their DOM/CSS effect;
  hide only optional cue explanation text while leaving decision, observation,
  result, history, resolution, and debrief text present.
- Prevention: For every user-facing setting, pair a stable control with an
  observable effect, a storage fallback, and a boundary test proving it cannot
  reach host commands or simulation state.

## Phase 11: Session launch must commit only after the replacement read succeeds

- Context: The GUI previously assumed an adapter-owned `sessionId`, while the
  planned first competitive slice begins with starting or loading a campaign.
- Risk: Replacing the active ID immediately after a start response could leave
  the action, regional, and campaign clients pointed at a session whose typed
  presentation failed to load.
- Resolution: Keep the current view until the existing presentation/action
  load path succeeds, then replace the active session ID and refresh shared
  surfaces. Treat missing start capability and malformed envelopes as
  recoverable adapter conditions, never as an invitation to create local game
  state.
- Prevention: Test valid start/load, malformed responses, failed replacement
  loads, and the absence of command submission as one boundary contract.

## Phase 12: Visual tokens must remain presentation vocabulary

- Context: The first competitive regional desktop used generic glyphs even
  though the proposal requires stable system identities and category markers.
- Risk: A visual catalog can accidentally become a second source of actor
  state, infer severity from metrics, or introduce unreviewed asset rights.
- Resolution: Map only visible IDs/names/kinds/labels to generated text-plus-
  symbol tokens, keep source/status text alongside each token, and use an
  explicit generic fallback. Record the catalog and credits as project-
  generated metadata with no external files.
- Prevention: Treat identity/marker lookup as pure presentation code; assert
  hidden fields, network calls, and third-party assets remain absent before
  expanding the visual language.

## Phase 13: Provenance fields must distinguish repository sources from retrievals

- Context: Phase 9.1 needed to close the licensing checklist without adding
  third-party files or pretending that repository-authored sources had been
  retrieved from the web.
- Risk: Requiring a URL/date for every entry would create false provenance;
  allowing free-form metadata would make future external assets easy to ship
  without a license basis or reproducible notice.
- Resolution: Add a constrained provenance kind. Repository-authored entries
  require a local policy reference and null external fields, while external and
  locally generated entries require HTTPS source/license references and an ISO
  retrieval date. Generate credits and notices from the same registry input.
- Prevention: Keep source/release hashes and human approval separate from
  provenance shape checks, fail closed on denylisted text, and describe the
  remaining legal-audit limit explicitly in release documentation.

## Phase 14: In-game credits must consume the canonical registry projection

- Context: Phase 9.1 required credits to be accessible in-game while the
  canonical registry remained the only source of asset rights metadata.
- Risk: A hand-authored GUI credits list could drift from the release registry,
  omit written equivalents, or become a hidden network/host dependency.
- Resolution: Generate a static ES-module projection from the registries and
  render it through a text-only disclosure that exists before host/session
  loading. Check projection parity and exercise a minimal DOM fallback.
- Prevention: Keep the renderer outside command/session code, use `textContent`
  rather than HTML injection, and treat the panel as contributor/release
  evidence rather than human accessibility or legal clearance.

## Phase 15: Security scanners must be strict without mutating source assets

- Context: Phase 9.2 required file-integrity safeguards while source and
  release assets remain reviewable, hash-bound repository artifacts.
- Risk: A permissive SVG or malformed binary could reach a decoder; an
  auto-sanitizing scanner could silently change approved bytes and invalidate
  provenance hashes.
- Resolution: Add a dependency-free, read-only scanner with explicit SVG
  forbidden-content rules, file/pixel/dimension ceilings, and raster/audio
  signature checks. Exercise malicious fixtures and scan the current roots in
  CI.
- Prevention: Keep security validation separate from registry metadata and
  human/legal review, report every failure deterministically, and never rewrite
  or delete an asset as part of validation.

## Phase 16: Release manifests must be projections, not a second asset registry

- Context: Phase 9.2 needed reproducible release evidence while the canonical
  visual/audio registries remain the only authority for asset identity,
  approval, and hashes.
- Risk: A hand-maintained package inventory could drift in ordering, omit a
  release file, or imply that metadata auditing had sanitized the source.
- Resolution: Derive a sorted manifest from approved registry release paths,
  compare recorded hashes and sizes, and audit release metadata without
  rewriting bytes. Keep source previews outside the release-only metadata rule.
- Prevention: Treat the manifest as a checked projection, require stale-output
  failure in CI, and state that reproducibility evidence is not legal,
  accessibility, decoder, or human-review evidence.

## Phase 17: Asset failure must preserve meaning, not pretend a file loaded

- Context: Phase 9.2 requires optional release assets to fail gracefully while
  the browser remains a presentation-only client.
- Risk: A missing illustration can remove an institution/facility label or a
  stale release path can imply that an unavailable asset is still visible.
- Resolution: Normalize caller-supplied availability results and project an
  explicit generic fallback with the requested label, written equivalent,
  status, reason, and cleared release path. Keep the proof local and static.
- Prevention: Test loaded, missing, failed, malformed, and unknown outcomes;
  forbid network/host access and do not infer outcomes, severity, or hidden
  state from asset availability.

## Phase 18: Audio failure must remain optional and recoverable

- Context: Phase 9.2 needed runtime fallback evidence for unsupported Web Audio
  setup and generated-cue playback exceptions, not only static asset status.
- Risk: A browser audio exception can interrupt a queue or make sound appear to
  be an authoritative outcome channel; permanently disabling a recoverable
  context would also regress existing retry behavior.
- Resolution: Reuse the pure availability projection, expose the catalog source
  and written equivalent in a local fallback descriptor/status, clear the failed
  cue without changing host data, and permit a later cue to retry when a local
  context remains available.
- Prevention: Test setup failure, thrown cue playback, unknown/contradictory
  statuses, successful retry, mute/visual-only behavior, and forbidden
  authority/network markers; keep recorded audio and decoder integration out of
  the slice.

## Phase 19: Catalog coverage must join runtime IDs to release IDs

- Context: Phase 11.1 already listed facility IDs in a campaign ledger and the
  asset registry already validated every release file, but neither artifact
  alone proved that the live catalog and registry referred to the same assets.
- Risk: A newly added facility could have a valid registry entry while the
  runtime points at a different path, or a live catalog entry could bypass the
  approved release registry entirely.
- Resolution: Add a fail-closed join test that derives file-backed facilities
  from `FACILITY_COMPONENTS`, maps them to the `visual.facility.<id>` namespace,
  checks source/release paths and exact hashes, and requires the generic
  fallback to remain pathless.
- Prevention: Keep catalog-to-registry joins in focused coverage tests, retain
  the general asset validator as the release gate, and distinguish asset
  wiring from campaign placement, screenshot, quality, and human evidence.

## Phase 20: Audio coverage must prove both host and fallback parity

- Context: Phase 11.1 had a host event-cue projection test and an older browser
  classifier test, but the campaign ledger did not prove that both vocabularies
  matched the event-channel contract.
- Risk: A cue could be documented without a host trigger, or a legacy fallback
  could emit an ID that the host never declares; either drift would make audio
  optional in theory but misleading in practice.
- Resolution: Join the event-channel contract to the host projection and
  visible-only fallback IDs, and require source/equivalent/cues-only metadata
  for every cue while retaining explicit-empty and unknown boundaries.
- Prevention: Keep parity evidence separate from claims about audio quality,
  loudness, fatigue, device behavior, or human usefulness, and leave broader
  event taxonomy open until it has its own source-backed projection.

## Phase 21: Separate browser stage states from host resolution states

- Context: The music catalog includes a `menu` planning state while the host
  resolution envelope emits only six committed-resolution states.
- Risk: Treating every catalog entry as a host state would imply that local
  browser stage classification is a simulation fact or that the host omitted
  a required resolution state.
- Resolution: Record catalog, host, and browser-only ID sets separately; test
  classifier coverage for all seven and Rust runtime allowlist/priority for the
  six host states.
- Prevention: Keep local stage, visible observation, and committed host
  projection sources explicit in contracts and never promote a presentation
  state into commands, transitions, history, replay, or debrief data.

## Phase 22: History rows must preserve host alignment and recoverability

- Context: Phase 11.1 history-view coverage uses an existing host envelope and
  browser text surface rather than adding new history semantics.
- Risk: Treating transition count, turn rows, and state hashes independently
  could display a misleading history; clearing the last valid view after a
  transient read failure would also erase useful player context.
- Resolution: Require `competitive-history-v1` validation to accept only an
  aligned count/row set, render turn and state-hash pairs together, and preserve
  the last valid view while exposing a recoverable adapter error.
- Prevention: Keep host schema/route, adapter, renderer, and failure behavior in
  one ledger-backed focused test, and distinguish this handoff from full
  campaign history/debrief, durable save/load/replay, and human-quality gates.

## Phase 23: A source checkout is a distribution decision, not a package claim

- Context: Phase 8.3 needed a reproducible distribution boundary while the
  project has no published binary or archive format.
- Risk: Calling the repository a release package without naming its exact
  inputs, build prerequisites, support evidence, and deferred publication
  paths could make a clean checkout appear more portable or certified than it
  is.
- Resolution: Define the exact Git source checkout as the v0.13.10
  distribution unit, preserve the existing read-only checks, distinguish
  first-build dependency access from runtime offline behavior, and state
  current browser/device limits explicitly.
- Prevention: Treat archives, binaries, installers, registry publication,
  broader certification, and human-quality evidence as separate release
  decisions rather than implicit consequences of a passing source checkout.

## Phase 24: Keep in-memory checkpoint claims bounded

- Context: The existing competitive GUI already supports host-owned save/load
  checkpoints, but the Phase 11.1 checklist still named save/load visual
  continuity as untested.
- Risk: Closing that item without distinguishing a live cloned session snapshot
  from durable serialization, cross-process recovery, or browser-refresh
  recovery would overstate the presentation contract.
- Resolution: Record `checkpoint_view_coverage` with the exact
  `competitive-save-v1` metadata, host/MCP/route/adapter/browser sources,
  refresh/failure behavior, and explicit persistence limits. Link it to focused
  checkpoint tests and existing Rust restore tests.
- Prevention: For each continuity slice, name the storage owner, the metadata
  alignment guarantee, the recovery behavior, and the untested durability
  boundary before changing the roadmap checkbox.

## Phase 25: Distinguish replay projection from replay playback

- Context: The competitive GUI already reads immutable host history through a
  versioned replay envelope and renders it through the text-first history view,
  but the Phase 11.1 replay checkbox remained open.
- Risk: Treating aligned replay metadata as a playback or regenerated-trace
  feature would imply simulation reconstruction, persistence, or client-owned
  hash authority that the current surface does not provide.
- Resolution: Record `replay_view_coverage` with the exact host/MCP/route/
  adapter/browser sources, row/count/hash contract, last-valid-view recovery,
  and explicit playback/regeneration limits. Link it to focused replay tests
  and existing Rust/MCP/transport history tests.
- Prevention: Name whether each replay slice is a read-only projection,
  playback engine, or regeneration path before closing any continuity item.

## Phase 26: Define registry completeness without inflating asset claims

- Context: The current visual/audio registries already pass schema, provenance,
  approval, hash, release, security, and credits checks, but the Phase 11.1
  registry-coverage checkbox remained open.
- Risk: Calling registry validity “100% coverage” could imply that every future
  campaign need has a file-backed asset, or that approval proves quality,
  placement, screenshots, accessibility, or human review.
- Resolution: Record `asset_registry_coverage` with exact current visual/audio
  counts, approved/unique closure, the 15 release-path versus 30 null-path
  boundary, validator sources, and explicit future/quality limits.
- Prevention: Define the denominator before closing registry coverage and keep
  current document/runtime registration separate from release-file promotion,
  campaign placement, and human quality gates.

## Phase 27: Treat local screenshot inspection as bounded evidence

- Context: The current GUI can render an actor-visible executive desktop in a
  local browser, and the repository already has deterministic SVG and
  structural presentation checks, but there is no committed raster screenshot
  runner or cross-browser/device capture matrix.
- Risk: Closing a “full campaign screenshot suite” merely because one local
  viewport renders could imply pixel-level quality, full-state coverage,
  accessibility, or human comprehension that has not been evaluated.
- Resolution: Record `screenshot_coverage` as a current supported-surface
  contract, link each named surface to its source and focused tests, and keep
  the browser viewport capture as inspection-only evidence without hashing or
  persisting it as a golden artifact.
- Prevention: Separate source/structural/SVG regression, local smoke capture,
  raster goldens, browser/device compatibility, and human visual review in
  both the ledger and roadmap before checking a screenshot item.

## Phase 28: Separate portrait inventory integrity from portrait approval

- Context: Phase 8.2 already preserves one source preview for each of the
  seven canonical fictional actor roles and maintains a pending review queue,
  but those documents were not summarized by one integrity ledger.
- Risk: Calling the seven-entry preview set “complete” could imply approved
  model/seed provenance, human review, quality, legal clearance, release
  readiness, or runtime suitability.
- Resolution: Record `portrait-preview-coverage.json` for exact role/preview/
  review counts, repository-relative paths, source PNG hashes/dimensions, and
  the empty generation manifest while preserving every pending/release-block
  field.
- Prevention: Keep current inventory/hash closure separate from per-portrait
  identity, resemblance, protected-mark, artifact, accessibility, small-size,
  grayscale, provenance, legal, release-derivative, registry, and runtime-use
  gates.

## Phase 29: Treat written equivalents as metadata closure, not accessibility approval

- Context: Each portrait candidate already has an identity-only written
  equivalent and generic fallback, alongside a defined role and preserved
  source/hash binding.
- Risk: Checking “alt text written” or “source image preserved” could be read
  as human accessibility, recognition, quality, or identity-consistency
  approval.
- Resolution: Record the three fields as machine-checkable technical gates in
  the portrait ledger and test their parity, while leaving lived accessibility,
  small-size/grayscale, human review, and release promotion open.
- Prevention: Name whether a checklist item verifies a field/path/hash or a
  human judgment before changing its roadmap state.

## Phase 30: Aggregate technical release evidence without declaring release readiness

- Context: The repository passed the current Rust, GUI, asset, offline,
  browser, replay, checkpoint, and bounded screenshot checks, while the Phase
  13.1 technical checklist remained visually indistinguishable from the open
  product/content/human release gates.
- Risk: Checking a broad “release candidate audit” could imply full-campaign
  completeness, public-release approval, durable persistence, cross-browser
  certification, or educational readiness.
- Resolution: Add a Phase 13.1 technical ledger and check only the current
  source-checkout evidence, with each command/source and narrower limits
  explicit.
- Prevention: Keep automated technical contracts, bounded local proxies,
  product/content review, and human/public-release decisions as separate
  checklist layers.

## Phase 31: Inventory campaign presentation before commissioning campaign art

- Context: Phase 12 already had a typed `campaign-coverage-v1` surface for
  stabilization and regional affiliation, but the roadmap did not record
  which campaign-visible surfaces were shared or whether the current abstract
  and stage contracts required new map/facility assets.
- Risk: Treating the broad Phase 12 checklist as an undifferentiated art queue
  could duplicate reusable presentation primitives or imply that generic
  campaign coverage completed tutorial, pressure-state, stage-art, audio,
  replay/debrief, or educational work.
- Resolution: Add a campaign-specific inventory ledger and parity test that
  bind the current campaign IDs and shared host/browser surfaces, record the
  no-new-map/facility boundary, and list open campaign work explicitly.
- Prevention: Separate current inventory evidence from implementation,
  provenance, human review, and educational usability before checking a
  campaign-specific roadmap item.

## Phase 32: Distinguish reuse eligibility from direct campaign mapping

- Context: The existing visual and generated-audio catalogs already provide
  reusable identities, markers, statuses, UI cues, ambience, and campaign
  motifs, while Phase 12 still lacked one matrix showing which primitives were
  appropriate for each additional campaign.
- Risk: Calling catalog presence “asset reuse” could imply that every cue is
  already mapped into campaign state, that audio is required, or that a shared
  fallback proves campaign-specific visual quality.
- Resolution: Record exact catalog IDs, source/provenance status, written
  equivalents, fallback-only decisions, and eligible-but-not-directly-mapped
  audio rows per campaign; close only the reusable-assets checklist items.
- Prevention: Keep reuse eligibility, direct runtime mapping, quality review,
  and human evaluation as separate gates in every asset matrix.

## Phase 33: Record asset absence as a decision with reopen triggers

- Context: The current stabilization and affiliation contracts have no visible
  geography or facility-placement requirement, but the roadmap still had an
  open “map or facility needs identified” item.
- Risk: Leaving the item open obscured a useful scope decision; checking it
  without a reopen condition could be misread as proof that future campaign
  art, placement, quality, or screenshots will never be needed.
- Resolution: Add a dedicated decision record joining both campaign surfaces
  to the existing inventory, reuse matrix, facility fallback, and fallback
  tests, with explicit triggers for future geography, placement, or causal-
  legibility requirements.
- Prevention: Treat “no new asset currently required” as a bounded decision,
  not a permanent asset or quality conclusion.

## Phase 34: Register shared pressure vocabulary without inventing severity

- Context: Existing actor-visible operational overlays, statuses, event cues,
  and music states already covered common workforce, demand, financial, policy,
  trust, project, uncertainty, and recovery signals, but Phase 12 had no one
  cross-catalog pressure-state registration record.
- Risk: Adding a new pressure taxonomy without direct visible triggers could
  leak hidden severity, expose inferred causality, or turn optional audio into
  an outcome channel.
- Resolution: Register only current visible-field categories, bind each to
  existing overlay/status/audio IDs, retain text/pattern/reduced-motion
  equivalents, and keep campaign-specific registration empty.
- Prevention: Require a visible source, written equivalent, fallback, and
  explicit direct-mapping boundary before promoting any future pressure state.

## Phase 35: Separate CLI tutorial evidence from browser tutorial completion

- Context: The five-turn stabilization beginner flow and player guide already
  provide written choices, trade-offs, and host-owned commands, while the
  browser launcher currently supports only the competitive campaign.
- Risk: Calling the existing CLI beginner flow a completed visual tutorial
  could imply browser integration, direct audio, human comprehension, or an
  optimal policy recommendation.
- Resolution: Record the current CLI/tutorial contract, shared campaign-
  coverage renderer boundary, and competitive-only live GUI limitation in one
  parity-checked ledger; keep browser-native integration and human review open.
- Prevention: Name the current presentation surface and live-launch scope
  before checking any tutorial roadmap item.
## Phase 36: Treat audio-state mapping as a visible-contract join (2026-07-28)

The shared pressure taxonomy already named eligible music and event-cue IDs,
but that did not by itself establish a campaign mapping. The stabilization
mapping ledger now joins those IDs to visible trigger sources, audio-direction
prototypes, written equivalents, and the current CLI/live-GUI boundary. Keep
direct campaign-envelope audio and human quality review open until a real
browser surface and audience evidence exist.

## Phase 37: Separate current debrief rendering from educational validation (2026-07-28)

The stabilization path already emits deterministic tradeoff, rationale,
effect, revision, and replay-aligned debrief lines, and the shared browser
renderers can display host-supplied debrief text. That does not establish a
browser-native stabilization debrief, instructor-surface decision, or human
educational result. Record the existing CLI instructor appendix explicitly so
future visual work does not silently promote it into a new public true-state
view.

## Phase 38: Keep technical accessibility proxies separate from lived access (2026-07-28)

The shared GUI already tests keyboard/focus landmarks, non-color status
language, text scale, reduced motion, written equivalents, and optional-audio
fallback. A stabilization evidence ledger can join those checks to the current
text-first/competitive-only boundary, but it must keep screen-reader, device,
assistive-technology, lived accessibility, and educational findings open.

## Phase 39: Treat machine provenance as a release boundary, not approval (2026-07-28)

The current reusable stabilization surface is fully repository-authored or
runtime-generated, with registry, release-manifest, credits, and no-new-asset
checks. Unverified portrait previews remain unreleased. Keep legal clearance,
training-data provenance, human quality, and public-release decisions open even
when the technical audit is green.

## Phase 40: Separate partner identity from portrait promotion (2026-07-28)

Regional-affiliation host projections already expose a partner name, condition,
stage, and status, and the shared renderer can provide a generic actor and
written fallback. That is enough to record current identity treatment, but not
enough to promote the `affiliation-partner-executive` portrait preview or claim
browser-native partner presentation. Keep identity decoration, partner-specific
visual/audio work, provenance, legal review, and human identity/quality review
as separate gates.

## Phase 41: Treat negotiation-stage display as a host contract (2026-07-28)

The affiliation host already exposes a typed `NegotiateCommitments` stage, an
active institutional-stage process, a bounded commitment decision, visible
commitment values, and written uncertainty. The shared renderer can present
those supplied fields, while the reusable affiliation-negotiation music state
remains optional. Keep browser integration, stage art/audio, hidden thresholds,
true responses, replay/debrief completion, and human review as separate gates.

## Phase 42: Separate commitment visibility from review authority (2026-07-28)

The affiliation projection already makes commitment metrics and partner
response statuses visible, then represents institutional review as a pending
process with submit/await commands and reported response/status values. Record
that contract without exposing private deliberation, hidden thresholds, legal
validity, or future integration results. Keep optional audio, state-specific
art, browser integration, replay/debrief completion, and human review separate.

## Phase 43: Keep integration consequences separate from hidden inputs (2026-07-28)

The affiliation projection already exposes an integration-obligation process,
begin/decline decision, and integrated/declined statuses with written
consequence language. Integration drag and continuity shock are resolved inputs,
not actor-visible forecasts. Record status and consequence boundaries without
turning hidden inputs into visual controls or claims about future integration;
keep browser integration, state-specific art/audio, replay/debrief, and human
review separate.

## Phase 44: Keep affiliation audio tied to visible commitments (2026-07-28)

The reusable `affiliation_negotiation` state and
`event.affiliation-milestone` cue already have visible triggers, text
equivalents, and audio-off fallback. Record eligibility without turning audio
into an agreement, severity, or outcome channel. Keep direct campaign
integration, new audio, provenance, human listening, and public release
separate.

## Phase 45: Treat affiliation stage order as host evidence (2026-07-28)

The affiliation campaign already has a deterministic typed stage successor
chain, legal command gates, visible labels/process, and replay-aligned history.
Record that sequence without inventing browser animation or turning resolved
inputs, private rationale, or future outcomes into actor-visible steps. Keep
stage-specific presentation, persistence, instructor views, and human review
separate.

## Phase 46: Keep replay/debrief detail in its contract (2026-07-28)

Regional-affiliation replay artifacts can verify version, ruleset, prior
observation, transition, and state hashes, while the terminal debrief can
explain outcomes, decision quality, and alternatives. Record those technical
surfaces without promoting post-resolution response detail into a live browser
actor view or claiming educational effectiveness. Keep browser views,
persistence, instructor boundaries, and human review separate.

## Phase 47: Let provenance gates stop asset promotion (2026-07-28)

The regional-affiliation technical audit can pass registry, security, release,
generation, credits, reuse, asset-need, and audio-packaging checks while
partner/stage art, recorded audio, portrait provenance, legal clearance, and
human quality remain open. Keep machine provenance evidence separate from
direct campaign use and public-release approval.

## Phase 48: Document instructor authority before designing views (2026-07-28)

Existing CLI/typed debrief details can support post-run review without becoming
player-visible controls or a new browser true-state route. Record each
campaign’s observation/detail boundary first, then keep true-state visual
language, export, instructor design, and educational review as separate work.

## Phase 49: Make true-state language explicit before visualizing it (2026-07-28)

The current debrief already separates `Observed`, `True Prior`, `True Outcome`,
and instructor-reveal text, but those labels are a textual post-run boundary,
not a complete browser visual language. Source-link the distinction and keep
browser-native visual design, export, causal/counterfactual/distributional
views, accessibility, and human educational review open until each has its own
evidence and authority contract.

## Phase 50: Preserve the decision-time record while naming the browser gap (2026-07-28)

The immutable core history already pairs each command with the observation
available before it, and the debrief preserves those observations when later
reported estimates are revised. Host history/replay summaries are intentionally
narrower and the current browser view shows summary turn/command/hash data.
Document those layers separately so technical recoverability is not mistaken
for complete browser playback or human decision-time comprehension.

## Phase 51: Keep direct effects descriptive (2026-07-28)

Host-sourced effect records and before/after resolution stages can make a
committed consequence inspectable, and source-linked consequence items can make
that evidence readable. They do not justify an inferred causal graph, causal
certainty, calibrated forecast, or policy-validity claim. Keep direct effect
attribution, causal inference, and human review as separate gates.

## Phase 52: Composite accessibility modes must restore local preferences (2026-07-29)

A low-distraction setting can safely compose existing reduced-motion, text,
written-equivalent, mute, and notification controls only if it captures the
prior local presentation/audio state and restores it on exit. Keep the mode in
the browser boundary, lock conflicting controls while active, and test both
enable and restore paths so a convenience setting does not silently overwrite a
player's preferences or enter simulation authority.

## Phase 53: Put limitations beside the first-session instructions (2026-07-29)

A technical release can be usable without being a policy forecast, a real-world
decision tool, or evidence of human accessibility and educational approval. Keep
the fictional/educational boundary, actor-visible limits, host authority, and
remaining human/release gates in the player guide so a first-time player sees
the scope before treating a game outcome as advice.

## Phase 54: Close technical vertical-slice items with bounded evidence (2026-07-29)

Existing live board, facility, project, first-month, and visible-music contracts
can satisfy narrowly defined technical roadmap items when their sources and
tests are joined in one ledger. Keep that evidence bounded to current supported
conditions; it does not imply full-campaign coverage, asset provenance,
first-time-user evaluation, or human approval.

## Phase 55: Separate hidden-state scans from content review (2026-07-29)

Forbidden-field scans and read-only DTO tests are useful evidence that the
current browser surface does not carry simulation-world or resolved-input data.
They do not prove that every narrative, visual, audio, clinical implication,
institutional resemblance, or educational interpretation is safe; keep those
content and human gates explicit.

## Phase 56: Make content-boundary QA evidence narrow (2026-07-29)

A source-level scan can verify that the current player guide and GUI surfaces
retain fictional/non-forecast limits and do not make direct clinical-advice
claims. It cannot establish clinical validity, policy validity, player
comprehension, or educational safety. Close only the repository-owned wording
gate and keep expert, human, provenance, accessibility, and release review
explicit.

## Phase 57: Keep attribution technical when portraits are unreleased (2026-07-29)

Canonical registry fields, generated credits/notices, runtime credits, and
release-manifest parity can close the current technical attribution gate. An
unverified portrait preview must remain outside those release surfaces when
model/seed metadata and human review are missing. Do not convert machine
attribution into legal, ownership, training-data, resemblance, or release
approval.

## Phase 58: Separate first-session mechanics from first-time-user evidence (2026-07-29)

Host-bound launch/load, a complete seven-stage first-month rail, recoverable
validation/submission errors, and clear guide text can establish a technical
first-session path. They cannot establish that a new player understands it,
can complete it without assistance, or finds it accessible and educationally
useful. Keep structured human evaluation separate from technical path closure.

## Phase 59: Separate campaign duration from campaign presentation coverage (2026-07-29)

A deterministic host test can establish that `competitive-regional-v1` reaches
its 24-month terminal state, and existing actor-visible board, facility,
overlay, event, music, history, replay, checkpoint, and debrief contracts can
establish current presentation coverage. That does not establish full-campaign
facility placement/use coverage, campaign-specific visual/audio quality,
first-time comprehension, or educational value. Record the technical campaign
boundary separately and keep product/content and human expansion gates open;
also state explicitly when a shared campaign envelope does not support the
campaign being assessed.

## Phase 60: Treat technical debrief rendering as a boundary, not a visual review (2026-07-29)

Terminal envelope validation, aligned history/replay/hash metadata, written
debrief/direct-effect rendering, read-only controls, and audio/motion fallbacks
can establish a technical presentation contract. They cannot establish visual
hierarchy, comprehension, accessibility quality, educational usefulness,
causal certainty, or classroom readiness. Keep the technical renderer probe
and the human debrief review as separate gates.

## Phase 61: Keep milestone evidence out of the visitor README (2026-07-29)

Appending each release boundary to the root README placed implementation
evidence before the playable overview and made the first-session path harder to
find. Keep the README focused on orientation, first play, current limitations,
and clear next links; preserve milestone detail in the changelog,
specification, roadmap, and evaluation records that already own it.

## Phase 63: Reuse typed campaign coverage at the live boundary (2026-07-29)

An existing typed campaign envelope is not browser-integrated merely because a
renderer and MCP tool exist. The loopback transport, launcher, adapter, and
mutation handoff must be joined explicitly. Keep competitive-only reads and
validation separate from campaign-specific coverage, and let failed fallback
reads preserve the current view. This technical route still does not establish
campaign-specific visual/audio quality, human usability, or release approval.

## Phase 64: Persist the host artifact, not the browser projection (2026-07-30)

Durable GUI recovery can reuse the existing competitive save artifact when the
host adds only an opaque session-ID wrapper and reconstructs the in-memory
session from immutable history. Keep the file behind the host boundary, write
only after an explicit checkpoint request, and retry hydration only after the
ordinary live-session read reports an unknown ID. This preserves the browser's
actor-visible contract and makes deterministic hash/continuation tests the
proof of restart recovery; it does not imply autosave, campaign-coverage
durability, replay playback, or human release readiness.

## Phase 65: Validate the restart boundary’s hidden intermediate state (2026-07-30)

A persisted competitive transition does not point directly from the prior
history state to the recorded `prior`: the deterministic month-start tick runs
first. Validate the exact reconstructed intermediate state, the aggregated
action month, and occupied-session behavior before hydrating. Otherwise a
tampered save can look hash-consistent while driving inconsistent read/debrief
views, or a restarted host can overwrite a newly created session with a stale
checkpoint.

## Phase 66: Reuse the canonical campaign replay serializer (2026-07-30)

When a campaign history already has a text serializer and deterministic verifier,
keep the GUI wrapper thin: persist the canonical artifact text plus only the
opaque host session ID and schema marker. Requiring new JSON serialization for
an internal history type would expand the model contract and invite a second
validation path. The wrapper can remain host-only while the existing verifier
continues to own replay integrity.

## Phase 67: Treat file replacement as a platform contract (2026-07-30)

`rename` is a clean replacement primitive on Unix but does not overwrite an
existing destination on Windows. A temporary sibling still gives the host a
recoverable write boundary, but the replacement helper must handle the
platform difference and the documentation must avoid promising stronger
atomicity than the implementation provides. Keep a repeated-save regression
test beside the persistence wrapper.

## Phase 68: Dispatch typed campaign artifacts behind one host checkpoint boundary (2026-07-30)

When multiple campaigns share an explicit GUI checkpoint path, keep the
transport and browser contract stable while dispatching by a host-only schema
marker into each campaign's canonical artifact verifier. The affiliation path
can then reuse `AffiliationReplayArtifact` without inventing a second history
format or exposing serialized state to JavaScript. Test each campaign's
fresh-host stage/hash/continuation behavior, while keeping autosave, replay
playback/regeneration, and full-campaign continuity as separate gates.

## Phase 69: Make replay playback a local review cursor (2026-07-30)

An immutable host replay list can support useful review without replaying the
simulation. Keep previous/next/play/pause as local cursor operations over
visible summaries, write the selected command/context/effects/hash into the
existing history surface, and preserve the last valid cursor when a host read
fails. Do not call submission, regenerate a trace, or infer hidden state from a
row; deterministic regeneration and human replay comprehension remain separate
gates.

## Phase 70: Regenerate replay from recorded explicit inputs at the host boundary (2026-07-30)

When a competitive history stores the full `AggregatedMonthlyActions` for each
month, the host can regenerate the deterministic transition without inventing
a fresh AI decision or exposing core state to the browser. Compare the full
transition—including month-start events, institution effects, consultant
options, next state, and hash—before returning the existing visible replay
projection, and reuse the same verifier for durable saves. Keep client playback
local and treat fresh policy/AI search as a separate future gate.

## Phase 62: Keep AI metadata readiness separate from AI metadata completion (2026-07-29)

An approved local model registry and a strict generation workflow can prove
that the project is ready to capture provenance, but they cannot supply the
actual model identity, immutable revision, sampler, or seed for previews
created by a tool that did not expose those fields. Keep current previews
pending and outside the manifest/registry, and require a promotion-shaped
negative test so guessed metadata cannot pass. Human portrait, legal,
accessibility, ownership, training-data, and public-release review remain
separate gates.
# Prove Full-Campaign Presentation Continuity at the Host Read Boundary

- Context: current facility catalogs and regional-world rendering were tested
  at the initial competitive state, while the roadmap still called out
  full-campaign placement/use coverage as open.
- Risk: treating an initial snapshot or stable asset catalog as evidence that
  facility presentation remains available through committed campaign changes
  can hide a stale or incomplete projection.
- Prevention: exercise the host-owned read before every committed month and at
  terminal completion; assert source-bound player metrics and explicit private-
  rival absence without inventing client-side utilization semantics.
# Compare Restored and Original Runs at the Full Host Endpoint

- Context: a one-month checkpoint/next-turn hash proves local restore but not
  full-campaign continuity across terminal presentation surfaces.
- Risk: a restored session can diverge later while immediate checkpoint metadata
  still matches, leaving replay, regional context, or terminal debrief parity
  untested.
- Prevention: checkpoint mid-campaign, continue original and restored hosts to
  the same terminal turn, compare immutable hashes and actor-visible envelopes,
  and clean only the matching recovered checkpoint.
# Checkpoint Each Campaign at Its Own Durable Boundary

- Context: competitive continuity was proven at month 12, but stabilization
  still had only a one-stage restore/next-transition regression.
- Risk: using one campaign’s checkpoint depth as evidence for another can miss
  stage-specific terminal/debrief divergence.
- Prevention: choose a meaningful mid-stage checkpoint for each campaign,
  continue original and restored hosts to that campaign’s endpoint, compare
  actor-visible terminal reads, and clean only the matching checkpoint.
# Checkpoint Each Campaign at Its Own Durable Boundary

- Context: competitive and stabilization continuity were proven from bounded
  mid-campaign checkpoints, while regional affiliation still had only a
  stage-1 restore/next-transition regression.
- Risk: using another campaign's checkpoint depth as evidence can miss
  affiliation-specific review, integration, terminal, or debrief divergence.
- Resolution: checkpoint after the committed affiliation posture/hold path,
  continue original and restored hosts through the six-stage endpoint, compare
  immutable history/replay and actor-visible coverage, and clean only the
  matching recovered checkpoint.
- Prevention: require a campaign-specific durable checkpoint target and
  terminal comparison surfaces before treating persistence continuity as
  complete.
# Cross-Campaign Checkpoints Must Fail Closed by Identity

- Context: the application intentionally stores one latest durable checkpoint,
  and each campaign now has its own full continuation evidence.
- Risk: a later campaign save could accidentally restore an older campaign ID,
  remove the newer wrapper during cleanup, or be presented as an archive.
- Resolution: replace wrappers sequentially, use fresh hosts to load each
  replaced ID, require the existing `checkpoint_missing` boundary, verify the
  newest campaign identity, and clean only its matching ID.
- Prevention: treat campaign and opaque-session identity as a joint durable
  invariant; never infer archive semantics from a single latest-save path.
# Full-Campaign Audio Evidence Must Walk Every Host Read

- Context: representative music/cue mappings and registry checks passed, but a
  single active/terminal fixture could not establish continuity across all
  campaign stages.
- Risk: an unvisited stage could emit an unregistered cue, lose written
  equivalents, or fail to switch to debrief music while the browser appears
  healthy.
- Resolution: walk each launchable campaign through every host coverage read,
  validate IDs against existing catalogs, require terminal debrief state, and
  keep audio optional with written fallbacks.
- Prevention: treat full-campaign metadata continuity as host-source evidence,
  separate from human listening/accessibility quality and release approval.
# Full-Campaign Replay Evidence Must Compare Every Host Read

- Context: checkpoint regressions compared replay/history at selected restore
  points, while full-campaign audio coverage now walks every campaign read.
- Risk: a later transition could drop a history row, reorder replay rows, or
  expose a stale latest hash while the terminal view still appears complete.
- Resolution: read immutable history and replay at genesis and after every
  committed transition through each campaign endpoint, compare ordered rows,
  counts, and hashes, and keep regeneration/authority at the host boundary.
- Prevention: treat full-campaign replay continuity as a separate technical
  gate from browser serialization, archive design, and human replay quality.
# Full-Campaign Renderer Evidence Must Preserve the Host Envelope

- Context: host coverage, audio, and history/replay continuity now walk every
  campaign read, while browser tests exercise only representative fixtures.
- Risk: a renderer can silently drop terminal debrief text, supplied audio, or
  campaign identity even when the host envelope remains correct, or enable a
  second decision path through a fixture callback.
- Resolution: exercise active and terminal fixtures for all campaigns through
  the existing renderer, assert written/optional metadata retention, and keep
  decisions disabled without an explicit host submit callback.
- Prevention: treat browser rendering as a consumer of the complete host
  envelope and keep fixture evidence separate from real-browser and human
  quality claims.
# Full-Campaign Transport Evidence Must Walk the Existing Route

- Context: host full-run and renderer fixture evidence can both pass while the
  loopback route still drops a field or stops serving a campaign at a later
  transition.
- Risk: a stale route serializer can leave the browser with an apparently
  healthy initial panel but no terminal debrief, counts, or audio metadata.
- Resolution: start each campaign through the existing route, read coverage at
  genesis and after every transition, and assert terminal identity/counts,
  debrief, and optional audio without adding transport authority.
- Prevention: keep host, renderer, and route continuity as separate evidence
  gates; passing one boundary must not stand in for the others.

# Persisted Browser Rasters Need Native-Size Provenance

- Context: the in-app browser screenshot API returned content-area JPEGs
  smaller than the requested outer viewport when scrollbars were present.
- Risk: labeling those bytes as 1024×768 artifacts would make the manifest
  dimension claim drift from the file and hide the capture-area difference.
- Resolution: normalize each evaluation-only frame to a 1024×768 canvas with
  right-and-bottom padding, record the native campaign-specific dimensions,
  and validate both native metadata and final JPEG dimensions/hash.
- Prevention: treat output canvas size, native capture size, and pixel-quality
  review as separate facts; never promote padded evidence to a release asset
  or visual-quality approval without an explicit review contract.

# Keep Browser Screenshot Inspection Separate From Raster Release Evidence

- Context: the live loopback GUI can be inspected at the documented baseline,
  but the repository does not yet have a committed raster-capture harness or
  golden image set.
- Risk: recording a successful browser screenshot as a completed release,
  visual-quality, or accessibility gate would turn ephemeral inspection into
  unsupported approval.
- Resolution: record exactly one active and one terminal inspection per
  campaign with viewport, host source, written equivalent, optional-audio, and
  terminal-debrief fields; set artifact path/hash to null and retain explicit
  limits.
- Prevention: require persisted files, reproducible capture tooling, and
  separate human review before promoting the screenshot boundary to a raster
  or public-release claim.

# Terminal Filenames Do Not Prove Terminal State

- Context: the first persisted full-campaign raster pass stopped on the last
  active decision screen while naming those files `terminal`.
- Risk: a turn label such as `24/24`, `5/5`, or `6/6` can coexist with a still
  available host decision and a placeholder debrief, producing false evidence.
- Resolution: capture after the final host transition and require
  `session.done`, exact endpoint history count, non-empty debrief content, and
  zero campaign decision controls in both source coverage and artifact tests.
- Prevention: treat terminal filenames as untrusted labels; validate the
  host envelope and rendered decision surface before persisting or approving
  terminal evidence.

# Technical Review Packets Do Not Close Human Gates

- Context: corrected terminal rasters can support a structured debrief review,
  but the repository has no authorized participant results.
- Risk: marking a technical packet as a completed visual, accessibility,
  educational, classroom, or audio review would overclaim evidence.
- Resolution: bind exact cases, host sources, written fallbacks, review
  questions, and explicit pending-human fields to the technical artifacts.
- Prevention: keep the roadmap human checkbox unchecked until authorized
  anonymized feedback and a recorded go/no-go decision exist.

# Participant-Ready Packets Need Workflow and Recovery Boundaries

- Context: the technical first-session path already had source-bound launch,
  stage, settings, and recovery evidence, but a first-time-user review still
  had no single participant task sequence.
- Risk: a facilitator could over-teach the workflow, conflate draft and
  committed outcomes, or treat source tests as proof of comprehension.
- Resolution: bind exact stage schemas and existing recovery/accommodation
  sources to participant prompts, technical success observations, review
  questions, and an explicit pending-human record.
- Prevention: keep participant-ready evidence separate from participant
  results, and make rejected submissions, unavailable reads, presentation
  preferences, and host refresh requirements visible in every future packet.

# Full-Campaign Review Packets Need Checkpoint and Surface Parity

- Context: a technical 24-month competitive ledger can prove host continuity
  while leaving facility placement/use, overlays, replay, checkpoint, audio,
  and terminal-debrief review difficult to conduct as one bounded session.
- Risk: a reviewer may overgeneralize a first-month or terminal screenshot,
  or treat host-read continuity as proof of visual quality or comprehension.
- Resolution: bind exact early/mid/terminal checkpoints, current facility and
  capacity catalogs, all named presentation surfaces, host-owned state, live
  recovery, and terminal evidence to participant tasks and review questions.
- Prevention: keep full-campaign technical parity, screenshot evidence, human
  findings, and expansion approval as separate gates.

# Audio Review Packets Need Mode and Fallback Parity

- Context: the existing Phase 10.2 protocol named an audio task, but its
  full/muted/cues-only/unavailable paths were distributed across contracts,
  runtime code, controls, and the pilot instrument.
- Risk: a reviewer could report a broad audio preference without checking that
  every mode retains written meaning, or mistake a source-level contract for
  listening usefulness.
- Resolution: bind the exact protocol and pilot task to separate mode steps,
  contract IDs, priority limits, visible-only triggers, fallback controls,
  privacy fields, and pending human-evidence fields.
- Prevention: treat audio mode coverage, source/contract checks, participant
  listening results, revision decisions, and go/no-go as separate gates.

# AI Preview Packets Need Null Metadata and Promotion Parity

- Context: the preserved portrait previews have useful hashes, prompts,
  written equivalents, and role contracts, but the preview tool did not expose
  the approved model revision, sampler, or actual seed.
- Risk: copying values from an approved model registry or inferring them from
  an image would create false provenance and could accidentally promote an
  unreviewed preview into credits, registries, or release assets.
- Resolution: bind every preview to source bytes, dimensions, role/family,
  fallback, queue gates, and explicit null/not-exposed metadata while testing
  generation-manifest, registry, runtime-credit, and release-manifest
  exclusion.
- Prevention: treat inventory identity, model/seed provenance, human review,
  legal/training-data review, release derivative, registry bridge, and public
  release as separate gates; never replace a missing field with a plausible
  value.

# Browser/Device Packets Need Engine and Hardware Claim Separation

- Context: the repository already had a green Chromium compatibility check and
  an emulated low-power proxy, while Firefox/WebKit and real hardware were
  unavailable.
- Risk: a passing syntax or local-smoke check could be reported as broad
  browser support, device performance, or lived accessibility evidence.
- Resolution: bind the browser/device policies, checker outputs, guide limits,
  target queue, and measured proxy values into one packet while keeping each
  unsupported runtime and human gate explicitly pending.
- Prevention: separate declared target support, emulated proxy evidence,
  runtime certification, hardware measurements, human accessibility/usability,
  and public-release approval; never promote an engine or device claim from a
  neighboring test.

# Runtime Smoke Must Bind the Host, Not Only the Shell

- Context: a Firefox screenshot proved that the static GUI shell rendered, but
  the meaningful browser boundary also includes the host adapter and session
  start.
- Risk: shell readiness could be mistaken for a working host-backed GUI or for
  full campaign/browser certification.
- Resolution: use Firefox Marionette to load the loopback page, inspect the
  readiness/start control, click the real start control, and record the host
  status and opaque session ID while keeping Safari/WebKit permission failure
  explicit.
- Prevention: label shell smoke, host-backed smoke, full engine coverage,
  device performance, human review, and release approval as separate gates.

# Pilot Intake Must Be Empty Before Humans Fill It

- Context: the project has a participant-ready first-session packet and
  feedback instrument, but no authorized pilot results.
- Risk: adding a result-shaped artifact too early could silently collect
  identity, raw media, browser/session identifiers, hidden game state, or
  unbounded notes and be mistaken for human evidence.
- Resolution: keep a source-bound intake packet with zero records, bounded
  categories and ratings, explicit consent metadata, and a pending decision;
  validate record shapes without checking in participant data.
- Prevention: separate preparation, authorized evidence capture, findings,
  revision decisions, expansion approval, and public release; never infer a
  human conclusion from an empty or automated intake check.

# Review Packets Need an Evidence Intake, Not Just Questions

- Context: the terminal debrief review packet already bound three corrected
  cases and five review questions, but it had no bounded place to capture an
  authorized review later.
- Risk: a reviewer could add unstructured findings, identity, private state,
  or new media and blur technical debrief evidence with human quality or
  release approval.
- Resolution: add an empty intake with exact case/source parity, bounded
  reviewer/status/rating/accommodation/finding fields, and explicit pending
  decisions.
- Prevention: keep technical review packets, human evidence intake, revision
  decisions, provenance/legal review, and public release as separate gates.

# Provenance Intake Must Mirror Inventory

- Context: the repository has separate visual/audio registries, a generated
  portrait queue, generation metadata policy, credits, and release manifest.
- Risk: a manually copied review list can omit an asset, merge registry and
  preview semantics, or make a later human decision appear to cover an item
  that was never in scope.
- Resolution: derive the intake inventory and gate vocabulary from canonical
  sources, require exact source markers, and start with zero records and no
  promotion fields.
- Prevention: keep technical inventory parity, model/seed provenance,
  identity/resemblance, license/training-data, accessibility, release
  derivative, registry, legal, human review, and public release as separate
  gates; never claim clearance from validator success.

# Revision Decisions Need Source-Bound Targets

- Context: pilot, debrief-visual, and asset-provenance evidence use different
  target vocabularies and remain empty until authorized human review.
- Risk: a free-form revision log can blend findings across sources, capture
  private or identifying notes, or make a technical packet look like a human
  decision.
- Resolution: derive target IDs from each canonical source, constrain
  dispositions/actions/rationales to enums, and keep the decision intake empty
  with a pending human-evidence status.
- Prevention: separate evidence capture, revision decisions, implementation
  verification, campaign expansion, provenance/legal review, and public
  release; never infer a revision from validator success.

# Expansion Decisions Need Gate-Level Evidence

- Context: campaign continuity, first-session behavior, human evaluation,
  visual/audio review, provenance, revision decisions, and public release have
  different sources and different authorization boundaries.
- Risk: a single go/no-go field can hide an unresolved accessibility,
  educational, audio, provenance, or legal gate and make technical continuity
  look like product approval.
- Resolution: bind the three campaign IDs and nine gate IDs to source packets,
  keep the expansion decision empty, and constrain future records to bounded
  status, evidence-strength, blocker, outcome, and rationale codes.
- Prevention: require gate-level human evidence and explicit expansion
  authorization before changing scope; never infer campaign expansion from
  automated coverage or an empty intake.
# Educational Evidence Must Stay Separate From Educational Claims

- Context: the project has canonical evaluation tasks, pilot/debrief packets,
  and a roadmap item for educational usability, but no authorized participant
  results.
- Risk: copying review questions into an unbounded intake or treating technical
  parity as learning evidence could capture private material or falsely close
  the educational/classroom gate.
- Resolution: derive a zero-record intake from existing task, reviewer,
  rating, accommodation, finding, and privacy vocabularies; use deterministic
  review IDs; invoke upstream validators; and keep all human decisions null.
- Prevention: keep technical preparation, participant evidence, educational
  interpretation, revision decisions, expansion approval, and public release
  as separate gates; never infer educational effectiveness from automation.

# A Single Remaining-Gate Audit Prevents Technical Evidence Drift

- Context: the roadmap now has many source-bound technical packets, but its
  open human/runtime gates span portrait provenance, audio, evaluation,
  debrief, content, browser/device, revision, and expansion work.
- Risk: separate packets can make an open gate disappear from the next plan or
  make technical preparation look like product approval.
- Resolution: map every substantive unchecked marker to one stable gate with
  exact source markers, technical status, pending authority, next action, and
  promotion-blocking status; validate the mapping and pending decision fields.
- Prevention: re-audit the consolidated ledger after every merge and require
  authorized evidence before changing a human/runtime status.

# Runtime Smoke Must Bind Engine Identity and Promotion Limits

- Context: the in-app browser completed a current Chromium host-backed smoke,
  while Firefox and Safari/WebKit capabilities were unavailable or permission-
  gated in the same host environment.
- Risk: a passing shell interaction could be copied into a broad browser or
  device certification claim, while an absent CLI binary could be mistaken for
  a failure of the supported in-app runtime.
- Resolution: record the exact observed engine/version, loopback shell state,
  opaque host-start result, zero warning/error counts, and capability statuses
  in a strict additive packet; keep browser policy, human review, hardware, and
  release booleans fail-closed.
- Prevention: treat runtime observations, browser support policy, real-device
  measurements, human evidence, and public-release approval as separate gates;
  do not infer one from another.

# Optional Cue Copy Must Be Distinct From Written Results

- Context: the live GUI hides the optional audio explanation when optional cue
  explanations are disabled, while the settings summary and written result,
  history, and debrief surfaces remain available.
- Risk: treating the optional paragraph as the complete written-equivalent
  contract would either report a false fallback defect or hide a real loss of
  decision-relevant content.
- Resolution: verify both states explicitly: the optional explanation is
  present when enabled and intentionally hidden when disabled, while written
  results remain complete in both cases; keep muted/cues-only playback and
  listening quality unverified.
- Prevention: distinguish optional explanatory copy from mandatory written
  outcomes in runtime evidence, accessibility review, and audio evaluation.

# Player Endpoints Must Not Reuse Instructor Debriefs

- Context: the competitive end-session host route reused a debrief builder that
  appended an instructor-only decision-quality appendix, and a stale campaign
  coverage panel could remain visible beside the terminal debrief.
- Risk: a player-facing endpoint can leak review-only information and present a
  contradictory placeholder surface even when the host envelope is otherwise
  correct.
- Resolution: keep the full `competitive_debrief` builder for the authorized
  CLI/instructor surface, add a player-safe terminal projection for the host
  route, hide the stale companion panel, select a visible debrief target, and
  bind the correction to a live evidence packet plus regression tests.
- Prevention: treat player and instructor projections as separate contracts;
  validate information boundaries and visible terminal targets together rather
  than assuming a shared formatter is safe for every endpoint.

# Regenerate Measurements After Every Source-Bound Renderer Change

- Context: the terminal renderer correction passed its focused and full checks,
  but its final cross-campaign guard changed the canonical GUI source byte total
  after the first merge, leaving the emulated device evidence stale.
- Risk: source-bound evidence can fail on the next clean checkout even when the
  functional behavior is correct, or stale measurements can be mistaken for a
  current performance result.
- Resolution: the post-merge audit recomputed the live-source total, updated the
  policy/review packet/test fixture, and kept the proxy limit and certification
  boundaries unchanged.
- Prevention: run generated asset, device, and release projection checks after
  the final renderer diff; treat every byte-count mismatch as evidence drift,
  not as a reason to loosen the bound or claim device quality.

# Refresh Consolidated Audits After Evidence Slices

- Context: the remaining-gate audit was still versioned to the earlier v0.13.96
  preparation slice after newer runtime capability, first-session/audio,
  terminal-debrief, and device evidence had merged.
- Risk: a technically accurate but stale index can omit the strongest current
  evidence and make the next authorized human action harder to identify.
- Resolution: refresh the audit package version, add a dedicated current
  runtime-boundary check, and retain the same eight gate mappings and pending
  decision boundary.
- Prevention: re-run the consolidated audit after each evidence packet merge;
  update source indexes without converting technical preparation into human or
  release approval.

# Keep Durable GUI Checkpoints Per Session

- Context: the GUI host stored every campaign's explicit checkpoint in one
  latest-file slot, so saving a second campaign replaced the first campaign's
  durable recovery artifact.
- Risk: a restart could preserve the host authority boundary while silently
  losing a valid checkpoint that still had an opaque session ID in browser
  storage.
- Resolution: write each validated session ID to a sibling `.checkpoints`
  archive file, hydrate the matching file first, and retain the old single
  file as a migration fallback.
- Prevention: test concurrent campaign saves, live-ID collision behavior,
  per-session cleanup, legacy reads, and path-safe session IDs whenever host
  persistence changes.

# Discover Checkpoints Through Validated Metadata

- Context: once per-session archives existed, the browser needed a way to find
  opaque IDs without receiving host save contents or guessing which campaign a
  file represented.
- Risk: a discovery scan could leak serialized state, treat malformed or
  unsupported files as usable, or make directory iteration order appear stable.
- Resolution: validate each archive and legacy candidate through the existing
  host save/replay checks, return only campaign/seed/count/source metadata,
  count omitted candidates, shadow a legacy entry with a valid archive of the
  same ID, and sort the accepted descriptors by opaque ID before rendering.
- Prevention: keep discovery observational and manual-load-only; test
  malformed, mismatched, unreadable, legacy, shadowed, and path-unsafe entries
  whenever checkpoint storage or its browser picker changes.
## Keep Host Save Downloads Opaque (v0.13.105)

- Context: the host already owns validated checkpoint files, while the GUI
  needed a user-facing way to download an existing save artifact.
- Risk: allowing the browser to deserialize or synthesize the file would move
  true state, history, or serialization authority into the presentation layer.
- Resolution: validate the selected archive/legacy file on the host and serve
  its exact bytes as an attachment; validate the same in-memory bytes that
  will be returned, then let the browser create only a transient download
  object URL and never inspect, load, or store the artifact.
- Prevention: preserve explicit storage-source selection, open archive directories
  and files with no-follow handle confinement, reject unsafe paths and invalid
  content, and keep automatic resume/replay regeneration separate.

## Keep Automatic Resume Narrow (v0.13.106)

- Context: browser refresh can recover a best-effort opaque session ID while
  the host owns the durable checkpoint and hydration path.
- Risk: applying durable recovery to manually entered IDs or retrying without a
  bound would make an explicit user action surprising and could create loops.
- Resolution: allow one host restore attempt only for the refresh-recovered
  opaque ID; manual loads remain explicit, transient failures retain the ID,
  and confirmed unknown sessions clear it.
- Prevention: keep the policy versioned and source-bound, test the one-attempt
  boundary, and never add browser save parsing, serialization, or state.

## Keep Browser Smoke Evidence Honest (v0.13.107)

- Context: the live GUI host embeds the browser module graph at Rust compile
  time, and a browser refresh normally finds the still-running host session
  before the conditional durable-restore branch is needed.
- Risk: probing a stale host binary can miss the new visible contract, while a
  successful refresh against a live host can be overstated as proof of host
  restart recovery.
- Resolution: rebuild the GUI host before the Firefox smoke, verify one
  explicit checkpoint save plus one refresh and opaque-ID recovery, and record
  that the probe does not simulate a stopped host or claim the durable-restore
  branch ran.
- Prevention: separate live-session refresh evidence from stopped-host restore
  evidence, keep Firefox/WebKit/device certification boundaries fail-closed,
  and rerun the source-byte proxy after every embedded GUI change.

## Keep Campaign Launch Smoke Below Full-Campaign Claims (v0.13.108)

- Context: the Firefox runtime can start all three supported GUI campaigns, but
  the roadmap gate asks for full-campaign browser certification.
- Risk: launch success can be mistaken for transition continuity, audio
  coverage, accessibility quality, or complete campaign certification.
- Resolution: record campaign-specific labels, opaque IDs, non-demo shell state,
  and ready state only; retain a separate boundary stating that no campaign
  advanced through its full transition sequence.
- Prevention: keep launch/read smoke, full-campaign runtime certification, and
  human review as separate evidence fields and promotion decisions.

## Keep Full-Campaign Browser Smoke Host-Backed (v0.13.109)

- Context: the Firefox launch probe proved only that campaign shells could
  load, while the browser gate still needed evidence across a transition
  sequence.
- Risk: clicking controls without waiting for host validation, autosave,
  history/replay, and terminal rendering could report a browser-only loop
  rather than a committed campaign.
- Resolution: drive the existing visible Hold form, validation, submission,
  end-session controls, and host status fields; require exact month-by-month
  history/replay/autosave counts and a host-provided terminal debrief.
- Prevention: keep this technical smoke separate from Firefox support
  certification, alternative action coverage, audio decoding, real-device
  measurement, and human review; do not infer any of those from a passing
  24-month Hold path.

## Keep Campaign-Specific Firefox Smoke Host-Shaped (v0.13.110)

- Context: stabilization and regional affiliation use a different visible
  campaign-coverage decision contract than competitive action drafts.
- Risk: reusing competitive selectors or treating a visible form refresh as a
  committed stage could overstate Firefox full-transition continuity.
- Resolution: drive each campaign's rendered coverage form, fill only visible
  minimum/default values, require exact host autosave and history counts, then
  use the visible end-session path for the host terminal debrief and hash.
- Prevention: keep campaign-specific runtime smoke separate from Firefox
  support certification, alternative decision coverage, audio decoding,
  human review, device measurement, and public-release approval.

## Keep Workspace Handoffs Explicit (v0.14.1)

- Context: reducing the mounted surface required separating presentation
  navigation from first-session progress and host refresh events.
- Risk: treating a load, refresh, or direct navigation click as a review
  acknowledgement could advance the task strip without the player seeing the
  actor-visible brief or resolution.
- Resolution: keep `briefingReviewed` and `resolutionReviewed` in ephemeral
  first-month flow state and update them only from explicit handoff controls;
  ordinary workspace navigation remains presentation-only.
- Prevention: test event mapping, visibility/focus boundaries, terminal
  routing, and failure/retry states independently from host transition tests.

## Keep One Action Surface Host-Ordered (v0.14.2)

- Context: competitive and campaign-coverage payloads exposed overlapping
  decision/catalog/builder panels with different copy and interaction rules.
- Risk: duplicate rows, stale validation, or client-side technical language can
  make a presentation refactor look like a new authority boundary.
- Resolution: normalize each host payload into one private action view model,
  render a single-open card surface, keep the exact canonical command with its
  draft, and let the host remain authoritative for validation, legality, cost,
  uncertainty, and transition results.
- Prevention: characterize one-card-per-host-action, focus/live-region recovery,
  direct rejection preservation, hidden live technical controls, and the device
  source budget before changing card or plan markup; record human usability as
  pending until an authorized pilot exists.

## Keep Documentation Currentness Agent-Executable (v0.14.3)

- Context: broad GUI growth left active Markdown, SDD summaries, and roadmap
  gates describing older implementation boundaries even while runtime tests
  remained green.
- Risk: human-dependent approval language and stale browser/persistence claims
  can block safe technical work or misstate the actor-visible authority
  boundary.
- Resolution: classify every tracked Markdown path, keep current SDD prose
  compact, preserve historical evidence verbatim, and make future GUI work
  advance through agent-executable checks with explicit evidence limits.
- Prevention: run `scripts/check_documentation_currentness.py` in CI and keep
  Chromium-default, fail-closed asset, host-authority, replay/checkpoint, and
  optional-human-feedback boundaries synchronized with source and tests.

## Re-measure the Emulated Device Proxy After Live GUI Source Changes (v0.14.4)

- Context: adding event-gated navigation changed the live module byte count,
  while the device-performance contract intentionally compares source bytes to
  a captured measurement and fails closed on drift.
- Risk: a technically correct GUI slice can appear broken or silently exceed
  the declared low-power proxy if the evidence artifact is left stale.
- Resolution: re-run `scripts/check_device_performance.py`, synchronize the
  policy and current review packet to 445,346 measured bytes under a 446,000
  byte limit, and keep the result labeled emulated rather than hardware
  certification.
- Prevention: treat source-byte evidence as part of every live-GUI change's
  validation and update only the current policy/packet, not historical reports.
