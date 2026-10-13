"""SVG scatter planes for the performance space (S, c, q)."""
from common import SANS, MONO

TXT = f"font-family: {SANS}"
W, H, ML, MT, PW, PH = 640, 520, 64, 20, 552, 440

from common import v


def _methods():
    """Semantic family; GES and FCI on the scenarios where they run (analysis/results/space)."""
    return {lab: tuple(v("m.%s.%s" % (k, c)) for c in ("S", "c", "q", "a"))
            for lab, k in (("PC", "PC"), ("GES*", "GES"), ("FCI*", "FCI"), ("LiNGAM", "LiNGAM"), ("NOTEARS", "NOTEARS"))}


def _cc():
    """Causal-Copilot, mean over the 10 S2 runs per arm: (stage, S, c, q, a). Stages equal to the previous one are dropped."""
    out = {}
    for role in ("real", "neutral", "swapped"):
        pts = []
        for st in ("S0", "S1", "S2", "S3"):
            p = (st,) + tuple(v("cc.%s.%s.%s" % (role, st, c)) for c in ("S", "c", "q", "a"))
            if pts and all(abs(a - b) < 0.012 for a, b in zip(p[1:], pts[-1][1:])):
                continue
            pts.append(p)
        out[role] = pts
    return out


CCCOL = {"real": "#B85A12", "neutral": "#6A716B", "swapped": "#8E2A2A"}
BLUE = "#1D5C99"


