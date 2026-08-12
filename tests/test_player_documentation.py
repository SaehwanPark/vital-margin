import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "docs" / "images" / "readme"
SCREENSHOTS = (
  "gui-competitive-brief.png",
  "gui-stabilization-decide.png",
  "gui-affiliation-debrief.png",
  "cli-stabilization-beginner.png",
  "cli-competitive-report.png",
)


class PlayerDocumentationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cls.install = (ROOT / "docs" / "guides" / "installation.md").read_text(
      encoding="utf-8"
    )
    cls.contributors = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    cls.manifest = (SCREENSHOT_DIR / "README.md").read_text(encoding="utf-8")

  def test_readme_leads_with_player_first_run(self):
    hero = self.readme.index("gui-competitive-brief.png")
    play_now = self.readme.index("## Play now")
    self.assertLess(hero, play_now)
    self.assertIn("cargo run --bin vital-margin-gui", self.readme)
    self.assertIn("Stabilization tutorial", self.readme)
    self.assertIn("seed `42`", self.readme)
    self.assertNotIn("imgur", self.readme.lower())
    self.assertNotIn("Codex in-app browser", self.readme)

  def test_campaign_distinctions_and_nontransfer_are_explicit(self):
    for campaign in (
      "stabilization-v1",
      "competitive-regional-v1",
      "regional-affiliation-v1",
    ):
      self.assertIn(campaign, self.readme)
    for phrase in (
      "alternatives, not sequential chapters",
      "do not transfer",
      "24-month",
      "simultaneous AI-rival",
      "lagged public information",
      "six-stage",
      "not legal, valuation, antitrust, or transaction advice",
    ):
      self.assertIn(phrase, self.readme)

  def test_installation_and_contributor_links(self):
    for path in (
      "docs/guides/installation.md",
      "docs/guides/how-to-play.md",
      "docs/guides/gui-how-to-play.md",
      "docs/README.md",
      "ARCHITECTURE.md",
      "CHANGELOG.md",
    ):
      self.assertIn(path, self.readme)
    for url in (
      "https://www.rust-lang.org/learn/get-started",
      "https://git-scm.com/downloads",
      "https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository",
    ):
      self.assertIn(url, self.install)
    self.assertIn("Codex in-app browser", self.contributors)

  def test_local_screenshot_manifest_covers_five_lossless_pngs(self):
    for filename in SCREENSHOTS:
      path = SCREENSHOT_DIR / filename
      self.assertTrue(path.is_file(), filename)
      self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
      self.assertIn(filename, self.manifest)
      digest = hashlib.sha256(path.read_bytes()).hexdigest()
      self.assertRegex(self.manifest, rf"{re.escape(filename)}.*{digest}")
    self.assertIn("1440×900", self.manifest)
    self.assertIn("documentation screenshots rather than runtime/release assets", self.manifest)


if __name__ == "__main__":
  unittest.main()
