#!/usr/bin/env python3
"""Generate the A+ Studio site. Arabic at the repo root, English under en/.
Run from anywhere: python3 build/build.py
"""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ICON = {
 "wind": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/></svg>',
 "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 2 8.5 4.5L12 11 3.5 6.5 12 2z"/><path d="m3.5 12 8.5 4.5 8.5-4.5"/><path d="m3.5 17.5 8.5 4.5 8.5-4.5"/></svg>',
 "ruler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4z"/><path d="m14 7 2 2M11 10l2 2M8 13l2 2"/></svg>',
 "hammer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 12-8.5 8.5a2.1 2.1 0 1 1-3-3L12 9"/><path d="M17.6 15 21 11.6a1 1 0 0 0 0-1.4l-5.2-5.2a1 1 0 0 0-1.4 0L11 8.4"/><path d="m14 5 4 4"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.5 5-6.5"/></svg>',
 "arrow": '<svg class="flip" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8 9.7a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.5 2.6.7a2 2 0 0 1 1.7 2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 7L2 7"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8.5 8.5 0 0 1-12.3 7.6L3 21l1.4-5.7A8.5 8.5 0 1 1 21 12z"/></svg>',
 "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>',
 "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor"/></svg>',
}
LOGO = open(os.path.join(ROOT, "assets/logo.svg")).read().strip()
FONTS = {
 "en": "https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Inter:wght@400;500;600&display=swap",
 "ar": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap",
}
PLACEHOLDER = {"whatsapp":"https://wa.me/213000000000","messenger":"https://m.me/aplusstudio","phone":"+213000000000","phone_text":"+213 000 00 00 00","email":"hello@aplusstudio.dz","facebook":"https://www.facebook.com/","instagram":"https://www.instagram.com/"}

# ---------- diagrams ----------
def hero_svg(L):
    return f'''<svg class="diagram" viewBox="0 0 560 380" role="img" aria-labelledby="hero-svg-title hero-svg-desc">
  <title id="hero-svg-title">{L["hero_title"]}</title><desc id="hero-svg-desc">{L["hero_desc"]}</desc>
  <line x1="20" y1="330" x2="540" y2="330" class="wall"/>
  <rect x="60" y="150" width="150" height="180" class="mass"/><rect x="350" y="120" width="150" height="210" class="mass"/>
  <path d="M60 150 L135 95 L210 150" class="wall"/><path d="M350 120 L425 65 L500 120" class="wall"/>
  <path d="M210 150 L210 330 M350 120 L350 330" class="wall"/><path d="M210 150 L350 120" class="wall"/>
  <rect x="235" y="255" width="90" height="75" fill="none" class="thin"/>
  <path d="M245 330 q10 -30 0 -60 M265 330 q-8 -24 0 -50 M300 330 q10 -30 0 -60 M315 330 q-6 -20 0 -40" class="leaf" fill="none"/>
  <circle cx="255" cy="266" r="6" class="leaf"/><circle cx="305" cy="270" r="7" class="leaf"/><circle cx="280" cy="282" r="5" class="leaf"/>
  <path d="M500 200 L540 200 M500 214 L540 214 M500 228 L540 228 M500 242 L540 242" class="thin"/><path d="M500 190 L545 190 L545 255 L500 255" class="thin"/>
  <path d="M60 240 L40 240 M60 260 L40 260 M60 280 L40 280" class="thin"/>
  <path d="M25 300 Q60 300 100 300 T175 290 T230 250 T280 190 T290 130 T280 60" class="air"/>
  <path d="M25 275 Q70 270 130 270 T215 240 T255 200 T275 150 T268 100 T250 45" class="air"/>
  <path d="M280 60 L270 70 M280 60 L290 70 M250 45 L241 56 M250 45 L262 52" class="air" stroke-dasharray="0"/>
  <circle cx="500" cy="40" r="18" class="sun"/><path d="M500 10 v-6 M500 70 v6 M470 40 h-6 M530 40 h6 M479 19 l-4 -4 M521 61 l4 4 M521 19 l4 -4 M479 61 l-4 4" class="sun"/>
  <path d="M485 62 L455 118 M498 66 L470 120 M472 55 L440 115" class="sun" stroke-dasharray="3 5" stroke-width="1.4"/>
  <text x="30" y="355" class="label">{L["hero_l1"]}</text><text x="235" y="355" class="label">{L["hero_l2"]}</text><text x="420" y="355" class="label">{L["hero_l3"]}</text><text x="25" y="40" class="label">{L["hero_l4"]}</text>
</svg>'''

