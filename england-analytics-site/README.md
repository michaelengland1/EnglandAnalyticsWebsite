# England Analytics — website (v1)

Plain HTML, one CSS file, one small JS file. No build step required, no framework,
nothing to install. Every page is hand-editable.

## Preview it locally

Because the pages link to each other with root-relative paths (`/templates/`),
open it through a tiny local server rather than double-clicking the files:

```bash
cd site
python3 -m http.server 8000
# then open http://localhost:8000
```

## Put it online

Drag the whole folder into **Netlify Drop** (app.netlify.com/drop) or **Cloudflare
Pages**, then point `englandanalytics.com` at it. Both are free for a site this
size, both give you HTTPS, and both serve `/templates/` style clean URLs and the
`404.html` page automatically.

## Before you launch — three things to do

1. **Hook up the form.** `contact/index.html` has
   `action="https://formspree.io/f/YOUR_FORM_ID"`. Create a free form at
   Formspree (or use Netlify Forms / Basin) and paste the endpoint in. Until you
   do, submissions go nowhere. Send yourself a test message.
2. **Swap in real dashboard screenshots.** The previews in `assets/previews/`
   are placeholder illustrations. Replace them with PNG exports of your actual
   dashboards and update the `src` in the matching pages (search for
   `assets/previews/`).
3. **Fill in `work/index.html`.** Two portfolio slots are built and waiting for
   the problem / what it does / key metrics / result text. This page does more
   for credibility than any other copy on the site.

## Where things live

```
index.html                     Home
templates/index.html           Product catalog
templates/<slug>/index.html    One page per dashboard product
services/index.html            The three services
work/index.html                Portfolio (structure ready, content to add)
about/index.html               About
contact/index.html             The single inquiry form
404.html
assets/site.css                All styling. Brand colors are in the :root block at the top.
assets/site.js                 Mobile menu, form branching, URL prefill
assets/previews/               Dashboard preview images
assets/logo.png                Your logo
assets/favicon.svg             Browser icon
assets/social-card.png         Link-sharing image (1200×630)
robots.txt, sitemap.xml
build.py                       Optional: regenerates all pages from shared parts
```

## Colors (sampled from your logo)

| Token | Value | Used for |
|---|---|---|
| `--green` | `#123d2b` | Logo background green: hero, page headers, buttons |
| `--green-deep` | `#0c2a1d` | Headings, footer, hover states |
| `--gold` / `--gold-deep` / `--gold-light` | `#c49f50` / `#b99342` / `#e6c979` | Bar mark, rules, prices, primary CTA |
| `--sand` | `#d5c299` | The "ANALYTICS" wordmark color: labels on dark |
| `--paper` | `#fcfcfa` | Page background |
| `--ink` | `#14231c` | Body text |

Change any of these once in `assets/site.css` and the whole site follows.
Type is Archivo (headings, UI) and Source Serif 4 (body), loaded from Google Fonts.

## Adding a new dashboard product

**The quick way:** open `templates/index.html`, copy one whole
`<article class="product">` block, and edit the name, description, slug, and
image. Then copy a `templates/<slug>/` folder for the detail page. Add it to the
select list in `contact/index.html` too.

**The tidy way:** add an entry to the `PRODUCTS` list in `build.py` and run
`python3 build.py`. It rewrites every page — catalog, detail page, footer links,
form options, and sitemap — from that one list. Note that this overwrites any
edits you made directly in the generated HTML, so pick one approach and stick
with it.

## How the CTAs feed the form

Every button points at the one form with parameters, e.g.
`/contact/?interest=template&product=warehouse-operations`. The form reads them
and pre-selects the service and the dashboard, so the visitor only answers the
questions that apply to them. `interest` accepts `template`, `custom`, `hourly`,
or `unsure`.

## Later, when you want checkout

The structure is already shaped for it: each product has its own URL, its own
price display, and its own CTA. Adding Stripe means swapping the "Get started"
link on a product page for a payment button and adding an onboarding form after
payment. Nothing above it has to be redesigned.
