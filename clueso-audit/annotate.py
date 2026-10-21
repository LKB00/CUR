"""Draw numbered highlight boxes on audit screenshots.

Usage: python3 annotate.py spec.json
spec.json: {"src_dir": "...", "out_dir": "...", "images": {"file.jpg": [[x0, y0, x1, y1, "1", "sev"], ...]}}
Coordinates are in the screenshot's own pixel space. sev is one of critical|major|minor.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SCALE = 2
COLORS = {"critical": (220, 38, 38), "major": (234, 88, 12), "minor": (202, 138, 4), "good": (22, 163, 74)}
FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15 * SCALE // 2 + 6)


def annotate(src, dst, boxes):
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * SCALE, im.height * SCALE), Image.LANCZOS)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x0, y0, x1, y1, label, sev in boxes:
        c = COLORS.get(sev, COLORS["major"])
        od.rectangle([x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE], fill=c + (28,))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1, label, sev in boxes:
        c = COLORS.get(sev, COLORS["major"])
        X0, Y0, X1, Y1 = x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE
        d.rectangle([X0, Y0, X1, Y1], outline=c, width=4)
        r = 16
        cx, cy = X0, Y0
        cx = max(r + 2, min(cx, im.width - r - 2))
        cy = max(r + 2, min(cy, im.height - r - 2))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=(255, 255, 255), width=3)
        tw = d.textlength(label, font=FONT)
        d.text((cx - tw / 2, cy - 11), label, fill=(255, 255, 255), font=FONT)
    im.save(dst, quality=90)


def main():
    spec = json.load(open(sys.argv[1]))
    os.makedirs(spec["out_dir"], exist_ok=True)
    for name, boxes in spec["images"].items():
        annotate(os.path.join(spec["src_dir"], name), os.path.join(spec["out_dir"], name), boxes)
        print("annotated", name)


if __name__ == "__main__":
    main()
