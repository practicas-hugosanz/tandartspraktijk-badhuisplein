# -*- coding: utf-8 -*-
"""Bouwt de statische site van Tandartspraktijk Badhuisplein.

Gebruik (vanuit de projectmap):  python -I _build/build.py
Alle pagina's, sitemap.xml en robots.txt worden opnieuw geschreven.
De URL-structuur volgt de oude WordPress-site, zodat bestaande Google-posities behouden blijven.
"""
import json
import os
import posixpath
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import TEAM, TREATMENTS, T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://praktijkbadhuisplein.nl/"
# Laatste inhoudelijke wijziging. Pas aan als teksten echt veranderen; een datum die bij elke build verspringt, gelooft Google niet.
TODAY = "2026-11-02"
NAME = "Tandartspraktijk Badhuisplein"
TEL = "0523-216967"
TEL_HREF = "tel:+31523216967"
MAIL = "info@praktijkbadhuisplein.nl"
JOBS = "lucette.mondzorg@gmail.com"
AGENDA = "https://internetagenda.vertimart.nl/?id=21330"
INSTA = "https://www.instagram.com/tandartspraktijkbadhuisplein/"
FACEBOOK = "https://www.facebook.com/Tandartspraktijk-Badhuisplein-2297213440556099"
CID = int("0x577c747a3cb8b8c8", 16)
MAPS = f"https://www.google.com/maps?cid={CID}"
MAP_EMBED = "https://www.google.com/maps?q=Tandartspraktijk+Badhuisplein,+Badhuisplein+6,+7772+XC+Hardenberg&output=embed"
ROUTE = "https://www.google.com/maps/dir/?api=1&destination=Tandartspraktijk+Badhuisplein+Badhuisplein+6+7772+XC+Hardenberg"
# Google Maps kent de praktijk onder huisnummer 6; op de site staat, zoals de praktijk zelf schrijft, "2 en 6".
POSTAL = {"@type": "PostalAddress", "streetAddress": "Badhuisplein 6", "postalCode": "7772 XC", "addressLocality": "Hardenberg", "addressRegion": "Overijssel", "addressCountry": "NL"}

TMAP = {t[0]: t for t in TREATMENTS}

# Demo-build (bv. GitHub Pages): BH_DEMO=1 zet noindex op elke pagina zodat de demo niet concurreert met de echte site;
# BH_BASE is het pad waaronder de site draait (voor de 404-pagina), bv. /tandartspraktijk-badhuisplein/
DEMO = os.environ.get("BH_DEMO") == "1"
SITE_BASE = os.environ.get("BH_BASE", "/")


def _v(path):
    import hashlib
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


CSS_V = _v("assets/css/style.css")
JS_V = _v("assets/js/main.js")

PRAKTIJK = [
    ("homepage/praktijkinformatie/", "Over de praktijk"),
    ("homepage/ons-team/", "Ons team"),
    ("cbct-rontgen/", "CBCT-scan (3D-röntgen)"),
    ("vacatures/", "Vacatures"),
]
ZORG = [
    ("de-lieve-tandarts/", "De Lieve Tandarts"),
    ("angst-voor-de-tandarts/", "Angst voor de tandarts"),
    ("behandeling-onder-lachgas/", "Behandeling onder lachgas"),
    ("narcose/", "Behandeling onder narcose"),
    ("kinderen-en-de-tandarts/", "Kinderen en de tandarts"),
    ("patienten-met-een-beperking/", "Patiënten met een beperking"),
]
INFO = [
    ("homepage/spoedgevallen-en-weekenddienst/", "Spoed en weekenddienst"),
    ("homepage/tarieven-en-betaling/", "Tarieven en betaling"),
    ("homepage/betalen-en-vergoedingen/", "Verzekering en vergoedingen"),
    ("homepage/huisregels/", "Huisregels"),
    ("overschrijven/", "Overschrijven"),
    ("cbct-scan-doorverwijzing/", "Voor verwijzers: CBCT"),
    ("doorverwijzing-narcose-voor-behandelaars/", "Voor verwijzers: narcose"),
]

HOURS_ROWS = [
    (1, "Maandag", "08:00-12:00 en 13:00-16:30"),
    (2, "Dinsdag", "08:00-12:00 en 13:00-16:30"),
    (3, "Woensdag", "08:00-12:00 en 13:00-16:30"),
    (4, "Donderdag", "08:00-12:00 en 13:00-16:30"),
    (5, "Vrijdag", "08:30-12:30 en 13:00-16:30"),
    (6, "Zaterdag", None),
    (0, "Zondag", None),
]

# ---------------------------------------------------------------- helpers

def rel(cur, target):
    """Relatieve link van pagina-map `cur` naar `target` (map met / of bestand)."""
    is_dir = target == "" or target.endswith("/")
    t = target.rstrip("/") or "."
    c = cur.rstrip("/") or "."
    r = posixpath.relpath(t, c)
    if is_dir:
        return "./" if r == "." else r + "/"
    return r


def resolve(html, cur):
    html = re.sub(r"\{u:([^}]*)\}", lambda m: rel(cur, m.group(1)), html)
    return re.sub(r"\{a:([^}]*)\}", lambda m: rel(cur, m.group(1)), html)


def icon(name, cls=""):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>' if cls else f'<svg aria-hidden="true"><use href="#i-{name}"/></svg>'


def tico(cur, key):
    u = rel(cur, "assets/img/icons/" + key + ".png")
    return f'<span class="ico" aria-hidden="true"><i style="-webkit-mask-image:url({u});mask-image:url({u})"></i></span>'


STARS = '<span class="stars" aria-hidden="true">' + "".join('<svg><use href="#i-star"/></svg>' for _ in range(4)) + '<span class="hstar"><svg><use href="#i-star"/></svg><svg><use href="#i-star"/></svg></span></span>'

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3.5h3.2l1.6 4.2-2 1.4a11 11 0 0 0 7.1 7.1l1.4-2 4.2 1.6V19a1.8 1.8 0 0 1-1.9 1.8A16.5 16.5 0 0 1 3.2 5.4 1.8 1.8 0 0 1 5 3.5Z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12h15M13.5 6l6 6-6 6"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></symbol>
<symbol id="i-cal" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5 2.8 19.5h18.4L12 3.5Z"/><path d="M12 10v4.2M12 17h.01"/></symbol>
<symbol id="i-insta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor"/></symbol>
<symbol id="i-fb" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14 8.5h2.5V5H14a3.5 3.5 0 0 0-3.5 3.5V11H8v3.5h2.5V21H14v-6.5h2.5L17 11h-3V8.9c0-.2.2-.4.4-.4Z"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path fill="currentColor" d="m12 2.8 2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8L12 2.8Z"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="8" r="3.8"/><path d="M3.5 20a6.5 6.5 0 0 1 13 0M19 8v6M16 11h6"/></symbol>
</svg>"""

# ---------------------------------------------------------------- schema

EXTRA_SERVICES = [("Spark-aligners", "invisalign/"), ("Brackets (vaste beugel)", "bracket-slotjesbeugel/"), ("Behandeling onder lachgas", "behandeling-onder-lachgas/"),
                  ("Behandeling onder narcose", "narcose/"), ("CBCT-scan", "cbct-rontgen/")]


def dentist_schema(full=True):
    d = {
        "@type": "Dentist",
        "@id": BASE + "#praktijk",
        "name": NAME,
        "alternateName": "Tandartsenpraktijk Badhuisplein",
        "url": BASE,
    }
    if not full:
        return d
    d.update({
        "description": "Tandartspraktijk in Hardenberg met het keurmerk De Lieve Tandarts, voor algemene tandheelkunde, implantologie, orthodontie, protheses, esthetiek en preventie. Met eigen CBCT-scanner en tandtechnisch laboratorium; behandeling ook onder lachgas of narcose.",
        "logo": BASE + "assets/img/icon-512.png",
        "image": [BASE + "assets/img/og-badhuisplein.jpg", BASE + "assets/img/gevel.webp"],
        "telephone": "+31523216967",
        "email": MAIL,
        "address": POSTAL,
        "geo": {"@type": "GeoCoordinates", "latitude": 52.5775475, "longitude": 6.618542},
        "hasMap": MAPS,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "12:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "13:00", "closes": "16:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:30", "closes": "12:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "13:00", "closes": "16:30"},
        ],
        "areaServed": [{"@type": "City", "name": n} for n in ["Hardenberg", "Gramsbergen", "Bergentheim", "Slagharen", "Dedemsvaart", "Ommen"]],
        "medicalSpecialty": "Dentistry",
        "isAcceptingNewPatients": True,
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Pin, factuur via Infomedics",
        "sameAs": [INSTA, FACEBOOK, MAPS],
        "priceRange": "Tarieven volgens de NZa",
        "award": "Keurmerk De Lieve Tandarts (sinds 2018)",
        "potentialAction": {"@type": "ReserveAction", "name": "Afspraak maken", "target": {"@type": "EntryPoint", "urlTemplate": AGENDA}},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Behandelingen", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": BASE + u}}
            for n, u in [(T[s]["procedure"], "behandelingen/" + s + "/") for s, *_ in TREATMENTS] + EXTRA_SERVICES
        ]},
    })
    return d


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (p, n) in enumerate(crumbs)]}


def ld(*objs):
    graph = {"@context": "https://schema.org", "@graph": list(objs)}
    return '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>"

# ---------------------------------------------------------------- layout

def head(p):
    cur = p["path"]
    canon = BASE + cur
    title = escape(p["title"])
    desc = escape(p["desc"])
    og_img = BASE + "assets/img/og-badhuisplein.jpg"
    robots = "noindex,follow" if p.get("noindex") else "index,follow,max-image-preview:large,max-snippet:-1"
    if DEMO:
        robots = "noindex,nofollow"
    preload = ""
    if p.get("preload") == "assets/img/hero-poster.webp":
        preload = (f'<link rel="preload" as="image" href="{rel(cur, p["preload"])}" fetchpriority="high" '
                   f'imagesrcset="{rel(cur, "assets/img/hero-poster-800.webp")} 800w, {rel(cur, p["preload"])} 1600w" imagesizes="100vw">\n')
    elif p.get("preload"):
        preload = f'<link rel="preload" as="image" href="{rel(cur, p["preload"])}" fetchpriority="high">\n'
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="nl-NL" href="{canon}">
<meta name="theme-color" content="#1b2134">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="NL-OV">
<meta name="geo.placename" content="Hardenberg">
<meta name="geo.position" content="52.5775475;6.618542">
<meta name="ICBM" content="52.5775475, 6.618542">
<meta property="og:type" content="{p.get('ogtype', 'website')}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{NAME}, Hardenberg">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME} in Hardenberg: op uw gemak bij de tandarts">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel(cur, 'favicon.ico')}" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="{rel(cur, 'assets/img/icon-192.png')}">
<link rel="apple-touch-icon" href="{rel(cur, 'assets/img/apple-touch-icon.png')}">
<link rel="manifest" href="{rel(cur, 'site.webmanifest')}">
<link rel="preload" href="{rel(cur, 'assets/fonts/archivo-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel(cur, 'assets/fonts/worksans-latin.woff2')}" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="{rel(cur, 'assets/css/style.css')}?v={CSS_V}">
{p.get('schema', '')}
</head>"""


def header(p):
    cur = p["path"]
    sect = p.get("section")

    def a(path, label, cls="nav__link"):
        ac = ' aria-current="page"' if path == cur else ""
        return f'<a class="{cls}" href="{rel(cur, path)}"{ac}>{label}</a>'

    mega = "".join(
        f'<a href="{rel(cur, "behandelingen/" + s + "/")}"{" aria-current=\"page\"" if cur == "behandelingen/" + s + "/" else ""}>{tico(cur, ic)}<span>{n}</span><small>{d}</small></a>'
        for s, n, d, ic in TREATMENTS)
    mega += f'<a class="all" href="{rel(cur, "behandelingen/")}">Alle behandelingen bekijken {icon("arrow")}</a>'

    def simple(lst):
        return "".join(f'<a href="{rel(cur, pth)}"{" aria-current=\"page\"" if pth == cur else ""}>{n}</a>' for pth, n in lst)

    def dd(id_, label, inner, mega_=False, key=None):
        act = " is-active" if sect == key else ""
        return (f'<li class="nav__item has-drop"><button class="nav__link{act}" type="button" aria-expanded="false" aria-controls="dd-{id_}">'
                f'{label} {icon("chev")}</button><div class="drop{" drop--mega" if mega_ else ""}" id="dd-{id_}">{inner}</div></li>')

    def mob(label, lst):
        return f'<details><summary>{label} {icon("chev")}</summary><div>{simple(lst)}</div></details>'

    beh_list = [("behandelingen/", "Alle behandelingen")] + [("behandelingen/" + s + "/", n) for s, n, *_ in TREATMENTS]
    return f"""<body>
{SPRITE}
<a class="skip" href="#main">Direct naar de inhoud</a>
<header class="mast">
  <div class="wrap mast__top">
    <div class="mast__visit">
      <span class="status" data-status role="status">Open maandag tot en met vrijdag</span>
      <a href="{MAPS}" rel="noopener" target="_blank">Badhuisplein 2 en 6, Hardenberg</a>
    </div>
    <a class="mast__logo" href="{rel(cur, '')}" aria-label="{NAME}, naar de homepage"><img src="{rel(cur, 'assets/img/logo-licht.png')}" alt="{NAME}" width="580" height="160"></a>
    <div class="mast__act">
      <a class="mast__tel" href="{TEL_HREF}">{icon("phone")}<span>{TEL}</span></a>
      <a class="btn" href="{rel(cur, 'afspraak-maken/')}">Afspraak maken</a>
    </div>
    <a class="mast__call" href="{TEL_HREF}" aria-label="Bel {TEL}">{icon("phone")}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu openen"><span></span></button>
  </div>
  <div class="mast__bar">
    <div class="wrap mast__row">
      <a class="mast__mark" href="{rel(cur, '')}" tabindex="-1" aria-hidden="true"><img src="{rel(cur, 'assets/img/mark-licht.png')}" alt="" width="124" height="114"></a>
      <nav class="nav" aria-label="Hoofdmenu">
        <ul class="nav__list">
          {dd("beh", "Behandelingen", mega, True, "beh")}
          {dd("zorg", "Extra aandacht", simple(ZORG), key="zorg")}
          {dd("praktijk", "Praktijk", simple(PRAKTIJK), key="praktijk")}
          {dd("info", "Patiënteninfo", simple(INFO), key="info")}
          <li class="nav__item">{a("inschrijven-als-nieuwe-patient/", "Nieuwe patiënten")}</li>
          <li class="nav__item">{a("contact/", "Contact")}</li>
        </ul>
      </nav>
      <a class="mast__quick" href="{rel(cur, 'afspraak-maken/')}" tabindex="-1">Afspraak maken</a>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
  {mob("Behandelingen", beh_list)}
  {mob("Extra aandacht", ZORG)}
  {mob("Praktijk", PRAKTIJK)}
  {mob("Patiënteninfo", INFO)}
  <a href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">Nieuwe patiënten {icon("arrow")}</a>
  <a href="{rel(cur, 'contact/')}">Contact {icon("arrow")}</a>
  <div class="drawer__cta">
    <a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a>
    <a class="btn btn--line" href="{TEL_HREF}">{icon("phone")}Bel {TEL}</a>
  </div>
  <p class="drawer__meta"><span class="status" data-status></span><br>Badhuisplein 2 en 6, 7772 XC Hardenberg<br><a href="mailto:{MAIL}">{MAIL}</a></p>
</div>"""


