# How to Play in GUI Mode

[Documentation Home](../index.md) | [Installation Guide](installation.md) | [CLI Guide](how-to-play.md) | [Strategy & Mechanics](strategy-and-mechanics.md) | [Glossary](../reference/glossary.md)

---

## 🖥️ Overview of the Browser Interface

The Vital Margin Live GUI delivers a rich, visual executive command center
hosted locally by a high-performance Rust web server. It runs entirely inside
your local browser without requiring external cloud accounts, remote servers,
or database configurations.

```
+----------------------------------------------------------------------------------------------------+
|                                    VITAL MARGIN EXECUTIVE DESK                                     |
+----------------------------------------------------------------------------------------------------+
| [ BRIEF ]                 | [ DECIDE ]                | [ RESOLVE ]               | [ REVIEW ]     |
| Executive KPIs            | Action Catalog            | Simultaneous Resolution   | History Log    |
| Regional Board & Map      | Plan Drafting Rail        | Attributed Effects        | Debrief Ledger |
| Market & Rival Signals    | Host Validation Check     | Animation Controls        | Replay Player  |
+----------------------------------------------------------------------------------------------------+
```

The recommended first session is the 5-turn **Stabilization Tutorial**
(`stabilization-v1`). The **Competitive Regional Market**
(`competitive-regional-v1`) and **Regional Affiliation**
(`regional-affiliation-v1`) campaigns are full standalone alternatives.

---

## ⚙️ System Requirements & Browser Target

- **Rust & Cargo:** Installed locally (see the [Installation Guide](installation.md)).
- **Supported Browser:** **Chromium evergreen desktop** (Chrome, Edge, Brave,
  Chromium 120+) with ECMAScript Modules enabled.
- **Experimental / Deferred:** Firefox and WebKit/Safari support are deferred
  and non-certified.
- **Audio:** Optional Web Audio API (starts muted until enabled by user gesture).

---

## 🚀 Launching the GUI

1. Open a terminal in the repository root directory.
2. Launch the local GUI server:
   ```bash
   cargo run --bin vital-margin-gui
   ```
3. Keep the terminal running. Once compiled, the host prints the local URL:
   ```text
   Vital Margin GUI: http://127.0.0.1:7878
   ```
4. Open `http://127.0.0.1:7878` in your Chromium browser.
5. Choose **Stabilization tutorial** (`stabilization-v1`), accept seed `42`, and
   click **Start selected session**.

> [!WARNING]
> Do **not** double-click or open `gui/index.html` directly from your file
> manager! Opening the static HTML file bypasses the live Rust simulation host and
> displays static mock demonstration data. Always run `cargo run --bin vital-margin-gui`.

---

## 🧭 The Four Workspaces

The GUI organizes your leadership workflow into four dedicated workspaces:

### 1. 📋 Brief Workspace
- **Executive Metric Cards:** Real-time visibility into Cash Runway, Bed
  Occupancy, Nursing Vacancy, Operating Margin, and Regulatory Standing.
- **Regional Board Map:** Interactive SVG map displaying your primary hospital,
  satellite clinics, outpatient centers, and competing health systems.
- **Selected Entity Drawer:** Click on any facility or regional parcel to
  inspect its operational capacity, staffing levels, and service lines.
- **Public Intelligence Rail:** View public announcements, permit filings, and
  pricing signals from rival systems.
- **Acknowledge:** Click **Continue to decisions** when ready to proceed.

### 2. 🎯 Decide Workspace
- **Action Catalog:** Browse available strategic moves categorized into
  Capital, Workforce, Market, and Payer domains.
- **Action Configuration Cards:** Open any card to adjust parameters (e.g.,
  selecting recruit headcount, investment amount, or capital project type).
- **Monthly Draft Plan Rail:** Actions are staged in a local draft queue before
  commitment.
- **Check Plan (Host Validation):** Click **Check plan** to verify your draft
  against Action Point (AP) limits, cash reserves, and political capital. The
  host checks constraints and provides clear feedback if adjustments are
  needed.
- **Commit Month:** Once validated without errors, click **Commit month** to
  submit your decisions to the simulation core.

### 3. ⚡ Resolve Workspace
- **Simultaneous Action Resolution:** Watch the engine resolve your moves
  alongside NPC responses and rival actions.
