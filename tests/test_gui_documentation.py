import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GuiDocumentationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cls.how_to = (ROOT / "docs" / "guides" / "how-to-play.md").read_text(
      encoding="utf-8"
    )
    cls.gui = (ROOT / "docs" / "guides" / "gui-how-to-play.md").read_text(
      encoding="utf-8"
    )
    cls.gui_readme = (ROOT / "gui" / "README.md").read_text(encoding="utf-8")

  def test_quickstarts_agree_on_command_url_and_campaign(self):
    for text in (self.readme, self.how_to, self.gui, self.gui_readme):
      self.assertIn("cargo run --bin vital-margin-gui", text)
      self.assertIn("competitive-regional-v1", text)
    for text in (self.readme, self.how_to, self.gui):
      self.assertIn("http://127.0.0.1:7878", text)

  def test_canonical_guide_covers_common_player_failures(self):
    for marker in (
      "Ctrl-C",
      "127.0.0.1:8787",
      "connection refused",
      "address is already in use",
      "demo data",
      "Validation rejects",
      "existing session ID is unknown",
      "Audio is silent",
      "user gesture",
      "in-memory",
    ):
      self.assertIn(marker.lower(), self.gui.lower())

  def test_static_demo_is_distinguished_from_live_play(self):
    for text in (self.readme, self.how_to, self.gui, self.gui_readme):
      self.assertIn("gui/index.html", text)
      self.assertIn("demo", text.lower())

  def test_gui_guide_links_resolve(self):
    self.assertTrue((ROOT / "docs" / "guides" / "gui-how-to-play.md").is_file())
    self.assertIn("docs/guides/gui-how-to-play.md", self.readme)
    self.assertIn("gui-how-to-play.md", self.how_to)
    self.assertIn("../docs/guides/gui-how-to-play.md", self.gui_readme)


if __name__ == "__main__":
  unittest.main()