def plan_svg(L):
    return f'''<svg class="diagram" viewBox="0 0 560 420" role="img" aria-labelledby="plan-title plan-desc">
  <title id="plan-title">{L["plan_title"]}</title><desc id="plan-desc">{L["plan_desc"]}</desc>
  <rect x="40" y="40" width="480" height="340" class="wall" fill="none"/><rect x="200" y="140" width="160" height="140" class="thin" fill="none"/>
  <path d="M40 140 H200 M360 140 H520 M40 280 H200 M360 280 H520 M200 40 V140 M360 40 V140 M200 280 V380 M360 280 V380" class="wall"/>
  <rect x="40" y="40" width="12" height="340" class="mass"/><rect x="508" y="40" width="12" height="340" class="mass"/>
  <path d="M40 90 h-14 M40 100 h-14 M40 110 h-14" class="thin"/><path d="M520 300 h14 M520 310 h14 M520 320 h14" class="thin"/>
  <path d="M60 100 C 120 100, 160 120, 200 200 S 300 220, 360 200 S 460 300, 500 310" class="air"/>
  <path d="M215 160 q8 12 0 24 q-8 12 0 24 q8 12 0 24 M240 160 q8 12 0 24 q-8 12 0 24 q8 12 0 24" class="leaf" fill="none"/>
  <circle cx="300" cy="200" r="22" class="thin" fill="none"/><circle cx="300" cy="200" r="12" class="thin" fill="none"/>
  <path d="M210 380 h140 M215 392 h130 M220 404 h120" class="sun"/>
  <path d="M40 300 q10 -8 20 0 q10 8 20 0 q10 -8 20 0 q10 8 20 0" class="leaf" fill="none"/>
  <g><rect x="47" y="87" width="26" height="26" class="marker" transform="skewX(-20) translate(36 0)"/><text x="60" y="100" class="marker-text">1</text></g>
  <g><rect x="287" y="137" width="26" height="26" class="marker" transform="skewX(-20) translate(54 0)"/><text x="300" y="150" class="marker-text">2</text></g>
  <g><rect x="501" y="187" width="26" height="26" class="marker" transform="skewX(-20) translate(73 0)"/><text x="514" y="200" class="marker-text">3</text></g>
  <g><rect x="267" y="379" width="26" height="26" class="marker" transform="skewX(-20) translate(143 0)"/><text x="280" y="392" class="marker-text">4</text></g>
  <g><rect x="87" y="317" width="26" height="26" class="marker" transform="skewX(-20) translate(120 0)"/><text x="100" y="330" class="marker-text">5</text></g>
  <text x="70" y="70" class="label">{L["plan_living"]}</text><text x="380" y="70" class="label">{L["plan_kitchen"]}</text><text x="70" y="310" class="label">{L["plan_patio"]}</text><text x="380" y="310" class="label">{L["plan_bedrooms"]}</text><text x="250" y="130" class="label">{L["plan_court"]}</text>
</svg>'''

