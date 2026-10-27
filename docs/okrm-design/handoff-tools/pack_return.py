#!/usr/bin/env python3
"""Pack the results of the stage-1 experiment into one zip for the return.

Usage:
  python3 pack_return.py --manifest manifest.json \
      --run A1=/path/to/work-A1 --run C1=/path/to/work-C1 [--run A2=... --run C2=...] \
      --judge-room /path/to/judge-room --key /path/to/key.json \
      [--operator-notes OPERATOR-NOTES.md] --out okrm-return-01.zip

From each run folder it takes out/ (everything) and transcript/ (if present; put the exported
session there). From the judge room it takes everything (including judge.md) and judge-room/transcript/.
It checks every run for the twelve PNGs and their pixel sizes, adds file sizes and sha256 hashes to
the manifest, and zips it all under okrm-return-<id>/.
"""
import argparse, hashlib, json, pathlib, shutil, struct, tempfile, zipfile

SIZES = {(1,1):(1600,1100),(1,2):(1800,1100),(2,1):(1800,1200),(2,2):(1600,1100),(3,1):(1200,1700),(3,2):(1800,1000),
         (4,1):(1200,1600),(4,2):(1800,1200),(5,1):(1600,1000),(5,2):(1200,1000),(6,1):(1800,1100),(6,2):(1600,1100)}
def png_size(p):
    with open(p, "rb") as f: h = f.read(24)
    return struct.unpack(">II", h[16:24]) if h[:8] == b"\x89PNG\r\n\x1a\n" else None
ap = argparse.ArgumentParser()
ap.add_argument("--manifest", required=True); ap.add_argument("--run", action="append", required=True)
ap.add_argument("--judge-room", required=True); ap.add_argument("--key", required=True)
ap.add_argument("--operator-notes"); ap.add_argument("--out", required=True)
a = ap.parse_args()
man = json.loads(pathlib.Path(a.manifest).read_text()); rid = man.get("return_id", "01")
tmp = pathlib.Path(tempfile.mkdtemp()); root = tmp / f"okrm-return-{rid}"; root.mkdir()
checks = {}
for r in a.run:
    lab, p = r.split("=", 1); p = pathlib.Path(p); dst = root / "runs" / lab
    shutil.copytree(p / "out", dst / "out")
    if (p / "transcript").exists(): shutil.copytree(p / "transcript", dst / "transcript")
    probs = []
    for (n, i), (w, h) in SIZES.items():
        f = p / "out" / f"b{n}-{i}.png"
        if not f.exists(): probs.append(f"missing b{n}-{i}.png")
        elif png_size(f) != (w, h): probs.append(f"b{n}-{i}.png is {png_size(f)}, expected {(w, h)}")
    if not (p / "transcript").exists(): probs.append("no transcript/")
    checks[lab] = probs or ["ok"]
shutil.copytree(a.judge_room, root / "judge" / "judge-room"); shutil.copy(a.key, root / "judge" / "key.json")
if a.operator_notes: shutil.copy(a.operator_notes, root / "OPERATOR-NOTES.md")
files = {}
for f in sorted(root.rglob("*")):
    if f.is_file(): files[str(f.relative_to(root))] = {"bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
man["checks"] = checks; man["files"] = files
(root / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(root.rglob("*")):
        if f.is_file(): z.write(f, f.relative_to(tmp))
print("checks:", json.dumps(checks, indent=1, ensure_ascii=False)); print("wrote", a.out)
