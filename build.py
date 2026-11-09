#!/usr/bin/env python3
"""
England Analytics — static site builder.

You do NOT need this file to run the website. Every page it writes is plain,
hand-editable HTML. It exists so you can change the header, footer, or a
product in ONE place and regenerate all pages:

    python3 build.py

Edit content in the PRODUCTS list and the page functions below.
"""

import os, shutil, textwrap

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "England Analytics"
EMAIL = "michael@englandanalytics.com"
DOMAIN = "https://englandanalytics.com"
SHOP = "https://shop.englandanalytics.com"

# ---------------------------------------------------------------------------
# SELF-SERVICE DOWNLOADS — sold through the Shopify store.
# "slug" must match the product's URL handle in Shopify; the Buy now button
# links to SHOP/products/<slug>.
# ---------------------------------------------------------------------------
DOWNLOADS = [
    {
        "slug": "ecommerce-kpi-dashboard",
        "name": "E-Commerce KPI",
        "price": "$29",
        "pages": "1",
        "image": "/assets/previews/ecommerce-kpi-1.png",
        "one_line": "20 essential metrics on one page: sales, customers, profitability, and operations.",
        "includes": [
            "20 KPI cards with month-over-month and year-over-year comparisons",
            "Interactive filters",
        ],
    },
    {
        "slug": "ecommerce-standard-dashboard",
        "name": "E-Commerce Standard",
        "price": "$79",
        "pages": "2",
        "image": "/assets/previews/ecommerce-dashboard-1.png",
        "one_line": "Sales trends, product performance, customers, and profitability across two pages.",
        "includes": [
            "Sales Performance: sales and profit trends, channels, campaigns, top products",
            "Product &amp; Customer Performance: product profit, customers, returns, discounts, location",
        ],
    },
    {
        "slug": "ecommerce-combined-dashboard",
        "name": "E-Commerce Combined",
        "price": "$99",
        "pages": "4",
        "image": "/assets/previews/ecommerce-dashboard-2.png",
        "one_line": "Everything in KPI and Standard, plus an order list, connected in one four-page dashboard.",
        "includes": [
            "The KPI page and both Standard pages",
            "An order list with products, quantities, sales, costs, and profit",
        ],
    },
]
DOWNLOADS_PAGE = "/templates/ecommerce-dashboard/"

# ---------------------------------------------------------------------------
# PRODUCT CATALOG — add a dashboard by copying one entry and editing it.
# "status": "available" or "development"
# "price":  the dollar figure for THIS product, e.g. "$99" or "$249"
# "pages":  how many report pages it includes, e.g. "2-3" or "3-4"
#           (used in the copy so the price/scope stay honest per product)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "ecommerce-business-performance",
        "name": "E-Commerce Business Performance Dashboard",
        "status": "available",
        "price": "$249",
        "pages": "3",
        "one_line": "See revenue, orders, products, and marketing performance in one place instead of five exports.",
        "best_for": "Online stores on Shopify or a similar platform doing enough volume that the built-in reports stop being enough.",
        "shots": [
            {"heading": "Executive Overview Dashboard", "image": "/assets/previews/ecommerce-business-performance-1.png"},
            {"heading": "Growth and Marketing", "image": "/assets/previews/ecommerce-business-performance-2.png"},
        ],
        "understand": [
            "How sales are tracking this month against the months before it",
            "Which products carry the revenue and which ones just take up space",
            "Where orders are coming from and what marketing is actually returning",
            "How much an average order is worth and whether that is moving",
        ],
        "metrics": [
            "Revenue, orders, and average order value with period comparisons",
            "Sales trend by day, week, and month",
            "Product-level performance and ranking",
            "Customer counts, new versus returning",
            "Marketing and channel performance",
        ],
        "notes": "3 report pages, including a full executive overview and a growth/marketing breakdown.",
    },
    {
        "slug": "warehouse-dashboard",
        "name": "Warehouse Dashboard",
      "status": "development",
      "price": "Coming soon",
      "pages": None,
      "one_line": "Warehouse self-service packages are in development, following the KPI, Standard, and Combined format.",
      "development_notes": "Planned packages will include four PBIX files (Sage, Ocean, Slate, and Sand), a sample Excel workbook, and setup instructions.",
        "best_for": "Small warehouses and fulfillment operations tracking volume in spreadsheets or a WMS export.",
        "shots": [
            {"heading": "Fulfillment Overview", "image": "/assets/previews/warehouse-dashboard-1.png"},
            {"heading": "Client & Labor", "image": "/assets/previews/warehouse-dashboard-2.png"},
        ],
        "understand": [
            "How much volume moved through the operation",
            "Where orders slow down between received and shipped",
            "Whether accuracy holds up as volume changes",
        ],
        "metrics": [
            "Orders received, picked, and shipped",
            "On-time shipment rate",
            "Order accuracy and error rates",
        ],
        "notes": "2 report pages.",
    },
    {
        "slug": "warehouse-business-performance",
        "name": "Warehouse Business Performance Dashboard",
        "status": "available",
        "price": "$249",
        "pages": "4",
        "one_line": "Track throughput, accuracy, and order flow across the warehouse without building a reporting system first.",
        "best_for": "Warehouses and fulfillment operations tracking volume and accuracy in spreadsheets or a WMS export.",
        "shots": [
            {"heading": "Warehouse Performance — Executive Summary", "image": "/assets/previews/warehouse-business-performance-1.png"},
            {"heading": "Supplier & Receiving Performance", "image": "/assets/previews/warehouse-business-performance-2.png"},
            {"heading": "Item & Inventory Detail", "image": "/assets/previews/warehouse-business-performance-3.png"},
            {"heading": "Order Fulfillment Detail", "image": "/assets/previews/warehouse-business-performance-4.png"},
        ],
        "understand": [
            "How much volume moved through the operation and how that compares to last period",
            "Where orders slow down between received and shipped",
            "Whether picking and shipping accuracy is holding up as volume changes",
            "How today or this week looks against the trend",
        ],
        "metrics": [
            "Orders received, picked, and shipped over time",
            "On-time shipment rate",
            "Order accuracy and error rates",
            "Units per hour and throughput by period",
            "Open and backlogged order volume",
        ],
        "notes": "4 report pages. Built on a standard operations data model so it maps onto most WMS exports.",
    },
    {
        "slug": "insurance-agency",
        "name": "Insurance Agency Dashboard",
        "status": "development",
        "price": "Coming soon",
        "pages": None,
        "one_line": "A dashboard for insurance agencies. In development.",
        "best_for": "Insurance agencies reporting from spreadsheets or agency-management exports.",
        "shots": [
            {"heading": "Preview", "image": "/assets/previews/insurance-agency.svg"},
        ],
        "understand": ["Details will be confirmed as the dashboard is finalized"],
        "metrics": ["Metrics will be confirmed as the dashboard is finalized"],
        "notes": "In development. Ask about availability.",
    },
]

