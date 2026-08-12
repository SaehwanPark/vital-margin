# Vital Margin

Vital Margin is a fictional, deterministic strategy game about
leading a nonprofit US health system while finance, workforce, policy,
community, and market pressures pull in different directions. You make the
decision; the host reports what was visible, what changed, and what remains
uncertain.

The current release is a playable Rust prototype at v0.14.14. It is distributed
as source code: there is no installer or prebuilt binary. The GUI is the easiest
way to see the game, while the CLI remains a complete alternative.

![Live competitive Brief workspace with executive metrics, the regional board, and public rival signals](docs/images/readme/gui-competitive-brief.png)

## Play now

The shortest first run is the GUI stabilization tutorial. Install the
prerequisites using the [beginner installation guide](docs/guides/installation.md),
then:

```bash
cargo run --bin vital-margin-gui
```

Keep that terminal open and visit the printed URL, normally
`http://127.0.0.1:7878`. Choose **Stabilization tutorial** (`stabilization-v1`)
and seed `42`. Follow the Brief → Decide → Resolve → Review workspace; the
tutorial has five abstract executive decisions and does not ask for a calendar
duration or difficulty.

If you prefer a terminal, run `cargo run`, choose `1` for
`stabilization-v1`, choose beginner guided choices (`b`), and accept seed `42`.
The [CLI guide](docs/guides/how-to-play.md) explains the prompts and the
competitive command vocabulary.

## Screenshots from live play

These maintained documentation captures show actor-visible state from the live
loopback host. They are not runtime or release assets.

| GUI decision workspace | GUI terminal review |
| --- | --- |
| ![Seed-42 stabilization tutorial decision workspace showing a host-provided action](docs/images/readme/gui-stabilization-decide.png)<br>*Stabilization tutorial: choose one visible action.* | ![Terminal regional-affiliation Review state with six stages, final status, commitments, and decision-quality explanation](docs/images/readme/gui-affiliation-debrief.png)<br>*Regional affiliation: the true terminal debrief.* |

| CLI beginner choice | CLI competitive report |
| --- | --- |
| ![Beginner-guided stabilization choice without local usernames or filesystem paths](docs/images/readme/cli-stabilization-beginner.png)<br>*CLI stabilization: guided first choice.* | ![Competitive executive report with the monthly command prompt](docs/images/readme/cli-competitive-report.png)<br>*CLI competitive: report and monthly prompt.* |

Capture details and SHA-256 checksums are in the
[screenshot manifest](docs/images/readme/README.md).

## Choose a campaign

The campaigns are alternatives, not sequential chapters. Progress, decisions,
and checkpoints do not transfer between them.

| Campaign | Purpose | Length | Interface behavior | Difficulty applicability | Recommended audience |
| --- | --- | --- | --- | --- | --- |
| **Stabilization tutorial** (`stabilization-v1`) | Five abstract executive decisions about access, capacity, workforce, policy, coalition, and rival pressure. | Five decisions; no calendar duration. | GUI shows one host-provided action card at each stage; the CLI alone offers beginner guided choices. | No difficulty setting. | Everyone's first run; especially new players. |
| **Competitive regional market** (`competitive-regional-v1`) | A separate 24-month regional-market campaign where your monthly plan meets simultaneous AI-rival actions and lagged public information. | 24 months. | GUI uses the monthly action rail and Brief/Decide/Resolve loop; CLI accepts command batches. | Easy, Normal, Hard, and Expert tiers change rival count and monthly AP. | Players ready for a longer, more information-limited strategy loop. |
| **Regional affiliation** (`regional-affiliation-v1`) | A separate six-stage nonprofit-partner scenario covering assessment, posture, commitments, review, and early integration or independence. | Six stages. | GUI and CLI expose one bounded stage decision at a time. | No AI rivals or difficulty tiers; not legal, valuation, antitrust, or transaction advice. | Players who want an institutional fit and obligation scenario. |

Competitive is not network multiplayer: rivals are local AI or bounded MCP
agents. Every campaign is deterministic for the same seed and choices, while
actor-visible observations remain separate from the engine's true state.
The regional-affiliation scenario is not legal, valuation, antitrust, or transaction advice.

## Installation in one minute

This is a source-only checkout. Install Rust/Cargo, download the repository as
a GitHub ZIP (lowest-friction path) or clone it for repeatable updates, open a
terminal in the repository folder, and run the GUI command above. The full
macOS, Windows, and Linux walkthrough—including Cargo verification, updates,
checkpoint cautions, and recovery FAQ—is in
[Installation and first launch](docs/guides/installation.md).

## Common first-run fixes

- **`cargo` or `git` is not found:** install the tool from the official links
  in the [installation guide](docs/guides/installation.md), close the terminal,
  open a new one, and try again.
- **Connection refused:** the GUI host is not running or compilation has not
  finished; keep the Cargo terminal open and use the exact printed URL.
- **The page shows demo data:** you opened `gui/index.html` directly. Start
  `cargo run --bin vital-margin-gui` for live play.
- **Port 7878 is busy:** stop the other GUI host or use
  `cargo run --bin vital-margin-gui -- --bind 127.0.0.1:8787`.
- **A saved checkpoint seems missing:** checkpoints belong to the host and
  source checkout; use the GUI's saved-checkpoint finder before starting over.

See the complete [troubleshooting FAQ](docs/guides/installation.md#faq) and
[GUI recovery guide](docs/guides/gui-how-to-play.md) for more cases.

## Current boundaries

This is a research and educational prototype, not a finished educational
release and not a model of any real institution. Game units and thresholds are
documented abstractions, not calibrated forecasts. Automated and AI-agent
playtests establish technical evidence only; they do not establish human
learning, lived accessibility, classroom effectiveness, legal conclusions, or
policy validity. Do not use the game for operational, clinical, financial,
regulatory, legal, or policy decisions.

The live host owns commands, legality, transitions, history, replay,
checkpoints, and debriefs. The declared browser target is Chromium evergreen
desktop. Firefox, WebKit/Safari, mobile, and legacy-browser support are
deferred and non-certified. Contributor-only browser inspection notes live in
the [contributor documentation index](docs/README.md), not in the player path.

## Learn more

### Players

- [Installation and first launch](docs/guides/installation.md)
- [How to Play in the CLI](docs/guides/how-to-play.md)
- [How to Play in GUI Mode](docs/guides/gui-how-to-play.md)

### Project and contributors

- [Contributor documentation index](docs/README.md)
- [Project specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Proposal](docs/proposal.md)
- [Roadmap](docs/roadmap.md)
- [Design principles](docs/design_principles.md)
- [Changelog](CHANGELOG.md)

## License

[GPL-3](LICENSE)
