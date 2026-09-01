"""M4 verification: escape-cloud profile, both sides of the dissolve axis.
Targets from PROPOSALS_EDGE (4 works measured):
  intact side  : fill <0.008 beyond 0.05 S  (vacuum cliff)
  dissolve side: near-field e-fold 0.05-0.12 S ; fill(0.5S)/near-peak 0.15-0.35
  core         : dissolved-side fill / intact-side fill at equal depth ~0.46
  islands      : core splits into >=2 components; roughness 2.3-6.0
"""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt, label, binary_closing

png, deg = sys.argv[1], float(sys.argv[2])
a = np.asarray(Image.open(png).convert('L'), dtype=np.float32)/255.
H,W = a.shape
lit = a > 0.15
cell = 4
hh,ww = H//cell, W//cell
fill = lit[:hh*cell,:ww*cell].reshape(hh,cell,ww,cell).mean(axis=(1,3))
core = gaussian_filter(fill,1.0) > 0.14
core = binary_closing(core, np.ones((3,3)))
lab,n = label(core)
sizes = np.bincount(lab.ravel())[1:]
keep = [i+1 for i,s in enumerate(sizes) if s>=100]
core = np.isin(lab, keep)
if core.sum()==0: print("no core"); sys.exit()
S = np.sqrt(core.sum())*cell          # subject size in image px
d = (distance_transform_edt(~core) - distance_transform_edt(core))*cell
yy,xx = np.mgrid[0:hh,0:ww]
cy,cx = yy[core].mean(), xx[core].mean()
ax,ay = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
proj = (xx-cx)*ax + (yy-cy)*ay
side = proj > 0                        # dissolve side
print(f"{png}: S={S:.0f}px  core cells={core.sum()}  components={len(keep)}")
per = np.abs(np.diff(core.astype(int),axis=0)).sum()+np.abs(np.diff(core.astype(int),axis=1)).sum()
print(f"  roughness = {per/(2*np.sqrt(np.pi*core.sum())):.2f}   (smooth circle ~1.3, ref 2.3-6.0)")
bins=[(-0.30,-0.18),(-0.18,-0.10),(-0.10,-0.04),(-0.04,0.0),
      (0.0,0.03),(0.03,0.07),(0.07,0.14),(0.14,0.25),(0.25,0.45),(0.45,0.75),(0.75,1.2)]
# 样本A, dissolve side, resampled onto these bins (S=183 native px)
REF={0.015:0.19,0.05:0.085,0.105:0.052,0.195:0.035,0.35:0.026,0.60:0.009,0.975:0.003}
print("   d/S      intact     dissolve    ref")
prof={}
for lo,hi in bins:
    m=(d>=lo*S)&(d<hi*S)
    A=fill[m&~side]; B=fill[m&side]
    va=A.mean() if A.size>20 else float('nan'); vb=B.mean() if B.size>20 else float('nan')
    prof[(lo+hi)/2]=(va,vb)
    mid=(lo+hi)/2
    r = REF.get(round(mid,3))
    rs = f"{r:8.4f}" if r else "        "
    flag = ""
    if r and vb==vb:
        q = vb/r
        flag = "  <-- %.1fx" % q if (q>1.8 or q<0.55) else ""
    print(f"  {lo:+.2f}~{hi:+.2f}  {va:8.4f}   {vb:8.4f} {rs}{flag}")
# key numbers
def g(k,i):
    return prof[k][i]
try:
    ci = np.nanmean([g(k,0) for k in prof if k<-0.05]); cd = np.nanmean([g(k,1) for k in prof if k<-0.05])
    print(f"  core fill  intact {ci:.3f} / dissolve {cd:.3f}  ratio {cd/ci:.2f}  (ref 0.46)")
except Exception as e: print(e)
outside=[k for k in prof if k>0.02]
pk = prof[min(outside)][1]
far = [prof[k][1] for k in prof if 0.4<k<0.6]
print(f"  intact side beyond 0.05S: {np.nanmean([prof[k][0] for k in prof if k>0.05]):.4f}  (ref <0.008)")
if far: print(f"  dissolve fill(0.5S)/near-peak = {far[0]/max(pk,1e-6):.2f}  (ref 0.15-0.35)")
