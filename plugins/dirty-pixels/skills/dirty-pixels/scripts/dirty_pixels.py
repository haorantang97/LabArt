#!/usr/bin/env python3
"""dirty_pixels.py v4 — two-layer "dirty pixels" renderer on pure black.

Canon references (approved 2026-08-24):
  * PRIMARY / composition — YUDHO "The Wanderer" (D1RTYPXLS #017, 2024):
    solid dithered masses anchor the scene and NEVER move; a particle-dust
    figure carries the energy; ONE radial star burst is the focal point;
    streak dashes near the burst travel along their own direction; the sky
    stays almost entirely pure black.
  * SECONDARY / boundary & motion — YUDHO "Husk//Halo" (INSILIO, 2025):
    the figure is a stable dithered mass, ALL motion lives in the dash ring,
    and a wide moat of pure black separates the two.

The one law learned from those works: clear boundaries do not come from
strokes — they come from the CONTRAST between a static solid-dither layer
(form) and a moving particle/dash layer (energy). Render everything as
strokes and the picture turns into fur.

Layers, drawn in this order:
  1. MASS   — large smooth bright regions, Bayer-dithered at output-pixel
              scale. Static in every frame. This is what makes the forms read.
  2. DUST   — the v3 stroke tracer, now weighted toward edges and bright
              detail OUTSIDE the masses. Moves along the structure-tensor
              orientation field (--motion flow) or breathes (--motion shimmer).
  3. BURST  — the top-K brightest local maxima become radial star bursts;
              their dotted rays stream outward, wrapping seamlessly.
  4. RAIN   — parallel streak dashes that exist ONLY near burst zones and
              slide along their own direction, one full dash period per loop
              (so frame N == frame 0 exactly). Rain never sits still.
  5. STARS  — a few isolated static dots in the void.

Only numpy + Pillow (ffmpeg only for --mp4). No network. Deterministic per
seed: same input + same command + same seed = the same file, byte for byte.

Usage:
  python3 dirty_pixels.py INPUT [-o OUT]
      [--preset wanderer|faithful|poster|curl|detail|web]
      [--palette ash|blood|neon|violet|phosphor|ember|gold]
      [--size 1400] [--seconds 4] [--fps 12] [--seed 305] [--mp4]
      [--mass 1.0] [--bursts -1] [--rain 1.0] [--rain-angle -14] [--rain-speed 1]
      ... (run with -h for the full parameter manual)
"""

import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

# --------------------------------------------------------------- palettes
# hues[0] is the body colour (mass + most dust), the LAST hue is the hottest
# (burst cores, brightest marks). "ash" is the canon: white pixels on black.

PALETTES = {
    "ash": ["#d9d9e2", "#8a8a9c", "#ffffff"],
    "blood": ["#ff1f1f", "#c40d0d", "#ff6b6b"],
    "neon": ["#ff2fd0", "#3a2bff", "#ff2020", "#ffffff"],
    "violet": ["#a78bfa", "#6d4bd8", "#e8dcff", "#e8a33d"],
    "phosphor": ["#31ff6a", "#0fb03e", "#c9ffd6"],
    "ember": ["#ff7a1a", "#ff3b1f", "#ffd08a"],
    "gold": ["#ffc24a", "#c8860f", "#fff3d0"],
}


# --------------------------------------------------------------- presets
# A preset freezes every style-defining parameter. Explicit CLI flags win.
# "wanderer" is the canon preset; the v3 presets are kept so that old
# commands still run, but v4 changed the rain layer everywhere (it moves
# now), so v3 GIFs are not reproduced bit-for-bit.

PRESETS = {
    # THE CANON — modelled on The Wanderer + Husk//Halo. Solid masses,
    # sparse dust, one to three bursts, moving rain, >=50% pure black.
    "wanderer": dict(supersample=2, thickness=1.0, density=0.85, sparsity=1.9,
                     stroke=3, jitter=0.10, curve=0.08, coherence=3.0,
                     rain=1.0, stars=0.7, gamma=2.2, edge=0.9,
                     mass=1.0, bursts=-1, floor=0.45, boil=1.6),
    "faithful": dict(supersample=1, thickness=1.0, density=1.0, sparsity=1.3,
                     stroke=8, jitter=0.25, curve=0.15, coherence=3.0,
                     rain=1.0, stars=1.0, gamma=1.6, edge=0.6,
                     mass=0.0, bursts=0, boil=0.0),
    "poster": dict(supersample=3, thickness=1.0, density=1.7, sparsity=1.2,
                   stroke=10, jitter=0.06, curve=0.10, coherence=3.0,
                   rain=0.3, stars=0.5, gamma=2.2, edge=0.4,
                   mass=0.0, bursts=0, boil=0.0),
    "curl": dict(supersample=2, thickness=1.0, density=0.85, sparsity=1.6,
                 stroke=11, jitter=0.15, curve=0.6, coherence=2.2,
                 rain=0.4, stars=0.5, gamma=2.5, edge=0.5,
                 mass=0.0, bursts=0, boil=0.0),
    "detail": dict(supersample=3, thickness=1.0, density=2.0, sparsity=1.6,
                   stroke=5, jitter=0.10, curve=0.08, coherence=3.0,
                   rain=0.6, stars=0.6, gamma=2.8, edge=0.5,
                   mass=0.0, bursts=0, boil=0.0),
    "web": dict(supersample=2, thickness=1.0, density=1.4, sparsity=1.3,
                stroke=9, jitter=0.10, curve=0.12, coherence=3.0,
                rain=0.5, stars=0.6, gamma=1.9, edge=0.5,
                mass=0.0, bursts=0, boil=0.0),
}


BAYER8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
], dtype=np.float32) / 64.0


def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def smooth(a, passes=2):
    for _ in range(passes):
        b = a.copy()
        b[1:-1, 1:-1] = (a[1:-1, 1:-1] * 4 + a[:-2, 1:-1] + a[2:, 1:-1]
                         + a[1:-1, :-2] + a[1:-1, 2:]) / 8.0
        a = b
    return a


def flow_field(gray, coherence=3.0):
    """Local edge ORIENTATION from the structure tensor.

    A gradient rotated 90 degrees circulates: strokes collapse into little
    vortices around every highlight. The structure tensor yields an
    orientation (mod 180) averaged over a neighbourhood — the direction the
    local structure actually runs — and orientation fields do not circulate.
    """
    from PIL import Image as _Image
    h, w = gray.shape
    k = max(1.0, coherence)
    sw, sh = max(16, int(w / k)), max(16, int(h / k))
    small = np.asarray(
        _Image.fromarray((gray * 255).astype(np.uint8)).resize((sw, sh), _Image.LANCZOS),
        dtype=np.float32) / 255.0

    g = smooth(small, 1)
    gy, gx = np.gradient(g)
    j11 = smooth(gx * gx, 4)
    j22 = smooth(gy * gy, 4)
    j12 = smooth(gx * gy, 4)
    theta = 0.5 * np.arctan2(2.0 * j12, j11 - j22)
    tx, ty = -np.sin(theta), np.cos(theta)

    trace = j11 + j22
    aniso = np.sqrt((j11 - j22) ** 2 + 4.0 * j12 ** 2) / (trace + 1e-9)
    flat = aniso < 0.25
    tx = np.where(flat, 0.94, tx).astype(np.float32)
    ty = np.where(flat, -0.34, ty).astype(np.float32)
    tx, ty = smooth(tx, 2), smooth(ty, 2)

    up = lambda a: np.asarray(_Image.fromarray(a).resize((w, h), _Image.BILINEAR), dtype=np.float32)
    an = up(smooth(aniso.astype(np.float32), 2))
    tx, ty = up(tx), up(ty)
    n = np.hypot(tx, ty) + 1e-6
    return (tx / n).astype(np.float32), (ty / n).astype(np.float32), np.clip(an, 0, 1)