# Computed once from PRODUCTS so headline copy never drifts out of sync
# with the actual per-product prices above.
_prices = sorted({int(p["price"][1:]) for p in PRODUCTS if p["status"] == "available" and p["price"][1:].isdigit()})
AVAILABLE_PRODUCTS = [p for p in PRODUCTS if p["status"] == "available"]
DEVELOPMENT_PRODUCTS = [p for p in PRODUCTS if p["status"] != "available"]
FEATURED_PRODUCTS = [p for p in AVAILABLE_PRODUCTS if p["slug"] in ("ecommerce-business-performance", "warehouse-business-performance")]
# PRICE_* cover the set-up-for-you templates only.
PRICE_LOW = f"${_prices[0]}"
PRICE_HIGH = f"${_prices[-1]}"
PRICE_RANGE = PRICE_LOW if PRICE_LOW == PRICE_HIGH else f"{PRICE_LOW}\u2013{PRICE_HIGH}"
# ALL_* include the self-service downloads, for copy that covers every template.
_dl_prices = sorted(int(d["price"][1:]) for d in DOWNLOADS)
DOWNLOAD_LOW = f"${_dl_prices[0]}"
DOWNLOAD_HIGH = f"${_dl_prices[-1]}"
DOWNLOAD_RANGE = f"{DOWNLOAD_LOW}\u2013{DOWNLOAD_HIGH}"
ALL_LOW = f"${min(_dl_prices[0], _prices[0])}"
ALL_RANGE = f"{ALL_LOW}\u2013{PRICE_HIGH}"

NAV = [
    (SHOP, "Shop Templates"),
    ("/services/", "Services"),
    ("/about/", "About"),
]


def logo_mark(size=30):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 30 30" aria-hidden="true" focusable="false">
      <g fill="#c49f50">
        <rect x="2"  y="18" width="3.6" height="7"/>
        <rect x="7.6" y="15" width="3.6" height="10"/>
        <rect x="13.2" y="11.5" width="3.6" height="13.5"/>
        <rect x="18.8" y="8" width="3.6" height="17"/>
        <rect x="24.4" y="4" width="3.6" height="21"/>
      </g>
      <rect x="0" y="25.5" width="30" height="1" fill="#123d2b"/>
    </svg>'''


def head(title, desc, canonical, depth):
    up = "../" * depth if depth else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/social-card.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#123d2b">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''


def header(active):
    links = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'      <a href="{href}"{cur}>{label}</a>\n'
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">
      {logo_mark()}
      <span class="brand-name">England<span>Analytics</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}      <a class="btn" href="/contact/">Get started</a>
    </nav>
  </div>
</header>
'''


def footer():
    prod_links = f'        <li><a href="{DOWNLOADS_PAGE}">E-Commerce</a></li>\n' + "\n".join(
        f'        <li><a href="/templates/{p["slug"]}/">{p["name"].replace(" Dashboard", "")}</a></li>'
        for p in FEATURED_PRODUCTS
    )
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <span class="brand-name">England<span>Analytics</span></span>
        <p style="margin-top:1rem;max-width:34ch">Business analytics and dashboards for small and growing companies. Run independently by Michael England.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Dashboard templates</h4>
        <ul>
{prod_links}
        </ul>
      </div>
      <div>
        <h4>Site</h4>
        <ul>
          <li><a href="{SHOP}">Shop</a></li>
          <li><a href="/templates/">All templates</a></li>
          <li><a href="/services/">Services</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {SITE}. All rights reserved.</span>
      <span>England Analytics is an independent business.</span>
    </div>
  </div>
</footer>
<script src="/assets/site.js?v=theme-preview-1" defer></script>
</body>
</html>
'''


def page(path, title, desc, active, body):
    depth = len([p for p in path.split("/") if p]) - 1
    depth = max(depth, 0)
    canonical = "/" + path.replace("index.html", "")
    html = head(title, desc, canonical, depth) + header(active) + body + footer()
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------

def img(p):
    shots = p.get("shots") or []
    if shots:
        return shots[0]["image"]
    return f"/assets/previews/{p['slug']}.svg"


def pages_label(p):
    return f'{p["pages"]} pages' if p.get("pages") else "Coming soon"


def product_card(p, heading_level="h3"):
    available = p["status"] == "available"
    badge = "" if available else '<p class="small" style="margin-bottom:.5rem"><em>In development</em></p>'
    badge_markup = f"          {badge}\n" if badge else ""
    price = p["price"] if available else "Coming soon"
    price_note = pages_label(p) if available else "Details to come"
    action = "Get started" if available else "View details"
    return f'''      <article class="product">
        <!-- Replace this image with a real screenshot: /assets/previews/{p["slug"]}.png -->
        <img class="product-preview" src="{img(p)}" alt="Preview of the {p["name"]}" width="640" height="400" loading="lazy">
        <div class="product-body">
          <{heading_level}><a href="/templates/{p["slug"]}/">{p["name"]}</a></{heading_level}>
{badge_markup}          <p>{p["one_line"]}</p>
          <div class="product-meta">
            <p class="price">{price}<small>{price_note}</small></p>
            <a class="btn" href="/templates/{p["slug"]}/">{action}</a>
          </div>
        </div>
      </article>
