import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
ASSETS = ROOT / "assets"
SCRIPTS = ROOT / "scripts"
REFERENCES = ROOT / "references"


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


class SkillWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")

    def test_primary_layout_separates_identity_from_relational_geometry(self):
        layout = section(self.skill, "### 2.", "### 3.")
        self.assertIn("make_semantic_layout_guides.py", layout)
        self.assertIn("content-legend.png", layout)
        self.assertIn("layout-zones.png", layout)
        self.assertIn("关系场", layout)
        self.assertIn("不含任何汉字轮廓", layout)
        self.assertNotIn("cadence", layout.lower())
        self.assertNotIn("3×3", layout)

    def test_runtime_declares_two_images_and_no_visual_style_reference(self):
        generation = section(self.skill, "### 3.", "### 4.")
        self.assertIn("两张图", generation)
        self.assertIn("content-legend.png", generation)
        self.assertIn("layout-zones.png", generation)
        self.assertNotIn("style-reference", generation)
        self.assertNotIn("图 3", generation)
        self.assertIn("运行时不得传入任何风格参考图", self.skill)

    def test_installed_skill_contains_no_source_media_or_source_statistics(self):
        media_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
        media = [path for path in ROOT.rglob("*") if path.suffix.lower() in media_suffixes]
        self.assertEqual(media, [])
        asset_files = list(ASSETS.iterdir()) if ASSETS.exists() else []
        self.assertEqual(asset_files, [])
        forbidden_names = {
            "cadence-profile-3x3.json",
            "collaborative-context.webp",
            "reference-provenance.json",
            "style-reference.webp",
        }
        self.assertTrue(forbidden_names.isdisjoint({path.name for path in ROOT.rglob("*")}))

    def test_runtime_style_is_a_distilled_media_free_kernel(self):
        kernel = REFERENCES / "runtime-style-kernel.txt"
        self.assertTrue(kernel.is_file())
        text = kernel.read_text(encoding="utf-8").lower()
        self.assertIn("distilled style kernel", text)
        self.assertIn("contains no source pixels", text)
        self.assertIn("relational composition", text)
        self.assertIn("ordinary fluent running-regular calligraphy", text)

    def test_documented_commands_use_only_reference_free_entrypoints(self):
        self.assertNotIn("python scripts/", self.skill)
        self.assertNotIn("validate_reference_scope.py", self.skill)
        self.assertNotIn("--cadence-profile", self.skill)
        self.assertIn("python3 scripts/make_semantic_layout_guides.py", self.skill)
        self.assertIn("python3 scripts/build_generic_generation_prompt.py", self.skill)
        self.assertIn("包含 `SKILL.md` 的本 skill 根目录", self.skill)

    def test_raw_reference_is_offline_evaluation_only(self):
        self.assertIn("原始参考只用于离线研究和生成后验收", self.skill)
        self.assertIn("不得为了运行 skill 打开抖音", self.skill)
        self.assertIn("不得把研究档案复制回 skill", self.skill)

    def test_rejected_shortcuts_remain_closed(self):
        forbidden_runtime_routes = [
            "build_incremental_character_prompt.py",
            "make_registered_topology_canvas.py",
            "make_strict_lineage_pair_board.py",
            "make_layout_guide.py \\",
        ]
        for route in forbidden_runtime_routes:
            self.assertNotIn(route, self.skill)
        self.assertIn("不得改用逐字增量编辑", self.skill)
        self.assertIn("不得靠反复抽样等待偶然命中", self.skill)

    def test_installed_runtime_package_has_only_reference_free_scripts(self):
        self.assertEqual(
            {path.name for path in SCRIPTS.glob("*.py")},
            {
                "build_generic_generation_prompt.py",
                "make_semantic_layout_guides.py",
                "test_build_generic_generation_prompt.py",
                "test_make_semantic_layout_guides.py",
                "test_skill_workflow_contract.py",
            },
        )


if __name__ == "__main__":
    unittest.main()
