# Repository Agents Guide

Keep this file short and repo-wide. Detailed workflow rules live in
`.agents/skills/` and `docs/harness/`.

## What
- This repository is Vital Margin, a Rust health-policy strategy game with a
  reference CLI, bounded MCP adapter, and active loopback browser GUI. The
  player leads a fictional nonprofit US health system.
- Canonical project docs are `README.md`, `docs/proposal.md`,
  `docs/roadmap.md`, and `docs/design_principles.md`.
- The durable design boundaries are deterministic core transitions, explicit
  stochastic inputs, true state versus actor observations, immutable history,
  strategic non-player actors, visible assumptions, and educational debriefing.

## Why
- The project models health-policy outcomes as strategic interaction among
  institutions, not as direct policy levers or single-metric optimization.
- Scope control matters: credible vertical slices, inspectable mechanisms, and
  documented assumptions come before broad framework expansion.

## How
- Before major changes, read the canonical docs and the harness team spec at
  `docs/harness/vital-margin/team-spec.md`.
- Use repo-local skills only for project-specific health-policy simulation and
  actor-visible presentation workflows. Use global skills for generic
  functional programming, Rust quality, UX, code review, comments, spec
  maintenance, planning, and release preparation.
- Current Rust commands: `cargo fmt`, `cargo test`, and `cargo run` (or
  `cargo run --bin vital-margin-gui`).
- Current GUI development targets the host-backed Setup/Brief/Decide/Resolve/
  Review workspace and all three launchable campaigns. Chromium evergreen is
  the default browser target; Codex browser inspection is development evidence.
- Future development uses deterministic automated and AI-agent checks. Human
  learning, lived accessibility, legal-quality, and policy-validity limits are
  recorded honestly but do not form routine stop gates. Unverifiable assets use
  generic fallbacks.
- Do not invent build, CI, scenario, data, or release conventions until the
  roadmap phase calls for them and they are documented.
- You may install any necessary dependencies or tools via `cargo install`.
- When you cannot find CLI tools, use `which <tool>` to find the installed path.
- Do bookkeeping lessons learned into `LESSONS.md` and keep revisitng during development to avoid repeating mistakes.
- You may use **emojis** in the game display when necessary.
- Use tabsize of **2 spaces** throughout the codebase.
- Follow the principle of **simple code writing**
- Bump up project version: increase version number by 0.0.1 for each PR or PR-equivalent change. increase 0.1 for major feature releases or meaningful accumulated changes. no need to carry over, but when bumping up higher digits, reset the lower digits to 0.

## Versioning Policy

The project follows a modified semantic versioning format: `x.y.z`, where **x**, **y**, and **z** are integers.

### Increment Rules

* **Patch (`z`):** Increment by `1` for every Pull Request (PR) or PR-equivalent change.
* **Minor (`y`):** Increment by `1` when the project receives significant improvements or feature updates.
* **Major (`x`):** Increment by `1` for categorical, architectural, or structurally different changes.

### Reset & Carrying Rules

* **No Automatic Carry-Over:** Lower digits do **not** automatically roll over or carry over when a higher digit is incremented, nor do they roll over when reaching `10` (e.g., version `0.1.9` increments to `0.1.10`, not `0.2.0`).
* **Digit Initialization:** When a higher-order digit (**x** or **y**) is incremented, all lower-order digits are explicitly reset to `0` (e.g., incrementing `y` resets `z` to `0`; incrementing `x` resets both `y` and `z` to `0`).