SKETCH = {
 "courtyard": '<svg class="diagram" viewBox="20 20 280 200" aria-hidden="true"><rect x="30" y="30" width="260" height="180" class="wall" fill="none"/><rect x="120" y="90" width="80" height="60" class="thin" fill="none"/><path d="M30 90 H120 M200 90 H290 M30 150 H120 M200 150 H290 M120 30 V90 M200 30 V90 M120 150 V210 M200 150 V210" class="wall"/><circle cx="160" cy="120" r="14" class="leaf"/><path d="M40 120 C 90 100, 110 140, 120 120" class="air"/></svg>',
 "villa": '<svg class="diagram" viewBox="0 0 320 240" aria-hidden="true"><path d="M30 200 H290" class="wall"/><rect x="60" y="110" width="200" height="90" class="mass"/><path d="M60 110 L160 60 L260 110" class="wall"/><path d="M180 200 V150 H230 V200" class="thin"/><path d="M80 130 h50 M80 145 h50 M80 160 h50" class="sun"/><circle cx="270" cy="50" r="12" class="sun"/></svg>',
 "tower": '<svg class="diagram" viewBox="0 0 320 240" aria-hidden="true"><path d="M30 210 H290" class="wall"/><rect x="100" y="40" width="120" height="170" class="wall" fill="none"/><path d="M100 80 H220 M100 120 H220 M100 160 H220" class="thin"/><path d="M140 210 V40" class="air"/><path d="M225 60 h30 M225 100 h30 M225 140 h30" class="sun"/><path d="M140 40 l-8 10 M140 40 l8 10" class="air" stroke-dasharray="0"/></svg>',
 "kitchen": '<svg class="diagram" viewBox="0 0 320 240" aria-hidden="true"><rect x="40" y="40" width="240" height="160" class="wall" fill="none"/><rect x="40" y="150" width="240" height="50" class="mass"/><rect x="40" y="40" width="60" height="110" class="mass"/><path d="M110 70 h150 M110 100 h150" class="thin"/><path d="M130 80 v-30 M200 80 v-30 M260 80 v-30" class="sun"/><circle cx="150" cy="175" r="10" class="thin" fill="none"/><circle cx="220" cy="175" r="10" class="thin" fill="none"/></svg>',
 "facade": '<svg class="diagram" viewBox="0 0 320 240" aria-hidden="true"><rect x="60" y="30" width="200" height="180" class="wall" fill="none"/><path d="M60 75 H260 M60 120 H260 M60 165 H260" class="thin"/><path d="M80 210 q0 -60 20 -90 q10 -30 -5 -60 M140 210 q0 -70 25 -100 q10 -40 -10 -70 M210 210 q5 -60 -15 -90 q-10 -40 10 -70" class="leaf" fill="none"/><circle cx="98" cy="120" r="6" class="leaf"/><circle cx="170" cy="90" r="7" class="leaf"/><circle cx="200" cy="150" r="6" class="leaf"/><circle cx="130" cy="170" r="5" class="leaf"/></svg>',
 "reno": '<svg class="diagram" viewBox="0 0 320 240" aria-hidden="true"><path d="M30 200 H290" class="wall"/><rect x="50" y="100" width="130" height="100" class="mass"/><rect x="180" y="70" width="90" height="130" class="wall" fill="none"/><path d="M180 70 L225 40 L270 70" class="wall"/><path d="M195 90 h60 M195 110 h60 M195 130 h60" class="sun"/><path d="M70 130 h30 v40 h-30z" class="thin" fill="none"/><path d="M120 130 h30 v40 h-30z" class="thin" fill="none"/></svg>',
 "portrait": '<svg class="diagram" viewBox="0 0 400 480" aria-hidden="true"><rect x="40" y="40" width="320" height="400" class="thin" fill="none"/><circle cx="200" cy="180" r="60" class="thin" fill="none"/><path d="M110 400 C 110 300, 290 300, 290 400" class="thin" fill="none"/><path d="M60 60 h80 M60 75 h50" class="sun"/></svg>',
}

# ---------- shell ----------
def shell_head(T, P, title, desc):
    lang, d = T["lang"], T["dir"]
    other = T["switch_href"]
    nav = "".join(f'        <li><a href="{h}">{t}</a></li>\n' for h,t in T["nav"])
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{d}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · A+ Studio</title>
  <meta name="description" content="{desc}">
  <link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg">
  <link rel="alternate" hreflang="{T["alt_lang"]}" href="{other}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS[lang]}">
  <link rel="stylesheet" href="{P}css/site.css">