'''


def buy_url(d):
    return f"{SHOP}/products/{d['slug']}"


def download_card(d, heading_level="h3"):
    pages = "1 page" if d["pages"] == "1" else f'{d["pages"]} pages'
    return f'''      <article class="product" id="{d["slug"]}">
        <img class="product-preview" src="{d["image"]}" alt="Preview of the {d["name"]} dashboard" width="640" height="400" loading="lazy">
        <div class="product-body">
          <{heading_level}><a href="{buy_url(d)}">{d["name"]}</a></{heading_level}>
          <p>{d["one_line"]}</p>
          <div class="product-meta">
            <p class="price">{d["price"]}<small>{pages} &middot; instant download</small></p>
            <a class="btn" href="{buy_url(d)}">Buy now</a>
          </div>
        </div>
      </article>
'''


def ecommerce_family_card():
    """One card on the homepage standing in for all three e-commerce downloads."""
    return f'''      <article class="product">
        <img class="product-preview" src="{DOWNLOADS[0]["image"]}" alt="Preview of the E-Commerce dashboards" width="640" height="400" loading="lazy">
        <div class="product-body">
          <h3><a href="{DOWNLOADS_PAGE}">E-Commerce Dashboards</a></h3>
          <p>Choose KPI, Standard, or Combined. Each $29–$99 package is self-service and includes four theme files, a sample Excel workbook, and setup instructions.</p>
          <div class="product-meta">
            <p class="price">{DOWNLOAD_RANGE}<small>self-service downloads</small></p>
            <a class="btn" href="{SHOP}">Buy now</a>
          </div>
        </div>
      </article>
'''


KPI_THEMES = [
    {"name": "Sage", "image": "/assets/previews/KPI%20Sage.png", "token": "sage"},
    {"name": "Ocean", "image": "/assets/previews/KPI%20Ocean.png", "token": "ocean"},
    {"name": "Slate", "image": "/assets/previews/KPI%20Slate.png", "token": "slate"},
    {"name": "Sand", "image": "/assets/previews/KPI%20Sand.png", "token": "sand"},
]
THEME_SWATCHES = "\n".join(
    f'          <li><span class="theme-dot theme-dot--{theme["token"]}" aria-hidden="true"></span>{theme["name"]}</li>'
    for theme in KPI_THEMES
)
DOWNLOAD_FACTS = f'''<div class="download-facts">
  <div>
    <p class="download-facts-title">Four theme files in every download</p>
    <ul class="theme-swatches" aria-label="Included color themes">
{THEME_SWATCHES}
    </ul>
  </div>
  <p class="small">Each $29–$99 download includes four PBIX files (one per theme), a sample Excel workbook for your data, and setup instructions. These are self-service products; implementation and color customization are not included. Power BI Desktop is free on Windows.</p>
</div>'''


def compare_block(price_label=None):
    price_label = price_label or PRICE_RANGE
    return f'''  <div class="compare">
    <div class="compare-col card-lead">
      <h3>Dashboard setup &mdash; {price_label}</h3>
      <p>A supported dashboard connected to your data and adjusted to your fields.</p>
      <dl>
        <dt>Scope</dt><dd>Data connection, field adjustments, and a refreshable dashboard delivered ready to use.</dd>
        <dt>Price</dt><dd>$249 for selected dashboard setups</dd>
        <dt>Timeline</dt><dd>Usually running within a week of receiving your data</dd>
        <dt>Best when</dt><dd>You need solid reporting on standard business questions, soon</dd>
      </dl>
    </div>
    <div class="compare-col">
      <h3>Custom analytics &mdash; quoted per project</h3>
      <p>Built specifically for your business, around the questions you need answered.</p>
      <dl>
        <dt>Scope</dt><dd>Your metrics, your data sources, your calculations and layout</dd>
        <dt>Price</dt><dd>Based on what the project actually involves</dd>
        <dt>Timeline</dt><dd>Agreed up front, once the scope is clear</dd>
        <dt>Best when</dt><dd>A template would leave out something that matters</dd>
      </dl>
    </div>
  </div>
  <p class="small" style="margin-top:1.5rem;max-width:62ch">Not sure which one fits? Tell me what you are trying to figure out and I will point you to whichever makes sense, including the cheaper one.</p>
'''


def implementation_steps(price_label=None):
    return f'''  <ol class="steps">
    <li>
      <h4>You tell me what you need</h4>
      <p>A short form: which dashboard, what system your data comes from, and what your business does.</p>
    </li>
    <li>
      <h4>I confirm it fits</h4>
      <p>I look at your data situation and tell you honestly whether the template works, needs changes, or whether a custom project would serve you better. No charge for this part.</p>
    </li>
    <li>
      <h4>Payment and setup</h4>
      <p>Once we confirm it's a fit, I send your invoice and begin setup.</p>
    </li>
    <li>
      <h4>You're in control from here</h4>
      <p>I connect your data, make the adjustments needed to fit your fields, and send the finished dashboard with written instructions for using and refreshing it. You maintain control of your ongoing business data going forward.</p>
    </li>
  </ol>
'''


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
home = f'''<main id="main">

