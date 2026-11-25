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

# Baby dragon
DRAGON = hexc("#d9423a")
DRAGON_SHADE = hexc("#a3282f")
DRAGON_LIGHT = hexc("#f06a4f")
BELLY = hexc("#f7c87a")
BELLY_SHADE = hexc("#e0a35a")
WING = hexc("#f08a5d")
HORN = hexc("#f4e3c3")
EYE_SHINE = hexc("#ffffff")

# Hunters
COAT_GREEN = hexc("#5f7a3a")
COAT_GREEN_SHADE = hexc("#44592a")
COAT_LEATHER = hexc("#8a5a3b")
COAT_LEATHER_SHADE = hexc("#6b4430")
HAT = hexc("#5b4636")
HAT_SHADE = hexc("#43332a")
BEARD_DARK = hexc("#5a3a26")
BEARD_DARK_SHADE = hexc("#432a1c")
BEARD_GINGER = hexc("#b8602e")
BEARD_GINGER_SHADE = hexc("#8e4622")
TROUSERS = hexc("#6e6255")
TROUSERS_SHADE = hexc("#544a40")
GLOVE = hexc("#4a2c1e")
BELT = hexc("#3a2418")
BUCKLE = hexc("#d9b44a")
FEATHER = hexc("#c94f3a")
ROPE = hexc("#c9b48a")
ROPE_SHADE = hexc("#9c875f")
WOOD = hexc("#7a4b2a")
METAL = hexc("#8d8f98")
METAL_SHADE = hexc("#5d5f68")
SMOKE = hexc("#cfc8bd")

# FX
SPARK = hexc("#fff4c2")
EMBER = hexc("#ff9a3c")
