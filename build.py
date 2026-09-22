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
PRICE = "$249"

# ---------------------------------------------------------------------------
# PRODUCT CATALOG — add a dashboard by copying one entry and editing it.
# "status": "available" or "development"
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "ecommerce-performance",
        "name": "E-commerce Performance Dashboard",
        "status": "available",
        "one_line": "See revenue, orders, products, and marketing performance in one place instead of five exports.",
        "for_whom": "Online stores on Shopify or a similar platform doing enough volume that the built-in reports stop being enough.",
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
        "notes": "Three report pages: a business snapshot, product performance, and marketing.",
    },
    {
        "slug": "warehouse-operations",
        "name": "Warehouse Operations Dashboard",
        "status": "available",
        "one_line": "Track throughput, accuracy, and order flow across the warehouse without building a reporting system first.",
        "for_whom": "Warehouses and fulfillment operations tracking volume and accuracy in spreadsheets or a WMS export.",
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
        "notes": "Built on a standard operations data model so it maps onto most WMS exports.",
    },
    {
        "slug": "sales-performance",
        "name": "Sales Performance Dashboard",
        "status": "development",
        "one_line": "Revenue, pipeline, and rep performance in one view for small sales teams.",
        "for_whom": "Small sales teams tracking results in a CRM export or a spreadsheet.",
        "understand": [
            "How revenue is tracking against the previous period",
            "Which products, regions, or customers are driving results",
            "How individual performance compares across the team",
        ],
        "metrics": [
            "Revenue and units by period",
            "Performance by rep, product, and customer",
            "Period-over-period comparisons",
        ],
        "notes": "In development. The final metric list is confirmed before any implementation starts.",
    },
    {
        "slug": "dental-practice",
        "name": "Dental Practice Dashboard",
        "status": "development",
        "one_line": "Production, scheduling, and patient volume for a single practice or a small group.",
        "for_whom": "Dental practices pulling reports out of practice-management software by hand each month.",
        "understand": [
            "How production is tracking month to month",
            "How full the schedule is and where the gaps are",
            "How patient visit volume is changing",
        ],
        "metrics": [
            "Production by period and by provider",
            "Appointment volume and schedule utilization",
            "New versus returning patient counts",
        ],
        "notes": "In development. The final metric list is confirmed before any implementation starts.",
    },
]

