import sys
from PIL import Image, ImageSequence
src, dst, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src)
if src.lower().endswith('.gif'):
    fr=[f.convert('RGB').resize((W, round(W*f.height/f.width)), Image.NEAREST)
        for f in ImageSequence.Iterator(im)]
    fr[0].save(dst, save_all=True, append_images=fr[1:], loop=0,
               duration=im.info.get('duration',40), disposal=2, optimize=True)
else:
    im.convert('RGB').resize((W, round(W*im.height/im.width)), Image.NEAREST).save(dst)
print("wrote", dst)
