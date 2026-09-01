"""M0.5 P4 for the statue: the ear and the smoke sit at the SAME luminance
(both median 0.055) -- no --floor can separate them. Local contrast can:
ear grooves p95 0.091 vs smooth smoke 0.026, a 3.5x gap.

The documented trap: texture energy used AS the form gives a wireframe. So the
texture only builds a REGION MASK (close -> fill -> smooth); the form inside it
comes back from the source's own luminance. Embers are kept separately: they are
small, bright and saturated, and would fail any texture test.
"""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import (uniform_filter, gaussian_filter as gf, binary_closing,
                           binary_fill_holes, label)
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB'), dtype=np.float32)/255.
g  = np.asarray(Image.open(src).convert('L'),  dtype=np.float32)/255.
H, W = g.shape
w = max(5, int(round(W*0.006)) | 1)
m1 = uniform_filter(g, w); m2 = uniform_filter(g*g, w)
C = np.sqrt(np.maximum(m2 - m1*m1, 0))
Cs = gf(C, W*0.004)
t = float(np.percentile(Cs, 88))
mask = Cs > t
mask = binary_closing(mask, np.ones((int(W*0.012)|1,)*2))
mask = binary_fill_holes(mask)
lab, n = label(mask); sz = np.bincount(lab.ravel())[1:]
if n: mask = lab == (1 + int(np.argmax(sz)))
soft = np.clip(gf(mask.astype(np.float32), W*0.006)*1.6 - 0.3, 0, 1)
keep_embers = '--embers' in sys.argv
if keep_embers:
    mx = im.max(2); mn = im.min(2); sat = (mx-mn)/np.maximum(mx, 1e-6)
    ember = ((mx > 0.42) & (sat > 0.42)).astype(np.float32)
    ember = np.clip(gf(ember, 2)*3.0, 0, 1)
else:
    ember = np.zeros_like(soft)
keep = np.clip(soft + ember, 0, 1)[..., None]
res = np.clip(im*keep, 0, 1)
Image.fromarray((res*255).astype(np.uint8)).save(out)
gg = res.mean(2)
print(f"mask covers {mask.mean()*100:.1f}% of canvas   contrast threshold {t:.4f}")
for nm, b in [("ear", (0.30,0.375,0.62,0.80)), ("smoke", (0.80,0.98,0.30,0.60)),
              ("face", (0.36,0.50,0.60,0.78))]:
    r = gg[int(b[2]*H):int(b[3]*H), int(b[0]*W):int(b[1]*W)]
    print(f"  {nm:6s} median {np.median(r):.4f}")
