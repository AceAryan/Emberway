"""Tiny pixel-drawing helpers on top of Pillow (no anti-aliasing, ever)."""
from PIL import Image

from palette import CLEAR, OUTLINE


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), CLEAR)
        self.px = self.img.load()

    def set(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[x, y] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[x, y]
        return CLEAR

    def rect(self, x0, y0, x1, y1, c):
        """Filled rectangle, inclusive corners."""
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                self.set(x, y, c)

    def line(self, x0, y0, x1, y1, c, width=1):
        """Bresenham line stamped with a width x width square."""
        x0, y0, x1, y1 = map(lambda v: int(round(v)), (x0, y0, x1, y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        off = (width - 1) // 2
        while True:
            for oy in range(width):
                for ox in range(width):
                    self.set(x0 - off + ox, y0 - off + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def poly(self, pts, c):
        """Scanline polygon fill (even-odd), pixel centres."""
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            yc = y + 0.5
            xs = []
            n = len(pts)
            for i in range(n):
                (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
                if (ya <= yc < yb) or (yb <= yc < ya):
                    xs.append(xa + (yc - ya) * (xb - xa) / (yb - ya))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1]))):
                    self.set(x, y, c)

    def stamp(self, rows, x0, y0, colors):
        """Draw an ASCII template. '.' = skip; other chars are looked up in `colors`."""
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch != ".":
                    self.set(x0 + dx, y0 + dy, colors[ch])

    def composite(self, other):
        """Paste another canvas on top (alpha)."""
        self.img.alpha_composite(other.img)
        self.px = self.img.load()

    def outline(self, color=OUTLINE):
        """Add a 1px outline around every opaque pixel (4-neighbourhood)."""
        src = self.img.copy().load()
        for y in range(self.h):
            for x in range(self.w):
                if src[x, y][3] != 0:
                    continue
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < self.w and 0 <= ny < self.h and src[nx, ny][3] != 0 and src[nx, ny] != color:
                        self.px[x, y] = color
                        break


def sheet(frames):
    """Lay frames out horizontally into one sprite sheet."""
    w, h = frames[0].w, frames[0].h
    out = Image.new("RGBA", (w * len(frames), h), CLEAR)
    for i, f in enumerate(frames):
        out.paste(f.img, (i * w, 0))
    return out


def preview(img, scale=8, bg=(236, 226, 205, 255)):
    """Upscaled preview on a warm background, for checking art by eye."""
    big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    base = Image.new("RGBA", big.size, bg)
    base.alpha_composite(big)
    return base
