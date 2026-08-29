# Handoff: Player Manuals, Guides Refinement & GitHub Pages Migration

- **Branch:** `feat/player-manuals-and-github-pages`
- **Date:** 2026-08-28
- **Task Class:** Document-only enhancement (no version bump, no codebase logic changes).

## Summary of Changes

1. **Player Documentation Portal & GitHub Pages Landing (`docs/index.md`):**
   - Built a comprehensive documentation portal designed for both web-hosted GitHub Pages (`https://saehwanpark.github.io/vital-margin/`) and repository browsing.
   - Includes quickstart guides, 3-campaign comparison matrix, core loop diagram, and guide index.

2. **GitHub Pages Deployment Workflow & Configuration:**
   - Added `docs/_config.yml` with Jekyll and theme settings.
   - Added `.github/workflows/pages.yml` to automatically build and deploy the documentation site to GitHub Pages on pushes to `main`.
   - Enabled GitHub Pages build via `gh api` with workflow deployment.

3. **Player-Facing Manuals & Guides Refinement:**
   - `docs/guides/installation.md`: Clear, beginner-friendly instructions for macOS, Windows (PowerShell), and Linux, verifying Cargo, ZIP vs Git workflows, and comprehensive troubleshooting.
   - `docs/guides/how-to-play.md`: Full gameplay breakdown of the 3 campaigns (Stabilization Tutorial, 24-Month Competitive Regional Market, Regional Affiliation), complete command grammar and parameter catalog, and step-by-step example walkthrough.
   - `docs/guides/gui-how-to-play.md`: Detailed visual guide covering the Brief, Decide, Resolve, and Review workspaces, action card drafting, host validation checks, autosaves and checkpoint recovery, accessibility presets (Low-distraction mode, Reduced motion, Large text), and Web Audio controls.
   - `docs/guides/strategy-and-mechanics.md`: Brand new strategic playbook detailing the five operational pillars (Finance & Cash Runway, Workforce & Vacancy, Commercial/Public Payers, Public Legitimacy vs Follow-Through, Rival Dynamics), four tested strategic archetypes, and emergency triage playbooks.
   - `docs/reference/glossary.md`: Enriched terminology definitions covering simulation core, executive resources, actor roles, commands, and debrief metrics.

4. **Navigation & Entry Points:**
   - Synchronized `README.md` and `docs/README.md` to link to the new documentation portal and strategy guide.

## Verification
- `python3 scripts/check_documentation_links.py`: Passed (499 files checked).
- `python3 scripts/check_documentation_currentness.py`: Passed.
- `python3 scripts/check_release_metadata.py`: Passed (v0.14.14).
- `cargo fmt --check`: Passed.
- `cargo clippy --all-targets -- -D warnings`: Passed.
- `cargo test`: Passed (388 library tests + integration tests).
