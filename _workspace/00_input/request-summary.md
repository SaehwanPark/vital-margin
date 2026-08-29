# Request Summary: Player Manuals, Guides & GitHub Pages Migration

- **Date:** 2026-08-28
- **Scope:** Documentation-only enhancement to player-facing manuals, guides, GitHub Pages migration, and end-to-end PR merge.
- **Roadmap Track:** Documentation & Player Onboarding.
- **Deliverables:**
  1. Refined, highly approachable player-facing guides:
     - `docs/guides/installation.md` (Installation and first launch)
     - `docs/guides/how-to-play.md` (How to Play - CLI & general gameplay)
     - `docs/guides/gui-how-to-play.md` (GUI player manual & workspace guide)
     - `docs/guides/strategy-and-mechanics.md` (Comprehensive player strategy & triage guide)
     - `docs/reference/glossary.md` (Terminology reference)
  2. GitHub Pages configuration & migration:
     - `docs/index.md` (Interactive player documentation portal homepage)
     - `docs/_config.yml` (Jekyll GitHub Pages configuration)
     - `.github/workflows/pages.yml` (Automated GitHub Pages build & deployment workflow)
  3. Seamless cross-document navigation, table of contents, and link validation.
  4. Full validation suite execution (`cargo test`, Python doc link/currentness checkers, release metadata checks).
  5. PR creation on `main` and autonomous squash merge.
- **Constraints:**
  - Strictly document-only changes (no version bumping, no Rust codebase logic edits).
  - 2-space indentation where applicable.
  - Simple, clear, and informative writing.
  - All doc links must be valid local relative links (no machine-local paths).
  - Preserve all currentness markers checked by `scripts/check_documentation_currentness.py`.