def footer(p):
    cur = p["path"]
    beh = "".join(f'<li><a href="{rel(cur, "behandelingen/" + s + "/")}">{n}</a></li>' for s, n, *_ in TREATMENTS)
    beh += f'<li><a href="{rel(cur, "invisalign/")}">Spark-beugel</a></li><li><a href="{rel(cur, "bracket-slotjesbeugel/")}">Brackets</a></li>'
    prak = "".join(f'<li><a href="{rel(cur, pth)}">{n}</a></li>' for pth, n in ZORG + PRAKTIJK + INFO[:4])
    return f"""<footer class="footer dark">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" href="{rel(cur, '')}" aria-label="{NAME}, homepage"><img src="{rel(cur, 'assets/img/logo-licht.png')}" alt="{NAME}" width="580" height="160" loading="lazy"></a>
        <p>Goede zorg en extra aandacht voor het hele gezin, in Hardenberg. Met het keurmerk De Lieve Tandarts.</p>
        <address style="font-style:normal">
          <p><a href="{MAPS}" rel="noopener" target="_blank">Badhuisplein 2 en 6<br>7772 XC Hardenberg</a></p>
          <p><a href="{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
        </address>
        <div class="social"><a href="{INSTA}" rel="noopener" target="_blank" aria-label="Volg ons op Instagram">{icon("insta")}</a><a href="{FACEBOOK}" rel="noopener" target="_blank" aria-label="Volg ons op Facebook">{icon("fb")}</a><a href="{MAPS}" rel="noopener" target="_blank" aria-label="Bekijk ons op Google Maps">{icon("pin")}</a></div>
      </div>
      <div><h2>Behandelingen</h2><ul>{beh}</ul></div>
      <div><h2>Praktijk</h2><ul>{prak}</ul></div>
      <div><h2>Openingstijden</h2>
        <ul>
          <li>Ma t/m do: 08:00-12:00 / 13:00-16:30</li>
          <li>Vr: 08:30-12:30 / 13:00-16:30</li>
          <li>Za en zo: gesloten</li>
        </ul>
        <p style="margin-top:14px"><a href="{rel(cur, 'afspraak-maken/')}">Afspraak maken</a><br><a href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">Inschrijven als nieuwe patiënt</a></p>
      </div>
    </div>
  </div>
  <div class="wrap footer__bottom">
    <span>© <span data-year>{date.today().year}</span> {NAME}, Hardenberg</span>
    <span class="footer__legal"><a href="{rel(cur, 'privacybeleid/')}">Privacybeleid</a><a href="{rel(cur, 'homepage/huisregels/')}">Huisregels</a><a href="{rel(cur, 'sitemap.xml')}">Sitemap</a></span>
  </div>
</footer>
<div class="mbar"><a class="btn btn--navy" href="{TEL_HREF}">{icon("phone")}Bellen</a><a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a></div>
<script src="{rel(cur, 'assets/js/main.js')}?v={JS_V}" defer></script>
</body>
</html>
"""


def crumbs_html(cur, crumbs):
    items = []
    for i, (pth, n) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{n}</li>')
        else:
            items.append(f'<li><a href="{rel(cur, pth)}">{n}</a></li>')
    return f'<nav class="crumbs" aria-label="Kruimelpad"><ol>{"".join(items)}</ol></nav>'


# Elke soort pagina krijgt een eigen kop, zodat niet alles op hetzelfde sjabloon lijkt.
HERO_KIND = {
    "behandelingen/": "plain",
    "homepage/ons-team/": "team",
    "homepage/praktijkinformatie/": "poster",
    "cbct-rontgen/": "poster",
    "kinderen-en-de-tandarts/": "poster",
    "de-lieve-tandarts/": "poster",
    "homepage/spoedgevallen-en-weekenddienst/": "spoed",
    "contact/": "plain",
    "homepage/tarieven-en-betaling/": "plain",
    "homepage/betalen-en-vergoedingen/": "plain",
    "homepage/huisregels/": "plain",
    "privacybeleid/": "plain",
    "narcose/": "plain",
    "cbct-scan-doorverwijzing/": "plain",
    "doorverwijzing-narcose-voor-behandelaars/": "plain",
    "afspraak-maken/": "form",
    "inschrijven-als-nieuwe-patient/": "form",
    "overschrijven/": "form",
}
POSTER = {
    "homepage/praktijkinformatie/": ("luchtfoto.webp", "Luchtfoto van het pand van Tandartspraktijk Badhuisplein in Hardenberg", "50% 55%"),
    "cbct-rontgen/": ("opg.webp", "Assistente en patiënt bij de Cone Beam CT-scanner in de praktijk", "50% 35%"),
    "kinderen-en-de-tandarts/": ("preventie-kind.webp", "Preventieassistente Roos bij een jong kind in de behandelstoel", "60% 45%"),
    "de-lieve-tandarts/": ("balie.webp", "De balie van de praktijk, met het logo op het glas", "60% 45%"),
}


def page_hero(p, cta=True):
    cur = p["path"]
    kind = HERO_KIND.get(cur) or ("light" if p.get("img") else "plain")
    crumbs = crumbs_html(cur, p["crumbs"])
    btns = ""
    if cta:
        line = "btn--line" if kind in ("poster", "spoed") else "btn--line btn--ink"
        btns = (f'<div class="btn-row"><a class="btn" href="{rel(cur, "afspraak-maken/")}">{icon("cal")}Afspraak maken</a>'
                f'<a class="btn {line}" href="{TEL_HREF}">{icon("phone")}Bel {TEL}</a></div>')
    h1, lead = p["h1"], p["lead"]

    if kind == "light":
        pos = f' style="object-position:{p["img_pos"]}"' if p.get("img_pos") else ""
        img = (f'<figure class="ph__img"><img src="{rel(cur, "assets/img/" + p["img"])}" alt="{escape(p.get("img_alt", ""))}" '
               f'width="480" height="600" fetchpriority="high" decoding="async"{pos}></figure>')
        return f"""<section class="ph ph--light on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__grid">
      <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
      {img}
    </div>
  </div>
</section>"""

    if kind == "poster":
        src, alt, pos = POSTER[cur]
        return f"""<section class="ph ph--poster dark">
  <div class="ph__bg"><img src="{rel(cur, "assets/img/" + src)}" alt="{escape(alt)}" width="1600" height="900" fetchpriority="high" decoding="async" style="object-position:{pos}"></div>
  <div class="wrap">
    {crumbs}
    <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
  </div>
</section>"""

    if kind == "spoed":
        return f"""<section class="ph ph--spoed dark">
  <div class="wrap">
    {crumbs}
    <div class="ph__grid">
      <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p></div>
      <div class="ph__call">
        <p>Tijdens openingstijden</p>
        <a href="{TEL_HREF}">{TEL}</a>
        <p>Buiten openingstijden: Tandartsspoedpraktijk in Zwolle, <a class="ph__call-alt" href="tel:09008602">0900-8602</a>.</p>
      </div>
    </div>
  </div>
</section>"""

    if kind == "team":
        return f"""<section class="ph ph--plain ph--team on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__split">
      <h1>{h1}</h1>
      <div><p class="lead">{lead}</p>{btns}</div>
    </div>
  </div>
  <figure class="ph__pano"><img src="{rel(cur, "assets/img/team-panorama.webp")}" alt="Het team van Tandartspraktijk Badhuisplein op de brug in Hardenberg" width="1920" height="350" fetchpriority="high" decoding="async"></figure>
</section>"""

    if kind == "form":
        return f"""<section class="ph ph--form dark">
  <div class="wrap">
    {crumbs}
    <div class="ph__copy"><h1>{h1}</h1><p class="lead">{lead}</p></div>
  </div>
</section>"""

    return f"""<section class="ph ph--plain on-light">
  <div class="wrap">
    {crumbs}
    <div class="ph__split">
      <h1>{h1}</h1>
      <div><p class="lead">{lead}</p>{btns}</div>
    </div>
  </div>
</section>"""


def aside(p, nav=None):
    cur = p["path"]
    hours = "".join(f'<li data-day="{d}"><span>{n[:2]}</span><span>{h.replace(" en ", "<br>") if h else "gesloten"}</span></li>' for d, n, h in HOURS_ROWS[:5])
    navhtml = ""
    if nav:
        navhtml = '<div class="card"><h2>' + nav[0] + '</h2><nav aria-label="' + nav[0] + '"><ul>' + "".join(
            f'<li><a href="{rel(cur, pth)}"{" aria-current=\"page\"" if pth == cur else ""}>{n}</a></li>' for pth, n in nav[1]) + "</ul></nav></div>"
    return f"""<aside class="aside" aria-label="Afspraak en openingstijden">
  <div class="card dark">
    <h2>Afspraak maken</h2>
    <p>Direct inplannen in onze online agenda kan altijd. Bellen kan ma t/m vr tijdens onze openingstijden.</p>
    <a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a>
    <a class="btn btn--line" href="{TEL_HREF}">{icon("phone")}{TEL}</a>
  </div>
  <div class="card">
    <h2>Openingstijden</h2>
    <p><span class="status" data-status></span></p>
    <ul class="mini-hours">{hours}</ul>
    <a class="link" href="{rel(cur, 'homepage/spoedgevallen-en-weekenddienst/')}">Spoed buiten openingstijden {icon("arrow")}</a>
  </div>
  {navhtml}
</aside>"""


def cta_band(cur, title="Klaar voor een gezonde glimlach?", text="Bel ons, plan direct in onze online agenda of schrijf u in als nieuwe patiënt. We nemen weer nieuwe patiënten aan."):
    return f"""<section class="cta-band dark">
  <div class="wrap">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn" href="{rel(cur, 'afspraak-maken/')}">{icon("cal")}Afspraak maken</a><a class="btn btn--line" href="{rel(cur, 'inschrijven-als-nieuwe-patient/')}">{icon("user")}Inschrijven</a></div>
  </div>
</section>"""


def who_html(cur, keys, label="Uw behandelaar"):
    out = []
    for k in keys:
        n, role, _ = TEAM[k]
        out.append(f'<div class="who"><img src="{rel(cur, "assets/img/team/" + k + ".webp")}" alt="{escape(n)}" width="84" height="84" loading="lazy" decoding="async">'
                   f'<div><small>{label}</small><b><a href="{rel(cur, "homepage/ons-team/")}#team-{k}">{n}</a></b><span>{role}</span></div></div>')
    return '<div class="who-row">' + "".join(out) + "</div>"


def faq_html(faq):
    items = "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in faq)
    return f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Veelgestelde vragen</h2>{items}</section>'


def faq_schema(url, faq):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def hours_table():
    rows = []
    for d, n, h in HOURS_ROWS:
        rows.append(f'<tr data-day="{d}"><th scope="row">{n}</th>' + (f"<td>{h} uur</td>" if h else '<td class="closed">Gesloten</td>') + "</tr>")
    return f'<table class="hours"><caption class="sr-only">Openingstijden van de praktijk</caption>{"".join(rows)}</table>'


def contact_dl(cur):
    return f"""<dl class="dl">
  <div>{icon("pin")}<div><dt>Adres</dt><dd><a href="{MAPS}" rel="noopener" target="_blank">Badhuisplein 2 en 6, 7772 XC Hardenberg</a></dd></div></div>
  <div>{icon("phone")}<div><dt>Telefoon</dt><dd><a href="{TEL_HREF}">{TEL}</a><span class="dl__note">Tijdens onze openingstijden. Verplaatsen of afzeggen kan alleen telefonisch.</span></dd></div></div>
  <div>{icon("mail")}<div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div></div>
</dl>"""


def map_block():
    return f"""<div class="map">
  <div>
    {icon("pin", "")}
    <h3>Badhuisplein 2 en 6, Hardenberg</h3>
    <p>De kaart wordt geladen via Google Maps. Daarbij kan Google gegevens verwerken.</p>
    <div class="btn-row" style="justify-content:center"><button class="btn" type="button" data-map="{MAP_EMBED}">Kaart laden</button><a class="btn btn--line" href="{ROUTE}" rel="noopener" target="_blank">Route plannen</a></div>
  </div>
</div>"""


def write(p, main):
    cur = p["path"]
    html = head(p) + "\n" + header(p) + '\n<main id="main">\n' + main + "\n</main>\n" + footer(p)
    html = resolve(html, cur)
    html = re.sub(r'<em class="g">(.*?)</em>', r"\1", html)
    out = ROOT / (cur + "index.html" if cur.endswith("/") or cur == "" else cur)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    PAGES.append(p)


PAGES = []

# ---------------------------------------------------------------- formulieren

def field(name, label, typ="text", req=True, full=False, ac=None, opts=None, err=None, hint=None, attrs=""):
    cls = "field full" if full else "field"
    r = " required" if req else ""
    opt = "" if req else ' <span class="opt">(optioneel)</span>'
    ac_ = f' autocomplete="{ac}"' if ac else ""
    err = err or "Vul dit veld in."
    hint_html = f'<small class="hint" id="{name}-h">{hint}</small>' if hint else ""
    desc = f' aria-describedby="{name}-h"' if hint else ""
    if typ == "select":
        o = "".join(f'<option value="{v}">{t}</option>' for v, t in opts)
        ctl = f'<select id="{name}" name="{name}"{r}{attrs}><option value="">Maak een keuze</option>{o}</select>'
    elif typ == "textarea":
        ctl = f'<textarea id="{name}" name="{name}"{r}{desc}{attrs}></textarea>'
    else:
        ctl = f'<input id="{name}" name="{name}" type="{typ}"{r}{ac_}{desc}{attrs}>'
    return f'<div class="{cls}"><label for="{name}">{label}{opt}</label>{ctl}{hint_html}<span class="err">{err}</span></div>'


def checks(name, legend, vals):
    boxes = "".join(f'<label class="chip"><input type="checkbox" name="{name}" value="{v}"><span>{v}</span></label>' for v in vals)
    return f'<div class="field full"><fieldset><legend>{legend} <span class="opt">(optioneel)</span></legend><div class="chips">{boxes}</div></fieldset></div>'


def choice(name, legend, opts, param=None):
    """Een verplichte keuze als knoppen (radio's); de waarde blijft de code die ook ?soort= gebruikt."""
    dp = f' data-param="{param}"' if param else ""
    items = "".join(f'<label class="chip"><input type="radio" name="{name}" value="{v}" required><span>{t}</span></label>' for v, t in opts)
    return f'<div class="field full"><fieldset{dp}><legend>{legend}</legend><div class="chips">{items}</div></fieldset><span class="err">Maak een keuze.</span></div>'


def group(title, inner):
    return f'<fieldset class="fgroup full"><legend class="fgroup__t">{title}</legend><div class="fgroup__b">{inner}</div></fieldset>'