<section class="hero">
  <div class="wrap hero-inner">
    <div>
      <p class="hero-eyebrow">Independent business analytics, run by Michael England</p>
      <h1>Business analytics that make your data easier to use.</h1>
      <p>Turn your spreadsheets, exports, and business data into clear dashboards that help you understand what's happening and make better decisions.</p>
      <div class="btn-row">
        <a class="btn btn-gold" href="/contact/?interest=custom">Tell me about your project</a>
        <a class="btn btn-on-dark" href="/templates/">Browse dashboard templates</a>
      </div>
    </div>
    <figure class="hero-figure" style="margin:0">
      <div class="bars" role="img" aria-label="Illustration of a rising bar chart, the England Analytics mark">
        <i></i><i></i><i></i><i></i><i></i>
      </div>
      <div class="bars-base"></div>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Three ways to work together</h2>
      <p class="lede">Start with a ready-made dashboard, commission something built around your business, or hand me a single piece of work that needs doing.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.5rem">
      <article class="card card-lead">
        <h3>Dashboard templates</h3>
        <p class="price" style="margin-bottom:1rem">{DOWNLOAD_RANGE}<small>self-service downloads</small></p>
        <p>Download a ready-made KPI, Standard, or Combined dashboard. Each includes four PBIX theme files, a sample Excel workbook, and setup instructions. Data-connected implementation is available separately for $249 on selected dashboards.</p>
        <div class="card-cta"><a class="btn" href="/templates/">Browse templates</a></div>
      </article>
      <article class="card">
        <h3>Custom analytics</h3>
        <p>Custom analytics work built around your business: dashboards, reporting, data analysis, KPI development, or pulling several data sources into one place. Scope and price depend on the project.</p>
        <div class="card-cta"><a class="btn btn-ghost" href="/contact/?interest=custom">Tell me about your project</a></div>
      </article>
      <article class="card">
        <h3>Hourly and project work</h3>
        <p>For the smaller things. Excel reporting, data cleanup, a Power BI file that is misbehaving, a one-time analysis, a report that eats a day every month.</p>
        <div class="card-cta"><a class="btn btn-ghost" href="/contact/?interest=hourly">Tell me what you need</a></div>
      </article>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head">
      <h2>Dashboards built for the questions your business needs to answer</h2>
      <p class="lede">Self-service downloads are {DOWNLOAD_RANGE}. For selected dashboards, data-connected setup is available for {PRICE_LOW}.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.5rem">
{ecommerce_family_card()}{"".join(product_card(p) for p in FEATURED_PRODUCTS)}    </div>
    <div class="btn-row">
      <a class="btn btn-ghost" href="/templates/">See all dashboard templates</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Not every business needs a complicated analytics system</h2>
    </div>
    <div class="prose" style="margin-top:1.5rem">
      <p>Plenty of the reporting problems I see do not need new software or a data warehouse. They need someone to look at what you already have and build something clear on top of it.</p>
      <p>I focus on practical solutions that answer the questions you actually have about your business: which products make money, where orders slow down, what last month really looked like next to the one before it.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.5rem">
      <div class="card">
        <h4>Start with your questions</h4>
        <p>The dashboard comes after we know what you are trying to find out. That order matters more than the tool.</p>
      </div>
      <div class="card">
        <h4>Use the data you have</h4>
        <p>Spreadsheets, platform exports, and existing systems are usually enough to get something useful running.</p>
      </div>
      <div class="card">
        <h4>Build something you keep using</h4>
        <p>A report nobody opens is not worth the time it took to make. Clear beats clever.</p>
      </div>
    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap">
    <div class="center-narrow">
      <h2>Have a data problem you are trying to solve?</h2>
      <p class="lede" style="color:#dbe6dd">Let's talk about it. Tell me what is going on and I will let you know whether I can help and what it would take.</p>
      <div class="btn-row">
        <a class="btn btn-gold" href="/contact/">Get started</a>
        <a class="btn btn-on-dark" href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </div>
  </div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# Templates catalog
# ---------------------------------------------------------------------------
FAMILY_OVERVIEW = '''<section class="section family-overview">
  <div class="wrap">
    <div class="head">
      <h2>Browse dashboard families</h2>
      <p class="lede">Choose a business area first, then compare the dashboard packages available for it.</p>
    </div>
    <div class="family-grid">
      <article class="family-card">
        <img src="/assets/previews/KPI%20Sage.png" alt="E-Commerce KPI dashboard preview in Sage theme" width="1581" height="888" loading="lazy">
        <div class="family-card-body">
          <p class="family-status">Download packages</p>
          <h3>E-Commerce</h3>
          <p>KPI, Standard, and Combined packages, with all four color themes included.</p>
          <a class="family-link" href="#download-dashboards">Compare E-Commerce packages</a>
        </div>
      </article>
      <article class="family-card">
        <img src="/assets/previews/warehouse-business-performance-1.png" alt="Warehouse Business Performance dashboard preview" width="1348" height="805" loading="lazy">
        <div class="family-card-body">
          <p class="family-status">$249 setup available</p>
          <h3>Warehouse</h3>
          <p>Get a supported warehouse dashboard connected to your data. Self-service KPI, Standard, and Combined downloads are planned.</p>
          <a class="family-link" href="#setup-dashboards">View Warehouse set-up options</a>
        </div>
      </article>
      <article class="family-card family-card--planned">
        <div class="family-preview family-preview--planned" role="img" aria-label="Financial dashboard family planned">
          <span>FINANCIAL<br>PREVIEW TO COME</span>
        </div>
        <div class="family-card-body">
          <p class="family-status">Planned</p>
          <h3>Financial</h3>
          <p>Future dashboard family. Package scope, previews, and availability will be added when defined.</p>
          <span class="family-link family-link--muted">Details to come</span>
        </div>
      </article>
    </div>
  </div>
</section>'''


templates_page = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Dashboard templates</h1>
    <p>Download self-service dashboards for {DOWNLOAD_RANGE}, or choose a supported $249 dashboard setup connected to your data.</p>
  </div>
</section>
{FAMILY_OVERVIEW}

<section id="download-dashboards" class="section">
  <div class="wrap">
    <div class="head">
      <h2>Download and use today</h2>
      <p class="lede">Ready-made e-commerce dashboards. Buy, download, add your sales data, and refresh. <a href="{DOWNLOADS_PAGE}">Compare the three versions</a>.</p>
    </div>
    <!-- To add a download: add an entry to DOWNLOADS in build.py and re-run the build. -->
    <div class="grid grid-3" style="margin-top:2.5rem">
{"".join(download_card(d, "h3") for d in DOWNLOADS)}    </div>
    <div style="margin-top:2rem">{DOWNLOAD_FACTS}</div>
  </div>
</section>

<section id="setup-dashboards" class="section tint">
  <div class="wrap">
    <div class="head">
      <h2>Set up for you</h2>
      <p class="lede">Selected $249 dashboards are connected to your data, adjusted to your fields, and delivered ready to use.</p>
    </div>
    <!-- To add a product: copy one <article class="product"> block and edit it,
         or add an entry to PRODUCTS in build.py and re-run the build. -->
    <div class="grid grid-3" style="margin-top:2.5rem">
{"".join(product_card(p, "h2") for p in AVAILABLE_PRODUCTS)}    </div>
    <p class="small" style="margin-top:2rem;max-width:62ch">More dashboards are being added. If you need something that is not here, <a href="/contact/?interest=custom">tell me what you are trying to track</a> &mdash; it may be a custom project, or it may be the next template.</p>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head">
      <h2>How setup works</h2>
    </div>
    <div style="margin-top:2.5rem;max-width:60ch">
{implementation_steps()}    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>Not sure which dashboard fits your data?</h2>
    <p class="lede" style="color:#dbe6dd">Send me a note about what you are tracking today and I will tell you which template works, or whether you need something custom.</p>
    <div class="btn-row"><a class="btn btn-gold" href="/contact/">Get started</a></div>
  </div></div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# Product detail
