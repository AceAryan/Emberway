"""Mira, the heroine: pose-driven pixel-art generator.

Frame: 32x48 px, 32 PPU, pivot at frame centre (matches the Player's CapsuleCollider2D 0.9x0.9).
Feet rest on row 38, which is exactly the collider's bottom edge.
Faces RIGHT; Unity mirrors her by flipping transform.localScale.x.

Design: white bob with teal tips, yellow open-front robe-jacket over a charcoal undershirt,
red-brown sash, dark trousers, brown boots. Unarmed at the start (palm strike).
"""
from palette import (BOOT, BOOT_SHADE, EMBER, EYE, HAIR, HAIR_SHADE, HAIR_TIP, INNER, PANTS,
                     PANTS_SHADE, ROBE, ROBE_LIGHT, ROBE_SHADE, SASH, SKIN, SKIN_SHADE, SPARK)
from pixel import Canvas

W, H = 32, 48
CX = 15        # body centre column
FOOT = 38      # bottom row of the boots (ground contact)

ARM_DOWN_BACK = ((-1, 3), (-1, 6))
ARM_DOWN_FRONT = ((1, 3), (1, 6))

# Head template, 11x11, facing right. H hair, h hair shade, T teal tip, S skin, s skin shade, E eye.
HEAD = [
    "...HHHHH...",
    "..HHHHHHHH.",
    ".HHHHHHHHHH",
    ".hHHHHHHHHH",
    ".hHHHHhSHhS",
    ".hHHHHSSESS",
    ".hHHHHSSESS",
    ".hHHHHSSSSs",
    ".hhHHhSSSs.",
    ".TTTh.Sss..",
    ".T.T.......",
]
HEAD_HAIR_UP = HEAD[:9] + [".hhHhhSss..", "..........."]
HEAD_COLORS = {"H": HAIR, "h": HAIR_SHADE, "T": HAIR_TIP, "S": SKIN, "s": SKIN_SHADE, "E": EYE}


