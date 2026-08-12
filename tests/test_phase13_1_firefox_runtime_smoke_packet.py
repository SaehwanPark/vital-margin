import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-firefox-runtime-smoke-packet.json"
PROBE_PATH = ROOT / "scripts" / "check_firefox_runtime_smoke.py"
BROWSER_POLICY_PATH = ROOT / "assets" / "browser-compatibility-policy.json"

EXPECTED_SHELL = {
  "title": "Vital Margin — Executive Desktop",
  "ready": "complete",
  "start_control": True,
  "demo_fixture": True,
  "url": "http://127.0.0.1:7878/",
}
SESSION_ID_PATTERN = r"session-[A-Za-z0-9_-]+"
EXPECTED_REVIEW_BOUNDARY = {
  "firefox_shell_runtime_smoke_complete": True,
  "firefox_host_backed_start_smoke_complete": True,
  "firefox_browser_refresh_resume_smoke_complete": True,
  "firefox_all_campaign_launch_smoke_complete": True,
  "firefox_competitive_full_campaign_smoke_complete": True,
  "firefox_stabilization_full_campaign_smoke_complete": True,
  "firefox_affiliation_full_campaign_smoke_complete": True,
  "firefox_full_campaign_certification_complete": False,
  "firefox_audio_decoder_review_complete": False,
  "webkit_runtime_certification_complete": False,
  "real_device_certification_complete": False,
  "hardware_performance_certification_complete": False,
  "human_accessibility_review_complete": False,
  "human_usability_review_complete": False,
  "public_release_approval": False,
}


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13FirefoxRuntimeSmokePacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    cls.browser_policy = load_json(BROWSER_POLICY_PATH)
    spec = importlib.util.spec_from_file_location("check_firefox_runtime_smoke", PROBE_PATH)
    cls.probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.probe)

  def test_packet_is_observed_smoke_only(self):
    self.assertEqual(self.packet["schema_version"], "phase13.1-firefox-runtime-smoke-packet-v1")
    self.assertEqual(self.packet["status"], "complete-firefox-host-backed-smoke-pending-matrix")
    self.assertEqual(self.packet["roadmap_item"], "cross-browser/device certification")
    self.assertEqual(self.packet["policy_boundary"]["canonical_browser_policy_unchanged"], True)
    self.assertEqual(self.packet["policy_boundary"]["firefox_policy_status"], "not-certified")
    self.assertEqual(self.packet["policy_boundary"]["webkit_policy_status"], "not-certified")
    self.assertTrue(self.packet["policy_boundary"]["smoke_result_does_not_promote_browser_support"])
    self.assertEqual(self.packet["review_boundary"], EXPECTED_REVIEW_BOUNDARY)

  def test_runtime_observation_is_exact_and_host_backed(self):
    observation = self.packet["runtime_observation"]
    self.assertEqual(observation["status"], "pass")
    self.assertEqual(observation["url"], "http://127.0.0.1:7878/")
    self.assertEqual(observation["marionette_protocol"], 3)
    self.assertEqual(observation["browser"], {
      "name": "firefox",
      "version": "147.0.2",
      "platform": "mac",
      "headless": True,
    })
    self.assertEqual(observation["shell"], EXPECTED_SHELL)
    host_start = observation["host_start"]
    self.assertRegex(host_start["session"], SESSION_ID_PATTERN)
    self.assertEqual(host_start["status"], f"competitive regional session loaded: {host_start['session']}")
    self.assertFalse(host_start["demo_fixture"])
    self.assertEqual(host_start["campaign"], "competitive-regional-v1")
    self.assertEqual(host_start["ready"], "complete")
    self.assertTrue(host_start["checkpoint_saved"])
    self.assertEqual(host_start["checkpoint_status"], "Host checkpoint saved at 0 committed transitions.")
    self.assertEqual(host_start["stored_session_id"], host_start["session"])
    resume = observation["browser_refresh_resume"]
    self.assertEqual(resume["status"], f"Host session refreshed after browser refresh: {host_start['session']}")
    self.assertEqual(resume["session"], host_start["session"])
    self.assertEqual(resume["stored_session_id"], host_start["session"])
    self.assertFalse(resume["demo_fixture"])
    self.assertEqual(resume["ready"], "complete")
    launches = observation["campaign_launches"]
    self.assertEqual(launches["competitive-regional-v1"], host_start)
    for campaign, label in (("stabilization-v1", "stabilization"), ("regional-affiliation-v1", "regional affiliation")):
      launch = launches[campaign]
      self.assertRegex(launch["session"], SESSION_ID_PATTERN)
      self.assertEqual(launch["status"], f"{label} session loaded: {launch['session']}")
      self.assertFalse(launch["demo_fixture"])
      self.assertEqual(launch["ready"], "complete")
    self.assertEqual(len({launches[campaign]["session"] for campaign in launches}), 3)
    full_campaign = observation["competitive_full_campaign"]
    self.assertEqual(full_campaign["campaign"], "competitive-regional-v1")
    self.assertEqual(full_campaign["session"], host_start["session"])
    self.assertEqual(full_campaign["target_turns"], 24)
    self.assertEqual(full_campaign["committed_turns"], 24)
    self.assertEqual(full_campaign["history_count"], 24)
    self.assertEqual(full_campaign["replay_count"], 24)
    self.assertEqual(full_campaign["autosave_count"], 24)
    self.assertEqual(len(full_campaign["turns"]), 24)
    self.assertEqual(full_campaign["turns"][0]["state_hash"], "61357596d8800592")
    self.assertEqual(full_campaign["turns"][-1]["state_hash"], "b24eea963c3abfe2")
    self.assertEqual(full_campaign["terminal"]["status"], "Host session ended; final history and debrief loaded")
    self.assertEqual(full_campaign["terminal"]["history_count"], 24)
    self.assertGreater(full_campaign["terminal"]["debrief_count"], 0)
    self.assertEqual(full_campaign["terminal"]["final_state_hash"], "b24eea963c3abfe2")
    full_runs = observation["campaign_full_runs"]
    stabilization = full_runs["stabilization-v1"]
    self.assertEqual(stabilization["session"], launches["stabilization-v1"]["session"])
    self.assertEqual(stabilization["target_stages"], 5)
    self.assertEqual(stabilization["committed_stages"], 5)
    self.assertEqual(stabilization["history_count"], 5)
    self.assertEqual(stabilization["autosave_count"], 5)
    self.assertEqual([stage["state_hash"] for stage in stabilization["stages"]], [
      "4a41dfcb5438b5f8", "113e6acccc04f651", "ae271eae8d552f15",
      "6d306853a415633a", "6982f2ef9a3df4e7",
    ])
    self.assertEqual(stabilization["terminal"]["debrief_count"], 29)
    affiliation = full_runs["regional-affiliation-v1"]
    self.assertEqual(affiliation["session"], launches["regional-affiliation-v1"]["session"])
    self.assertEqual(affiliation["target_stages"], 6)
    self.assertEqual(affiliation["committed_stages"], 6)
    self.assertEqual(affiliation["history_count"], 6)
    self.assertEqual(affiliation["autosave_count"], 6)
    self.assertEqual([stage["state_hash"] for stage in affiliation["stages"]], [
      "9d38e1d2ebc1e05d", "31c9e7e5e7cc16fd", "ee38360229afe70c",
      "0a1a88f40ee9bba5", "5ca716a1c0ce6826", "00025c494e6299ae",
    ])
    self.assertEqual(affiliation["terminal"]["debrief_count"], 14)
    self.assertTrue(self.packet["probe"]["writes_project_state"] is False)

  def test_probe_source_and_browser_policy_boundaries_are_exact(self):
    probe_text = PROBE_PATH.read_text(encoding="utf-8")
    for marker in self.packet["required_source_markers"]["probe"]:
      self.assertIn(marker, probe_text, marker)
    policy_text = BROWSER_POLICY_PATH.read_text(encoding="utf-8")
    for marker in self.packet["required_source_markers"]["browser_policy"]:
      self.assertIn(marker, policy_text, marker)
    guides_text = (
      (ROOT / "docs/guides/reproducible-distribution.md").read_text(encoding="utf-8")
      + (ROOT / "docs/guides/gui-how-to-play.md").read_text(encoding="utf-8")
    )
    for marker in self.packet["required_source_markers"]["guides"]:
      self.assertIn(marker, guides_text, marker)
    target_ids = {target["id"] for target in self.browser_policy["not_certified_targets"]}
    self.assertIn("firefox-desktop", target_ids)
    self.assertIn("webkit-desktop", target_ids)

  def test_safari_blocker_and_release_boundary_are_explicit(self):
    safari = self.packet["safari_webkit_boundary"]
    self.assertEqual(safari["status"], "blocked-permission")
    self.assertEqual(safari["support_status"], "not-certified")
    self.assertFalse(safari["runtime_result_recorded"])
    self.assertIn("Allow remote automation", safari["message"])
    limits = " ".join(self.packet["evidence_limits"])
    for marker in ("full-campaign", "audio decoding", "real hardware", "lived accessibility", "human", "public-release"):
      self.assertIn(marker, limits)
    release = self.packet["release_boundary"]
    self.assertTrue(all(release[key] == 0 for key in (
      "runtime_changes", "simulation_changes", "asset_changes", "audio_changes",
      "screenshot_changes", "release_manifest_changes",
    )))
    self.assertFalse(release["public_release_approval"])
    self.assertTrue(release["technical_packet_does_not_authorize_support_promotion"])

  def test_probe_is_valid_python_without_writing_bytecode(self):
    parsed = ast.parse(PROBE_PATH.read_text(encoding="utf-8"), filename=str(PROBE_PATH))
    self.assertIsNotNone(parsed)

  def test_probe_rejects_invalid_observations_and_non_loopback_urls(self):
    observation = self.packet["runtime_observation"]
    self.probe.validate_observations(
      observation["shell"],
      observation["host_start"],
      observation["url"],
      observation["browser"],
      observation["marionette_protocol"],
      observation["browser_refresh_resume"],
      observation["campaign_launches"],
      observation["competitive_full_campaign"],
      observation["campaign_full_runs"],
    )
    bad_host = dict(observation["host_start"])
    bad_host["status"] = "stabilization session loaded: session-1"
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        bad_host,
        observation["url"],
        observation["browser"],
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
        observation["campaign_launches"],
        observation["competitive_full_campaign"],
        observation["campaign_full_runs"],
      )
    bad_browser = dict(observation["browser"])
    bad_browser["headless"] = False
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        observation["host_start"],
        observation["url"],
        bad_browser,
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
        observation["campaign_launches"],
      )
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        observation["host_start"],
        "https://example.com/",
        observation["browser"],
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
        observation["campaign_launches"],
      )
    with self.assertRaises(RuntimeError):
      self.probe._validate_loopback_url("http://example.com/")
    with self.assertRaises(RuntimeError):
      self.probe._validate_loopback_url("http://localhost:7878/")

  def test_existing_browser_device_and_technical_checks_remain_authoritative(self):
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_browser_compatibility",
        "tests.test_device_performance",
        "tests.test_phase13_technical_coverage",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
  unittest.main()
