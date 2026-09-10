# A+ Studio — portfolio website

Static, multi-page presentation site for Amine | A+ Studio, a bioclimatic
residential architecture practice in Algeria. English at the root, Arabic
under `ar/`. Plain HTML output, one stylesheet, one script. Pages are
generated from `build/` with Python 3 and nothing else.

## Run locally

```sh
python3 -m http.server 8080
```

Then open <http://localhost:8080> (English) or <http://localhost:8080/ar/> (Arabic).

## Edit content and rebuild

Text lives in `build/content_ar.py` and `build/content_en.py`; page
structure, diagrams, and icons live in `build/build.py`. After editing:

```sh
python3 build/build.py
```

This rewrites the eight root pages and the eight `ar/` pages. Commit the
generated HTML with the source. Never hand-edit the HTML files.

## Pages

| File | Content |
|------|---------|
| `index.html`, `ar/index.html` | Hero, principles, stats, services, projects, field notes, FAQ |
| `approach.html` | How the house breathes: physics, principles, method |
| `services.html` | Design, execution supervision, renovation and consulting, FAQ |
| `projects.html` | Filterable project grid |
| `project-courtyard-villa.html` | Project detail template |
| `field-notes.html` | Episode series 01 to 07 |
| `about.html` | Amine and the studio |
| `contact.html` | Form, WhatsApp, Messenger, phone, email, map |

Every page exists in both languages with the same file name. Shared files: `css/site.css`, `js/site.js`, `assets/logo.svg`, `assets/logo-mark.svg`, `assets/favicon.svg`. The home page also loads `js/day.js`, which drives the scroll-driven "a day in the house" hero: scroll progress maps to the hour, the sun, wall heat, airflow, and captions follow, and a Thermal view toggle switches to a heat-map rendering. Under `prefers-reduced-motion` the hero is a static 15:00 frame with the captions listed.

## Placeholders to replace before launch

Every placeholder carries a `data-placeholder` attribute. Find them with:

```sh
grep -rn 'data-placeholder' *.html ar/*.html
```

| Key | What to supply |
|-----|----------------|
| `whatsapp`, `messenger`, `phone`, `email`, `address` | Real contact details (footer, contact page, CTA bands) |
| `facebook`, `instagram` | Profile URLs |
| `stat` | Real figures for the stats strip on the home page |
| `project` | Real project names, locations, areas, outcomes, and photographs |
| `portrait`, `bio`, `credential` | Photograph, biography, diploma and registration details |
| `turnstile-sitekey` | Real Turnstile site key in `build/build.py` (`TURNSTILE_SITE_KEY`); the test key always passes |
| `map` | A map embed for the studio address |

The logo is an SVG redraw of the studio's mark: `assets/logo-mark.svg`
holds the mark alone, `assets/logo.svg` adds the "Studio" wordmark and is
inlined in the header and footer of every page. The A uses `currentColor`
so it inverts on dark backgrounds; the plus stays brand orange `#F4511E`.
If the client supplies vector artwork, replace the polygons in both files
and re-copy the header and footer markup into each page.

## Design

Tokens live at the top of `css/site.css`. The palette follows the logo:
off-white paper, near-black ink, and one orange accent `#F4511E` (darkened
to `#C43E0E` for small text so it meets 4.5:1). Shapes are rectangular with no rounding, and heroes carry a faint construction grid.
Fonts: Archivo and Inter for English, Cairo for Arabic. Layout uses logical
CSS properties so `dir="rtl"` mirrors it. Scroll reveal, stat count-up, and
hover motion are transform and opacity only, and are disabled entirely under
`prefers-reduced-motion`.

Design notes: `docs/superpowers/specs/2026-09-09-aplusstudio-site-design.md`.

## Deploy on Cloudflare Pages

The contact form posts to `/api/contact`, a Pages Function in
`functions/api/contact.js`. It validates the fields, checks the Turnstile
token, and emails the studio through Resend. Cloudflare deploys the function
with the site; no separate Worker is needed.

1. In the Cloudflare dashboard create a Pages project from the GitHub repo.
   Build command: empty. Output directory: `/`. `wrangler.toml` supplies the
   rest.
2. Create a Turnstile widget (Turnstile, Add site, domain of the Pages
   project). Put the site key in `build/build.py` as `TURNSTILE_SITE_KEY`,
   rebuild, and commit. Add the secret key to the project as
   `TURNSTILE_SECRET_KEY`.
3. Create a Resend account, verify the studio's domain, and add the API key
   to the project as `RESEND_API_KEY`. Set the `CONTACT_TO` and
   `CONTACT_FROM` variables in the dashboard or in `wrangler.toml`.

Secrets can also be set from the terminal:

```sh
npx wrangler pages secret put RESEND_API_KEY
npx wrangler pages secret put TURNSTILE_SECRET_KEY
```

Until `RESEND_API_KEY` is set the function logs the message and still
reports success, so preview deployments can exercise the form. Until
`TURNSTILE_SECRET_KEY` is set the token check is skipped.

Local test with the real routing:

```sh
cp .dev.vars.example .dev.vars
npx wrangler pages dev .
```

Then open <http://localhost:8788/contact.html>. The test keys in
`.dev.vars.example` make Turnstile always pass.
