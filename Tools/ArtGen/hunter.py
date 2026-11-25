"""Hunters: two variants of a burly, bearded classic hunter, sharing one pose-driven body.

Frame: 48x48 px, 32 PPU, pivot at the centre. Feet rest on row 39 (16 px below the centre),
i.e. a 1-unit-tall collider centred on the pivot (current PatrolEnemy box collider). Faces RIGHT.

- Trapper: green tunic, dark beard, feathered hat, throws a rope net.
- Gunner:  leather coat, ginger beard, fires a flared blunderbuss.
"""
from palette import (BEARD_DARK, BEARD_DARK_SHADE, BEARD_GINGER, BEARD_GINGER_SHADE, BELT, BUCKLE,
                     COAT_GREEN, COAT_GREEN_SHADE, COAT_LEATHER, COAT_LEATHER_SHADE, EMBER, EYE,
                     FEATHER, GLOVE, HAT, HAT_SHADE, METAL, METAL_SHADE, ROPE, ROPE_SHADE, SKIN,
                     SKIN_SHADE, SMOKE, SPARK, TROUSERS, TROUSERS_SHADE, WOOD, BOOT, BOOT_SHADE)
from pixel import Canvas

W, H = 48, 48
CX = 22
FOOT = 39

VARIANTS = {
    "trapper": dict(coat=COAT_GREEN, coat_shade=COAT_GREEN_SHADE, beard=BEARD_DARK,
                    beard_shade=BEARD_DARK_SHADE, feather=True),
    "gunner": dict(coat=COAT_LEATHER, coat_shade=COAT_LEATHER_SHADE, beard=BEARD_GINGER,
                   beard_shade=BEARD_GINGER_SHADE, feather=False),
}


