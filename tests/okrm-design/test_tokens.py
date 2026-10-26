"""Behavioral checks for the okrm-design order-sheet generator and checker."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2] / "plugins/okrm-design/skills/okrm-design"
SCRIPT = ROOT / "scripts/tokens.py"
spec = importlib.util.spec_from_file_location("tokens", SCRIPT)
tokens = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tokens)


def sheet(**overrides):
    base = tokens.build("web", None, "Helvetica Neue, Helvetica, Arial, sans-serif",
                        "Times New Roman, Times, serif", None, "#1F3FBF", None, "#F4F2EC", "#111111", 66)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key].update(value)
        else:
            base[key] = value
    return base


class GenerateTests(unittest.TestCase):
    def test_every_medium_passes_its_own_gates(self):
        for medium in tokens.MEDIA:
            with self.subTest(medium=medium):
                s = tokens.build(medium, None, "Helvetica, Arial, sans-serif", "Times, serif", None,
                                 "#1F3FBF", None, "#F4F2EC", "#111111", 66)
                self.assertEqual(tokens.check(s), [])

    def test_two_poles_and_no_middle(self):
        s = sheet()
        self.assertGreaterEqual(s["sizes"]["monument"] / s["sizes"]["body"], 8)
        self.assertTrue(all(not 2 < v / s["sizes"]["body"] < 8 for v in s["sizes"].values()))

    def test_css_contains_every_token_once(self):
        css = tokens.to_css(sheet())
        for name in ("--font-sans", "--font-serif", "--size-monument", "--tracking-label", "--grid-columns",
                     "--border-plate", "--field", "--rule"):
            self.assertEqual(css.count(name + ":"), 1, name)
        self.assertNotIn(".0px", css)

    def test_mono_second_voice_is_allowed(self):
        s = tokens.build("web", None, "Inter, sans-serif", None, "Courier New, monospace", "#1F3FBF",
                         None, "#F4F2EC", "#111111", 66)
        self.assertEqual(tokens.check(s), [])
        self.assertIn("--font-mono", tokens.to_css(s))


class CheckTests(unittest.TestCase):
    def test_three_families_fail(self):
        s = sheet(fonts={"sans": "Inter, sans-serif", "serif": "Times, serif", "mono": "Courier, monospace"})
        self.assertTrue(any(f.startswith("fonts:") for f in tokens.check(s)))

    def test_headline_in_the_middle_fails(self):
        s = sheet(sizes={"caption": 13, "body": 16, "lead": 20, "label": 12, "monument": 64})
        failures = tokens.check(s)
        self.assertTrue(any("middle" in f for f in failures), failures)

    def test_small_monument_fails(self):
        s = sheet(sizes={"caption": 13, "body": 16, "lead": 20, "label": 12, "monument": 30})
        self.assertTrue(any("monument" in f for f in tokens.check(s)))

    def test_second_colour_fails(self):
        s = sheet(colors={"paper": "#F4F2EC", "ink": "#111111", "field": "#1F3FBF", "accent": "#FF0000"})
        self.assertTrue(any(f.startswith("colors: only paper") for f in tokens.check(s)))

    def test_field_used_as_accent_fails(self):
        s = sheet(field_use="accent")
        self.assertTrue(any("material" in f for f in tokens.check(s)))

    def test_field_that_cannot_carry_type_fails(self):
        s = sheet(colors={"paper": "#F4F2EC", "ink": "#777777", "field": "#888888"})
        self.assertTrue(any("cannot carry type" in f for f in tokens.check(s)))

    def test_low_contrast_ink_fails(self):
        s = sheet(colors={"paper": "#F4F2EC", "ink": "#BBBBBB", "field": "#1F3FBF"})
        self.assertTrue(any("4.5:1" in f for f in tokens.check(s)))

    def test_default_twelve_column_grid_fails(self):
        s = sheet(grid={"columns": 12})
        self.assertTrue(any(f.startswith("grid: columns") for f in tokens.check(s)))

    def test_measure_outside_range_fails(self):
        s = sheet(grid={"measure_ch": 110})
        self.assertTrue(any("45–75" in f for f in tokens.check(s)))

    def test_small_caption_fails_on_mobile(self):
        s = sheet(medium="mobile", sizes={"caption": 9, "body": 12, "lead": 14, "label": 9, "monument": 120})
        self.assertTrue(any("legibility floor" in f for f in tokens.check(s)))


class CliTests(unittest.TestCase):
    def test_generate_then_check_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            css = Path(tmp) / "tokens.css"
            js = Path(tmp) / "tokens.json"
            run = subprocess.run([sys.executable, "-B", str(SCRIPT), "generate", "--medium", "mobile",
                                  "--out", str(css), "--json", str(js)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(css.read_text().startswith(":root {"))
            data = json.loads(js.read_text())
            self.assertEqual(data["medium"], "mobile")
            check = subprocess.run([sys.executable, "-B", str(SCRIPT), "check", str(js)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout)
            data["colors"]["accent"] = "#FF0000"
            js.write_text(json.dumps(data))
            check = subprocess.run([sys.executable, "-B", str(SCRIPT), "check", str(js)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 1)
            self.assertIn("only paper, ink and one field colour", check.stdout)


if __name__ == "__main__":
    unittest.main()