</head>
<body>
<a class="skip-link" href="#main">{T["skip"]}</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="{T["home_label"]}">{LOGO}</a>
    <nav aria-label="{T["nav_label"]}">
      <ul class="nav-list">
{nav}      </ul>
    </nav>
    <div class="nav-right">
      <a class="lang-switch" href="{other}" lang="{T["alt_lang"]}" hreflang="{T["alt_lang"]}">{T["switch_label"]}</a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-drawer" aria-label="{T["menu_label"]}">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
  </div>
  <div class="drawer container" id="nav-drawer" data-open="false">
    <ul>
{nav}    </ul>
  </div>
</header>
<main id="main" tabindex="-1">
'''

def cta(T):
    c = T["cta"]
    return f'''
<section class="section section--dark">
  <div class="container cta">
    <div><p class="eyebrow">{c["eyebrow"]}</p><h2>{c["h2"]}</h2><p class="lede">{c["lede"]}</p></div>
    <div class="btn-row">
      <a class="btn btn--primary" href="contact.html">{c["primary"]} {ICON["arrow"]}</a>
      <a class="btn btn--ghost" href="{PLACEHOLDER["whatsapp"]}" data-placeholder="whatsapp">{c["whatsapp"]}</a>
    </div>
  </div>
</section>
'''

def foot(T, P):
    f = T["footer"]
    return f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" aria-label="{T["home_label"]}">{LOGO}</a>
        <p>{f["tagline"]}</p>
        <div class="social">
          <a href="{PLACEHOLDER["facebook"]}" aria-label="Facebook" data-placeholder="facebook">{ICON["facebook"]}</a>
          <a href="{PLACEHOLDER["instagram"]}" aria-label="Instagram" data-placeholder="instagram">{ICON["instagram"]}</a>
          <a href="{PLACEHOLDER["whatsapp"]}" aria-label="WhatsApp" data-placeholder="whatsapp">{ICON["chat"]}</a>
        </div>
      </div>
      <div><h4>{f["studio"]}</h4><ul>
        <li><a href="approach.html">{T["nav"][1][1]}</a></li><li><a href="services.html">{T["nav"][2][1]}</a></li><li><a href="projects.html">{T["nav"][3][1]}</a></li><li><a href="about.html">{T["nav"][5][1]}</a></li>
      </ul></div>
      <div><h4>{f["learn"]}</h4><ul>
        <li><a href="field-notes.html">{T["nav"][4][1]}</a></li><li><a href="services.html#faq">{f["questions"]}</a></li><li><a href="contact.html">{T["nav"][6][1]}</a></li>
      </ul></div>
      <div><h4>{f["contact"]}</h4><ul>
        <li><a href="tel:{PLACEHOLDER["phone"]}" data-placeholder="phone" dir="ltr">{PLACEHOLDER["phone_text"]}</a></li>
        <li><a href="mailto:{PLACEHOLDER["email"]}" data-placeholder="email">{PLACEHOLDER["email"]}</a></li>
        <li data-placeholder="address">{f["address"]}</li>
      </ul></div>
    </div>
    <div class="footer-bottom"><p>{f["rights"]}</p><p>{f["strap"]}</p></div>
  </div>
</footer>
<script src="{P}js/site.js" defer></script>
</body>
</html>
'''

# ---------- components ----------
def project_card(p):
    cls = "project" + (" project--tall" if p.get("tall") else "")
    return f'''<a class="{cls}" href="project-courtyard-villa.html" data-type="{p["type"]}" data-placeholder="project">
  <div class="project__media">{SKETCH[p["kind"]]}</div>
  <div class="project__body"><div class="project__meta"><span>{p["city"]}</span><span>{p["meta"]}</span></div><h3>{p["name"]}</h3><p>{p["desc"]}</p></div>
</a>'''

def note_card(e):
    return f'''<a class="note" href="field-notes.html#ep-{e["num"]}"><span class="note__num">{e["num"]}</span><h3>{e["title"]}</h3><p>{e["quote"]}</p><span class="note__tag">{e["tag"]}</span></a>'''

def faq(items, id_="faq"):
    return f'<div class="faq" id="{id_}">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items) + '</div>'

