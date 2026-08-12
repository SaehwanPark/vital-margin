# Contributor Documentation

This index separates current instructions from dated evidence. Current
documentation must describe the checked-in code and tests; historical and
workspace records preserve what was known at an earlier slice and are not
current implementation instructions.

## Document authority

| Class | Location | Authority |
| --- | --- | --- |
| Maintained product direction | `README.md`, `docs/proposal.md`, `docs/roadmap.md`, `docs/design_principles.md` | Current intent and scope |
| Software SDD | `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md` | Current state, boundaries, and release history |
| Active design/reference | `docs/design/`, `docs/reference/`, `docs/research/`, `docs/validation/` | Current mechanics, terminology, evidence, and workflows |
| GUI/presentation | `gui/README.md`, `docs/guides/gui-how-to-play.md`, visual/audio roadmap, asset READMEs | Current GUI contracts and player/contributor operation |
| ADR / decision records | `docs/decision-records/` | Point-in-time decisions; later records supersede changed direction |
| Generated/registry records | `assets/`, generated credits, release manifests | Machine-produced or provenance-controlled outputs; do not hand-edit generated files |
| Historical/evaluation evidence | `docs/history/`, `docs/evaluation/`, `docs/blog-posts/` | Immutable prior findings, milestones, superseded plans, dated narratives, and point-in-time evidence packets |
| Workspace evidence | `_workspace/` | Dated handoffs and experiment artifacts; append current handoffs, do not rewrite prior slices |

## Software contributor path

1. Read [SPEC](../SPEC.md) and [ARCHITECTURE](../ARCHITECTURE.md).
2. Review the [core loop](design/core-loop-spec.md), [system boundary](design/system-boundary.md), and [MCP interface](reference/mcp-agent-interface.md) relevant to the change.
3. Use the [versioning policy](reference/versioning-policy.md) and
   [release metadata check](guides/contributor-release-check.md).
4. Consult the [decision records](decision-records/README.md) before changing
   an accepted boundary.
5. Run the documentation-currentness checker before committing documentation.

### Developer quickstart

Work from a clean checkout and keep the source-only workflow intact. The GUI
host is useful for presentation inspection, but it does not change the Rust
simulation or host authority:

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
python3 scripts/check_documentation_currentness.py
python3 scripts/check_documentation_links.py
python3 scripts/check_release_metadata.py
python3 -m unittest discover -s tests
```

For a live GUI smoke, run `cargo run --bin vital-margin-gui`, open the printed
`http://127.0.0.1:7878` URL in Chromium evergreen, and use seed `42`. Stop the
host with Ctrl-C. Read [ARCHITECTURE](../ARCHITECTURE.md), the
[versioning policy](reference/versioning-policy.md), and the
[changelog](../CHANGELOG.md) before changing public boundaries.

## GUI and presentation path

1. Read the current [GUI roadmap](visual_audio_enhancement_roadmap.md),
   [design principles](design_principles.md), and [presentation architecture](../ARCHITECTURE.md).
2. Confirm that every semantic visual/audio element has an actor-visible host
   source, written equivalent, safe unknown state, and replay-safe boundary.
3. Keep commands, legality, transitions, history, replay, checkpoints, and
   debriefs host-owned. Browser navigation, drafts, settings, motion, and audio
   remain presentation state.
4. Use the [GUI player guide](guides/gui-how-to-play.md) and
   [GUI technical reference](../gui/README.md) for current operation.
5. Treat Chromium evergreen desktop as the default browser target. The Codex in-app browser
   is a development inspection surface and its captures are
   technical evidence; non-default engines are deferred.

### Refreshing the maintained README screenshots

The five images in [`images/readme/`](images/readme/) are documentation
screenshots, not runtime assets. Refresh them only from the live loopback host:

1. Start the GUI host and open it in Chromium evergreen at 1440×900, 100% zoom.
2. Use seed `42`; capture the competitive Brief hero, stabilization Decide,
   and the true terminal affiliation Review/debrief state after all six stages.
3. Capture the CLI beginner stabilization choice and the competitive report at
   a consistent readable terminal size. Remove usernames and filesystem paths
   from the visible frame.
4. Do not expose hidden state, private rival actions, static demo fixtures, or
   instructor-only detail. Record campaign, stage, seed/difficulty, dimensions,
   capture method, revision, cropping, and SHA-256 in
   [`images/readme/README.md`](images/readme/README.md).

The [presentation contract](../_workspace/02_presentation_contract.md) and
[presentation QA](../_workspace/03_presentation_qa.md) explain the source-bound and
actor-visible boundaries used for these captures.

## Game and domain design path

Use the [glossary](reference/glossary.md), [actor cards](design/actor-cards.md),
[action catalog](design/action-catalog-draft.md), campaign briefs, scenario
format, [evidence registry](research/evidence-registry.md), and [workforce
ledger](research/workforce-ledger.md). Route breadth through the
[expansion proposal review](design/expansion-proposal-review.md).

## AI-native validation path

The active validation path uses deterministic MCP/GUI adapters, AI-agent
profiles, source-bound traces, replay/hash checks, accessibility-mode checks,
and presentation/domain QA. These establish technical and gameplay evidence,
not human learning, lived accessibility, legal clearance, calibration, balance,
or policy validity. Those limits are recorded honestly but do not stop routine
technical progression; unsafe or unverifiable assets remain excluded.

See the [playtesting protocol](validation/playtesting.md), [MCP playtesting
guide](guides/mcp-playtesting-guide.md), and repository-local [agent harness](harness/vital-margin/team-spec.md).

## Player guides

- [CLI guide](guides/how-to-play.md)
- [GUI guide](guides/gui-how-to-play.md)

## Historical context

The [history index](history/README.md) explains retained findings and why they
should not be treated as present-tense instructions.