# ---------------------------------------------------------------------------

def shot_blocks(p):
    out = []
    for s in p["shots"]:
        out.append(f'''        <div class="shot-block">
          <h3>{s["heading"]}</h3>
          <img src="{s["image"]}" alt="{s["heading"]} &mdash; {p["name"]}" width="960" height="600" loading="lazy">
        </div>
''')
    return "".join(out)


def product_detail(p):
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    available = p["status"] == "available"
    badge = "" if available else '<p class="small"><em>Self-service download in development; not available yet.</em></p>'
    badge_markup = f"          {badge}\n" if badge else ""
    if available:
        deliverables = '''<h2 style="margin-top:2.5rem">What you receive</h2>
          <ul>
            <li>The dashboard, connected to your data and ready to refresh</li>
            <li>Setup and the adjustments needed to fit your fields</li>
            <li>Written instructions for using and updating it</li>
          </ul>
          <h2 style="margin-top:2.5rem">How implementation works</h2>'''
        implementation = f'''<div style="max-width:60ch;margin-top:1.5rem">
{implementation_steps()}        </div>'''
        price = p["price"]
        price_note = "one-time, includes implementation"
        offer_text = "Fixed price for this dashboard. I confirm the template fits your data before you pay anything."
        action_href = f'/contact/?interest=template&amp;product={p["slug"]}'
        action_label = "Get started"
        closing_heading = "Ready to get started?"
        closing_text = "Tell me a bit about your business and your data, and I will confirm this dashboard fits before anything is charged."
    else:
        deliverables = f'''<h2 style="margin-top:2.5rem">Planned self-service release</h2>
          <p>{p.get("development_notes", "This product is in development. Package contents, themes, and pricing will be announced when ready.")}</p>'''
        implementation = ""
        price = "Coming soon"
        price_note = "self-service release planned"
        offer_text = "This download is not available yet. It will not include data-connected setup or color customization."
        action_href = "/contact/?interest=unsure"
        action_label = "Ask about availability"
        closing_heading = "Want to hear when it is ready?"
        closing_text = "Send a note and mention this dashboard. I can let you know when its self-service files are available."
    return f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <p class="hero-eyebrow"><a href="/templates/" style="color:var(--sand)">Dashboard templates</a></p>
    <h1>{p["name"]}</h1>
    <p>{p["one_line"]}</p>
    <p class="best-for"><strong>Best for:</strong> {p["best_for"]}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="layout-form">
      <div>
        <div class="prose">
          <h2 style="margin-top:0">See what's included</h2>
        </div>
{shot_blocks(p)}
        <div class="prose" style="margin-top:3rem">
          <h2>What this dashboard helps you understand</h2>
          <ul>
{"".join(f"            <li>{u}</li>%s" % chr(10) for u in p["understand"])}          </ul>

          <h3 style="margin-top:2rem">Key metrics</h3>
          <!-- Edit this list as the dashboard is finalized. -->
          <ul>
{"".join(f"            <li>{m}</li>%s" % chr(10) for m in p["metrics"])}          </ul>
          <p class="small">{p["notes"]}</p>

{deliverables}
        </div>
{implementation}
      </div>

      <aside>
        <div class="card card-lead">
          <p class="price" style="margin-bottom:1rem">{price}<small>{price_note}</small></p>
{badge_markup}          <p>{offer_text}</p>
          <div class="card-cta">
            <a class="btn" href="{action_href}" style="width:100%">{action_label}</a>
            <p class="small" style="margin-top:1rem">Or email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
          </div>
        </div>
        <div class="card" style="margin-top:1.5rem">
          <h4>Need something different?</h4>
          <p>If this covers most of what you need but not all of it, a <a href="/services/#custom">custom analytics project</a> is usually the better route.</p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>{closing_heading}</h2>
    <p class="lede" style="color:#dbe6dd">{closing_text}</p>
    <div class="btn-row"><a class="btn btn-gold" href="{action_href}">{action_label}</a></div>
  </div></div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head"><h2>Other dashboard templates</h2></div>
    <div class="grid grid-3" style="margin-top:2.5rem">
{"".join(product_card(q) for q in others)}    </div>
  </div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# E-commerce downloads page (replaces the old set-up E-Commerce Dashboard page,
# keeping its URL so existing links still work)
# ---------------------------------------------------------------------------

def tier_card(d):
    pages = "1 page" if d["pages"] == "1" else f'{d["pages"]} pages'
    lead = " card-lead" if d is DOWNLOADS[-1] else ""
    items = "".join(f"          <li>{i}</li>\n" for i in d["includes"])
    return f'''      <article class="card{lead}">
        <h3>{d["name"]}</h3>
        <p class="price" style="margin-bottom:1rem">{d["price"]}<small>{pages}</small></p>
        <p>{d["one_line"]}</p>
        <ul>
{items}        </ul>
        <div class="card-cta"><a class="btn" href="{buy_url(d)}" style="width:100%">Buy now</a></div>
      </article>
'''


def kpi_theme_preview():
  buttons = []
  for index, theme in enumerate(KPI_THEMES):
    selected = "true" if index == 0 else "false"
    buttons.append(f'''            <button type="button" class="theme-option" data-theme-option data-theme-name="{theme["name"]}" data-theme-src="{theme["image"]}" aria-pressed="{selected}"><span class="theme-dot theme-dot--{theme["token"]}" aria-hidden="true"></span>{theme["name"]}</button>''')
  first_theme = KPI_THEMES[0]
  return f'''        <div class="shot-block theme-preview-block" data-theme-gallery>
      <h3>KPI Snapshot</h3>
      <p class="small">In KPI and Combined</p>
      <div class="theme-options" role="group" aria-label="Preview KPI dashboard color theme">
{chr(10).join(buttons)}
      </div>
      <p class="small theme-preview-status" data-theme-status aria-live="polite">Previewing {first_theme["name"]}.</p>
      <img data-theme-preview src="{first_theme["image"]}" alt="KPI Snapshot dashboard in {first_theme["name"]} theme" width="1581" height="888" loading="lazy">
    </div>
'''


