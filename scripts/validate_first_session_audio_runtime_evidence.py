#!/usr/bin/env python3
"""Validate bounded first-session and audio presentation runtime evidence."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-first-session-audio-runtime-evidence.json"
EXPECTED_SCHEMA = "phase13.1-first-session-audio-runtime-evidence-v1"
EXPECTED_STATUS = "complete-first-session-audio-runtime-boundary-pending-human-evaluation"
EXPECTED_VERSION = "0.13.98"
EXPECTED_URL = "http://127.0.0.1:7878/"
EXPECTED_TITLE = "Vital Margin — Executive Desktop"
SESSION_PATTERN = re.compile(r"^session-[A-Za-z0-9_-]+$")
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}
EXPECTED_RAIL_LABELS = [
  "Start or load",
  "Inspect the visible market",
  "Draft contextual actions",
  "Review and validate",
  "Submit the unchanged batch",
  "Review monthly resolution",
  "Continue to the next observation",
]
REQUIRED_FIELDS = {
  "schema_version",
  "status",
  "package_version",
  "roadmap_item",
  "observed_on",
  "observation",
  "settings_observation",
  "audio_observation",
  "review_boundary",
  "source_contract",
  "evidence_limits",
  "release_boundary",
}
EXPECTED_REVIEW_BOUNDARY = {
  "technical_first_session_observation_complete": True,
  "technical_accessibility_state_observation_complete": True,
  "technical_audio_fallback_observation_complete": True,
  "first_time_user_evaluation_complete": False,
  "audio_preference_feedback_collected": False,
  "quantitative_audio_ratings_collected": False,
  "qualitative_audio_interviews_completed": False,
  "human_accessibility_review_complete": False,
  "educational_usability_review_complete": False,
  "browser_device_certification_complete": False,
  "public_release_approval": False,
}
EXPECTED_FORBIDDEN_CLAIMS = [
  "human first-time-user evaluation complete",
  "audio preference feedback collected",
  "quantitative audio ratings collected",
  "qualitative audio interviews completed",
  "audio quality approved",
  "human accessibility review complete",
  "public release approved",
  "Firefox/WebKit certified",
]


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
  _require(set(browser) == {"name", "engine", "version", "platform", "user_agent", "protocol"}, "browser fields are not exact")
  _require(browser["name"] == "Chrome", "observed browser must be Chrome")
  _require(browser["engine"] == "Chromium", "observed browser engine must be Chromium")
  _require(browser["version"] == "150.0.0.0", "browser version must match the observed runtime")
  _require(browser["platform"] == "macOS", "browser platform must identify macOS")
  _require(isinstance(browser["user_agent"], str) and "Chrome/150.0.0.0" in browser["user_agent"], "browser user agent must bind the observed version")
  _require(browser["protocol"] == "Chrome DevTools Protocol", "browser protocol must identify the runtime observation")


def _validate_observation(observation: object) -> None:
  _require(isinstance(observation, dict), "observation must be an object")
  _require(set(observation) == {
    "method",
    "url",
    "browser",
    "host_start",
    "first_session_rail",
    "actor_visible_surface",
    "repository_state_written",
    "host_session_started",
  }, "observation fields are not exact")
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

  rail = observation["first_session_rail"]
  _require(isinstance(rail, dict), "first_session_rail must be an object")
  _require(set(rail) == {
    "flow_schema",
    "stage_count",
    "stage_labels",
    "current_stage",
    "progress",
    "source",
    "all_stage_details_present",
    "host_authority_language_present",
  }, "first_session_rail fields are not exact")
  _require(rail["flow_schema"] == "competitive-first-month-v1", "first-session flow schema drifted")
  _require(type(rail["stage_count"]) is int and rail["stage_count"] == 7, "first-session rail must contain seven stages")
  _require(rail["stage_labels"] == EXPECTED_RAIL_LABELS, "first-session rail labels drifted")
  _require(rail["current_stage"] == "Draft contextual actions", "observed first-session stage drifted")
  _require(rail["progress"] == "Draft contextual actions · 3 of 7", "observed first-session progress drifted")
  _require(rail["source"] == "gui/first-month.mjs", "first-session rail source drifted")
  _require(rail["all_stage_details_present"] is True, "first-session stage details are incomplete")
  _require(rail["host_authority_language_present"] is True, "first-session host-authority language is missing")

  visible = observation["actor_visible_surface"]
  _require(isinstance(visible, dict), "actor_visible_surface must be an object")
  _require(set(visible) == {
    "title",
    "ready",
    "briefing_present",
    "current_observation_present",
    "written_history_present",
    "debrief_placeholder_present",
    "private_state_claim_absent",
    "written_equivalent_policy_present",
  }, "actor_visible_surface fields are not exact")
  _require(visible["title"] == EXPECTED_TITLE, "GUI title drifted")
  _require(visible["ready"] == "complete", "GUI did not reach readyState=complete")
  for field in (
    "briefing_present",
    "current_observation_present",
    "written_history_present",
    "debrief_placeholder_present",
    "private_state_claim_absent",
    "written_equivalent_policy_present",
  ):
    _require(visible[field] is True, f"actor-visible surface field is incomplete: {field}")
  _require(observation["repository_state_written"] is False, "runtime evidence must not write repository state")
  _require(observation["host_session_started"] is True, "host-backed session start must be observed")


def _validate_settings(settings: object) -> None:
  _require(isinstance(settings, dict), "settings_observation must be an object")
  _require(set(settings) == {"low_distraction_forced", "independent_accommodation", "written_content_contract"}, "settings fields are not exact")
  forced = settings["low_distraction_forced"]
  _require(isinstance(forced, dict), "low_distraction_forced must be an object")
  _require(set(forced) == {
    "mode_active",
    "reduced_motion_active",
    "large_text_active",
    "cue_explanations_active",
    "audio_controls_disabled",
    "reduced_notifications_active",
    "written_results_complete",
  }, "low-distraction fields are not exact")
  _require(all(value is True for value in forced.values()), "low-distraction forced settings must all be active")

  independent = settings["independent_accommodation"]
  _require(isinstance(independent, dict), "independent_accommodation must be an object")
  _require(set(independent) == {
    "mode_active",
    "reduced_motion_active",
    "large_text_active",
    "cue_explanations_active",
    "written_results_complete",
    "restored_after_low_distraction",
  }, "independent accommodation fields are not exact")
  _require(independent["mode_active"] is False, "independent accommodation must be outside low-distraction mode")
  _require(all(independent[field] is True for field in (
    "reduced_motion_active",
    "large_text_active",
    "cue_explanations_active",
    "written_results_complete",
    "restored_after_low_distraction",
  )), "independent accommodation evidence is incomplete")

  contract = settings["written_content_contract"]
  _require(isinstance(contract, dict), "written_content_contract must be an object")
  _require(set(contract) == {"settings_summary_present", "written_results_present", "history_surface_present", "debrief_surface_present"}, "written content fields are not exact")
  _require(all(value is True for value in contract.values()), "written content contract is incomplete")


def _validate_audio(audio: object) -> None:
  _require(isinstance(audio, dict), "audio_observation must be an object")
  _require(set(audio) == {"audio_controls_exposed", "low_distraction_state", "cues_only_state", "muted_state", "optional_equivalent_contract", "audio_playback_verified", "audio_listening_review_complete"}, "audio fields are not exact")
  _require(audio["audio_controls_exposed"] is True, "audio controls were not observed")
  low = audio["low_distraction_state"]
  _require(isinstance(low, dict), "low_distraction_state must be an object")
  _require(set(low) == {"controls_disabled", "reduced_notifications_active", "muted_by_mode"}, "low-distraction audio fields are not exact")
  _require(all(value is True for value in low.values()), "low-distraction audio state is incomplete")

  cues = audio["cues_only_state"]
  _require(isinstance(cues, dict), "cues_only_state must be an object")
  _require(set(cues) == {"mode", "status", "written_equivalent_present", "playback_verified"}, "cues-only fields are not exact")
  _require(cues["mode"] == "cues-only", "cues-only mode was not observed")
  _require(isinstance(cues["status"], str) and cues["status"].startswith("Cues-only mode enabled; music and ambience are off"), "cues-only status language drifted")
  _require(cues["written_equivalent_present"] is True, "cues-only written equivalent is missing")
  _require(cues["playback_verified"] is False, "cues-only evidence must not claim playback verification")

  muted = audio["muted_state"]
  _require(isinstance(muted, dict), "muted_state must be an object")
  _require(set(muted) == {"status", "written_equivalent_present", "playback_verified"}, "muted fields are not exact")
  _require(muted["status"] == "Audio muted; visual and text equivalents remain active.", "muted status language drifted")
  _require(muted["written_equivalent_present"] is True, "muted written equivalent is missing")
  _require(muted["playback_verified"] is False, "muted evidence must not claim playback verification")

  equivalent = audio["optional_equivalent_contract"]
  _require(isinstance(equivalent, dict), "optional_equivalent_contract must be an object")
  _require(set(equivalent) == {"visible_when_text_equivalents_enabled", "hidden_when_optional_explanations_disabled", "written_results_remain_complete_when_hidden"}, "optional equivalent fields are not exact")
  _require(all(value is True for value in equivalent.values()), "optional equivalent contract is incomplete")
  _require(audio["audio_playback_verified"] is False, "audio playback must remain unverified")
  _require(audio["audio_listening_review_complete"] is False, "audio listening review must remain pending")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "runtime evidence packet must be an object")
  _require(set(packet) == REQUIRED_FIELDS, "runtime evidence packet fields are not exact")
  _require(packet["schema_version"] == EXPECTED_SCHEMA, "runtime evidence schema drifted")
  _require(packet["status"] == EXPECTED_STATUS, "runtime evidence must remain pending human evaluation")
  _require(packet["package_version"] == EXPECTED_VERSION, "runtime evidence package version drifted")
  _require(packet["roadmap_item"] == "audio and first-session evaluation", "roadmap item drifted")
  _require(packet["observed_on"] == "2026-08-01", "observed date drifted")
  _validate_observation(packet["observation"])
  _validate_settings(packet["settings_observation"])
  _validate_audio(packet["audio_observation"])
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
  joined_limits = " ".join(limits)
  for marker in ("participant", "listening", "audio quality", "human accessibility", "browser/device", "public release"):
    _require(marker in joined_limits, f"evidence limits omit {marker}")

  release = packet["release_boundary"]
  _require(isinstance(release, dict), "release boundary must be an object")
  _require(set(release) == {"technical_evidence_added", "gui_changes", "runtime_changes", "simulation_changes", "audio_changes", "asset_changes", "persistence_changes", "support_policy_changed", "public_release_approval"}, "release boundary fields are not exact")
  _require(release["technical_evidence_added"] is True, "technical evidence addition must be recorded")
  _require(release["support_policy_changed"] is False, "support policy must remain unchanged")
  for key in ("gui_changes", "runtime_changes", "simulation_changes", "audio_changes", "asset_changes", "persistence_changes"):
    _require(type(release[key]) is int and release[key] == 0, f"{key} must be an integer zero")
  _require(release["public_release_approval"] is False, "public release approval must remain false")

  searchable = json.dumps({
    "observation": packet["observation"],
    "settings_observation": packet["settings_observation"],
    "audio_observation": packet["audio_observation"],
  })
  for forbidden in EXPECTED_FORBIDDEN_CLAIMS:
    _require(forbidden not in searchable, f"forbidden claim leaked into evidence: {forbidden}")


def build_report(packet: object) -> dict:
  report = {
    "schema_version": "first-session-audio-runtime-evidence-report-v1",
    "status": "fail",
    "errors": [],
    "package_version": None,
    "flow_schema": None,
    "review_boundary": None,
  }
  try:
    validate_packet(packet)
  except (TypeError, ValueError, OSError, json.JSONDecodeError) as error:
    report["errors"] = [str(error)]
    return report
  report["status"] = "pass"
  report["package_version"] = packet["package_version"]
  report["flow_schema"] = packet["observation"]["first_session_rail"]["flow_schema"]
  report["review_boundary"] = packet["review_boundary"]
  return report


def main() -> int:
  try:
    packet = _load_json(PACKET_PATH)
    report = build_report(packet)
  except (OSError, json.JSONDecodeError) as error:
    report = {
      "schema_version": "first-session-audio-runtime-evidence-report-v1",
      "status": "fail",
      "errors": [str(error)],
    }
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  sys.exit(main())
