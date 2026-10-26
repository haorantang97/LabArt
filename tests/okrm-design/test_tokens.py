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
                        "Times New Roman, Times, serif", None, "#FFE600", None, "#F4F2EC", "#111111", 66)
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
                                 "#FFE600", None, "#F4F2EC", "#111111", 66)
                self.assertEqual(tokens.check(s), [])

    def test_scale_spans_three_magnitudes(self):
        s = sheet()
        self.assertGreaterEqual(s["sizes"]["giant"] / s["sizes"]["caption"], 8)
        self.assertGreaterEqual(s["sizes"]["display"] / s["sizes"]["body"], 4)

    def test_css_contains_every_token_once(self):
        css = tokens.to_css(sheet())
        for name in ("--font-sans", "--font-serif", "--size-giant", "--grid-columns", "--accent", "--rule"):
            self.assertEqual(css.count(name + ":"), 1, name)
        self.assertNotIn(".0px", css)

    def test_mono_second_voice_is_allowed(self):
        s = tokens.build("web", None, "Inter, sans-serif", None, "JetBrains Mono, monospace", "#FFE600",
                         None, "#F4F2EC", "#111111", 66)
        self.assertEqual(tokens.check(s), [])
        self.assertIn("--font-mono", tokens.to_css(s))


class CheckTests(unittest.TestCase):
    def test_three_families_fail(self):
        s = sheet(fonts={"sans": "Inter, sans-serif", "serif": "Times, serif", "mono": "Courier, monospace"})
        self.assertTrue(any(f.startswith("fonts:") for f in tokens.check(s)))

    def test_flat_scale_fails(self):
        s = sheet(sizes={"caption": 14, "body": 16, "lead": 18, "subhead": 20, "display": 24, "giant": 28})
        self.assertTrue(any("three magnitudes" in f for f in tokens.check(s)))

    def test_second_accent_fails(self):
        s = sheet(colors={"paper": "#F4F2EC", "ink": "#111111", "accent": "#FFE600", "accent2": "#FF0000"})
        self.assertTrue(any(f.startswith("colors: only paper") for f in tokens.check(s)))

    def test_low_contrast_ink_fails(self):
        s = sheet(colors={"paper": "#F4F2EC", "ink": "#BBBBBB", "accent": "#FFE600"})
        self.assertTrue(any("4.5:1" in f for f in tokens.check(s)))

    def test_default_twelve_column_grid_fails(self):
        s = sheet(grid={"columns": 12})
        self.assertTrue(any(f.startswith("grid: columns") for f in tokens.check(s)))

    def test_measure_outside_range_fails(self):
        s = sheet(grid={"measure_ch": 110})
        self.assertTrue(any("45–75" in f for f in tokens.check(s)))

    def test_small_caption_fails_on_mobile(self):
        s = sheet(medium="mobile", sizes={"caption": 9, "body": 12, "lead": 15, "subhead": 30, "display": 72, "giant": 144})
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
            data["colors"]["accent2"] = "#FF0000"
            js.write_text(json.dumps(data))
            check = subprocess.run([sys.executable, "-B", str(SCRIPT), "check", str(js)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 1)
            self.assertIn("only paper, ink and one accent", check.stdout)


if __name__ == "__main__":
    unittest.main()
