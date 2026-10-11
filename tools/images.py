"""Optimise Building Repair Centre's original job photos for the static site.

Reads originals from the cPanel backup (read-only, outside this repository) and
writes resized, metadata-free WebP files to website/assets/img/:

    python tools/images.py

The backup location defaults to the Roof Centre project's reference folder.
Override it with the BRC_BACKUP environment variable (the folder that contains
homedir/). The optimised images are committed, so build.py does not need this.
"""
from pathlib import Path
import json
import os
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BACKUP_GLOB = ROOT.parent / "roofcentre" / "reference" / "extracted"
OUT = ROOT / "website" / "assets" / "img"
MANIFEST = ROOT / "tools" / "image-manifest.json"
WIDTHS = [480, 800, 1200, 1600]


def find_uploads():
    if os.environ.get("BRC_BACKUP"):
        base = Path(os.environ["BRC_BACKUP"])
    else:
        found = sorted(DEFAULT_BACKUP_GLOB.glob("backup-*"))
        if not found:
            raise SystemExit("Original photos not found. Set BRC_BACKUP to the extracted cPanel backup folder.\n"
                             "The optimised images in website/assets/img/ are committed, so build.py works without this step.")
        base = found[-1]
    uploads = base / "homedir/public_html/buildingrepaircentre.com.au/wp-content/uploads"
    if not uploads.is_dir():
        raise SystemExit(f"Not found: {uploads}")
    return uploads


# key: (source path, alt text)
# Only confirmed job photos. Excluded: stock images, banner graphics, staff
# portraits, the Neutral Bay render and photos showing other businesses' branding.
PHOTOS = {
    # Commercial
    "cafe-fitout": ("2020/06/commercial.jpeg", "Completed café fit-out with timber-clad counter, display cabinet and pendant lights"),
    "camperdown-stairs": ("2020/09/camperdown-1600x1200-1.jpeg", "Camperdown commercial fit-out: open-plan floor with a new steel staircase"),
    "camperdown-1": ("2020/07/camperdown-1.png", "Camperdown fit-out: tradespeople installing plasterboard walls"),
    "camperdown-3": ("2020/07/camperdown-3.png", "Camperdown fit-out: scissor lift and tradespeople working on ceilings"),
    "camperdown-4": ("2020/07/camperdown-4.png", "Camperdown fit-out: open commercial floor during construction"),
    "camperdown-6": ("2020/07/camperdown-6.png", "Camperdown fit-out: concrete floor being cleaned in the finished space"),
    "college-frame": ("2020/07/pic-1.png", "College building: steel roof framing with scissor lifts on the floor"),
    "college-1": ("2020/07/College-1.png", "College building: steel-framed walls and roof structure"),
    "college-2": ("2020/07/College-2.png", "College building: brick wall and steel framing"),
    "college-3": ("2020/07/College-3.png", "College building: steel ceiling and wall framing"),
    "college-4": ("2020/07/College-4.png", "College building: room with new walls and window ready for finishing"),
    # Strata and apartments
    "redfern-apartments": ("2020/09/strata.jpeg", "Multi-storey apartment building in Redfern"),
    "redfern-1": ("2020/07/redburn-1.png", "Redfern apartment building: balconies and awning"),
    "redfern-2": ("2020/07/redburn-2.png", "Redfern apartment building: upper-level balconies"),
    "redfern-3": ("2020/07/redburn-3.png", "Redfern apartment building: facade and balconies"),
    "redfern-4": ("2020/07/redburn-4.png", "Redfern apartment building: full height of the facade"),
    "apartment-block": ("2020/09/2.jpeg", "Redfern apartment building seen from street level"),
    # Residential
    "deck-pergola-cn": ("2020/09/chipping-norton-1600x1200-1.jpeg", "Chipping Norton: new timber deck and pergola framing at the back of a brick home"),
    "deck-frame-cn": ("2020/07/chipping-norton-4.png", "Chipping Norton: deck and pergola under construction"),
    "plastered-room": ("2020/07/chipping-norton-2.png", "Room with new plasterboard walls set and ready for painting"),
    "lindfield-frame": ("2020/07/640x480.png", "Lindfield: steel-framed structure under construction on a bush block"),
    "hallway-doors": ("2020/06/residential.jpeg", "Hallway with timber doors, cornices and tiled floor"),
    "pergola-1": ("2020/11/1.jpeg", "Back of the house before the new deck and pergola"),
    "pergola-2": ("2020/11/2.jpeg", "Metal roof sheets being laid over sarking on the new pergola roof"),
    "pergola-3": ("2020/11/3.jpeg", "Treated pine subfloor framing for the raised deck"),
    "pergola-4": ("2020/11/4.jpeg", "Underside of the new pergola roof with timber battens"),
    "pergola-5": ("2020/11/5.jpeg", "Pergola rafters going up over the deck frame"),
    "pergola-6": ("2020/11/6.jpeg", "Deck joists in place across the subfloor"),
    "pergola-7": ("2020/11/7.jpeg", "Pergola rafters seen from below"),
    "pergola-8": ("2020/11/8.jpeg", "Back of the house and existing stairs before work started"),
    "pergola-9": ("2020/11/9.jpeg", "Carpenter fixing framing at the roof edge"),
    "pergola-10": ("2020/11/10.jpeg", "Timber deck frame set out on the ground"),
    "pergola-11": ("2020/11/11.jpeg", "Finished metal roof over the new pergola"),
    "pergola-12": ("2020/11/12.jpeg", "White posts and beams of a new pergola against a brick home"),
    # Insurance repairs
    "storm-tree-roof": ("2020/06/insurance.jpeg", "Tree fallen across the tiled roof of a two-storey house"),
    "storm-tree-yard": ("2020/09/6.jpeg", "Large tree fallen into a backyard beside a house"),
    # Other trades
    "tile-roof-skylights": ("2020/09/8.jpeg", "Terracotta tile roof with two skylights"),
    "concrete-courtyard": ("2020/09/concrete.jpeg", "Concrete courtyard path with planters"),
    "fence-walkway": ("2020/09/13.jpeg", "Tall black fence along a bush walkway"),
    "aluminium-frame": ("2020/09/12.jpeg", "Aluminium frame on site ready for installation"),
}


