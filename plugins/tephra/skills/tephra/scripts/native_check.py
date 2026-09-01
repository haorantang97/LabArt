"""Score a native-grid render against the measured target profile (sample A)."""
import sys, numpy as np
from PIL import Image, ImageSequence
from scipy.ndimage import label
f=sys.argv[1]
fr=[np.asarray(im.convert('L'),np.uint8) for im in ImageSequence.Iterator(Image.open(f))]
A=np.stack(fr); n,H,W=A.shape
lit=A>40
per=lit.mean(0); solid=per>=0.80
d0=lit[0]&~solid
lab,_=label(d0,np.ones((3,3))); sz=np.bincount(lab.ravel())[1:]
sz=np.sort(sz)
def q(p): return int(sz[min(len(sz)-1,int(p*len(sz)))]) if len(sz) else 0
s1=(lit[0]&lit[1])[solid].mean() if solid.any() else 0
best=(-1,0,0)
for dy in range(-4,5):
    for dx in range(-4,5):
        b=np.roll(np.roll(d0,dy,0),dx,1)
        sc=(lit[1]&~solid)[b].mean() if b.any() else 0
        if sc>best[0]: best=(sc,dx,dy)
print(f"{f}  grid {W}x{H}  frames {n}")
print(f"  lit          {lit[0].mean()*100:5.2f}%   REF 10.21%")
print(f"  solid        {solid.mean()*100:5.2f}%   REF  8.18%")
print(f"  debris       {d0.mean()*100:5.2f}%   REF  2.03%")
print(f"  pieces       {len(sz):5d}     REF  1101")
print(f"  piece area   med {q(.5)}  p90 {q(.9)}  p99 {q(.99)}  max {sz[-1] if len(sz) else 0}   REF med 2 / p90 8 / p99 25 / max 36")
print(f"  solid static {s1:.3f}      REF 1.000")
print(f"  debris drift {best[1]},{best[2]}  match {best[0]:.3f}   REF +1,+1 match 0.387 (61%/frame die)")
