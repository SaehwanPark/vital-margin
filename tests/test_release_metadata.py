import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
  "check_release_metadata",
  ROOT / "scripts" / "check_release_metadata.py",
)
CHECK = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECK)


class ReleaseMetadataTests(unittest.TestCase):
  def test_repository_metadata_is_consistent(self):
    versions = CHECK.read_versions(ROOT)
    self.assertEqual(CHECK.validate_versions(versions), [])
    self.assertEqual(versions["Cargo.toml"], "0.14.14")

  def test_checker_accepts_modified_semver_shape(self):
    self.assertEqual(
      CHECK.validate_versions(
        {
          "Cargo.toml": "1.2.10",
          "Cargo.lock": "1.2.10",
          "README.md": "1.2.10",
          "CHANGELOG.md": "1.2.10",
        }
      ),
      [],
    )

  def test_checker_reports_projection_mismatch(self):
    errors = CHECK.validate_versions(
      {
        "Cargo.toml": "0.12.13",
        "Cargo.lock": "0.12.12",
        "README.md": "0.12.13",
        "CHANGELOG.md": "0.12.13",
      }
    )
    self.assertEqual(
      errors,
      ["Cargo.lock: found '0.12.12'; expected '0.12.13'"],
    )

  def test_checker_reports_invalid_package_version(self):
    errors = CHECK.validate_versions(
      {
        "Cargo.toml": "0.12",
        "Cargo.lock": "0.12",
        "README.md": "0.12",
        "CHANGELOG.md": "0.12",
      }
    )
    self.assertIn("Cargo.toml: invalid package version '0.12'", errors)


if __name__ == "__main__":
  unittest.main()
