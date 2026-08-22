import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from make_semantic_layout_guides import make_semantic_layout_guides


class SemanticLayoutGuideTests(unittest.TestCase):
    def make(self, text="有风自南翼彼新苗", columns=2, seed="semantic-layout-test"):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        manifest = make_semantic_layout_guides(
            text=text,
            legend_output=root / "content-legend.png",
            layout_output=root / "layout-zones.png",
            width=1024,
            height=1024,
            columns=columns,
            seed=seed,
        )
        return root, manifest

    def test_separates_unicode_identity_from_reference_free_relation_field(self):
        root, manifest = self.make()
        self.assertTrue((root / "content-legend.png").exists())
        self.assertTrue((root / "layout-zones.png").exists())
        self.assertEqual(manifest["content_condition"], "small_neutral_unicode_legend_only")
        self.assertEqual(manifest["layout_condition"], "relational_colored_fields_without_glyphs")
        self.assertEqual(manifest["style_condition"], "distilled_rules_without_reference_media")
        self.assertEqual(manifest["layout_mode"], "relational_pressure_field")
        self.assertFalse(manifest["uses_external_style_reference"])
        self.assertFalse(manifest["uses_source_derived_statistics"])
        self.assertFalse(manifest["uses_fixed_grid"])
        self.assertEqual(manifest["runtime_image_count"], 2)
        self.assertTrue(manifest["layout_contains_no_unicode_glyphs"])
        self.assertFalse(manifest["uses_character_image_library"])
        self.assertFalse(manifest["uses_reference_glyphs"])

    def test_reference_free_contract_holds_for_4_7_9_and_13_characters(self):
        cases = [
            ("山高月小", 1),
            ("松风吹解带", 2),
            ("孤舟夜泊芦花浅水寒", 3),
            ("寒灯照壁雨疏竹影横窗月满庭", 4),
        ]
        for text, columns in cases:
            with self.subTest(text=text):
                _, manifest = self.make(text=text, columns=columns, seed=f"length-{len(text)}")
                serialized = str(manifest).lower()
                self.assertFalse(manifest["uses_fixed_grid"])
                self.assertFalse(manifest["uses_source_derived_statistics"])
                self.assertNotIn("cadence", serialized)
                self.assertNotIn("sha256", serialized)
                self.assertEqual(len(manifest["zones"]), len(text))

    def test_exact_text_and_vertical_reading_order_are_manifested(self):
        _, manifest = self.make()
        self.assertEqual(manifest["text"], "有风自南翼彼新苗")
        self.assertEqual(manifest["columns"], ["有风自南", "翼彼新苗"])
        self.assertEqual(
            manifest["reading_order"],
            "vertical_top_to_bottom_columns_right_to_left",
        )
        self.assertEqual([row["char"] for row in manifest["zones"]], list("有风自南翼彼新苗"))

    def test_every_character_has_one_unique_color_shared_by_legend_and_zone(self):
        root, manifest = self.make()
        colors = [tuple(row["color_rgb"]) for row in manifest["zones"]]
        self.assertEqual(len(colors), len(set(colors)))
        legend = np.asarray(Image.open(root / "content-legend.png").convert("RGB"))
        layout = np.asarray(Image.open(root / "layout-zones.png").convert("RGB"))
        for color in colors:
            color_array = np.asarray(color, dtype=np.uint8)
            self.assertGreater(int(np.all(legend == color_array, axis=2).sum()), 40)
            self.assertGreater(int(np.all(layout == color_array, axis=2).sum()), 120)

    def test_layout_has_no_dark_glyph_like_ink(self):
        root, _ = self.make()
        layout = np.asarray(Image.open(root / "layout-zones.png").convert("RGB"), dtype=np.uint8)
        self.assertEqual(int((layout.mean(axis=2) < 80).sum()), 0)

    def test_zones_are_irregular_polygons_not_rectangular_cells(self):
        _, manifest = self.make(text="孤舟夜泊芦花浅水寒", columns=3, seed="polygonal-nine")
        self.assertEqual(manifest["zone_rendering"], "irregular_relational_outlines")
        for zone in manifest["zones"]:
            polygon = zone["polygon"]
            self.assertGreaterEqual(len(polygon), 8)
            self.assertGreaterEqual(len({x for x, _ in polygon}), 5)
            self.assertGreaterEqual(len({y for _, y in polygon}), 5)

    def test_polygon_points_stay_inside_the_canvas(self):
        _, manifest = self.make(
            text="孤舟夜泊芦花浅水寒",
            columns=3,
            seed="forward-9-reference-free-v1",
        )
        for zone in manifest["zones"]:
            for x, y in zone["polygon"]:
                self.assertGreaterEqual(x, 0)
                self.assertLessEqual(x, manifest["width"])
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(y, manifest["height"])

    def test_column_axes_drift_and_cross_column_rows_do_not_form_bands(self):
        _, manifest = self.make(text="天地玄黄宇宙洪荒日", columns=3, seed="broken-bands")
        by_column = {}
        for zone in manifest["zones"]:
            by_column.setdefault(zone["column"], []).append(zone)
        for zones in by_column.values():
            zones.sort(key=lambda zone: zone["row"])
            centers_x = [(zone["bbox"][0] + zone["bbox"][2]) / 2 for zone in zones]
            self.assertGreater(max(centers_x) - min(centers_x), manifest["width"] * 0.025)

        common_rows = min(len(zones) for zones in by_column.values())
        row_spreads = []
        for row in range(common_rows):
            centers_y = []
            for zones in by_column.values():
                zone = sorted(zones, key=lambda item: item["row"])[row]
                centers_y.append((zone["bbox"][1] + zone["bbox"][3]) / 2)
            row_spreads.append(max(centers_y) - min(centers_y))
        self.assertGreaterEqual(
            sum(spread > manifest["height"] * 0.035 for spread in row_spreads),
            2,
        )

    def test_within_column_advances_are_not_equal_cell_steps(self):
        _, manifest = self.make(
            text="寒灯照壁雨疏竹影横窗月满庭",
            columns=3,
            seed="unequal-advances",
        )
        for column in range(3):
            zones = sorted(
                [zone for zone in manifest["zones"] if zone["column"] == column],
                key=lambda zone: zone["row"],
            )
            centers = [(zone["bbox"][1] + zone["bbox"][3]) / 2 for zone in zones]
            advances = [round(second - first, 1) for first, second in zip(centers, centers[1:])]
            self.assertGreaterEqual(len(set(advances)), min(2, len(advances)))

    def test_sparse_content_does_not_inflate_to_poster_cells(self):
        for text, columns in (("欹危饶地势", 2), ("松月", 2)):
            _, manifest = self.make(text=text, columns=columns, seed=f"sparse-{len(text)}")
            widths = [row["bbox"][2] - row["bbox"][0] for row in manifest["zones"]]
            heights = [row["bbox"][3] - row["bbox"][1] for row in manifest["zones"]]
            self.assertLessEqual(max(widths), round(manifest["width"] * 0.46))
            self.assertLessEqual(max(heights), round(manifest["height"] * 0.38))

    def test_deterministic_for_same_seed(self):
        first_root, first = self.make(seed="repeatable")
        first_legend = (first_root / "content-legend.png").read_bytes()
        first_layout = (first_root / "layout-zones.png").read_bytes()
        second_root, second = self.make(seed="repeatable")
        self.assertEqual(first, second)
        self.assertEqual(first_legend, (second_root / "content-legend.png").read_bytes())
        self.assertEqual(first_layout, (second_root / "layout-zones.png").read_bytes())


if __name__ == "__main__":
    unittest.main()
