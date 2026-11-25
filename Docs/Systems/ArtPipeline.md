# Art Pipeline

`Tools/ArtGen/`

## Overview
All pixel art is generated from Python code (Pillow), so every asset is reproducible, uses one palette, and can be adjusted by editing parameters instead of repainting.

```
python Tools/ArtGen/build.py                    # regenerate sheets into Assets/Art
python Tools/ArtGen/build.py --preview <dir>    # also write 8x previews
```
Requires Python 3 with Pillow (`pip install pillow`).

| File | Responsibility |
|---|---|
| `palette.py` | Master palette (warm storybook). All assets use only these colours |
| `pixel.py` | `Canvas` primitives: lines, polygons, ASCII templates, compositing, automatic 1px outline. `sheet()` and `preview()` |
| `mira.py` | Heroine: pose-driven frame builder and animation pose tables |
| `dragon.py` | Baby dragon (stage 1) |
| `hunter.py` | Shared hunter body with `trapper` and `gunner` variants |
| `metagen.py` | Writes `.meta` files for new sheets and folders: pre-sliced, Point filter, no compression, 32 PPU, deterministic IDs. Never overwrites an existing `.meta` |
| `build.py` | Builds every target listed in `TARGETS` |

## Specifications

| Property | Value |
|---|---|
| Pixels per unit | 32 |
| Frames | Horizontal strip, pivot at frame centre. Size per character (see below) |
| Ground contact | Chosen so the feet touch the bottom of the character's collider (see below) |
| Facing | Right (flipped at runtime via `localScale.x`) |
| Outline | 1px `#2b1d2e`. Limbs in front of the body get their own outline layer |
| Import | Sprite Mode *Multiple*, Filter *Point*, Compression *None* |

## Replacing assets without breaking references
Animation clips reference sprites by the texture's GUID (in `.meta`) and the sprite's internal ID. To replace an asset:
- Overwrite the PNG in place, keeping the same dimensions and frame count. References stay valid.
- To rename, move the PNG **and** its `.meta` together, and rename the sprite names inside the `.meta`.

## Characters

| Character | Sheets | Frame size | Feet row (collider) | Frames |
|---|---|---|---|---|
| Mira | `Sprites/Player/mira_{idle,run,jump,attack}.png` | 32×48 | 38 (0.9-unit capsule) | 4 / 4 / 3 / 4 |
| Baby dragon | `Sprites/Dragon/dragon_baby_{idle,walk}.png` | 32×32 | 23 (0.5-unit collider) | 4 / 4 |
| Hunter (trapper) | `Sprites/Enemies/Hunters/hunter_trapper_{idle,walk,attack}.png` | 48×48 | 39 (1-unit box) | 4 / 4 / 4 |
| Hunter (gunner) | `Sprites/Enemies/Hunters/hunter_gunner_{idle,walk,attack}.png` | 48×48 | 39 (1-unit box) | 4 / 4 / 4 |

Later dragon evolution stages (hop, flutter) are added as new pose tables and sheets (`dragon_<stage>_*`).