def sample(field, xq, yq):
    h, w = field.shape
    x = np.clip(xq, 0, w - 1.001)
    y = np.clip(yq, 0, h - 1.001)
    x0, y0 = x.astype(np.int32), y.astype(np.int32)
    ax, ay = x - x0, y - y0
    x1, y1 = np.minimum(x0 + 1, w - 1), np.minimum(y0 + 1, h - 1)
    return ((field[y0, x0] * (1 - ax) + field[y0, x1] * ax) * (1 - ay)
            + (field[y1, x0] * (1 - ax) + field[y1, x1] * ax) * ay)


def stamp(canvas, xs, ys, hue_idx, weight, thickness=1):
    """Hard-edged marks into per-hue planes; supersampling softens later."""
    n_hues, H, W = canvas.shape
    ix0 = np.rint(xs).astype(np.int32)
    iy0 = np.rint(ys).astype(np.int32)
    t = max(1, int(thickness))
    for dy in range(t):
        for dx in range(t):
            ix, iy = ix0 + dx, iy0 + dy
            ok = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < H) & (weight > 0)
            if not np.any(ok):
                continue
            flat = hue_idx[ok].astype(np.int64) * (H * W) + iy[ok] * W + ix[ok]
            np.add.at(canvas.reshape(-1), flat, weight[ok])


def simplified(gray, factor):
    """Downscale-upscale copy of the image: only forms >= factor px survive."""
    H, W = gray.shape
    sw, sh = max(8, int(W / factor)), max(8, int(H / factor))
    return np.asarray(
        Image.fromarray((gray * 255).astype(np.uint8)).resize((sw, sh), Image.LANCZOS)
        .resize((W, H), Image.BICUBIC), dtype=np.float32) / 255.0


def drop_small_components(mask, min_frac=0.0018):
    """Remove connected blobs smaller than min_frac of the canvas.

    Pure numpy: label by iterative max-propagation on a /4-scale copy —
    reference masses are FEW and LARGE; dither confetti is not a mass."""
    H, W = mask.shape
    sw, sh = max(8, W // 4), max(8, H // 4)
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                   .resize((sw, sh), Image.BILINEAR), dtype=np.float32) > 127
    lab = np.where(m, np.arange(m.size, dtype=np.int64).reshape(m.shape) + 1, 0)
    for _ in range(max(sw, sh)):
        prev = lab
        p = np.pad(lab, 1)
        lab = np.maximum.reduce([p[1:-1, 1:-1], p[:-2, 1:-1], p[2:, 1:-1],
                                 p[1:-1, :-2], p[1:-1, 2:]])
        lab = np.where(m, lab, 0)
        if np.array_equal(lab, prev):
            break
    ids, counts = np.unique(lab[lab > 0], return_counts=True)
    keep_ids = ids[counts >= min_frac * m.size]
    kept = np.isin(lab, keep_ids) & m
    big = np.asarray(Image.fromarray((kept * 255).astype(np.uint8))
                     .resize((W, H), Image.BILINEAR), dtype=np.float32) > 127
    return (mask > 0.5) & big


