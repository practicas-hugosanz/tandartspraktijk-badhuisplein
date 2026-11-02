"""Zet de originele beelden van de oude site om naar geoptimaliseerde WebP/PNG.

Gebruik:  python -I _build/assets.py <map-met-gedownloade-beelden>
Draai eenmalig; de resultaten staan in assets/img/.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
NAVY = (27, 33, 52)
GOLD = (200, 185, 146)


def webp(src, dst, width, quality=78):
    im = Image.open(SRC / src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)
    print(dst.relative_to(ROOT), im.size)


# Teamportretten (950x1424) -> 480 breed
TEAM = {"alvaro": "Alvaro", "kinan": "Kinan", "ana": "AnaRecas", "itschi": "Itschi", "lucette": "lucette", "roos": "roos",
        "anja": "Anja-preventieassistente", "maaike": "Maaike", "mirjam": "Mirjam2", "sigita": "Sigita", "stefanie": "Stefanie",
        "madee": "Madee", "rozemarijn": "Rozemarijn", "serge": "Serge", "ferdy": "Ferdy", "henriette": "Henriette",
        "louise": "louise", "veerle": "Veerle", "hala": "Hala"}
for k, n in TEAM.items():
    webp(f"{n}.jpg", IMG / "team" / f"{k}.webp", 480)

# Praktijk- en behandelfoto's
PHOTOS = {
    "gevel": "Praktijk-buitenkant", "luchtfoto": "Praktijk-buitenkant-1", "balie": "Balie-099", "wachtkamer": "Wachtkamer",
    "balie-team": "TP-Badhuisplein-088", "behandeling-alvaro": "Behandeling-Alvaro", "behandeling-kinan": "Behandeling-Kinan",
    "behandeling-anja": "Behandeling-Anja", "anja-spiegel": "Behandeling-Anja-prev.-spiegel", "ferdy-techniek": "Ferdy-techniek",
    "cadcam": "Cad-cam-kronen", "serge-behandeling": "Serge-behandeling", "itschi-stoel": "Itschi-aan-de-stoel", "opg": "OPG-",
    "scan": "TP-Badhuisplein-1324", "bleken": "TP-Badhuisplein-352", "esthetisch": "TP-Badhuisplein-234", "wortelkanaal": "TP-Badhuisplein-636",
    "extractie": "extractie", "kinderen": "blokje-kids-1", "kinderen-stoel": "TP-Badhuisplein-745", "preventie-kind": "Roos-kies-voor-gaaf-preventiebehandeling-kinderen",
    "lachgas": "Lachgas-volwassenen-lieve-tandarts", "lachgas-kind": "Lachgas-kinderen", "angst": "angst-1", "invisalign": "foto_invisalign",
    "beperking": "foto_beperking", "steri": "Steri-Anja",
}
for dst, src in PHOTOS.items():
    webp(f"{src}.jpg", IMG / f"{dst}.webp", 950)
webp("brackets.png", IMG / "brackets.webp", 587)
webp("TP-Badhuisplein-494.jpg", IMG / "team-panorama.webp", 1920, 80)
Image.open(SRC / "logo-lieve-tandarts-768x224-2.png").convert("RGBA").resize((384, 112), Image.LANCZOS).save(IMG / "lieve-tandarts.png", optimize=True)

# Poster van de hero (getoond zolang er geen video is, en als stilstaand beeld bij de video)
balie = Image.open(SRC / "Balie-099.jpg").convert("RGB")
balie = ImageOps.fit(balie, (1600, 900), Image.LANCZOS, centering=(0.5, 0.5))
balie.save(IMG / "hero-poster.webp", "WEBP", quality=74, method=6)
balie.resize((800, 450), Image.LANCZOS).save(IMG / "hero-poster-800.webp", "WEBP", quality=72, method=6)

# Behandeliconen: witte lijniconen -> alfamasker (kleur via CSS mask)
(IMG / "icons").mkdir(parents=True, exist_ok=True)
for n in ["esthetisch", "bleken", "implantaten", "kronen", "protheses", "orthodontie", "vullingen", "extractie", "wortelkanaal", "preventie"]:
    a = Image.open(SRC / f"{n}.png").convert("RGBA").getchannel("A").resize((160, 160), Image.LANCZOS)
    out = Image.new("RGBA", (160, 160), (255, 255, 255, 0))
    out.putalpha(a)
    out.save(IMG / "icons" / f"{n}.png", optimize=True)

# Logo: origineel is crème + wit, bedoeld voor donkere achtergrond
logo = Image.open(SRC / "logo-retina.png").convert("RGBA")
logo.save(IMG / "logo-licht.png", optimize=True)
dark = logo.copy()
px, dp = logo.load(), dark.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        dp[x, y] = (*NAVY, a) if r > 235 and g > 235 and b > 235 else (150, 128, 78, a)
dark.save(IMG / "logo-donker.png", optimize=True)

# Beeldmerk (de tand) uitsnijden voor favicons en de kleine kop
mark = logo.crop((0, 0, 140, logo.height))
mark = mark.crop(mark.getchannel("A").getbbox())
mark.save(IMG / "mark-licht.png", optimize=True)
print("mark", mark.size)


def icon(size, pad=0.2, radius=0.22):
    can = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg = Image.new("RGBA", (size, size), (*NAVY, 255))
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), round(size * radius), fill=255)
    can.paste(bg, (0, 0), m)
    inner = round(size * (1 - 2 * pad))
    k = inner / max(mark.size)
    t = mark.resize((round(mark.width * k), round(mark.height * k)), Image.LANCZOS)
    can.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2))
    return can


icon(512).save(IMG / "icon-512.png", optimize=True)
icon(192).save(IMG / "icon-192.png", optimize=True)
icon(180, pad=0.18, radius=0).save(IMG / "apple-touch-icon.png", optimize=True)
icon(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# Open Graph-afbeelding 1200x630
og = Image.new("RGB", (1200, 630), NAVY)
d = ImageDraw.Draw(og)
portrait = Image.open(SRC / "Alvaro.jpg").convert("RGB")
portrait = ImageOps.fit(portrait, (430, 630), centering=(0.5, 0.3))
og.paste(portrait, (770, 0))
grad = Image.new("L", (160, 630))
for x in range(160):
    ImageDraw.Draw(grad).line([(x, 0), (x, 630)], fill=round(255 * (1 - x / 159)))
og.paste(Image.new("RGB", (160, 630), NAVY), (770, 0), grad)
lg = logo.copy()
lg.thumbnail((360, 100), Image.LANCZOS)
og.paste(lg, (80, 70), lg)
head = ImageFont.truetype(str(ROOT / "_build" / "Archivo.ttf"), 58)
head.set_variation_by_axes([700])
sans = ImageFont.truetype("arial.ttf", 28)
d.text((80, 230), "Op uw gemak bij de", font=head, fill=(255, 255, 255))
d.text((80, 302), "tandarts in Hardenberg.", font=head, fill=GOLD)
d.line([(82, 410), (150, 410)], fill=GOLD, width=3)
d.text((80, 440), "Badhuisplein 2 en 6, Hardenberg", font=sans, fill=(220, 222, 230))
d.text((80, 482), "Bel 0523-216967", font=sans, fill=(220, 222, 230))
og.save(IMG / "og-badhuisplein.jpg", quality=86)
print("klaar")