def form_page(cur, crumbs, title, desc, h1, lead, side, form, form_title, img=None, img_alt=None, before="", form_id=None):
    """Een formulierpagina: korte kop, links de praktische info, rechts het formulier."""
    url = BASE + cur
    p = dict(path=cur, title=title, desc=desc, h1=h1, lead=lead, crumbs=crumbs, img=img, img_alt=img_alt)
    p["schema"] = ld({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "nl-NL",
                      "dateModified": TODAY, "publisher": {"@id": BASE + "#praktijk"}}, breadcrumb_schema(crumbs), dentist_schema(False))
    main = page_hero(p, cta=False) + f"""
<section class="fp section on-light">
  <div class="wrap fp__grid">
    <aside class="fp__side" aria-label="Praktische informatie">{side}</aside>
    <div class="fp__main">{before}<h2{f' id="{form_id}"' if form_id else ""}>{form_title}</h2>{form}</div>
  </div>
</section>"""
    write(p, main)


def consent(cur):
    return (f'<div class="field full"><label class="consent"><input type="checkbox" name="akkoord" required> '
            f'<span>Ik ga akkoord met de verwerking van mijn gegevens volgens de <a href="{rel(cur, "privacybeleid/")}">privacybeleid</a>.</span></label>'
            f'<span class="err">Geef toestemming om uw aanvraag te kunnen versturen.</span></div>')


def form_wrap(cur, subject, inner, ok, button):
    return (f'<form class="form" data-form="{subject}" action="mailto:{MAIL}" method="post">{inner}{consent(cur)}'
            f'<div class="full"><button class="btn btn--navy" type="submit">{button} {icon("arrow")}</button></div>'
            f'<p class="form__ok" role="status">{ok}</p><p class="form__err" role="alert" hidden>Versturen is niet gelukt. Bel ons gerust op {TEL}.</p></form>')

# ================================================================= PAGINA'S

