"""Generate the static Building Repair Centre website into website/.

    python tools/images.py   # only after changing photos (needs the original backup)
    python tools/build.py    # regenerate HTML, sitemap.xml, robots.txt and site.webmanifest
"""
from pathlib import Path
from html import escape
import datetime
import hashlib
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import SITE, ABOUT, SERVICES, TRADES, CLIENTS, FAQS, PROJECTS, PROJECT_FILTERS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website"
IMG = json.loads((ROOT / "tools" / "image-manifest.json").read_text(encoding="utf-8"))
YEAR = datetime.date.today().year
# Cache-busting version from the CSS/JS content, so rebuilds without asset changes leave the HTML identical.
ASSET_V = hashlib.sha1(b"".join((OUT / "assets" / f).read_bytes() for f in ("css/site.css", "js/site.js"))).hexdigest()[:10]
PAGES = []  # (path, priority) for the sitemap
SVC = {s["slug"]: s for s in SERVICES}

E = escape


def esc_attr(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- images

def img(key, sizes="100vw", cls="", loading="lazy", priority=False, alt=None):
    m = IMG[key]
    files = m["files"]
    srcset = ", ".join(f"/assets/img/{f['file']} {f['w']}w" for f in files)
    default = next((f for f in files if f["w"] >= 800), files[-1])
    a = esc_attr(m["alt"] if alt is None else alt)
    extra = ' fetchpriority="high"' if priority else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{default["file"]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{default["w"]}" height="{default["h"]}" alt="{a}" loading="{"eager" if priority else loading}" decoding="async"{extra}>')


def largest(key):
    return "/assets/img/" + IMG[key]["files"][-1]["file"]


def gallery_cls(n, lead=False):
    """Pick a column layout that leaves no part-empty last row on desktop."""
    if n == 1:
        return "gallery gallery--1"
    if n == 2:
        return "gallery gallery--2"
    if lead and n >= 5 and (n - 5) % 4 == 0:
        return "gallery gallery--lead"
    if n % 4 == 0:
        return "gallery"
    if n % 3 == 0:
        return "gallery gallery--3"
    return "gallery"


def gallery(keys, cls=None, sizes="(min-width: 1000px) 25vw, (min-width: 600px) 33vw, 50vw"):
    cls = cls or gallery_cls(len(keys))
    items = "".join(
        f'<li><button type="button" class="gallery__item" data-full="{largest(k)}" data-caption="{esc_attr(IMG[k]["alt"])}" '
        f'aria-label="View larger: {esc_attr(IMG[k]["alt"])}">{img(k, sizes=sizes)}</button></li>' for k in keys)
    return f'<ul class="{cls}" role="list">{items}</ul>'


# ---------------------------------------------------------------- icons (24px line icons)

ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "quote": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "alert": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "tools": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "hammer": '<path d="m15 12-8.5 8.5a2.12 2.12 0 0 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25a1.5 1.5 0 0 1-.44-1.06v-.62a1 1 0 0 0-.29-.7L15.6 4.73A6 6 0 0 0 11.36 3H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/>',
    "roller": '<rect x="2" y="2" width="16" height="6" rx="2"/><path d="M10 16v-2a2 2 0 0 1 2-2h8a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="8" y="16" width="4" height="6" rx="1"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "trowel": '<path d="m14 3 7 7-9 4-2-2z"/><path d="m10 12-7 7M5 17l2 2"/>',
    "trash": '<path d="M3 6h18M8 6V4h8v2M6 6l1 15h10l1-15"/><path d="M10 11v6M14 11v6"/>',
    "pipe": '<path d="M4 4v6a4 4 0 0 0 4 4h8a4 4 0 0 1 4 4v2"/><path d="M2 4h4M18 20h4"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    "drop": '<path d="M12 2.7s7 7.1 7 11.8a7 7 0 0 1-14 0C5 9.8 12 2.7 12 2.7z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "gutter": '<path d="M2 8h20v3a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3z"/><path d="M17 14v8"/>',
    "grid": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    "roof": '<path d="m2 13 10-8 10 8"/><path d="m5 17 7-5.5 7 5.5"/><path d="M12 21v-4"/>',
    "joinery": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18M9 10v2M15 10v2"/>',
    "scaffold": '<path d="M5 2v20M19 2v20M5 7h14M5 13h14M5 19h14M5 7l14 6"/>',
    "sparkle": '<path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/><path d="M19 3v4M17 5h4"/>',
    "floor": '<path d="M2 20h20"/><path d="m5 20 3-8h8l3 8"/><path d="m10 12-1 8M14 12l1 8"/>',
    "brick": '<rect x="2" y="4" width="20" height="16" rx="1"/><path d="M2 9.3h20M2 14.6h20M8 4v5.3M16 4v5.3M12 9.3v5.3M8 14.6V20M16 14.6V20"/>',
    "window": '<rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/>',
    "render": '<path d="M3 5h18M3 10h12M3 15h18M3 20h9"/>',
    "fence": '<path d="M4 3 2 5v15h4V5zM12 3l-2 2v15h4V5zM20 3l-2 2v15h4V5z"/><path d="M6 8h4M14 8h4M6 15h4M14 15h4"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


# ---------------------------------------------------------------- layout

def nav_link(href, label, current):
    cur = ' aria-current="page"' if href == current else ""
    return f'<a href="{href}"{cur}>{E(label)}</a>'


def header(current):
    svc_links = ""
    for s in SERVICES:
        href = f"/{s['slug']}/"
        cur = ' aria-current="page"' if current == href else ""
        svc_links += f'<li><a href="{href}"{cur}>{icon(s["icon"])}{E(s["name"])}</a></li>'
    svc_active = " is-active" if current in ["/services/"] + [f"/{s['slug']}/" for s in SERVICES] else ""
    return f'''
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container topbar__inner">
    <span>{icon("clock")} {E(SITE["hours"])} &nbsp;·&nbsp; {E(SITE["area"])}</span>
    <span class="topbar__links"><a href="mailto:{SITE["email"]}">{icon("mail")} {SITE["email"]}</a><a href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a></span>
  </div>
</div>
<header class="site-header" data-header>
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Building Repair Centre home">
      <img src="/assets/img/logo.webp" width="{IMG["_logo"]["w"]}" height="{IMG["_logo"]["h"]}" alt="Building Repair Centre">
    </a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list" role="list">
        <li>{nav_link("/", "Home", current)}</li>
        <li>{nav_link("/about-us/", "About", current)}</li>
        <li class="nav__has-sub{svc_active}">
          <a href="/services/"{' aria-current="page"' if current == "/services/" else ""}>Services</a>
          <button class="nav__sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services"><span class="visually-hidden">Show services</span>{icon("chev")}</button>
          <div class="nav__sub" id="sub-services">
            <ul role="list">{svc_links}</ul>
          </div>
        </li>
        <li>{nav_link("/projects/", "Projects", current)}</li>
        <li>{nav_link("/faq/", "FAQ", current)}</li>
        <li>{nav_link("/contact-us/", "Contact", current)}</li>
      </ul>
      <div class="nav__mobile-cta">
        <a class="btn btn--accent btn--block" href="/contact-us/#quote">{icon("quote")} Request a Quote</a>
        <a class="btn btn--ghost-light btn--block" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
        <p>{E(SITE["hours"])}<br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
      </div>
    </nav>
    <div class="header-cta">
      <a class="btn btn--outline header-cta__call" href="{SITE["phone_href"]}" aria-label="Call {SITE["phone"]}">{icon("phone")}<span>{SITE["phone"]}</span></a>
      <a class="btn btn--accent header-cta__quote" href="/contact-us/#quote">Request a Quote</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle>
        {icon("menu", "icon icon--open")}{icon("close", "icon icon--close")}<span class="visually-hidden">Menu</span>
      </button>
    </div>
  </div>
</header>'''


def footer():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''
<section class="cta-band" aria-labelledby="cta-band-title">
  <div class="container cta-band__inner">
    <div>
      <h2 id="cta-band-title">Need building repairs or maintenance?</h2>
      <p>Tell us about the job and we will get back to you with a quote.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--accent btn--lg" href="/contact-us/#quote">Request a Quote {icon("arrow")}</a>
      <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <img src="/assets/img/logo-white.webp" width="{IMG["_logo-white"]["w"]}" height="{IMG["_logo-white"]["h"]}" alt="Building Repair Centre" loading="lazy">
      <p>Building repairs, maintenance and trade services for insurance, strata, commercial and residential clients across Sydney.</p>
    </div>
    <div>
      <h2 class="site-footer__title">Contact</h2>
      <ul class="site-footer__contact" role="list">
        <li>{icon("phone")}<a href="{SITE["phone_href"]}">{SITE["phone"]}</a></li>
        <li>{icon("mail")}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        <li>{icon("clock")}<span>{E(SITE["hours"])}</span></li>
        <li>{icon("pin")}<span>{E(SITE["area"])}</span></li>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__title">Services</h2>
      <ul role="list">{svc}</ul>
    </div>
    <div>
      <h2 class="site-footer__title">Quick links</h2>
      <ul role="list">
        <li><a href="/about-us/">About us</a></li>
        <li><a href="/projects/">Projects</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact-us/">Contact us</a></li>
        <li><a href="{SITE["roofcentre"]}" rel="noopener">Roof Centre (roofing)</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__base">
    <div class="container">
      <p>&copy; {YEAR} Building Repair Centre. All rights reserved.</p>
      <p><a href="/privacy/">Privacy</a></p>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick contact">
  <a class="mobile-bar__call" href="{SITE["phone_href"]}">{icon("phone")} Call</a>
  <a class="mobile-bar__quote" href="/contact-us/#quote">{icon("quote")} Request a Quote</a>
</div>
<dialog class="lightbox" data-lightbox aria-label="Photo viewer">
  <figure>
    <img alt="" data-lightbox-img>
    <figcaption data-lightbox-caption></figcaption>
  </figure>
  <button class="lightbox__btn lightbox__close" type="button" data-lightbox-close aria-label="Close">{icon("close")}</button>
  <button class="lightbox__btn lightbox__prev" type="button" data-lightbox-prev aria-label="Previous photo">{icon("arrow")}</button>
  <button class="lightbox__btn lightbox__next" type="button" data-lightbox-next aria-label="Next photo">{icon("arrow")}</button>
</dialog>'''


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "GeneralContractor",
    "@id": SITE["url"] + "/#business",
    "name": SITE["name"],
    "url": SITE["url"] + "/",
    "logo": SITE["url"] + "/assets/img/logo.png",
    "image": SITE["url"] + "/assets/img/og-building-repair-centre.jpg",
    "telephone": "+61 431 848 619",
    "email": SITE["email"],
    "areaServed": {"@type": "City", "name": "Sydney"},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00", "closes": "17:00"}],
}


def page(path, title, description, body, current=None, priority="0.7", noindex=False, ld=None, crumbs=None, og_image=None):
    url = SITE["url"] + path
    lds = [ORG_LD] if path == "/" else []
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["url"] + "/"}]
        for i, (name, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": i, "name": name, "item": SITE["url"] + href})
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if ld:
        lds.append(ld)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    og = SITE["url"] + (og_image or "/assets/img/og-building-repair-centre.jpg")
    html = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{esc_attr(description)}">
{'<meta name="robots" content="noindex, follow">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Building Repair Centre">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="{esc_attr(title)}">
<meta property="og:description" content="{esc_attr(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a2552">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{ld_html}
</head>
<body>
{header(current if current is not None else path)}
<main id="main" tabindex="-1">
{body}
</main>
{footer()}
</body>
</html>
'''
    dest = OUT / path.strip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(l for l in html.splitlines() if l.strip()) + "\n", encoding="utf-8")
    if not noindex:
        PAGES.append((path, priority))


# ---------------------------------------------------------------- components

def crumbs_html(crumbs):
    parts = ['<li><a href="/">Home</a></li>'] + [
        f'<li><a href="{h}">{E(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{E(n)}</li>'
        for i, (n, h) in enumerate(crumbs)]
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol role="list">{"".join(parts)}</ol></nav>'


def page_hero(title, lead, key=None, eyebrow=None, crumbs=None, cta=True):
    """Text beside a framed photo. The original photos are at most 1600px wide, so they are never stretched edge to edge."""
    ey = f'<p class="eyebrow eyebrow--light">{E(eyebrow)}</p>' if eyebrow else ""
    actions = f'''<div class="hero__actions">
        <a class="btn btn--accent btn--lg" href="/contact-us/#quote">Request a Quote {icon("arrow")}</a>
        <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
      </div>''' if cta else ""
    photo = f'<div class="page-hero__photo">{img(key, sizes="(min-width: 900px) 500px, min(560px, 92vw)", priority=True)}</div>' if key else ""
    return f'''
<section class="page-hero{"" if key else " page-hero--sm"}">
  <div class="container page-hero__grid">
    <div class="page-hero__content">
      {crumbs_html(crumbs) if crumbs else ""}{ey}
      <h1>{title}</h1>
      <p class="page-hero__lead">{lead}</p>
      {actions}
    </div>
    {photo}
  </div>
</section>'''


def faq_list(faqs, level=3):
    return '<div class="faq-list">' + "".join(
        f'<details class="faq"><summary><h{level} class="faq__q">{E(q)}</h{level}>{icon("chev")}</summary><div class="faq__a"><p>{a}</p></div></details>'
        for q, a in faqs) + "</div>"


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


def sector_cards(slugs=None, cls="sector-grid"):
    cards = []
    for s in SERVICES:
        if slugs is not None and s["slug"] not in slugs:
            continue
        cards.append(f'''<li class="sector reveal">
  <a href="/{s["slug"]}/">
    <div class="sector__img">{img(s["card"], sizes="(min-width: 1100px) 300px, (min-width: 560px) 50vw, 100vw")}</div>
    <span class="sector__badge">{icon(s["icon"])}</span>
    <div class="sector__body">
      <h3>{E(s["name"])}</h3>
      <p>{E(s["summary"])}</p>
      <span class="sector__more">Learn more {icon("arrow")}</span>
    </div>
  </a>
</li>''')
    return f'<ul class="{cls}" role="list">' + "".join(cards) + "</ul>"


def trades_grid(compact=False):
    if compact:
        items = "".join(f'<li class="trade">{icon(i)}<h3>{E(n)}</h3></li>' for n, i, _ in TRADES)
        return f'<ul class="trades trades--compact" role="list">{items}</ul>'
    items = "".join(f'<li class="trade reveal">{icon(i)}<div><h3>{E(n)}</h3><p>{E(d)}</p></div></li>' for n, i, d in TRADES)
    return f'<ul class="trades trades--full" role="list">{items}</ul>'


SERVICE_OPTIONS = [s["name"] for s in SERVICES] + ["Something else"]
ROLE_OPTIONS = ["Homeowner", "Strata or building manager", "Real estate agent or landlord", "Insurance builder, assessor or insurer",
                "Business or commercial property", "Tradesperson or supplier", "Other"]


def quote_form(heading="Request a quote", intro="Tell us about the job and we will get back to you as soon as possible.", hid="quote"):
    svc = "".join(f'<option value="{esc_attr(o)}">{E(o)}</option>' for o in SERVICE_OPTIONS)
    roles = "".join(f'<option value="{esc_attr(o)}">{E(o)}</option>' for o in ROLE_OPTIONS)
    return f'''
<div class="quote-card" id="{hid}">
  <h2>{E(heading)}</h2>
  <p class="quote-card__intro">{E(intro)}</p>
  <form class="quote-form" action="/api/enquiry.php" method="post" data-enquiry-form novalidate>
    <div class="field-row">
      <div class="field">
        <label for="{hid}-name">Name <span aria-hidden="true">*</span></label>
        <input id="{hid}-name" name="name" type="text" autocomplete="name" required maxlength="100">
      </div>
      <div class="field">
        <label for="{hid}-phone">Phone <span aria-hidden="true">*</span></label>
        <input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="30">
      </div>
    </div>
    <div class="field-row">
      <div class="field">
        <label for="{hid}-email">Email <span aria-hidden="true">*</span></label>
        <input id="{hid}-email" name="email" type="email" autocomplete="email" required maxlength="150">
      </div>
      <div class="field">
        <label for="{hid}-suburb">Suburb</label>
        <input id="{hid}-suburb" name="suburb" type="text" autocomplete="address-level2" maxlength="80">
      </div>
    </div>
    <div class="field-row">
      <div class="field">
        <label for="{hid}-service">Type of work</label>
        <select id="{hid}-service" name="service"><option value="">Please choose</option>{svc}</select>
      </div>
      <div class="field">
        <label for="{hid}-role">I am a</label>
        <select id="{hid}-role" name="role"><option value="">Please choose</option>{roles}</select>
      </div>
    </div>
    <div class="field">
      <label for="{hid}-message">How can we help? <span aria-hidden="true">*</span></label>
      <textarea id="{hid}-message" name="message" rows="5" required maxlength="3000" placeholder="For example: what needs repairing, the type of property and when you would like the work done."></textarea>
    </div>
    <div class="field field--hp" aria-hidden="true">
      <label for="{hid}-website">Leave this field empty</label>
      <input id="{hid}-website" name="website" type="text" tabindex="-1" autocomplete="off">
    </div>
    <input type="hidden" name="page" value="">
    <input type="hidden" name="started" value="">
    <p class="form-note">Fields marked * are required. We only use your details to respond to your enquiry. See our <a href="/privacy/">privacy statement</a>.</p>
    <button class="btn btn--primary btn--lg btn--block" type="submit">Send enquiry {icon("arrow")}</button>
    <div class="form-status" role="status" aria-live="polite" tabindex="-1" data-form-status></div>
  </form>
</div>'''


def contact_aside():
    return f'''
<aside class="contact-aside">
  <h2>Contact details</h2>
  <ul class="contact-list" role="list">
    <li>{icon("phone")}<div><span>Phone</span><a href="{SITE["phone_href"]}">{SITE["phone"]}</a></div></li>
    <li>{icon("mail")}<div><span>Email</span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></li>
    <li>{icon("clock")}<div><span>Business hours</span>{E(SITE["hours"])}</div></li>
    <li>{icon("pin")}<div><span>Service area</span>{E(SITE["area"])}</div></li>
  </ul>
  <div class="contact-aside__note">
    {icon("alert")}
    <p><strong>Storm or tree damage?</strong> Call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a> during business hours. If life or property is at immediate risk, call the NSW SES on <a href="tel:132500">132 500</a>, or 000 in a life-threatening emergency.</p>
  </div>
</aside>'''


def steps():
    return f'''
<section class="section section--dark">
  <div class="container">
    <div class="section-head section-head--light reveal">
      <p class="eyebrow eyebrow--light">How it works</p>
      <h2>From enquiry to finished job</h2>
    </div>
    <ol class="steps__list" role="list">
      <li class="reveal"><span class="steps__num">1</span><h3>Tell us about the job</h3><p>Call us or send an enquiry with the address or suburb, what needs doing and, if you can, a few photos.</p></li>
      <li class="reveal"><span class="steps__num">2</span><h3>Inspection and quote</h3><p>We look at the job, inspecting the property where needed, and send you a quote.</p></li>
      <li class="reveal"><span class="steps__num">3</span><h3>We do the work</h3><p>Once you accept the quote, we book the job and organise the trades to complete it.</p></li>
    </ol>
  </div>
</section>'''


# ---------------------------------------------------------------- pages

def build_home():
    facts = [("pin", SITE["area"]), ("clock", "Mon–Fri, 9 am – 5 pm"), ("quote", "Free quotes"), ("tools", "21 trade services")]
    facts_html = "".join(f"<li>{icon(i)}<span>{E(t)}</span></li>" for i, t in facts)
    featured = [p for p in PROJECTS if p["id"] in ("camperdown", "redfern", "deck-roof")]
    fp = "".join(f'''<article class="fp reveal">
  <a class="fp__img" href="/projects/#{p["id"]}" tabindex="-1" aria-hidden="true">{img(p["photos"][0], sizes="(min-width: 960px) 380px, (min-width: 620px) 50vw, 100vw")}</a>
  <div class="fp__body"><span class="pgroup__tag">{E(p["label"])}</span><h3><a href="/projects/#{p["id"]}">{E(p["title"])}</a></h3><p>{E(p["text"])}</p></div>
</article>''' for p in featured)
    clients = "".join(f"<li>{icon('check')}{E(c)}</li>" for c in CLIENTS)
    body = f'''
<section class="hero">
  <div class="container hero__grid">
    <div class="hero__content">
      <p class="eyebrow eyebrow--light">Sydney building repairs &amp; maintenance</p>
      <h1>Building repairs, maintenance and trade services across Sydney</h1>
      <p class="hero__lead">Reliable building repairs, insurance work, strata and real estate maintenance, commercial fit-outs and residential projects, with the trades to get the job done.</p>
      <div class="hero__actions">
        <a class="btn btn--accent btn--lg" href="#quote">Request a Quote {icon("arrow")}</a>
        <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
      </div>
      <ul class="hero__facts" role="list">{facts_html}</ul>
    </div>
    <div class="collage hero__media-anim">
      {img("cafe-fitout", sizes="(min-width: 960px) 300px, 52vw", cls="collage__a", priority=True)}
      {img("deck-pergola-cn", sizes="(min-width: 960px) 260px, 44vw", cls="collage__b", priority=True)}
      {img("redfern-apartments", sizes="(min-width: 960px) 260px, 44vw", cls="collage__c", priority=True)}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Who we work for</p>
      <h2>Building services for every kind of property</h2>
      <p>Insurance repairs, strata and rental maintenance, commercial premises and homes: one team that can handle the building work and the trades.</p>
    </div>
    {sector_cards(["insurance-building", "strata-real-estate-maintenance", "commercial", "residential"])}
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__text reveal">
      <p class="eyebrow">About Building Repair Centre</p>
      <h2>Building works and maintenance, organised for you</h2>
      <p>{ABOUT[0]}</p>
      <p>{ABOUT[1]}</p>
      <a class="btn btn--primary" href="/about-us/">More about us {icon("arrow")}</a>
    </div>
    <div class="split__media reveal">
      <div class="stack">
        {img("camperdown-stairs", sizes="(min-width: 900px) 40vw, 90vw", cls="stack__a")}
        {img("pergola-5", sizes="(min-width: 900px) 22vw, 50vw", cls="stack__b")}
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head section-head--light section-head--row reveal">
      <div>
        <p class="eyebrow eyebrow--light">Trade services</p>
        <h2>The trades your job needs</h2>
        <p>From carpentry and plastering to plumbing, electrical and tiling, organised through one contact.</p>
      </div>
      <a class="btn btn--ghost-light" href="/tradie-services/">All trade services {icon("arrow")}</a>
    </div>
    {trades_grid(compact=True)}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--row reveal">
      <div>
        <p class="eyebrow">Projects</p>
        <h2>Recent work</h2>
        <p>Photos from our own jobs across Sydney.</p>
      </div>
      <a class="btn btn--outline" href="/projects/">View all projects {icon("arrow")}</a>
    </div>
    <div class="featured">{fp}</div>
  </div>
</section>

{steps()}

<section class="section">
  <div class="container split split--top">
    <div class="reveal">
      <p class="eyebrow">Our clients</p>
      <h2>Who we provide services to</h2>
      <ul class="clients" role="list">{clients}</ul>
      <h2 style="margin-top:56px">Common questions</h2>
      {faq_list(FAQS[:4])}
      <p class="more-link"><a class="link-arrow" href="/faq/">See all FAQs {icon("arrow")}</a></p>
    </div>
    <div class="reveal">
      {quote_form()}
    </div>
  </div>
</section>
'''
    page("/", "Building Repair Centre | Building Repairs & Maintenance Sydney",
         "Building repairs, insurance work, strata and real estate maintenance, commercial fit-outs and trade services across Sydney. Call 0431 848 619.",
         body, priority="1.0", ld=faq_ld(FAQS[:4]))


def build_about():
    clients = "".join(f"<li>{icon('check')}{E(c)}</li>" for c in CLIENTS)
    crumbs = [("About us", "/about-us/")]
    body = page_hero("About Building Repair Centre", "Building works and maintenance across Sydney, from one-off repairs to renovations, fit-outs and ongoing maintenance.", "camperdown-stairs", crumbs=crumbs) + f'''
<section class="section">
  <div class="container split">
    <div class="split__text prose reveal">
      <h2>Who we are</h2>
      {"".join(f"<p>{p}</p>" for p in ABOUT)}
      <div class="btn-row">
        <a class="btn btn--primary" href="/contact-us/#quote">Request a Free Quote {icon("arrow")}</a>
        <a class="btn btn--outline" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
      </div>
    </div>
    <div class="split__media reveal">
      <div class="stack">
        {img("deck-pergola-cn", sizes="(min-width: 900px) 40vw, 90vw", cls="stack__a")}
        {img("hallway-doors", sizes="(min-width: 900px) 22vw, 50vw", cls="stack__b")}
      </div>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container split split--top">
    <div class="reveal">
      <p class="eyebrow">Our clients</p>
      <h2>Who we provide services to</h2>
      <ul class="clients" role="list">{clients}</ul>
    </div>
    <div class="reveal">
      <p class="eyebrow">Trades and suppliers</p>
      <h2>Work with us</h2>
      <p>We accept trades, suppliers and individual tradespeople. If you would like to work with us, email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> with your trade and contact details.</p>
      <a class="link-arrow" href="/tradie-services/">See our trade services {icon("arrow")}</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal"><h2>What we do</h2></div>
    {sector_cards(cls="sector-grid sector-grid--5")}
  </div>
</section>'''
    page("/about-us/", "About Us | Building Repair Centre Sydney",
         "Building Repair Centre carries out building works and maintenance across Sydney for insurance, strata, real estate, commercial and residential clients.",
         body, crumbs=crumbs)


def build_services_hub():
    crumbs = [("Services", "/services/")]
    body = page_hero("Our services", "Insurance building, strata and real estate maintenance, commercial and residential work, and 21 trade services across Sydney.", "camperdown-1", crumbs=crumbs) + f'''
<section class="section">
  <div class="container">
    {sector_cards(cls="sector-grid sector-grid--5")}
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head section-head--row reveal">
      <div>
        <p class="eyebrow">Trade services</p>
        <h2>Trades we provide</h2>
      </div>
      <a class="btn btn--outline" href="/tradie-services/">Trade services {icon("arrow")}</a>
    </div>
    {trades_grid()}
  </div>
</section>
{steps()}'''
    page("/services/", "Building Services in Sydney | Building Repair Centre",
         "Insurance building, strata and real estate maintenance, commercial, residential and trade services across Sydney. Request a quote or call 0431 848 619.",
         body, priority="0.8", crumbs=crumbs)


def other_services(slug):
    return f'''
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><h2>Other services</h2></div>
    {sector_cards([s["slug"] for s in SERVICES if s["slug"] != slug])}
  </div>
</section>'''


def service_aside(s, image_key):
    return f'''
<aside class="svc-aside">
  <div class="svc-aside__card reveal">
    {img(image_key, sizes="(min-width: 1000px) 360px, 90vw")}
    <div class="svc-aside__body">
      <h2>Request a quote</h2>
      <p>Tell us about the job: the address or suburb, what needs doing and any photos.</p>
      <a class="btn btn--accent btn--block" href="/contact-us/?service={s["slug"]}#quote">Request a Quote</a>
      <a class="btn btn--outline btn--block" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
      <p class="svc-aside__hours">{icon("clock")} {E(SITE["hours"])}</p>
    </div>
  </div>
</aside>'''


def build_service(s):
    path = f"/{s['slug']}/"
    crumbs = [("Services", "/services/"), (s["name"], path)]
    includes = "".join(f'<li>{icon("check")}<div><strong>{E(t)}</strong><span>{E(d)}</span></div></li>' for t, d in s["includes"])
    faqs = s["faqs"] + [FAQS[5], FAQS[6]]
    side = next(k for k in s["gallery"] if k != s["hero"])
    body = page_hero(E(s["name"]), s["lead"], s["hero"], eyebrow="Our services", crumbs=crumbs) + f'''
<section class="section">
  <div class="container svc-layout">
    <div class="prose">
      <section class="prose-block reveal">
        <h2>{E(s["name"])} services</h2>
        {"".join(f"<p>{p}</p>" for p in s["intro"])}
      </section>
      <section class="prose-block reveal">
        <h2>What we do</h2>
        <ul class="includes" role="list">{includes}</ul>
      </section>
    </div>
    {service_aside(s, side)}
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our work</p>
      <h2>Photos from our jobs</h2>
      <p>Select a photo to enlarge it. See more on the <a href="/projects/">projects page</a>.</p>
    </div>
    {gallery(s["gallery"])}
  </div>
</section>
<section class="section">
  <div class="container narrow reveal">
    <h2>Questions about {E(s["name"].lower())}</h2>
    {faq_list(faqs)}
  </div>
</section>
{other_services(s["slug"])}'''
    page(path, s["seo_title"], s["description"], body, priority="0.8", crumbs=crumbs, ld=faq_ld(faqs),
         og_image="/assets/img/" + IMG[s["hero"]]["files"][min(2, len(IMG[s["hero"]]["files"]) - 1)]["file"])


def build_trades():
    s = SVC["tradie-services"]
    path = "/tradie-services/"
    crumbs = [("Services", "/services/"), (s["name"], path)]
    faqs = s["faqs"] + [FAQS[5], FAQS[6]]
    body = page_hero("Trade services", s["lead"], s["hero"], eyebrow="Our services", crumbs=crumbs) + f'''
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <h2>Trades we provide</h2>
      <p>Book a single trade, or let us organise the trades a bigger job needs.</p>
    </div>
    {trades_grid()}
    <div class="btn-row">
      <a class="btn btn--accent btn--lg" href="/contact-us/?service=tradie-services#quote">Request a Quote {icon("arrow")}</a>
      <a class="btn btn--outline btn--lg" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our work</p>
      <h2>Photos from our jobs</h2>
      <p>Select a photo to enlarge it.</p>
    </div>
    {gallery(s["gallery"])}
  </div>
</section>
<section class="section">
  <div class="container narrow reveal">
    <h2>Questions about trade services</h2>
    {faq_list(faqs)}
  </div>
</section>
{other_services(s["slug"])}'''
    page(path, s["seo_title"], s["description"], body, priority="0.8", crumbs=crumbs, ld=faq_ld(faqs))


def build_projects():
    crumbs = [("Projects", "/projects/")]
    chips = "".join(f'<button type="button" class="chip" data-filter="{v}" aria-pressed="{"true" if v == "all" else "false"}">{E(l)}</button>' for v, l in PROJECT_FILTERS)
    groups = []
    for p in PROJECTS:
        n = len(p["photos"])
        cls = gallery_cls(n, lead=True)
        groups.append(f'''<article class="pgroup" id="{p["id"]}" data-category="{p["type"]}" aria-labelledby="{p["id"]}-title">
  <header class="pgroup__head">
    <div>
      <h3 id="{p["id"]}-title">{E(p["title"])}</h3>
      <p>{E(p["text"])}</p>
    </div>
    <span class="pgroup__tag">{E(p["label"])} · {n} photo{"s" if n != 1 else ""}</span>
  </header>
  {gallery(p["photos"], cls=cls)}
</article>''')
    total = sum(len(p["photos"]) for p in PROJECTS)
    body = page_hero("Our projects", "A selection of our commercial, strata, residential and repair work across Sydney. Take a look, then get in touch to start your own project.", "deck-pergola-cn", crumbs=crumbs) + f'''
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <h2>Project gallery</h2>
      <p>{len(PROJECTS)} projects and {total} photos, grouped by job. Filter by type of work, and select a photo to enlarge it.</p>
    </div>
    <div class="chips" role="group" aria-label="Filter projects">{chips}</div>
    <p class="visually-hidden" role="status" data-filter-status></p>
    <div class="pgroups">{"".join(groups)}</div>
  </div>
</section>'''
    page("/projects/", "Our Projects | Building Repair Centre Sydney",
         "Photos of Building Repair Centre projects in Sydney: commercial fit-outs, apartment buildings, decks and pergolas, storm damage and trade work.",
         body, priority="0.8", crumbs=crumbs)


def build_faq():
    crumbs = [("FAQ", "/faq/")]
    groups = [("General", FAQS)] + [(s["name"], s["faqs"]) for s in SERVICES]
    sections = "".join(f'<section class="faq-group reveal"><h2>{E(n)}</h2>{faq_list(f)}</section>' for n, f in groups)
    allf, seen = [], set()
    for _, fs in groups:
        for q, a in fs:
            if q not in seen:
                seen.add(q)
                allf.append((q, a))
    body = page_hero("Frequently asked questions", "Answers to common questions about our services. Can't find what you need? Call us or send an enquiry.", "pergola-5", crumbs=crumbs) + f'''
<section class="section">
  <div class="container narrow">
    {sections}
  </div>
</section>'''
    page("/faq/", "FAQ | Building Repair Centre Sydney",
         "Answers to common questions about Building Repair Centre: services, business hours, service area, quotes, storm damage and working with us.",
         body, priority="0.6", ld=faq_ld(allf), crumbs=crumbs)


def build_contact():
    crumbs = [("Contact us", "/contact-us/")]
    body = page_hero("Contact us", "Fill out the form to request a quote, or call us during business hours.", crumbs=crumbs, cta=False) + f'''
<section class="section">
  <div class="container contact-layout">
    {quote_form(intro="Tell us about the job. Include the suburb and, if you can, a description of what needs doing.")}
    {contact_aside()}
  </div>
</section>'''
    page("/contact-us/", "Contact Us | Request a Quote | Building Repair Centre",
         "Contact Building Repair Centre for a quote. Call 0431 848 619 or email info@buildingrepaircentre.com.au. Monday to Friday, 9 am to 5 pm.",
         body, priority="0.8", crumbs=crumbs)


def build_thanks():
    body = f'''
<section class="section message-page">
  <div class="container narrow center">
    {icon("check", "icon icon--xl")}
    <h1>Thanks, your enquiry has been sent</h1>
    <p>We will get back to you as soon as possible. If your job is urgent, please call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="/">Back to home</a>
      <a class="btn btn--outline" href="/projects/">View our projects</a>
    </div>
  </div>
</section>'''
    page("/thank-you/", "Thank You | Building Repair Centre", "Your enquiry has been sent to Building Repair Centre.", body, noindex=True)


def build_privacy():
    crumbs = [("Privacy", "/privacy/")]
    body = page_hero("Privacy statement", "How Building Repair Centre handles the personal information you send us.", crumbs=crumbs, cta=False) + f'''
<section class="section">
  <div class="container narrow prose">
    <h2>Information we collect</h2>
    <p>When you send an enquiry through this website, we collect the details you enter: your name, phone number, email address, suburb, the type of work, who you are enquiring as, and your message.</p>
    <h2>How we use it</h2>
    <p>We use these details only to respond to your enquiry, prepare a quote and contact you about your job. We do not sell your information.</p>
    <h2>How it is sent and stored</h2>
    <p>Enquiries are sent to our business email. They are kept for as long as needed to respond to you and to keep business records.</p>
    <h2>Access and corrections</h2>
    <p>To ask about, correct or delete the information we hold about you, email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> or call <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
  </div>
</section>'''
    page("/privacy/", "Privacy Statement | Building Repair Centre",
         "How Building Repair Centre collects and uses the personal information you send through our website enquiry form.",
         body, priority="0.2", crumbs=crumbs)


def build_404():
    body = f'''
<section class="section message-page">
  <div class="container narrow center">
    <p class="eyebrow">Error 404</p>
    <h1>Sorry, we couldn't find that page</h1>
    <p>The page may have moved. Try one of these instead, or call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="/">Home</a>
      <a class="btn btn--outline" href="/services/">Services</a>
      <a class="btn btn--outline" href="/contact-us/">Contact</a>
    </div>
  </div>
</section>'''
    page("/404.html", "Page Not Found | Building Repair Centre", "The page you are looking for could not be found.", body, noindex=True, current="")


def build_meta_files():
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE['url']}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nDisallow: /api/\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "Building Repair Centre", "short_name": "BRC", "start_url": "/", "display": "browser",
        "background_color": "#ffffff", "theme_color": "#0a2552",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n", encoding="utf-8")


def main():
    build_home()
    build_about()
    build_services_hub()
    for s in SERVICES:
        if s["slug"] == "tradie-services":
            build_trades()
        else:
            build_service(s)
    build_projects()
    build_faq()
    build_contact()
    build_privacy()
    build_thanks()
    build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} indexable pages + thank-you + 404")


if __name__ == "__main__":
    main()
