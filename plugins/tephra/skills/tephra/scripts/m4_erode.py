"""Non-self-referential erosion check.
Bins the RENDER's fill by the ramp value computed from the SOURCE (deterministic,
no noise, independent of the render) -- so the metric cannot manufacture the
structure it is testing. Reports fill vs ramp inside the source subject mask.
usage: m4_erode.py src.png render.png DEG START SOFT FLOOR [--invert]
"""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter as gf
src, ren = sys.argv[1], sys.argv[2]
deg, start, soft, floor = map(float, sys.argv[3:7])
inv = '--invert' in sys.argv
R = np.asarray(Image.open(ren).convert('L'), dtype=np.float32)/255.
H,W = R.shape
g = np.asarray(Image.open(src).convert('L').resize((W,H), Image.LANCZOS), dtype=np.float32)/255.
if inv: g = 1.-g
lo,hi = np.percentile(g,2), np.percentile(g,99.5); g = np.clip((g-lo)/max(1e-6,hi-lo),0,1)
g8 = gf(g,8); SUBJ = np.clip((g8-np.percentile(g8,55))/max(1e-6,np.percentile(g8,97)-np.percentile(g8,55)),0,1)
yy,xx = np.mgrid[0:H,0:W].astype(np.float32)
ax,ay = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
t = xx/W*ax + yy/H*ay
sel = SUBJ>0.25
t = (t-np.percentile(t[sel],2))/max(1e-6, np.percentile(t[sel],98)-np.percentile(t[sel],2))
ramp = np.clip((t-start)/soft, 0, 1)
ink = g > floor                                     # source-defined solid, not render-defined
lit = R > 0.15
print(f"{ren}   subject px {ink.sum()/ink.size*100:.1f}% of canvas")
print("   ramp band     area%   fill     rel")
base=None
for a,b in [(0,.05),(.05,.2),(.2,.4),(.4,.6),(.6,.8),(.8,1.01)]:
    m = ink & (ramp>=a) & (ramp<b)
    if m.sum()<500: print(f"  {a:.2f}-{b:.2f}      (thin)"); continue
    f = lit[m].mean()
    if base is None: base=f
    print(f"  {a:.2f}-{b:.2f}    {m.sum()/ink.sum()*100:5.1f}   {f:.3f}   {f/base:.2f}")
print(f"  ref: fill at ramp>0.8 should be ~0.46x of ramp<0.05")
