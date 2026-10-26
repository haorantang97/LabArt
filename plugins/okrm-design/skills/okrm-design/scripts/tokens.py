#!/usr/bin/env python3
"""Generate and check an order sheet (design tokens) for the okrm-design method.

generate: writes CSS custom properties and a JSON sheet from a few decisions
          (medium, base size, font pair, accent, fold-derived columns).
check:    validates a JSON sheet against the method's order gates
          (two families at most, three magnitudes of scale, one accent, contrast).

No dependencies beyond the standard library.
"""
import argparse
import json
import math
import sys

MEDIA = {
    # unit, base size default, caption/body/lead/subhead/display/giant ratios, line-height, columns default
    "web": {"unit": "px", "base": 16, "ratios": (0.8125, 1, 1.25, 2.5, 6, 12), "leading": 1.4, "columns": 4},
    "mobile": {"unit": "px", "base": 17, "ratios": (0.75, 1, 1.2, 2, 4, 8), "leading": 1.4, "columns": 2},
    "print": {"unit": "pt", "base": 9.5, "ratios": (0.8, 1, 1.25, 2.5, 8, 16), "leading": 1.35, "columns": 4},
}
LEVELS = ("caption", "body", "lead", "subhead", "display", "giant")
MIN_CAPTION = {"web": 12, "mobile": 11, "print": 6.5}


def rnd(value, places=2):
    value = float(f"{value:.{places}f}")
    return int(value) if value.is_integer() else value


def split_families(stack):
    """First family of a CSS font stack, stripped of quotes."""
    return stack.split(",")[0].strip().strip("\"'")


