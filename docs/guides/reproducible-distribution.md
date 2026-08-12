# Reproducible Distribution

## Decision

The canonical distribution unit for v0.14.3 is an exact Git source checkout
of this repository. The checkout is identified by its package version and
commit SHA, and it is built with the stable Rust toolchain and Cargo. The
repository itself is the reproducibility package; this decision does not
publish a prebuilt binary, archive, installer, container, registry package, or
release tag.

The source checkout supports the CLI campaigns and the loopback GUI host. The
GUI host embeds its current browser module graph and catalogs, so the live GUI
does not need external browser modules or runtime asset downloads. The first
Cargo build may still need network access to resolve dependencies unless those
dependencies are already cached.

## Required checkout contents

An exact reproducible checkout retains these tracked inputs:

- `Cargo.toml`, `Cargo.lock`, `src/`, and `LICENSE`;
- the versioned scenario files under `scenarios/`;
- `gui/` and the approved presentation files under `assets/`;
- `tests/`, including replay and presentation fixtures;
- `scripts/` for release, documentation, asset, offline, and compatibility
  checks; and
- the current contributor and player documentation under `README.md`,
  `docs/`, `SPEC.md`, and `ARCHITECTURE.md`.

The working `target/` directory, generated reports, temporary session saves,
and local replay exports are not required checkout inputs. A shared run should
record the checkout commit SHA, package version, campaign, seed, difficulty,
and the exported machine-readable replay artifact when applicable.

## Reproduce from a clean checkout

Clone the repository, check out the versioned commit supplied with the release
handoff, and run the following read-only repository checks from its root:

```bash
python3 scripts/check_release_metadata.py
python3 scripts/check_documentation_links.py
python3 scripts/check_offline_availability.py
python3 scripts/check_browser_compatibility.py
python3 scripts/check_device_performance.py
python3 scripts/validate_assets.py
python3 scripts/validate_asset_security.py
python3 scripts/sanitize_svg_metadata.py --check-release
python3 scripts/verify_asset_release.py --check
python3 scripts/generate_asset_credits.py --check
python3 scripts/validate_generation_metadata.py
python3 scripts/audit_visual_audio_contract.py
python3 -m unittest discover -s tests
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

The `--check`, `--check-release`, and metadata/report commands above must not
rewrite tracked release outputs. Confirm the final worktree is clean after the
checks. The existing release metadata check verifies the package version in
`Cargo.toml`, `Cargo.lock`, `README.md`, and the first `CHANGELOG.md` heading.

## Run the distributed surfaces

For the CLI:

```bash
cargo run
```

For the live GUI:

```bash
cargo run --bin vital-margin-gui
```

The live GUI supports `competitive-regional-v1`, `stabilization-v1`, and
`regional-affiliation-v1` and binds to a
loopback address. The supported browser evidence covers Chromium evergreen
desktop version 120 or newer with ECMAScript modules, `fetch`, native SVG, and
CSS Grid. Web Audio and local presentation preferences remain optional.

Firefox and WebKit are not runtime-certified by this contract. The repository
records a bounded 1024×768 reduced-capability browser proxy for the current
low-power checklist, but it is not a real-device, battery, thermal, memory, or
frame-rate certification. Legacy non-module browsers, cross-platform
performance, and lived accessibility remain outside the current evidence
boundary. When audio is unavailable, visible and written equivalents remain
the authoritative meaning.

Historical packet wording retained for source parity: Chromium surface; Firefox and WebKit are not certified yet.

## Deferred distribution work

The following require a separate release decision and are not implied by this
source-checkout contract:

- prebuilt binaries, downloadable archives, installers, containers, or package
  registry publication;
- release tags, deployment, hosted services, or external runtime assets;
- Firefox/WebKit certification or real low-power-device measurements;
  these remain deferred and non-certified;
- service-worker or browser-cache persistence; and
- human accessibility, usability, learning, or classroom-effectiveness claims.