NAV = [
    ("/templates/", "Templates"),
    ("/services/", "Services"),
    ("/work/", "Work"),
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
    prod_links = "\n".join(
        f'        <li><a href="/templates/{p["slug"]}/">{p["name"].replace(" Dashboard", "")}</a></li>'
        for p in PRODUCTS
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
          <li><a href="/templates/">All templates</a></li>
          <li><a href="/services/">Services</a></li>
          <li><a href="/work/">Work</a></li>
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
<script src="/assets/site.js" defer></script>
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

def product_card(p, heading_level="h3"):
    badge = "" if p["status"] == "available" else '<p class="small" style="margin-bottom:.5rem"><em>In development &mdash; ask about availability</em></p>'
    return f'''      <article class="product">
        <!-- Replace this image with a real screenshot: /assets/previews/{p["slug"]}.png -->
        <img class="product-preview" src="/assets/previews/{p["slug"]}.svg" alt="Preview of the {p["name"]}" width="640" height="400" loading="lazy">
        <div class="product-body">
          <{heading_level}><a href="/templates/{p["slug"]}/">{p["name"]}</a></{heading_level}>
          {badge}
          <p>{p["one_line"]}</p>
          <div class="product-meta">
            <p class="price">{PRICE}<small>one-time</small></p>
            <a class="btn" href="/contact/?interest=template&amp;product={p["slug"]}">Get started</a>
          </div>
        </div>
      </article>
'''


def compare_block():
    return f'''  <div class="compare">
    <div class="compare-col card-lead">
      <h3>Dashboard template &mdash; {PRICE}</h3>
      <p>A dashboard already designed for a common business need, set up with your data.</p>
      <dl>
        <dt>Scope</dt><dd>What the template includes, plus the setup needed to fit your data</dd>
        <dt>Price</dt><dd>Fixed at {PRICE} per dashboard</dd>
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


def implementation_steps():
    return '''  <ol class="steps">
    <li>
      <h4>You tell me what you need</h4>
      <p>A short form: which dashboard, what system your data comes from, and what your business does.</p>
    </li>
    <li>
      <h4>I confirm it fits</h4>
      <p>I look at your data situation and tell you honestly whether the template works, needs changes, or whether a custom project would serve you better. No charge for this part.</p>
    </li>
    <li>
      <h4>Payment and data handoff</h4>
      <p>Once we agree it is a fit, I invoice the ''' + PRICE + ''' and you send an export or connection details.</p>
    </li>
    <li>
      <h4>Setup and delivery</h4>
      <p>I connect your data, make the adjustments needed to fit your fields, and send the finished dashboard with written instructions for using and refreshing it.</p>
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
      <h1>Business analytics and dashboards that make your data easier to understand and use.</h1>
      <p>Most small businesses already have the data they need. It is just sitting in spreadsheets, order exports, and systems that do not talk to each other. I build the dashboards and reports that turn it into something you can look at and make decisions from.</p>
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
      <figcaption>Dashboards, reporting, and analysis for small and growing businesses.</figcaption>
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
        <p class="price" style="margin-bottom:1rem">{PRICE}<small>one-time, per dashboard</small></p>
        <p>Dashboards already designed for a specific kind of business. Pick one, I set it up with your data, you start using it. Faster and cheaper than building from scratch.</p>
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
      <p class="lede">Each one is designed around a specific kind of business, priced at {PRICE}, and set up with your own data.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.5rem">
{"".join(product_card(p) for p in PRODUCTS[:3])}    </div>
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

<section class="section tint">
  <div class="wrap">
    <div class="head">
      <h2>Which one fits?</h2>
      <p class="lede">The difference between a template and custom work comes down to how specific your questions are.</p>
    </div>
    <div style="margin-top:2.5rem">
{compare_block()}    </div>
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
templates_page = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Dashboard templates</h1>
    <p>Dashboards already built for a specific kind of business. Choose one, and I set it up with your data for a fixed {PRICE}.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <!-- To add a product: copy one <article class="product"> block and edit it,
         or add an entry to PRODUCTS in build.py and re-run the build. -->
    <div class="grid grid-3">
{"".join(product_card(p, "h2") for p in PRODUCTS)}    </div>
    <p class="small" style="margin-top:2rem;max-width:62ch">More dashboards are being added. If you need something that is not here, <a href="/contact/?interest=custom">tell me what you are trying to track</a> &mdash; it may be a custom project, or it may be the next template.</p>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head">
      <h2>What {PRICE} covers</h2>
      <p class="lede">Every template includes the same implementation. It is a setup service, not open-ended development.</p>
    </div>
    <div class="grid grid-2" style="margin-top:2.5rem">
      <div class="card">
        <h3>Included</h3>
        <ul>
          <li>The dashboard template itself</li>
          <li>Connecting it to your data source or export</li>
          <li>The adjustments needed to fit your fields and naming</li>
          <li>A working, refreshable dashboard delivered to you</li>
          <li>Written instructions for using and updating it</li>
        </ul>
      </div>
      <div class="card">
        <h3>Beyond the template</h3>
        <p>If you need metrics the template does not cover, extra report pages, several data sources combined, or calculations specific to how your business works, that is a <a href="/services/#custom">custom analytics project</a> instead.</p>
        <p>I will tell you which one you need before you pay for anything.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>How implementation works</h2>
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

def product_detail(p):
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    badge = "" if p["status"] == "available" else '<p class="small"><em>This dashboard is in development. You can still get in touch to be notified or to discuss it.</em></p>'
    return f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <p class="hero-eyebrow"><a href="/templates/" style="color:var(--sand)">Dashboard templates</a></p>
    <h1>{p["name"]}</h1>
    <p>{p["one_line"]}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="layout-form">
      <div>
        <!-- Replace with a real screenshot: /assets/previews/{p["slug"]}.png -->
        <img src="/assets/previews/{p["slug"]}.svg" alt="Preview of the {p["name"]}" width="960" height="600" style="border:1px solid var(--border);border-radius:4px">

        <div class="prose" style="margin-top:3rem">
          <h2>What this dashboard helps you understand</h2>
          <ul>
{"".join(f"            <li>{u}</li>%s" % chr(10) for u in p["understand"])}          </ul>

          <h2 style="margin-top:2.5rem">Key metrics</h2>
          <!-- Edit this list as the dashboard is finalized. -->
          <ul>
{"".join(f"            <li>{m}</li>%s" % chr(10) for m in p["metrics"])}          </ul>
          <p class="small">{p["notes"]}</p>

          <h2 style="margin-top:2.5rem">What you receive</h2>
          <ul>
            <li>The dashboard, connected to your data and ready to refresh</li>
            <li>Setup and the adjustments needed to fit your fields</li>
            <li>Written instructions for using and updating it</li>
          </ul>

          <h2 style="margin-top:2.5rem">Who it is designed for</h2>
          <p>{p["for_whom"]}</p>

          <h2 style="margin-top:2.5rem">How implementation works</h2>
        </div>
        <div style="max-width:60ch;margin-top:1.5rem">
{implementation_steps()}        </div>
      </div>

      <aside>
        <div class="card card-lead">
          <p class="price" style="margin-bottom:1rem">{PRICE}<small>one-time, includes implementation</small></p>
          {badge}
          <p>Fixed price. I confirm the template fits your data before you pay anything.</p>
          <div class="card-cta">
            <a class="btn" href="/contact/?interest=template&amp;product={p["slug"]}" style="width:100%">Get started</a>
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
# Services
# ---------------------------------------------------------------------------
services = f'''<main id="main">

<section class="page-head">
  <div class="wrap">
    <h1>Services</h1>
    <p>Three ways to work together, depending on how specific your questions are and how much you need built.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article id="templates" class="prose-wide">
      <h2>Dashboard templates &mdash; {PRICE} each</h2>
      <p class="lede">Start with a proven dashboard structure instead of building one from scratch.</p>
      <p>Each template is a dashboard already designed around a specific kind of business. You buy the implementation: I connect it to your data, adjust it to fit your fields, and hand it back working, with instructions.</p>
      <h3>Who it is for</h3>
      <p>Businesses that need solid reporting on fairly standard questions and would rather have something running next week than commission a build.</p>
      <h3>What is included</h3>
      <ul>
        <li>The dashboard template</li>
        <li>Data connection and configuration</li>
        <li>The initial customization needed to fit your data</li>
        <li>Written instructions for using and refreshing it</li>
      </ul>
      <p>Significant changes beyond the template become a custom analytics project. I will say so before you pay, not after.</p>
      <div class="btn-row"><a class="btn" href="/templates/">Browse templates</a></div>
    </article>
  </div>
</section>

<section class="section tint">
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

<section class="section">
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

<section class="section tint">
  <div class="wrap">
    <div class="head"><h2>Template or custom?</h2></div>
    <div style="margin-top:2.5rem">
{compare_block()}    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap"><div class="center-narrow">
    <h2>Not sure where your project fits?</h2>
    <p class="lede" style="color:#dbe6dd">Describe the problem and I will tell you which of these makes sense.</p>
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
        <img src="/assets/previews/ecommerce-performance.svg" alt="E-commerce performance dashboard" width="960" height="600" style="border:1px solid var(--border);border-radius:4px">
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
        <img src="/assets/previews/warehouse-operations.svg" alt="Warehouse operations dashboard" width="960" height="600" style="border:1px solid var(--border);border-radius:4px">
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
        <a class="btn btn-ghost" href="/work/">See the work</a>
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
        <p>If a {PRICE} template covers it, I will say so. If it does not, I will say that too, before you pay.</p>
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
    f'              <option value="{p["slug"]}">{p["name"]} &mdash; {PRICE}</option>'
    for p in PRODUCTS
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
      <!-- ============================================================
           FORM SETUP: this form needs somewhere to send submissions.
           Sign up for Formspree, Netlify Forms, or Basin and paste the
           endpoint into the action attribute below. Nothing else changes.
           ============================================================ -->
      <form id="inquiry-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">

        <fieldset class="fieldset">
          <legend>What can England Analytics help you with?</legend>
          <div class="choices">
            <label class="choice">
              <input type="radio" name="interest" value="template" required>
              <span>A dashboard template &mdash; {PRICE}
                <em>Set up one of the ready-made dashboards with my data</em></span>
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
            <label for="dashboard">Which dashboard are you interested in?</label>
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
        <p class="form-note">I reply personally, usually within one business day. Nothing is charged and no payment details are collected here &mdash; for template requests I confirm the dashboard fits your data first, then explain payment and next steps.</p>
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
      <li><a href="/work/">Work</a></li>
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
         "Dashboards, reporting, and analytics for small and growing businesses. Ready-made dashboard templates from $249, or custom analytics work built around your business.",
         "/", home)

    page("templates/index.html",
         f"Dashboard Templates — {PRICE} Each | England Analytics",
         f"Ready-to-implement Power BI dashboard templates for e-commerce, warehouse operations, sales, and more. {PRICE} one-time, set up with your own data.",
         "/templates/", templates_page)

    for p in PRODUCTS:
        page(f"templates/{p['slug']}/index.html",
             f"{p['name']} — {PRICE} | England Analytics",
             p["one_line"],
             "/templates/", product_detail(p))

    page("services/index.html",
         "Services — Dashboards, Custom Analytics, and Data Projects | England Analytics",
         "Three ways to work together: $249 dashboard templates, custom analytics projects, and hourly data work including Excel, Power BI, and SQL.",
         "/services/", services)

    page("work/index.html",
         "Work — Dashboard Examples | England Analytics",
         "Examples of dashboards built for e-commerce and warehouse operations, including the problem each one solved and what it shows.",
         "/work/", work)

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
    urls = ["/", "/templates/", "/services/", "/work/", "/about/", "/contact/"] + \
           [f"/templates/{p['slug']}/" for p in PRODUCTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{DOMAIN}{u}</loc></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