def principles(T):
    return '<ol class="principles">' + "".join(f'<li class="principle"><span class="principle__num" aria-hidden="true"><span>{i+1}</span></span><div><h3>{t}</h3><p>{d}</p></div></li>' for i,(t,d) in enumerate(T["principles"])) + '</ol>'

def steps(items):
    return '<ol class="steps mt-4">' + "".join(f'<li class="step"><h3>{t}</h3><p>{d}</p></li>' for t,d in items) + '</ol>'

def service_cards(T):
    s = T["services_cards"]; icons = ["ruler","hammer","leaf"]; ids = ["design","execution","renovation"]
    return "".join(f'<article class="card"><div class="card__icon">{ICON[icons[i]]}</div><h3>{t}</h3><p>{d}</p><a class="card__link" href="services.html#{ids[i]}">{T["learn_more"]} {ICON["arrow"]}</a></article>' for i,(t,d) in enumerate(s))

# ---------- pages ----------
def build_pages(T):
    L = T["labels"]; H = hero_svg(L); PL = plan_svg(L); pages = {}
    g = T["pages"]
    h = g["home"]
    pages["index.html"] = (h["title"], h["desc"], f'''
<section class="hero"><div class="container hero__grid">
  <div><p class="eyebrow">{h["eyebrow"]}</p><h1>{h["h1"]}</h1><p class="lede">{h["lede"]}</p>
    <div class="btn-row"><a class="btn btn--primary" href="contact.html">{T["cta"]["primary"]} {ICON["arrow"]}</a><a class="btn btn--ghost" href="approach.html">{h["secondary"]}</a></div></div>
  <figure class="hero__diagram">{H}</figure>
</div></section>
<section class="section section--grey section--tight"><div class="container stats">
  {"".join(f'<div class="stat" data-placeholder="stat"><div class="stat__value">{v}</div><div class="stat__label">{l}</div></div>' for v,l in h["stats"])}
</div></section>
<section class="section"><div class="container split split--wide">
  <figure class="figure">{PL}<figcaption>{h["plan_caption"]}</figcaption></figure>
  <div><p class="eyebrow">{h["principles_eyebrow"]}</p><h2>{h["principles_h2"]}</h2><p class="lede">{h["principles_lede"]}</p>{principles(T)}
    <div class="btn-row mt-4"><a class="btn btn--ghost" href="approach.html">{h["principles_btn"]} {ICON["arrow"]}</a></div></div>
</div></section>
<section class="section section--grey"><div class="container">
  <div class="section-head"><div><p class="eyebrow">{T["nav"][2][1]}</p><h2>{h["services_h2"]}</h2></div><a class="btn btn--ghost" href="services.html">{h["services_btn"]}</a></div>
  <div class="grid grid--3">{service_cards(T)}</div>
</div></section>
<section class="section"><div class="container">
  <div class="section-head"><div><p class="eyebrow">{h["work_eyebrow"]}</p><h2>{T["nav"][3][1]}</h2></div><a class="btn btn--ghost" href="projects.html">{h["work_btn"]}</a></div>
  <div class="project-grid">{"".join(project_card(p) for p in T["projects"][:3])}</div>
</div></section>
<section class="section section--dark"><div class="container">
  <div class="section-head"><div><p class="eyebrow">{T["nav"][4][1]}</p><h2>{h["notes_h2"]}</h2></div><a class="btn btn--ghost" href="field-notes.html">{h["notes_btn"]}</a></div>
  <div class="notes-strip">{"".join(note_card(e) for e in T["episodes"])}</div>
</div></section>
<section class="section"><div class="container split">
  <div><p class="eyebrow">{h["faq_eyebrow"]}</p><h2>{h["faq_h2"]}</h2><p class="lede">{h["faq_lede"]}</p></div>{faq(T["faq"][:3], "faq-home")}
</div></section>
{cta(T)}''')

    a = g["approach"]
    pages["approach.html"] = (a["title"], a["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][1][1]}</p><h1>{a["h1"]}</h1><p class="lede">{a["lede"]}</p></div></section>
<section class="section"><div class="container split split--wide">
  <div class="prose"><h2>{a["why_h2"]}</h2><p>{a["why_p1"]}</p><p>{a["why_p2"]}</p><div class="callout"><p><strong>{a["callout_strong"]}</strong> {a["callout"]}</p></div></div>
  <figure class="figure">{H}<figcaption>{a["section_caption"]}</figcaption></figure>
</div></section>
<section class="section section--grey"><div class="container"><p class="eyebrow">{a["five_eyebrow"]}</p><h2>{a["five_h2"]}</h2>
  <div class="split split--wide mt-5"><figure class="figure">{PL}<figcaption>{a["plan_caption"]}</figcaption></figure>{principles(T)}</div>
</div></section>
<section class="section"><div class="container"><p class="eyebrow">{a["effects_eyebrow"]}</p><h2>{a["effects_h2"]}</h2>
  <div class="grid grid--3 mt-4">{"".join(f'<article class="card"><div class="card__icon">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></article>' for i,(t,d) in zip(["wind","layers","sun"], a["effects"]))}</div>
</div></section>
<section class="section section--dark"><div class="container"><p class="eyebrow">{a["light_eyebrow"]}</p>
  <div class="split"><blockquote class="quote">{a["light_quote"]}<cite>{a["light_cite"]}</cite></blockquote><div><p>{a["light_p1"]}</p><p>{a["light_p2"]}</p></div></div>
</div></section>
<section class="section"><div class="container"><p class="eyebrow">{a["method_eyebrow"]}</p><h2>{a["method_h2"]}</h2>{steps(a["method"])}</div></section>
{cta(T)}''')

    s = g["services"]
    def svc(id_, icon, sk, title, lede, p, items, cap, flip=False):
        text = f'<div><div class="card__icon">{ICON[icon]}</div><h2>{title}</h2><p class="lede">{lede}</p><p>{p}</p><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>'
        fig = f'<figure class="figure">{SKETCH[sk]}<figcaption>{cap}</figcaption></figure>'
        return f'<section class="section{" section--grey" if flip else ""}" id="{id_}"><div class="container split">{fig+text if flip else text+fig}</div></section>'
    pages["services.html"] = (s["title"], s["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][2][1]}</p><h1>{s["h1"]}</h1><p class="lede">{s["lede"]}</p></div></section>
{svc("design","ruler","villa",*s["design"])}
{svc("execution","hammer","tower",*s["execution"], flip=True)}
{svc("renovation","leaf","facade",*s["renovation"])}
<section class="section section--dark"><div class="container"><p class="eyebrow">{s["process_eyebrow"]}</p><h2>{s["process_h2"]}</h2>{steps(s["process"])}</div></section>
<section class="section"><div class="container split"><div><p class="eyebrow">{s["faq_eyebrow"]}</p><h2>{s["faq_h2"]}</h2></div>{faq(T["faq"], "faq")}</div></section>
{cta(T)}''')

    pr = g["projects"]
    pages["projects.html"] = (pr["title"], pr["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][3][1]}</p><h1>{pr["h1"]}</h1><p class="lede">{pr["lede"]}</p></div></section>
<section class="section"><div class="container">
  <div class="filters" role="group" aria-label="{pr["filter_label"]}">{"".join(f'<button class="filter" type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{l}</button>' for k,l in T["filters"])}</div>
  <p class="visually-hidden" id="filter-status" aria-live="polite" data-status-template="{pr["status_template"]}">{pr["status_template"].replace("{n}", str(len(T["projects"])))}</p>
  <div class="project-grid">{"".join(project_card(p) for p in T["projects"])}</div>
</div></section>
{cta(T)}''')

    d = g["detail"]
    pages["project-courtyard-villa.html"] = (d["title"], d["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow"><a href="projects.html">{T["nav"][3][1]}</a> · {d["crumb"]}</p><h1>{d["h1"]}</h1><p class="lede">{d["lede"]}</p></div></section>
<section class="section"><div class="container split split--wide">
  <figure class="figure">{H}<figcaption>{d["section_caption"]}</figcaption></figure>
  <dl class="spec-list">{"".join(f'<div><dt>{k}</dt><dd data-placeholder="project">{v}</dd></div>' for k,v in d["specs"])}</dl>
</div></section>
<section class="section section--grey"><div class="container prose"><p class="eyebrow">{d["brief_eyebrow"]}</p>
  {"".join(f"<h2>{h2}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for h2,ps in d["story"])}
</div></section>
<section class="section"><div class="container"><p class="eyebrow">{d["drawings_eyebrow"]}</p><h2>{d["drawings_h2"]}</h2>
  <div class="grid grid--2 mt-4"><figure class="figure">{PL}<figcaption>{d["plan_caption"]}</figcaption></figure><figure class="figure">{SKETCH["courtyard"]}<figcaption>{d["sketch_caption"]}</figcaption></figure></div>
</div></section>
<section class="section section--grey"><div class="container"><div class="section-head"><div><p class="eyebrow">{d["more_eyebrow"]}</p><h2>{d["more_h2"]}</h2></div><a class="btn btn--ghost" href="projects.html">{pr["all_btn"]}</a></div>
  <div class="project-grid">{"".join(project_card(p) for p in T["projects"][1:4])}</div></div></section>
{cta(T)}''')

    fn = g["field_notes"]
    pages["field-notes.html"] = (fn["title"], fn["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][4][1]}</p><h1>{fn["h1"]}</h1><p class="lede">{fn["lede"]}</p></div></section>
<section class="section"><div class="container notes-list">
  {"".join(f'<article class="episode" id="ep-{e["num"]}"><span class="episode__num" aria-hidden="true">{e["num"]}</span><div><h2>{e["title"]}</h2><div class="episode__meta"><span>{fn["episode_word"]} {e["num"]}</span><span>{e["tag"]}</span></div><blockquote>{e["quote"]}</blockquote><p>{e["body"]}</p><ul>{"".join(f"<li>{b}</li>" for b in e["bullets"])}</ul></div></article>' for e in T["episodes"])}
</div></section>
<section class="section section--grey"><div class="container split"><div><p class="eyebrow">{fn["follow_eyebrow"]}</p><h2>{fn["follow_h2"]}</h2><p class="lede">{fn["follow_lede"]}</p></div>
  <div class="btn-row"><a class="btn btn--ghost" href="{PLACEHOLDER["facebook"]}" data-placeholder="facebook">{ICON["facebook"]} Facebook</a><a class="btn btn--ghost" href="{PLACEHOLDER["instagram"]}" data-placeholder="instagram">{ICON["instagram"]} Instagram</a></div></div></section>
{cta(T)}''')

    ab = g["about"]
    pages["about.html"] = (ab["title"], ab["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][5][1]}</p><h1>{ab["h1"]}</h1><p class="lede">{ab["lede"]}</p></div></section>
<section class="section"><div class="container split split--wide">
  <div class="prose"><h2>{ab["why_h2"]}</h2><p data-placeholder="bio">{ab["why_p1"]}</p><p>{ab["why_p2"]}</p><h2>{ab["believe_h2"]}</h2><ul>{"".join(f"<li>{b}</li>" for b in ab["beliefs"])}</ul></div>
  <figure class="figure" data-placeholder="portrait">{SKETCH["portrait"]}<figcaption>{ab["portrait_caption"]}</figcaption></figure>
</div></section>
<section class="section section--grey"><div class="container"><p class="eyebrow">{ab["cred_eyebrow"]}</p><h2>{ab["cred_h2"]}</h2>
  <div class="grid grid--3 mt-4">{"".join(f'<article class="card" data-placeholder="credential"><h3>{t}</h3><p>{d}</p></article>' for t,d in ab["credentials"])}</div></div></section>
<section class="section section--dark"><div class="container split"><blockquote class="quote">{ab["quote"]}<cite>{ab["quote_cite"]}</cite></blockquote>
  <div><p>{ab["series_p"]}</p><div class="btn-row"><a class="btn btn--ghost" href="field-notes.html">{ab["series_btn"]} {ICON["arrow"]}</a></div></div></div></section>
{cta(T)}''')

    c = g["contact"]; f = c["form"]
    pages["contact.html"] = (c["title"], c["desc"], f'''
<section class="page-hero"><div class="container"><p class="eyebrow">{T["nav"][6][1]}</p><h1>{c["h1"]}</h1><p class="lede">{c["lede"]}</p></div></section>
<section class="section"><div class="container split split--wide" style="align-items:start">
  <form class="form" id="contact-form" action="#" method="post" data-demo="true" data-demo-message="{f["demo_message"]}" novalidate data-placeholder="form-action">
    <div class="form-row">
      <div class="field"><label for="name">{f["name"]} <span aria-hidden="true">*</span></label><input id="name" name="name" type="text" autocomplete="name" required><span class="error">{f["name_err"]}</span></div>
      <div class="field"><label for="phone">{f["phone"]} <span aria-hidden="true">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" dir="ltr" required><span class="hint">{f["phone_hint"]}</span><span class="error">{f["phone_err"]}</span></div>
    </div>
    <div class="field"><label for="email">{f["email"]}</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" dir="ltr"><span class="error">{f["email_err"]}</span></div>
    <div class="form-row">
      <div class="field"><label for="wilaya">{f["wilaya"]}</label><input id="wilaya" name="wilaya" type="text" autocomplete="address-level1"></div>
      <div class="field"><label for="service">{f["service"]}</label><select id="service" name="service">{"".join(f'<option value="{v}">{l}</option>' for v,l in f["services"])}</select></div>
    </div>
    <div class="field"><label for="message">{f["message"]} <span aria-hidden="true">*</span></label><textarea id="message" name="message" required minlength="20"></textarea><span class="hint">{f["message_hint"]}</span><span class="error">{f["message_err"]}</span></div>
    <div class="btn-row"><button class="btn btn--primary" type="submit">{f["submit"]} {ICON["arrow"]}</button></div>
    <p class="form-status" id="form-status" role="status" tabindex="-1" hidden></p>
  </form>
  <div>
    <ul class="contact-list">
      <li>{ICON["chat"]}<div><strong>WhatsApp</strong><a href="{PLACEHOLDER["whatsapp"]}" data-placeholder="whatsapp">{c["whatsapp_text"]}</a></div></li>
      <li>{ICON["facebook"]}<div><strong>Messenger</strong><a href="{PLACEHOLDER["messenger"]}" data-placeholder="messenger" dir="ltr">m.me/aplusstudio</a></div></li>
      <li>{ICON["phone"]}<div><strong>{c["phone_label"]}</strong><a href="tel:{PLACEHOLDER["phone"]}" data-placeholder="phone" dir="ltr">{PLACEHOLDER["phone_text"]}</a></div></li>
      <li>{ICON["mail"]}<div><strong>{c["email_label"]}</strong><a href="mailto:{PLACEHOLDER["email"]}" data-placeholder="email" dir="ltr">{PLACEHOLDER["email"]}</a></div></li>
      <li>{ICON["pin"]}<div><strong>{c["studio_label"]}</strong><span data-placeholder="address">{c["address"]}</span></div></li>
    </ul>
    <div class="map mt-4" data-placeholder="map"><span>{c["map_text"]}</span></div>
  </div>
</div></section>''')
    return pages

def main():
    for mod, outdir, prefix in [("content_ar", ROOT, ""), ("content_en", os.path.join(ROOT, "en"), "../")]:
        T = importlib.import_module(mod).T
        os.makedirs(outdir, exist_ok=True)
        for fname, (title, desc, body) in build_pages(T).items():
            T["switch_href"] = T["switch_prefix"] + fname
            with open(os.path.join(outdir, fname), "w") as fh:
                fh.write(shell_head(T, prefix, title, desc) + body + foot(T, prefix))
            print("wrote", os.path.relpath(os.path.join(outdir, fname), ROOT))

if __name__ == "__main__":
    main()
