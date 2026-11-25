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
| `build.py` | Writes sheets to their asset paths |

## Specifications

| Property | Value |
|---|---|
| Pixels per unit | 32 |
| Character frame | 32×48 px, horizontal strip, pivot at frame centre |
| Ground contact | Row 38 from top, which aligns with the bottom of a 0.9-unit collider |
| Facing | Right (flipped at runtime via `localScale.x`) |
| Outline | 1px `#2b1d2e`. Limbs in front of the body get their own outline layer |
| Import | Sprite Mode *Multiple*, Filter *Point*, Compression *None* |

## Replacing assets without breaking references
Animation clips reference sprites by the texture's GUID (in `.meta`) and the sprite's internal ID. To replace an asset:
- Overwrite the PNG in place, keeping the same dimensions and frame count. References stay valid.
- To rename, move the PNG **and** its `.meta` together, and rename the sprite names inside the `.meta`.

## Characters

| Character | Sheets | Frames |
|---|---|---|
| Mira | `Assets/Art/Sprites/Player/mira_{idle,run,jump,attack}.png` | 4 / 4 / 3 / 4 |
