#!/usr/bin/env python3
"""Build a two-image calligraphy prompt from a reference-free manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STYLE_KERNEL = Path(__file__).resolve().parents[1] / "references/runtime-style-kernel.txt"
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def _load_style_kernel(path: Path = STYLE_KERNEL) -> str:
    kernel = path.read_text(encoding="utf-8").strip()
    lowered = kernel.lower()
    required = (
        "distilled style kernel",
        "contains no source pixels",
        "structural roles",
        "relational composition",
        "ordinary fluent running-regular calligraphy",
    )
    for phrase in required:
        if phrase not in lowered:
            raise ValueError(f"incomplete distilled style kernel: {phrase}")
    forbidden = ("image 3", ".webp", ".png", "sha256", "cadence", "artist named")
    for phrase in forbidden:
        if phrase in lowered:
            raise ValueError(f"unsafe distilled style kernel: {phrase}")
    if HAN.search(kernel):
        raise ValueError("distilled style kernel must contain no Han demonstration glyphs")
    return kernel


def _validate_manifest(manifest: dict) -> tuple[str, list[str]]:
    required_conditions = {
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
    }
    for key, expected in required_conditions.items():
        if manifest.get(key) != expected:
            raise ValueError(f"unsafe semantic-layout manifest: {key}")
    text = str(manifest.get("text", ""))
    columns = [str(value) for value in manifest.get("columns", [])]
    if not text or not columns or "".join(columns) != text:
        raise ValueError("manifest text and columns are inconsistent")
    if manifest.get("reading_order") != "vertical_top_to_bottom_columns_right_to_left":
        raise ValueError("unsupported reading order")
    forbidden_keys = {
        "cadence_condition",
        "cadence_grid",
        "cadence_profile_sha256",
        "runtime_reference",
        "source_sha256",
    }
    if forbidden_keys.intersection(manifest):
        raise ValueError("manifest contains a source-specific runtime condition")
    return text, columns


def build_generic_generation_prompt(manifest: dict) -> str:
    _, columns = _validate_manifest(manifest)
    kernel = _load_style_kernel()
    column_lines = "\n".join(
        f"column {index} from the right, top to bottom: {' '.join(column)}"
        for index, column in enumerate(columns, start=1)
    )
    return f"""Generate one finished monochrome Chinese calligraphy work. The two input images have strictly separate roles.

IMAGE 1 is a compact Unicode identity key. Each colored square is paired with exactly one small printed character. Use it only to identify the exact Unicode character assigned to that color. Do not trace, enlarge, imitate, simplify, traditionalize, substitute, or preserve the system-font contours.

IMAGE 2 is a glyph-free relational pressure field made of irregular colored outlines. Match every keyed character to its colored field exactly once. Each outline is a loose center, occupation and neighbor-pressure cue, not a cell and not a glyph skeleton. Preserve unequal axes, unequal vertical advances, overlaps, retreats, hanging endings and cross-column pressure. Do not straighten the field into rows or clean gutters. Remove every color and guide shape from the finished image.

{kernel}

IMMUTABLE RUNTIME CONTENT
Read vertical columns top to bottom and columns right to left:
{column_lines}

Write exactly the listed characters, each exactly once, with no omissions, substitutions, variant-form changes, merges, duplicated marks, or added writing. Preserve every requested Unicode identity and every structural component required for legibility. There are no character-specific decomposition hints: solve every structure from IMAGE 1 under the same distilled rules.

WHOLE-WORK INTEGRATION
- Write the sheet once as one continuous event; never create independent character cards or assemble fragments.
- Let the relational field determine pressure and retreat, then invent every skeleton anew under the structural roles.
- Preserve reading order without restoring shared baselines, equal centers or repeated private boxes.
- Use dark brown-black soft-brush ink on plain warm xuan paper.

HARD OUTPUT GATE
Output only the finished calligraphy image. Add no title, signature, seal, punctuation, Latin text, border, ornament, color key, guide shape, or unrequested writing."""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    prompt = build_generic_generation_prompt(manifest)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(prompt + "\n", encoding="utf-8")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