- **Attributed Effects Ledger:** Clear before-and-after deltas showing how your
  actions and external events impacted metrics.
- **Animation Controls:** Play, pause, step through, or click **Skip to
  result** for instant written resolution.
- **Next Turn:** Click **Continue to next brief** to enter the next month.

### 4. 🎓 Review Workspace
- **Committed History:** Scroll through the immutable append-only record of
  every past decision and resolution.
- **Replay Scrubber:** Step forward and backward through past turns to audit the
  evolution of your health system.
- **Decision-Time Context:** Expand any historical turn to view the exact
  information visible to you when you made that choice.
- **Terminal Debrief:** Comprehensive post-game causal debrief evaluating
  *Decision Quality* vs. *Outcome Quality*.

---

## 💾 Saved Checkpoints & Session Management

Vital Margin provides robust session persistence:

```
[ Active Session ] --(Autosave on Commit)--> [ Host Checkpoint Archive ]
                                                     |
                                            [ Find Checkpoints ]
                                            [ Export Reference ]
                                            [ Download Save    ]
```

- **Automatic Autosave:** The host automatically writes a checkpoint after
  every committed turn.
- **Manual Checkpoint Save:** Click **Save host checkpoint** in the session
  drawer at any time.
- **Finding Saved Checkpoints:**
  1. Click **Find saved checkpoints** under Saved Host Checkpoints.
  2. Inspect discovered sessions (showing campaign, seed, turn count, and
     opaque session ID).
  3. Click **Use this session ID**, then select **Load existing session**.
- **Export / Import References:**
  - Click **Export reference** to save a lightweight `gui-checkpoint-reference-v1`
    JSON metadata descriptor.
  - Click **Import reference** in another browser window to populate the session ID.
- **Download Host Save:** Click **Download host save** to save the raw,
  host-validated binary checkpoint archive file to your disk.

---

## ♿ Settings, Audio & Accessibility

Open the **Settings, audio, and help** utility drawer at any time:

### Accessibility & Visual Settings
- **Low-distraction mode:** A safe, one-click preset that locks Reduced Motion,
  Large Text, visible cue explanations, muted audio, and reduced notifications.
- **Reduced motion:** Completely disables non-essential transitions and pacing;
  presents all results as immediate written text.
- **Text size:** Toggle between **Standard** and **Large** font scaling.
- **Visible cue explanations:** Displays clear text descriptions for all audio
  cues and ambient changes.

### Web Audio Controls
- **Enable audio:** Unmutes the Web Audio synthesizer (requires an initial user
  click).
- **Independent Sliders:** Fine-tune Master Volume, Background Music, Interface
  Feedback, Event Cues, and Ambient Audio.
- **Audio Modes:** Toggle **Mute audio**, **Cues only** (interface sounds
  without music), or **Music only mute**.

---

## 🔧 GUI Troubleshooting & Quick Fixes

### "Connection Refused" when visiting `http://127.0.0.1:7878`
- **Cause:** The Cargo server process is either still compiling or has stopped.
- **Fix:** Check your terminal. Ensure `cargo run --bin vital-margin-gui` has
  finished building and is actively running.

### "Address already in use (port 7878)"
- **Cause:** Another instance of Vital Margin (or another application) is using
  port 7878.
- **Fix:** Launch on an alternate port:
  ```bash
  cargo run --bin vital-margin-gui -- --bind 127.0.0.1:8787
  ```
  Then open `http://127.0.0.1:8787` in your browser.

### "Validation Failed: Too many concurrent projects"
- **Cause:** You drafted a capital project while 2 construction projects are
  already active.
- **Fix:** Remove the new project card from your draft rail. Wait until one
  existing project completes before launching another.

### "Audio is silent"
- **Cause:** Web browsers require an explicit user gesture before enabling Web
  Audio.
- **Fix:** Open **Settings, audio, and help**, click **Enable audio**, and verify
  your system and browser tab volume.

---

## 📖 Related Guides

- [How to Play in the CLI](how-to-play.md)
- [Comprehensive Strategy & Mechanics Guide](strategy-and-mechanics.md)
- [Installation and First Launch](installation.md)
- [Terminology Glossary](../reference/glossary.md)