def draw(v, p):
    c = Canvas(W, H)
    by = p.get("by", 0)
    lean = p.get("lean", 0)
    hip_y = 31 + by

    # ---- legs ----
    def leg(hx, foot, back):
        fx, fy = foot
        c.line(hx, hip_y, fx, fy - 2, TROUSERS_SHADE if back else TROUSERS, 3)
        c.rect(fx - 1, fy - 2, fx + 3, fy, BOOT_SHADE if back else BOOT)

    leg(CX - 3 + lean, p.get("back_foot", (CX - 4, FOOT)), True)
    leg(CX + 3 + lean, p.get("front_foot", (CX + 3, FOOT)), False)

    sh_back = (CX - 5 + lean, 21 + by)
    sh_front = (CX + 5 + lean, 21 + by)

    def arm(target, sh, pose, back):
        (ex, ey), (hx, hy) = pose
        elbow = (sh[0] + ex, sh[1] + ey)
        hand = (sh[0] + hx, sh[1] + hy)
        col = v["coat_shade"] if back else v["coat"]
        target.line(*sh, *elbow, col, 3)
        target.line(*elbow, *hand, col, 3)
        target.rect(hand[0] - 1, hand[1] - 1, hand[0] + 1, hand[1] + 1, GLOVE)
        return hand

    # ---- back arm ----
    back_hand = arm(c, sh_back, p.get("back_arm", ((-1, 4), (0, 8))), True)

    # ---- barrel torso ----
    top, hem = 19 + by, 34 + by
    c.poly([(CX - 6 + lean, top), (CX + 7 + lean, top), (CX + 9 + lean, top + 6),
            (CX + 8, hem), (CX - 7, hem), (CX - 8 + lean, top + 6)], v["coat_shade"])
    c.poly([(CX - 5 + lean, top), (CX + 7 + lean, top), (CX + 9 + lean, top + 6),
            (CX + 8, hem - 1), (CX - 5, hem - 1), (CX - 6 + lean, top + 6)], v["coat"])
    belt_y = 29 + by
    for x in range(W):
        if c.get(x, belt_y)[3]:
            c.set(x, belt_y, BELT)
            c.set(x, belt_y + 1, BELT)
    c.rect(CX + 3 + lean // 2, belt_y, CX + 4 + lean // 2, belt_y + 1, BUCKLE)
    c.line(CX - 4 + lean, top + 1, CX - 2 + lean, belt_y - 1, v["coat_shade"])   # strap across chest
    if v["feather"]:                                                             # trapper: rope coil at hip
        c.ellipse(CX - 6, belt_y + 3, 2.5, 2.5, ROPE)
        c.ellipse(CX - 6, belt_y + 3, 1, 1, ROPE_SHADE)

    # ---- head ----
    hx, hy = CX + 1 + lean, 14 + by
    c.rect(hx - 3, hy - 3, hx + 5, hy + 3, SKIN)                     # face
    c.rect(hx - 3, hy - 3, hx - 2, hy + 3, SKIN_SHADE)                # ear side
    c.rect(hx + 5, hy - 1, hx + 6, hy + 1, SKIN_SHADE)                # big nose
    c.set(hx + 6, hy - 1, SKIN)
    c.set(hx + 3, hy - 1, EYE)                                        # eye
    c.ellipse(hx + 2, hy + 4, 5.5, 4, v["beard_shade"])               # bushy beard
    c.ellipse(hx + 2.5, hy + 3.5, 5, 3.5, v["beard"])
    c.rect(hx + 1, hy + 1, hx + 5, hy + 1, v["beard"])                # moustache
    c.set(hx + 6, hy + 2, v["beard"])
    c.rect(hx + 2, hy - 2, hx + 4, hy - 2, v["beard_shade"])          # bushy brow
    # hat: wide brim + crown
    c.rect(hx - 6, hy - 4, hx + 8, hy - 4, HAT_SHADE)
    c.rect(hx - 5, hy - 5, hx + 7, hy - 5, HAT)
    c.poly([(hx - 3, hy - 5), (hx + 5, hy - 5), (hx + 4, hy - 10), (hx - 2, hy - 10)], HAT)
    c.line(hx - 3, hy - 6, hx + 5, hy - 6, HAT_SHADE)                 # hat band
    if v["feather"]:
        c.line(hx - 3, hy - 6, hx - 7, hy - 11, FEATHER)
        c.line(hx - 4, hy - 6, hx - 7, hy - 10, FEATHER)

    c.outline()

    # ---- weapon + front arm (own layer, own outline) ----
    fl = Canvas(W, H)
    weapon = p.get("weapon")
    if weapon == "gun":
        gx, gy, tip = p.get("gun", (CX + 1, 27, CX + 17))
        gy += by
        fl.line(gx - 3, gy + 1, gx + 3, gy, WOOD, 3)                  # stock
        fl.line(gx + 3, gy, tip, gy - 1, METAL_SHADE, 2)              # barrel
        fl.line(gx + 3, gy - 1, tip, gy - 2, METAL)
        fl.rect(tip, gy - 3, tip + 1, gy + 1, METAL)                  # flared muzzle
        fl.set(tip + 1, gy - 4, METAL)
        fl.set(tip + 1, gy + 2, METAL)
    arm(fl, sh_front, p.get("front_arm", ((1, 4), (1, 8))), False)
    if weapon == "net_bundle":
        hx2, hy2 = sh_front[0] + p["front_arm"][1][0], sh_front[1] + p["front_arm"][1][1]
        fl.ellipse(hx2 + 1, hy2 - 2, 3, 2.5, ROPE)
        for dx in (-1, 1, 3):
            fl.set(hx2 + dx, hy2 - 2, ROPE_SHADE)
    fl.outline()
    c.composite(fl)

    # ---- FX ----
    for kind, x, y in p.get("fx", []):
        if kind == "muzzle":
            for dx, dy in ((0, 0), (1, 0), (2, 0), (3, 0), (1, -1), (1, 1), (2, -2), (2, 2), (4, 0)):
                c.set(x + dx, y + dy, SPARK)
            for dx, dy in ((3, -1), (3, 1), (5, 0), (4, -2), (4, 2)):
                c.set(x + dx, y + dy, EMBER)
        elif kind == "smoke":
            for dx, dy in ((0, 0), (1, -1), (2, -1), (3, -2), (2, -3), (4, -3), (1, -2)):
                c.set(x + dx, y + dy, SMOKE)
        elif kind == "net":
            # net spreading forward from the hand as a rope grid
            spread = p.get("spread", 8)
            for i in range(0, spread + 1, 2):
                c.line(x + i, y - i // 2 - 1, x + i, y + i // 2 + 1, ROPE)
            for j in range(-spread // 2, spread // 2 + 1, 2):
                c.line(x, y, x + spread, y + j, ROPE_SHADE)
    return c


# ---------------- animations ----------------

IDLE_COMMON = [dict(by=0), dict(by=0), dict(by=1), dict(by=1)]
WALK_FEET = [
    dict(front_foot=(CX + 6, FOOT), back_foot=(CX - 6, FOOT - 1), by=0),
    dict(front_foot=(CX + 3, FOOT), back_foot=(CX - 3, FOOT - 3), by=-1),
    dict(front_foot=(CX, FOOT - 1), back_foot=(CX - 1, FOOT), by=0),
    dict(front_foot=(CX + 3, FOOT - 3), back_foot=(CX - 4, FOOT), by=-1),
]

GUN_HOLD = dict(weapon="gun", front_arm=((2, 4), (5, 6)), back_arm=((1, 4), (2, 6)))
NET_HOLD = dict(weapon="net_bundle", front_arm=((2, 4), (3, 7)))


def poses(name):
    if name == "gunner":
        idle = [dict(GUN_HOLD, **f) for f in IDLE_COMMON]
        walk = [dict(GUN_HOLD, **f) for f in WALK_FEET]
        attack = [
            dict(GUN_HOLD, by=1, front_arm=((3, 2), (6, 4)), gun=(CX + 2, 25, CX + 18)),          # aim
            dict(GUN_HOLD, lean=-1, front_arm=((3, 2), (5, 4)), gun=(CX + 1, 25, CX + 17),        # fire
                 fx=[("muzzle", CX + 19, 24)]),
            dict(GUN_HOLD, lean=-2, front_arm=((2, 2), (4, 4)), gun=(CX, 24, CX + 16),            # recoil
                 fx=[("smoke", CX + 18, 22)]),
            dict(GUN_HOLD, by=0, fx=[("smoke", CX + 19, 19)]),                                    # recover
        ]
    else:
        idle = [dict(NET_HOLD, **f) for f in IDLE_COMMON]
        walk = [dict(NET_HOLD, **f) for f in WALK_FEET]
        attack = [
            dict(weapon="net_bundle", by=1, lean=-1, front_arm=((3, -5), (4, -11))),             # wind-up overhead
            dict(lean=1, front_arm=((3, -2), (7, -2)), fx=[("net", CX + 14, 19)], spread=6),     # throw
            dict(lean=2, front_arm=((4, 0), (8, 1)), fx=[("net", CX + 16, 22)], spread=12),      # net opens
            dict(by=0, front_arm=((2, 4), (3, 7))),                                               # recover
        ]
    return {"idle": idle, "walk": walk, "attack": attack}


def build(variant):
    v = VARIANTS[variant]
    return {anim: [draw(v, p) for p in ps] for anim, ps in poses(variant).items()}
