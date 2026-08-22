#!/usr/bin/env python3
"""Build Unicode identity and a source-independent relational layout field.

The legend declares what to write with small neutral glyphs.  The layout image
contains no glyphs and is not derived from any artwork: irregular colored
outlines encode only occurrence, approximate occupation, axis drift and
pressure between neighbors.  Vertical order is preserved without constructing
equal rows, equal columns or a reusable source grid.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


PAPER = (246, 241, 226)
LEGEND_INK = (82, 79, 73)
DEFAULT_FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
STRUCTURAL_ROLES = ("beam", "tower", "cavity", "knot", "suspended")
RELATIONSHIPS = ("press", "retreat", "intrude", "hang")


def split_columns(text: str, columns: int) -> list[str]:
    """Split cleaned text into top-to-bottom, right-to-left reading columns."""

    clean = "".join(char for char in text if not char.isspace())
    if not clean:
        raise ValueError("text contains no visible characters")
    columns = max(1, min(columns, len(clean)))
    base, extra = divmod(len(clean), columns)
    sizes = [base + (1 if index >= columns - extra else 0) for index in range(columns)]
    result: list[str] = []
    cursor = 0
    for size in sizes:
        result.append(clean[cursor : cursor + size])
        cursor += size
    return result


def _rng(seed: str) -> np.random.Generator:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "big"))


def _palette(count: int) -> list[tuple[int, int, int]]:
    """Return distinct colors that cannot be confused with dark ink."""

    colors: list[tuple[int, int, int]] = []
    used: set[tuple[int, int, int]] = set()
    for index in range(count):
        hue = (0.037 + index * 0.6180339887498949) % 1.0
        saturation = 0.48 + 0.06 * (index % 3)
        value = 0.86 - 0.035 * (index % 2)
        rgb = tuple(
            int(round(channel * 255))
            for channel in colorsys.hsv_to_rgb(hue, saturation, value)
        )
        while rgb in used:
            rgb = (rgb[0], rgb[1], 96 + ((rgb[2] - 95) % 128))
        used.add(rgb)
        colors.append(rgb)
    return colors


def _nonuniform_axes(
    *,
    column_count: int,
    width: int,
    margin_x: float,
    rng: np.random.Generator,
) -> tuple[list[float], float]:
    """Return right-to-left axes separated by unequal distances."""

    usable = width - 2 * margin_x
    if column_count == 1:
        return [width * 0.52], usable * 0.72

    gap_pattern = (0.82, 1.19, 0.71, 1.08, 0.91, 1.27)
    gaps = np.asarray(
        [
            gap_pattern[index % len(gap_pattern)] + float(rng.uniform(-0.08, 0.08))
            for index in range(column_count - 1)
        ],
        dtype=float,
    )
    gaps *= usable * 0.82 / float(gaps.sum())
    right_axis = width - margin_x - usable * 0.07
    axes = [right_axis]
    for gap in gaps:
        axes.append(axes[-1] - float(gap))
    average_span = usable / column_count
    return axes, average_span


def _vertical_centers(
    *,
    count: int,
    column_index: int,
    height: int,
    dense: bool,
    rng: np.random.Generator,
) -> tuple[list[float], float]:
    """Accumulate unequal advances; never derive positions from row cells."""

    if count == 1:
        center = height * (0.46 + 0.055 * ((column_index % 3) - 1))
        return [center], height * 0.29

    span_by_count = {2: 0.46, 3: 0.67, 4: 0.82}
    span_fraction = span_by_count.get(count, min(0.90, 0.70 + count * 0.04))
    if dense:
        span_fraction = min(0.92, span_fraction + 0.045)

    top_phase = (-0.047, 0.018, 0.066, -0.012, 0.042)[column_index % 5]
    bottom_phase = (0.025, -0.052, 0.035, -0.018, 0.057)[column_index % 5]
    start = height * (0.50 - span_fraction / 2 + top_phase)
    end = height * (0.50 + span_fraction / 2 + bottom_phase)
    start = max(height * 0.045, start)
    end = min(height * 0.955, end)

    advance_pattern = (0.74, 1.23, 0.88, 1.34, 0.79, 1.09, 0.69)
    advances = np.asarray(
        [
            advance_pattern[(column_index * 2 + index) % len(advance_pattern)]
            + float(rng.uniform(-0.075, 0.075))
            for index in range(count - 1)
        ],
        dtype=float,
    )
    advances *= (end - start) / float(advances.sum())
    centers = [start]
    for advance in advances:
        centers.append(centers[-1] + float(advance))
    typical_advance = (end - start) / (count - 1)
    return centers, typical_advance


def _role_dimensions(role: str) -> tuple[float, float]:
    return {
        "beam": (1.22, 0.84),
        "tower": (0.70, 1.17),
        "cavity": (1.04, 1.02),
        "knot": (0.82, 0.79),
        "suspended": (0.68, 0.88),
    }[role]


def _irregular_polygon(
    *,
    bbox: list[int],
    rng: np.random.Generator,
) -> list[list[int]]:
    x0, y0, x1, y1 = bbox
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    rx = max(5.0, (x1 - x0) / 2)
    ry = max(5.0, (y1 - y0) / 2)
    points: list[list[int]] = []
    count = 12
    phase = float(rng.uniform(-0.20, 0.20))
    for index in range(count):
        angle = phase + 2 * math.pi * index / count
        radial = 0.88 + float(rng.uniform(-0.10, 0.13))
        skew_x = 1.0 + 0.09 * math.sin(angle * 3 + phase)
        skew_y = 1.0 + 0.07 * math.cos(angle * 2 - phase)
        x = int(round(cx + math.cos(angle) * rx * radial * skew_x))
        y = int(round(cy + math.sin(angle) * ry * radial * skew_y))
        points.append([min(x1, max(x0, x)), min(y1, max(y0, y))])
    return points


def _zone_geometry(
    *,
    reading_columns: list[str],
    width: int,
    height: int,
    rng: np.random.Generator,
) -> tuple[list[dict], list[dict]]:
    character_count = sum(len(column) for column in reading_columns)
    dense = character_count >= 8
    margin_x = width * (0.025 if dense else 0.075)
    axes, average_span = _nonuniform_axes(
        column_count=len(reading_columns),
        width=width,
        margin_x=margin_x,
        rng=rng,
    )
    zones: list[dict] = []
    occurrence = 0

    for column_index, column_text in enumerate(reading_columns):
        centers_y, typical_advance = _vertical_centers(
            count=len(column_text),
            column_index=column_index,
            height=height,
            dense=dense,
            rng=rng,
        )
        drift_amplitude = max(width * 0.035, average_span * 0.16)
        drift_pattern = (-0.72, 0.54, -0.18, 0.81, -0.49, 0.29, -0.86)
        for row_index, (char, center_y) in enumerate(zip(column_text, centers_y)):
            role = STRUCTURAL_ROLES[(occurrence + column_index) % len(STRUCTURAL_ROLES)]
            relation = RELATIONSHIPS[(occurrence + row_index) % len(RELATIONSHIPS)]
            width_factor, height_factor = _role_dimensions(role)
            local_drift = drift_pattern[(row_index + column_index) % len(drift_pattern)]
            slant = (
                ((row_index / max(1, len(column_text) - 1)) - 0.5)
                * drift_amplitude
                * (0.52 if column_index % 2 == 0 else -0.61)
            )
            center_x = axes[column_index] + drift_amplitude * local_drift + slant

            base_width = average_span * (1.02 if dense else 0.86)
            base_height = typical_advance * (1.04 if dense else 0.86)
            zone_width = base_width * width_factor * float(rng.uniform(0.94, 1.06))
            zone_height = base_height * height_factor * float(rng.uniform(0.94, 1.06))
            if relation == "press":
                zone_width *= 1.08
                zone_height *= 1.05
            elif relation == "retreat":
                zone_width *= 0.84
                zone_height *= 0.88
            elif relation == "intrude":
                center_x -= average_span * 0.055
                zone_width *= 1.10
            elif relation == "hang":
                center_y -= typical_advance * 0.055
                zone_height *= 0.91

            if character_count <= 5:
                zone_width = min(zone_width, width * 0.46)
                zone_height = min(zone_height, height * 0.38)

            zone_width = min(zone_width, width * 0.48)
            zone_height = min(zone_height, height * 0.43)
            x0 = max(0, int(round(center_x - zone_width / 2)))
            y0 = max(0, int(round(center_y - zone_height / 2)))
            x1 = min(width, int(round(center_x + zone_width / 2)))
            y1 = min(height, int(round(center_y + zone_height / 2)))
            bbox = [x0, y0, max(x0 + 8, x1), max(y0 + 8, y1)]
            zone = {
                "occurrence": occurrence + 1,
                "char": char,
                "column": column_index,
                "row": row_index,
                "structural_role": role,
                "relation_to_next": relation if row_index < len(column_text) - 1 else "terminal",
                "bbox": bbox,
                "polygon": _irregular_polygon(bbox=bbox, rng=rng),
            }
            zones.append(zone)
            occurrence += 1

    relationships: list[dict] = []
    by_column: dict[int, list[dict]] = {}
    for zone in zones:
        by_column.setdefault(int(zone["column"]), []).append(zone)
    for column, column_zones in by_column.items():
        column_zones.sort(key=lambda item: int(item["row"]))
        for first, second in zip(column_zones, column_zones[1:]):
            relationships.append(
                {
                    "from_occurrence": first["occurrence"],
                    "to_occurrence": second["occurrence"],
                    "kind": first["relation_to_next"],
                    "scope": "within_column",
                }
            )
        if column + 1 in by_column:
            other = by_column[column + 1]
            anchor = column_zones[len(column_zones) // 2]
            anchor_y = (anchor["bbox"][1] + anchor["bbox"][3]) / 2
            nearest = min(other, key=lambda item: abs((item["bbox"][1] + item["bbox"][3]) / 2 - anchor_y))
            relationships.append(
                {
                    "from_occurrence": anchor["occurrence"],
                    "to_occurrence": nearest["occurrence"],
                    "kind": "cross_column_pressure",
                    "scope": "between_columns",
                }
            )
    return zones, relationships


def _draw_legend(
    *,
    text: str,
    colors: list[tuple[int, int, int]],
    output: Path,
    width: int,
    height: int,
) -> None:
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    count = len(text)
    grid_columns = max(1, min(4, math.ceil(math.sqrt(count * 1.6))))
    grid_rows = math.ceil(count / grid_columns)
    card_width = width * 0.78
    card_height = min(height * 0.42, max(height * 0.20, grid_rows * height * 0.095))
    card_x0 = int(round((width - card_width) / 2))
    card_y0 = int(round((height - card_height) / 2))
    card_x1 = int(round(card_x0 + card_width))
    card_y1 = int(round(card_y0 + card_height))
    draw.rounded_rectangle(
        (card_x0, card_y0, card_x1, card_y1),
        radius=max(8, int(width * 0.012)),
        fill=(252, 249, 240),
        outline=(218, 211, 195),
        width=max(1, int(width * 0.002)),
    )
    cell_width = card_width / grid_columns
    cell_height = card_height / grid_rows
    font_size = max(20, int(min(64, cell_width * 0.27, cell_height * 0.48)))
    font = ImageFont.truetype(DEFAULT_FONT, font_size)
    swatch_size = max(12, int(font_size * 0.70))
    gap = max(8, int(font_size * 0.28))
    for index, (char, color) in enumerate(zip(text, colors)):
        row, column = divmod(index, grid_columns)
        cx = card_x0 + cell_width * (column + 0.5)
        cy = card_y0 + cell_height * (row + 0.5)
        glyph_box = draw.textbbox((0, 0), char, font=font)
        glyph_width = glyph_box[2] - glyph_box[0]
        glyph_height = glyph_box[3] - glyph_box[1]
        group_width = swatch_size + gap + glyph_width
        sx0 = int(round(cx - group_width / 2))
        sy0 = int(round(cy - swatch_size / 2))
        draw.rectangle((sx0, sy0, sx0 + swatch_size, sy0 + swatch_size), fill=color)
        gx = sx0 + swatch_size + gap
        gy = int(round(cy - glyph_height / 2 - glyph_box[1]))
        draw.text((gx, gy), char, font=font, fill=LEGEND_INK)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=False, compress_level=6)


def _draw_layout(*, zones: list[dict], output: Path, width: int, height: int) -> None:
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    for zone in zones:
        color = tuple(zone["color_rgb"])
        polygon = [tuple(point) for point in zone["polygon"]]
        x0, y0, x1, y1 = zone["bbox"]
        outline_width = max(5, int(min(x1 - x0, y1 - y0) * 0.045))
        draw.line(polygon + [polygon[0]], fill=color, width=outline_width, joint="curve")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=False, compress_level=6)


def make_semantic_layout_guides(
    *,
    text: str,
    legend_output: Path,
    layout_output: Path,
    width: int,
    height: int,
    columns: int,
    seed: str = "relational-layout-v1",
) -> dict:
    clean = "".join(char for char in text if not char.isspace())
    if not clean:
        raise ValueError("text contains no visible characters")
    if width < 256 or height < 256:
        raise ValueError("width and height must both be at least 256")

    reading_columns = split_columns(clean, columns)
    rng = _rng(seed)
    colors = _palette(len(clean))
    zones, relationships = _zone_geometry(
        reading_columns=reading_columns,
        width=width,
        height=height,
        rng=rng,
    )
    for zone, color in zip(zones, colors):
        zone["color_rgb"] = list(color)

    _draw_legend(text=clean, colors=colors, output=legend_output, width=width, height=height)
    _draw_layout(zones=zones, output=layout_output, width=width, height=height)

    manifest = {
        "schema_version": 2,
        "text": clean,
        "reading_order": "vertical_top_to_bottom_columns_right_to_left",
        "columns": reading_columns,
        "width": width,
        "height": height,
        "seed": seed,
        "content_condition": "small_neutral_unicode_legend_only",
        "layout_condition": "relational_colored_fields_without_glyphs",
        "style_condition": "distilled_rules_without_reference_media",
        "layout_mode": "relational_pressure_field",
        "zone_rendering": "irregular_relational_outlines",
        "layout_contains_no_unicode_glyphs": True,
        "uses_character_image_library": False,
        "uses_reference_glyphs": False,
        "uses_external_style_reference": False,
        "uses_source_derived_statistics": False,
        "uses_fixed_grid": False,
        "runtime_image_count": 2,
        "large_layout_encodes": [
            "occurrence_order",
            "approximate_center",
            "approximate_occupancy",
            "structural_role",
            "neighbor_pressure",
        ],
        "large_layout_does_not_encode": [
            "glyph_outline",
            "font_skeleton",
            "radical_geometry",
            "stroke_order",
            "source_artwork_coordinates",
        ],
        "relationships": relationships,
        "zones": zones,
    }
    serialized = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    legend_output.with_suffix(".json").write_text(serialized, encoding="utf-8")
    layout_output.with_suffix(".json").write_text(serialized, encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True)
    parser.add_argument("--legend-out", type=Path, required=True)
    parser.add_argument("--layout-out", type=Path, required=True)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--seed", default="relational-layout-v1")
    args = parser.parse_args()
    manifest = make_semantic_layout_guides(
        text=args.text,
        legend_output=args.legend_out,
        layout_output=args.layout_out,
        width=args.width,
        height=args.height,
        columns=args.columns,
        seed=args.seed,
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
