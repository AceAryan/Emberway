"""Build all generated art into the Unity project.

Usage (from repo root):
    python Tools/ArtGen/build.py            # write sprite sheets into Assets/Art
    python Tools/ArtGen/build.py --preview DIR   # also write 8x upscaled previews into DIR
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mira  # noqa: E402
from pixel import preview, sheet  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = {
    "mira": os.path.join(ROOT, "Assets", "Art", "Sprites", "Player"),
}


def main():
    prev_dir = None
    if "--preview" in sys.argv:
        prev_dir = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(prev_dir, exist_ok=True)

    for anim, frames in mira.build().items():
        img = sheet(frames)
        path = os.path.join(OUT["mira"], f"mira_{anim}.png")
        img.save(path)
        print("wrote", os.path.relpath(path, ROOT), img.size)
        if prev_dir:
            preview(img).save(os.path.join(prev_dir, f"mira_{anim}.png"))


if __name__ == "__main__":
    main()
