#!/usr/bin/env python3
# Generates docs/assets/logo/quantum_og.png — the 1200x630 Open Graph /
# Twitter card image used by theme/main.html. Run it after changing the logo,
# the tagline or the hero screenshot:
#
#   python scripts/make-og-image.py
#
# Everything is composited from assets already in the repo, so the card never
# drifts from the shipped brand.

import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(REPO, "docs", "assets")
LOGO = os.path.join(ASSETS, "logo", "quantum_logo_dark.png")
HERO = os.path.join(ASSETS, "screenshots", "editor-overview.png")
OUT = os.path.join(ASSETS, "logo", "quantum_og.png")

W, H = 1200, 630

# Theme tokens, kept in sync with theme/css/quantum.css by hand.
BG = (7, 11, 22)            # --bg-primary
TEXT = (237, 246, 255)      # --text-primary
MUTED = (127, 148, 181)     # --text-muted
CYAN = (34, 211, 238)
PURPLE = (139, 92, 246)

TAGLINE = "C++17 game engine & visual editor"
PLATFORMS = "MIT  ·  Windows  ·  Linux  ·  macOS  ·  Android  ·  iOS  ·  HTML5"


def font(size, bold=False):
    for name in ("segoeuib.ttf" if bold else "segoeui.ttf",
                 "arialbd.ttf" if bold else "arial.ttf"):
        path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def trim(im):
    """Crop the transparent padding around an RGBA logo.

    The brand PNGs already carry an alpha channel (glyphs at 245,246,250 on a
    fully transparent canvas), so getbbox() on the alpha is all that is needed
    to scale them predictably.
    """
    rgba = im.convert("RGBA")
    bbox = rgba.getbbox()
    return rgba.crop(bbox) if bbox else rgba


def main():
    card = Image.new("RGB", (W, H), BG)

    # Soft radial glow behind the logo corner, like the site's hero.
    glow = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(glow)
    d.ellipse((-260, -320, 620, 460), fill=(17, 26, 48))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    card.paste(glow, (0, 0))

    # Hero screenshot on the right, faded into the background on its left edge.
    # Pre-darkened so it reads as a backdrop: the editor's viewport is bright
    # sky and would otherwise out-shout the wordmark.
    hero = Image.open(HERO).convert("RGB")
    crop_h = int(hero.width * H / W)
    hero = hero.crop((0, (hero.height - crop_h) // 2, hero.width,
                      (hero.height - crop_h) // 2 + crop_h)).resize((W, H))
    hero = Image.blend(hero, Image.new("RGB", (W, H), BG), 0.45)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    fade_start, fade_end = int(W * 0.40), int(W * 0.74)
    for x in range(W):
        if x < fade_start:
            a = 0
        elif x > fade_end:
            a = 175
        else:
            a = int(175 * (x - fade_start) / (fade_end - fade_start))
        md.line([(x, 0), (x, H)], fill=a)
    card.paste(hero, (0, 0), mask)

    logo = trim(Image.open(LOGO).convert("RGBA"))
    lw = 640
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    card.paste(logo, (76, 150), logo)

    draw = ImageDraw.Draw(card)
    draw.text((80, 330), TAGLINE, font=font(34), fill=TEXT)

    # Accent rule in the brand gradient.
    for i, x in enumerate(range(80, 460)):
        t = i / 380
        draw.line([(x, 396), (x, 400)], fill=(
            int(CYAN[0] + (PURPLE[0] - CYAN[0]) * t),
            int(CYAN[1] + (PURPLE[1] - CYAN[1]) * t),
            int(CYAN[2] + (PURPLE[2] - CYAN[2]) * t)))

    draw.text((80, 428), PLATFORMS, font=font(24), fill=MUTED)

    card.save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
