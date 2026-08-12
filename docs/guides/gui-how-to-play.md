# How to Play in GUI Mode

The live browser GUI provides the competitive regional, stabilization, and
regional-affiliation campaigns through a local Rust host. It does not require
MCP setup, a separate web server, or manual JavaScript adapter injection. The
recommended first session is the five-decision **Stabilization tutorial**;
competitive and affiliation are separate alternatives.

## Requirements

- A Rust toolchain with Cargo.
- A current Chromium-based desktop browser with JavaScript modules enabled.
  The repository's compatibility matrix supports the documented evergreen
  Chromium surface. Firefox, WebKit/Safari, mobile, and legacy browsers are
  deferred and non-certified. Audio is optional and uses the browser Web Audio
  API.
- A local checkout of this repository.

The launcher supports `competitive-regional-v1`, `stabilization-v1`, and
`regional-affiliation-v1`. All three campaigns use the shared `Actions`
surface: competitive play drafts a `Monthly plan`, while stabilization and
regional affiliation commit one decision directly. Custom scenarios still use
`cargo run`.

The host also exposes `campaign-coverage-v1` for a typed campaign coverage read of
the current player-visible metrics, public signals, process summaries, action
metadata, history, and terminal debrief. This read does not replace the
competitive catalog/validation/submit sequence or reveal private rival state.
In the normal competitive GUI it is split across the Brief, Decide, Resolve,
and Review workspaces after start/load and accepted monthly refreshes; if that
optional read is unavailable, the actions remain usable.

For a first session, choose `stabilization-v1`, seed `42`, and no difficulty.
Use the task workspace to reveal one visible action at a time. Presentation
settings are local browser preferences; they do not change commands, host
validation, simulation outcomes, or replay history.

## Campaign choices

The campaigns are alternatives rather than sequential chapters; progress and
checkpoints do not transfer between them.

- **Stabilization tutorial** (`stabilization-v1`) is five abstract executive
  decisions. It has no calendar duration or difficulty. The GUI shows one
  host-provided action card per stage; the CLI also offers beginner guided
  choices.
- **Competitive regional market** (`competitive-regional-v1`) is a separate
  24-month campaign with monthly AP planning, simultaneous AI-rival actions,
  and lagged public signals. Easy/Normal/Hard/Expert change rival count and AP;
  it is not network multiplayer.
- **Regional affiliation** (`regional-affiliation-v1`) is a separate six-stage
  nonprofit-partner scenario covering assessment, posture, commitments, review,
  and early integration or independence. It has no AI rivals or difficulty
  tiers and is not legal, valuation, antitrust, or transaction advice.

## Start the GUI

1. Open a terminal in the repository root.
2. Run:

   ```bash
   cargo run --bin vital-margin-gui
   ```

3. Keep the terminal running. After compilation, it prints a line like:

   ```text
   Vital Margin GUI: http://127.0.0.1:7878
   ```

4. Open that URL in your browser.
5. Leave the campaign set to **Stabilization tutorial**
   (`stabilization-v1`), use seed `42`, and select **Start selected session**.
   Difficulty is not used for this campaign. The same start control launches
   the competitive or regional-affiliation alternatives when you are ready; for
   the competitive alternative, the button is **Start competitive regional
   session**.

The server listens only on your computer's loopback interface. It does not make
the game available to other computers and does not provide network multiplayer.
At startup it prints the application-config path used for explicit checkpoint
files for all three campaigns; the file is host-owned and is never sent to the
browser.

## Follow the first session

The GUI opens one task workspace at a time. Use **Brief**, **Decide**,
**Resolve**, and **Review** in the task navigation; inactive workspaces are
removed from keyboard navigation. The compact Current task strip shows the
primary next action, while **Show all first-session steps** reveals the full
rail. Competitive sessions track seven action handoffs:

1. **Start or load:** create a session or load an ID from this running host.
2. **Inspect:** read the executive briefing, regional market, selected-entity
   drawer, visible resources, capacity, workforce, payer, and rival signals,
   then choose **Continue to decisions** to acknowledge the brief.
3. **Draft:** open an action card, choose its parameters, and select **Add**.
4. **Validate:** add the actions you need, then select **Check plan**.
5. **Submit:** after the host accepts the unchanged plan, select **Commit
   month**.
6. **Resolution:** in **Resolve**, read, play, pause, skip, or review the
   committed monthly resolution. Skipping animation does not skip the game
   result.
7. **Continue:** select **Continue to next brief** to acknowledge the written
   resolution and inspect the refreshed observation for the next month.

For stabilization and regional affiliation, the rail instead tracks five
campaign-coverage handoffs: start/load, inspect the visible campaign envelope,
choose a card in **Actions**, review the committed stage in Resolve, and
explicitly continue. These campaigns do not use the competitive local-draft or
validation steps.