ECOM_SHOTS = [
    ("Sales Performance", "/assets/previews/ecommerce-dashboard-1.png", "In Standard and Combined"),
    ("Product &amp; Customer Performance", "/assets/previews/ecommerce-dashboard-2.png", "In Standard and Combined"),
]

ecommerce_downloads = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <p class="hero-eyebrow"><a href="/templates/" style="color:var(--sand)">Dashboard templates</a></p>
    <h1>E-Commerce Dashboards</h1>
    <p>Ready-made dashboards for online sellers. Buy, download, add your sales data, and refresh. No setup call, no waiting.</p>
    <p class="best-for"><strong>Best for:</strong> E-commerce sellers on Shopify, eBay, Poshmark, or several marketplaces at once.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><h2>Choose your version</h2></div>
    <div class="grid grid-3" style="margin-top:2.5rem">
{"".join(tier_card(d) for d in DOWNLOADS)}    </div>
    <div style="margin-top:2rem">{DOWNLOAD_FACTS}</div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="prose"><h2 style="margin-top:0">See what's included</h2></div>
{kpi_theme_preview()}{"".join(f"""        <div class="shot-block">
          <h3>{h}</h3>
          <p class="small">{note}</p>
          <img src="{src}" alt="{h} &mdash; E-Commerce Dashboards" width="960" height="600" loading="lazy">
        </div>
""" for h, src, note in ECOM_SHOTS)}  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="layout-form">
      <div>
        <div class="prose"><h2 style="margin-top:0">How it works</h2></div>
        <ol class="steps" style="max-width:60ch;margin-top:1.5rem">
          <li><h4>Buy and download</h4><p>Your files arrive right after checkout.</p></li>
          <li><h4>Pick your color theme</h4><p>All four themes are included, so choose the one that fits your business.</p></li>
          <li><h4>Add your sales data</h4><p>Fill in the included data template, then follow the setup guide to connect it.</p></li>
          <li><h4>Refresh whenever you update</h4><p>Add new sales to the template and refresh. You stay in control of your data.</p></li>
        </ol>
      </div>
      <aside>
        <div class="card">
          <h4>What you need</h4>
          <p>Power BI Desktop, which is free from Microsoft and runs on Windows. It doesn't run natively on Mac.</p>
        </div>
        <div class="card" style="margin-top:1.5rem">
          <h4>Rather have it set up for you?</h4>
          <p>The <a href="/templates/ecommerce-business-performance/">E-Commerce Business Performance Dashboard</a> is connected to your data and matched to your colors and logo for you. For something built around your business, see <a href="/services/#custom">custom analytics</a>.</p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>Ready to see your numbers clearly?</h2>
    <p class="lede" style="color:#dbe6dd">Pick a version and download it today.</p>
    <div class="btn-row"><a class="btn btn-gold" href="{SHOP}">Buy now</a></div>
  </div></div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
services = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Services</h1>
    <p>Two ways to work together, depending on how specific your questions are and how much you need built. Looking for a ready-made dashboard instead? <a href="/templates/" style="color:var(--sand)">Browse dashboard templates</a>.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article id="custom" class="prose-wide">
      <h2>Custom analytics</h2>
      <p class="lede">Custom analytics work built around your business.</p>
      <p>We start with what you are trying to figure out, then build the reporting that answers it. This is the right route when your questions are specific to how your business runs, your data lives in more than one place, or nothing off the shelf lines up.</p>
      <h3>Who it is for</h3>
      <p>Businesses with real data and real questions that do not map onto a standard dashboard.</p>
      <h3>What this can include</h3>
      <ul>
        <li>Custom dashboards and business reporting</li>
        <li>Data analysis on a specific question</li>
        <li>Combining multiple data sources into one view</li>
        <li>Excel and Power BI solutions</li>
        <li>SQL and data preparation</li>
        <li>KPI development and definitions</li>
        <li>Other analytics projects, scoped individually</li>
      </ul>
      <h3>Pricing</h3>
      <p>Quoted per project. Scope varies enough that a fixed price would be dishonest in one direction or the other, so we talk about what you need first and I give you a number before any work starts.</p>
      <div class="btn-row"><a class="btn" href="/contact/?interest=custom">Tell me about your project</a></div>
    </article>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <article id="hourly" class="prose-wide">
      <h2>Hourly and project-based analytics</h2>
      <p class="lede">For the work that does not need a whole dashboard.</p>
      <p>Sometimes the job is a single report, a messy file, or a broken measure. This is for that.</p>
      <h3>Who it is for</h3>
      <p>Anyone with a specific piece of data work that needs doing and nobody in-house with the time to do it.</p>
      <h3>Examples</h3>
      <ul>
        <li>Excel reporting and spreadsheet analysis</li>
        <li>Data cleanup and preparation</li>
        <li>Power BI help, including DAX that is not behaving</li>
        <li>SQL and data work</li>
        <li>One-time analysis for a decision you are making</li>
        <li>Troubleshooting an existing dashboard or report</li>
      </ul>
      <h3>Pricing</h3>
      <p>Based on the work involved. Small jobs get a flat quote, longer ones an hourly rate. Either way you know the cost before I start.</p>
      <div class="btn-row"><a class="btn" href="/contact/?interest=hourly">Tell me what you need</a></div>
    </article>
  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>Not sure where your project fits?</h2>
    <p class="lede" style="color:#dbe6dd">Describe the problem and I will tell you which of these makes sense, including a ready-made dashboard template if that is cheaper.</p>
    <div class="btn-row"><a class="btn btn-gold" href="/contact/">Get started</a></div>
  </div></div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# Work / portfolio