def build_mass(gray, mass_scale, ss, out_w, out_h, floor=0.0, plan_solid=None, light=None):
    """The anchor layer: the image's LARGE bright forms -> ordered dither.

    Returns (mass_plane float HxW in [0,1] = dithered white dots at render
    scale, mass_mask float HxW in [0,1] = where the masses are).

    The MASK comes from a strongly simplified copy of the image, so only
    forms spanning many pixels qualify — a shelf, a desk, a column of light.
    The dither TONE comes from the fine image, so the small structure inside
    a mass (individual books, panes, ribs) stays legible as light/dark
    dither, exactly how The Wanderer's ground band carries its grasses.
    A morphological opening removes slivers; if the surviving area exceeds
    ~35% of the canvas the brightness bar rises: the void must dominate.
    """
    H, W = gray.shape
    g_big = simplified(gray, 9.0 * ss)

    if plan_solid is not None:
        # the plan IS the decision: solid wherever the plan says so and the
        # image has any structure to dither there at all
        cand = plan_solid > 0.35          # the plan alone decides the geometry
        mask_im = Image.fromarray((cand * 255).astype(np.uint8))
        r = max(3, int(round(2.0 * ss)) | 1)
        mask_im = mask_im.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
        mask = np.asarray(mask_im, dtype=np.float32) / 255.0
    else:
        thr = max(0.05, max(0.30, floor * 0.8) / max(0.05, mass_scale))
        for _ in range(10):
            cand = g_big > thr
            if cand.mean() <= 0.35:
                break
            thr += 0.05
        mask_im = Image.fromarray((cand * 255).astype(np.uint8))
        r = max(3, int(round(3.0 * ss)) | 1)          # odd kernel, ~3 output px
        mask_im = mask_im.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
        mask = np.asarray(mask_im, dtype=np.float32) / 255.0
        mask = drop_small_components(mask).astype(np.float32)

    # dither on the OUTPUT grid so the dot lattice survives downscaling;
    # tone = fine image, mildly contrast-stretched inside the mass
    g_out = np.asarray(Image.fromarray((gray * 255).astype(np.uint8))
                       .resize((out_w, out_h), Image.LANCZOS), dtype=np.float32) / 255.0
    m_out = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                       .resize((out_w, out_h), Image.BILINEAR), dtype=np.float32) / 255.0
    ty = np.tile(BAYER8, (out_h // 8 + 1, out_w // 8 + 1))[:out_h, :out_w]
    if plan_solid is not None:
        # planned solids must stay CONTINUOUS even where the image falls into
        # deep shadow: lift the tone curve AND give it a floor, so dark stone
        # still carries sparse dots — the form never breaks, the shading stays
        # relative (lit faces dense, shadowed faces a thin veil)
        tone = np.clip((g_out ** 0.60) * 1.30, 0.0, 0.92)
        tone = np.maximum(tone, 0.16)
    else:
        tone = np.clip((g_out ** 0.85) * 0.92, 0.0, 0.92)
    if light is not None:
        # sculptural chiaroscuro: the designed light source (the burst) shades
        # the solids — surfaces facing it brighten, extremities fall into
        # shadow. This is what makes a dithered mass read as a BODY, not a
        # flat cut-out. Purely derived from the plan's light position.
        lx, ly, sk = light
        oyy, oxx = np.mgrid[0:out_h, 0:out_w].astype(np.float32)
        d = np.sqrt(((oxx - lx * out_w) / out_w) ** 2 * 2.4
                    + ((oyy - ly * out_h) / out_h) ** 2 * 1.1)
        shade = 0.35 + 0.65 * np.clip(1.30 - 1.15 * d, 0.0, 1.0)
        shade = (1.0 - sk) + sk * shade               # --shade scales the effect
        tone = np.clip(tone * shade * (1.0 + 0.25 * sk), 0.0, 0.92)
    dots = ((tone > ty) & (m_out > 0.5)).astype(np.float32)
    dots_render = np.asarray(Image.fromarray((dots * 255).astype(np.uint8))
                             .resize((W, H), Image.NEAREST), dtype=np.float32) / 255.0
    return dots_render, mask


def find_bursts(gray, n_req, W, H):
    """Top-K local maxima of the smoothed image, minimum-separation greedy.

    n_req == -1 -> auto: keep peaks while they stay within 55% of the first
    peak's brightness, up to three. Returns list of (x, y, strength)."""
    g = smooth(gray.copy(), 5)
    gg = g.copy()
    peaks = []
    kmax = 3 if n_req < 0 else n_req
    sep = 0.28 * min(W, H)
    yy, xx = np.mgrid[0:H, 0:W]
    first = None
    while len(peaks) < kmax:
        i = int(np.argmax(gg))
        v = float(gg.flat[i])
        y, x = divmod(i, W)
        if first is None:
            first = v
            if v < 0.30:
                break
        elif n_req < 0 and (v < 0.55 * first or v < 0.30):
            break
        peaks.append((float(x), float(y), v))
        gg[np.hypot(xx - x, yy - y) < sep] = 0.0
        if not np.any(gg > 0):
            break
    return peaks


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--preset", default="wanderer", choices=list(PRESETS),
                    help="frozen parameter set; 'wanderer' is the canon (two-layer, moving rain)")
    ap.add_argument("--palette", default="ash", choices=list(PALETTES),
                    help="'ash' (white on black) is the canon")
    ap.add_argument("--size", type=int, default=1400, help="output width in px")
    ap.add_argument("--supersample", type=int, default=None,
                    help="render N x larger, downscale with Lanczos; 2-3 = clean at any display size")
    ap.add_argument("--thickness", type=float, default=None, help="mark weight in render pixels")
    ap.add_argument("--density", type=float, default=None, help="how many dust strokes overall")
    ap.add_argument("--stroke", type=int, default=None, help="max stroke length in px")
    ap.add_argument("--jitter", type=float, default=None, help="how crooked each stroke is")
    ap.add_argument("--curve", type=float, default=None,
                    help="how much each mark bends with the field; 0 = straight, 1 = swirls")
    ap.add_argument("--coherence", type=float, default=None,
                    help="how large the forms strokes follow are; 1 = every speck, 6 = only big shapes")
    ap.add_argument("--sparsity", type=float, default=None, help="higher = emptier void")
    ap.add_argument("--mass", type=float, default=None,
                    help="anchor layer amount: 0 = off (v3 look), 1 = canon, >1 = lower brightness bar")
    ap.add_argument("--floor", type=float, default=None,
                    help="luminance floor: everything below it becomes true void (no dust). "
                         "This MANUFACTURES the black that the reference works design in — "
                         "an evenly lit source has no void of its own. 0 = keep everything")
    ap.add_argument("--bursts", type=int, default=None,
                    help="focal star bursts: -1 = auto (1-3 from image brightness peaks), 0 = none, N = exactly N")
    ap.add_argument("--plan", default=None,
                    help="art-direction mask PNG (any size, resized to fit): R = solid/mass weight, "
                         "G = dust density multiplier, B = rain zone. Where all three are 0 the canvas "
                         "is void (stars only). The plan OVERRIDES statistical segmentation — it is the "
                         "composition decision, made by a human or by Claude looking at the image")
    ap.add_argument("--burst-at", action="append", default=None, metavar="X,Y[,S]",
                    help="place a burst at relative coords (0-1), e.g. 0.4,0.05,1.0; repeatable; "
                         "overrides automatic peak finding")
    ap.add_argument("--texture", choices=["calm", "fine"], default="calm",
                    help="dust sampling texture. calm = from a simplified copy (clean, big-form); "
                         "fine = from the full-detail image (v3 energy: every page, spark and "
                         "crack seeds dust — the fragmentation the style lives on). With a --plan "
                         "the plan controls WHERE, so fine texture is usually safe and stronger")
    ap.add_argument("--shade", type=float, default=1.0,
                    help="strength of synthetic chiaroscuro on the solids (0-1). Use ~0.3 when the "
                         "input is already dramatically lit (e.g. a relit intermediate) so the "
                         "baked-in shadows are not darkened twice")
    ap.add_argument("--rain", type=float, default=None,
                    help="moving streak dashes near the bursts; rain ALWAYS moves along its own direction")
    ap.add_argument("--rain-angle", type=float, default=-14.0,
                    help="direction of the rain dashes in degrees")
    ap.add_argument("--rain-speed", type=float, default=1.0,
                    help="how many full flight-tracks each dash travels per loop "
                         "(integer values keep the loop seamless). Dashes REALLY fly across "
                         "the canvas — measured from the reference works")
    ap.add_argument("--boil", type=float, default=None,
                    help="per-frame positional re-jitter of dust marks, in px. The reference "
                         "works redraw ~70% of their marks every few frames — this 'boiling' "
                         "is where the temporal energy comes from. 0 = smooth advection only")
    ap.add_argument("--stars", type=float, default=None, help="isolated static dots in the void")
    ap.add_argument("--flow", type=float, default=1.0, help="dust travel distance over one loop")
    ap.add_argument("--flow-bias", type=float, default=None, metavar="DEG",
                    help="give the orientation field a SENSE: particles start travelling in the "
                         "hemisphere of this angle (deg, y down). Omit = bidirectional along the lines.")
    ap.add_argument("--flow-from-burst", action="store_true",
                    help="particles stream radially AWAY from the first burst (light drives the dust)")
    ap.add_argument("--flow-region", action="append", default=None,
                    metavar="X,Y,RX,RY,ANGLE[,S]",
                    help="REGIONAL flow direction. Inside this soft ellipse the dust travels in "
                         "the ANGLE hemisphere (deg, y down: 90 = falls, -90 = rises, 0 = right). "
                         "Repeatable, and it OVERRIDES --flow-bias where it applies. The field's "
                         "geometry is untouched — only which way along it a particle sets off. "
                         "Use one region per thing the picture depicts: a light shaft falls, embers "
                         "rise, surf runs with the break. A single global angle is always wrong "
                         "somewhere.")
    ap.add_argument("--swirl", action="append", default=None, metavar="X,Y[,S[,R]]",
                    help="bend a REGION into a vortex: centre at relative coords (0-1), signed "
                         "strength S (negative = the other way round, default 1.0) and radius R as "
                         "a fraction of the canvas (default 0.35). Repeatable. The structure field "
                         "keeps the fine detail, the vortex supplies the collective sense of turn, "
                         "so a whole block rotates together instead of each mark going its own way.")
    ap.add_argument("--length-mix", type=float, default=1.0, metavar="P",
                    help="mark-length distribution. 1 = uniform (every length equally common); "
                         "3-5 = mostly specks with a minority of long streaks. Short marks carry "
                         "the IMAGE, long ones carry the MOTION — the reference mixes both.")
    ap.add_argument("--aniso-len", type=float, default=0.0, metavar="G",
                    help="let the image decide length: where the local structure is strongly "
                         "directional the mark may run long, where it is isotropic detail it stays "
                         "a speck. 0 = off, 1-2 = on.")
    ap.add_argument("--fray", type=float, default=0.0, metavar="PX",
                    help="THE DIRT. A mark is not one clean line: it is a chain of sub-segments of "
                         "random length, each nudged sideways off the ideal path. This is the "
                         "mis-registration / data-error feel. 0 = clean vector line, 1-2 = frayed.")
    ap.add_argument("--gap", type=float, default=0.0,
                    help="chance a sub-segment is dropped entirely, so the line breaks up")
    ap.add_argument("--trail", type=float, default=1.0,
                    help="0 = mark lies on the raw field (old look); 1 = mark trails behind the "
                         "particle along its actual heading, so it reads as a moving streak")
    ap.add_argument("--motion", choices=["flow", "shimmer"], default="flow",
                    help="dust motion: flow = travels along the forms; shimmer = fixed positions, "
                         "brightness breathes. Mass never moves; rain and bursts always do.")
    ap.add_argument("--gamma", type=float, default=None, help="brightness->density curve for dust")
    ap.add_argument("--contrast", type=float, default=1.0,
                    help="push tones apart before drawing; 2-3 rescues flat or busy sources")
    ap.add_argument("--simplify", type=float, default=1.0,
                    help="blur away detail smaller than this factor before drawing")
    ap.add_argument("--edge", type=float, default=None,
                    help="how strongly dust hugs light/dark boundaries — this draws the outlines")
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--static-only", action="store_true")
    ap.add_argument("--mp4", action="store_true",
                    help="also write a looping .mp4 — far smaller than the GIF at the same size")
    ap.add_argument("--declump", type=int, default=0, metavar="N",
                    help="cap how many marks may occupy one cell after advection. The flow field "
                         "has attracting curves and particles funnel onto them; those curves belong "
                         "to the FIELD's topology, not to anything in the picture, so the bright "
                         "lines they make outline nothing. N (6-14) suppresses the surplus and the "
                         "meaningless contours disappear. 0 = off.")
    ap.add_argument("--contour", type=float, default=0.0, metavar="S",
                    help="a DELIBERATE hard-line layer, drawn on the image's own contours: strong "
                         "gradient ridges that are also directionally coherent (a real boundary, "
                         "not texture), thinned to one pixel and drawn as static marks lying along "
                         "the edge. This is the hard line that actually outlines the object. "
                         "0.5-1.5 typical.")
    ap.add_argument("--contour-pct", type=float, default=1.2, metavar="P",
                    help="what fraction of the canvas the contour layer may occupy, in percent")
    ap.add_argument("--conserve", type=float, default=0.0, metavar="S",
                    help="density conservation: advection funnels particles onto the field's "
                         "attracting curves, which show up as meaningless bright squiggles. Each "
                         "frame, compare the particles' CURRENT local density with their HOME "
                         "density and attenuate brightness by (home/now)**S — the compression is "
                         "cancelled exactly, the squiggles vanish, everything else is untouched. "
                         "1.0 = full compensation.")
    ap.add_argument("--ink", type=float, default=0.0, metavar="K",
                    help="ink depletion: a coverage grid absorbs every stamped mark, and further "
                         "marks landing on an already-soaked cell are attenuated by 1/(1+K*cov). "
                         "Unlike --declump (which caps stroke HEADS per cell and misses the 20px "
                         "BODIES piling on an attractor), this bounds the line itself: dense ridges "
                         "stay dense but can no longer blow out into solid white veins. 1-3 typical.")
    ap.add_argument("--soften", type=float, default=0.0, metavar="K",
                    help="soft-compress the accumulation instead of hard-clipping it. Advection "
                         "funnels particles onto the flow field's attracting curves; every mark "
                         "that lands there is SUMMED, so those curves blow out into hard bright "
                         "lines. K compresses the pile-up (0.6-1.2 typical) so a dense ridge stays "
                         "dense but stops saturating. 0 = old hard clip.")
    ap.add_argument("--seed", type=int, default=305)
    args = ap.parse_args()
    for key, value in PRESETS[args.preset].items():
        if getattr(args, key, None) is None:
            setattr(args, key, value)

    rng = np.random.default_rng(args.seed)
    src = Image.open(args.input)
    ss = max(1, int(args.supersample))
    out_w = args.size
    W = args.size * ss
    H = max(64, round(src.height / src.width * W))
    out_h = max(1, round(H / ss))
    gray = np.asarray(src.convert("L").resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0
    if args.invert:
        gray = 1.0 - gray
    if args.simplify > 1.0:
        k = args.simplify
        sw, sh = max(8, int(W / k)), max(8, int(H / k))
        gray = np.asarray(
            Image.fromarray((gray * 255).astype(np.uint8)).resize((sw, sh), Image.LANCZOS)
            .resize((W, H), Image.BICUBIC), dtype=np.float32) / 255.0
    lo, hi = np.percentile(gray, 2), np.percentile(gray, 99.5)
    gray = np.clip((gray - lo) / max(1e-6, hi - lo), 0, 1)
    if args.contrast != 1.0:
        c = max(0.1, args.contrast)
        gray = np.clip(0.5 + np.tanh((gray - 0.5) * 2.0 * c) / (2.0 * np.tanh(c)), 0, 1)

    fx, fy, aniso = flow_field(gray, args.coherence)
    if args.swirl:
        # A vortex is a SIGNED field; the structure tensor is an unsigned line
        # field. Flip the lines into the vortex's hemisphere FIRST, then blend —
        # otherwise half the region turns one way and half the other and the
        # rotation cancels out into mush.
        _yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
        SW_TX = np.zeros((H, W), dtype=np.float32)
        SW_TY = np.zeros((H, W), dtype=np.float32)
        SW_W = np.zeros((H, W), dtype=np.float32)
        for _spec in args.swirl:
            _p = [float(v) for v in _spec.split(",")]
            _cx, _cy = _p[0] * W, _p[1] * H
            _st = _p[2] if len(_p) > 2 else 1.0
            _rad = (_p[3] if len(_p) > 3 else 0.35) * max(W, H)
            _dx, _dy = _xx - _cx, _yy - _cy
            _r = np.hypot(_dx, _dy) + 1e-6
            _tx, _ty = _dy / _r, -_dx / _r                    # tangential
            if _st < 0:
                _tx, _ty = -_tx, -_ty
            _w = min(abs(_st), 1.0) * np.exp(-(_r / _rad) ** 2)
            _sg = np.where(fx * _tx + fy * _ty < 0, -1.0, 1.0).astype(np.float32)
            fx = fx * _sg * (1.0 - _w) + _tx * _w
            fy = fy * _sg * (1.0 - _w) + _ty * _w
            _n = np.hypot(fx, fy) + 1e-6
            fx, fy = (fx / _n).astype(np.float32), (fy / _n).astype(np.float32)
            _take = _w > SW_W
            SW_TX = np.where(_take, _tx, SW_TX).astype(np.float32)
            SW_TY = np.where(_take, _ty, SW_TY).astype(np.float32)
            SW_W = np.maximum(SW_W, _w).astype(np.float32)
    else:
        SW_TX = SW_TY = SW_W = None
    # ---- layer 0: CONTOUR — the only hard lines that are allowed to exist ----
    CT_X = CT_Y = CT_W = None
    if args.contour > 0:
        _gs = smooth(gray.copy(), max(1, int(1.5 * ss)))
        _gy, _gx = np.gradient(_gs)
        _mag = np.hypot(_gx, _gy)
        # RELATIVE contrast, not absolute: an edge in a dark area must be able to
        # compete with one in a bright area, or the whole contour layer collapses
        # onto whatever part of the picture happens to be brightest
        _loc = smooth(gray.copy(), max(2, int(6 * ss))) + 0.02
        _mag = _mag / _loc
        # a real boundary is strong AND directionally coherent; texture is strong
        # but isotropic, so the anisotropy gate is what keeps noise out
        _mag = _mag * np.clip(aniso, 0, 1) ** 1.2
        _mag = np.minimum(_mag, np.percentile(_mag, 99.9))
        _mx = np.asarray(Image.fromarray((_mag / (_mag.max() + 1e-9) * 255).astype(np.uint8))
                         .filter(ImageFilter.MaxFilter(3)), dtype=np.float32) / 255.0
        _mn = _mag / (_mag.max() + 1e-9)
        _ridge = _mn >= _mx - 1e-6                       # thin to the crest of the ridge
        _thr = np.percentile(_mn, 100.0 - args.contour_pct)
        _sel = _ridge & (_mn > _thr) & (gray > (args.floor or 0.0) * 0.5)
        _cy, _cx = np.nonzero(_sel)
        if _cy.size:
            _cap = int(W * H * 0.004)
            if _cy.size > _cap:
                _p = rng.permutation(_cy.size)[:_cap]
                _cy, _cx = _cy[_p], _cx[_p]
            CT_X = _cx.astype(np.float32) + rng.random(_cx.size).astype(np.float32) * 0.6
            CT_Y = _cy.astype(np.float32) + rng.random(_cy.size).astype(np.float32) * 0.6
            CT_W = (args.contour * (0.45 + 0.55 * _mn[_cy, _cx])).astype(np.float32)
            print("contour layer: %d marks on %.2f%% of the canvas"
                  % (CT_X.size, 100.0 * CT_X.size / (W * H)), file=sys.stderr)

    hues = [hex_rgb(c) for c in PALETTES[args.palette]]
    n_hues = len(hues)
    hot = n_hues - 1                                  # brightest hue index

    # ---- art-direction plan (optional) ----
    plan_solid = plan_dust = plan_rain = None
    if args.plan:
        pl = Image.open(args.plan).convert("RGB").resize((W, H), Image.BILINEAR)
        pa = np.asarray(pl, dtype=np.float32) / 255.0
        plan_solid, plan_dust, plan_rain = pa[:, :, 0], pa[:, :, 1], pa[:, :, 2]

    # ---- layer 1: MASS (static anchor) ----
    light = None
    if args.burst_at and args.shade > 0:
        p0 = [float(v) for v in args.burst_at[0].split(",")]
        light = (p0[0], p0[1], min(1.0, args.shade))
    if args.mass > 0 or plan_solid is not None:
        mass_plane, mass_mask = build_mass(gray, max(args.mass, 0.01), ss, out_w, out_h,
                                           args.floor if args.floor is not None else 0.0,
                                           plan_solid=plan_solid, light=light)
    else:
        mass_plane = np.zeros((H, W), dtype=np.float32)
        mass_mask = np.zeros((H, W), dtype=np.float32)

    # ---- layer 3 geometry: BURSTS ----
    if args.burst_at:
        bursts = []
        for spec in args.burst_at:
            parts = [float(v) for v in spec.split(",")]
            bx_, by_ = parts[0] * W, parts[1] * H
            bs_ = parts[2] if len(parts) > 2 else 1.0
            bursts.append((bx_, by_, bs_))
    else:
        bursts = find_bursts(gray, args.bursts, W, H) if args.bursts != 0 else []
    b_dot_x = b_dot_y = None
    if bursts:
        bx = np.array([b[0] for b in bursts], dtype=np.float32)
        by = np.array([b[1] for b in bursts], dtype=np.float32)
        bs = np.array([b[2] for b in bursts], dtype=np.float32)
        b_R = (0.10 + 0.07 * bs) * min(W, H)
        ray_angle, ray_len, ray_phase, ray_cx, ray_cy, ray_w = [], [], [], [], [], []
        core_x, core_y = [], []
        for j in range(len(bursts)):
            n_rays = int(90 + 50 * bs[j])
            a = rng.random(n_rays).astype(np.float32) * 2 * np.pi
            L = b_R[j] * (0.25 + rng.rayleigh(0.45, n_rays).astype(np.float32))
            ray_angle.append(a)
            ray_len.append(L)
            ray_phase.append(rng.random(n_rays).astype(np.float32))
            ray_cx.append(np.full(n_rays, bx[j], np.float32))
            ray_cy.append(np.full(n_rays, by[j], np.float32))
            ray_w.append(np.full(n_rays, 0.55 + 0.45 * bs[j], np.float32))
            n_core = int(60 * bs[j] * ss)
            rr = rng.rayleigh(b_R[j] * 0.05, n_core).astype(np.float32)
            aa = rng.random(n_core).astype(np.float32) * 2 * np.pi
            core_x.append(bx[j] + rr * np.cos(aa))
            core_y.append(by[j] + rr * np.sin(aa))
        ray_angle = np.concatenate(ray_angle); ray_len = np.concatenate(ray_len)
        ray_phase = np.concatenate(ray_phase); ray_cx = np.concatenate(ray_cx)
        ray_cy = np.concatenate(ray_cy); ray_w = np.concatenate(ray_w)
        core_x = np.concatenate(core_x); core_y = np.concatenate(core_y)
        ray_ux, ray_uy = np.cos(ray_angle), np.sin(ray_angle)
        dot_pitch = 3.0 * ss                          # px between dots on a ray
        n_dots = int(np.ceil(ray_len.max() / dot_pitch))

    # ---- layer 2: DUST (stroke tracer, suppressed inside masses) ----
    # Both weight components come from a SIMPLIFIED copy of the image when the
    # mass layer is on: fine texture (books, foliage, brick) must not seed
    # dust, or the picture turns into fur — that is the mass layer's job now.
    # Dust hugs the boundaries of the big forms and the bright energy zones.
    g_w = simplified(gray, 4.0 * ss) if (args.mass > 0 and args.texture == "calm") else gray
    gy_, gx_ = np.gradient(smooth(g_w.copy(), 2))
    emag = np.hypot(gx_, gy_)
    emag = emag / (np.percentile(emag, 99) + 1e-6)
    emag = np.clip(emag, 0, 1)
    floor = args.floor if args.floor is not None else 0.0
    if floor > 0:
        # THE VOID IS MANUFACTURED. The reference works design their emptiness;
        # an evenly lit source has none, so everything below the floor is cut
        # to true black and the tonal range above it is restretched. Dust and
        # its edges exist only above the floor.
        lift = np.clip((g_w - floor) / max(1e-6, 1.0 - floor), 0, 1)
        weight = lift ** args.gamma + args.edge * (emag ** 0.7) * (lift > 0)
    else:
        weight = g_w ** args.gamma + args.edge * emag ** 0.7
    weight *= (1.0 - 0.85 * mass_mask)                # masses are already drawn
    if plan_dust is not None:
        weight *= plan_dust                           # the plan decides where dust lives
    weight = np.maximum(weight - 0.02 * args.sparsity, 0.0)
    if weight.sum() <= 0:
        print("image has no bright structure — try --invert", file=sys.stderr)
        return 1
    n_particles = max(500, int(W * H * 0.020 * args.density / (ss * ss)))
    probs = (weight / weight.sum()).ravel()
    idx = rng.choice(probs.size, size=n_particles, p=probs)
    home_y, home_x = np.divmod(idx, W)
    home_x = home_x.astype(np.float32) + rng.random(n_particles).astype(np.float32)
    home_y = home_y.astype(np.float32) + rng.random(n_particles).astype(np.float32)

    p_hue = rng.integers(0, n_hues, n_particles)
    b_home = sample(gray, home_x, home_y)
    p_hue = np.where(rng.random(n_particles) < b_home * 0.7, 0, p_hue)
    _short = max(2, 2 * ss)
    _u = rng.random(n_particles).astype(np.float32)
    if args.aniso_len > 0:
        _a = np.clip(sample(aniso, home_x, home_y), 0, 1) ** args.aniso_len
    else:
        _a = np.float32(1.0)
    _hi = _short + (args.stroke * ss - _short) * _a
    p_len = np.maximum(_short, (_short + (_hi - _short) * _u ** args.length_mix)).astype(np.int64)
    p_dash = rng.random(n_particles) < 0.28
    p_bright = 0.45 + 0.55 * rng.random(n_particles).astype(np.float32)
    p_drift = (rng.random(n_particles).astype(np.float32) - 0.5) * args.jitter

    frames = 1 if args.static_only else max(2, int(args.seconds * args.fps))
    life = frames
    for cand in (frames // 4, frames // 3, frames // 2):
        if cand >= 4 and frames % cand == 0:
            life = cand
            break
    p_offset = rng.integers(0, life, n_particles)
    travel = args.flow * 10.0 * ss / max(1, life)
    # BOIL: the reference redraws most marks every few frames — persistence
    # measured at only 25-28%. Each particle gets a per-frame positional
    # re-jitter, a fixed table over one life so the loop stays seamless.
    boil_amp = (args.boil or 0.0) * ss
    jit = (rng.standard_normal((life, n_particles, 2)).astype(np.float32) * boil_amp
           ) if (boil_amp > 0 and frames > 1) else None

    # ---- layer 4: RAIN (moving dashes, focal zones only) ----
    dark = np.clip(1.0 - simplified(gray, 4.0 * ss) * 2.2, 0, 1)
    n_rain = max(0, int(W * H * 0.00013 * args.rain / (ss * ss)))
    if plan_rain is not None and plan_rain.sum() > 1.0:
        # the plan paints the rain zone directly; no darkness gating —
        # painted rain over a bright shaft is a legitimate decision
        rp = (plan_rain * (1.0 - 0.8 * mass_mask)).ravel()
        ridx = rng.choice(rp.size, size=n_rain, p=rp / rp.sum())
        ry, rx = np.divmod(ridx, W)
        rx = rx.astype(np.float32) + rng.random(n_rain).astype(np.float32)
        ry = ry.astype(np.float32) + rng.random(n_rain).astype(np.float32)
    else:
        if bursts:
            pick = rng.integers(0, len(bursts), n_rain)
            sigma = b_R[pick] * 1.7
            rx = (bx[pick] + rng.standard_normal(n_rain).astype(np.float32) * sigma)
            ry = (by[pick] + rng.standard_normal(n_rain).astype(np.float32) * sigma * 0.55)
        else:
            rx = rng.random(n_rain).astype(np.float32) * W
            ry = rng.random(n_rain).astype(np.float32) * H
        inside = (rx >= 0) & (rx < W) & (ry >= 0) & (ry < H)
        rx, ry = rx[inside], ry[inside]
        keep = rng.random(rx.size) < sample(dark, rx, ry) * sample(1.0 - mass_mask, rx, ry)
        rx, ry = rx[keep], ry[keep]
    # Each dash owns a long flight TRACK through its home point and really
    # travels along it — measured from the reference: streak segments move
    # 2-3px per frame ACROSS the canvas, they do not crawl inside a window.
    r_len = rng.integers(10 * ss, 34 * ss, rx.size)          # dash length
    r_span = (rng.integers(110, 260, rx.size) * ss).astype(np.float32)  # track length
    r_phase = rng.random(rx.size).astype(np.float32)
    r_hue = rng.integers(0, n_hues, rx.size)
    rdx = np.float32(np.cos(np.deg2rad(args.rain_angle)))
    rdy = np.float32(np.sin(np.deg2rad(args.rain_angle)))
    rain_zone = plan_rain if plan_rain is not None else dark

    # ---- layer 5: STARS ----
    n_star = max(0, int(W * H * 0.00010 * args.stars))
    sx0 = rng.random(n_star).astype(np.float32) * W
    sy0 = rng.random(n_star).astype(np.float32) * H
    if plan_solid is not None:
        # stars live only in the DESIGNED void
        voidness = np.clip(1.0 - plan_solid - plan_dust - plan_rain, 0, 1)
        keep = rng.random(n_star) < sample(voidness, sx0, sy0) * 0.9
    else:
        keep = rng.random(n_star) < sample(dark, sx0, sy0) * 0.8
    sx0, sy0 = sx0[keep], sy0[keep]
    s_hue = rng.integers(0, n_hues, sx0.size)

    # home-density grid for --conserve (constant across frames)
    CSV_CS = max(3, 3 * ss)
    if args.conserve > 0:
        _gh = int(H // CSV_CS) + 2; _gw = int(W // CSV_CS) + 2
        CSV_HOME = np.zeros((_gh, _gw), dtype=np.float32)
        np.add.at(CSV_HOME, (np.clip(home_y // CSV_CS, 0, _gh - 1).astype(np.int64),
                             np.clip(home_x // CSV_CS, 0, _gw - 1).astype(np.int64)), 1.0)
        CSV_HOME = smooth(CSV_HOME, 1)
    else:
        CSV_HOME = None

    # seed direction for heading coherence
    if args.flow_from_burst and bursts:
        seed_bx = (home_x - bursts[0][0]).astype(np.float32)
        seed_by = (home_y - bursts[0][1]).astype(np.float32)
        nn = np.hypot(seed_bx, seed_by) + 1e-6
        seed_bx, seed_by = seed_bx / nn, seed_by / nn
    elif args.flow_bias is not None:
        seed_bx = np.full(n_particles, np.cos(np.deg2rad(args.flow_bias)), dtype=np.float32)
        seed_by = np.full(n_particles, np.sin(np.deg2rad(args.flow_bias)), dtype=np.float32)
    else:
        seed_bx = np.zeros(n_particles, dtype=np.float32)   # keep the field's own sign
        seed_by = np.zeros(n_particles, dtype=np.float32)
    if args.flow_region:
        # PHYSICS PER REGION. Each entry says what that part of the picture is
        # doing; the strongest claim on a particle wins.
        _best = np.zeros(n_particles, dtype=np.float32)
        for _spec in args.flow_region:
            _p = [float(v) for v in _spec.split(",")]
            _cx, _cy, _rx, _ry, _ang = _p[0] * W, _p[1] * H, _p[2] * W, _p[3] * H, _p[4]
            _st = _p[5] if len(_p) > 5 else 1.0
            _d = np.sqrt(((home_x - _cx) / max(_rx, 1e-6)) ** 2 +
                         ((home_y - _cy) / max(_ry, 1e-6)) ** 2)
            _w = (min(abs(_st), 1.0) * np.exp(-_d ** 2)).astype(np.float32)
            _take = _w > _best
            seed_bx = np.where(_take, np.cos(np.deg2rad(_ang)), seed_bx).astype(np.float32)
            seed_by = np.where(_take, np.sin(np.deg2rad(_ang)), seed_by).astype(np.float32)
            _best = np.maximum(_best, _w)

    if SW_W is not None:
        # inside a vortex the SWIRL decides which way round a particle sets off,
        # not the global bias — otherwise half the eddy runs backwards and the
        # rotation reads as chaos instead of a turn
        _ws = sample(SW_W, home_x, home_y)
        seed_bx = seed_bx * (1 - _ws) + sample(SW_TX, home_x, home_y) * _ws
        seed_by = seed_by * (1 - _ws) + sample(SW_TY, home_x, home_y) * _ws

    # ---- FRAY: break every mark into sub-segments that sit slightly off the line
    _maxk = int(p_len.max()) + 1
    if args.fray > 0 or args.gap > 0:
        p_seg = rng.integers(max(1, ss), max(2, 3 * ss) + 1, n_particles)      # sub-segment length
        _nseg = int(_maxk // max(1, p_seg.min())) + 2
        _to = rng.random((_nseg, n_particles)).astype(np.float32) * 2.0 - 1.0  # sideways
        _tg = rng.random((_nseg, n_particles)).astype(np.float32)              # dropout
        _tb = rng.random((_nseg, n_particles)).astype(np.float32)              # brightness
        _sid = (np.arange(_maxk)[:, None] // p_seg[None, :]) % _nseg
        _cols = np.arange(n_particles)
        FRAY_O = _to[_sid, _cols] * (args.fray * ss)
        FRAY_G = _tg[_sid, _cols] >= args.gap
        FRAY_B = 0.55 + 0.75 * _tb[_sid, _cols]
    else:
        FRAY_O = FRAY_G = FRAY_B = None

    thick = max(1, int(round(args.thickness * ss)))
    out = args.out or (args.input.rsplit(".", 1)[0] + "-dirty")
    images = []

    for t in range(frames):
        canvas = np.zeros((n_hues, H, W), dtype=np.float32)
        tt = t / frames if frames > 1 else 0.0

        # -- dust --
        _ink_cs = max(2, 2 * ss)
        _ink = (np.zeros((H // _ink_cs + 2, W // _ink_cs + 2), dtype=np.float32)
                if args.ink > 0 else None)
        age = (t + p_offset) % life
        if frames == 1:
            alpha = np.ones(n_particles, dtype=np.float32)
        elif args.motion == "shimmer":
            ph = p_offset / max(1, life)
            alpha = (0.55 + 0.45 * np.sin(2.0 * np.pi * (tt + ph))).astype(np.float32)
        else:
            alpha = np.clip(np.sin(np.pi * (age / life)) * 2.4, 0, 1).astype(np.float32)

        x, y = home_x.copy(), home_y.copy()
        # HEADING COHERENCE. The structure tensor gives an ORIENTATION (mod 180),
        # so its sign flips arbitrarily across the image; advecting it naively lets
        # a particle reverse and oscillate in place. Each particle instead carries
        # its heading and always steps into the hemisphere it is already going —
        # the line field becomes a set of tracks that are travelled, not vibrated.
        dirx, diry = sample(fx, x, y), sample(fy, x, y)
        s0 = dirx * seed_bx + diry * seed_by
        sgn = np.where(s0 < 0, -1.0, 1.0).astype(np.float32)
        dirx, diry = dirx * sgn, diry * sgn
        steps = 0 if args.motion == "shimmer" else (int(age.max()) if age.size else 0)
        for k in range(steps):
            live = age > k
            if not np.any(live):
                break
            u, v = sample(fx, x, y), sample(fy, x, y)
            sg = np.where(u * dirx + v * diry < 0, -1.0, 1.0).astype(np.float32)
            u, v = u * sg, v * sg
            dirx = np.where(live, u, dirx)
            diry = np.where(live, v, diry)
            x = np.where(live, x + u * travel, x)
            y = np.where(live, y + v * travel, y)

        if jit is not None:
            x = x + jit[t % life, :, 0]
            y = y + jit[t % life, :, 1]

        if args.declump > 0:
            # the attractor pile-up is a property of the FIELD, not of the
            # picture — cap the occupancy so it cannot draw phantom contours.
            # Rank inside a cell is a pure function of position, so the loop
            # stays seamless.
            _cs = max(1, 4 * ss)
            _ncol = int(W // _cs) + 2
            _key = (np.clip(y // _cs, 0, H // _cs + 1).astype(np.int64) * _ncol
                    + np.clip(x // _cs, 0, _ncol - 1).astype(np.int64))
            _ord = np.argsort(_key, kind="stable")
            _sk = _key[_ord]
            _rank = np.arange(_sk.size) - np.searchsorted(_sk, _sk, side="left")
            _keep = np.zeros(_sk.size, dtype=bool)
            _keep[_ord] = _rank < args.declump
            alpha = alpha * _keep

        if CSV_HOME is not None:
            _gh, _gw = CSV_HOME.shape
            _iy = np.clip(y // CSV_CS, 0, _gh - 1).astype(np.int64)
            _ix = np.clip(x // CSV_CS, 0, _gw - 1).astype(np.int64)
            _now = np.zeros_like(CSV_HOME)
            np.add.at(_now, (_iy, _ix), 1.0)
            _ratio = np.clip((CSV_HOME + 0.8) / (_now + 0.8), 0.0, 1.0) ** args.conserve
            alpha = alpha * _ratio[_iy, _ix]

        hx, hy = sample(fx, x, y), sample(fy, x, y)
        if args.trail > 0 and args.motion != "shimmer":
            # lay the mark along where the particle CAME FROM, not along a
            # coin-flip of the field's sign: the stroke becomes its own motion blur
            sg = np.where(hx * dirx + hy * diry < 0, -1.0, 1.0).astype(np.float32)
            tx_, ty_ = -(hx * sg), -(hy * sg)
            hx = hx * (1 - args.trail) + tx_ * args.trail
            hy = hy * (1 - args.trail) + ty_ * args.trail
            nn = np.hypot(hx, hy) + 1e-6
            hx, hy = hx / nn, hy / nn
        for k in range(int(p_len.max())):
            on = (p_len > k) & (~p_dash | (k % 2 == 0))
            if args.curve > 0:
                fu, fv = sample(fx, x, y), sample(fy, x, y)
                hx = hx * (1 - args.curve) + fu * args.curve
                hy = hy * (1 - args.curve) + fv * args.curve
                n = np.hypot(hx, hy) + 1e-6
                hx, hy = hx / n, hy / n
            ang = p_drift * k * 0.35
            c, s = np.cos(ang), np.sin(ang)
            ru, rv = hx * c - hy * s, hx * s + hy * c
            # taper along the mark's OWN length, not a fixed 0.05/step slope
            # (the old slope hard-capped every stroke at 20 render px, so
            #  --stroke above ~7 did nothing and the marks stayed bug-sized)
            fall = np.clip(1.0 - k / np.maximum(p_len.astype(np.float32), 1.0), 0.0, 1.0) ** 0.55
            w = alpha * p_bright * np.where(on, 1.0, 0.0) * fall
            if _ink is not None:
                _iy = np.clip(y / _ink_cs, 0, _ink.shape[0] - 1).astype(np.int32)
                _ix = np.clip(x / _ink_cs, 0, _ink.shape[1] - 1).astype(np.int32)
                w = w / (1.0 + args.ink * _ink[_iy, _ix])
                np.add.at(_ink, (_iy, _ix), w)
            if FRAY_O is not None:
                # stamp OFF the ideal path; the path itself stays clean, so the
                # mark reads as several short pieces that do not quite line up
                w = w * FRAY_B[k] * FRAY_G[k]
                o = FRAY_O[k]
                stamp(canvas, x - rv * o, y + ru * o, p_hue, w.astype(np.float32), thick)
            else:
                stamp(canvas, x, y, p_hue, w.astype(np.float32), thick)
            x = x + ru
            y = y + rv

        # -- contour: static, identical every frame, lying along the edge --
        if CT_X is not None:
            _hx, _hy = sample(fx, CT_X, CT_Y), sample(fy, CT_X, CT_Y)
            _x, _y = CT_X.copy(), CT_Y.copy()
            _hue = np.full(CT_X.size, hot, dtype=np.int64)
            for _k in range(max(2, 2 * ss)):
                _w = CT_W * (1.0 - 0.10 * _k)
                stamp(canvas, _x, _y, _hue, _w.astype(np.float32), thick)
                _x = _x + _hx
                _y = _y + _hy

        # -- bursts: dotted rays streaming outward, seamless wrap --
        if bursts:
            for m in range(n_dots):
                # dots fly outward ~20 pitches per loop — real radial travel,
                # integer pitch count keeps the loop seamless
                r = (m * dot_pitch + (ray_phase + tt * 20.0) * dot_pitch) % (ray_len + dot_pitch)
                fall = np.clip(1.0 - r / (ray_len + 1e-3), 0, 1) ** 0.7
                w = (ray_w * fall).astype(np.float32)
                w[r > ray_len] = 0.0
                stamp(canvas, ray_cx + ray_ux * r, ray_cy + ray_uy * r,
                      np.full(ray_cx.size, hot), w, thick)
            stamp(canvas, core_x, core_y, np.full(core_x.size, hot),
                  np.full(core_x.size, 0.9, dtype=np.float32), thick)

        # -- rain: every dash FLIES along its track, --rain-speed tracks per
        #    loop (integer -> frame N == frame 0). Brightness follows the
        #    rain-zone envelope at the dash's current position, and fades at
        #    the track ends so the wrap never pops --
        if rx.size:
            ph = (r_phase + tt * args.rain_speed) % 1.0
            cx_ = rx + rdx * (ph - 0.5) * r_span
            cy_ = ry + rdy * (ph - 0.5) * r_span
            env = sample(rain_zone, cx_, cy_).astype(np.float32)
            endfade = np.clip(np.minimum(ph, 1.0 - ph) * 7.0, 0, 1).astype(np.float32)
            for k in range(int(r_len.max())):
                w = np.where(r_len > k, 0.85, 0.0).astype(np.float32) * env * endfade
                stamp(canvas, cx_ + rdx * (k - r_len * 0.5), cy_ + rdy * (k - r_len * 0.5),
                      r_hue, w, thick)

        if sx0.size:
            stamp(canvas, sx0, sy0, s_hue, np.full(sx0.size, 0.9, dtype=np.float32), thick)

        # -- compose: additive marks over black, then the static mass layer --
        rgb = np.zeros((H, W, 3), dtype=np.float32)
        for i, hue in enumerate(hues):
            if args.soften > 0:
                # soft knee: a lone mark keeps its exact brightness; only the
                # PILE-UP above the knee is compressed, and it approaches 1.0
                # asymptotically instead of clipping, so an attractor curve
                # reads as dense rather than as a hard white line
                _t, _k = 0.70, args.soften
                _c = np.where(canvas[i] <= _t, canvas[i],
                              _t + (1.0 - _t) * (1.0 - np.exp(-(canvas[i] - _t) / _k)))
                _c = np.clip(_c, 0, 1.0)
            else:
                _c = np.clip(canvas[i], 0, 1.6)
            rgb += _c[:, :, None] * hue[None, None, :]
        if args.mass > 0:
            body = hues[0] * 0.86
            rgb = np.maximum(rgb, mass_plane[:, :, None] * body[None, None, :])
        frame = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
        if ss > 1:
            frame = frame.resize((out_w, out_h), Image.LANCZOS)
        images.append(frame)

    # composition report — the "canon health check"
    g0 = np.asarray(images[0].convert("L"), dtype=np.float32) / 255.0
    void = float((g0 < 0.04).mean())
    print(f"canon check: void={void:.0%} (target >=50%), mass={float(mass_mask.mean()):.0%}, "
          f"bursts={len(bursts)}, rain dashes={rx.size}")

    images[0].save(out + ".png")
    print(f"wrote {out}.png ({images[0].width}x{images[0].height}, {n_particles} strokes, ss={ss})")
    if args.mp4 and not args.static_only:
        import subprocess, tempfile, shutil
        tmp = tempfile.mkdtemp()
        try:
            for i, im in enumerate(images):
                im.save(os.path.join(tmp, f"f{i:04d}.png"))
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(args.fps),
                "-i", os.path.join(tmp, "f%04d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                out + ".mp4",
            ], check=True)
            print(f"wrote {out}.mp4 ({os.path.getsize(out + '.mp4') // 1024} KB)")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    if not args.static_only:
        gw2, gh2 = images[0].width, images[0].height
        small = [im.resize((gw2, gh2), Image.BILINEAR).quantize(colors=32, dither=Image.NONE)
                 for im in images]
        small[0].save(out + ".gif", save_all=True, append_images=small[1:],
                      duration=int(1000 / args.fps), loop=0, optimize=True)
        print(f"wrote {out}.gif ({len(images)} frames, {os.path.getsize(out + '.gif') // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
