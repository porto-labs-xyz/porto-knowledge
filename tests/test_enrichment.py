import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("refresh", ROOT / "scripts/refresh.py")
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)

class SourceSections(unittest.TestCase):
    def test_keeps_subsections_and_stops_at_peer(self):
        text = "# Guide\nIntro\n## Player\nBody\n### States\nLive demo\n## Other\nNot selected\n"
        self.assertEqual(refresh.selected_section(text, "Player"), "## Player\nBody\n### States\nLive demo")

    def test_missing_heading_fails_instead_of_inventing_evidence(self):
        with self.assertRaises(ValueError):
            refresh.selected_section("# Guide\nBody", "Player")

    def test_matching_heading_must_be_exact(self):
        with self.assertRaises(ValueError):
            refresh.selected_section("## Player demo\nBody", "Player")

if __name__ == "__main__":
    unittest.main()
