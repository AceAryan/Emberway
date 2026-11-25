"""Baby dragon (stage 1: walker): pose-driven pixel-art generator.

Frame: 32x32 px, 32 PPU, pivot at the centre. Feet rest on row 23 (8 px below the centre),
i.e. a 0.5-unit-tall collider centred on the pivot. Faces RIGHT.

Design: chibi proportions (big head, round body), big eye, two cream horns, cream belly,
tiny orange wings on the back that can only flick, stubby legs, curly tail with a spade tip.
Later stages (hop, flutter) get their own pose tables.
"""
from palette import (BELLY, BELLY_SHADE, DRAGON, DRAGON_LIGHT, DRAGON_SHADE, EYE, EYE_SHINE,
                     HORN, OUTLINE, WING)
from pixel import Canvas

W, H = 32, 32
FOOT = 23


def draw(p):
    c = Canvas(W, H)
    by = p.get("by", 0)          # body bob
    tail = p.get("tail", 0)      # tail tip sway (+ = up)
    wing = p.get("wing", 0)      # 0 folded, 1 raised
    blink = p.get("blink", False)
    legs = p.get("legs", (0, 0, 0, 0))   # lift per leg: far-back, far-front, near-back, near-front

    def leg(x, lift, col):
        c.rect(x, FOOT - 3 - lift, x + 1, FOOT - lift, col)
        c.set(x + 2, FOOT - lift, col)   # little toe forward

    # far legs (darker, behind the body)
    leg(10, legs[0], DRAGON_SHADE)
    leg(16, legs[1], DRAGON_SHADE)

    # tail: curls up behind, spade tip
    c.line(10, 19 + by, 6, 18 + by, DRAGON_SHADE, 2)
    c.line(6, 18 + by, 4, 15 + by - tail, DRAGON_SHADE, 2)
    tx, ty = 3, 13 + by - tail
    c.rect(tx, ty, tx + 1, ty + 1, DRAGON)
    c.set(tx - 1, ty + 1, DRAGON)
    c.set(tx + 1, ty - 1, DRAGON)

    # body: shade ellipse with the base colour offset up-right = rim shading
    c.ellipse(13, 17.5 + by, 6, 4.5, DRAGON_SHADE)
    c.ellipse(13.5, 17 + by, 5.5, 4, DRAGON)
    belly_mask = Canvas(W, H)
    belly_mask.ellipse(13.5, 17 + by, 5.5, 4, DRAGON)
    c.ellipse(15, 19 + by, 3.5, 3, BELLY, mask=belly_mask)
    c.line(13, 21 + by, 17, 21 + by, BELLY_SHADE)
    for x in range(12, 18, 2):                       # belly scale stripes
        c.set(x, 18 + by, BELLY_SHADE)

    # wings: tiny, on the back
    if wing:
        c.poly([(9, 6 + by), (15, 11 + by), (12, 14 + by)], WING)
        c.line(12, 13 + by, 9, 5 + by, DRAGON_SHADE)
        c.line(9, 5 + by, 15, 10 + by, DRAGON_SHADE)
    else:
        c.poly([(8, 9 + by), (15, 11 + by), (12, 14 + by)], WING)
        c.line(12, 13 + by, 8, 8 + by, DRAGON_SHADE)
        c.line(8, 8 + by, 15, 11 + by, DRAGON_SHADE)

    # head: big and round, snout to the right
    hy = 11 + by
    c.ellipse(19.5, hy + 0.5, 5.5, 5, DRAGON_SHADE)
    c.ellipse(20, hy, 5, 4.5, DRAGON)
    c.ellipse(24, hy + 2, 2.5, 2, DRAGON)            # snout
    c.ellipse(19, hy - 1.5, 2.5, 1.5, DRAGON_LIGHT)  # forehead highlight
    c.set(25, hy + 1, DRAGON_SHADE)                  # nostril
    c.line(22, hy + 3, 25, hy + 3, DRAGON_SHADE)     # little smile
    c.set(19, hy + 2, BELLY)                         # cheek
    # horns
    c.set(17, hy - 5, HORN)
    c.set(17, hy - 4, HORN)
    c.set(20, hy - 5, HORN)
    c.set(20, hy - 4, HORN)
    c.set(21, hy - 6, HORN)
    # eye: big, cute, with shine
    if blink:
        c.line(20, hy, 22, hy, EYE)
    else:
        c.rect(20, hy - 2, 22, hy + 1, EYE)
        c.set(20, hy - 2, EYE_SHINE)
        c.set(21, hy - 2, EYE_SHINE)
        c.set(20, hy - 1, EYE_SHINE)

    c.outline(OUTLINE)

    # near legs on top (own outline)
    near = Canvas(W, H)
    for x, lift in ((11, legs[2]), (17, legs[3])):
        near.rect(x, FOOT - 3 - lift, x + 1, FOOT - lift, DRAGON)
        near.set(x + 2, FOOT - lift, DRAGON)
        near.set(x, FOOT - 3 - lift, DRAGON_LIGHT)
    near.outline(OUTLINE)
    c.composite(near)
    return c


IDLE = [
    dict(by=0, tail=0),
    dict(by=0, tail=1),
    dict(by=1, tail=1, wing=1),
    dict(by=1, tail=0, blink=True),
]

WALK = [
    dict(by=0, tail=1, legs=(1, 0, 0, 1)),
    dict(by=-1, tail=0, legs=(0, 0, 0, 0)),
    dict(by=0, tail=1, legs=(0, 1, 1, 0)),
    dict(by=-1, tail=2, legs=(0, 0, 0, 0)),
]

ANIMATIONS = {"idle": IDLE, "walk": WALK}


def build():
    return {name: [draw(p) for p in poses] for name, poses in ANIMATIONS.items()}
