#!/usr/bin/env python3
"""Validate bounded current-browser runtime capability evidence."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-runtime-capability-evidence.json"
EXPECTED_SCHEMA = "phase13.1-runtime-capability-evidence-v1"
EXPECTED_STATUS = "complete-supported-chromium-host-smoke-pending-cross-engine-certification"
EXPECTED_VERSION = "0.13.97"
EXPECTED_URL = "http://127.0.0.1:7878/"
EXPECTED_TITLE = "Vital Margin — Executive Desktop"
SESSION_PATTERN = re.compile(r"^session-[A-Za-z0-9_-]+$")
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}
REQUIRED_FIELDS = {
  "schema_version",
  "status",
  "package_version",
  "roadmap_item",
  "observed_on",
  "observation",
  "capability_inventory",
  "review_boundary",
  "source_contract",
  "evidence_limits",
  "release_boundary",
}
EXPECTED_REVIEW_BOUNDARY = {
  "chromium_host_backed_smoke_complete": True,
  "chromium_console_warning_error_free": True,
  "firefox_runtime_certification_complete": False,
  "webkit_runtime_certification_complete": False,
  "real_device_certification_complete": False,
  "hardware_performance_certification_complete": False,
  "human_accessibility_review_complete": False,
  "human_usability_review_complete": False,
  "public_release_approval": False,
  "canonical_browser_policy_promoted": False,
}
EXPECTED_FORBIDDEN_CLAIMS = [
  "Firefox is supported",
  "WebKit is supported",
  "Firefox/WebKit certified",
  "real-device certification complete",
  "battery certification complete",
  "human accessibility review complete",
  "public release approved",
]
EXPECTED_CAPABILITY_STATUS = {
  "in-app-chromium": "observed",
  "chromium-command-line": "absent",
  "firefox-command-line": "absent",
  "safari-webdriver": "permission-blocked",
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


def _validate_observation(observation: object) -> None:
  _require(isinstance(observation, dict), "observation must be an object")
  _require(set(observation) == {
    "method",
    "url",
    "browser",
    "shell",
    "console",
    "repository_state_written",
    "host_session_started",
  }, "observation fields are not exact")
  _require(isinstance(observation["method"], str) and observation["method"], "observation method is required")
  _validate_loopback_url(observation["url"])
  _require(observation["url"] == EXPECTED_URL, "observation URL must match the GUI default loopback route")

  browser = observation["browser"]
  _require(isinstance(browser, dict), "browser observation must be an object")
  _require(set(browser) == {"name", "engine", "version", "platform", "user_agent", "protocol"}, "browser fields are not exact")
  _require(browser["name"] == "Chrome", "observed browser must be Chrome")
  _require(browser["engine"] == "Chromium", "observed browser engine must be Chromium")
  _require(browser["version"] == "150.0.0.0", "browser version must match the observed Chrome runtime")
  _require(browser["platform"] == "macOS", "browser platform must identify macOS")
  _require(isinstance(browser["user_agent"], str) and "Chrome/150.0.0.0" in browser["user_agent"], "browser user agent must bind the observed Chrome version")
  _require(browser["protocol"] == "Chrome DevTools Protocol", "browser protocol must identify the read-only runtime observation")

  shell = observation["shell"]
  _require(isinstance(shell, dict), "shell observation must be an object")
  _require(set(shell) == {"title", "ready", "start_control", "demo_fixture", "status", "session_id"}, "shell fields are not exact")
  _require(shell["title"] == EXPECTED_TITLE, "shell title does not match the executive desktop")
  _require(shell["ready"] == "complete", "shell did not reach readyState=complete")
  _require(shell["start_control"] is True, "session-start control was not observed")
  _require(shell["demo_fixture"] is False, "demo fixture must be absent after host start")
  _require(isinstance(shell["status"], str) and shell["status"].startswith("competitive regional session loaded: "), "host status must report a competitive session")
  _require(isinstance(shell["session_id"], str) and SESSION_PATTERN.fullmatch(shell["session_id"]), "host session ID must be opaque and non-empty")
  _require(shell["session_id"] in shell["status"], "host status must bind the observed opaque session ID")

  console = observation["console"]
  _require(isinstance(console, dict), "console observation must be an object")
  _require(set(console) == {"warning_count", "error_count"}, "console fields are not exact")
  for field in ("warning_count", "error_count"):
    _require(type(console[field]) is int and console[field] >= 0, f"console {field} must be a non-negative integer")
  _require(console["warning_count"] == 0 and console["error_count"] == 0, "runtime smoke must have no warning/error console entries")
  _require(observation["repository_state_written"] is False, "runtime evidence must not write repository state")
  _require(observation["host_session_started"] is True, "host-backed session start must be observed")


def _validate_capability_inventory(inventory: object) -> None:
  _require(isinstance(inventory, list), "capability_inventory must be a list")
  observed = {}
  for item in inventory:
    _require(isinstance(item, dict), "capability inventory entries must be objects")
    _require(set(item) == {"id", "status", "evidence", "next_action"}, "capability inventory fields are not exact")
    _require(isinstance(item["id"], str) and item["id"], "capability ID is required")
    _require(item["id"] not in observed, f"duplicate capability ID: {item['id']}")
    _require(isinstance(item["status"], str) and item["status"], f"capability status is required: {item['id']}")
    _require(isinstance(item["evidence"], str) and item["evidence"], f"capability evidence is required: {item['id']}")
    _require(isinstance(item["next_action"], str) and item["next_action"], f"capability next action is required: {item['id']}")
    observed[item["id"]] = item["status"]
  _require(observed == EXPECTED_CAPABILITY_STATUS, "capability inventory drifted from the observed host boundary")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "runtime evidence packet must be an object")
  _require(set(packet) == REQUIRED_FIELDS, "runtime evidence packet fields are not exact")
  _require(packet["schema_version"] == EXPECTED_SCHEMA, "runtime evidence schema drifted")
  _require(packet["status"] == EXPECTED_STATUS, "runtime evidence must remain pending cross-engine certification")
  _require(packet["package_version"] == EXPECTED_VERSION, "runtime evidence package version drifted")
  _require(packet["roadmap_item"] == "cross-browser/device certification", "roadmap item drifted")
  _require(packet["observed_on"] == "2026-08-01", "observed date drifted")
  _validate_observation(packet["observation"])
  _validate_capability_inventory(packet["capability_inventory"])
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
  for marker in ("Firefox", "WebKit", "real hardware", "human accessibility", "public release"):
    _require(marker in joined_limits, f"evidence limits omit {marker}")
  release = packet["release_boundary"]
  _require(isinstance(release, dict), "release boundary must be an object")
  _require(set(release) == {
    "technical_evidence_added",
    "support_policy_changed",
    "runtime_changes",
    "simulation_changes",
    "asset_changes",
    "audio_changes",
    "persistence_changes",
    "public_release_approval",
  }, "release boundary fields are not exact")
  _require(release["technical_evidence_added"] is True, "technical evidence addition must be recorded")
  _require(release["support_policy_changed"] is False, "support policy must remain unchanged")
  for key in ("runtime_changes", "simulation_changes", "asset_changes", "audio_changes", "persistence_changes"):
    _require(type(release[key]) is int and release[key] == 0, f"{key} must be an integer zero")
  _require(release["public_release_approval"] is False, "public release approval must remain false")

  searchable = json.dumps({
    "observation": packet["observation"],
    "capability_inventory": packet["capability_inventory"],
  })
  for forbidden in EXPECTED_FORBIDDEN_CLAIMS:
    _require(forbidden not in searchable, f"forbidden promotion claim leaked into evidence: {forbidden}")


def build_report(packet: object) -> dict:
  report = {
    "schema_version": "runtime-capability-evidence-report-v1",
    "status": "fail",
    "errors": [],
    "package_version": None,
    "observed_browser": None,
    "review_boundary": None,
  }
  try:
    validate_packet(packet)
  except (TypeError, ValueError, OSError, json.JSONDecodeError) as error:
    report["errors"] = [str(error)]
    return report
  report["status"] = "pass"
  report["package_version"] = packet["package_version"]
  report["observed_browser"] = packet["observation"]["browser"]
  report["review_boundary"] = packet["review_boundary"]
  return report


def main() -> int:
  try:
    packet = _load_json(PACKET_PATH)
    report = build_report(packet)
  except (OSError, json.JSONDecodeError) as error:
    report = {
      "schema_version": "runtime-capability-evidence-report-v1",
      "status": "fail",
      "errors": [str(error)],
    }
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  sys.exit(main())
