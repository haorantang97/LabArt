#!/usr/bin/env python3
"""tephra 输入体检。用法: python3 dp_fitness.py img.png [--invert]

两个数决定成败：
  中位亮度 med —— 这张图自带多少虚空。低 = 不用我编。
  可分离性 sep —— 一个亮度阈值能把主体和背景分多开。高 = 该删哪儿由图决定，不由我猜。
判据：med < 0.20 直接过；否则要 sep > 0.55（删得多，但图指明了删哪儿）。
"""
import sys, numpy as np
from PIL import Image

def check(path, invert=False):
    im = Image.open(path).convert("L")
    W = 1400; H = max(1, round(im.height / im.width * W))
    a = np.asarray(im.resize((W, H), Image.LANCZOS), dtype=np.float32) / 255
    lo, hi = np.percentile(a, 2), np.percentile(a, 99.5)
    a = np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1)
    if invert: a = 1 - a

    med  = float(np.median(a))
    void = float((a < 0.06).mean())
    h, _ = np.histogram(a, 256, (0, 1)); h = h / h.sum(); b = (np.arange(256) + .5) / 256
    w0 = np.cumsum(h); w1 = 1 - w0; c = np.cumsum(h * b); tot = c[-1]
    m0 = c / np.maximum(w0, 1e-9); m1 = (tot - c) / np.maximum(w1, 1e-9)
    k = int(np.argmax(w0 * w1 * (m0 - m1) ** 2))
    sep = float(m1[k] - m0[k]); thr = float(b[k])
    area = float((a > thr).mean())

    if med < 0.20:      ok, why = True,  "虚空是图自带的"
    elif sep > 0.55:    ok, why = True,  "虚空要删，但可分离性够高，删哪儿由图决定"
    else:               ok, why = False, "虚空要大量删，而图又分不开主体和背景 —— 成品会是臆想"
    print(f"  中位亮度   {med:.3f}  (天然虚空 {void:.1%})")
    print(f"  可分离性   {sep:.3f}  (最佳阈值 {thr:.2f}，主体占比 {area:.1%})")
    print(f"  => {'可以渲' if ok else '不建议硬渲'}：{why}")
    if ok: print(f"     --floor 起点建议 {thr:.2f}")
    return ok

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("-")]
    check(a[0], "--invert" in sys.argv)

def fidelity(orig, cand):
    """重打光后有没有偷改几何：比两张图的边缘位置相关性。
    >0.60 = 只动了明暗；<0.40 = 模型重画了内容，不能用。"""
    import scipy.ndimage as nd
    def edges(p):
        im = Image.open(p).convert("L").resize((900, 500), Image.LANCZOS)
        a = np.asarray(im, dtype=np.float32) / 255
        gy, gx = np.gradient(nd.gaussian_filter(a, 2))
        e = np.hypot(gx, gy)
        return (e - e.mean()) / (e.std() + 1e-9)
    A, B = edges(orig), edges(cand)
    r = float((A * B).mean())
    print(f"  结构保真度 {r:.3f}  {'OK 只动了明暗' if r > 0.60 else ('可疑' if r > 0.40 else 'FAIL 模型重画了内容')}")
    return r