def flatten(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def white_logo(lg, bg=(10, 37, 82)):
    """Swap the logo's navy and white so it reads on the dark footer. Shape and alpha are unchanged."""
    out = []
    for r, g, b, a in lg.getdata():
        t = (0.299 * r + 0.587 * g + 0.114 * b) / 255  # 0 = navy, 1 = white
        out.append(tuple(round(255 + (c - 255) * t) for c in bg) + (a,))
    w = Image.new("RGBA", lg.size)
    w.putdata(out)
    return w


def main():
    uploads = find_uploads()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, (src, alt) in PHOTOS.items():
        im = flatten(Image.open(uploads / src))
        widths = sorted({w for w in WIDTHS if w <= im.width} | ({im.width} if im.width < WIDTHS[-1] else set()))
        files = []
        for w in widths:
            h = round(im.height * w / im.width)
            name = f"{key}-{w}.webp"
            dest = OUT / name
            if not dest.exists():
                im.resize((w, h), Image.LANCZOS).save(dest, "WEBP", quality=76 if w > 1000 else 80, method=6)
            files.append({"w": w, "h": h, "file": name})
        manifest[key] = {"alt": alt, "files": files, "source": src}
        print(f"{key:22} {im.width}x{im.height} -> {[f['w'] for f in files]}")

    # Social sharing image
    og = ImageOps.fit(flatten(Image.open(uploads / PHOTOS["cafe-fitout"][0])), (1200, 630), Image.LANCZOS)
    og.save(OUT / "og-building-repair-centre.jpg", "JPEG", quality=80, optimize=True, progressive=True)

    # Logo (trimmed, transparent) and a white version for dark backgrounds
    lg = Image.open(uploads / "2020/09/BRC-final-logo.png").convert("RGBA")
    lg = lg.crop(lg.getbbox())
    for name, im in (("logo", lg), ("logo-white", white_logo(lg))):
        im.save(OUT / f"{name}.png", optimize=True)
        im.save(OUT / f"{name}.webp", "WEBP", quality=92, method=6)
        manifest[f"_{name}"] = {"w": im.width, "h": im.height}

    # Favicons from the original site icon
    icon = Image.open(uploads / "2020/09/BRC-favicon.png").convert("RGBA")
    icon.resize((32, 32), Image.LANCZOS).save(ROOT / "website" / "favicon-32.png", optimize=True)
    icon.save(ROOT / "website" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    icon.convert("RGB").resize((180, 180), Image.LANCZOS).save(ROOT / "website" / "apple-touch-icon.png", optimize=True)
    for s in (192, 512):
        icon.convert("RGB").resize((s, s), Image.LANCZOS).save(OUT / f"icon-{s}.png", optimize=True)

    MANIFEST.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print("images:", len(PHOTOS))


if __name__ == "__main__":
    main()
