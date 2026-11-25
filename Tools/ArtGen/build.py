"""Build all generated art into the Unity project.

Usage (from repo root):
    python Tools/ArtGen/build.py                  # write sprite sheets (+ missing .meta files) into Assets/Art
    python Tools/ArtGen/build.py --preview DIR    # also write 8x upscaled previews into DIR

Existing .meta files are never touched, so Unity references stay valid across rebuilds.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dragon  # noqa: E402
import hunter  # noqa: E402
import mira  # noqa: E402
from metagen import ensure_folder_meta, ensure_sheet_meta  # noqa: E402
from pixel import preview, sheet  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SPRITES = os.path.join(ROOT, "Assets", "Art", "Sprites")

# (output folder, file prefix, {anim: [frames]})
TARGETS = [
    (os.path.join(SPRITES, "Player"), "mira", mira.build),
    (os.path.join(SPRITES, "Dragon"), "dragon_baby", dragon.build),
    (os.path.join(SPRITES, "Enemies", "Hunters"), "hunter_trapper", lambda: hunter.build("trapper")),
    (os.path.join(SPRITES, "Enemies", "Hunters"), "hunter_gunner", lambda: hunter.build("gunner")),
]


def main():
    prev_dir = None
    if "--preview" in sys.argv:
        prev_dir = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(prev_dir, exist_ok=True)

    for folder, prefix, builder in TARGETS:
        os.makedirs(folder, exist_ok=True)
        ensure_folder_meta(folder, ROOT)
        for anim, frames in builder().items():
            img = sheet(frames)
            path = os.path.join(folder, f"{prefix}_{anim}.png")
            img.save(path)
            ensure_sheet_meta(path, frames[0].w, frames[0].h, len(frames), ROOT)
            print("wrote", os.path.relpath(path, ROOT), img.size)
            if prev_dir:
                preview(img).save(os.path.join(prev_dir, f"{prefix}_{anim}.png"))


if __name__ == "__main__":
    main()