def draw(p):
    c = Canvas(W, H)
    by = p.get("by", 0)          # body bob (+ = down)
    lean = p.get("lean", 0)      # upper-body forward offset
    sway = p.get("sway", 0)      # robe hem offset (- = trails behind)
    hs = p.get("hair", 0)        # hair trailing amount
    hair_up = p.get("hair_up", False)
    hip_y = 31 + by

    # ---- legs (drawn first, robe covers the tops) ----
    def leg(hip_x, foot, back):
        fx, fy = foot
        c.line(hip_x, hip_y, fx, fy - 2, PANTS_SHADE if back else PANTS, 2)
        c.rect(fx, fy - 1, fx + 2, fy, BOOT_SHADE if back else BOOT)

    leg(CX - 2 + lean, p.get("back_foot", (CX - 3, FOOT)), True)
    leg(CX + 1 + lean, p.get("front_foot", (CX + 1, FOOT)), False)

    sh_back = (CX - 2 + lean, 21 + by)
    sh_front = (CX + 2 + lean, 21 + by)

    def arm(target, sh, pose, back):
        (ex, ey), (hx, hy) = pose
        elbow = (sh[0] + ex, sh[1] + ey)
        hand = (sh[0] + hx, sh[1] + hy)
        col = ROBE_SHADE if back else ROBE
        target.line(*sh, *elbow, col, 2)
        target.line(*elbow, *hand, col, 2)
        target.set(sh[0], sh[1], ROBE_LIGHT if not back else col)
        target.rect(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN_SHADE if back else SKIN)

    # ---- back arm (behind the body) ----
    arm(c, sh_back, p.get("back_arm", ARM_DOWN_BACK), True)

    # ---- robe: shoulders -> cinched waist -> flared hem ----
    top, waist, hem = 20 + by, 27 + by, 34 + by
    wl = lean // 2 + (sway // 2 if sway < 0 else 0)
    c.poly([(CX - 4 + lean, top), (CX + 5 + lean, top), (CX + 5 + wl, waist),
            (CX + 7 + sway, hem), (CX - 6 + sway, hem), (CX - 4 + wl, waist)], ROBE)
    c.poly([(CX - 4 + lean, top), (CX - 2 + lean, top), (CX - 2 + wl, waist),
            (CX - 3 + sway, hem), (CX - 6 + sway, hem), (CX - 4 + wl, waist)], ROBE_SHADE)
    c.line(CX + 1 + lean, top + 1, CX + 3 + lean, top + 1, ROBE_LIGHT)
    c.line(CX + 3 + lean, top + 2, CX + 3 + wl, waist, INNER)              # open front shows undershirt
    c.line(CX + 3 + wl, waist + 1, CX + 4 + sway, hem - 1, ROBE_SHADE)    # skirt split
    for x in range(W):                                                     # hem trim
        if c.get(x, hem - 1)[3]:
            c.set(x, hem - 1, ROBE_SHADE)
    sash_y = 27 + by
    for x in range(W):                                                     # sash follows the robe outline
        if c.get(x, sash_y)[3]:
            c.set(x, sash_y, SASH)
    tail_x = CX - 5 + min(sway, 0)
    c.line(tail_x, sash_y, tail_x - 1 + min(sway, 0) // 2, sash_y + 3, SASH)  # knot tail trails behind
    c.rect(CX - 1 + lean, top - 1, CX + 2 + lean, top, INNER)                 # high collar

    # ---- head ----
    hx, ht = CX + lean - 5, 9 + by                                         # template top-left
    if hair_up:
        c.stamp(HEAD_HAIR_UP, hx, ht, HEAD_COLORS)
        c.rect(hx - 1, ht + 1, hx, ht + 1, HAIR_TIP)                       # tips flick up when falling
        c.set(hx, ht, HAIR_TIP)
    else:
        c.stamp(HEAD, hx, ht, HEAD_COLORS)
        for i in range(hs):                                                # tips trail behind when moving
            c.set(hx - i, ht + 8, HAIR)
            c.set(hx - i, ht + 9, HAIR_TIP)

    c.outline()

    # ---- front arm: own layer + own outline so it reads against the robe ----
    fa = Canvas(W, H)
    arm(fa, sh_front, p.get("front_arm", ARM_DOWN_FRONT), False)
    fa.outline()
    c.composite(fa)

    # ---- FX (drawn after outline so they glow) ----
    for fx in p.get("fx", []):
        kind, x, y = fx
        if kind == "streak":
            c.line(x, y, x + 3, y, SPARK)
            c.line(x - 1, y - 2, x + 2, y - 2, EMBER)
            c.line(x - 1, y + 2, x + 2, y + 2, EMBER)
        elif kind == "burst":
            for dx, dy in ((0, -3), (2, -2), (3, 0), (2, 2), (0, 3)):
                c.set(x + dx, y + dy, SPARK)
            for dx, dy in ((1, -1), (1, 1), (2, 0)):
                c.set(x + dx, y + dy, EMBER)
    return c


# ---------------- animations ----------------

IDLE = [
    dict(by=0, hair=0),
    dict(by=0, hair=1),
    dict(by=1, hair=1, sway=-1),
    dict(by=1, hair=0),
]

RUN_ARM_FWD = ((1, 3), (3, 5))
RUN_ARM_BACK = ((-1, 3), (-3, 5))
RUN = [
    dict(lean=1, sway=-2, hair=1, front_foot=(CX + 4, FOOT), back_foot=(CX - 5, FOOT - 1),
         front_arm=RUN_ARM_BACK, back_arm=RUN_ARM_FWD),
    dict(lean=1, sway=-2, hair=2, by=-1, front_foot=(CX + 1, FOOT), back_foot=(CX - 2, FOOT - 3),
         front_arm=ARM_DOWN_FRONT, back_arm=ARM_DOWN_BACK),
    dict(lean=1, sway=-2, hair=1, front_foot=(CX - 4, FOOT - 1), back_foot=(CX + 3, FOOT),
         front_arm=RUN_ARM_FWD, back_arm=RUN_ARM_BACK),
    dict(lean=1, sway=-2, hair=2, by=-1, front_foot=(CX, FOOT - 3), back_foot=(CX - 1, FOOT),
         front_arm=ARM_DOWN_FRONT, back_arm=ARM_DOWN_BACK),
]

JUMP = [
    dict(by=-1, hair=1, front_foot=(CX + 3, FOOT - 3), back_foot=(CX - 3, FOOT),
         front_arm=((2, 0), (4, -1)), back_arm=((-1, 3), (-3, 4))),
    dict(by=-1, hair=1, front_foot=(CX + 2, FOOT - 3), back_foot=(CX - 3, FOOT - 2),
         front_arm=((2, 1), (4, 2)), back_arm=((-2, 1), (-4, 2))),
    dict(by=0, sway=1, hair_up=True, front_foot=(CX + 2, FOOT), back_foot=(CX - 3, FOOT - 1),
         front_arm=((2, -1), (4, -3)), back_arm=((-2, -1), (-4, -3))),
]

ATTACK = [
    dict(by=1, lean=-1, front_foot=(CX + 3, FOOT), back_foot=(CX - 4, FOOT),
         front_arm=((-2, 2), (-4, 3)), back_arm=((2, 2), (3, 1))),
    dict(lean=2, sway=-2, hair=2, front_foot=(CX + 5, FOOT), back_foot=(CX - 4, FOOT),
         front_arm=((4, 0), (8, 0)), back_arm=((-1, 3), (-3, 4)), fx=[("streak", 28, 21)]),
    dict(lean=2, sway=-1, hair=1, front_foot=(CX + 5, FOOT), back_foot=(CX - 4, FOOT),
         front_arm=((4, 0), (8, 0)), back_arm=((-1, 3), (-3, 4)), fx=[("burst", 28, 21)]),
    dict(by=0, lean=0, front_foot=(CX + 3, FOOT), back_foot=(CX - 3, FOOT),
         front_arm=((2, 2), (3, 4)), back_arm=ARM_DOWN_BACK),
]

ANIMATIONS = {"idle": IDLE, "run": RUN, "jump": JUMP, "attack": ATTACK}


def build():
    return {name: [draw(p) for p in poses] for name, poses in ANIMATIONS.items()}
