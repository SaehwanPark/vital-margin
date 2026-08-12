#!/usr/bin/env python3
"""Validate bounded terminal-debrief runtime evidence."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-terminal-debrief-runtime-evidence.json"
EXPECTED_SCHEMA = "phase13.2-terminal-debrief-runtime-evidence-v1"
EXPECTED_STATUS = "complete-terminal-debrief-runtime-boundary-pending-human-review"
EXPECTED_VERSION = "0.13.99"
EXPECTED_URL = "http://127.0.0.1:7878/"
EXPECTED_TITLE = "Vital Margin — Executive Desktop"
EXPECTED_HASH = "61357596d8800592"
SESSION_PATTERN = re.compile(r"^session-[A-Za-z0-9_-]+$")
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}
EXPECTED_DEBRIEF_MARKERS = [
  "Final state hash:",
  "Final calendar:",
  "Final player tradeoff:",
  "Final player resources:",
  "Player: hold",
  "Operating result:",
  "Rival Northlake Health:",
  "[Private Action] (unobserved by you)",
  "Attributed mechanisms to inspect:",
  "Resolved events:",
  "Decision quality and outcome quality remain separate:",
]
EXPECTED_FORBIDDEN_CLAIMS = [
  "human visual debrief review complete",
  "educational usability review complete",
  "human accessibility review complete",
  "audio listening review complete",
  "audio quality approved",
  "Firefox/WebKit certified",
  "public release approved",
]
REQUIRED_FIELDS = {
  "schema_version",
  "status",
  "package_version",
  "roadmap_item",
  "observed_on",
  "observation",
  "terminal_surface",
  "renderer_contract",
  "review_boundary",
  "source_contract",
  "evidence_limits",
  "release_boundary",
}
EXPECTED_REVIEW_BOUNDARY = {
  "technical_terminal_debrief_observation_complete": True,
  "technical_player_debrief_boundary_complete": True,
  "technical_read_only_terminal_controls_complete": True,
  "human_visual_debrief_review_complete": False,
  "educational_usability_review_complete": False,
  "human_accessibility_review_complete": False,
  "audio_listening_review_complete": False,
  "browser_device_certification_complete": False,
  "public_release_approval": False,
}


def _require(condition: bool, message: str) -> None:
  if not condition:
    raise ValueError(message)


def _load_json(path: Path) -> object:
  return json.loads(path.read_text(encoding="utf-8"))


def _source_marker_is_valid(source: object) -> None:
  _require(isinstance(source, str) and ": " in source, "source markers must use 'path: marker'")
  relative, marker = source.split(": ", 1)
  path = Path(relative)
  _require(not path.is_absolute(), "source marker paths must be relative")
  resolved = (ROOT / path).resolve()
  _require(ROOT.resolve() in resolved.parents, "source marker path escapes repository root")
  _require(resolved.is_file(), f"source marker path is missing: {relative}")
  _require(marker in resolved.read_text(encoding="utf-8"), f"source marker is missing: {source}")


def _validate_loopback_url(url: object) -> None:
  _require(isinstance(url, str), "observation URL must be a string")
  parsed = urlparse(url)
  _require(parsed.scheme in {"http", "https"}, "observation URL must use HTTP(S)")
  _require(parsed.hostname in LOOPBACK_HOSTS, "observation URL must use a loopback host")
  _require(not parsed.username and not parsed.password, "observation URL must not include credentials")


def _validate_browser(browser: object) -> None:
  _require(isinstance(browser, dict), "browser observation must be an object")
  _require(
    set(browser) == {"name", "engine", "version", "platform", "user_agent", "protocol"},
    "browser fields are not exact",
  )
  _require(browser["name"] == "Chrome", "observed browser must be Chrome")
  _require(browser["engine"] == "Chromium", "observed browser engine must be Chromium")
  _require(browser["version"] == "150.0.0.0", "browser version must match the observed runtime")
  _require(browser["platform"] == "macOS", "browser platform must identify macOS")
  _require(
    isinstance(browser["user_agent"], str) and "Chrome/150.0.0.0" in browser["user_agent"],
    "browser user agent must bind the observed version",
  )
  _require(browser["protocol"] == "Chrome DevTools Protocol", "browser protocol must identify the runtime observation")


def _validate_observation(observation: object) -> None:
  _require(isinstance(observation, dict), "observation must be an object")
  _require(
    set(observation) == {
      "method",
      "url",
      "browser",
      "host_start",
      "committed_action",
      "repository_state_written",
      "host_session_started",
    },
    "observation fields are not exact",
  )
  _require(isinstance(observation["method"], str) and observation["method"], "observation method is required")
  _validate_loopback_url(observation["url"])
  _require(observation["url"] == EXPECTED_URL, "observation URL must match the GUI loopback route")
  _validate_browser(observation["browser"])

  host = observation["host_start"]
  _require(isinstance(host, dict), "host_start must be an object")
  _require(set(host) == {"status", "session_id", "demo_fixture"}, "host_start fields are not exact")
  _require(isinstance(host["status"], str) and host["status"].startswith("competitive regional session loaded: "), "host status must report a competitive session")
  _require(isinstance(host["session_id"], str) and SESSION_PATTERN.fullmatch(host["session_id"]), "host session ID must be opaque")
  _require(host["session_id"] in host["status"], "host status must bind its opaque session ID")
  _require(host["demo_fixture"] is False, "demo fixture must be absent after host start")

  action = observation["committed_action"]
  _require(isinstance(action, dict), "committed_action must be an object")
  _require(set(action) == {"command", "transition_count", "latest_state_hash"}, "committed action fields are not exact")
  _require(action["command"] == "hold", "runtime evidence must bind the observed Hold action")
  _require(type(action["transition_count"]) is int and action["transition_count"] == 1, "one committed transition is required")
  _require(action["latest_state_hash"] == EXPECTED_HASH, "committed state hash drifted")
  _require(observation["repository_state_written"] is False, "runtime evidence must not write repository state")
  _require(observation["host_session_started"] is True, "host-backed session start must be observed")


def _validate_terminal_surface(surface: object) -> None:
  _require(isinstance(surface, dict), "terminal_surface must be an object")
  _require(
    set(surface) == {"title", "status", "presentation_state", "meta", "history", "debrief", "read_only", "onboarding", "audio"},
    "terminal surface fields are not exact",
  )
  _require(surface["title"] == EXPECTED_TITLE, "GUI title drifted")
  _require(surface["status"] == "Host session ended; final history and debrief loaded", "terminal status drifted")
  _require(surface["presentation_state"] == surface["status"], "presentation status must match terminal status")
  _require(surface["meta"] == "competitive-regional-v1 · final turn 1/24 · 1 transitions · hash 61357596d8800592", "terminal metadata drifted")

  history = surface["history"]
  _require(isinstance(history, dict), "terminal history must be an object")
  _require(set(history) == {"row_count", "rows", "placeholder_absent"}, "terminal history fields are not exact")
  _require(type(history["row_count"]) is int and history["row_count"] == 1, "terminal history must contain one row")
  _require(history["rows"] == [{"turn": 1, "command": "[Hold]", "state_hash": EXPECTED_HASH}], "terminal history row drifted")
  _require(history["placeholder_absent"] is True, "terminal history placeholder must be absent")

  debrief = surface["debrief"]
  _require(isinstance(debrief, dict), "terminal debrief must be an object")
  _require(
    set(debrief) == {"row_count", "first_line", "last_line", "required_markers", "placeholder_absent", "instructor_only_markers_absent", "written_rows_present"},
    "terminal debrief fields are not exact",
  )
  _require(type(debrief["row_count"]) is int and debrief["row_count"] == 19, "terminal debrief row count drifted")
  _require(debrief["first_line"] == "Competitive preview completed 1 committed month(s).", "terminal debrief first line drifted")
  _require(debrief["last_line"] == "Decision quality and outcome quality remain separate: the MCP surface reports actor-visible observations plus committed transition summaries.", "terminal debrief last line drifted")
  _require(debrief["required_markers"] == EXPECTED_DEBRIEF_MARKERS, "terminal debrief markers drifted")
  _require(all(value is True for value in debrief.values() if isinstance(value, bool)), "terminal debrief boolean boundary is incomplete")

  read_only = surface["read_only"]
  _require(isinstance(read_only, dict), "read_only must be an object")
  _require(set(read_only) == {"command_form_hidden", "action_builder_hidden", "session_end_disabled", "action_submission_deferred"}, "read-only fields are not exact")
  _require(all(value is True for value in read_only.values()), "terminal read-only controls are incomplete")

  onboarding = surface["onboarding"]
  _require(isinstance(onboarding, dict), "onboarding must be an object")
  _require(set(onboarding) == {"next_text", "directs_to_debrief"}, "onboarding fields are not exact")
  _require(onboarding["next_text"] == "Review the debrief", "terminal onboarding text drifted")
  _require(onboarding["directs_to_debrief"] is True, "terminal onboarding must direct the debrief review")

  audio = surface["audio"]
  _require(isinstance(audio, dict), "terminal audio must be an object")
  _require(set(audio) == {"state", "written_fallback_present", "playback_verified", "listening_review_complete"}, "terminal audio fields are not exact")
  _require(audio["state"] == "Audio off; visual and text equivalents are active.", "terminal audio state drifted")
  _require(audio["written_fallback_present"] is True, "terminal written audio fallback is missing")
  _require(audio["playback_verified"] is False and audio["listening_review_complete"] is False, "terminal audio evidence must remain unverified")


def _validate_renderer_contract(contract: object) -> None:
  _require(isinstance(contract, dict), "renderer_contract must be an object")
  _require(set(contract) == {"source_test", "campaign_coverage_hidden_after_end_session", "visible_terminal_debrief_target_selected"}, "renderer contract fields are not exact")
  _require(contract["source_test"] == "tests/test_phase11_live_debrief.py", "renderer source test drifted")
  _require(contract["campaign_coverage_hidden_after_end_session"] is True, "stale campaign coverage must be hidden after terminal end")
  _require(contract["visible_terminal_debrief_target_selected"] is True, "onboarding target must select a visible terminal debrief")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "terminal runtime evidence packet must be an object")
  _require(set(packet) == REQUIRED_FIELDS, "terminal runtime evidence packet fields are not exact")
  _require(packet["schema_version"] == EXPECTED_SCHEMA, "terminal runtime evidence schema drifted")
  _require(packet["status"] == EXPECTED_STATUS, "terminal runtime evidence must remain pending human review")
  _require(packet["package_version"] == EXPECTED_VERSION, "terminal runtime evidence package version drifted")
  _require(packet["roadmap_item"] == "debrief visuals reviewed", "roadmap item drifted")
  _require(packet["observed_on"] == "2026-08-01", "observed date drifted")
  _validate_observation(packet["observation"])
  _validate_terminal_surface(packet["terminal_surface"])
  _validate_renderer_contract(packet["renderer_contract"])
  _require(packet["review_boundary"] == EXPECTED_REVIEW_BOUNDARY, "review boundary must remain fail-closed")

  source_contract = packet["source_contract"]
  _require(isinstance(source_contract, dict), "source_contract must be an object")
  _require(set(source_contract) == {"sources", "required_markers", "forbidden_claim_markers"}, "source contract fields are not exact")
  sources = source_contract["sources"]
  _require(isinstance(sources, list) and sources and all(isinstance(item, str) for item in sources), "source paths are required")
  for source in sources:
    path = Path(source)
    _require(not path.is_absolute() and (ROOT / path).is_file(), f"source path is missing: {source}")
  markers = source_contract["required_markers"]
  _require(isinstance(markers, list) and markers, "source markers are required")
  for marker in markers:
    _source_marker_is_valid(marker)
  _require(source_contract["forbidden_claim_markers"] == EXPECTED_FORBIDDEN_CLAIMS, "forbidden claims drifted")

  limits = packet["evidence_limits"]
  _require(isinstance(limits, list) and limits and all(isinstance(item, str) and item for item in limits), "evidence limits are required")
  joined_limits = " ".join(limits).lower()
  for marker in ("human", "educational", "accessibility", "audio", "browser/device", "public release"):
    _require(marker in joined_limits, f"evidence limits omit {marker}")

  release = packet["release_boundary"]
  _require(isinstance(release, dict), "release boundary must be an object")
  _require(set(release) == {"technical_evidence_added", "player_terminal_projection_corrected", "gameplay_changes", "simulation_changes", "audio_changes", "asset_changes", "persistence_changes", "support_policy_changed", "public_release_approval"}, "release boundary fields are not exact")
  _require(release["technical_evidence_added"] is True and release["player_terminal_projection_corrected"] is True, "technical terminal correction must be recorded")
  _require(release["support_policy_changed"] is False and release["public_release_approval"] is False, "support/release boundaries must remain false")
  for key in ("gameplay_changes", "simulation_changes", "audio_changes", "asset_changes", "persistence_changes"):
    _require(type(release[key]) is int and release[key] == 0, f"{key} must be an integer zero")

  searchable = json.dumps({"observation": packet["observation"], "terminal_surface": packet["terminal_surface"], "renderer_contract": packet["renderer_contract"]})
  for forbidden in EXPECTED_FORBIDDEN_CLAIMS:
    _require(forbidden not in searchable, f"forbidden claim leaked into evidence: {forbidden}")


def build_report(packet: object) -> dict:
  report = {
    "schema_version": "terminal-debrief-runtime-evidence-report-v1",
    "status": "fail",
    "errors": [],
    "package_version": None,
    "history_count": None,
    "debrief_count": None,
    "review_boundary": None,
  }
  try:
    validate_packet(packet)
  except (TypeError, ValueError, OSError, json.JSONDecodeError) as error:
    report["errors"] = [str(error)]
    return report
  report["status"] = "pass"
  report["package_version"] = packet["package_version"]
  report["history_count"] = packet["terminal_surface"]["history"]["row_count"]
  report["debrief_count"] = packet["terminal_surface"]["debrief"]["row_count"]
  report["review_boundary"] = packet["review_boundary"]
  return report


def main() -> int:
  try:
    packet = _load_json(PACKET_PATH)
    report = build_report(packet)
  except (OSError, json.JSONDecodeError) as error:
    report = {
      "schema_version": "terminal-debrief-runtime-evidence-report-v1",
      "status": "fail",
      "errors": [str(error)],
    }
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  sys.exit(main())
