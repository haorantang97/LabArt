#!/usr/bin/env python3
"""Build a blind judge room from finished runs. The judge writes verdict.md in the room.

Usage:
  python3 make_judge_room.py --run A1=/path/to/work-A1 --run C1=/path/to/work-C1 [--run A2=... --run C2=...] \
      --kit /path/to/judge-kit --out /path/to/judge-room --key /path/to/key.json [--seed 20261101]

Each run folder must contain out/b{n}-{i}.png for n=1..6, i=1..2.
Writes judge-room/ (briefs.md, JUDGE.md, images/, boards/) and key.json OUTSIDE the room.
Never put key.json inside the judge room.
"""
import argparse, json, random, shutil, string, pathlib, sys

ap = argparse.ArgumentParser()
ap.add_argument("--run", action="append", required=True, help="LABEL=path to a work folder")
ap.add_argument("--kit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--key", required=True)
ap.add_argument("--seed", type=int, default=20261101)
a = ap.parse_args()
runs = dict(r.split("=", 1) for r in a.run)
kit, room, keyp = pathlib.Path(a.kit), pathlib.Path(a.out), pathlib.Path(a.key)
if keyp.resolve().is_relative_to(room.resolve()): sys.exit("key.json must be outside the judge room")
briefs = None
for lab, p in runs.items():
    b = pathlib.Path(p) / "briefs.md"
    if b.exists(): briefs = b; break
if not briefs: sys.exit("briefs.md not found in any run folder")
missing = [f"{lab}: out/b{n}-{i}.png" for lab, p in runs.items() for n in range(1, 7) for i in (1, 2) if not (pathlib.Path(p) / "out" / f"b{n}-{i}.png").exists()]
if missing: print("WARNING missing images:\n  " + "\n  ".join(missing))
room.mkdir(parents=True, exist_ok=True); (room / "images").mkdir(exist_ok=True); (room / "boards").mkdir(exist_ok=True)
shutil.copy(briefs, room / "briefs.md"); shutil.copy(kit / "JUDGE.md", room / "JUDGE.md")
random.seed(a.seed); letters = "PQRSTUVW"; key = {}
for n in range(1, 7):
    order = list(runs); random.shuffle(order); key[n] = {}
    for L, lab in zip(letters, order):
        key[n][L] = lab
        for i in (1, 2):
            src = pathlib.Path(runs[lab]) / "out" / f"b{n}-{i}.png"
            if src.exists(): shutil.copy(src, room / "images" / f"b{n}-{L}-{i}.png")
keyp.write_text(json.dumps(key, indent=1))
# Boards: PNG via Pillow if available, else HTML (render with render.mjs).
try:
    from PIL import Image, ImageDraw, ImageFont
    for n in range(1, 7):
        rows = list(key[n]); W, RH, LW, G = 2400, 680, 90, 16
        board = Image.new("RGB", (W, 60 + len(rows) * (RH + G)), (138, 138, 138)); d = ImageDraw.Draw(board)
        font = small = None
        for cand in ("DejaVuSans.ttf", "/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf",
                     "/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
            try: font = ImageFont.truetype(cand, 56); small = ImageFont.truetype(cand, 28); break
            except Exception: continue
        if font is None: font = small = ImageFont.load_default()
        d.text((24, 14), f"Brief {n}", fill="white", font=small)
        cw = (W - 24 * 2 - LW - G * 2) // 2
        for r, L in enumerate(rows):
            y = 60 + r * (RH + G); d.text((24, y + 8), L, fill="white", font=font)
            for i in (1, 2):
                f = room / "images" / f"b{n}-{L}-{i}.png"; x = 24 + LW + (i - 1) * (cw + G)
                d.rectangle([x, y, x + cw, y + RH], fill=(122, 122, 122))
                if f.exists():
                    im = Image.open(f).convert("RGB"); im.thumbnail((cw, RH)); board.paste(im, (x + (cw - im.width) // 2, y + (RH - im.height) // 2))
        board.save(room / "boards" / f"board-b{n}.png")
    print("boards written as PNG")
except ImportError:
    for n in range(1, 7):
        rows = "".join(f'<div class="row"><div class="lab">{L}</div>' + "".join(f'<div class="cell"><img src="../images/b{n}-{L}-{i}.png"></div>' for i in (1, 2)) + "</div>" for L in key[n])
        h = 60 + len(key[n]) * 696
        (room / "boards" / f"board-b{n}.html").write_text(f'<!doctype html><meta charset="utf-8"><meta name="size" content="2400x{h}"><style>html,body{{margin:0;background:#8a8a8a;font:28px sans-serif;color:#fff}}.head{{height:60px;padding:14px 24px;box-sizing:border-box}}.row{{display:grid;grid-template-columns:90px 1fr 1fr;height:680px;gap:16px;padding:0 24px 16px}}.lab{{font-size:56px}}.cell{{display:flex;align-items:center;justify-content:center;background:#7a7a7a;overflow:hidden}}.cell img{{max-width:100%;max-height:100%;object-fit:contain}}</style><div class="head">Brief {n}</div>{rows}')
    print("Pillow not installed: boards written as HTML. Render them:\n  node render.mjs", room / "boards")
print("judge room:", room, "\nkey (keep away from the judge):", keyp)
