"""Emberway master palette: warm storybook.

All generated art draws only from these colours so every asset stays consistent.
Colours are (R, G, B, A).
"""

def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


CLEAR = (0, 0, 0, 0)

# Shared
OUTLINE = hexc("#2b1d2e")      # warm dark plum, used for every silhouette outline
SKIN = hexc("#f2c9a0")
SKIN_SHADE = hexc("#d49b7a")
EYE = hexc("#2e5c6e")

# Mira
HAIR = hexc("#f4f1ea")
HAIR_SHADE = hexc("#c9c4d6")
HAIR_TIP = hexc("#6fd3d0")      # signature teal tips
ROBE = hexc("#f2c14e")
ROBE_LIGHT = hexc("#fbe08a")
ROBE_SHADE = hexc("#c98f2a")
INNER = hexc("#3b3446")         # charcoal undershirt / collar / robe lining
SASH = hexc("#8c3b2f")
PANTS = hexc("#4a4058")
PANTS_SHADE = hexc("#372f44")
BOOT = hexc("#6b4430")
BOOT_SHADE = hexc("#4a2c1e")

# FX
SPARK = hexc("#fff4c2")
EMBER = hexc("#ff9a3c")