def hex_to_rgb(value):
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        raise ValueError(f"Not a hex colour: {value}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(hex_to_rgb(a)), luminance(hex_to_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def build(medium, base, sans, serif, mono, accent, columns, paper, ink, measure):
    spec = MEDIA[medium]
    base = base or spec["base"]
    columns = columns or spec["columns"]
    unit = spec["unit"]
    sizes = {name: rnd(base * ratio) for name, ratio in zip(LEVELS, spec["ratios"])}
    line = base * spec["leading"]
    spaces = {f"space-{i}": rnd(line * factor) for i, factor in enumerate((0.5, 1, 2, 3, 5, 8), start=1)}
    families = {"sans": sans}
    if serif:
        families["serif"] = serif
    if mono:
        families["mono"] = mono
    rule = 1 if unit == "px" else 0.5
    return {
        "method": "okrm-design",
        "medium": medium,
        "unit": unit,
        "base": base,
        "fonts": families,
        "sizes": sizes,
        "leading": spec["leading"],
        "spaces": spaces,
        "grid": {"columns": columns, "gutter": rnd(line), "measure_ch": measure, "derivation": "fold"},
        "colors": {"paper": paper, "ink": ink, "accent": accent},
        "rule": rule,
        "furniture_max": 3,
    }


def to_css(sheet):
    u = sheet["unit"]
    lines = [":root {"]
    for role, stack in sheet["fonts"].items():
        lines.append(f"  --font-{role}: {stack};")
    for name, size in sheet["sizes"].items():
        lines.append(f"  --size-{name}: {size}{u};")
    lines.append(f"  --leading: {sheet['leading']};")
    for name, size in sheet["spaces"].items():
        lines.append(f"  --{name}: {size}{u};")
    grid = sheet["grid"]
    lines.append(f"  --grid-columns: {grid['columns']};")
    lines.append(f"  --grid-gutter: {grid['gutter']}{u};")
    lines.append(f"  --measure: {grid['measure_ch']}ch;")
    for name, value in sheet["colors"].items():
        lines.append(f"  --{name}: {value};")
    lines.append(f"  --rule: {sheet['rule']}{u};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def check(sheet):
    """Return a list of failures; empty means the sheet passes the order gates."""
    failures = []
    fonts = sheet.get("fonts", {})
    families = {split_families(stack).lower() for stack in fonts.values()}
    if not fonts or "sans" not in fonts:
        failures.append("fonts: a sans (grotesk) main voice is required")
    if len(families) > 2:
        failures.append(f"fonts: {len(families)} families; at most two")
    sizes = sheet.get("sizes", {})
    missing = [name for name in LEVELS if name not in sizes]
    if missing:
        failures.append(f"sizes: missing {', '.join(missing)}")
    else:
        body = sizes["body"]
        if sizes["giant"] / sizes["caption"] < 8:
            failures.append("sizes: scale spans less than three magnitudes (giant/caption < 8)")
        if sizes["display"] / body < 4:
            failures.append("sizes: no unreasonably large element (display/body < 4)")
        if sizes["caption"] / body < 0.7 or sizes["caption"] >= body:
            failures.append("sizes: caption must sit just below body (0.7–1.0 × body)")
        if sizes["giant"] <= sizes["display"] or sizes["display"] <= sizes["subhead"] or sizes["subhead"] <= sizes["lead"] or sizes["lead"] <= body:
            failures.append("sizes: levels must strictly increase")
        medium = sheet.get("medium", "web")
        if sizes["caption"] < MIN_CAPTION.get(medium, 12):
            failures.append(f"sizes: caption below the legibility floor for {medium}")
    colors = sheet.get("colors", {})
    extra = [k for k in colors if k not in {"paper", "ink", "accent"}]
    if extra:
        failures.append(f"colors: only paper, ink and one accent are allowed (found {', '.join(extra)})")
    try:
        if "paper" in colors and "ink" in colors and contrast(colors["paper"], colors["ink"]) < 4.5:
            failures.append("colors: ink on paper below 4.5:1")
        if colors.get("accent") and contrast(colors["accent"], colors.get("ink", "#000000")) < 3:
            failures.append("colors: accent must contrast with ink at 3:1 or more (text on accent needs 4.5:1)")
    except ValueError as error:
        failures.append(f"colors: {error}")
    grid = sheet.get("grid", {})
    if grid.get("columns", 0) not in (1, 2, 3, 4, 6, 8):
        failures.append("grid: columns should derive from folds or content (1, 2, 3, 4, 6, 8)")
    measure = grid.get("measure_ch", 0)
    if not 45 <= measure <= 75:
        failures.append("grid: measure must stay within 45–75 characters")
    if sheet.get("furniture_max", 3) > 3:
        failures.append("furniture: at most three kinds")
    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="write an order sheet")
    gen.add_argument("--medium", choices=sorted(MEDIA), default="web")
    gen.add_argument("--base", type=float, help="body size in the medium's unit")
    gen.add_argument("--sans", default="Helvetica Neue, Helvetica, Arial, sans-serif")
    gen.add_argument("--serif", default="Times New Roman, Times, serif")
    gen.add_argument("--mono", default="", help="optional monospace second voice (replaces serif if serif is empty)")
    gen.add_argument("--accent", default="#FFE600")
    gen.add_argument("--paper", default="#F4F2EC")
    gen.add_argument("--ink", default="#111111")
    gen.add_argument("--columns", type=int, help="fold-derived column count")
    gen.add_argument("--measure", type=int, default=66, help="line length in characters")
    gen.add_argument("--out", help="CSS output path (stdout if omitted)")
    gen.add_argument("--json", dest="json_out", help="JSON sheet output path")
    chk = sub.add_parser("check", help="validate a JSON order sheet")
    chk.add_argument("sheet")
    args = parser.parse_args(argv)

    if args.command == "generate":
        sheet = build(args.medium, args.base, args.sans, args.serif or None, args.mono or None,
                      args.accent, args.columns, args.paper, args.ink, args.measure)
        failures = check(sheet)
        if failures:
            print("Generated sheet fails its own gates:", file=sys.stderr)
            for f in failures:
                print(f"  - {f}", file=sys.stderr)
            return 1
        css = to_css(sheet)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(css)
        else:
            sys.stdout.write(css)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                json.dump(sheet, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        return 0

    with open(args.sheet, encoding="utf-8") as fh:
        sheet = json.load(fh)
    failures = check(sheet)
    if failures:
        print("Order sheet fails:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("Order sheet passes: two voices at most, three magnitudes of scale, one accent, legible contrast.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