# ---------------------------------------------------------------------------
work = '''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Work</h1>
    <p>Examples of dashboards I have built, what problem each one solved, and what it shows.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">

    <!-- ===================================================================
         PORTFOLIO ITEM TEMPLATE — copy this whole <article> for each project.
         Replace the image, the four headings' content, and the title.
         Delete the .placeholder note once real content is in.
         =================================================================== -->
    <article class="layout-form" style="margin-bottom:4rem">
      <div>
        <img src="/assets/previews/ecommerce-dashboard-1.png" alt="E-commerce performance dashboard" width="960" height="600" style="border:1px solid var(--border);border-radius:4px">
      </div>
      <div>
        <h2 style="font-size:var(--t-lg)">E-commerce performance dashboard</h2>
        <h4>The problem</h4>
        <p class="small">[Add: what the business could not see before this existed.]</p>
        <h4>What it does</h4>
        <p class="small">[Add: what the dashboard shows and how it is used.]</p>
        <h4>Key metrics</h4>
        <p class="small">[Add: the main measures on it.]</p>
        <h4>Result</h4>
        <p class="small">[Add: what changed as a result. Leave this out rather than guessing.]</p>
      </div>
    </article>

    <article class="layout-form" style="margin-bottom:4rem">
      <div>
        <img src="/assets/previews/warehouse-dashboard.svg" alt="Warehouse operations dashboard" width="960" height="600" style="border:1px solid var(--border);border-radius:4px">
      </div>
      <div>
        <h2 style="font-size:var(--t-lg)">Warehouse operations dashboard</h2>
        <h4>The problem</h4>
        <p class="small">[Add: what the business could not see before this existed.]</p>
        <h4>What it does</h4>
        <p class="small">[Add: what the dashboard shows and how it is used.]</p>
        <h4>Key metrics</h4>
        <p class="small">[Add: the main measures on it.]</p>
        <h4>Result</h4>
        <p class="small">[Add: what changed as a result.]</p>
      </div>
    </article>

    <div class="placeholder">
      <h3>Adding your next project</h3>
      <p>Copy one of the article blocks above in <code>work/index.html</code>, drop a screenshot into <code>/assets/previews/</code>, and fill in the four sections. A sales performance dashboard slot is ready to go whenever that one is finished.</p>
    </div>

  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>Want something like this for your business?</h2>
    <p class="lede" style="color:#dbe6dd">Tell me what you are trying to see and I will tell you what it would take.</p>
    <div class="btn-row"><a class="btn btn-gold" href="/contact/">Get started</a></div>
  </div></div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
about = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>About England Analytics</h1>
    <p>One person, doing analytics work for businesses that need it.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose">
      <p>I am Michael England. I work in business intelligence, and England Analytics is the independent side of that: dashboards, reporting, and analysis for small and growing businesses.</p>
      <p>Most of my experience is in taking real business data &mdash; sales, orders, operations, the exports nobody enjoys opening &mdash; and turning it into reporting that people actually use. Power BI, Excel, and SQL are the tools. The harder part is usually figuring out which questions matter, and I have spent enough time in customer-facing and operational roles to know that the answer is rarely "all of them."</p>
      <p>I have an MBA with an emphasis in business analytics and a Power BI certification, which is a long way of saying I understand both halves of the conversation: the data side, and the side where someone has to make a decision on Monday.</p>
      <p>England Analytics is deliberately small. You work with me directly, you hear back from me directly, and if a project is not a good fit I will say so.</p>
      <div class="btn-row">
        <a class="btn" href="/contact/">Get in touch</a>
        <a class="btn btn-ghost" href="/templates/">Browse dashboard templates</a>
      </div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head"><h2>How I work</h2></div>
    <div class="grid grid-3" style="margin-top:2.5rem">
      <div class="card">
        <h4>Questions before tools</h4>
        <p>We establish what you need to know first. The build follows from that.</p>
      </div>
      <div class="card">
        <h4>Straight answers on scope</h4>
        <p>If a template covers it, I will say so. If it does not, I will say that too, before you pay.</p>
      </div>
      <div class="card">
        <h4>Something you can maintain</h4>
        <p>Every deliverable comes with instructions, so it keeps working when I am not around.</p>
      </div>
    </div>
  </div>
</section>

</main>
'''

# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
product_options = "\n".join(
    f'              <option value="{p["slug"]}">{p["name"]} &mdash; {p["price"]}</option>'
  for p in AVAILABLE_PRODUCTS
)

contact = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Get started</h1>
    <p>Tell me what you are working with and what you are trying to figure out. I read every message myself and reply personally.</p>
  </div>
</section>

