import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter as gf, label, distance_transform_edt, find_objects
f=sys.argv[1]
a=np.asarray(Image.open(f).convert('L'),dtype=np.float32)/255.
H,W=a.shape; lit=a>0.15
cell=8; hh,ww=H//cell,W//cell
fill=lit[:hh*cell,:ww*cell].reshape(hh,cell,ww,cell).mean(axis=(1,3))
sm=gf(fill,3); core=sm>np.percentile(sm[sm>0.005],85)
lab,n=label(core); sz=np.bincount(lab.ravel())[1:]
core=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>=60])
S=np.sqrt(max(core.sum(),1))*cell
d=(distance_transform_edt(~core)-distance_transform_edt(core))*cell
print(f"{f}: lit {lit.mean()*100:.2f}%  dense-core S={S:.0f}px")
print("   d/S band     fill    rel     ARTIST")
ART={(-0.3,0.0):1.00,(0.0,0.1):0.31,(0.1,0.25):0.15,(0.25,0.5):0.11,(0.5,0.9):0.10,(0.9,1.6):0.12,(1.6,3.0):0.31}
base=None
for k in [(-0.3,0.0),(0.0,0.1),(0.1,0.25),(0.25,0.5),(0.5,0.9),(0.9,1.6),(1.6,3.0)]:
    m=(d>=k[0]*S)&(d<k[1]*S)
    if m.sum()<80: continue
    v=fill[m].mean()
    if base is None: base=v
    print(f"  {k[0]:+.2f}~{k[1]:+.2f}   {v:.4f}   {v/base:.2f}    {ART[k]:.2f}")
lab2,_=label(lit,structure=np.ones((3,3)))
objs=np.bincount(lab2.ravel())[1:]; sl=find_objects(lab2)
ln=[max(s[0].stop-s[0].start,s[1].stop-s[1].start) for i,s in enumerate(sl) if objs[i]>=6]
ln=np.array(ln)
print(f"  strands: median {np.median(ln)/S:.3f} S   p99 {np.percentile(ln,99)/S:.2f} S   max {ln.max()/S:.2f} S")
print(f"  ARTIST : median 0.017 S       p99 0.10 S        max 0.35 S")
