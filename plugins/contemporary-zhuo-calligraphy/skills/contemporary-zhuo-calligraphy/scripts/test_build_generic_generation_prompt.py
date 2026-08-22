import re
import unittest

from build_generic_generation_prompt import build_generic_generation_prompt


HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


class GenericGenerationPromptTests(unittest.TestCase):
    def manifest(self, text, columns):
        return {
            "text": text,
            "columns": columns,
            "reading_order": "vertical_top_to_bottom_columns_right_to_left",
            "content_condition": "small_neutral_unicode_legend_only",
            "layout_condition": "relational_colored_fields_without_glyphs",
            "style_condition": "distilled_rules_without_reference_media",
            "layout_mode": "relational_pressure_field",
            "layout_contains_no_unicode_glyphs": True,
            "uses_character_image_library": False,
            "uses_reference_glyphs": False,
            "uses_external_style_reference": False,
            "uses_source_derived_statistics": False,
            "uses_fixed_grid": False,
            "runtime_image_count": 2,
            "zone_rendering": "irregular_relational_outlines",
        }

    def test_runtime_text_is_the_only_han_content_in_prompt(self):
        text = "欹危饶地势"
        prompt = build_generic_generation_prompt(self.manifest(text, ["欹危", "饶地势"]))
        self.assertEqual(HAN.findall(prompt), list(text))

    def test_columns_are_serialized_once_in_right_to_left_order(self):
        prompt = build_generic_generation_prompt(
            self.manifest("寒灯照壁雨疏竹影横窗月满庭", ["寒灯照壁", "雨疏竹影", "横窗月满庭"])
        )
        self.assertIn("column 1 from the right, top to bottom: 寒 灯 照 壁", prompt)
        self.assertIn("column 2 from the right, top to-bottom: 雨 疏 竹 影".replace("to-bottom", "to bottom"), prompt)
        self.assertIn("column 3 from the right, top to bottom: 横 窗 月 满 庭", prompt)
        self.assertEqual(prompt.count("寒"), 1)
        self.assertEqual(prompt.count("庭"), 1)

    def test_prompt_has_exactly_two_runtime_image_roles(self):
        prompt = build_generic_generation_prompt(self.manifest("松月", ["松", "月"]))
        self.assertIn("The two input images have strictly separate roles", prompt)
        self.assertIn("IMAGE 1", prompt)
        self.assertIn("IMAGE 2", prompt)
        self.assertNotIn("IMAGE 3", prompt)
        lowered = prompt.lower()
        self.assertNotIn("style-reference", lowered)
        self.assertNotIn("fixed whole-work handwriting reference", lowered)
        self.assertNotIn("source-derived", lowered)

    def test_prompt_embeds_distilled_kernel_and_relational_composition(self):
        prompt = build_generic_generation_prompt(
            self.manifest("藏壑松聲雲窗墨氣生", ["藏壑松", "聲雲窗", "墨氣生"])
        ).lower()
        self.assertIn("distilled style kernel", prompt)
        self.assertIn("relational composition", prompt)
        self.assertIn("structural roles", prompt)
        self.assertIn("not a grid", prompt)
        self.assertIn("ordinary fluent running-regular calligraphy", prompt)

    def test_contains_no_character_specific_exception_language(self):
        prompt = build_generic_generation_prompt(self.manifest("欹危饶地势", ["欹危", "饶地势"]))
        lowered = prompt.lower()
        self.assertIn("no character-specific decomposition hints", lowered)
        self.assertIn("preserve every requested unicode identity", lowered)
        self.assertNotIn("radical named", lowered)
        self.assertNotIn("simplified form of", lowered)

    def test_rejects_reference_media_grid_or_source_statistics(self):
        for key in (
            "uses_external_style_reference",
            "uses_source_derived_statistics",
            "uses_fixed_grid",
        ):
            unsafe = self.manifest("松月", ["松", "月"])
            unsafe[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                build_generic_generation_prompt(unsafe)

    def test_rejects_unsafe_or_inconsistent_manifest(self):
        unsafe = self.manifest("松月", ["松", "月"])
        unsafe["runtime_image_count"] = 3
        with self.assertRaises(ValueError):
            build_generic_generation_prompt(unsafe)
        inconsistent = self.manifest("松月", ["松", "山"])
        with self.assertRaises(ValueError):
            build_generic_generation_prompt(inconsistent)


if __name__ == "__main__":
    unittest.main()