<section class="section">
  <div class="wrap layout-form">

    <div class="form-shell">
      <!-- Netlify detects this form during deploy. Configure email notifications in Netlify. -->
      <form id="inquiry-form" name="inquiry" method="POST" data-netlify="true">
        <input type="hidden" name="form-name" value="inquiry">

        <fieldset class="fieldset">
          <legend>What can England Analytics help you with?</legend>
          <div class="choices">
            <label class="choice">
              <input type="radio" name="interest" value="template" required>
              <span>Dashboard setup &mdash; $249
                <em>Have an available dashboard connected to my data</em></span>
            </label>
            <label class="choice">
              <input type="radio" name="interest" value="download">
              <span>Self-service download question &mdash; $29–$99
                <em>Purchases are through the shop; each includes four PBIX themes, sample Excel, and setup instructions</em></span>
            </label>
            <label class="choice">
              <input type="radio" name="interest" value="custom">
              <span>Custom analytics
                <em>Build something specific to my business</em></span>
            </label>
            <label class="choice">
              <input type="radio" name="interest" value="hourly">
              <span>Hourly or project work
                <em>A report, some cleanup, or a dashboard that needs fixing</em></span>
            </label>
            <label class="choice">
              <input type="radio" name="interest" value="unsure">
              <span>Not sure yet
                <em>Help me work out which one I need</em></span>
            </label>
          </div>
        </fieldset>

        <div class="two-up">
          <div class="field">
            <label for="name">Your name</label>
            <input type="text" id="name" name="name" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="company">Business name</label>
            <input type="text" id="company" name="company" autocomplete="organization">
          </div>
        </div>

        <div class="field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" autocomplete="email" required>
        </div>

        <!-- Branch: dashboard template -->
        <div class="branch" data-branch="template" hidden>
          <div class="field">
            <label for="dashboard">Which dashboard would you like set up?</label>
            <select id="dashboard" name="dashboard" data-required>
              <option value="">Choose a dashboard</option>
{product_options}
              <option value="not-listed">Something not listed yet</option>
            </select>
          </div>
          <div class="field">
            <label for="source">What system or file does your data come from?</label>
            <p class="hint">Shopify, QuickBooks, a WMS, spreadsheets &mdash; whatever it is.</p>
            <input type="text" id="source" name="data_source" data-required>
          </div>
          <div class="field">
            <label for="biz">Briefly, what does your business do?</label>
            <textarea id="biz" name="business" data-required></textarea>
          </div>
          <div class="field">
            <label for="reqs">Questions or special requirements</label>
            <textarea id="reqs" name="requirements"></textarea>
          </div>
        </div>

        <!-- Branch: custom analytics -->
        <div class="branch" data-branch="custom" hidden>
          <div class="field">
            <label for="c-biz">What does your business do?</label>
            <textarea id="c-biz" name="business_custom" data-required></textarea>
          </div>
          <div class="field">
            <label for="goal">What are you trying to accomplish?</label>
            <textarea id="goal" name="goal" data-required></textarea>
          </div>
          <div class="field">
            <label for="current">What data and reporting do you use now?</label>
            <textarea id="current" name="current_reporting"></textarea>
          </div>
          <div class="field">
            <label for="improve">What would you most like to improve?</label>
            <textarea id="improve" name="improve"></textarea>
          </div>
          <div class="field">
            <label for="timeline">Rough timeline</label>
            <input type="text" id="timeline" name="timeline" placeholder="As soon as possible, next quarter, no rush">
          </div>
        </div>

        <!-- Branch: hourly / project -->
        <div class="branch" data-branch="hourly" hidden>
          <div class="field">
            <label for="need">What do you need help with?</label>
            <textarea id="need" name="need" data-required></textarea>
          </div>
          <div class="field">
            <label for="tools">What tools or files are involved?</label>
            <input type="text" id="tools" name="tools" placeholder="Excel, Power BI, SQL Server, CSV exports">
          </div>
          <div class="field">
            <label for="h-timeline">When do you need it done?</label>
            <input type="text" id="h-timeline" name="timeline_hourly">
          </div>
        </div>

        <!-- Branch: not sure -->
        <div class="branch" data-branch="unsure" hidden>
          <div class="field">
            <label for="u-problem">What are you trying to figure out about your business?</label>
            <p class="hint">Plain language is fine. You do not need to know what the solution is called.</p>
            <textarea id="u-problem" name="problem" data-required></textarea>
          </div>
          <div class="field">
            <label for="u-current">What do you use today to track it?</label>
            <input type="text" id="u-current" name="current_tools">
          </div>
        </div>

        <div class="field">
          <label for="anything">Anything else I should know?</label>
          <textarea id="anything" name="anything"></textarea>
        </div>

        <button class="btn btn-gold" type="submit">Send inquiry</button>
        <p class="form-note">I reply personally, usually within one business day. This form does not take payment. For $249 setup requests I confirm the dashboard fits your data before sending an invoice. Self-service downloads are purchased through the shop and do not include implementation or color customization.</p>
      </form>
    </div>

    <aside class="contact-aside">
      <dl>
        <dt>Email</dt>
        <dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Response time</dt>
        <dd>Usually within one business day.</dd>
        <dt>Who you are writing to</dt>
        <dd>Michael England, directly. England Analytics is an independent business.</dd>
      </dl>
      <div class="card" style="margin-top:2rem">
        <h4>Prefer to browse first?</h4>
        <p>Have a look at the <a href="/templates/">dashboard templates</a> to see whether one of them already covers what you need.</p>
      </div>
    </aside>

  </div>
</section>

</main>
'''

not_found = '''<main id="main">
<section class="section" style="padding-top:6rem">
  <div class="wrap prose">
    <h1 style="font-size:var(--t-2xl)">That page does not exist</h1>
    <p>The link may be out of date. Everything on the site is one of these:</p>
    <ul>
      <li><a href="/templates/">Dashboard templates</a></li>
      <li><a href="/services/">Services</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Get started</a></li>
    </ul>
  </div>
</section>
</main>
'''

# ---------------------------------------------------------------------------
# Write everything
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    page("index.html",
         "England Analytics — Business Analytics and Dashboards for Small Businesses",
          f"Self-service Power BI dashboards from {DOWNLOAD_LOW} to {DOWNLOAD_HIGH}, $249 data-connected setup for selected dashboards, and custom analytics for small businesses.",
         "/", home)

    page("templates/index.html",
         f"Dashboard Templates — {ALL_RANGE} | England Analytics",
          f"Self-service Power BI downloads from {DOWNLOAD_LOW} to {DOWNLOAD_HIGH}, plus selected dashboard setup connected to your data for {PRICE_LOW}.",
         "/templates/", templates_page)

    for p in PRODUCTS:
        page(f"templates/{p['slug']}/index.html",
             f"{p['name']} — {p['price']} | England Analytics",
             p["one_line"],
             "/templates/", product_detail(p))

    page("templates/ecommerce-dashboard/index.html",
         f"E-Commerce Dashboards — from {DOWNLOAD_LOW} | England Analytics",
         f"Ready-made Power BI dashboards for online sellers. KPI, Standard, and Combined versions from {DOWNLOAD_LOW}. Instant download, four color themes.",
         "/templates/", ecommerce_downloads)

    page("services/index.html",
         "Services — Dashboards, Custom Analytics, and Data Projects | England Analytics",
          f"Self-service dashboards from {DOWNLOAD_LOW} to {DOWNLOAD_HIGH}, selected $249 dashboard setup, custom analytics projects, and hourly data work.",
         "/services/", services)

    page("about/index.html",
         "About — Michael England | England Analytics",
         "England Analytics is an independent analytics business run by Michael England, covering business intelligence, Power BI, Excel, and SQL work for small businesses.",
         "/about/", about)

    page("contact/index.html",
         "Get Started — Contact England Analytics",
         "Tell me about your dashboard, reporting, or analytics project. Email michael@englandanalytics.com or use the inquiry form.",
         "/contact/", contact)

    page("404.html", "Page not found | England Analytics",
         "That page does not exist.", "/", not_found)

    # robots + sitemap
    urls = ["/", "/templates/", "/services/", "/about/", "/contact/"] + \
           [f"/templates/{p['slug']}/" for p in PRODUCTS] + [DOWNLOADS_PAGE]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{DOMAIN}{u}</loc></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
