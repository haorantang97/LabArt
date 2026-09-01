#!/usr/bin/env python3
"""Two-layer pixel renderer on pure black.

Canon profiles, derived from frame-by-frame measurement of published
particle-animation work (statistics only — no artwork is reproduced):
  * PRIMARY / composition — profile J:
    solid dithered masses anchor the scene and NEVER move; a particle-dust
    figure carries the energy; ONE radial star burst is the focal point;
    streak dashes near the burst travel along their own direction; the sky
    stays almost entirely pure black.
  * SECONDARY / boundary & motion — profile K:
    the figure is a stable dithered mass, ALL motion lives in the dash ring,
    and a wide moat of pure black separates the two.

The one law learned from those measurements: clear boundaries do not come from
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
  python3 tephra.py INPUT [-o OUT]
      [--preset flux|anchor|faithful|poster|curl|detail|web]
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


# Legacy preset spellings still accepted on the command line, so that
# commands written against older versions keep reproducing their output.
_PRESET_ALIASES = {"wanderer": "anchor"}


def _preset_alias(v):
    return _PRESET_ALIASES.get(v, v)


# --------------------------------------------------------------- presets
# A preset freezes every style-defining parameter. Explicit CLI flags win.
# "flux" is the canon preset; the v3/v4 presets are kept so that old
# commands still run, but v4 changed the rain layer everywhere (it moves
# now), so v3 GIFs are not reproduced bit-for-bit.

PRESETS = {
    # THE v5 CANON — pure particle. No mass layer, no bursts by default: strokes
    # travel along the image's own structure, short specks carry the image and
    # long frayed streaks carry the motion. Everything this idiom needs is ON
    # here, because a skill's defaults must BE its canon.
    "flux": dict(supersample=3, thickness=1.0, density=1.5, sparsity=1.8,
                 stroke=20, jitter=0.02, curve=0.03, coherence=35.0,
                 rain=0.4, stars=0.6, gamma=2.4, edge=0.7,
                 mass=0.0, bursts=0, boil=0.35, floor=None,
                 flow=5.0, conserve=1.5, length_mix=3.0, aniso_len=1.5,
                 fray=1.4, gap=0.22),

    # THE CANON — modelled on 样本J + 样本K. Solid masses,
    # sparse dust, one to three bursts, moving rain, >=50% pure black.
    "anchor": dict(supersample=2, thickness=1.0, density=0.85, sparsity=1.9,
                     stroke=3, jitter=0.10, curve=0.08, coherence=3.0,
                     rain=1.0, stars=0.7, gamma=2.2, edge=0.9,
                     mass=1.0, bursts=-1, floor=0.45, boil=1.6,
               flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
    "faithful": dict(supersample=1, thickness=1.0, density=1.0, sparsity=1.3,
                     stroke=8, jitter=0.25, curve=0.15, coherence=3.0,
                     rain=1.0, stars=1.0, gamma=1.6, edge=0.6,
                     mass=0.0, bursts=0, boil=0.0,
               flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
    "poster": dict(supersample=3, thickness=1.0, density=1.7, sparsity=1.2,
                   stroke=10, jitter=0.06, curve=0.10, coherence=3.0,
                   rain=0.3, stars=0.5, gamma=2.2, edge=0.4,
                   mass=0.0, bursts=0, boil=0.0,
             flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
    "curl": dict(supersample=2, thickness=1.0, density=0.85, sparsity=1.6,
                 stroke=11, jitter=0.15, curve=0.6, coherence=2.2,
                 rain=0.4, stars=0.5, gamma=2.5, edge=0.5,
                 mass=0.0, bursts=0, boil=0.0,
           flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
    "detail": dict(supersample=3, thickness=1.0, density=2.0, sparsity=1.6,
                   stroke=5, jitter=0.10, curve=0.08, coherence=3.0,
                   rain=0.6, stars=0.6, gamma=2.8, edge=0.5,
                   mass=0.0, bursts=0, boil=0.0,
             flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
    "web": dict(supersample=2, thickness=1.0, density=1.4, sparsity=1.3,
                stroke=9, jitter=0.10, curve=0.12, coherence=3.0,
                rain=0.5, stars=0.6, gamma=1.9, edge=0.5,
                mass=0.0, bursts=0, boil=0.0,
          flow=1.0, conserve=0.0, length_mix=1.0, aniso_len=0.0, fray=0.0, gap=0.0),
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
    dither, exactly how 样本J's ground band carries its grasses.
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
    ap.add_argument("--preset", default="flux", type=_preset_alias,
                    choices=list(PRESETS),
                    help="frozen parameter set; 'flux' is the canon (pure particle). "
                         "'anchor' and the other legacy presets are kept so old commands still reproduce")
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
    ap.add_argument("--floor", default=None, metavar="X|auto",
                    help="luminance floor: everything below it becomes true void (no dust). "
                         "'auto' (the flux default) reads it off this image's own "
                         "histogram, because the right floor is the one parameter that "
                         "genuinely cannot be shared between pictures. "
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
    ap.add_argument("--rain-life", type=float, default=0.16, metavar="SEC",
                    help="P-4. A dash is a FLASH, not a cruise. Measured on the reference: zero "
                         "residue at the old position between frames, 14.7%% pixel survival, "
                         "tracks never longer than 4 steps -- a dash lives 2-5 frames then the "
                         "whole thing is gone and new ones appear elsewhere. seconds/life should "
                         "be an integer so the loop still closes.")
    ap.add_argument("--rain-px-per-sec", type=float, default=0.6, metavar="F",
                    help="P-3. Travel per second as a fraction of canvas width. Measured median "
                         "1600px/s on a 2560 canvas = 0.62 W/s. The old span-derived speed was "
                         "~12x too slow.")
    ap.add_argument("--rain-speed-len", type=float, default=0.5, metavar="A",
                    help="P-3. Speed scales as (L/L_med)^A -- measured displacement/length "
                         "correlation +0.36, so long dashes really do move faster.")
    ap.add_argument("--rain-spread", type=float, default=25.0, metavar="DEG",
                    help="per-dash angle spread around --rain-angle, in degrees. The reference's "
                         "dashes are near-parallel: 5-10 is right, and CURVING them is wrong -- "
                         "they are ruled straight lines.")
    ap.add_argument("--rain-taper", type=float, default=1.0, metavar="R",
                    help="tail/head size ratio WITHIN one dash. 1.0 is canon: re-measured against "
                         "the reference with a strict collinearity test, block size along a run "
                         "has no gradient at all -- it is constant with noise. (An earlier loose "
                         "chain-finder joined a big blob to a nearby speck run and manufactured a "
                         "comet taper that is not in the source.) Below 1 gives meteor tails.")
    ap.add_argument("--rain-spacing", type=float, default=1.0, metavar="G",
                    help="how much the gap opens from head to tail. 1.0 = even, which is canon.")
    ap.add_argument("--rain-speed-mix", default="1,1,1,1.5,1.5,2", metavar="LIST",
                    help="per-dash speed multipliers, sampled uniformly from this list and scaled "
                         "by --rain-speed. Measured off the reference animation: displacement per "
                         "frame runs 0 to 20px, coefficient of variation 0.60, and speed is "
                         "UNCORRELATED with length -- some dashes barely move while others tear "
                         "across. One shared speed for every dash is what reads as dead. Integers "
                         "keep the loop seamless.")
    ap.add_argument("--rain-short", type=float, default=4.0, metavar="P",
                    help="how hard the length distribution is skewed to short marks. Measured: "
                         "median run is 5px and the 95th percentile is 17px, so most marks are "
                         "specks and long streaks are the rare exception. Higher = shorter.")
    ap.add_argument("--rain-block", type=float, default=1.1, metavar="PX",
                    help="block size in output px. The VARIATION IS BETWEEN DASHES, not inside "
                         "one: each dash picks its own size around this, then holds it.")
    ap.add_argument("--rain-keepout", action="append", default=None, metavar="X,Y,RX,RY[,S]",
                    help="soft ellipse the rain must stay out of (repeatable). Dashes are neither "
                         "seeded inside it nor allowed to fly through it -- they fade out at its "
                         "edge. Use it to keep the void layer off the subject.")
    ap.add_argument("--rain-flow", type=float, default=0.0, metavar="DEG",
                    help="amplitude, in degrees, of a SMOOTH angular field the dashes read their "
                         "direction from. Each dash stays straight; neighbours agree and distant "
                         "ones differ, so the layer flows instead of reading as ruled hatching. "
                         "This is the third option: not per-dash curvature (worms) and not one "
                         "global angle with noise (rigid) -- a field.")
    ap.add_argument("--rain-flow-scale", type=float, default=0.28, metavar="S",
                    help="how large the flow cells are, as a fraction of the canvas")
    ap.add_argument("--rain-wild", type=float, default=1.0, metavar="K",
                    help="how far block size, run length, dot count and angle spread out between "
                         "dashes. 1 = current, 2 = twice the spread in every one of them.")
    ap.add_argument("--rain-jitter", type=float, default=0.35, metavar="J",
                    help="random wobble of block size and gap within a dash (no direction to it)")
    ap.add_argument("--rain-speed", type=float, default=1.0,
                    help="how many full flight-tracks each dash travels per loop "
                         "(integer values keep the loop seamless). Dashes REALLY fly across "
                         "the canvas — measured from the reference works")
    ap.add_argument("--boil", type=float, default=None,
                    help="per-frame positional re-jitter of dust marks, in px. The reference "
                         "works redraw ~70%% of their marks every few frames — this 'boiling' "
                         "is where the temporal energy comes from. 0 = smooth advection only")
    ap.add_argument("--stars", type=float, default=None, help="isolated static dots in the void")
    ap.add_argument("--flow", type=float, default=None, help="dust travel distance over one loop")
    ap.add_argument("--flow-bias", type=float, default=None, metavar="DEG",
                    help="give the orientation field a SENSE: particles start travelling in the "
                         "hemisphere of this angle (deg, y down). Omit = bidirectional along the lines.")
    ap.add_argument("--flow-from-burst", action="store_true",
                    help="particles stream radially AWAY from the first burst (light drives the dust)")
    ap.add_argument("--dissolve", default=None, metavar="DEG,START,SOFT[,BREATH]",
                    help="THE ARTISTIC DECISION. Hold part of the subject as solid dither and let "
                         "the rest disintegrate into particles that escape into the void. DEG = the "
                         "direction the disintegration progresses (deg, y down: -90 = upward decay, "
                         "90 = collapse downward, or aim it outward). START = how far along the "
                         "subject the dissolving begins (0-1). SOFT = width of the transition band. "
                         "BREATH = how much the boundary flickers open and shut over the loop "
                         "(the reference boundary is deliberately unstable, never a clean cut).")
    ap.add_argument("--turbulence", type=float, default=1.0, metavar="T",
                    help="how much the escaping ash curls on its way out. 0 = every mark marches "
                         "along one straight angle (rigid, and the dead giveaway of a machine); "
                         "1-2 = it peels off along the FORM first and then wanders on a "
                         "divergence-free turbulent field, the way ash actually leaves a fire.")
    ap.add_argument("--escape", type=float, default=1.0, metavar="K",
                    help="how far the dissolved particles fly free of the form and fade into the "
                         "black, relative to the flow distance. 0 = they stay on the surface "
                         "(a tonal description of the object); 1-2 = they actually leave it.")
    ap.add_argument("--flow-region", action="append", default=None,
                    metavar="X,Y,RX,RY,ANGLE[,S]",
                    help="REGIONAL flow direction. Inside this soft ellipse the dust travels in "
                         "the ANGLE hemisphere (deg, y down: 90 = falls, -90 = rises, 0 = right). "
                         "Repeatable, and it OVERRIDES --flow-bias where it applies. The field's "
                         "geometry is untouched — only which way along it a particle sets off. "
                         "Use one region per thing the picture depicts: a light shaft falls, embers "
                         "rise, surf runs with the break. A single global angle is always wrong "
                         "somewhere.")
    ap.add_argument("--anchor", action="append", default=None,
                    metavar="X,Y,RX,RY[,S]",
                    help="hold this ellipse SOLID and in the source's own colour: an ordered "
                         "halftone built from the photo itself, frozen (no advection). The "
                         "counterweight the dissolving material needs -- one thing that stays.")
    ap.add_argument("--anchor-src", default=None, metavar="FILE",
                    help="read anchor pixels from THIS image instead of the input. Pairs with a "
                         "relit/graded input: the water gets the new lighting, the held object "
                         "keeps the detail the grade destroyed. Must share the input's framing.")
    ap.add_argument("--swirl", action="append", default=None, metavar="X,Y[,S[,R]]",
                    help="bend a REGION into a vortex: centre at relative coords (0-1), signed "
                         "strength S (negative = the other way round, default 1.0) and radius R as "
                         "a fraction of the canvas (default 0.35). Repeatable. The structure field "
                         "keeps the fine detail, the vortex supplies the collective sense of turn, "
                         "so a whole block rotates together instead of each mark going its own way.")
    ap.add_argument("--length-mix", type=float, default=None, metavar="P",
                    help="mark-length distribution. 1 = uniform (every length equally common); "
                         "3-5 = mostly specks with a minority of long streaks. Short marks carry "
                         "the IMAGE, long ones carry the MOTION — the reference mixes both.")
    ap.add_argument("--aniso-len", type=float, default=None, metavar="G",
                    help="let the image decide length: where the local structure is strongly "
                         "directional the mark may run long, where it is isotropic detail it stays "
                         "a speck. 0 = off, 1-2 = on.")
    ap.add_argument("--fray", type=float, default=None, metavar="PX",
                    help="THE DIRT. A mark is not one clean line: it is a chain of sub-segments of "
                         "random length, each nudged sideways off the ideal path. This is the "
                         "mis-registration / data-error feel. 0 = clean vector line, 1-2 = frayed.")
    ap.add_argument("--gap", type=float, default=None,
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
    ap.add_argument("--conserve", type=float, default=None, metavar="S",
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
    ap.add_argument("--dissolve-life", type=float, default=0.10, metavar="SEC",
                    help="lifetime of a DISSOLVED particle. Measured on the reference: an escaped "
                         "mark survives 2-3 frames (80-120ms) and is then reborn somewhere else. "
                         "The far field is not reached by flying, it is BORN there.")
    ap.add_argument("--dissolve-near", type=float, default=0.08, metavar="F",
                    help="near-field e-folding length of the escape cloud, as a fraction of the "
                         "subject size S (measured 0.05-0.10 across four works).")
    ap.add_argument("--dissolve-min", type=float, default=0.05, metavar="F",
                    help="minimum escape offset, as a fraction of S. A mark that leaves the solid "
                         "has to actually clear it: without this floor most escapees land back "
                         "inside their own core and the dissolving side never thins to the "
                         "measured 0.46x.")
    ap.add_argument("--dissolve-tail", type=float, default=0.25, metavar="F",
                    help="fraction of escaped marks drawn from the heavy tail (~1/d out to 0.9 S) "
                         "instead of the near-field exponential. 0 = no far base.")
    ap.add_argument("--dissolve-patch", type=float, default=0.35, metavar="A",
                    help="amplitude of the LOCAL patchiness of the dissolve field. The reference "
                         "front is not a straight ramp: it erodes in patches and leaves detached "
                         "solid islands behind. 0 = the old monotone half-plane gradient.")
    ap.add_argument("--comb", default=None, metavar="ANGLE,LEN[,SPREAD,THIN,WOBBLE]",
                    help="FRACTURE THE HALFTONE ITSELF. Past the dissolve front the ordered-dither "
                         "solid is combed along ANGLE: every dot is smeared into a streak up to "
                         "LEN (in units of the subject size S), the streak thins along its length "
                         "and breaks into flakes, and the solid it came from is eaten away by "
                         "exactly that much. This is what 样本A actually does -- the "
                         "broken half is the SAME dot screen pulled sideways, not a cloud of "
                         "particles born somewhere else. SPREAD deg of angular variation from a "
                         "smooth field (so the streaks bend like wind, not like a radial fan), "
                         "THIN the fade exponent, WOBBLE the field's spatial scale (fraction of W).")
    ap.add_argument("--comb-life", type=float, default=0.04, metavar="SEC",
                    help="how often the comb is recomputed (one plane per this many seconds). "
                         "Independent of --rain-life, which is a measured constant of the rain "
                         "layer and must not be changed to drive the comb.")
    ap.add_argument("--comb-emit", type=float, default=0.22, metavar="P",
                    help="fraction of the halftone dots that actually streak. At 1.0 every dot "
                         "paints a line, the lines overlap completely and the result reads as a "
                         "flame or a ribbon; the reference has SEPARATED streaks with black between "
                         "them. The choice is made per source dot, so a streak keeps its identity "
                         "along its whole run instead of dissolving into fog. 0.15-0.30.")
    ap.add_argument("--spray-bite", type=float, default=0.65, metavar="F",
                    help="how much of the emitter's own ink the spray takes with it. The material "
                         "that flies off has to come from somewhere: at 0 the head stays whole while "
                         "a blizzard of its own substance leaves it. The bite is broken up by coarse "
                         "noise so it eats chunks, not an even fade.")
    ap.add_argument("--rain-bow", type=float, default=0.0, metavar="K",
                    help="per-dash track curvature. The lateral offset grows as K*(arc^2)/W with a "
                         "sign drawn per dash, so each streak bows instead of running dead straight "
                         "and the field reads as wind rather than as a radial fan. 0.6-1.6 typical; "
                         "0 = the old straight rays.")
    ap.add_argument("--spray", default=None, metavar="N,ANGLE,FAN[,SPEED,SPAN]",
                    help="PUSH THE BROKEN PIXELS OUT. Same machinery as the rain -- short-lived "
                         "flashes of small blocks, angle drawn per dash, not from a smooth field -- "
                         "but the emitters are the BROKEN MATERIAL itself (seeded on the dissolve "
                         "field), and the angles are a fan about ANGLE with half-width FAN degrees. "
                         "So the fragments leave the form as a spray that opens up with distance "
                         "instead of sitting where they broke. SPEED multiplies the rain speed, "
                         "SPAN the track length.")
    ap.add_argument("--filament", default=None, metavar="N,LEN[,BRANCH,WIDTH,GAIN]",
                    help="grow the escaped material into BRANCHING FILAMENTS instead of dust. N "
                         "root strands are seeded on the dissolve front and integrated downstream "
                         "through the image's own flow field for LEN (in units of the subject size "
                         "S), each spawning BRANCH side shoots. The paths are painted into the dust "
                         "weight, so the normal marks land along them and chain into veins -- which "
                         "is how a broken-off part reads as an EXTENSION of the form (a wing, roots, "
                         "nerves) rather than as debris that fell off and faded. WIDTH px, GAIN "
                         "relative to the subject's own weight. Marks born on a filament do not "
                         "escape again.")
    ap.add_argument("--dissolve-strand", type=float, default=0.6, metavar="K",
                    help="0 = escaped marks are placed on a straight ray from home (dust). "
                         "1 = the birth point is ADVECTED along the image's own flow field for the "
                         "whole escape distance, so neighbouring marks land on the same streamline "
                         "and chain into veins/filaments. K blends the two: the strand keeps a net "
                         "heading of K toward DEG and (1-K) from the field. Measured on the "
                         "reference: connected strands reach 0.35 S, ~10x a single mark.")
    ap.add_argument("--dissolve-floor", type=float, default=0.0, metavar="F",
                    help="fraction of escaped marks spread UNIFORMLY BY AREA over the lobe out to "
                         "--dissolve-reach, giving a flat far-field plateau instead of a decay "
                         "tail. The reference holds ~0.10-0.12 of core fill from 0.25 S all the way "
                         "off canvas: the escaped material does not fade out, it becomes part of "
                         "the picture. 0.3-0.5 for that; 0 for a work that really does fade.")
    ap.add_argument("--dissolve-reach", type=float, default=0.9, metavar="F",
                    help="how far the heavy tail may reach, as a fraction of S. Raise this to throw "
                         "ash further WITHOUT thickening it -- the tail carries few marks. Raising "
                         "--dissolve-near instead fattens the whole cloud into an even grey blanket, "
                         "which is not what the reference does.")
    ap.add_argument("--dissolve-keepout", default=None, metavar="X,Y,RX,RY[,S]",
                    help="soft ellipse the escaped ash must stay OUT of (relative coords). Use it "
                         "to keep the ash off a second element that has to stay legible on its own "
                         "-- embers, a lit window, an anchored object. Offsets that would land "
                         "inside are pulled back to just outside it; nothing is deleted.")
    ap.add_argument("--escape-legacy", action="store_true",
                    help="restore the pre-E2 escape: one long 0.22*W flight per life. Produces an "
                         "even haze instead of local disintegration; kept only for reproducing "
                         "older renders.")
    ap.add_argument("--seed", type=int, default=305)
    args = ap.parse_args()
    MASS_EXPLICIT = args.mass is not None
    for key, value in PRESETS[args.preset].items():
        if getattr(args, key, None) is None:
            setattr(args, key, value)
    if args.floor is None:
        args.floor = "auto" if args.preset == "flux" else 0.0
    if isinstance(args.floor, str):
        args.floor = None if args.floor.lower() == "auto" else float(args.floor)

    rng = np.random.default_rng(args.seed)
    src = Image.open(args.input)
    ss = max(1, int(args.supersample))
    out_w = args.size
    W = args.size * ss
    H = max(64, round(src.height / src.width * W))
    out_h = max(1, round(H / ss))
    SRC_RGB = (np.asarray(src.convert("RGB").resize((W, H), Image.LANCZOS),
                          dtype=np.float32) / 255.0)
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

    DIS = SUBJ = None
    DIS_S = None
    if args.dissolve:
        _p = [float(v) for v in args.dissolve.split(",")]
        _deg, _start, _soft = _p[0], _p[1], max(1e-3, _p[2])
        DIS_BREATH = _p[3] if len(_p) > 3 else 0.0
        _g8 = smooth(gray.copy(), max(2, 8 * ss))
        SUBJ = np.clip((_g8 - np.percentile(_g8, 55)) /
                       max(1e-6, np.percentile(_g8, 97) - np.percentile(_g8, 55)), 0, 1)
        _yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _ax, _ay = np.cos(np.deg2rad(_deg)), np.sin(np.deg2rad(_deg))
        _t = _xx / W * _ax + _yy / H * _ay
        _sel = SUBJ > 0.25
        if _sel.any():
            _lo, _hi = np.percentile(_t[_sel], 2), np.percentile(_t[_sel], 98)
        else:
            _lo, _hi = _t.min(), _t.max()
        _t = (_t - _lo) / max(1e-6, _hi - _lo)
        _ramp = np.clip((_t - _start) / _soft, 0, 1)
        # SUBJECT SIZE, in px: every length in M4 is expressed as a fraction of it,
        # because the reference profiles only collapse onto each other once
        # normalised by sqrt(core area).
        DIS_S = float(np.sqrt(max(1.0, float(_sel.sum()))))
        # edges erode first -- BUT ONLY INSIDE THE RAMP. Ungated, this 0.30 term
        # sprinkled ash along every strong contour, including the intact side,
        # softening the vacuum cliff that the reference keeps there (measured:
        # 0.86 -> 0.006 fill within 0.03 S, then true black).
        _gy, _gx = np.gradient(smooth(gray.copy(), max(1, 2 * ss)))
        _e = np.hypot(_gx, _gy); _e = _e / (np.percentile(_e, 97) + 1e-6)
        _gate = np.clip(4.0 * _ramp, 0, 1)
        # LOCAL, NOT GLOBAL. A monotone ramp dissolves the subject like a wipe.
        # The reference front erodes in patches and leaves detached solid islands
        # behind it (core splits into 2+ components, contour roughness 2.8-5.0 vs
        # 1.3 for a smooth circle). Zero-mean noise at 0.08 S, alive across the
        # WHOLE dissolved zone -- not just the transition band -- both eats
        # bites ahead of the front and spares islands behind it.
        _nsc = int(max(3, round(0.08 * DIS_S))) if args.dissolve_patch > 0 else max(3, 10 * ss)
        _n = smooth(rng.random((H, W)).astype(np.float32), _nsc)
        _n = (_n - _n.mean()) / (_n.std() + 1e-6)
        DIS = np.clip(_ramp
                      + 0.30 * np.clip(_e, 0, 1) * _gate
                      + args.dissolve_patch * _n * np.clip(1.6 * _ramp, 0, 1), 0, 1)
        DIS = smooth(DIS, max(1, ss))
        # The held part is the IMAGE ITSELF as ordered halftone — build_mass's own
        # image-derived segmentation, never a painted mask. DIS only GATES it.
        # (Looking at the reference finally settled this: the held face is a
        #  smooth dithered surface with real midtones, and the dissolving part is
        #  a different TEXTURE — small chaotic flecks — not the same marks thinned.)
        # --dissolve used to force the halftone mass layer on. That was wrong:
        # it silently changed the BASE rendering mode of any pure-particle image
        # (mass=0), so adding a little ash also dropped a solid dithered slab
        # onto the brightest coherent region. Dissolve now only gates whatever
        # mass layer the image was already asking for. If you want the held part
        # rendered as ordered halftone, say so: --mass 1.
        if not MASS_EXPLICIT and args.mass > 0:
            args.mass = max(args.mass, 1.0)
        print("dissolve: solid %.0f%% / transition %.0f%% / free %.0f%%"
              % (100*(DIS<0.25).mean(), 100*((DIS>=0.25)&(DIS<0.75)).mean(),
                 100*(DIS>=0.75).mean()), file=sys.stderr)
    else:
        DIS_BREATH = 0.0

    if args.floor is None:
        # THE VOID IS MANUFACTURED, and how much of it exists is a property of
        # THIS image. Cut the dimmest ~65% — measured across the reference set,
        # the hand-picked floors all sat between the 37th and 82nd percentile.
        args.floor = float(np.percentile(gray, 65.0))
        print("auto floor = %.3f" % args.floor, file=sys.stderr)

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
        SW_SPD = np.ones((H, W), dtype=np.float32)
        for _spec in args.swirl:
            _p = [float(v) for v in _spec.split(",")]
            _cx, _cy = _p[0] * W, _p[1] * H
            _st = _p[2] if len(_p) > 2 else 1.0
            _rad = (_p[3] if len(_p) > 3 else 0.35) * max(W, H)
            _ratio = _p[4] if len(_p) > 4 else 1.0       # minor/major of the PROJECTED ring
            _tilt = _p[5] if len(_p) > 5 else 0.0        # major-axis angle, degrees
            _pitch = _p[6] if len(_p) > 6 else 0.0       # radial inflow as a fraction of tangential
            _ratio = max(1e-2, min(1.0, _ratio))
            _dx, _dy = _xx - _cx, _yy - _cy
            # A VORTEX SEEN AT AN ANGLE IS NOT A CIRCLE. The water's concentric
            # rings are circles in the WATER plane; the camera compresses them to
            # ellipses. Rotate in the water plane, then project the VELOCITY back
            # -- that projection is what makes the ends of the ellipse look slow
            # and the near/far rims look fast. A circular field instead drives
            # material ACROSS the rings, which is what reads as a flat disc.
            _th = np.deg2rad(_tilt); _ct, _stl = np.cos(_th), np.sin(_th)
            _u = _dx * _ct + _dy * _stl
            _v = -_dx * _stl + _dy * _ct
            _pp, _qq = _u, _v / _ratio                   # back to the water plane
            _rw = np.hypot(_pp, _qq) + 1e-6
            _radw = _rad
            # angular momentum: the throat whips, the outer rim barely turns
            _core = max(1e-6, 0.22 * _radw)
            _spd = np.minimum(1.0, _core / np.maximum(_rw, 1e-6))
            _sgn_st = -1.0 if _st < 0 else 1.0
            # unit tangential + radial inflow, in the water plane
            _wp = _sgn_st * (-_qq / _rw) - _pitch * (_pp / _rw)
            _wq = _sgn_st * (_pp / _rw) - _pitch * (_qq / _rw)
            _wp, _wq = _wp * _spd, _wq * _spd
            # project the velocity back to the image (this is the foreshortening)
            _du, _dv = _wp, _wq * _ratio
            _tx = _du * _ct - _dv * _stl
            _ty = _du * _stl + _dv * _ct
            _mag = np.hypot(_tx, _ty) + 1e-9
            _tx, _ty = _tx / _mag, _ty / _mag            # direction for the field
            _w = min(abs(_st), 1.0) * np.exp(-(_rw / _radw) ** 2)
            _sp = _mag / (np.percentile(_mag[_w > 0.25], 90) + 1e-9) if np.any(_w > 0.25) else _mag
            SW_SPD = np.where(_w > SW_W, np.clip(_sp, 0.05, 2.5), SW_SPD).astype(np.float32)
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
        SW_SPD = None
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

    # ---- ANCHOR: one thing that stays solid, in its own colour ----
    ANCH = ANCH_PLANE = ANCH_RGB = None
    if args.anchor:
        _yy2, _xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
        ANCH = np.zeros((H, W), dtype=np.float32)
        ANCH_HEX = None; _ablk, _again, _abp, _asat = 2.0, 1.0, 58.0, 1.0
        for _spec in args.anchor:
            _parts = _spec.split(",")
            if _parts[-1].strip().startswith("#"):
                ANCH_HEX = _parts[-1].strip(); _parts = _parts[:-1]
            _a = [float(v) for v in _parts]
            _ax, _ay, _arx, _ary = _a[0] * W, _a[1] * H, max(_a[2], 1e-3) * W, max(_a[3], 1e-3) * H
            _as = _a[4] if len(_a) > 4 else 1.0
            _d = ((_xx2 - _ax) / _arx) ** 2 + ((_yy2 - _ay) / _ary) ** 2
            # tight edge: a soft Gaussian tail tints whatever is next to the
            # held object, and a red-stained wave reads as a mistake
            ANCH = np.maximum(ANCH, abs(_as) * np.exp(-(_d ** 2.6) * 2.6))
            _ablk = _a[5] if len(_a) > 5 else 2.0     # pixel block size (output px)
            _again = _a[6] if len(_a) > 6 else 1.0     # exposure lift
            _abp = _a[7] if len(_a) > 7 else 58.0      # black-point percentile in-region
            _asat = _a[8] if len(_a) > 8 else 1.0      # chroma boost
        ANCH = np.clip(ANCH, 0, 1)
        # NO SEGMENTATION. The object is already legible in the photograph --
        # black hull, red sail, dark mast. Just PIXELATE it: block the colour
        # down, then ordered-dither EACH CHANNEL against its own value. Dark
        # water prints nothing and stays void; the sail's red channel prints and
        # its green/blue do not, so it comes out red. Trying to "find the ship"
        # first was the mistake -- luminance has no threshold that isolates an
        # object which occupies both the darkest and the middle of the range.
        _sel = ANCH > 0.3
        _blk = max(2, int(round(_ablk * ss)))
        _b = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],
                       [12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],
                       [3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
                       [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]],
                      dtype=np.float32) / 64.0
        _bs = np.kron(_b, np.ones((_blk, _blk), np.float32))
        _bay = np.tile(_bs, (H // _bs.shape[0] + 1, W // _bs.shape[1] + 1))[:H, :W]
        _asrc = SRC_RGB
        if args.anchor_src:
            _asrc = (np.asarray(Image.open(args.anchor_src).convert("RGB")
                                .resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0)
        _sm = Image.fromarray((np.clip(_asrc, 0, 1) * 255).astype(np.uint8))
        _sm = _sm.resize((max(1, W // _blk), max(1, H // _blk)), Image.BOX) \
                 .resize((W, H), Image.NEAREST)
        _v3 = np.asarray(_sm, np.float32) / 255.0
        # black point per channel, read off the ellipse itself: the region is
        # mostly the water the object sits in, so that level becomes zero and
        # only the object survives -- no segmentation, just an exposure decision
        _bp = np.array([float(np.percentile(_v3[..., c][_sel], _abp)) for c in range(3)],
                       dtype=np.float32) if _sel.any() else np.zeros(3, np.float32)
        _lv3 = np.clip((_v3 - _bp[None, None, :]) / np.maximum(1.0 - _bp, 1e-3)[None, None, :],
                       0, 1)
        if _asat != 1.0:
            # a held object surrounded by pure monochrome needs more chroma than
            # the photograph has, or the one coloured thing in the frame reads
            # as a stain rather than as an object
            # only where there IS chroma. Boosting a near-neutral pixel amplifies
            # its tiny cast into a strong false hue -- white foam turns cyan.
            _lm = _lv3.mean(axis=2, keepdims=True)
            _c0 = (_lv3.max(axis=2, keepdims=True) - _lv3.min(axis=2, keepdims=True)) \
                  / (_lv3.max(axis=2, keepdims=True) + 1e-6)
            _bo = 1.0 + (_asat - 1.0) * np.clip((_c0 - 0.38) / 0.30, 0, 1) ** 1.2
            _lv3 = np.clip(_lm + (_lv3 - _lm) * _bo, 0, 1)
        _lv3 = np.clip(_lv3 * _again, 0, 1) ** (1.0 / 1.5)
        if ANCH_HEX is not None:
            _t = (hex_rgb(ANCH_HEX) / 255.0)[None, None, :]
            _lv3 = np.clip(_lv3.max(axis=2, keepdims=True) * _t, 0, 1)
        ANCH_DOTS = (_lv3 > _bay[:, :, None]).astype(np.float32)
        ANCH_PLANE = ANCH[:, :, None] * ANCH_DOTS
        ANCH_RGB = _lv3
        print("anchor: %.1f%% of canvas held solid" % (100.0 * (ANCH > 0.5).mean()),
              file=sys.stderr)

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
    if DIS is not None:
        # the solid must DIE AWAY into the particles, not be cut out of them:
        # build_mass thresholds hard, so fade its plane along the dissolve field
        _fade = np.clip(1.0 - (DIS - 0.10) / 0.55, 0.0, 1.0) ** 1.3
        def _fit(a, ref):
            if a.shape == ref.shape:
                return a
            return np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                              .resize((ref.shape[1], ref.shape[0]), Image.BILINEAR),
                              dtype=np.float32) / 255.0
        if args.comb:
            # ---- COMB: the halftone is dragged, not replaced ----
            _cp = [float(v) for v in args.comb.split(",")]
            _cang, _clen = _cp[0], _cp[1]
            _cspr = _cp[2] if len(_cp) > 2 else 18.0
            _cthin = _cp[3] if len(_cp) > 3 else 1.4
            _cwob = _cp[4] if len(_cp) > 4 else 0.16
            _R = np.clip((DIS - 0.05) / 0.55, 0, 1).astype(np.float32)   # how broken
            _Lmax = max(4.0, _clen * (DIS_S if DIS_S else 0.25 * W))
            # a smooth angle field: streaks bend with the wind instead of running
            # dead straight out of one point
            # smooth() counts PASSES, not sigma: a fraction of the RENDER width
            # here means hundreds of passes over a 10M array (minutes). Build the
            # field small and stretch it.
            def _octave(frac, amp):
                _sm = smooth(rng.random((max(8, H // 24), max(8, W // 24))).astype(np.float32),
                             max(2, int(frac * (W // 24))))
                _sm = (_sm - _sm.mean()) / (_sm.std() + 1e-6)
                return amp * np.asarray(Image.fromarray(
                    (np.clip(_sm * 0.25 + 0.5, 0, 1) * 255).astype(np.uint8))
                    .resize((W, H), Image.BILINEAR), np.float32) / 255.0
            # TWO OCTAVES. One smooth field bends every streak the same way, so the
            # escape leaves as a single bundle. A second, finer octave splits it
            # into a few lanes that separate as they travel -- which is what the
            # reference looks like near the break.
            _an = _octave(_cwob, 1.0) + _octave(_cwob * 0.28, 0.55)
            _an = (_an - _an.mean()) / (_an.std() + 1e-6)
            _ang = np.deg2rad(_cang) + np.deg2rad(_cspr) * _an
            _cx, _cy = np.cos(_ang).astype(np.float32), np.sin(_ang).astype(np.float32)
            _K = 32
            _CPER = float(_cp[6]) if len(_cp) > 6 else 12.0
            _CLIVE = float(_cp[7]) if len(_cp) > 7 else 0.55
            _CDIV = float(_cp[8]) if len(_cp) > 8 else 34.0
            _CNAR = float(_cp[9]) if len(_cp) > 9 else 0.30
            _CLONG = float(_cp[10]) if len(_cp) > 10 else 3.5
            _CRMIN = float(_cp[11]) if len(_cp) > 11 else 0.22
            _CWALK = float(_cp[12]) if len(_cp) > 12 else 1.8
            # ragged outer boundary of the debris field
            _EDGE = np.asarray(Image.fromarray((smooth(
                rng.random((max(8, H // 16), max(8, W // 16))).astype(np.float32), 5)
                * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255.0
            _EDGE = np.clip(0.45 + 1.5 * (_EDGE - _EDGE.mean()) / (_EDGE.std() + 1e-6)
                            * 0.28 + 0.55, 0.25, 1.55).astype(np.float32)
            _step = _Lmax / _K
            # ONE PLANE PER FLASH CYCLE. The flakes step outward by one tap per
            # cycle and the cycle index wraps, so the escape animates and the loop
            # still closes exactly. Recomputing the whole comb every frame is far
            # too slow; the reference's material flashes rather than cruises, so a
            # plane per --rain-life is the right granularity anyway.
            _CSF = (2.0 + 5.0 * np.asarray(Image.fromarray(
                (smooth(rng.random((max(8, H // 20), max(8, W // 20))).astype(np.float32), 6)
                 * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR),
                np.float32) / 255.0).astype(np.float32) * max(1, ss) * 0.6 + 1.0
            _csq = np.clip(_CSF, 1.0, 24.0).astype(np.float32); _CSF = _csq
            _yy1, _xx1 = np.mgrid[0:H, 0:W]
            _he0 = (((_xx1 / _CSF).astype(np.uint32) * np.uint32(2654435761))
                    ^ ((_yy1 / _CSF).astype(np.uint32) * np.uint32(2246822519)))
            _emit0 = ((_he0 & np.uint32(0xFFFF)).astype(np.float32) / 65535.0
                      < args.comb_emit)
            # a dot that left is GONE from where it was: the hole in the ear and
            # the back of the skull is the same event as the streak leaving.
            _base = (mass_plane * np.where(_emit0, 1.0 - _R,
                                           (1.0 - _R) ** 0.25)).astype(np.float32)
            MASS_SEQ = []
            _NC = 1 if args.static_only else max(1, int(round(args.seconds /
                                                              max(args.rain_life, 1e-3))))
            for _ph in range(_NC):
              _yy0, _xx0 = np.mgrid[0:H, 0:W].astype(np.float32)
              # SUB-STEP START OFFSET. Without it every sampled distance is an
              # exact multiple of the tap spacing, so the flakes line up on rings
              # at k*step and the far plume shows regular comb teeth.
              _hj = ((_xx0.astype(np.int64) * 374761393
                      + _yy0.astype(np.int64) * 668265263) & 0xFFFF)
              _uj = (_hj.astype(np.float32) / 65535.0)
              # a small LATERAL jitter as well: without it neighbouring sources
              # walk exactly parallel tracks spaced by the dither lattice, and
              # the lattice beats against the direction into a woven moire.
              _hl = ((_xx0.astype(np.int64) * 2246822519
                      + _yy0.astype(np.int64) * 3266489917) & 0xFFFF)
              _ul = (_hl.astype(np.float32) / 65535.0 - 0.5) * 1.6 * _step
              _px = _xx0 - np.cos(_ang) * _uj * _step - np.sin(_ang) * _ul
              _py = _yy0 - np.sin(_ang) * _uj * _step + np.cos(_ang) * _ul
            # base: what is LEFT behind. the solid is eaten by exactly how broken it is
              _out = _base
              for _k in range(1, _K + 1):
                  _ux = sample(_cx, _px, _py); _uy = sample(_cy, _px, _py)
                  # DIVERGE. With one smooth field every streak bends the same way
                  # and the plume closes into a bundle. Each clump gets its own
                  # angular offset that GROWS with distance, so the fan opens.
                  if _CDIV != 0.0:
                      # A FAN, NOT A WIDENING BAND. The offset has to be fixed for
                      # the whole path and applied from the first step, so rays
                      # leave the break in genuinely different directions.
                      # Hashing the CURRENT position instead re-randomises it every
                      # step, which is a wander, not a fan.
                      _hd = ((np.clip(_px, 0, W - 1).astype(np.int64) // 7) * 40503
                             + (np.clip(_py, 0, H - 1).astype(np.int64) // 7) * 12289)
                      _sd = ((_hd & 1023).astype(np.float32) / 1023.0 - 0.5)
                      _th2 = _sd * np.deg2rad(_CDIV) * (_k / _K) ** 1.4
                      _c2, _s2 = np.cos(_th2), np.sin(_th2)
                      _ux, _uy = _ux * _c2 - _uy * _s2, _ux * _s2 + _uy * _c2
                  _px = _px - _ux * _step; _py = _py - _uy * _step
                  if _CWALK > 0:
                      # RANDOM WALK. A fixed per-clump angle still gives straight
                      # rays -- a ribbon that merely widens. Adding an
                      # independent kick at every step makes the paths wander
                      # apart, so the far end is a loose scatter instead of a
                      # band. Amplitude grows with distance.
                      _hw = ((np.clip(_px, 0, W - 1).astype(np.int64) * 374761393
                              + np.clip(_py, 0, H - 1).astype(np.int64) * 668265263
                              + _k * 2246822519) & 4095)
                      _w1 = (_hw & 63).astype(np.float32) / 63.0 - 0.5
                      _w2 = ((_hw >> 6) & 63).astype(np.float32) / 63.0 - 0.5
                      # only the LAST THIRD wanders. Applied from the start it
                      # scatters the whole plume and the direction is lost.
                      _amp = _CWALK * _step * np.clip((_k / _K - 0.55) / 0.45, 0, 1) ** 2.0
                      _px = _px + _w1 * _amp; _py = _py + _w2 * _amp
                  _sr = sample(_R, _px, _py)
                  # SCATTER, DON'T BEAM. Every clump travelling the same distance
                  # makes a solid wedge with a clean edge. Each clump gets its own
                  # reach (some stop early, some go all the way), multiplied by a
                  # coarse field so the OUTER BOUNDARY of the debris is ragged
                  # rather than an arc.
                  _hr = ((np.clip(_px, 0, W - 1).astype(np.int64) // 5) * 668265263
                         + (np.clip(_py, 0, H - 1).astype(np.int64) // 5) * 2246822519)
                  _rr = ((_hr & 2047).astype(np.float32) / 2047.0)
                  _edge = sample(_EDGE, _px, _py)
                  _reach = (_Lmax * _sr * (_CRMIN + (1.0 - _CRMIN) * _rr ** 0.7)
                            * _edge + 1e-6)
                  _s = _k * _step
                  _f = (_s + _uj * _step) / _reach
                  # NEAREST, NOT BILINEAR. Interpolating the dot screen turns the
                  # comb into motion blur -- one continuous grey smear. The
                  # reference keeps hard separated flakes because the dots stay
                  # dots; and the survival is a hard per-(pixel,tap) lottery, so a
                  # streak breaks up ALONG its run instead of fading.
                  _xi = np.clip(_px + 0.5, 0, W - 1).astype(np.int32)
                  _yi = np.clip(_py + 0.5, 0, H - 1).astype(np.int32)
                  # WHICH DOTS STREAK AT ALL -- decided per SOURCE, so one streak
                  # keeps its identity down its whole run. With every dot streaking
                  # the lines merge into a ribbon and the thing reads as flame.
                  # FLAKES, NOT HAIRLINES: decide per CLUMP, and let the clump
                  # size itself vary, so the debris has ragged widths instead of
                  # a comb of equal one-dot filaments.
                  # PIXEL BARS, NOT BLOCKS. Quantising x and y by the same cell
                  # gives square blobs. The reference's debris is a BAR: one or
                  # two cells across, several cells long, lying along the flow.
                  # So quantise in the streak's own frame -- long along it,
                  # narrow across it.
                  _cs = _CSF[np.clip(_yi, 0, H - 1), np.clip(_xi, 0, W - 1)]
                  _dxs = _cx[np.clip(_yi, 0, H - 1), np.clip(_xi, 0, W - 1)]
                  _dys = _cy[np.clip(_yi, 0, H - 1), np.clip(_xi, 0, W - 1)]
                  _uu = _px * _dxs + _py * _dys
                  _vv = -_px * _dys + _py * _dxs
                  # stagger the lanes: without an offset every lane's clump
                  # boundaries line up across the flow and the field reads as a
                  # ladder. The offset is a hash of the lane index.
                  _lane = (_vv / np.maximum(_cs * _CNAR, 1.0)).astype(np.int64)
                  _lh = ((_lane * 2654435761) & 0xFFFF).astype(np.float32) / 65535.0
                  _cxq = ((_uu / np.maximum(_cs * _CLONG, 1.0)) + _lh
                          ).astype(np.int64).astype(np.uint32)
                  _cyq = _lane.astype(np.uint32)
                  _he = ((_cxq * np.uint32(2654435761))
                         ^ (_cyq * np.uint32(2246822519)))
                  _emit = ((_he & np.uint32(0xFFFF)).astype(np.float32) / 65535.0
                           < args.comb_emit)
                  # and a per-(pixel,tap) lottery breaks each streak into flakes
                  _h = ((_cxq * np.uint32(73856093))
                        ^ (_cyq * np.uint32(19349663)))
                  _q = (_h & np.uint32(0xFFFF)).astype(np.float32) / 65535.0
                  # per-source phase so flakes are not aligned across sources
                  # (that alignment is what showed as regular comb teeth), plus
                  # the cycle phase, which is what makes them travel
                  # THE FLAKES MUST TRAVEL, NOT JUST RE-ROLL. With the gap
                  # pattern re-hashed at every tap the lit set flickers in place
                  # (measured: best-match shift 0,0, survival .59 -- the reference
                  # is +1,+1 with .39). Make the gaps a PERIODIC function of
                  # distance minus phase and the whole dash pattern slides
                  # outward along the streak; the clump only sets its phase.
                  # Loop closes because the phase advances by exactly 1 period.
                  # a strict period makes every streak an evenly-spaced dashed
                  # line and neighbouring streaks fall into phase bands -- woven,
                  # machine-made. The period is drawn per clump instead.
                  _q2 = (((_he >> np.uint32(11)) & np.uint32(0x3FF)).astype(np.float32)
                         / 1023.0)
                  _per = _CPER * (0.55 + 1.10 * _q2)
                  _pat = np.mod(_f * _per - _ph / max(_NC, 1) - _q, 1.0)
                  # DRIFT AND DEATH ARE TWO DIFFERENT THINGS. The sliding pattern
                  # gives the slow outward drift (measured +1,+1 px/frame); the
                  # turnover is separate -- 61% of the reference's debris is gone
                  # the next frame and reborn elsewhere. So a whole flake blinks
                  # on a per-(clump, frame) draw, keyed on _ph so the loop closes.
                  _alive = (_emit & (_pat < 0.70 * np.clip(1.0 - _f, 0, 1) ** _cthin)
                            & (_f <= 1.0))
                  _out = np.maximum(_out, mass_plane[_yi, _xi] * _alive)
              # BLINK WHOLE BARS, IN OUTPUT SPACE. Done inside the tap loop the
              # decision is averaged over 32 taps and the flicker vanishes
              # (measured survival .82 against the reference's .39). Here each
              # bar -- one cell of the streak-frame lattice at the place it
              # LANDED -- is on or off for the whole frame.
              _uo = _xx0 * np.cos(_ang) + _yy0 * np.sin(_ang)
              _vo = -_xx0 * np.sin(_ang) + _yy0 * np.cos(_ang)
              _lo2 = (_vo / np.maximum(_CSF * _CNAR, 1.0)).astype(np.int64)
              _uo2 = (_uo / np.maximum(_CSF * _CLONG, 1.0)).astype(np.int64)
              _hb = (((_uo2 * 2246822519) ^ (_lo2 * 3266489917)
                      ^ (_ph * 668265263)) & 0xFFFF).astype(np.float32) / 65535.0
              _new = np.clip(_out - _base, 0, 1)
              _out = np.maximum(_base, _new * (_hb < _CLIVE))
              MASS_SEQ.append(_out.astype(np.float32))
            mass_plane = MASS_SEQ[0]
            mass_mask = np.maximum(mass_mask * (1.0 - _R) ** 0.85,
                                   smooth(np.clip(_out, 0, 1), max(2, int(0.004 * W))) * 0.9)
            print("comb: angle %.0f, reach %.0f px (%.2f S), spread %.0f deg, %d taps"
                  % (_cang, _Lmax, _clen, _cspr, _K), file=sys.stderr)
        else:
            mass_plane = mass_plane * _fit(_fade, mass_plane)
            mass_mask = mass_mask * _fit(_fade, mass_mask)

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
    # 虚实结合: with a dissolve in play the flecks must also live ON the held
    # halftone, not be swept off it — in the reference the two textures occupy
    # the SAME space, they are not two territories with a border between them.
    weight *= (1.0 - (0.45 if DIS is not None else 0.85) * mass_mask)
    if DIS is not None:
        # ASH IS CONSERVED. Whatever solidity the dissolve field takes away must
        # come back as particles — dissolving is a change of STATE, not a
        # subtraction. Under the born engine conservation is exact by
        # construction (the same particle is either sitting in the core or out
        # in the cloud this cycle), so no weight hump is needed; the hump is
        # kept only for the legacy flight, which really did lose marks.
        if args.escape_legacy or args.escape <= 0:
            weight = weight * (0.55 + 1.45 * DIS)
    # curl of a smooth random field: divergence-free, so anything riding it
    # wanders and swirls instead of splaying out from a source
    # OWN STREAM, on purpose. This field is built on every render, so drawing
    # it from the shared rng shifts every later draw (stroke seeding, rain) and
    # the same seed stops reproducing the same file across versions. Anything
    # added here later must take a side stream too.
    _rng_turb = np.random.default_rng((args.seed * 2654435761) & 0xFFFFFFFF)
    _n1 = smooth(_rng_turb.random((H, W)).astype(np.float32), max(4, 14 * ss))
    _n1 = (_n1 - _n1.mean()) / (_n1.std() + 1e-6)
    _ny, _nx = np.gradient(_n1)
    _nn = np.hypot(_nx, _ny) + 1e-6
    TRB_X = (_ny / _nn).astype(np.float32)
    TRB_Y = (-_nx / _nn).astype(np.float32)

    FIL = None
    if args.filament and DIS is not None:
        _fp = [float(v) for v in args.filament.split(",")]
        _fn = int(_fp[0]); _flen = _fp[1]
        _fbr = _fp[2] if len(_fp) > 2 else 1.5
        _fw = _fp[3] * ss if len(_fp) > 3 else 2.0 * ss
        _fg = _fp[4] if len(_fp) > 4 else 1.0
        _ftp = _fp[5] if len(_fp) > 5 else 1.6
        _fdeg = np.deg2rad([float(v) for v in args.dissolve.split(",")][0])
        _fax, _fay = np.float32(np.cos(_fdeg)), np.float32(np.sin(_fdeg))
        # seed on the dissolve front: material that is going, but has not gone
        _seedw = (weight * np.clip((DIS - 0.25) / 0.35, 0, 1)
                  * np.clip((0.95 - DIS) / 0.35, 0, 1))
        if _seedw.sum() > 0:
            _sp = (_seedw / _seedw.sum()).ravel()
            _si = rng.choice(_sp.size, size=_fn, p=_sp)
            _sy0, _sx0 = np.divmod(_si, W)
            _px = _sx0.astype(np.float32); _py = _sy0.astype(np.float32)
            _plen = (DIS_S * _flen * np.exp(rng.standard_normal(_fn).astype(np.float32) * 0.55))
            _kb = float(np.clip(args.dissolve_strand, 0, 1))
            FIL = np.zeros((H, W), dtype=np.float32)
            _paths = [(_px, _py, _plen, np.ones(_fn, dtype=np.float32))]
            _acc_x, _acc_y, _acc_w = [], [], []
            for _gen in range(3):
                if not _paths:
                    break
                _nx, _ny, _nl, _nw = _paths.pop(0)
                if _nx.size == 0:
                    continue
                _NS = 160
                _stp = (_nl / _NS).astype(np.float32)
                _cx, _cy = _nx.copy(), _ny.copy()
                _bx = np.full(_cx.shape, _fax, dtype=np.float32)
                _by = np.full(_cx.shape, _fay, dtype=np.float32)
                _child = []
                for _k in range(_NS):
                    _fu, _fv = sample(fx, _cx, _cy), sample(fy, _cx, _cy)
                    _sg = np.where(_fu * _bx + _fv * _by < 0, -1.0, 1.0).astype(np.float32)
                    _fu, _fv = _fu * _sg, _fv * _sg
                    _ux = _fu * (1.0 - _kb) + _fax * _kb
                    _uy = _fv * (1.0 - _kb) + _fay * _kb
                    _tu, _tv = sample(TRB_X, _cx, _cy), sample(TRB_Y, _cx, _cy)
                    _ux = _ux + _tu * max(args.turbulence, 0.4) * 0.55
                    _uy = _uy + _tv * max(args.turbulence, 0.4) * 0.55
                    _un = np.hypot(_ux, _uy) + 1e-6
                    _bx, _by = _ux / _un, _uy / _un
                    _cx = _cx + _bx * _stp
                    _cy = _cy + _by * _stp
                    # A VEIN IS ATTACHED, NOT PAINTED OVER. The first fifth of a
                    # path deposits nothing: a root that dumps ink where the form
                    # is still solid fills in the very grooves that make the form
                    # readable (this is what swallowed the ear). And the far end
                    # has to actually vanish -- a strand that keeps its weight to
                    # the end leaves an unexplained clump out in the void.
                    _u_ = _k / _NS
                    _att = np.clip(_u_ / 0.20, 0, 1) * (1.0 - _u_) ** _ftp
                    _acc_x.append(_cx.copy()); _acc_y.append(_cy.copy())
                    _acc_w.append((_nw * _att).astype(np.float32))
                    if _gen < 2 and _fbr > 0 and _k in (int(_NS * 0.30), int(_NS * 0.60)):
                        _pick = rng.random(_cx.size) < (_fbr * 0.5)
                        if _pick.any():
                            _ang = (rng.standard_normal(int(_pick.sum())).astype(np.float32)
                                    * 0.55 + np.sign(rng.standard_normal(int(_pick.sum()))) * 0.45)
                            _ca2, _sa2 = np.cos(_ang), np.sin(_ang)
                            _child.append((_cx[_pick].copy(), _cy[_pick].copy(),
                                           (_nl[_pick] * 0.45).astype(np.float32),
                                           (_nw[_pick] * 0.6).astype(np.float32)))
                if _child:
                    _paths.append((np.concatenate([c[0] for c in _child]),
                                   np.concatenate([c[1] for c in _child]),
                                   np.concatenate([c[2] for c in _child]),
                                   np.concatenate([c[3] for c in _child])))
            _ax_ = np.concatenate(_acc_x); _ay_ = np.concatenate(_acc_y)
            _aw_ = np.concatenate(_acc_w)
            _ok = (_ax_ >= 0) & (_ax_ < W) & (_ay_ >= 0) & (_ay_ < H)
            np.add.at(FIL, (_ay_[_ok].astype(np.int64), _ax_[_ok].astype(np.int64)), _aw_[_ok])
            FIL = smooth(FIL, max(1, int(_fw)))
            if args.dissolve_keepout:
                # the filaments obey the same void as the ash: a second element
                # that has to stay legible cannot have veins growing over it
                _q = [float(v) for v in args.dissolve_keepout.split(",")]
                _yy2, _xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
                _e2 = (((_xx2 - _q[0] * W) / max(_q[2] * W, 1e-3)) ** 2
                       + ((_yy2 - _q[1] * H) / max(_q[3] * H, 1e-3)) ** 2)
                FIL = FIL * np.clip((_e2 - 1.0) / 0.8, 0, 1).astype(np.float32)
            FIL = FIL / (np.percentile(FIL[FIL > 0], 97) + 1e-6)
            FIL = np.clip(FIL, 0, 1.6).astype(np.float32)
            # gate by the dissolve field: filaments belong to the material that is
            # leaving, so they cannot thicken the part that is staying solid
            FIL = (FIL * np.clip((DIS - 0.35) / 0.30, 0, 1)).astype(np.float32)
            weight = weight + _fg * FIL * float(np.percentile(weight[weight > 0], 70))
            print("filament: %d roots, len %.1f S, %d branch gens, coverage %.1f%%"
                  % (_fn, _flen, 3, 100.0 * (FIL > 0.05).mean()), file=sys.stderr)
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
    SPD = np.ones((H, W), dtype=np.float32)
    if SW_SPD is not None:
        SPD = SPD * SW_SPD
    if ANCH is not None:
        SPD = SPD * (1.0 - ANCH)          # the held part does not travel
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
    # A DASH IS A COMET, not a dotted line. Measured off the reference: within one
    # run the blocks shrink 5-15x from head to tail while the gaps open 3-4x, and
    # blob areas across the field span two orders of magnitude (2px^2 .. 220px^2).
    # Constant size + constant gap + constant brightness is why a ruled dotted
    # line still reads as machine-made however the angle is jittered.
    KEEP = None
    if args.rain_keepout:
        _yk, _xk = np.mgrid[0:H, 0:W].astype(np.float32)
        KEEP = np.ones((H, W), dtype=np.float32)
        for _spec in args.rain_keepout:
            _k = [float(v) for v in _spec.split(",")]
            _kx, _ky = _k[0] * W, _k[1] * H
            _krx, _kry = max(_k[2], 1e-3) * W, max(_k[3], 1e-3) * H
            _ks = _k[4] if len(_k) > 4 else 1.0
            _kd = ((_xk - _kx) / _krx) ** 2 + ((_yk - _ky) / _kry) ** 2
            KEEP = KEEP * (1.0 - _ks * np.exp(-(_kd ** 1.8) * 1.5))
        KEEP = np.clip(KEEP, 0, 1)
        # reject seeds that start inside the keep-out
        _ok = sample(KEEP, rx, ry) > 0.5
        if _ok.any():
            rx, ry = rx[_ok], ry[_ok]
            r_hue = r_hue[_ok]; r_len = r_len[_ok]; r_phase = r_phase[_ok]
            if np.ndim(r_span): r_span = r_span[_ok]
        print("rain keep-out: %.0f%% of canvas excluded" % (100 * (KEEP < 0.5).mean()),
              file=sys.stderr)

    # per-dash base angle / spread / speed: the ambient rain and the spray are two
    # populations sharing one dash engine, so every angle has to be per dash.
    r_ang0 = np.full(rx.size, float(args.rain_angle), np.float32)
    r_spr = np.full(rx.size, float(args.rain_spread), np.float32)
    r_spdm = np.ones(rx.size, np.float32)
    if args.spray and DIS is not None:
        _sp = [float(v) for v in args.spray.split(",")]
        _sn = int(_sp[0]); _sa = _sp[1]; _sf = _sp[2]
        _ssp = _sp[3] if len(_sp) > 3 else 1.6
        _ssn = _sp[4] if len(_sp) > 4 else 1.8
        # emitters = the broken material itself
        # the emitter reaches a little way INTO the held part, so chunks come off
        # the ear and the back of the skull too -- damage should not stop dead at
        # the ramp's edge
        _emit = (weight * np.clip((DIS - 0.08) / 0.40, 0, 1)) ** 1.0
        if KEEP is not None:
            _emit = _emit * KEEP
        if _emit.sum() > 0:
            _pi = rng.choice(_emit.size, size=_sn, p=(_emit / _emit.sum()).ravel())
            _sy, _sx = np.divmod(_pi, W)
            _sx = _sx.astype(np.float32) + rng.random(_sn).astype(np.float32)
            _sy = _sy.astype(np.float32) + rng.random(_sn).astype(np.float32)
            rx = np.concatenate([rx, _sx]); ry = np.concatenate([ry, _sy])
            r_len = np.concatenate([r_len, rng.integers(10 * ss, 34 * ss, _sn)])
            _span_add = (rng.integers(110, 260, _sn) * ss).astype(np.float32) * _ssn
            r_span = np.concatenate([np.asarray(r_span, np.float32), _span_add])
            r_phase = np.concatenate([r_phase, rng.random(_sn).astype(np.float32)])
            r_hue = np.concatenate([r_hue, rng.integers(0, n_hues, _sn)])
            r_ang0 = np.concatenate([r_ang0, np.full(_sn, _sa, np.float32)])
            r_spr = np.concatenate([r_spr, np.full(_sn, _sf, np.float32)])
            r_spdm = np.concatenate([r_spdm, np.full(_sn, _ssp, np.float32)])
            # MASS COMES FROM SOMEWHERE. The spray used to be added on top, so the
            # head stayed whole while a blizzard of its own material flew off it.
            # Whatever is emitted is removed from the emitter: the ear and the
            # back of the skull lose actual chunks.
            _bite = smooth(np.clip(_emit / (np.percentile(_emit[_emit > 0], 55) + 1e-9),
                                   0, 1), max(2, int(0.008 * W)))
            _bn = smooth(rng.random((H, W)).astype(np.float32), max(3, int(0.022 * W)))
            _bn = (_bn - _bn.mean()) / (_bn.std() + 1e-6)
            # chunks, not an even fade: the noise is thresholded so the bite lands
            # as discrete holes with intact material between them
            _bite = np.clip(_bite * np.clip(0.35 + 1.35 * _bn, 0, 1.6), 0, 1)
            weight = weight * (1.0 - args.spray_bite * _bite)
            print("spray: %d dashes from the broken material, fan %.0f deg +/- %.0f, "
                  "speed x%.1f, bite %.2f (removes %.0f%% of the emitter's ink)"
                  % (_sn, _sa, _sf, _ssp, args.spray_bite,
                     100 * args.spray_bite * float(_bite[_emit > 0].mean())), file=sys.stderr)

    # ---- P-1/P-3/P-4/P-5: a dash is a short-lived FLASH of small blocks --------
    # Rebuilt against 12 native frames of the reference GIF (2560x1440, 25fps):
    #   block area median 4px^2   -> edge ~1.1 output px          (P-1)
    #   displacement median 64px/frame @2560 = 0.62 canvas-widths/s, and it
    #     correlates +0.36 with dash length                        (P-3)
    #   zero residue at the old position, 14.7% pixel survival, tracks never
    #     longer than 4 steps -> a dash lives 2-5 frames and is replaced (P-4)
    #   chain-to-chain angle difference is the SAME at 200px and at 1200px, so
    #     the angle is drawn per dash, not read from a smooth field (P-5)
    R_IDX = R_S = R_OX = R_OY = R_W = None
    if rx.size:
        _K = max(0.2, args.rain_wild)
        _base = max(1.0, args.rain_block * args.size / 1400.0) * ss
        _G = max(0.0, args.rain_spacing - 1.0)
        _J = max(0.0, args.rain_jitter)
        _idx, _s2, _ox, _oy, _w2, _dlen = [], [], [], [], [], []
        for _i in range(rx.size):
            _u0 = float(rng.random())
            _nd = int(2 + (26 * _K) * _u0 ** max(1.0, args.rain_short))
            _len = float(r_span[_i] if np.ndim(r_span) else r_span) \
                   * (float(_nd) / 26.0) * float(rng.uniform(0.7, 1.4))
            _sz0 = _base * float(np.clip(np.exp(rng.normal(0.0, 0.32 * _K)), 0.35, 2.6))
            _br = float(np.clip(rng.uniform(0.30, 1.0) ** (1.0 / max(_K, 0.3)), 0.12, 1.0))
            for _j in range(_nd):
                _t = _j / max(1, _nd - 1)
                _sarc = _len * (_t + _G * _t * _t) / (1.0 + _G)
                _sarc *= (1.0 + _J * float(rng.standard_normal()) * 0.35)
                # P-2 partial: per-BLOCK lognormal, not one size for the whole run
                _sz = max(1, int(round(_sz0 * (args.rain_taper ** _t)
                                       * float(np.exp(rng.normal(0.0, 0.40))))))
                _wt = float(np.clip(0.95 * _br * (1.0 + 0.25 * rng.standard_normal() * _J),
                                    0.15, 1.0))
                for _dy in range(_sz):
                    for _dx in range(_sz):
                        _idx.append(_i); _s2.append(_sarc)
                        _ox.append(float(_dx)); _oy.append(float(_dy)); _w2.append(_wt)
            _dlen.append(_len)
        R_IDX = np.asarray(_idx, np.int64)
        R_S  = np.asarray(_s2, np.float32)
        R_OX = np.asarray(_ox, np.float32); R_OY = np.asarray(_oy, np.float32)
        R_W  = np.asarray(_w2, np.float32)
        R_LEN = np.asarray(_dlen, np.float32)
        R_HUE = r_hue[R_IDX]

        # per-dash speed: discrete mix x (L / L_med)^alpha
        _mix = np.array([float(v) for v in args.rain_speed_mix.split(",")], np.float32)
        _lmed = float(np.median(R_LEN)) + 1e-6
        R_SPD = (_mix[rng.integers(0, _mix.size, rx.size)] * r_spdm
                 * (R_LEN / _lmed) ** args.rain_speed_len).astype(np.float32)

        # LIFE CYCLES. seconds/life rounded to an integer so the loop still closes;
        # the cycle index wraps mod C, so frame N == frame 0 exactly.
        R_CYC = max(1, int(round(args.seconds / max(args.rain_life, 1e-3))))
        _n = rx.size
        _bx = np.empty((_n, R_CYC), np.float32); _by = np.empty((_n, R_CYC), np.float32)
        _ang = np.empty((_n, R_CYC), np.float32)
        _base_ang = np.deg2rad(args.rain_angle)
        for _c in range(R_CYC):
            # each dash is reborn near ITS OWN home, not at a shuffled one: a spray
            # dash has to keep coming out of the break it belongs to.
            _bx[:, _c] = rx + rng.standard_normal(_n).astype(np.float32) * (0.02 * W)
            _by[:, _c] = ry + rng.standard_normal(_n).astype(np.float32) * (0.02 * H)
            _o = rng.standard_normal(_n).astype(np.float32) * np.deg2rad(r_spr)
            if args.rain_flow > 0:
                _fs = max(4, int(args.rain_flow_scale * max(W, H) * 0.22))
                _fn = smooth(rng.random((H, W)).astype(np.float32), _fs)
                _fn = (_fn - _fn.mean()) / (_fn.std() + 1e-6)
                _o = _o + np.deg2rad(sample(_fn, _bx[:, _c], _by[:, _c]) * args.rain_flow)
            _ang[:, _c] = np.deg2rad(r_ang0) + _o
        R_BX, R_BY = _bx, _by
        R_CDX = np.cos(_ang).astype(np.float32); R_CDY = np.sin(_ang).astype(np.float32)
        # WIND, NOT A GUN. A dash's track bows: lateral offset grows with the
        # square of arc distance, curvature drawn per dash with a random sign.
        # Straight rays make a radial fan you can read as a diagram; the
        # reference reads like rain in wind / willow in a breeze.
        R_CRV = (rng.standard_normal((rx.size, R_CYC)).astype(np.float32)
                 * (args.rain_bow / max(W, 1.0)))
        R_TRAVEL = np.float32(args.rain_px_per_sec * W * args.rain_life)
        print("rain: %d dashes, %d block-px, %d life-cycles of %.0fms, travel %.0f render-px/life"
              % (rx.size, R_IDX.size, R_CYC, args.rain_life * 1000, R_TRAVEL), file=sys.stderr)
    else:
        R_HUE = R_SPD = R_BX = R_BY = R_CDX = R_CDY = None
        R_CYC = 1; R_TRAVEL = np.float32(0.0); R_LEN = None

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

    if DIS is not None and args.escape > 0:
        _d = np.deg2rad([float(v) for v in args.dissolve.split(",")][0])
        ESC_X = np.float32(np.cos(_d)); ESC_Y = np.float32(np.sin(_d))
        ESC_W = sample(DIS, home_x, home_y) ** 1.5 * args.escape
        ESC_S = sample(SUBJ, home_x, home_y)
        ESC_LAT = (rng.standard_normal(n_particles).astype(np.float32) * 0.8)
        BRE_PH = (sample(DIS, home_x, home_y) * 2.6
                  + home_x / max(1, W) * 1.4).astype(np.float32)
    else:
        ESC_W = None

    # ---- E-2/E-3: the escape cloud is BORN, not flown ----
    # Measured on four works: an escaped mark lives 2-3 frames and moves 1-5 px
    # per frame, i.e. 0.02-0.10 S in its whole life. It cannot have travelled to
    # where the far field is. The far field is a BIRTH distribution: a near-field
    # exponential of e-folding 0.05-0.10 S plus a ~1/d tail out to ~0.9 S.
    # The old code flew every dissolved mark 0.22*W in one life -- 10-30x too far,
    # which is what turned "disintegrating" into "an even grey haze".
    ESC_OX = ESC_OY = None
    if ESC_W is not None and not args.escape_legacy and frames > 1 and DIS_S:
        D_CYC = max(1, int(round(args.seconds / max(args.dissolve_life, 1e-3))))
        _w01 = np.clip(ESC_W, 0, 1).astype(np.float32)
        _near = max(2.0, args.dissolve_near * DIS_S)
        _u = rng.random((D_CYC, n_particles)).astype(np.float32)
        _rmin = args.dissolve_min * DIS_S
        _r = (_rmin - _near * np.log(np.maximum(1e-6, 1.0 - _u))).astype(np.float32)
        if args.dissolve_tail > 0:
            _v = rng.random((D_CYC, n_particles)).astype(np.float32)
            _rt = np.minimum(_rmin + _near / np.maximum(1e-4, 1.0 - _v) ** 0.9, args.dissolve_reach * DIS_S)
            _pick = rng.random((D_CYC, n_particles)) < args.dissolve_tail
            _r = np.where(_pick, _rt, _r).astype(np.float32)
        if args.dissolve_floor > 0:
            # FLAT PLATEAU, NOT A TAIL. r ~ sqrt(u) puts marks at constant areal
            # density, so the far field holds a level instead of fading to black.
            _vu = rng.random((D_CYC, n_particles)).astype(np.float32)
            _rf = (_rmin + np.sqrt(_vu) * args.dissolve_reach * DIS_S).astype(np.float32)
            _pf = rng.random((D_CYC, n_particles)) < args.dissolve_floor
            _r = np.where(_pf, _rf, _r).astype(np.float32)
        # EROSION IS REAL. Measured on the reference: at equal depth the
        # dissolving side's core sits at 0.46x the intact side's fill, graded
        # from the boundary inward over 0.07-0.26 S. So a mark in the dissolve
        # zone is not "the same mark, slightly displaced" -- each cycle it is
        # either still part of the (thinned) solid or it is out in the cloud.
        # P(out) = DIS, which reproduces the 0.46x directly, and re-drawing it
        # every cycle IS the "dies here, reborn over there" that the survival
        # measurements imply.
        _pout = np.clip(np.clip(sample(DIS, home_x, home_y), 0, 1) * max(0.0, args.escape), 0, 1)
        if FIL is not None:
            # a mark that landed ON a filament belongs to it -- scattering it
            # again would dissolve the very structure we just drew
            _pout = _pout * (1.0 - np.clip(sample(FIL, home_x, home_y), 0, 1))
        _out = (rng.random((D_CYC, n_particles)) < _pout[None, :])
        _r = np.where(_out, _r, 0.0).astype(np.float32) * np.clip(_w01, 0, 1)[None, :]
        # angular spread around DEG: the measured escape mass has R = 0.4-0.68
        # about the dissolve axis, so it is a lobe, not a ray.
        _th = np.deg2rad(_d * 0 + 0.0) + (rng.standard_normal((D_CYC, n_particles))
                                          .astype(np.float32) * 0.55)
        _ca, _sa = np.cos(_th), np.sin(_th)
        _dx1 = (ESC_X * _ca - ESC_Y * _sa).astype(np.float32)
        _dy1 = (ESC_Y * _ca + ESC_X * _sa).astype(np.float32)
        if args.dissolve_strand > 0:
            # VEINS, NOT DUST. Walking the birth point along the image's own flow
            # field means marks that started as neighbours stay on one streamline
            # and touch, so the escaped material draws branching filaments -- the
            # thing that lets a broken-off part read as an EXTENSION of the form
            # rather than as debris. A straight ray can only make a haze.
            _kb = float(np.clip(args.dissolve_strand, 0, 1))
            _NS = 24
            _sx = np.repeat(home_x[None, :], D_CYC, 0).astype(np.float32)
            _sy = np.repeat(home_y[None, :], D_CYC, 0).astype(np.float32)
            _st = (_r / _NS).astype(np.float32)
            _bx = np.repeat(_dx1[:, :], 1, 0); _by = np.repeat(_dy1[:, :], 1, 0)
            for _k in range(_NS):
                _fu, _fv = sample(fx, _sx, _sy), sample(fy, _sx, _sy)
                _sg = np.where(_fu * _bx + _fv * _by < 0, -1.0, 1.0).astype(np.float32)
                _fu, _fv = _fu * _sg, _fv * _sg
                _ux = _fu * (1.0 - _kb) + _bx * _kb
                _uy = _fv * (1.0 - _kb) + _by * _kb
                if args.turbulence > 0:
                    _tu, _tv = sample(TRB_X, _sx, _sy), sample(TRB_Y, _sx, _sy)
                    _ux = _ux + _tu * args.turbulence * 0.35
                    _uy = _uy + _tv * args.turbulence * 0.35
                _un = np.hypot(_ux, _uy) + 1e-6
                _sx = _sx + _ux / _un * _st
                _sy = _sy + _uy / _un * _st
            ESC_SX, ESC_SY = _sx, _sy
        else:
            ESC_SX = ESC_SY = None
        if args.dissolve_keepout:
            # A SECOND ELEMENT NEEDS ITS OWN VOID. Ash drifting over the embers
            # kills the figure/ground the two of them make together, so any
            # offset that would land inside the ellipse is shortened until it
            # does not. Pulling BACK (rather than deleting) keeps the ink budget.
            _kp = [float(v) for v in args.dissolve_keepout.split(",")]
            _kx, _ky, _krx, _kry = _kp[0] * W, _kp[1] * H, _kp[2] * W, _kp[3] * H
            _kpad = _kp[4] if len(_kp) > 4 else 1.0
            _krx *= _kpad; _kry *= _kpad
            # per-mark radius jitter: a clean ellipse edge reads as a mask, and a
            # mask edge is the one thing this idiom must never show.
            _kj = (0.85 + 0.30 * rng.random((D_CYC, n_particles))).astype(np.float32)
            _ex = (ESC_SX - home_x[None, :]) if ESC_SX is not None else (_r * _dx1)
            _ey = (ESC_SY - home_y[None, :]) if ESC_SX is not None else (_r * _dy1)
            for _f in (1.0, 0.55, 0.30, 0.12, 0.0):
                _tx = home_x[None, :] + _ex * _f
                _ty = home_y[None, :] + _ey * _f
                _in = (((_tx - _kx) / max(_krx, 1e-3)) ** 2
                       + ((_ty - _ky) / max(_kry, 1e-3)) ** 2) < _kj ** 2
                if _f == 1.0:
                    _keep = np.where(_in, np.float32(0.0), np.float32(1.0))
                    _bad = _in
                else:
                    _keep = np.where(_bad & ~_in & (_keep == 0), np.float32(_f), _keep)
            if ESC_SX is not None:
                ESC_SX = home_x[None, :] + _ex * _keep
                ESC_SY = home_y[None, :] + _ey * _keep
            else:
                _r = (_r * _keep).astype(np.float32)
            print("dissolve keep-out: %.0f%% of escape offsets pulled back"
                  % (100.0 * (_keep < 1.0).mean()), file=sys.stderr)
        if ESC_SX is not None:
            ESC_OX = (ESC_SX - home_x[None, :]).astype(np.float32)
            ESC_OY = (ESC_SY - home_y[None, :]).astype(np.float32)
        else:
            ESC_OX = (_r * _dx1).astype(np.float32)
            ESC_OY = (_r * _dy1).astype(np.float32)
        D_PH = rng.random(n_particles).astype(np.float32)
        D_AR = np.arange(n_particles)
        print("dissolve escape: born, %d life-cycles of %.0fms, near %.0f px (%.3f S), "
              "tail %.0f%%, patch %.2f"
              % (D_CYC, args.dissolve_life * 1000, _near, args.dissolve_near,
                 100 * args.dissolve_tail, args.dissolve_patch), file=sys.stderr)
    else:
        D_CYC = 0

    # home-density grid for --conserve (constant across frames)
    CSV_CS = max(3, 3 * ss)
    if args.conserve > 0:
        _gh = int(H // CSV_CS) + 2; _gw = int(W // CSV_CS) + 2
        CSV_HOME = np.zeros((_gh, _gw), dtype=np.float32)
        if ESC_OX is not None:
            # THE ESCAPE RELOCATION IS INTENDED DENSITY, NOT ADVECTION PILE-UP.
            # Built from the un-offset homes, --conserve saw the dissolving core
            # thinning and helpfully brightened it back up -- cancelling the
            # erosion exactly. Home density is therefore the cycle-average of
            # where the marks actually live.
            for _c in range(D_CYC):
                np.add.at(CSV_HOME,
                          (np.clip((home_y + ESC_OY[_c]) // CSV_CS, 0, _gh - 1).astype(np.int64),
                           np.clip((home_x + ESC_OX[_c]) // CSV_CS, 0, _gw - 1).astype(np.int64)),
                          np.float32(1.0 / D_CYC))
        else:
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
            _sp = sample(SPD, x, y)
            x = np.where(live, x + u * travel * _sp, x)
            y = np.where(live, y + v * travel * _sp, y)

        if jit is not None:
            x = x + jit[t % life, :, 0]
            y = y + jit[t % life, :, 1]

        if ESC_OX is not None:
            # BORN, NOT FLOWN. Each dissolve-life the mark is re-seeded at a new
            # offset drawn from the near+tail distribution, then drifts a couple
            # of px before the next cycle re-seeds it. Cycle index is taken mod
            # D_CYC so the loop still closes exactly.
            _g = tt * D_CYC + D_PH
            _k = (np.floor(_g).astype(np.int64)) % D_CYC
            _uu = (_g - np.floor(_g)).astype(np.float32)
            _fu, _fv = sample(fx, x, y), sample(fy, x, y)
            _sg = np.where(_fu * ESC_X + _fv * ESC_Y < 0, -1.0, 1.0).astype(np.float32)
            _fu, _fv = _fu * _sg, _fv * _sg
            # E-5: direction is the global flow plus a SMALL constant push along
            # DEG -- not a progressive turn onto DEG. Measured: every distance
            # band shares one direction, and it sits 63-90 deg off the local
            # outward normal.
            _ux = _fu * 0.6 + ESC_X * 0.4
            _uy = _fv * 0.6 + ESC_Y * 0.4
            if args.turbulence > 0:
                _tx, _ty = sample(TRB_X, x, y), sample(TRB_Y, x, y)
                _ux = _ux + _tx * args.turbulence * 0.5
                _uy = _uy + _ty * args.turbulence * 0.5
            _un = np.hypot(_ux, _uy) + 1e-6
            _dr = (_uu * (0.006 * W)).astype(np.float32) * np.clip(ESC_W, 0, 1)
            x = x + ESC_OX[_k, D_AR] + (_ux / _un) * _dr
            y = y + ESC_OY[_k, D_AR] + (_uy / _un) * _dr
            # E-1: the reference ink is strictly binary -- four works, one grey
            # value each, zero mid-tones. Fading is a survival lottery, never a
            # reduced alpha. So no taper here; the mark is on or it is gone.
            _w01 = np.clip(ESC_W, 0, 1)
            alpha = np.where(_w01 > 0.15,
                             (alpha > 0.30).astype(np.float32), alpha).astype(np.float32)
        elif ESC_W is not None:
            # RADIATE OUTWARD: the dissolved marks really leave the form and
            # fade in the black, instead of describing its surface forever
            _prog = (age / max(1, life)).astype(np.float32)
            _d = ESC_W * _prog * (0.22 * W)
            # Ash peels off ALONG THE FORM first and only then turns to the escape
            # direction, wandering on a curl field on the way. A constant vector
            # made every mark march in parallel — that is what read as rigid.
            _fu, _fv = sample(fx, x, y), sample(fy, x, y)
            _sg = np.where(_fu * ESC_X + _fv * ESC_Y < 0, -1.0, 1.0).astype(np.float32)
            _fu, _fv = _fu * _sg, _fv * _sg
            _w = np.clip(_prog * 1.3, 0, 1) ** 0.8
            _ux = _fu * (1 - _w) + ESC_X * _w
            _uy = _fv * (1 - _w) + ESC_Y * _w
            if args.turbulence > 0:
                _tx, _ty = sample(TRB_X, x, y), sample(TRB_Y, x, y)
                _ux = _ux + _tx * args.turbulence * _prog * 0.9
                _uy = _uy + _ty * args.turbulence * _prog * 0.9
            _un = np.hypot(_ux, _uy) + 1e-6
            _sp = ESC_W * _prog * (0.06 * W) * ESC_LAT
            x = x + (_ux / _un) * _d - _uy / _un * _sp
            y = y + (_uy / _un) * _d + _ux / _un * _sp
            alpha = alpha * np.clip(1.0 - 1.6 * np.clip(_prog - 0.72, 0, 1) * ESC_W, 0, 1)
            if DIS_BREATH > 0:
                # the boundary is deliberately unstable: the transition band
                # opens and shuts across the loop instead of sitting still
                _band = np.clip(4.0 * ESC_W * (1.0 - np.clip(ESC_W, 0, 1)), 0, 1)
                alpha = alpha * np.clip(
                    1.0 - DIS_BREATH * _band *
                    (0.5 - 0.5 * np.cos(2 * np.pi * (tt + BRE_PH))), 0, 1)

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
            # P-4: phase runs over ONE LIFE, not the whole loop. The cycle index
            # wraps mod C, so a dash is reborn somewhere else with a new angle and
            # the loop still closes exactly at frame N.
            _g = tt * R_CYC + r_phase
            _k = (np.floor(_g).astype(np.int64)) % R_CYC
            _u = (_g - np.floor(_g)).astype(np.float32)
            _ar = np.arange(rx.size)
            _bx = R_BX[_ar, _k]; _by = R_BY[_ar, _k]
            _dx = R_CDX[_ar, _k]; _dy = R_CDY[_ar, _k]
            _adv = (_u * R_TRAVEL * R_SPD).astype(np.float32)
            _arc = R_S + _adv[R_IDX]
            _hx = _bx[R_IDX] + _dx[R_IDX] * _arc + R_OX
            _hy = _by[R_IDX] + _dy[R_IDX] * _arc + R_OY
            if args.rain_bow > 0:
                _cv = R_CRV[_ar, _k][R_IDX]
                _lat = _cv * _arc * _arc
                _hx = _hx - _dy[R_IDX] * _lat
                _hy = _hy + _dx[R_IDX] * _lat
            _env = sample(rain_zone, _hx, _hy).astype(np.float32)
            if KEEP is not None:
                _env = _env * sample(KEEP, _hx, _hy).astype(np.float32)
            #生灭突然：斜坡压到约一帧宽，不做长渐隐
            _fpl = max(2.0, args.fps * args.rain_life)
            _fade = np.clip(np.minimum(_u, 1.0 - _u) * _fpl, 0, 1).astype(np.float32)
            stamp(canvas, _hx, _hy, R_HUE, R_W * _env * _fade[R_IDX], 1)

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
            _mpf = (MASS_SEQ[int(tt * len(MASS_SEQ)) % len(MASS_SEQ)]
                    if 'MASS_SEQ' in dir() and MASS_SEQ else mass_plane)
            rgb = np.maximum(rgb, _mpf[:, :, None] * body[None, None, :])
        if ANCH_PLANE is not None:
            rgb = np.maximum(rgb, ANCH_PLANE * ANCH_RGB * 255.0)
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
