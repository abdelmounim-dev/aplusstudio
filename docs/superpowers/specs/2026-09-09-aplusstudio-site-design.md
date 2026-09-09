# A+ Studio portfolio site — design

Date: 2026-09-09. Status: approved in chat, implemented in the same session.

## Goal

A multi-page presentation website for Amine | A+ Studio, a bioclimatic
residential architecture practice in Algeria. English only for now. Static
HTML, no build step, so the client can host it anywhere.

## Source material

- Architectural identity analysis from the shared Claude chat
  (55150621-a648-479d-a6eb-61b573fa9bea): Critical Regionalism /
  bioclimatic design, "the house breathes", thermal mass, cross-ventilation,
  stack effect, light shelves, ergonomic kitchens, low-cost sustainability,
  residential villas, educational Reels series "#فضاء" numbered 01-07.
- Competitor `sarltmr.com` (TMR Construction): Arabic site with Home,
  Services, Projects, Real Estate, About, Contact; stats strip, FAQ,
  service request form, WhatsApp/Facebook/Instagram links.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Hero with SVG airflow cross-section, five principles, stats strip, featured projects, field notes preview, FAQ, contact CTA |
| `approach.html` | "How the house breathes": annotated plan, principle deep-dives, the studio's method in four steps |
| `services.html` | Design, execution supervision, renovation and bioclimatic consulting, process, FAQ |
| `projects.html` | Filterable grid of placeholder projects |
| `project-courtyard-villa.html` | Project detail template |
| `field-notes.html` | Episode series 01-07 as a journal |
| `about.html` | Amine, the studio, values, credentials |
| `contact.html` | Form (placeholder action), WhatsApp, Messenger, phone, address, map placeholder |

## Shared assets

- `css/site.css`: design tokens, layout, components. One file.
- `js/site.js`: mobile nav drawer, active nav link, project filter,
  FAQ accordion, form validation feedback. No dependencies.
- `assets/logo.svg`: SVG redraw of the client's mark (sheared A, orange plus) with a "Studio" wordmark; `assets/logo-mark.svg` is the mark alone.
- `assets/favicon.svg`.

## Design system

- Style: editorial minimalism, oversized serif headings, generous
  whitespace, line-art SVG diagrams instead of stock photos.
- Palette: sand `#F4EFE6` background, clay `#E8DCC8` surfaces, ink
  `#1E1913` text, muted `#5B4F43`, ochre `#914710` accent, teal `#1E5C58`
  secondary accent, dark `#2A2119` for footer and inverted sections.
  All text pairs verified at 4.5:1 or better.
- Type: Fraunces (headings) and Inter (body) from Google Fonts,
  `font-display: swap`.
- Motion: 200ms ease-out transitions, disabled under
  `prefers-reduced-motion`.
- Breakpoints: 640, 900, 1200.

## Placeholders the client must replace

Marked with `data-placeholder` in the HTML and listed in `README.md`:
stats numbers, project names and images, phone, email, WhatsApp and
Messenger links, address, form action.

## Out of scope

Arabic version, CMS, photo lightbox, real project photography, analytics.
