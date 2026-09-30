import numpy as np
from PIL import Image
from scipy import ndimage as ndi

PAL = {'orange':(247,147,30),'purple':(160,120,220),'yellow':(255,214,79),'green':(124,197,118),
       'pink':(248,165,194),'sky':(210,196,255),'white':(255,255,255),'grey':(235,235,245),'mint':(170,225,200)}

def colorize(img, big=None, seed=0):
    """Fill closed white regions of line art with a Halloween palette. Returns RGB image."""
    g = np.array(img.convert('L'))
    line = g < 150
    free = ~ndi.binary_dilation(line, iterations=1)
    lab, n = ndi.label(free)
    areas = ndi.sum(np.ones_like(lab), lab, index=np.arange(1, n+1))
    H, W = g.shape
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    out = np.array(img.convert('RGB')).copy()
    rng = np.random.default_rng(seed)
    order = np.argsort(-areas)
    big = [PAL[b] for b in (big or ['orange','purple','green','yellow'])]
    cy = ndi.center_of_mass(np.ones_like(lab), lab, index=np.arange(1, n+1))
    small = [PAL['yellow'], PAL['pink'], PAL['orange'], PAL['mint'], PAL['purple']]
    bi = 0
    colors = np.zeros((n+1, 3), dtype=np.uint8)
    for idx in order:
        r = idx + 1; a = areas[idx]
        if r in border:
            c = None
        elif cy[idx][0] > 0.855*H:
            c = None
        elif a > 0.25*H*W:
            c = PAL['sky']
        elif a < 150:
            c = None
        elif a > 0.02*H*W:
            c = big[bi % len(big)]; bi += 1
        else:
            c = small[rng.integers(len(small))]
        if c is not None:
            colors[r] = c
    mask = colors[lab].any(axis=-1) & (lab > 0)
    out[mask] = colors[lab][mask]
    # soften: fill the dilation gap between color and line with neighbor color
    return Image.fromarray(out)
