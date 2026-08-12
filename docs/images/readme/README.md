# README screenshot manifest

These five lossless PNGs are maintained documentation screenshots, not runtime
or release assets. They are documentation screenshots rather than runtime/release assets. They were captured from the checked-out source on 2026-08-04
after compiling package version `0.14.13` on branch
`codex/feat/player-first-readme-v0.14.13`.

## Capture record

- Source revision: base commit `30cbb68e776054ce4ccc645f5b53ea2dad63ce51` plus
  the documentation/version working tree on this branch.
- GUI method: live Rust loopback host (`cargo run --bin vital-margin-gui`) in
  Chromium evergreen, 1440×900 viewport, 100% zoom, seed `42`.
- CLI method: live `cargo run` in a macOS Terminal pseudo-terminal through
  `script -q /dev/null`, Normal difficulty and seed `42` for competitive play.
  Both CLI captures used the same readable 120×30, 12-point terminal profile;
  the window frame was cropped to the content area (1720×940) to remove the
  shell title/path and desktop margins. No username or local filesystem path is
  visible in the resulting images.
- GUI cropping: none; each image is the 1440×900 viewport. The affiliation
  image is a true terminal Review state after six committed stages with the
  debrief expansion open; no decision controls or hidden/private state are
  shown. The stabilization image is the seed-42 Decide workspace before the
  visible action is committed. The competitive hero shows the live Brief
  regional board, player metrics/overlays, and public rival cards.
- CLI cropping: centered to the 1720×940 Terminal content rectangle; the
  source frame was not edited beyond removing the title bar and margins.
- Provenance boundary: these are actor-visible live-state captures, not static
  demo fixtures, historical evaluation rasters, hidden state, private rival
  actions, or instructor-only detail.

## Files and checksums

| File | Campaign / stage | Seed and difficulty | Viewport or terminal dimensions | SHA-256 |
| --- | --- | --- | --- | --- |
| `gui-competitive-brief.png` | `competitive-regional-v1`, Brief month 1/24, regional board | `42`, Normal | 1440×900 at 100% | `7a729107675b28d13141d322339a0b2083aafe23f7eb9177011be69156dab884` |
| `gui-stabilization-decide.png` | `stabilization-v1`, Decide turn 1/5 | `42`, no difficulty | 1440×900 at 100% | `112677fe3b7e875cb8df616bb2f98ecedbc37b02dd81baf7d2508c85f52bacaa` |
| `gui-affiliation-debrief.png` | `regional-affiliation-v1`, terminal Review after six stages | `42`, no difficulty | 1440×900 at 100% | `5efeadec1d1dbb59640607a2e6ea635d5e22ae0968cafd4223efc72ee15ce66b` |
| `cli-stabilization-beginner.png` | `stabilization-v1`, turn 1 beginner choice | `42`, beginner guided | 1720×940 cropped from 120×30 | `a38f1160bb9b00cf9f5c47a6202ce73386b661b44fa2857f0fe77cfb32bfa36e` |
| `cli-competitive-report.png` | `competitive-regional-v1`, month 1 report and command prompt | `42`, Normal | 1720×940 cropped from 120×30 | `c1dc541fe273340b9d3ab27d9c3dc474d4f91400551ccac58c46c567fde1d608` |

Recheck a checksum with:

```bash
shasum -a 256 docs/images/readme/*.png
```