After each accepted GUI decision, the host automatically requests a checkpoint
through the same host-only path. The GUI reports the committed transition count
when autosave succeeds; if it fails, the committed session remains active and
the written status gives the error. **Save host checkpoint** remains available
as a manual retry. The host stores one checkpoint file per opaque session ID in
its sibling archive; after a host restart, choose **Find saved checkpoints** to
inspect validated metadata, select **Use this session ID**, and then choose
**Load existing session** or **Restore host checkpoint**. Manual opaque-ID entry
remains available. The browser never serializes or loads the saved artifact,
and a missing or colliding checkpoint is reported as a recoverable error. An
explicit **Download host save** action transfers only the host-validated file
bytes to the user's download.

Drafting does not advance time. **Check plan** asks the host to validate action
points, cash, political capital, command syntax, and other host-owned
constraints without committing the month. Editing or removing a validated
draft requires validation again. **Details** exposes host-provided timing,
rules, uncertainty, cost, canonical command template, and source.

## What the interface shows

- **Seed:** controls reproducible uncertainty. The same seed and decisions
  reproduce the same run.
- **Difficulty:** changes rival count and available monthly action points.
- **Action points (AP):** limit the command batch you may commit this month.
- **Pending processes:** visible commitments or delayed effects, not guaranteed
  future outcomes.
- **Resolution:** host-derived before/after observations and direct committed
  effects from immutable history.
- **State hash:** a replay/audit identifier for the committed state.

Rival private state and unresolved stochastic inputs are deliberately not shown.

## Settings and accessibility

Open **Settings, audio, and help** to access the utility drawer before or during
a live session:

- **Low-distraction mode** combines Reduced motion, Large text, visible cue
  explanations, muted audio, and reduced notifications. While active, the
  individual presentation and audio controls are locked to that safe recipe;
  turning it off restores the prior local presentation/audio preferences.
- **Reduced motion** removes non-essential pacing and uses immediate written
  updates. It does not remove a result or a control.
- **Show optional cue explanations** keeps written explanations for audio/event
  cues visible when enabled. Written decisions, observations, results, history,
  and debrief remain complete either way.
- **Text size** supports **Standard** and **Large**. Choose **Large** when the
  default scale is difficult to read; browser zoom remains an additional local
  option.

The initial reduced-motion value follows the browser's `prefers-reduced-motion`
preference when available. Settings are stored in the browser when storage is
available and otherwise remain session-local; a storage failure does not block
play. Low-distraction mode is a local presentation preference, not a host game
mode.

## Optional audio

Audio starts off. Select **Enable audio** after the page opens; browsers require
a user gesture before sound can start. Use **Mute audio** for a complete audio
silence, **Cues only** when you want event/interface feedback without music,
**Music only mute** to remove music, or **Reduced notifications** for fewer
repeated cues. Master, music, interface, event, and ambience volumes are
independent sliders.

Audio emphasizes information already visible on the page. Every cue has a
written equivalent, and muted or unsupported audio never prevents play. For
campaign coverage, host-supplied music/cue metadata is optional and remains
limited to the existing catalog; the written stage and decision surface stays
complete when it is absent or muted.

After a campaign decision commits, expand **Decision-time observation** in the
history entry to revisit the visible information that preceded that command.
This is host-supplied written context, not a hidden-state or outcome forecast.

In **Committed history and replay**, use **Previous row**, **Next row**,
**Play replay**, and **Pause replay** to review the visible committed summaries.
The selected row shows its command, optional observation, visible events/effects,
and state hash in written text. These controls move a local review cursor only;
they do not submit a command or regenerate the simulation. The host verifies
competitive replay determinism before returning the visible projection. An
empty replay says that no committed rows exist, and a failed refresh preserves
the last valid view.

## Credits and provenance

Open **Asset credits and provenance** in the settings panel to inspect the
registered visual and audio sources used by the presentation. The disclosure
is text-first and keyboard-accessible. It describes contributor/release
provenance; it is not a claim that an asset is a real institution, person, or
policy authority.

## Load an existing session

Choose **Find saved checkpoints** under **Saved host checkpoints** to request a
host-owned metadata list. The list shows campaign, opaque session ID, committed
transition count, and whether the entry is from the current archive or the
legacy fallback. Select **Use this session ID**, then choose **Load existing
session**. You can also copy a session ID displayed by the current GUI and enter
it manually. For
`competitive-regional-v1`, `stabilization-v1`, or `regional-affiliation-v1`,
each accepted decision requests autosave; select **Save host checkpoint** before
stopping the host if you want an explicit retry. After a browser refresh, the
client may attempt that host checkpoint once when the stored opaque ID matches
an archived checkpoint file, then refreshes the ordinary
presentation/campaign/action/history/replay reads. Manual Load and Restore
remain explicit and do not automatically hydrate an unknown manually entered
ID. Transient refresh failures preserve the stored ID for retry; a confirmed
unknown session clears it. Without a successful checkpoint, stopping or
restarting the host invalidates the live session ID.