def hero_media(cur):
    """Achtergrondvideo van de hero. Zet de video van de praktijk in assets/video/ als hero.mp4 (en eventueel hero.webm);
    zolang die er niet is, toont de hero de poster (assets/img/hero-poster.webp)."""
    vid = ROOT / "assets" / "video"
    sources = ""
    if (vid / "hero.webm").exists():
        sources += f'<source src="{rel(cur, "assets/video/hero.webm")}" type="video/webm">'
    if (vid / "hero.mp4").exists():
        sources += f'<source src="{rel(cur, "assets/video/hero.mp4")}" type="video/mp4">'
    poster = rel(cur, "assets/img/hero-poster.webp")
    if not sources:
        return (f'<div class="hx__media" aria-hidden="true"><img src="{poster}" srcset="{rel(cur, "assets/img/hero-poster-800.webp")} 800w, {poster} 1600w" sizes="100vw" alt="" width="1600" height="900" '
                f'fetchpriority="high" decoding="async"></div>')
    return (f'<div class="hx__media" aria-hidden="true"><video class="hx__video" autoplay muted loop playsinline '
            f'preload="metadata" poster="{poster}" data-hero-video>{sources}</video></div>'
            f'<button class="hx__pause" type="button" aria-pressed="false" data-hero-pause>'
            f'<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M8 5v14M16 5v14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            f'<span>Video pauzeren</span></button>')


HOME_FAQ = [
    ("Neemt Tandartspraktijk Badhuisplein nieuwe patiënten aan?", 'Ja, wij nemen weer nieuwe patiënten aan. <a href="{u:inschrijven-als-nieuwe-patient/}">Schrijf u online in</a>, dan nodigen we u uit voor een eerste consult. Bent u patiënt bij een andere tandarts, dan kunt u zich ook <a href="{u:overschrijven/}">laten overschrijven</a>.'),
    ("Hoe maak ik een afspraak bij de tandarts in Hardenberg?", 'Plan direct in onze <a href="{u:afspraak-maken/}">online agenda</a> of bel 0523-216967. Verplaatsen of afzeggen kan alleen telefonisch, minstens 48 uur van tevoren.'),
    ("Wat zijn de openingstijden?", "Maandag tot en met donderdag van 08:00 tot 12:00 en van 13:00 tot 16:30 uur. Vrijdag van 08:30 tot 12:30 en van 13:00 tot 16:30 uur."),
    ("Wat moet ik doen bij kiespijn of spoed?", 'Bel tijdens openingstijden 0523-216967, indien mogelijk tussen 08:30 en 10:00 uur. Buiten openingstijden kunt u terecht bij de <a href="{u:homepage/spoedgevallen-en-weekenddienst/}">Tandartsspoedpraktijk in Zwolle</a>, telefoon 0900-8602.'),
    ("Ik ben bang voor de tandarts. Kunt u mij helpen?", 'Ja. Sinds 2018 hebben we het keurmerk <a href="{u:de-lieve-tandarts/}">De Lieve Tandarts</a>. We plannen zo nodig extra tijd in en leggen uit wat we doen. Een behandeling kan ook <a href="{u:behandeling-onder-lachgas/}">onder lachgas</a> of <a href="{u:narcose/}">onder narcose</a>.'),
    ("Waar zit de praktijk?", 'Aan het Badhuisplein 2 en 6 in Hardenberg. Ook als u in de omgeving woont, bijvoorbeeld in Gramsbergen, Bergentheim, Slagharen, Dedemsvaart of Ommen, bent u van harte welkom. <a href="{u:contact/}">Bekijk de route</a>.'),
]


def home():
    cur = ""
    p = dict(path=cur, title="Tandarts Hardenberg | Tandartspraktijk Badhuisplein",
             desc="Tandarts in Hardenberg met het keurmerk De Lieve Tandarts: controle, implantaten, Invisalign, kronen op één dag en lachgas. Nieuwe patiënten welkom.",
             preload="assets/img/hero-poster.webp")
    p["schema"] = ld(dentist_schema(), {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": NAME, "inLanguage": "nl-NL", "publisher": {"@id": BASE + "#praktijk"}},
                     {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": p["title"], "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#praktijk"}, "inLanguage": "nl-NL", "dateModified": TODAY},
                     {"@type": "FAQPage", "@id": BASE + "#home-faq", "mainEntity": [
                         {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in HOME_FAQ]})
    index = "".join(
        f'<li><a href="{{u:behandelingen/{s}/}}"><span class="hx__name">{n.replace("Wortelkanaalbehandeling", "Wortelkanaal&shy;behandeling")}</span>{icon("arrow", "hx__arr")}</a></li>'
        for s, n, d, ic in TREATMENTS)
    team = "".join(
        f'<figure class="person"><img src="{{a:assets/img/team/{k}.webp}}" alt="{escape(n)}, {escape(r.lower())}" width="480" height="720" loading="lazy" decoding="async"><figcaption><b>{n}</b><span>{r}</span></figcaption></figure>'
        for k, (n, r, _) in TEAM.items())
    week = ""
    for d, n, h in HOURS_ROWS:
        times = "".join(f"<span>{t.replace(' – ', '-')}</span>" for t in h.split(" en ")) if h else '<span class="week__closed">Gesloten</span>'
        week += f'<li data-day="{d}"{" class=\"is-closed\"" if not h else ""}><b>{n}</b>{times}</li>'
    main = f"""
<section class="hx dark" aria-labelledby="hero-h">
  {hero_media(cur)}
  <div class="wrap">
    <div class="hx__head">
      <h1 id="hero-h">Op uw gemak bij de <br>tandarts in <em class="sig">Hardenberg.</em></h1>
      <div class="hx__side">
        <p class="lead">Een klantgerichte praktijk met het keurmerk De Lieve Tandarts. Nieuwe patiënten zijn welkom.</p>
        <div class="btn-row">
          <a class="btn" href="{{u:afspraak-maken/}}">{icon("cal")}Afspraak maken</a>
          <a class="btn btn--line" href="{{u:inschrijven-als-nieuwe-patient/}}">{icon("user")}Inschrijven</a>
        </div>
      </div>
    </div>
    <nav class="hx__index" aria-label="Behandelingen">
      <ul>{index}</ul>
      <a class="hx__all" href="{{u:behandelingen/}}">Alle behandelingen met uitleg en vergoeding</a>
    </nav>
  </div>
</section>

<section class="pk section on-light" aria-labelledby="intro-h">
  <div class="wrap">
    <div class="pk__head rv">
      <h2 id="intro-h">Alle zorg voor uw gebit, onder één dak in Hardenberg.</h2>
      <div>
        <p class="lead">Bij Tandartspraktijk Badhuisplein kunt u terecht voor alle voorkomende tandheelkundige behandelingen, esthetische tandheelkunde, orthodontie en implantologie. Preventie neemt daarbij een centrale plaats in.</p>
        <p>Tandartsen, preventieassistentes, tandprothetici en een tandtechnieker werken hier nauw samen. Een 3D-scan maken we zelf, een normale kroon is meestal dezelfde dag klaar en uw prothese repareren we in ons eigen laboratorium.</p>
        <p><a class="link" href="{{u:homepage/praktijkinformatie/}}">Meer over de praktijk {icon("arrow")}</a></p>
      </div>
    </div>
    <div class="pk__pics rv">
      <figure class="pk__wide"><img src="{{a:assets/img/gevel.webp}}" alt="De gevel van Tandartspraktijk Badhuisplein in Hardenberg" width="950" height="634" loading="lazy" decoding="async"><figcaption><b>Badhuisplein 2 en 6, in Hardenberg.</b> In huis: een 3D CBCT-scanner en een eigen tandtechnisch laboratorium voor kronen, bruggen en protheses.</figcaption></figure>
      <figure class="pk__tall"><img src="{{a:assets/img/balie-team.webp}}" alt="Twee medewerkers van de praktijk aan de balie" width="950" height="1424" loading="lazy" decoding="async"><figcaption><b>Aan de balie begint uw bezoek.</b> Vertel het ons gerust als u het spannend vindt, dan houden we daar rekening mee.</figcaption></figure>
    </div>
  </div>
</section>

<section class="section section--sand on-light" aria-labelledby="zorg-h">
  <div class="wrap">
    <div class="section__head rv"><div><h2 id="zorg-h">Extra aandacht voor wie het spannend vindt, en voor kinderen.</h2></div></div>
    <div class="stories">
      <a class="story story--a rv" href="{{u:kinderen-en-de-tandarts/}}">
        <img src="{{a:assets/img/kinderen.webp}}" alt="Preventieassistente met een jong meisje in de behandelstoel" width="950" height="634" loading="lazy" decoding="async">
        <div class="story__body"><h3>Kinderen en de tandarts</h3><p>Vanaf twee jaar mag uw kind mee om rustig te wennen. Alles is vrijblijvend: lukt het niet, dan een volgende keer beter.</p><span class="link">Tips voor ouders {icon("arrow")}</span></div>
      </a>
      <a class="story story--b story--dark story--quote rv rv-d1" href="{{u:de-lieve-tandarts/}}">
        <div class="story__body"><blockquote>Laat ons weten hoe we u het beste kunnen helpen.</blockquote><p>Sinds 2018 hebben we het keurmerk De Lieve Tandarts, als eerste praktijk in Overijssel. We plannen zo nodig extra tijd in en leggen uit wat we doen. Ook lachgas en narcose zijn mogelijk.</p><span class="link">Over De Lieve Tandarts {icon("arrow")}</span></div>
      </a>
      <a class="story story--c rv" href="{{u:cbct-rontgen/}}">
        <img src="{{a:assets/img/opg.webp}}" alt="Assistente en patiënt bij de Cone Beam CT-scanner in de praktijk" width="950" height="634" loading="lazy" decoding="async">
        <div class="story__body"><h3>3D CBCT-scan in huis</h3><p>Minder straling dan een normale CT-scan en direct een betrouwbaar 3D-beeld. Ook voor verwijzende behandelaars.</p><span class="link">Over de CBCT-scan {icon("arrow")}</span></div>
      </a>
      <a class="story story--d rv rv-d1" href="{{u:behandelingen/othodontie-en-invisalign/}}">
        <img src="{{a:assets/img/invisalign.webp}}" alt="Doorzichtige aligner wordt op de tanden geplaatst" width="576" height="376" loading="lazy" decoding="async">
        <div class="story__body"><h3>Invisalign, Spark of brackets</h3><p>Onzichtbare aligners of een vaste beugel: tijdens een gratis intake kijken we wat bij u past.</p><span class="link">Meer over orthodontie {icon("arrow")}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper on-light" aria-labelledby="team-h">
  <div class="wrap">
    <div class="section__head rv">
      <div><h2 id="team-h">Ons team</h2><p>Negentien collega’s die elke dag klaarstaan voor uw mondgezondheid, van de balie tot het laboratorium.</p></div>
      <div class="team-head__act">
        <a class="link" href="{{u:homepage/ons-team/}}">Maak kennis met het team {icon("arrow")}</a>
        <div class="rail-nav"><button type="button" data-rail="-1" aria-controls="team-strip" aria-label="Vorige teamleden"><svg aria-hidden="true"><use href="#i-arrow"/></svg></button><button type="button" data-rail="1" aria-controls="team-strip" aria-label="Volgende teamleden"><svg aria-hidden="true"><use href="#i-arrow"/></svg></button></div>
      </div>
    </div>
    <div class="team-strip" id="team-strip" tabindex="0" aria-label="Teamleden, veeg of scroll horizontaal">{team}</div>
  </div>
</section>

<section class="np section on-light" aria-labelledby="nieuw-h">
  <div class="wrap np__grid">
    <figure class="np__pic rv"><img src="{{a:assets/img/wachtkamer.webp}}" alt="Een medewerker van de praktijk begroet een patiënte in de wachtkamer" width="950" height="634" loading="lazy" decoding="async"><figcaption>Welkom in onze wachtkamer aan het Badhuisplein</figcaption></figure>
    <div class="np__body rv rv-d1">
      <h2 id="nieuw-h">Nieuwe patiënten</h2>
      <p class="lead">Wij nemen weer nieuwe patiënten aan.</p>
      <ol class="np__list">
        <li><h3>Schrijf u in</h3><p>Vul het online formulier in. Heeft u nu een andere tandarts? Dan kunt u zich ook laten overschrijven.</p></li>
        <li><h3>U krijgt een uitnodiging</h3><p>Nadat u zich heeft ingeschreven, nodigen we u uit voor een eerste consult.</p></li>
        <li><h3>Eerste consult</h3><p>U vertelt wat uw wensen en klachten zijn. We bespreken uw medische vragenlijst, onderzoeken uw mond en maken digitale röntgenfoto’s.</p></li>
      </ol>
      <a class="btn btn--navy" href="{{u:inschrijven-als-nieuwe-patient/}}">{icon("user")}Nu inschrijven</a>
      <p class="np__proof">{STARS}<span><b>4,5 van 5</b> gemiddeld in 48 Google-reviews</span><a class="link" href="{MAPS}" rel="noopener" target="_blank">Lees de reviews op Google {icon("arrow")}</a></p>
    </div>
  </div>
</section>

<section class="section section--paper on-light" aria-labelledby="vragen-h">
  <div class="wrap">
    <div class="faq faq--home rv">
      <h2 id="vragen-h">Veelgestelde vragen over onze praktijk in Hardenberg</h2>
      {"".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in HOME_FAQ)}
    </div>
  </div>
</section>

<section class="cl dark" aria-labelledby="contact-h">
  <div class="wrap cl__grid">
    <div class="cl__info">
      <h2 id="contact-h">Contact en openingstijden</h2>
      <p class="lead">U vindt ons aan het Badhuisplein 2 en 6 in Hardenberg.</p>
      {contact_dl(cur)}
      <p><a class="link" href="{{u:contact/}}">Alle contactgegevens {icon("arrow")}</a></p>
    </div>
    <div class="cl__book">
      <p class="cl__now"><span class="status" data-status></span></p>
      <ol class="week" aria-label="Openingstijden per dag">{week}</ol>
      <div class="cl__intake">
        <h3>Gratis intake orthodontie</h3>
        <p>Invisalign, Spark of brackets: wat past bij u? Laat het ons weten, dan nemen wij contact met u op voor een gratis intake.</p>
        <div class="cl__choices">
          <a class="btn btn--line" href="{{u:afspraak-maken/}}?soort=intake-orthodontie#formulier">Gratis intake aanvragen</a>
          <a class="btn btn--line" href="{{u:behandelingen/othodontie-en-invisalign/}}">Meer over orthodontie</a>
        </div>
      </div>
      <a class="btn cl__cta" href="{{u:afspraak-maken/}}">{icon("cal")}Afspraak maken</a>
      <p class="cl__spoed">{icon("alert")}<span><b>Pijn of spoed?</b> Bel indien mogelijk tussen 08:30 en 10:00 uur, dan proberen we u dezelfde dag nog te helpen. <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">Wat te doen buiten openingstijden</a></span></p>
    </div>
  </div>
  <div class="wrap cl__map">{map_block()}</div>
</section>
"""
    write(p, main)


def treatment_pages():
    for s, n, d, ic in TREATMENTS:
        t = T[s]
        cur = f"behandelingen/{s}/"
        url = BASE + cur
        crumbs = [("", "Home"), ("behandelingen/", "Behandelingen"), (cur, n)]
        p = dict(path=cur, title=t["title"], desc=t["desc"], h1=t["h1"], lead=t["lead"], img=t.get("img"), img_alt=t.get("img_alt"), img_pos=t.get("img_pos"),
                 crumbs=crumbs, section="beh", preload="assets/img/" + t["img"] if t.get("img") else None, ogtype="article")
        p["schema"] = ld(
            {"@type": "MedicalWebPage", "@id": url + "#webpage", "url": url, "name": t["title"], "description": t["desc"], "inLanguage": "nl-NL",
             "dateModified": TODAY,
             "about": {"@type": "MedicalProcedure", "name": t["procedure"]},
             "publisher": {"@id": BASE + "#praktijk"}, "breadcrumb": {"@id": url + "#breadcrumb"}},
            dict(breadcrumb_schema(crumbs), **{"@id": url + "#breadcrumb"}),
            faq_schema(url, t["faq"]),
            dentist_schema(False))
        rel_items = "".join(
            f'<a href="{{u:behandelingen/{r}/}}">{tico(cur, TMAP[r][3])}<b>{TMAP[r][1]}</b></a>' for r in t["related"])
        main = page_hero(p) + f"""
<section class="section on-light">
  <div class="wrap layout">
    <article class="prose">
      {t["body"]}
      {who_html(cur, t["who"], "Uw behandelaar" if len(t["who"]) == 1 else "Behandeld door")}
      {faq_html(t["faq"])}
    </article>
    {aside(p, ("Behandelingen", [("behandelingen/" + x, y) for x, y, *_ in TREATMENTS]))}
  </div>
</section>
<section class="section section--sand on-light" style="padding-block:clamp(48px,6vw,80px)">
  <div class="wrap">
    <h2 style="font-size:clamp(1.6rem,2.6vw,2.2rem)">Gerelateerde behandelingen</h2>
    <div class="related">{rel_items}</div>
  </div>
</section>
""" + cta_band(cur)
        write(p, main)


def behandelingen_index():
    cur = "behandelingen/"
    crumbs = [("", "Home"), (cur, "Behandelingen")]
    p = dict(path=cur, title="Behandelingen | Tandarts Hardenberg | Badhuisplein",
             desc="Alle behandelingen van Tandartspraktijk Badhuisplein in Hardenberg: implantaten, Invisalign, kronen en bruggen, protheses, bleken, vullingen en preventie.",
             h1='Behandelingen bij uw tandarts in <em class="g">Hardenberg</em>',
             lead="Algemene tandheelkunde, esthetiek, orthodontie en implantologie onder één dak. Hieronder vindt u per behandeling uitleg over het verloop, de mogelijkheden en de vergoeding.",
             crumbs=crumbs, section="beh")
    p["schema"] = ld({"@type": "CollectionPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL",
                      "hasPart": [{"@type": "MedicalWebPage", "url": BASE + "behandelingen/" + s + "/", "name": n} for s, n, *_ in TREATMENTS]},
                     breadcrumb_schema(crumbs), dentist_schema(False))
    tlist = "".join(
        f'<li class="rv"><a href="{{u:behandelingen/{s}/}}">{tico(cur, ic)}<div><h2>{n}</h2><p>{d}</p></div>{icon("arrow", "arr")}</a></li>'
        for s, n, d, ic in TREATMENTS)
    main = page_hero(p) + f"""
<section class="section on-light"><div class="wrap"><ul class="tlist">{tlist}</ul>
<div class="note" style="margin-top:48px;max-width:760px"><p><b>Op zoek naar een beugel?</b> Lees ook over de <a href="{{u:invisalign/}}">onzichtbare Spark-beugel</a> en over <a href="{{u:bracket-slotjesbeugel/}}">brackets</a>.</p><p><b>Spannend?</b> Veel behandelingen kunnen ook <a href="{{u:behandeling-onder-lachgas/}}">onder lachgas</a> of <a href="{{u:narcose/}}">narcose</a>. Vraag er gerust naar.</p><p><b>Tarieven.</b> Voor alle behandelingen gelden de tarieven die jaarlijks door de Nederlandse Zorgautoriteit (NZa) worden vastgesteld. U kunt vooraf een begroting krijgen. Lees meer over <a href="{{u:homepage/tarieven-en-betaling/}}">tarieven en betaling</a> en <a href="{{u:homepage/betalen-en-vergoedingen/}}">vergoedingen</a>.</p></div>
</div></section>""" + cta_band(cur)
    write(p, main)


def team_page():
    cur = "homepage/ons-team/"
    crumbs = [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), (cur, "Ons team")]
    p = dict(path=cur, title="Ons team | Tandartsen in Hardenberg | Badhuisplein",
             desc="Maak kennis met het team van Tandartspraktijk Badhuisplein in Hardenberg: tandartsen, preventieassistentes, tandprotheticus, tandtechnieker en balie.",
             h1='Maak kennis met <em class="g">ons team</em>', lead="Negentien collega’s, één doel: dat u zich bij ons op uw gemak voelt en een gezond gebit houdt. U ziet hier wie u tegenkomt, van de balie tot de behandelstoel.",
             crumbs=crumbs, section="praktijk")
    people = [{"@type": "Person", "name": n, "jobTitle": r, "image": BASE + "assets/img/team/" + k + ".webp", "worksFor": {"@id": BASE + "#praktijk"}} for k, (n, r, _) in TEAM.items()]
    p["schema"] = ld({"@type": "AboutPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL", "about": {"@id": BASE + "#praktijk"}},
                     breadcrumb_schema(crumbs), dict(dentist_schema(False), employee=people))
    groups = [("tandarts", "Tandartsen"), ("mondzorg", "Preventie en assistentie"), ("prothetiek", "Prothetiek en tandtechniek"), ("balie", "Balie en praktijkmanagement")]
    html = ""
    for g, label in groups:
        figs = "".join(
            f'<figure class="person rv" id="team-{k}"><img src="{{a:assets/img/team/{k}.webp}}" alt="{escape(n)}, {escape(r.lower())}" width="480" height="720" loading="lazy" decoding="async"><figcaption><b>{n}</b><span>{r}</span></figcaption></figure>'
            for k, (n, r, gg) in TEAM.items() if gg == g)
        html += f'<div class="team-group"><h2>{label}</h2><div class="team-grid">{figs}</div></div>'
    main = page_hero(p) + f"""<section class="section on-light"><div class="wrap">
<div class="team-intro"><h2>Wie werkt er bij Tandartspraktijk Badhuisplein?</h2>
<p>In onze praktijk in Hardenberg werken vier tandartsen, met aandachtsgebieden als implantologie, orthodontie en esthetiek. Ons preventieteam van preventie- en paro-preventieassistentes helpt u met gebitsreiniging en persoonlijk advies. Voor protheses en tandtechnisch werk werken we samen met een tandprotheticus en een tandtechnieker in ons eigen laboratorium. Aan de balie staan onze baliemedewerksters en praktijkmanager Lucette voor u klaar.</p>
<p>Sinds 2018 hebben we het keurmerk <a href="{{u:de-lieve-tandarts/}}">De Lieve Tandarts</a>: een team dat altijd rekening houdt met kinderen en met mensen die het spannend vinden om naar de tandarts te gaan.</p></div>
{html}
<div class="note" style="margin-top:56px;max-width:760px"><p><b>Werken bij Badhuisplein?</b> Bekijk de <a href="{{u:vacatures/}}">vacatures</a>.</p></div>
</div></section>""" + cta_band(cur)
    write(p, main)


def text_page(cur, crumbs, section, title, desc, h1, lead, body, img=None, img_alt=None, img_pos=None, nav=None, faq=None, extra_schema=None, cta=True, after="", medical=None):
    url = BASE + cur
    p = dict(path=cur, title=title, desc=desc, h1=h1, lead=lead, crumbs=crumbs, section=section, img=img, img_alt=img_alt, img_pos=img_pos)
    page = {"@type": "MedicalWebPage" if medical else "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "nl-NL", "dateModified": TODAY, "publisher": {"@id": BASE + "#praktijk"}}
    if medical:
        page["about"] = {"@type": "MedicalProcedure", "name": medical}
    objs = [page, breadcrumb_schema(crumbs)]
    if faq:
        objs.append(faq_schema(url, faq))
    objs.extend(extra_schema or [dentist_schema(False)])
    p["schema"] = ld(*objs)
    main = page_hero(p) + f"""
<section class="section on-light">
  <div class="wrap layout">
    <article class="prose">{body}{faq_html(faq) if faq else ""}</article>
    {aside(p, nav)}
  </div>
</section>{after}""" + (cta_band(cur) if cta else "")
    write(p, main)


PRAKTIJK_NAV = ("Praktijk", PRAKTIJK)
ZORG_NAV = ("Extra aandacht", ZORG)
INFO_NAV = ("Patiënteninfo", INFO)
ORTHO_NAV = ("Orthodontie", [("behandelingen/othodontie-en-invisalign/", "Orthodontie en Invisalign"), ("invisalign/", "Spark-beugel"), ("bracket-slotjesbeugel/", "Brackets")])


def other_pages():
    # Over de praktijk
    text_page("homepage/praktijkinformatie/", [("", "Home"), ("homepage/praktijkinformatie/", "Over de praktijk")], "praktijk",
              "Over de praktijk | Tandartspraktijk Badhuisplein Hardenberg",
              "Tandartspraktijk Badhuisplein in Hardenberg: tandheelkunde, esthetiek, orthodontie en implantologie, met keurmerk De Lieve Tandarts, CBCT en eigen lab.",
              'Welkom bij Tandartspraktijk <em class="g">Badhuisplein</em>',
              "Een klantgerichte praktijk in Hardenberg voor alle voorkomende tandheelkundige behandelingen, esthetische tandheelkunde, orthodontie en implantologie.",
              f"""
<h2>De wensen van de patiënt staan centraal</h2>
<p>Bij Tandartspraktijk Badhuisplein kunt u terecht voor alle voorkomende tandheelkundige behandelingen, esthetische tandheelkunde, orthodontie en implantologie. Preventie neemt daarbij een centrale plaats in: we helpen u liever een gezond gebit te houden dan dat we later moeten behandelen.</p>
<p>Sinds 2018 hebben we als eerste praktijk in Overijssel het keurmerk <a href="{{u:de-lieve-tandarts/}}">De Lieve Tandarts</a>. Een lief team houdt altijd rekening met kinderen, en er is volop ervaring en begeleiding voor mensen die vanwege angst het moeilijk vinden om naar de tandarts te gaan.</p>
<figure><img src="{{a:assets/img/gevel.webp}}" alt="De gevel van Tandartspraktijk Badhuisplein in Hardenberg" width="950" height="634" loading="lazy" decoding="async"><figcaption>Onze praktijk aan het Badhuisplein 2 en 6 in Hardenberg.</figcaption></figure>
<h2>Alles onder één dak</h2>
<ul class="types">
  <li><b>Vier tandartsen</b><span>Met aandachtsgebieden als implantologie, orthodontie en esthetiek.</span></li>
  <li><b>Preventieteam</b><span>Preventie- en paro-preventieassistentes voor gebitsreiniging en persoonlijk advies.</span></li>
  <li><b>Tandtechnisch laboratorium</b><span>Tandtechnische werkstukken maken we in ons eigen laboratorium.</span></li>
  <li><b>Kroon vaak op één dag</b><span>Na een scan kan een normale kroon meestal dezelfde dag worden geplaatst.</span></li>
  <li><b>CBCT-scanner</b><span>3D-röntgenbeelden voor implantaten, orthodontie en meer.</span></li>
  <li><b>Lachgas en narcose</b><span>Voor wie een behandeling erg spannend vindt.</span></li>
</ul>
<h2>Tandprothetische Praktijk Zieck</h2>
<p>In ons pand op huisnummer 2 (ingang B) is ook Tandprothetische Praktijk Zieck gevestigd, voor het aanmeten, maken en repareren van uitneembare gebitsprotheses, frames, partiële protheses en gebitsprotheses op implantaten. Door de nauwe samenwerking tussen tandartsen, implantoloog en tandprothetici stemmen we behandelingen moeiteloos op elkaar af. Lees meer over <a href="{{u:behandelingen/protheses/}}">protheses</a>.</p>
<figure><img src="{{a:assets/img/wachtkamer.webp}}" alt="Een medewerker van de praktijk begroet een patiënte in de wachtkamer" width="950" height="634" loading="lazy" decoding="async"></figure>
<h2>Twee keer per jaar op controle</h2>
<p>We hanteren het beleid van halfjaarlijkse controles. Zo houden we uw gebit en tandvlees goed in de gaten en zijn we er snel bij als er iets is. Nieuw bij ons? <a href="{{u:inschrijven-als-nieuwe-patient/}}">Schrijf u in als nieuwe patiënt</a>.</p>
""", nav=PRAKTIJK_NAV, extra_schema=[dentist_schema(True)])

    # De Lieve Tandarts
    text_page("de-lieve-tandarts/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("de-lieve-tandarts/", "De Lieve Tandarts")], "zorg",
              "De Lieve Tandarts in Hardenberg | Keurmerk | Badhuisplein",
              "Tandartspraktijk Badhuisplein in Hardenberg heeft sinds 2018 het keurmerk De Lieve Tandarts, als eerste in Overijssel. Extra aandacht bij tandartsangst.",
              'De Lieve Tandarts in <em class="g">Hardenberg</em>',
              "Bent u bang om naar de tandarts te gaan en is de drempel daarom hoog? Dat begrijpen we. Sinds 2018 hebben we als eerste praktijk in Overijssel het keurmerk De Lieve Tandarts, en daar zijn we trots op.",
              f"""
<figure class="lt-logo"><img src="{{a:assets/img/lieve-tandarts.png}}" alt="Logo van het keurmerk De Lieve Tandarts" width="384" height="112" loading="lazy" decoding="async"></figure>
<h2>Wat betekent dit keurmerk voor u?</h2>
<p>Tijdens elk bezoek aan De Lieve Tandarts kunt u, naast goede zorg, extra aandacht verwachten. Dat geldt voor zowel bestaande als nieuwe patiënten.</p>
<ul class="types">
  <li><b>Extra tijd</b><span>Zo nodig plannen we extra tijd voor u in.</span></li>
  <li><b>Uitleg</b><span>Tijdens de behandeling leggen we uit wat we doen.</span></li>
  <li><b>Op uw gemak</b><span>We doen er alles aan om u op uw gemak te stellen.</span></li>
  <li><b>Ook voor kinderen</b><span>Een lief team houdt altijd rekening met kinderen.</span></li>
</ul>
<h2>Als het echt te spannend is</h2>
<p>Lees wat we doen bij <a href="{{u:angst-voor-de-tandarts/}}">angst voor de tandarts</a>. Daarnaast is een behandeling mogelijk <a href="{{u:behandeling-onder-lachgas/}}">onder lachgas</a> of <a href="{{u:narcose/}}">onder narcose</a>.</p>
<figure><img src="{{a:assets/img/lachgas.webp}}" alt="Een patiënte krijgt lachgas via een neusmasker tijdens de behandeling" width="950" height="634" loading="lazy" decoding="async"></figure>
<h2>Direct een afspraak maken?</h2>
<p><a href="{{u:inschrijven-als-nieuwe-patient/}}">Vul ons inschrijfformulier in</a>. U mag ons ook bellen op <a href="{TEL_HREF}">{TEL}</a> of mailen naar <a href="mailto:{MAIL}">{MAIL}</a>, dan nemen wij contact met u op.</p>
""", nav=ZORG_NAV)

    # Lachgas
    text_page("behandeling-onder-lachgas/", [("", "Home"), ("de-lieve-tandarts/", "Extra aandacht"), ("behandeling-onder-lachgas/", "Lachgas")], "zorg",
              "Tandarts met lachgas in Hardenberg | Badhuisplein",
              "Behandeling onder lachgas in Hardenberg: een veilige manier om angst en spanning bij de tandarts te verminderen. Werkt snel en heeft geen nawerking.",
              'Behandeling onder lachgas in <em class="g">Hardenberg</em>',
              "Lachgas, ook bekend als inhalatiesedatie, is een veilige en effectieve manier om angst en spanning tijdens een tandheelkundige ingreep te verminderen.",
              """
<h2>Hoe werkt lachgas?</h2>
<p>Tijdens de behandeling ademt u een mengsel van zuurstof en lachgas in via een masker over uw neus. Dat werkt ontspannend en kalmerend, waardoor u zich comfortabeler voelt. Lachgas werkt snel en heeft na de behandeling geen nawerking: u kunt direct daarna weer normaal functioneren.</p>
<figure><img src="{a:assets/img/lachgas-kind.webp}" alt="Een kind krijgt lachgas via een neusmasker tijdens de behandeling" width="950" height="634" loading="lazy" decoding="async"></figure>
<h2>Is het geschikt voor u?</h2>
<p>Voorafgaand aan de behandeling bespreken we uw medische geschiedenis en beoordelen we of lachgas bij u past. Tandartsen en assistentes letten de hele behandeling op uw veiligheid en comfort.</p>
<div class="note"><p><b>Is lachgas niet genoeg?</b> Bij ernstige tandartsangst kan een behandeling <a href="{u:narcose/}">onder narcose</a> uitkomst bieden.</p></div>
""", img="lachgas.webp", img_alt="Een patiënte krijgt lachgas via een neusmasker tijdens de behandeling", img_pos="50% 40%", nav=ZORG_NAV, medical="Inhalatiesedatie met lachgas",
              faq=[("Kan mijn kind ook lachgas krijgen?", "Dat kan. Op een rustige manier laten we uw kind eerst wennen aan het neusmasker. Vooraf beoordelen we of lachgas geschikt is."),
                   ("Mag ik lachgas als ik zwanger ben?", "Vertel het ons altijd als u zwanger bent of denkt te zijn. Dan bespreken we vooraf of lachgas voor u geschikt is."),
                   ("Ben ik onder lachgas nog wakker?", "Ja. Lachgas maakt u ontspannen en kalm, maar u slaapt niet. Wilt u volledig slapen tijdens de behandeling, dan is narcose een andere mogelijkheid."),
                   ("Merk ik na de behandeling nog iets van lachgas?", "Lachgas heeft na de behandeling geen nawerking. U kunt direct daarna weer normaal functioneren."),
                   ("Kan iedereen lachgas krijgen?", "Dat beoordelen we vooraf, aan de hand van uw medische geschiedenis.")])

    # Narcose
    text_page("narcose/", [("", "Home"), ("de-lieve-tandarts/", "Extra aandacht"), ("narcose/", "Narcose")], "zorg",
              "Tandarts onder narcose in Hardenberg | Badhuisplein",
              "Ernstige tandartsangst? Bij Tandartspraktijk Badhuisplein in Hardenberg kunt u onder narcose worden behandeld, met tandartsen en anesthesiologen naast u.",
              'Behandeling onder narcose in <em class="g">Hardenberg</em>',
              "Bij een narcosebehandeling wordt u in een diepe slaap gebracht, waardoor u volledig ontspant en niets van de behandeling merkt. Dat is ideaal voor mensen met ernstige tandartsangst.",
              f"""
<h2>Voor wie is narcose bedoeld?</h2>
<p>Een behandeling onder narcose is vooral bedoeld voor mensen met ernstige tandartsangst, voor wie een bezoek aan de tandarts anders niet of nauwelijks mogelijk is. Is uw angst minder groot, dan kan een <a href="{{u:behandeling-onder-lachgas/}}">behandeling onder lachgas</a> al genoeg zijn. We bespreken samen wat bij u past.</p>
<h2>Veilig en begeleid</h2>
<p>Ons ervaren team van tandartsen en anesthesiologen zorgt de hele behandeling voor uw veiligheid en comfort. Voorafgaand wordt uw gezondheid grondig beoordeeld, zodat we zeker weten dat narcose voor u veilig is.</p>
<h2>Na de behandeling</h2>
<p>U wordt rustig wakker onder begeleiding van ons zorgteam. Daarna kunt u veilig naar huis, met weinig tot geen herinnering aan de behandeling.</p>
<div class="note"><p><b>Meer weten?</b> Neem gerust contact met ons op via <a href="{TEL_HREF}">{TEL}</a>. We beantwoorden al uw vragen en plannen een afspraak die bij u past.</p></div>
<div class="note"><p><b>Bent u behandelaar?</b> <a href="{{u:doorverwijzing-narcose-voor-behandelaars/}}">Verwijs een patiënt door voor narcose</a>.</p></div>
""", nav=ZORG_NAV, medical="Tandheelkundige behandeling onder narcose",
              faq=[("Wat moet ik vooraf regelen?", "Dat bespreken we met u in het gesprek voorafgaand aan de behandeling, zodat u precies weet wat u moet doen en hoe u weer veilig thuiskomt."),
                   ("Merk ik iets van de behandeling?", "Nee. U wordt in een diepe slaap gebracht en merkt niets van de behandeling. Achteraf heeft u er weinig tot geen herinnering aan."),
                   ("Is narcose veilig?", "Voorafgaand wordt uw gezondheid grondig beoordeeld. Tandartsen en anesthesiologen zorgen tijdens de hele procedure voor uw veiligheid en comfort.")])

    # Patiënten met een beperking
    text_page("patienten-met-een-beperking/", [("", "Home"), ("de-lieve-tandarts/", "Extra aandacht"), ("patienten-met-een-beperking/", "Patiënten met een beperking")], "zorg",
              "Tandarts bij een beperking | Hardenberg | Badhuisplein",
              "Een beperking of bijzondere zorgvraag? Tandartspraktijk Badhuisplein in Hardenberg plant zo nodig extra tijd in en bespreekt vooraf wat u nodig heeft.",
              'Patiënten met een <em class="g">beperking</em>',
              "Heeft u of uw kind een lichamelijke of verstandelijke beperking? Laat ons vooraf weten wat u nodig heeft. Dan bekijken we samen hoe we uw bezoek zo prettig mogelijk maken.",
              f"""
<h2>Laat ons weten wat u nodig heeft</h2>
<p>Elke patiënt is anders. Vertel ons bij het maken van de afspraak waar we rekening mee kunnen houden. Zo nodig plannen we extra tijd in en leggen we tijdens de behandeling uit wat we doen, net als bij al onze patiënten met een <a href="{{u:de-lieve-tandarts/}}">extra zorgvraag</a>.</p>
<p>Is een behandeling te belastend, dan bespreken we of <a href="{{u:behandeling-onder-lachgas/}}">lachgas</a> of <a href="{{u:narcose/}}">narcose</a> een mogelijkheid is.</p>
<p>Bel ons gerust op <a href="{TEL_HREF}">{TEL}</a> of mail naar <a href="mailto:{MAIL}">{MAIL}</a>. U kunt op die manier ook vragen stellen over de toegankelijkheid van de praktijk.</p>
""", img="beperking.webp", img_alt="Iemand in een rolstoel, gezien van opzij", nav=ZORG_NAV)

    # Spoed
    text_page("homepage/spoedgevallen-en-weekenddienst/", [("", "Home"), ("homepage/spoedgevallen-en-weekenddienst/", "Spoed en weekenddienst")], "info",
              "Spoed tandarts Hardenberg | Avond en weekend | Badhuisplein",
              "Kiespijn of een spoedgeval? Bel Tandartspraktijk Badhuisplein op 0523-216967. Buiten openingstijden kunt u terecht bij de Tandartsspoedpraktijk in Zwolle.",
              'Spoed bij de tandarts in <em class="g">Hardenberg</em>',
              "Wacht bij pijnklachten niet tot uw volgende controle, maar neem contact met ons op. Dan proberen we u dezelfde dag nog te helpen.",
              f"""
<h2>Tijdens openingstijden</h2>
<p>Bel <a href="{TEL_HREF}"><b>{TEL}</b></a>, indien mogelijk tussen <b>08:30 en 10:00 uur</b>. Wij proberen u dan op dezelfde dag nog te helpen.</p>
<h2>Buiten openingstijden en op feestdagen</h2>
<p>Voor pijnklachten, nabloedingen en ongevallen kunt u buiten de reguliere werktijden en op feestdagen terecht bij:</p>
<div class="note">
<p><b>Tandartsspoedpraktijk</b><br>Dokter van Heesweg 2, Zwolle<br>Telefoon: <a href="tel:09008602"><b>0900-8602</b></a></p>
</div>
<p>Is de praktijk gesloten en belt u ons nummer, dan hoort u op het antwoordapparaat het nummer van de dienstdoende tandarts.</p>
<h2>Goed om te weten</h2>
<ul>
  <li>Een bezoek aan de spoeddienst brengt extra kosten met zich mee.</li>
  <li>Deze kosten rekent u direct contant of met de pin af.</li>
  <li>De factuur kunt u zelf indienen bij uw zorgverzekeraar.</li>
  <li>Vergeet uw zorgpas en identiteitsbewijs niet.</li>
</ul>
<h2>Wanneer is het spoed?</h2>
<ul>
  <li>hevige kiespijn die niet overgaat met een gewone pijnstiller;</li>
  <li>een dikke wang of zwelling, eventueel met koorts;</li>
  <li>een nabloeding na het trekken van een tand of kies;</li>
  <li>een ongeluk waarbij een tand is afgebroken of uit de mond is geslagen.</li>
</ul>
<p>Is er een tand uit de mond geslagen? Pak hem vast aan de kroon, niet aan de wortel. Bewaar hem in melk of in uw mond tegen de wang en bel direct.</p>
""", nav=INFO_NAV,
              faq=[("Waar kan ik in het weekend terecht met kiespijn?", "Buiten werktijden en op feestdagen kunt u terecht bij de Tandartsspoedpraktijk, Dokter van Heesweg 2 in Zwolle, telefoon 0900-8602."),
                   ("Wat kost een bezoek aan de spoeddienst?", "Een bezoek aan de spoeddienst brengt extra kosten met zich mee. U rekent direct contant of met de pin af en dient de factuur zelf in bij uw zorgverzekeraar."),
                   ("Wanneer bel ik de praktijk het beste bij pijn?", "Bel indien mogelijk tussen 08:30 en 10:00 uur. Wij proberen u dan dezelfde dag nog te helpen.")])

    # Tarieven
    text_page("homepage/tarieven-en-betaling/", [("", "Home"), ("homepage/tarieven-en-betaling/", "Tarieven en betaling")], "info",
              "Tarieven en betaling | Tandarts Hardenberg | Badhuisplein",
              "Tarieven van Tandartspraktijk Badhuisplein volgens de NZa. Betalen via Infomedics binnen 30 dagen, betalingsregeling mogelijk. Begroting op aanvraag.",
              'Tarieven en <em class="g">betaling</em>', "Duidelijkheid vooraf: u weet wat een behandeling kost en hoe u betaalt.",
              """
<h2>Uw tandartsrekening</h2>
<p>Uw rekening is opgebouwd uit de prestaties die tijdens een behandeling zijn uitgevoerd. Elke prestatie staat op de rekening omschreven met een code. De tarieven worden jaarlijks vastgesteld door de Nederlandse Zorgautoriteit (NZa).</p>
<div class="note"><p><b>Begroting.</b> We informeren u altijd vooraf zo nauwkeurig mogelijk over de kosten. Voor alle behandelingen kunt u vooraf een begroting krijgen; boven de € 250 ook schriftelijk.</p></div>
<h2>Betalen via Infomedics</h2>
<p>De betaling van behandelingen gaat via Infomedics, dat de facturering en inning voor ons verzorgt.</p>
<ul>
  <li>Infomedics hanteert een betalingstermijn van <b>30 dagen</b>.</li>
  <li>Lukt het niet om op tijd te betalen, dan kunt u via de website van Infomedics een <b>betalingsregeling</b> treffen.</li>
  <li>Met de <b>rekeningchecker</b> op <a href="https://www.infomedics.nl" rel="noopener" target="_blank">infomedics.nl</a> controleert u met de cijferreeks op uw rekening of deze is betaald.</li>
  <li>Andere vragen? De servicedesk van Infomedics is bereikbaar op <a href="tel:+31362031900">036-20 31 900</a>, maandag t/m vrijdag van 09:00 tot 17:00 uur.</li>
</ul>
<p>Onze baliemedewerksters vertellen u graag meer over de betalingsvoorwaarden.</p>
<h2>Afspraak verzet of vergeten?</h2>
<p>Afspraken moeten minstens <b>48 uur van tevoren</b> worden afgezegd. Niet of niet tijdig afgezegde afspraken kunnen in rekening worden gebracht. Verplaatsen en afzeggen kan alleen telefonisch.</p>
""", nav=INFO_NAV)

    # Verzekering
    text_page("homepage/betalen-en-vergoedingen/", [("", "Home"), ("homepage/betalen-en-vergoedingen/", "Verzekering en vergoedingen")], "info",
              "Verzekering en vergoedingen tandarts | Badhuisplein",
              "Wat vergoedt de basisverzekering bij de tandarts en waar let u op bij een aanvullende tandartsverzekering? Acht tips en uitleg voor volwassenen en kinderen.",
              'Verzekering en <em class="g">vergoedingen</em>', "Wat vergoedt uw zorgverzekering bij de tandarts? Een overzicht, met acht tips voor het kiezen van een aanvullende verzekering.",
              """
<h2>Basisverzekering</h2>
<p>Voor volwassenen wordt maar een heel beperkt deel van de behandelingen vergoed vanuit de basisverzekering. Kunstgebitten en klikgebitten worden wel voor een groot deel vergoed. Voor de juiste vergoeding neemt u het beste contact op met uw zorgverzekeraar.</p>
<h2>Kinderen tot 18 jaar</h2>
<p>Mondzorg voor kinderen tot 18 jaar zit in de basisverzekering, behalve beugels, kronen en bruggen.</p>
<h2>Acht tips voor een aanvullende tandartsverzekering</h2>
<p>Of u zich aanvullend verzekert, en hoe uitgebreid, bepaalt u zelf. Let daarbij op het volgende:</p>
<ol>
  <li>Zeg uw oude verzekering pas op als u zeker weet dat de nieuwe verzekeraar u heeft geaccepteerd.</li>
  <li>Kijk welke behandelingen precies worden vergoed en tot welk bedrag per jaar.</li>
  <li>De meeste verzekeringen vergoeden een maximumbedrag per jaar; ga daar slim mee om.</li>
  <li>Wisselt u van verzekeraar, controleer dan of dat gevolgen heeft voor de vergoeding bij uw eigen tandarts.</li>
  <li>Soms krijgt u pas na enkele jaren een vergoeding voor bijvoorbeeld een beugel.</li>
  <li>Vergelijk ieder jaar de polisvoorwaarden; er verandert regelmatig iets.</li>
  <li>Overleg met uw tandarts welke behandelingen er het komende jaar aankomen en stem uw verzekering daarop af.</li>
  <li>Het eigen risico geldt alleen voor de basisverzekering, niet voor aanvullende verzekeringen.</li>
</ol>
""", nav=INFO_NAV)

    # Huisregels
    text_page("homepage/huisregels/", [("", "Home"), ("homepage/huisregels/", "Huisregels")], "info",
              "Huisregels | Tandartspraktijk Badhuisplein Hardenberg",
              "Huisregels van Tandartspraktijk Badhuisplein: afspraken afzeggen, pijnklachten, prothesereparaties, medische gegevens, privacy en betaling.",
              'Onze <em class="g">huisregels</em>', "Een paar afspraken die ervoor zorgen dat alles prettig en duidelijk verloopt, voor u en voor ons.",
              """
<p>Mondgezondheid maakt deel uit van uw algemene gezondheid. Ons doel is u te helpen een optimale mondgezondheid te bereiken en te behouden. Bij de kennismaking brengen we uw huidige mondconditie in kaart en bespreken we uw wensen. Daarvoor vult u een gezondheidsvragenlijst in.</p>
<h2>Uw afspraak</h2>
<p>Kunt u niet komen? Zeg uw afspraak dan minstens <b>48 uur van tevoren</b> telefonisch af. Niet of niet tijdig afgezegde afspraken kunnen bij u in rekening worden gebracht.</p>
<h2>Pijnklachten en spoed</h2>
<p>Heeft u pijn, wacht dan niet tot de volgende controle maar neem contact met ons op. Bel indien mogelijk tussen 08:30 en 10:00 uur, dan proberen we u dezelfde dag nog te helpen. Is de praktijk gesloten, dan hoort u op het antwoordapparaat het nummer van de dienstdoende tandarts.</p>
<h2>Reparatie van protheses</h2>
<p>Reparaties gebeuren in ons eigen laboratorium en zijn doorgaans aan het eind van de dag klaar:</p>
<ul>
  <li>maandag t/m woensdag: brengen vóór 12:30 uur, ophalen om 16:00 uur;</li>
  <li>donderdag en vrijdag: alleen noodreparaties.</li>
</ul>
<h2>Medische gegevens</h2>
<p>Informeer ons voor uw en onze veiligheid steeds over medische bijzonderheden, zoals zwangerschap, medicijngebruik, ziektes, infecties en afwijkingen.</p>
<h2>Privacy en geheimhouding</h2>
<p>Patiënteninformatie wordt niet aan derden verstrekt. Een verwijzing gebeurt uitsluitend na overleg tussen de patiënt en de behandelaar. Lees ook ons <a href="{u:privacybeleid/}">privacybeleid</a>.</p>
<h2>Klanttevredenheid</h2>
<p>We meten regelmatig hoe tevreden u bent, om op de hoogte te blijven van uw wensen en behoeften. U kunt die ook melden bij de balie of uw behandelaar.</p>
<h2>Betaling</h2>
<p>De betaling van behandelingen gaat via Infomedics (<a href="tel:+31362031900">036-20 31 900</a>). Voor alle behandelingen kunt u vooraf een begroting krijgen; boven de € 250 ook schriftelijk. Meer over <a href="{u:homepage/tarieven-en-betaling/}">tarieven en betaling</a>.</p>
""", nav=INFO_NAV)

    # CBCT
    text_page("cbct-rontgen/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("cbct-rontgen/", "CBCT-scan")], "praktijk",
              "CBCT-scan Hardenberg | 3D-röntgenfoto in de praktijk",
              "Tandartspraktijk Badhuisplein in Hardenberg heeft een eigen Cone Beam CT-scanner: minder straling, korte scantijd en direct een betrouwbaar 3D-beeld.",
              'CBCT-scan in Hardenberg: uw kaak in <em class="g">3D</em>',
              "Onze praktijk beschikt over een Cone Beam CT-scan. Daarmee maken we een driedimensionaal beeld van de aangezichtsschedel, de holtes in uw hoofd, de onder- en bovenkaak en de kaakkopjes.",
              """
<h2>Wat zijn de voordelen?</h2>
<p>Een Cone Beam CT-scan is een speciaal soort CT-scan. Op de beelden worden afwijkingen of stoornissen zichtbaar.</p>
<ul class="types">
  <li><b>Minder straling</b><span>Er worden veel minder röntgenstralen gebruikt dan bij een normale CT-scan.</span></li>
  <li><b>Korter</b><span>Het scannen duurt minder lang; het apparaat draait ongeveer één minuut om u heen.</span></li>
  <li><b>Direct 3D</b><span>Na computerreconstructie zijn er direct betrouwbare driedimensionale beelden.</span></li>
</ul>
<h2>Wanneer krijgt u een CBCT-scan?</h2>
<ul>
  <li>bij het plannen van een <a href="{u:behandelingen/implantaten/}">implantaat</a>: hoeveel kaakbot is er en hoe staan eerder geplaatste implantaten ervoor?</li>
  <li>bij een tand of kies die nog in het kaakbot ligt, en de ligging van de zenuwen daaromheen;</li>
  <li>bij het beoordelen van de holtes en de behandeling van een bijholteontsteking;</li>
  <li>voor een orthodontische behandeling of een chirurgische kaakcorrectie;</li>
  <li>bij onderzoek van de kaakgewrichten of van bot dat door een infectie is aangetast;</li>
  <li>bij verwondingen na een ongeluk of geweld;</li>
  <li>bij het plannen van een corrigerende operatie in het gezicht.</li>
</ul>
<h2>Hoe verloopt het onderzoek?</h2>
<ol>
  <li>U meldt zich op de afgesproken tijd bij de balie. De assistente haalt u op uit de wachtruimte en vertelt wat er gaat gebeuren.</li>
  <li>Metalen voorwerpen en sieraden in het hoofd-halsgebied verstoren het onderzoek. Die doet u daarom af, net als een gebitsprothese.</li>
  <li>U staat of zit zo stil mogelijk achter het apparaat. Een röntgenbuis draait in ongeveer één minuut om u heen en maakt opnamen uit steeds een andere hoek. U hoort daarbij een zoemend geluid.</li>
</ol>
<div class="note"><p><b>Bent u behandelaar?</b> U kunt uw patiënten bij ons laten scannen. <a href="{u:cbct-scan-doorverwijzing/}">Verwijs een patiënt door</a>.</p></div>
""", nav=PRAKTIJK_NAV,
              faq=[("Is een CBCT-scan veilig?", "Een Cone Beam CT-scan gebruikt veel minder röntgenstraling dan een normale CT-scan."),
                   ("Hoe lang duurt een CBCT-scan?", "Het apparaat draait ongeveer één minuut om u heen. Blijf in die tijd zo stil mogelijk staan of zitten, anders kunnen de opnamen mislukken."),
                   ("Moet ik voor een CBCT-scan naar het ziekenhuis?", "Nee, de scanner staat bij ons in de praktijk aan het Badhuisplein in Hardenberg.")])

    # Kinderen
    text_page("kinderen-en-de-tandarts/", [("", "Home"), ("de-lieve-tandarts/", "Extra aandacht"), ("kinderen-en-de-tandarts/", "Kinderen en de tandarts")], "zorg",
              "Kindertandarts Hardenberg | Kinderen en de tandarts",
              "Met uw kind naar de tandarts in Hardenberg? Vanaf twee jaar is uw kind welkom bij Badhuisplein. Tips om het eerste bezoek rustig te laten verlopen.",
              'Met uw kind naar de tandarts in <em class="g">Hardenberg</em>',
              "Tandheelkundige behandeling van kinderen is gebaseerd op vertrouwen. Op speelse wijze maken we uw kind vertrouwd met het tandartsbezoek. Alles is vrijblijvend: lukt het niet, dan een volgende keer beter.",
              """
<h2>Het eerste bezoek</h2>
<p>Twee jaar is een prima leeftijd om uw kind voor het eerst mee te nemen. Dat kan bijvoorbeeld als u zelf op controle komt: uw kind ervaart dan dat ook u in de stoel gaat zitten, als iets vertrouwds, en wil dat misschien ook proberen. Een behandeling is op die leeftijd meestal nog niet nodig. De tandarts kijkt of alles goed is aangelegd, telt de tandjes en geeft advies. Ook de preventieassistente helpt u daar graag bij.</p>
<figure><img src="{a:assets/img/kinderen-stoel.webp}" alt="Preventieassistente met een jong meisje in de behandelstoel" width="950" height="634" loading="lazy" decoding="async"></figure>
<h2>Voorbereiden thuis</h2>
<ul>
  <li>Vertel dat uw kind mee mag, en wat er te zien is: een mooie stoel, een grote lamp, iemand in een jas.</li>
  <li>Kies een uitleg die bij de leeftijd past. Geef niet te veel details, maar vooral een gevoel van veiligheid.</li>
  <li>Begin niet over behandelingen bij een kind jonger dan vier jaar.</li>
  <li>Vertel de tandarts bij de controle wat uw kind al weet, bijvoorbeeld over tandenpoetsen.</li>
</ul>
<h2>Ziet u er zelf tegenop?</h2>
<p>Kinderen zijn gevoelig voor signalen van hun ouders. Laat uw kind liever thuis als u zelf wordt behandeld, of laat het met een andere volwassene meegaan. Overleg het gerust vooraf met ons.</p>
<h2>Gaatjes in het melkgebit</h2>
<p>Gaatjes zijn het meest voorkomende probleem bij het melkgebit, en ze beginnen meestal in de kiezen. Een groter gaatje kan pijn en ontstekingen geven en het blijvend gebit beschadigen. Meestal voorkomt de tandarts dat door het gaatje te vullen. Is het heel klein, dan is advies over voeding en poetsen soms genoeg. Gaat een tand of kies snel wisselen, dan doet de tandarts doorgaans niets.</p>
<div class="note"><p><b>Eerlijk is het fijnst.</b> Leg op een rustig moment uit dat een tand ziek is en dat de tandarts hem beter maakt, en laat de tandarts zelf vertellen wat er gaat gebeuren. Maakt u het mooier dan het is, dan verliest uw kind het vertrouwen, en ziet het de volgende keer er meer tegenop.</p></div>
""", img_pos="50% 40%", nav=ZORG_NAV,
              faq=[("Vanaf welke leeftijd kan mijn kind naar de tandarts?", "Neem uw kind vanaf twee jaar mee. Het eerste bezoek is vooral rondkijken en wennen aan de praktijk en de medewerkers."),
                   ("Hoe vaak moet mijn kind op controle?", "Twee keer per jaar is meestal voldoende."),
                   ("Wat kost de tandarts voor kinderen?", "Mondzorg voor kinderen tot 18 jaar zit in de basisverzekering, behalve beugels, kronen en bruggen.")])

    # Angst
    text_page("angst-voor-de-tandarts/", [("", "Home"), ("de-lieve-tandarts/", "Extra aandacht"), ("angst-voor-de-tandarts/", "Angst voor de tandarts")], "zorg",
              "Angst voor de tandarts? | De Lieve Tandarts in Hardenberg",
              "Bang voor de tandarts? U bent niet de enige. Tandartspraktijk Badhuisplein in Hardenberg heeft het keurmerk De Lieve Tandarts en biedt ook lachgas en narcose.",
              'Angst voor de <em class="g">tandarts?</em>',
              "U bent niet de enige. Ongeveer tachtig procent van de mensen is min of meer angstig bij de tandarts. We maken dit dagelijks mee, en we kunnen veel doen om het u makkelijker te maken.",
              """
<h2>Waar komt de angst vandaan?</h2>
<p>Dat kan een nare ervaring zijn met een pijnlijke behandeling in het verleden, of schaamte over de staat van uw gebit. Ook het geluid van de boor, vreemde geuren en het gevoel geen controle te hebben, maken mensen vaak bang.</p>
<h2>Zo maken we het u makkelijker</h2>
<ul class="types">
  <li><b>Tijd en rust</b><span>We nemen voldoende tijd voor u en zorgen voor een rustige, warme ontvangst.</span></li>
  <li><b>Kort wachten</b><span>We houden de wachttijd zo kort mogelijk, zodat u niet lang hoeft te piekeren.</span></li>
  <li><b>Uw eigen muziek</b><span>Luister gerust naar uw eigen muziek met een hoofdtelefoon, ook tijdens de behandeling.</span></li>
  <li><b>Vooraf uitleg</b><span>Een behandelplan voeren we in overleg uit, nadat we alles helder hebben uitgelegd.</span></li>
  <li><b>Goed verdoofd</b><span>Voelt u na de verdoving toch pijn, zeg het dan meteen. De tandarts kan extra verdoven.</span></li>
  <li><b>Uw stopteken</b><span>Spreek vooraf af hoe u aangeeft dat we even moeten stoppen, bijvoorbeeld door uw hand op te steken.</span></li>
</ul>
<blockquote>Er wordt goed geluisterd naar uw wensen, en die worden gerespecteerd.</blockquote>
<h2>Is dat niet genoeg?</h2>
<p>Dan kan een behandeling <a href="{u:behandeling-onder-lachgas/}">onder lachgas</a> of <a href="{u:narcose/}">onder narcose</a> uitkomst bieden. En sinds 2018 hebben we het keurmerk <a href="{u:de-lieve-tandarts/}">De Lieve Tandarts</a>.</p>
""", img="angst.webp", img_alt="Assistente in gesprek met een patiënte in de behandelstoel", img_pos="35% 40%", nav=ZORG_NAV,
              faq=[("Kan ik extra tijd krijgen?", "Ja. Zo nodig plannen we extra tijd voor u in. Laat ons weten hoe we u het beste kunnen helpen."),
                   ("Wat als ik me schaam voor mijn gebit?", "Daar bent u niet de enige in, en wij maken dit dagelijks mee. Vertel het ons gerust, dan kijken we samen naar de beste volgende stap.")])

    # Brackets
    text_page("bracket-slotjesbeugel/", [("", "Home"), ("behandelingen/othodontie-en-invisalign/", "Orthodontie"), ("bracket-slotjesbeugel/", "Brackets")], "beh",
              "Brackets en slotjesbeugel Hardenberg | Vaste beugel",
              "Een vaste beugel in Hardenberg: brackets zetten tanden en kiezen stuk voor stuk recht. Lees hoe het werkt en vraag een gratis intake aan bij Badhuisplein.",
              'Brackets en slotjesbeugel in <em class="g">Hardenberg</em>',
              "Een vaste beugel, ook wel slotjesbeugel, bracketbeugel of blokjesbeugel genoemd, zet tanden en kiezen afzonderlijk van elkaar recht. Dat is niet alleen mooi, maar ook goed voor uw gezondheid.",
              """
<h2>Waarom een vaste beugel?</h2>
<p>Na de behandeling staan uw tanden en kiezen netjes op een rij. Met een regelmatig gebit kunt u beter bijten, kauwen en praten, en tanden en kiezen die goed op elkaar passen zijn makkelijker te onderhouden.</p>
<h2>Hoe werkt het?</h2>
<p>De vaste beugel bestaat uit slotjes (brackets) en speciaal voorgevormde draden. Soms komen er op de eerste grote kiezen banden of ringetjes met slotjes in plaats van brackets.</p>
<ul class="types">
  <li><b>Slotjes en draad</b><span>Samen duwen ze de tanden en kiezen op de goede plaats en in de juiste positie.</span></li>
  <li><b>Elke vier tot acht weken</b><span>Is de draad uitgewerkt, dan krijgt u een dikkere, tot de maximale dikte is bereikt.</span></li>
  <li><b>Elastiekjes</b><span>Soms nodig om tanden en kiezen van boven- en onderkaak beter op elkaar te laten passen.</span></li>
</ul>
<div class="note"><p><b>Gratis intake orthodontie.</b> Brackets of toch aligners? <a href="{u:afspraak-maken/}?soort=intake-orthodontie#formulier">Vraag een gratis intake aan</a>, dan nemen wij contact met u op.</p></div>
""", img="brackets.webp", img_alt="Lachende mond met een vaste beugel", img_pos="50% 50%", nav=ORTHO_NAV, medical="Orthodontische behandeling met brackets",
              faq=[("Hoe vaak krijg ik een nieuwe draad?", "Na vier tot acht weken is de draad uitgewerkt. U krijgt dan een andere, dikkere draad, tot de maximale dikte is bereikt."),
                   ("Wordt een vaste beugel vergoed?", "Beugels vallen ook voor kinderen tot 18 jaar buiten de basisverzekering. Sommige aanvullende verzekeringen vergoeden een deel.")])

    # Spark
    text_page("invisalign/", [("", "Home"), ("behandelingen/othodontie-en-invisalign/", "Orthodontie"), ("invisalign/", "Spark-beugel")], "beh",
              "Spark onzichtbare beugel Hardenberg | Gratis intake",
              "De onzichtbare Spark-beugel in Hardenberg: transparante, uitneembare aligners op maat bij Tandartspraktijk Badhuisplein. Vraag een gratis intake aan.",
              'Spark onzichtbare beugel in <em class="g">Hardenberg</em>',
              "Met een Spark-beugel ziet bijna niemand dat u uw tanden recht laat zetten. De behandeling bestaat uit een reeks uitneembare, transparante aligners die speciaal voor uw gebit worden gemaakt.",
              """
<h2>Zo werkt Spark</h2>
<p>Iedere week vervangt u de aligner door een nieuwe die net iets verschilt van de vorige. Zo gaan uw tanden en kiezen stapje voor stapje naar de juiste positie.</p>
<ul class="types">
  <li><b>Onopvallend</b><span>De aligners zijn doorzichtig en vallen vrijwel niet op als u ze draagt.</span></li>
  <li><b>Comfortabel</b><span>Geen metalen slotjes of draden, dus geen last van irritaties in de mond.</span></li>
  <li><b>Uitneembaar</b><span>U neemt ze uit om te eten, te drinken en te poetsen en te flossen.</span></li>
</ul>
<p>Heeft u een belangrijke afspraak? Dan kunt u de aligners desgewenst even uitnemen. Meer informatie en ervaringen van gebruikers vindt u op de website van Spark.</p>
<div class="note"><p><b>Gratis intake.</b> Benieuwd wat er in uw situatie mogelijk is? <a href="{u:afspraak-maken/}?soort=intake-orthodontie#formulier">Vraag een gratis intake aan</a>, dan nemen wij contact met u op.</p></div>
<p>Lees ook meer over <a href="{u:behandelingen/othodontie-en-invisalign/}">Invisalign en orthodontie</a> en over <a href="{u:bracket-slotjesbeugel/}">brackets</a>.</p>
""", img="invisalign.webp", img_alt="Doorzichtige aligner wordt op de tanden geplaatst", img_pos="50% 50%", nav=ORTHO_NAV, medical="Orthodontische behandeling met Spark-aligners",
              faq=[("Wat is het verschil tussen Spark en brackets?", "Spark werkt met uitneembare, doorzichtige aligners. Brackets zijn een vaste beugel met slotjes en draden."),
                   ("Hoe vaak vervang ik de aligner?", "Iedere week krijgt u een nieuwe aligner die net iets verschilt van de vorige.")])

    # Vacatures
    text_page("vacatures/", [("", "Home"), ("homepage/praktijkinformatie/", "Praktijk"), ("vacatures/", "Vacatures")], "praktijk",
              "Vacature tandartsassistente Hardenberg | Badhuisplein",
              "Werken bij Tandartspraktijk Badhuisplein in Hardenberg? Wij zoeken een tandartsassistente, fulltime of parttime, met doorgroeimogelijkheden.",
              'Werken bij <em class="g">Badhuisplein</em>', "Een gezellig team en een leuke werkomgeving, met doorgroeimogelijkheden in preventie en orthodontie.",
              f"""
<h2>Tandartsassistente <span style="display:block;font:500 1rem var(--sans);color:var(--ink-2)">Fulltime of parttime</span></h2>
<p>Ter aanvulling van ons tandheelkundig team zoeken we een enthousiaste en gemotiveerde collega. Ben je op zoek naar een gezellig team en een leuke werkomgeving met doorgroeimogelijkheden in preventie en/of orthodontie? Zoek dan niet verder.</p>
<h3>Wat we vragen</h3>
<ul>
  <li>Een afgeronde mbo-opleiding tot tandartsassistent, eventueel met aanvullende preventieopleiding</li>
  <li>Een accurate, flexibele en communicatieve teamplayer</li>
  <li>Goede beheersing van de Nederlandse taal en redelijke beheersing van het Engels</li>
</ul>
<h3>Wat we bieden</h3>
<ul>
  <li>Een dynamische werkplek</li>
  <li>Leer- en doorgroeimogelijkheden</li>
  <li>Een fijn en collegiaal team</li>
</ul>
<h3>Reageren</h3>
<p>Stuur je sollicitatiebrief en cv naar <a href="mailto:{JOBS}?subject=Sollicitatie%20tandartsassistente">{JOBS}</a>. Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>
""", img="team/lucette.webp", img_alt="Lucette, praktijkmanager", nav=PRAKTIJK_NAV, cta=False,
              extra_schema=[dentist_schema(False), {"@type": "JobPosting", "title": "Tandartsassistente", "description": f"<p>Tandartsassistente, fulltime of parttime, bij Tandartspraktijk Badhuisplein in Hardenberg. Stuur je sollicitatiebrief en cv naar {JOBS}.</p>",
                                                    "datePosted": TODAY, "employmentType": ["FULL_TIME", "PART_TIME"], "hiringOrganization": {"@type": "Organization", "name": NAME, "sameAs": BASE, "logo": BASE + "assets/img/icon-512.png"},
                                                    "jobLocation": {"@type": "Place", "address": POSTAL}}])

    # Privacy
    text_page("privacybeleid/", [("", "Home"), ("privacybeleid/", "Privacybeleid")], None,
              "Privacybeleid | Tandartspraktijk Badhuisplein",
              "Hoe Tandartspraktijk Badhuisplein in Hardenberg omgaat met uw persoonsgegevens, conform de AVG en de WGBO.",
              "Privacybeleid", "Wij gaan zorgvuldig om met uw gegevens. Hier leest u welke gegevens we verwerken, waarom, en wat uw rechten zijn.",
              f"""
<h2>Wie zijn wij?</h2>
<p>{NAME}, Badhuisplein 2 en 6, 7772 XC Hardenberg, is verantwoordelijk voor de verwerking van persoonsgegevens zoals beschreven in dit privacybeleid. Vragen? Mail naar <a href="mailto:{MAIL}">{MAIL}</a> of bel <a href="{TEL_HREF}">{TEL}</a>.</p>
<h2>Welke gegevens verwerken wij?</h2>
<ul>
  <li><b>Patiëntendossier:</b> naam, geboortedatum, adres, contactgegevens, BSN, verzekeringsgegevens en uw medische en tandheelkundige gegevens. Dit is wettelijk verplicht op grond van de WGBO.</li>
  <li><b>Formulieren op deze website:</b> de gegevens die u invult bij een aanvraag, inschrijving, overschrijving, verwijzing of vraag. Die gebruiken we alleen om uw aanvraag af te handelen.</li>
</ul>
<h2>Online agenda</h2>
<p>Een afspraak inplannen kan via de online agenda van Vertimart. Die opent op de website van Vertimart; de gegevens die u daar invult, worden via dat systeem verwerkt.</p>
<h2>Bewaartermijn</h2>
<p>Medische dossiers bewaren we zo lang als de wet voorschrijft (in de regel twintig jaar). Gegevens uit formulieren die niet tot een behandeling leiden, verwijderen we zodra ze niet meer nodig zijn.</p>
<h2>Delen met anderen</h2>
<p>We verstrekken uw gegevens niet aan derden, tenzij dat nodig is voor uw behandeling (een verwijzing gebeurt altijd in overleg met u), voor de facturatie via Infomedics, of als de wet ons daartoe verplicht.</p>
<h2>Cookies en kaarten</h2>
<p>Deze website plaatst geen tracking- of advertentiecookies. De kaart van Google Maps wordt pas geladen nadat u daarvoor kiest; Google kan dan gegevens verwerken volgens zijn eigen privacybeleid.</p>
<h2>Uw rechten</h2>
<p>U heeft het recht om uw gegevens in te zien, te laten corrigeren of (waar de wet dat toestaat) te laten verwijderen. Neem daarvoor contact met ons op. Heeft u een klacht over de verwerking van uw gegevens, dan kunt u die ook indienen bij de Autoriteit Persoonsgegevens.</p>
""", cta=False)


def forms_pages():
    # Afspraak maken: de echte online agenda eerst, het formulier voor wie liever gebeld wordt
    cur = "afspraak-maken/"
    soort = [("intake-orthodontie", "Gratis intake orthodontie"), ("controle", "Controle"), ("klacht", "Klacht of pijn (niet acuut)"),
             ("preventie", "Gebitsreiniging of preventie"), ("implantaat", "Consult implantaat"), ("esthetisch", "Consult esthetiek of bleken"),
             ("lachgas-narcose", "Vraag over lachgas of narcose"), ("prothese-reparatie", "Reparatie prothese"), ("anders", "Anders")]
    inner = (group("Waarvoor komt u?",
                   choice("soort", "Soort afspraak", soort, param="soort") +
                   choice("patient", "Bent u al patiënt bij ons?", [("ja", "Ja"), ("nee", "Nee, ik ben nieuw")])) +
             group("Wanneer komt het u uit?",
                   checks("dagen", "Voorkeursdagen", ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]) +
                   checks("dagdeel", "Voorkeur dagdeel", ["Ochtend", "Middag"])) +
             group("Uw gegevens",
                   field("naam", "Naam", ac="name") + field("geboortedatum", "Geboortedatum", "date", ac="bday") +
                   field("telefoon", "Telefoonnummer", "tel", ac="tel", err="Vul een geldig telefoonnummer in.") +
                   field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
                   field("opmerking", "Toelichting", "textarea", req=False, full=True)))
    form = form_wrap(cur, "Afspraakverzoek via website", inner,
                     "Uw e-mailprogramma is geopend met uw verzoek. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Verzoek versturen")
    side = f"""
<h2 class="fp__h">Liever bellen?</h2>
<a class="fp__tel" href="{TEL_HREF}">{TEL}</a>
<p>Maandag tot en met donderdag van 08:00 tot 12:00 en van 13:00 tot 16:30 uur. Vrijdag van 08:30 tot 12:30 en van 13:00 tot 16:30 uur.</p>
<dl class="fp__facts">
  <div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  <div><dt>Verplaatsen of afzeggen</dt><dd>Alleen telefonisch, minstens 48 uur van tevoren.</dd></div>
</dl>
<div class="fp__alert">{icon("alert")}<p><b>Pijn of spoed?</b> Gebruik niet de agenda, maar bel direct. Buiten openingstijden: <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">spoed en weekenddienst</a>.</p></div>"""
    before = f"""<div class="book">
  <h2>Direct inplannen in onze agenda</h2>
  <p>Kies zelf een moment dat u uitkomt. De agenda opent in een nieuw venster.</p>
  <a class="btn btn--navy" href="{AGENDA}" rel="noopener" target="_blank">{icon("cal")}Open de online agenda</a>
</div>"""
    form_page(cur, [("", "Home"), (cur, "Afspraak maken")],
              "Afspraak maken | Tandarts Hardenberg | Badhuisplein",
              "Maak direct online een afspraak bij Tandartspraktijk Badhuisplein in Hardenberg, of bel 0523-216967. Ook voor een gratis intake orthodontie.",
              "Afspraak maken",
              "Plan direct in onze online agenda, of laat ons weten waarvoor u komt, dan nemen wij contact met u op.",
              side, form, "Liever dat wij contact opnemen?", before=before, form_id="formulier")

    # Inschrijven
    cur = "inschrijven-als-nieuwe-patient/"
    inner = (group("Uw gegevens",
                   field("naam", "Naam", ac="name") + field("geboortedatum", "Geboortedatum", "date", ac="bday") +
                   field("telefoon", "Telefoonnummer", "tel", ac="tel", err="Vul een geldig telefoonnummer in.") +
                   field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
                   field("adres", "Adres en woonplaats", full=True, ac="street-address")) +
             group("Waarom schrijft u zich in?",
                   choice("reden", "Reden van uw inschrijving", [("verhuisd", "Ik ben verhuisd"), ("geen-tandarts", "Ik heb nu geen tandarts"), ("overstappen", "Ik wil overstappen"), ("behandeling", "Voor een specifieke behandeling"), ("anders", "Anders")]) +
                   field("vorige", "Vorige tandarts", req=False, full=True)) +
             group("Schrijft u meer gezinsleden in?",
                   field("gezin", "Gezinsleden", "textarea", req=False, full=True, hint="Naam en geboortedatum per gezinslid.") +
                   field("opmerking", "Opmerkingen", "textarea", req=False, full=True)))
    form = form_wrap(cur, "Inschrijving nieuwe patiënt via website", inner,
                     "Uw e-mailprogramma is geopend met uw inschrijving. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Inschrijving versturen")
    side = f"""
<h2 class="fp__h">Zo gaat het</h2>
<ol class="fp__steps">
  <li><b>Inschrijven</b><span>U vult het formulier in, voor uzelf of het hele gezin.</span></li>
  <li><b>Uitnodiging</b><span>Daarna nodigen we u uit voor een eerste consult.</span></li>
  <li><b>Eerste consult</b><span>Dit kan iets langer duren dan een normale controle. U vertelt wat uw wensen en klachten zijn en vult een medische vragenlijst in (neem de namen van uw medicijnen mee). We bespreken uw tandheelkundige voorgeschiedenis, onderzoeken uw tandvlees, kaakbot, gaatjes, beet en kauwfunctie en maken digitale röntgenfoto’s. Die maken we gebruikelijk om de twee jaar, bij pijnklachten eerder.</span></li>
</ol>
<div class="fp__alert">{icon("user")}<p><b>Neem mee naar het eerste consult:</b> uw identiteitsbewijs en zorgpas. Uw BSN noteren we dan; dat hoeft u niet via de website te sturen.</p></div>
<p class="fp__call">Komt u van een andere tandarts? U kunt zich ook <a href="{{u:overschrijven/}}">laten overschrijven</a>. Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>"""
    form_page(cur, [("", "Home"), (cur, "Inschrijven")],
              "Inschrijven bij de tandarts in Hardenberg | Nieuwe patiënten",
              "Op zoek naar een tandarts in Hardenberg? Tandartspraktijk Badhuisplein neemt weer nieuwe patiënten aan. Schrijf u en uw gezin online in.",
              "Inschrijven als nieuwe patiënt in Hardenberg",
              "Wij nemen weer nieuwe patiënten aan. Schrijf uzelf of uw hele gezin in; daarna nodigen we u uit voor een eerste consult.",
              side, form, "Inschrijfformulier", img=None)

    # Overschrijven
    cur = "overschrijven/"
    inner = (group("Uw gegevens",
                   field("naam", "Naam", ac="name") + field("geboortedatum", "Geboortedatum", "date", ac="bday") +
                   field("telefoon", "Telefoonnummer", "tel", ac="tel", err="Vul een geldig telefoonnummer in.") +
                   field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
                   field("adres", "Adres en woonplaats", full=True, ac="street-address")) +
             group("Uw huidige tandarts",
                   field("huidige", "Naam van uw huidige tandarts of praktijk", full=True) +
                   field("plaats", "Plaats van de praktijk", req=False) +
                   field("opmerking", "Toelichting", "textarea", req=False, full=True, hint="Bijvoorbeeld als u meer gezinsleden wilt laten overschrijven.")))
    form = form_wrap(cur, "Overschrijving via website", inner,
                     "Uw e-mailprogramma is geopend met uw aanvraag. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Aanvraag versturen")
    side = f"""
<h2 class="fp__h">Overstappen naar Badhuisplein</h2>
<p>Bent u al patiënt bij een andere tandarts en wilt u bij ons verder? Vul dit formulier in, dan nemen wij contact met u op.</p>
<div class="fp__alert">{icon("user")}<p><b>Geen tandarts?</b> Gebruik dan het formulier <a href="{{u:inschrijven-als-nieuwe-patient/}}">inschrijven als nieuwe patiënt</a>.</p></div>
<p class="fp__call">Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>"""
    form_page(cur, [("", "Home"), ("inschrijven-als-nieuwe-patient/", "Inschrijven"), (cur, "Overschrijven")],
              "Overschrijven naar Badhuisplein | Tandarts Hardenberg",
              "Wilt u als patiënt worden overgeschreven naar Tandartspraktijk Badhuisplein in Hardenberg? Vul het formulier in, dan nemen wij contact met u op.",
              "Overschrijven naar onze praktijk",
              "Wilt u als patiënt worden overgeschreven naar onze praktijk? Vul onderstaand formulier in.",
              side, form, "Overschrijfformulier")

    # Contact
    cur = "contact/"
    inner = (field("naam", "Naam", ac="name") + field("email", "E-mailadres", "email", ac="email", err="Vul een geldig e-mailadres in.") +
             field("telefoon", "Telefoonnummer", "tel", req=False, ac="tel", err="Vul een geldig telefoonnummer in.") +
             field("onderwerp", "Onderwerp", req=False) + field("bericht", "Uw vraag", "textarea", full=True))
    form = form_wrap(cur, "Vraag via website", inner, "Uw e-mailprogramma is geopend met uw vraag. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Vraag versturen")
    crumbs = [("", "Home"), (cur, "Contact")]
    p = dict(path=cur, title="Contact en openingstijden | Tandarts Hardenberg",
             desc="Contact met Tandartspraktijk Badhuisplein, Badhuisplein 2 en 6, 7772 XC Hardenberg. Bel 0523-216967 of mail info@praktijkbadhuisplein.nl. Tijden en route.",
             h1='Contact en <em class="g">openingstijden</em>', lead="U vindt ons aan het Badhuisplein in Hardenberg. Bel, mail of kom langs, we helpen u graag.",
             crumbs=crumbs)
    p["schema"] = ld({"@type": "ContactPage", "@id": BASE + cur + "#webpage", "url": BASE + cur, "name": p["title"], "inLanguage": "nl-NL", "about": {"@id": BASE + "#praktijk"}},
                     breadcrumb_schema(crumbs), dentist_schema(True))
    main = page_hero(p, cta=False) + f"""
<section class="section on-light">
  <div class="wrap contact">
    <div>
      <div class="card" style="margin-bottom:22px">{contact_dl(cur)}</div>
      <h2 style="font-size:1.7rem">Openingstijden praktijk</h2>
      <p><span class="status" data-status></span></p>
      {hours_table()}
      <p style="color:var(--ink-2);font-size:.95rem;margin-top:14px">We zijn telefonisch bereikbaar op dezelfde tijden. Verplaatsen of afzeggen van afspraken kan alleen telefonisch.</p>
      <h2 style="font-size:1.7rem;margin-top:32px">Waar vindt u ons?</h2>
      <p>De praktijk zit aan het Badhuisplein 2 en 6 in Hardenberg. Tandprothetische Praktijk Zieck vindt u in hetzelfde pand op huisnummer 2, ingang B. Woont u in de omgeving, bijvoorbeeld in Gramsbergen, Bergentheim, Slagharen, Dedemsvaart of Ommen? Dan bent u ook van harte welkom. <a href="{ROUTE}" rel="noopener" target="_blank">Plan uw route</a>.</p>
      <div class="alert">{icon("alert")}<div><b>Spoed buiten openingstijden?</b> U kunt terecht bij de Tandartsspoedpraktijk in Zwolle, <a href="tel:09008602">0900-8602</a>. <a href="{{u:homepage/spoedgevallen-en-weekenddienst/}}">Lees meer over spoed</a></div></div>
    </div>
    <div>
      {map_block()}
      <div class="card" style="margin-top:22px">
        <h2 style="font-size:1.7rem">Stel een vraag</h2>
        <p style="color:var(--ink-2)">Niet voor spoed of afspraken: gebruik daarvoor de telefoon of de <a href="{{u:afspraak-maken/}}">online agenda</a>.</p>
        {form}
      </div>
    </div>
  </div>
</section>"""
    write(p, main)

    # Verwijzers CBCT
    cur = "cbct-scan-doorverwijzing/"
    inner = (field("praktijk", "Uw naam en praktijk") + field("telefoon", "Telefoonnummer", "tel", err="Vul een geldig telefoonnummer in.") +
             field("email", "E-mailadres", "email", err="Vul een geldig e-mailadres in.") + field("plaats", "Adres en plaats") +
             field("pnaam", "Naam patiënt") + field("pgeb", "Geboortedatum patiënt", "date") + field("ptel", "Telefoonnummer patiënt", "tel", err="Vul een geldig telefoonnummer in.") +
             field("indicatie", "Indicatie", "select", opts=[(v.lower(), v) for v in ["Implantologie", "Kaakchirurgie", "Orthodontie", "Endodontologie", "Gnathologie", "Anders"]]) +
             field("regio", "Regio en toelichting", "textarea", full=True))
    form = form_wrap(cur, "Verwijzing CBCT-scan", inner, "Uw e-mailprogramma is geopend met uw verwijzing. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Verwijzing versturen")
    text_page(cur, [("", "Home"), ("cbct-rontgen/", "CBCT-scan"), (cur, "Voor verwijzers")], "info",
              "CBCT-scan doorverwijzen | Voor behandelaars | Badhuisplein",
              "Verwijs uw patiënt voor een Cone Beam CT-scan naar Tandartspraktijk Badhuisplein in Hardenberg. Wij plannen de afspraak en sturen u de scan snel toe.",
              'CBCT-scan voor <em class="g">behandelaars</em>',
              "Wilt u voor uw patiënt gebruikmaken van de CBCT-scan in onze praktijk in Hardenberg? Vul het formulier in, dan nemen wij contact op met uw patiënt om een afspraak in te plannen.",
              f"""
<h2>Zo werkt het</h2>
<ol>
  <li>U vult het verwijsformulier in met de gegevens van de patiënt en de indicatie.</li>
  <li>Wij nemen contact op met uw patiënt om een afspraak in te plannen.</li>
  <li>De CBCT-scan wordt u zo spoedig mogelijk toegezonden.</li>
</ol>
<p>Mogelijke indicaties zijn implantologie, kaakchirurgie, orthodontie, endodontologie en gnathologie. Meer over het onderzoek leest u op de pagina <a href="{{u:cbct-rontgen/}}">CBCT-scan</a>. Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>
<div class="note"><p>Stuur geen BSN of uitgebreide medische gegevens via dit formulier; die nemen we bij de afspraak telefonisch met de patiënt door.</p></div>
<h2>Verwijsformulier</h2>
{form}
""", cta=False, nav=INFO_NAV)

    # Verwijzers narcose
    cur = "doorverwijzing-narcose-voor-behandelaars/"
    inner = (field("praktijk", "Uw naam en praktijk") + field("telefoon", "Telefoonnummer", "tel", err="Vul een geldig telefoonnummer in.") +
             field("email", "E-mailadres", "email", err="Vul een geldig e-mailadres in.") + field("plaats", "Adres en plaats") +
             field("pnaam", "Naam patiënt") + field("pgeb", "Geboortedatum patiënt", "date") + field("ptel", "Telefoonnummer patiënt", "tel", err="Vul een geldig telefoonnummer in.") +
             field("toelichting", "Reden van verwijzing", "textarea", full=True))
    form = form_wrap(cur, "Verwijzing narcose", inner, "Uw e-mailprogramma is geopend met uw verwijzing. Er is nog niets verstuurd: verstuur de e-mail om af te ronden.", "Verwijzing versturen")
    text_page(cur, [("", "Home"), ("narcose/", "Narcose"), (cur, "Voor verwijzers")], "info",
              "Narcose doorverwijzen | Voor behandelaars | Badhuisplein",
              "Wilt u een patiënt doorverwijzen voor een tandheelkundige behandeling onder narcose in Hardenberg? Vul het formulier in, wij bellen uw patiënt.",
              'Narcose voor <em class="g">behandelaars</em>',
              "Wilt u een patiënt doorverwijzen voor een behandeling onder narcose? Vul het formulier in, dan nemen wij contact op met uw patiënt om een afspraak in te plannen.",
              f"""
<p>Meer over de behandeling leest u op de pagina <a href="{{u:narcose/}}">narcose</a>. Vragen? Bel <a href="{TEL_HREF}">{TEL}</a>.</p>
<div class="note"><p>Stuur geen BSN of uitgebreide medische gegevens via dit formulier; die nemen we bij de afspraak telefonisch met de patiënt door.</p></div>
<h2>Verwijsformulier</h2>
{form}
""", cta=False, nav=INFO_NAV)


# Oude adressen die verdwijnen, met hun nieuwe plek
REDIRECTS = [("homepage/", "homepage/praktijkinformatie/"), ("inschrijven/", "inschrijven-als-nieuwe-patient/"),
             ("bereikbaarheid-kerstvakantie/", "homepage/spoedgevallen-en-weekenddienst/"),
             ("informatie-met-betrekking-tot-het-coronavirus/", "homepage/praktijkinformatie/")]


def misc():
    # 404
    p = dict(path="404.html", title="Pagina niet gevonden | Tandartspraktijk Badhuisplein", desc="Deze pagina bestaat niet (meer).", noindex=True)
    p["schema"] = ""
    # 404 wordt vanaf elke diepte geserveerd: relatieve paden vanaf <base href="/">
    html = head(dict(p, path="")) + "\n" + header(dict(p, path="")) + f"""
<main id="main">
<section class="phero dark" style="min-height:60vh;display:grid;align-items:center">
  <div class="wrap">
    <h1>Deze pagina is niet gevonden.</h1>
    <p class="lead">Misschien is de pagina verplaatst bij de vernieuwing van onze website. Kies hieronder waar u naartoe wilt, of bel ons op {TEL}.</p>
    <div class="btn-row"><a class="btn" href="./">Naar de homepage</a><a class="btn btn--line" href="behandelingen/">Behandelingen</a><a class="btn btn--line" href="afspraak-maken/">Afspraak maken</a></div>
  </div>
</section>
</main>
""" + footer(dict(p, path=""))
    html = resolve(html, "")
    html = html.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="{SITE_BASE}">', 1)
    (ROOT / "404.html").write_text(html, encoding="utf-8")

    # Doorverwijzingen van oude URL's (voor hosting zonder .htaccess)
    for old, new in REDIRECTS:
        target = rel(old, new)
        (ROOT / old).mkdir(parents=True, exist_ok=True)
        (ROOT / old / "index.html").write_text(
            f'<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Doorverwijzing | {NAME}</title><meta name="description" content="Deze pagina is verhuisd naar een nieuw adres op de website van {NAME}.">'
            f'<meta name="robots" content="noindex"><link rel="stylesheet" href="{rel(old, "assets/css/style.css")}?v={CSS_V}">'
            f'<link rel="canonical" href="{BASE + new}"><meta http-equiv="refresh" content="0; url={target}"></head>'
            f'<body><main id="main" class="wrap section"><h1>Deze pagina is verhuisd</h1><p><a class="link" href="{target}">Ga naar de nieuwe pagina</a></p></main></body></html>', encoding="utf-8")

    # sitemap + robots + manifest
    prio = {"": "1.0"}
    urls = []
    for p in PAGES:
        if p.get("noindex"):
            continue
        pr = prio.get(p["path"], "0.8" if p["path"].startswith("behandelingen/") or p["path"] in ("afspraak-maken/", "inschrijven-als-nieuwe-patient/", "contact/", "de-lieve-tandarts/") else "0.6")
        urls.append(f"  <url><loc>{BASE + p['path']}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": NAME, "short_name": "Badhuisplein", "lang": "nl", "start_url": "/", "display": "standalone",
        "background_color": "#1b2134", "theme_color": "#1b2134",
        "icons": [{"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
        ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    home()
    behandelingen_index()
    treatment_pages()
    team_page()
    other_pages()
    forms_pages()
    misc()
    print(f"{len(PAGES)} pagina's gebouwd + 404, sitemap.xml, robots.txt")