class Plane:
    def __init__(self, x0, x1, y0, y1, xlabel, ylabel, uid):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.xl, self.yl, self.uid = xlabel, ylabel, uid
        self.items = []

    def px(self, x):
        return ML + (x - self.x0) / (self.x1 - self.x0) * PW

    def py(self, y):
        return MT + (self.y1 - y) / (self.y1 - self.y0) * PH

    def add(self, s):
        self.items.append(s)

    def frame(self, xticks, yticks):
        out = []
        for t in xticks:
            x = self.px(t)
            out.append(f'<line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{MT + PH}" stroke="#ECEEE9" stroke-width="1"/>')
            out.append(f'<text x="{x:.1f}" y="{MT + PH + 18}" text-anchor="middle" font-size="12" fill="#4E5751" style="font-family: {MONO}">{t:g}</text>')
        for t in yticks:
            y = self.py(t)
            out.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{ML + PW}" y2="{y:.1f}" stroke="#ECEEE9" stroke-width="1"/>')
            out.append(f'<text x="{ML - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="12" fill="#4E5751" style="font-family: {MONO}">{t:g}</text>')
        out.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" stroke="#6A716B" stroke-width="1"/>')
        out.append(f'<text x="{ML + PW/2}" y="{MT + PH + 42}" text-anchor="middle" font-size="13" font-weight="600" fill="#17201B" style="{TXT}">{self.xl}</text>')
        out.append(f'<text x="16" y="{MT + PH/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#17201B" transform="rotate(-90 16 {MT + PH/2})" style="{TXT}">{self.yl}</text>')
        return out

    def curve(self, pts, colour, width=1.5, dash=""):
        d = " ".join(f"{'M' if i == 0 else 'L'} {self.px(x):.1f} {self.py(y):.1f}" for i, (x, y) in enumerate(pts))
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}"{da}/>')

    def area(self, pts, fill):
        d = " ".join(f"{'M' if i == 0 else 'L'} {self.px(x):.1f} {self.py(y):.1f}" for i, (x, y) in enumerate(pts)) + " Z"
        self.add(f'<path d="{d}" fill="{fill}" stroke="none"/>')

    def label(self, x, y, text, colour="#17201B", dx=8, dy=4, anchor="start", size=12, weight="400"):
        self.add(f'<text x="{self.px(x) + dx:.1f}" y="{self.py(y) + dy:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{colour}" style="{TXT}">{text}</text>')

    def dot(self, x, y, colour, r=5, hollow=False):
        f = "#FFFFFF" if hollow else colour
        self.add(f'<circle cx="{self.px(x):.1f}" cy="{self.py(y):.1f}" r="{r}" fill="{f}" stroke="{colour}" stroke-width="2"/>')

    def star(self, x, y, colour="#17201B"):
        cx, cy = self.px(x), self.py(y)
        self.add(f'<path d="M {cx} {cy-8} L {cx+2.6} {cy-2.6} L {cx+8} {cy-2.4} L {cx+3.6} {cy+1.6} L {cx+5} {cy+7.6} L {cx} {cy+4} L {cx-5} {cy+7.6} L {cx-3.6} {cy+1.6} L {cx-8} {cy-2.4} L {cx-2.6} {cy-2.6} Z" fill="{colour}"/>')

    def path_arrows(self, pts, colour, k):
        d = " ".join(f"{'M' if i == 0 else 'L'} {self.px(x):.1f} {self.py(y):.1f}" for i, (x, y) in enumerate(pts))
        self.add(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2" marker-mid="url(#{self.uid}m{k})" marker-end="url(#{self.uid}m{k})"/>')

    def svg(self, xticks, yticks, aria):
        defs = "".join(f'<marker id="{self.uid}m{k}" orient="auto" markerWidth="7" markerHeight="7" refX="6" refY="3.5"><path d="M0 0 L7 3.5 L0 7 Z" fill="{c}"/></marker>' for k, c in CCCOL.items())
        return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><defs>{defs}</defs>'
                + "".join(self.frame(xticks, yticks)) + "".join(self.items) + "</svg>")


def plane_Sa():
    METHODS, CC = _methods(), _cc()
    p = Plane(0, 1, 0.3, 1.0, "S · skeleton F1", "a · direction accuracy", "sa")
    # region beating the best published score
    F = v("pub.sem.D.best")
    PCF, LIM, LIMI, K = v("pc.F1"), v("lim.sem.D"), v("lim.sem.DI"), v("kappa.sem.D")
    pts = [(F / a, a) for a in [1.0 - i * (1.0 - F) / 40 for i in range(41)]]
    p.area(pts + [(1, F), (1, 1.0)], "#E8F3EC")
    for f, col, lab in ((0.2, "#C9CEC6", "F1 0.20"), (PCF, "#9AA39C", "F1 %.3f (PC)" % PCF), (F, "#2E7D4F", "F1 %.3f best published" % F)):
        lo = f
        hi = min(1.0, f / 0.3)
        c = [(lo + (hi - lo) * i / 60, 0) for i in range(61)]
        c = [(s, f / s) for s, _ in c if f / s <= 1.0 and f / s >= 0.3]
        p.curve(c, col, 1.5 if f != F else 2)
        if f == F:
            p.label(0.99, f / 0.99, lab, col, dx=-4, dy=-6, anchor="end", size=11)
        else:
            p.label(f / 0.86, 0.86, lab, col, dx=6, dy=0, anchor="start", size=11)
    p.curve([(0, 0.5), (1, 0.5)], "#9AA39C", 1.2, "4 4")
    p.label(0.02, 0.5, "a = 0.5: a coin", "#4E5751", dx=0, dy=-6, size=11)
    p.curve([(0, LIM), (1, LIM)], "#17201B", 1.2, "6 3")
    p.label(0.02, LIM, "limit on a with data alone: %.3f (D+I ≥ %.3f; D+K right: 1.000)" % (LIM, LIMI), "#17201B", dx=0, dy=-6, size=11)
    p.star(1.0, LIM)
    p.label(1.0, LIM, "D limit", "#17201B", dx=-10, dy=18, anchor="end", size=11, weight="600")
    for k, pts in CC.items():
        p.path_arrows([(s[1], s[4]) for s in pts], CCCOL[k], k)
        p.dot(pts[0][1], pts[0][4], CCCOL[k], 4, hollow=True)
    r0 = CC["real"][0]
    p.label(r0[1], r0[4], "S0 (FCI)", "#4E5751", dx=10, dy=-14, size=11)
    p.label(CC["real"][1][1], CC["real"][1][4], "S1 bootstrap", "#4E5751", dx=-8, dy=-12, anchor="end", size=11)
    p.label(CC["real"][-1][1], CC["real"][-1][4], "real, after model", CCCOL["real"], dx=-4, dy=24, anchor="middle", size=11, weight="600")
    p.label(CC["neutral"][-1][1], CC["neutral"][-1][4], "neutral: model changes nothing", CCCOL["neutral"], dx=8, dy=-2, size=11, weight="600")
    p.label(CC["swapped"][-1][1], CC["swapped"][-1][4], "swapped", CCCOL["swapped"], dx=-8, dy=14, anchor="end", size=11, weight="600")
    for name, (S, c, q, a) in METHODS.items():
        p.dot(S, a, BLUE)
        off = {"PC": (8, 14), "GES*": (8, -6), "FCI*": (8, -6), "LiNGAM": (-8, -8), "NOTEARS": (-8, 14)}[name]
        p.label(S, a, name, BLUE, dx=off[0], dy=off[1], anchor="start" if off[0] > 0 else "end", size=12, weight="600")
    return p.svg([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                 "Skeleton F1 against direction accuracy, with curves of equal directed F1")


def plane_cq():
    METHODS, CC = _methods(), _cc()
    p = Plane(0, 1, 0.35, 1.0, "c · commit rate", "q · commit accuracy", "cq")
    p.area([(0, 0.35), (1, 0.35), (1, 0.5), (0, 0.5)], "#F6E7E7")
    p.label(0.98, 0.37, "below a coin: committing costs points", "#8E2A2A", dx=0, dy=-4, anchor="end", size=11)
    p.curve([(0, 0.5), (1, 0.5)], "#8E2A2A", 1.2, "4 4")
    LIM, K = v("lim.sem.D"), v("kappa.sem.D")
    for a in (0.55, 0.65, 0.75, 0.85, LIM):
        lo = 2 * a - 1
        pts = [(lo + (1 - lo) * i / 60, 0) for i in range(61)]
        pts = [(c, 0.5 + (a - 0.5) / c) for c, _ in pts if c > 0]
        pts = [(c, q) for c, q in pts if q <= 1.0]
        p.curve(pts, "#17201B" if a == LIM else "#C9CEC6", 1.5 if a == LIM else 1.2, "6 3" if a == LIM else "")
        p.label(0.99, 0.5 + (a - 0.5), "a = %.3g" % a, "#17201B" if a == LIM else "#6A716B", dx=0, dy=-5, anchor="end", size=11)
    p.star(K, 1.0)
    p.label(K, 1.0, "D limit: commit the compelled %.1f%%, all right" % (100 * K), "#17201B", dx=-10, dy=16, anchor="end", size=11, weight="600")
    for k, pts in CC.items():
        p.path_arrows([(s[2], s[3]) for s in pts], CCCOL[k], k)
        p.dot(pts[0][2], pts[0][3], CCCOL[k], 4, hollow=True)
    p.label(CC["real"][0][2], CC["real"][0][3], "S0 (FCI)", "#4E5751", dx=-10, dy=4, anchor="end", size=11)
    p.label(CC["real"][1][2], CC["real"][1][3], "S1", "#4E5751", dx=0, dy=-12, size=11)
    p.label(CC["real"][-1][2], CC["real"][-1][3], "real", CCCOL["real"], dx=8, dy=4, size=11, weight="600")
    p.label(CC["swapped"][-1][2], CC["swapped"][-1][3], "swapped", CCCOL["swapped"], dx=-8, dy=16, anchor="end", size=11, weight="600")
    for name, (S, c, q, a) in METHODS.items():
        p.dot(c, q, BLUE)
        off = {"PC": (-8, 16), "GES*": (-8, -8), "FCI*": (8, 16), "LiNGAM": (-8, -6), "NOTEARS": (-8, 4)}[name]
        p.label(c, q, name, BLUE, dx=off[0], dy=off[1], anchor="start" if off[0] > 0 else "end", size=12, weight="600")
    return p.svg([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                 "Commit rate against commit accuracy, with curves of equal direction accuracy")
