import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-first-session-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"

EXPECTED_SOURCE_CONTRACT = {
  "player_guide": (
    "docs/guides/gui-how-to-play.md",
    "# How to Play in GUI Mode",
  ),
  "launch_markup": (
    "gui/index.html",
    'id="session-launch-form"',
  ),
  "launch_client": (
    "gui/app.mjs",
    "createSessionLauncher",
  ),
  "first_month_flow": (
    "gui/first-month.mjs",
    "FIRST_MONTH_FLOW_SCHEMA",
  ),
  "campaign_first_session_flow": (
    "gui/first-month.mjs",
    "CAMPAIGN_COVERAGE_FLOW_SCHEMA",
  ),
  "launch_test": (
    "tests/test_gui_session_launch.py",
    "test_launcher_start_and_existing_load_use_host_boundary",
  ),
  "first_month_sequence_test": (
    "tests/test_gui_first_month.py",
    "test_host_adapter_sequence_reaches_continue_and_rejection_stays_recoverable",
  ),
  "campaign_first_session_test": (
    "tests/test_phase12_live_campaign_coverage.py",
    "test_campaign_coverage_rail_advances_only_after_host_refresh",
  ),
  "recovery_guidance": (
    "docs/guides/gui-how-to-play.md",
    "Use **Retry current read** when offered.",
  ),
}


class Phase131FirstSessionBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_source_contract_markers_are_independently_anchored(self):
    self.assertEqual(
      self.ledger["schema_version"], "phase13.1-first-session-boundary-v1"
    )
    self.assertEqual(
      self.ledger["status"], "complete-current-technical-first-session-boundary-only"
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      normalized_marker = " ".join(marker.split())
      self.assertIn(normalized_marker, source_text, key)

  def test_launch_and_flow_contracts_keep_host_authority_and_stages_visible(self):
    html = (ROOT / "gui" / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    flow = (ROOT / "gui" / "first-month.mjs").read_text(encoding="utf-8")
    for marker in (
      'id="session-campaign"',
      'value="competitive-regional-v1"',
      'id="session-seed"',
      'id="session-difficulty"',
      'id="session-start"',
      'id="session-load"',
      'id="session-launch-status"',
      'aria-live="polite"',
    ):
      self.assertIn(marker, html)
    for marker in (
      "startSession",
      "requestedSessionId",
      "validateTurn",
      "submitTurn",
      "getResolution",
      "getPresentation",
    ):
      self.assertIn(marker, app)
    for marker in (
      '"start"',
      '"inspect"',
      '"draft"',
      '"validate"',
      '"submit"',
      '"resolution"',
      '"continue"',
      '"choose"',
      '"review"',
      "campaign-coverage-first-session-v1",
    ):
      self.assertIn(marker, flow)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "transition_competitive"):
      self.assertNotIn(forbidden, app)

  def test_ledger_claims_are_exactly_bounded_to_the_tested_path(self):
    self.assertEqual(
      self.ledger["technical_path"],
      [
        "launch or load one of the supported host campaigns",
        "competitive sessions inspect actor-visible briefing, market, resources, facilities, workforce, payer, and rival signals",
        "competitive sessions draft and host-validate contextual actions",
        "competitive sessions submit a validated month through the host boundary",
        "campaign-coverage sessions inspect visible campaign stage, actors, processes, decisions, history, and debrief",
        "campaign-coverage sessions choose a host-shaped decision and review the committed stage",
        "continue from the refreshed actor-visible observation or campaign stage",
        "recover from rejected submissions, refresh failures, storage limits, audio limits, and pacing friction",
      ],
    )
    self.assertEqual(
      self.ledger["findings"],
      {
        "launch_and_existing_load_are_host_bound": True,
        "seven_first_month_stages_are_source_bound": True,
        "five_campaign_coverage_first_session_stages_are_source_bound": True,
        "campaign_coverage_acceptance_requires_host_refresh": True,
        "written_recovery_guidance_is_present": True,
        "limitations_and_actor_visibility_are_present": True,
        "human_first_time_user_evaluation": False,
        "human_accessibility_and_educational_review": False,
      },
    )
    self.assertEqual(
      self.ledger["authority_boundary"],
      "The Rust host owns session creation, campaign decisions, validation, submission, resolution, history, and refreshed observations; the browser stores only local presentation preferences and draft UI state.",
    )
    self.assertEqual(
      self.ledger["limits"],
      [
        "This closes the current repository-owned technical first-session path boundary only.",
        "It does not establish first-time-user comprehension, task completion, human accessibility, educational usability, browser/device quality, or classroom readiness.",
        "The broader First-session workflow complete roadmap item remains open for structured human evaluation.",
      ],
    )

  def test_player_guidance_covers_first_session_and_recovery(self):
    guide = " ".join(
      (ROOT / "docs" / "guides" / "gui-how-to-play.md")
      .read_text(encoding="utf-8")
      .split()
    )
    for marker in (
      "cargo run --bin vital-margin-gui",
      "Start competitive regional session",
      "Competitive sessions track seven action handoffs",
      "five campaign-coverage handoffs",
      "Check plan",
      "Commit month",
      "Skip to result",
      "Review all",
      "Retry current read",
      "The host remains authoritative",
      "Do not use the game to make real-world decisions",
    ):
      self.assertIn(marker, guide)

  def test_roadmap_keeps_technical_and_human_first_session_gates_distinct(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] First-session workflow complete.", normalized)
    self.assertIn("[x] Current technical first-session path documented and recoverable.", normalized)
    limits = " ".join(self.ledger["limits"]).lower()
    for marker in (
      "first-time-user comprehension",
      "human accessibility",
      "educational usability",
      "structured human evaluation",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
