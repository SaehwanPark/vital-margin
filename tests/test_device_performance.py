import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_device_performance.py"
POLICY = ROOT / "assets" / "device-performance-policy.json"


class DevicePerformanceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_device_performance", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(POLICY.read_text(encoding="utf-8"))

  def test_current_proxy_report_is_green_and_bounded(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "device-performance-report-v1")
    self.assertEqual(report["source_bytes"], 449574)
    self.assertEqual(report["measurements"]["dom_elements"], 818)
    self.assertFalse(self.document["certification"]["real_device"])

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["profile"]["id"], "low-power-browser-proxy")

  def test_source_measurement_drift_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["measurements"]["live_source_bytes"] = 1
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("source bytes" in error for error in report["errors"]))

  def test_limit_exceedance_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["limits"]["dom_elements"] = 1
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertIn("DOM element measurement exceeds limit", report["errors"])

  def test_real_device_claim_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["certification"]["real_device"] = True
    errors = self.checker.validate_definition(ROOT, document)
    self.assertIn("certification.real_device must be false", errors)

  def test_profile_target_is_fixed(self):
    document = copy.deepcopy(self.document)
    document["profile"]["viewport"]["width"] = 800
    document["measurements"]["viewport"]["width"] = 800
    errors = self.checker.validate_definition(ROOT, document)
    self.assertIn("profile.viewport must be 1024x768 for the low-power proxy", errors)

  def test_invalid_profile_and_escaped_loading_policy_fail_closed(self):
    document = copy.deepcopy(self.document)
    document["profile"]["viewport"]["width"] = 0
    document["loading_policy"] = "../outside"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("profile.viewport.width" in error for error in errors))
    self.assertTrue(any("path escapes repository root" in error for error in errors))

  def test_sample_maximum_must_match_samples(self):
    document = copy.deepcopy(self.document)
    document["measurements"]["shell_reload_max_ms"] = 1
    errors = self.checker.validate_definition(ROOT, document)
    self.assertIn("measurements.shell_reload_max_ms must equal the sample maximum", errors)


if __name__ == "__main__":
  unittest.main()
