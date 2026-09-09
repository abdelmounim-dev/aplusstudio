# A+ Studio — portfolio website

Static, multi-page presentation site for Amine | A+ Studio, a bioclimatic
residential architecture practice in Algeria. Plain HTML, one stylesheet,
one script, no build step.

## Run locally

```sh
python3 -m http.server 8080
```

Then open <http://localhost:8080>.

## Pages

| File | Content |
|------|---------|
| `index.html` | Hero, principles, stats, services, projects, field notes, FAQ |
| `approach.html` | How the house breathes: physics, principles, method |
| `services.html` | Design, execution supervision, renovation and consulting, FAQ |
| `projects.html` | Filterable project grid |
| `project-courtyard-villa.html` | Project detail template |
| `field-notes.html` | Episode series 01 to 07 |
| `about.html` | Amine and the studio |
| `contact.html` | Form, WhatsApp, Messenger, phone, email, map |

Shared files: `css/site.css`, `js/site.js`, `assets/logo.svg`, `assets/favicon.svg`.

## Placeholders to replace before launch

Every placeholder carries a `data-placeholder` attribute. Find them with:

```sh
grep -rn 'data-placeholder' *.html
```

| Key | What to supply |
|-----|----------------|
| `whatsapp`, `messenger`, `phone`, `email`, `address` | Real contact details (footer, contact page, CTA bands) |
| `facebook`, `instagram` | Profile URLs |
| `stat` | Real figures for the stats strip on the home page |
| `project` | Real project names, locations, areas, outcomes, and photographs |
| `portrait`, `bio`, `credential` | Photograph, biography, diploma and registration details |
| `form-action` | A form backend. Set `action` on `#contact-form` and remove `data-demo="true"` |
| `map` | A map embed for the studio address |

The logo in `assets/logo.svg` is a placeholder wordmark. Replace the file
with the studio's logo, keeping the 220×48 viewBox or adjusting `.brand svg`
height in `css/site.css`.

## Design

Tokens live at the top of `css/site.css`. Palette: sand background, clay
surfaces, ink text, ochre accent, teal secondary. Fonts: Fraunces and Inter
from Google Fonts. Motion is disabled under `prefers-reduced-motion`.

Design notes: `docs/superpowers/specs/2026-09-09-aplusstudio-site-design.md`.
