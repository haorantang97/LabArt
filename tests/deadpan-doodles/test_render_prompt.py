"""Behavioral checks for fixed recipes, references, and narrow edits."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2] / "plugins/deadpan-doodles/skills/deadpan-doodles"
spec = importlib.util.spec_from_file_location("render_prompt", ROOT / "scripts/render_prompt.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def flower():
    return {
        "mode": "generate", "subject_type": "plant",
        "subject": "一枝下垂的白花",
        "scene": "玻璃瓶放在窗台上，窗外有两片云",
        "allocation": {"dominant": "两片宽花瓣", "cluster": "小花心和三片窄花瓣挤在右边",
                       "support": "一根细茎与两片小叶"},
        "construction": "花瓣衔接稍挤，瓶肩宽窄不同",
        "bleed": "花瓣下沿与叶尖",
    }

class BundleTests(unittest.TestCase):
    def test_explicit_cat_anchor_is_checked_and_used(self):
        req = flower()
        req["anchor"] = "cat"
        result = module.build(req, ROOT)
        self.assertEqual(Path(result["referenced_image_paths"][0]).name, "cat-shape-allocation.png")
        self.assertEqual(result["references"][0]["sha256"],
                         "7682c28dc71f1f5c11d03aa562d91c802b3054c36c7cf208a53ba2501406f2e3")

    def test_fixed_recipe_is_verbatim_across_subjects(self):
        core = module.recipe_section((ROOT / "STYLES.md").read_text(), "core")
        for kind, subject in (("plant", "一朵花"), ("animal", "趴在书上的狗"),
                              ("object", "一只茶壶"), ("scene", "小猫在窗边晾毛巾")):
            with self.subTest(kind=kind):
                req = flower()
                req.update(subject_type=kind, subject=subject)
                result = module.build(req, ROOT)
                self.assertEqual(result["prompt"].count(core), 1)
                self.assertIn("主体：" + subject, result["prompt"])
                self.assertNotIn("人物辨识来自", result["prompt"])
                self.assertEqual(result["status"], "standard-bundle")
                self.assertEqual(result["aesthetic_status"], "not-assessed")

    def test_portrait_identity_and_selected_shape_order(self):
        req = flower()
        req.update(subject_type="portrait", subject="一位长发男性",
                   subject_references=[
                       {"path": "assets/style/long-face.png", "role": "identity"},
                       {"path": "assets/style/high-forehead.png", "role": "selected-shape"}])
        result = module.build(req, ROOT)
        self.assertEqual([r["role"] for r in result["references"]],
                         ["style-anchor", "identity", "selected-shape"])
        self.assertEqual([r["image_index"] for r in result["references"]], [1, 2, 3])
        self.assertIn("人物辨识来自", result["prompt"])
        self.assertTrue(all(Path(p).is_absolute() for p in result["referenced_image_paths"]))

    def test_narrow_edit_does_not_append_generation_recipe(self):
        for mode in module.MODES - {"generate"}:
            with self.subTest(mode=mode):
                result = module.build({"mode": mode, "target": "assets/style/high-forehead.png",
                                       "change": "只调整左侧头发末端"}, ROOT)
                self.assertEqual(result["references"][0]["role"], "edit-target")
                self.assertEqual(result["references"][1]["role"], "style-anchor")
                self.assertNotIn("先按本次指定的形状分配", result["prompt"])
                self.assertEqual(result["prompt"].count("本次点名修改："), 1)

    def test_requested_text_and_optional_aspect(self):
        req = flower()
        result = module.build(req, ROOT)
        self.assertNotIn("画幅宽高比：", result["prompt"])
        req.update(text="夏天【快乐】", aspect="3:4")
        # Literal image text is allowed to contain brackets.
        result = module.build(req, ROOT)
        self.assertIn(json.dumps(req["text"], ensure_ascii=False), result["prompt"])
        self.assertIn("画幅宽高比：3:4", result["prompt"])

    def test_explicit_text_only_is_labeled_experiment(self):
        req = flower()
        req["reference_mode"] = "none"
        with self.assertRaisesRegex(ValueError, "exception_reason"):
            module.build(req, ROOT)
        req["exception_reason"] = "用户明确要求本次不附风格图"
        result = module.build(req, ROOT)
        self.assertEqual(result["status"], "experimental-no-style-anchor")
        self.assertEqual(result["references"], [])

    def test_missing_and_replaced_anchor_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            cloned = Path(tmp) / "skill"
            shutil.copytree(ROOT, cloned, ignore=shutil.ignore_patterns("__pycache__"))
            anchor = cloned / "assets/style/high-forehead.png"
            anchor.unlink()
            with self.assertRaisesRegex(ValueError, "缺失"):
                module.build(flower(), cloned, cloned)
            shutil.copyfile(cloned / "assets/style/long-face.png", anchor)
            with self.assertRaisesRegex(ValueError, "校验不符"):
                module.build(flower(), cloned, cloned)

    def test_changed_recipe_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            cloned = Path(tmp) / "skill"
            shutil.copytree(ROOT, cloned, ignore=shutil.ignore_patterns("__pycache__"))
            path = cloned / "STYLES.md"
            path.write_text(path.read_text() + "\naccidental edit\n")
            with self.assertRaisesRegex(ValueError, "校验不符"):
                module.build(flower(), cloned, cloned)

    def test_relocation_does_not_change_prompt(self):
        baseline = module.build(flower(), ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            cloned = Path(tmp) / "skill"
            shutil.copytree(ROOT, cloned, ignore=shutil.ignore_patterns("__pycache__"))
            result = module.build(flower(), cloned, cloned)
            self.assertEqual(result["prompt_sha256"], baseline["prompt_sha256"])
            self.assertTrue(Path(result["referenced_image_paths"][0]).is_relative_to(cloned.resolve()))

    def test_invalid_requests_fail(self):
        invalid = []
        req = flower()
        del req["allocation"]["support"]
        invalid.append(req)
        req = flower()
        req["style"] = "另一套画风"
        invalid.append(req)
        req = flower()
        req["scene"] = "改成蜡笔画风"
        invalid.append(req)
        req = flower()
        req["aspect"] = "0:4"
        invalid.append(req)
        req = flower()
        req["subject_references"] = [{"path": "missing.png", "role": "identity"}]
        invalid.append(req)
        for req in invalid:
            with self.subTest(req=req), self.assertRaises(ValueError):
                module.build(req, ROOT)

    def test_crayon_as_object_is_not_style_injection(self):
        req = flower()
        req["scene"] = "窗台上另放着一盒彩色蜡笔"
        self.assertIn(req["scene"], module.build(req, ROOT)["prompt"])

    def test_cli_writes_valid_json_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / "request.json", Path(tmp) / "call.json"
            source.write_text(json.dumps(flower(), ensure_ascii=False))
            cmd = [sys.executable, "-B", str(ROOT / "scripts/render_prompt.py"),
                   "--request", str(source), "--out", str(out)]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            stored = out.read_bytes()
            self.assertEqual(json.loads(stored)["status"], "standard-bundle")
            second = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(out.read_bytes(), stored)

if __name__ == "__main__":
    unittest.main()