Each discovered entry also offers **Export reference**. The resulting
`gui-checkpoint-reference-v1` JSON file contains only the opaque ID, campaign,
seed, committed-transition count, and archive/legacy source. Choose **Import
reference** to fill the existing ID field in another browser session; the
browser does not load, store, or reconstruct the checkpoint, and the host still
validates it when you choose **Load existing session** or **Restore host
checkpoint**. Invalid, stale, or extra-field references remain recoverable
errors.

Valid discovered entries also offer **Download host save**. This asks the host
to revalidate and serve the selected archive/legacy checkpoint as an
attachment; the browser does not serialize, parse, or load the downloaded
artifact.

## Stop the GUI

Return to the server terminal and press Ctrl-C. Active sessions held in process
memory end when the process stops; each autosaved competitive, stabilization, or
regional-affiliation checkpoint remains in the host application's sibling
checkpoint archive until that recovered session is ended. Older single-file
checkpoints remain readable as a migration fallback.

## Use a different port

If port 7878 is busy, choose another loopback port:

```bash
cargo run --bin vital-margin-gui -- --bind 127.0.0.1:8787
```

Open the exact URL printed by that process.

## Troubleshooting

### The browser says connection refused

Confirm the Cargo command is still running and that compilation completed. Open
the printed URL rather than a bookmarked port from an older run.

### The terminal says the address is already in use

Another process is using that port. Stop the older GUI host or use the alternate
port command above.

### I see demo data and Start says no host is configured

You opened `gui/index.html` directly or used a generic static file server. Stop
that server and run `cargo run --bin vital-margin-gui`; only the Rust GUI host
injects the live adapter.

### The seed is rejected

Use a non-negative whole number within JavaScript's safe integer range. Seed
`42` is the recommended first run.

### Validation rejects my draft

The month has not advanced. Read the validation message, reduce or revise the
draft to fit visible resources and command constraints, then validate again.

### Submission or refresh fails

The interface keeps the last successfully rendered session. Use **Retry current
read** when offered. If submission was rejected, revise and validate again. Do
not assume a month committed unless a resolution or refreshed host response is
shown.

### An existing session ID is unknown

The ID may belong to a different host, may have no explicit checkpoint, or may
be typed incorrectly. Manual Load remains explicit and does not automatically
hydrate an unknown ID. Only a browser-refresh recovery with a stored opaque ID
attempts one host checkpoint load after an unknown live-session response. If
that also fails, start a new session or enter a matching saved ID; no
replacement session is created.

### The browser was refreshed

When browser storage is available, the GUI retains only the opaque host-issued
session ID and attempts the normal host read after refresh. If the live session
is unknown, it tries the host checkpoint load once; this recovers only an
explicitly saved competitive session from the same host's configured file.
Stale or unmatched IDs are cleared with written guidance, while transient
failures preserve the ID for retry. Browser storage never contains commands,
observations, outcomes, hashes, or true state.

The repository retains a bounded Firefox/Marionette smoke as historical
technical evidence. It exercises one
explicit checkpoint save and one refresh against the live loopback host. It
launches each of the three supported campaigns, runs the visible Hold path
through all 24 competitive months, and runs the visible unified action cards
through the five stabilization and six regional-affiliation stages,
including host autosaves, history/replay, and terminal debriefs. It is not an
active support task and does not certify Firefox support, alternative action
values, WebKit, real hardware, audio decoding, or human accessibility/usability.

### Audio is silent

Select **Enable audio**, check browser/tab mute settings, raise Master and the
relevant channel volume, and return focus to the page. Continue with the written
equivalents if Web Audio is unavailable.

### Settings reset after restarting the browser

The GUI keeps settings in local browser storage when available, but private
browsing, blocked storage, or browser policy can make them session-local. Set
the preferences again after starting a session; this does not affect the host
session or replay.

### Text or motion is difficult to follow

Choose **Large** text, enable **Reduced motion**, and use the written resolution
controls (**Skip to result** or **Review all**) when pacing is distracting. The
host result remains unchanged.

## Scope, safety, and limitations

This is a fictional educational simulation and research prototype. It is not a
calibrated policy forecast or an operational, clinical, financial, regulatory,
or legal decision tool. The current rules, seed, commands, and explicit
stochastic inputs produce a bounded game outcome; they do not estimate what a
real institution, policy, payer, workforce, or community will do.

The GUI is a local loopback client. Active session state is in-memory during the
process lifetime; the host also keeps durable checkpoint archives; browser
refresh recovery may retain only
the opaque host session ID and reload the same running host process, while a
stopped/restarted host can discover explicit archives. Competitive actions and
campaign-coverage decisions remain host-owned. The host remains
authoritative, and actor-specific observations intentionally omit private rival
state and unresolved hidden inputs. Current technical checks do not replace
human accessibility, educational, audio-quality, provenance, resemblance,
browser/device, full-campaign, persistence, or public-release review. Do not
use the game to make real-world decisions or infer that a fictional institution
represents a real organization or person.
