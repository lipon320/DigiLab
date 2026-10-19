# -*- coding: utf-8 -*-
"""
DigiLab static site generator.
Run:  python3 tools/build.py
It reads tools/data.py and writes every HTML page into the project folder.
"""
import os
import sys
import html
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from data import *  # noqa

# ------------------------------------------------------------------ settings
SITE_URL = ""  # e.g. "https://yourname.github.io/digilab"  (leave empty to skip sitemap.xml)
NATIVE_ID = "container-ee2cdecf3c964b907fd537f1f4bb4642"
SMARTLINK = "https://www.profitableratecpmnetwork.com/rmzd9ec7d?key=8fb231e25030a5ea7876242ecc7534fa"

e = html.escape
PAGES = []  # for sitemap


# ------------------------------------------------------------------ small helpers
def money(n):
    return "${:,}".format(n)


def icon(name):
    return '<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>' % ICONS[name]


def ad_banner():
    return '<div class="ad ad-banner" data-ad="banner"></div>'


def ad_native():
    return '<div class="ad ad-native"><div id="%s"></div></div>' % NATIVE_ID


def sponsor():
    return ('<aside class="sponsor"><small>Sponsored</small>'
            '<p>Discover partner offers and deals from our advertising network.</p>'
            '<a class="btn btn-o btn-sm" href="%s" target="_blank" rel="sponsored nofollow noopener">View sponsored offers</a></aside>' % SMARTLINK)


def faq_html(items):
    return "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in items)


def checks(items):
    return '<ul class="checks">%s</ul>' % "".join("<li>%s</li>" % e(i) for i in items)


def min_price(s):
    return min(p[1] for p in s["pk"])


LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#4338ca"/><stop offset="1" stop-color="#0891b2"/></linearGradient></defs>'
        '<rect width="64" height="64" rx="16" fill="url(#lg)"/>'
        '<path d="M20 16h13a16 16 0 0 1 0 32H20z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>'
        '<circle cx="46" cy="18" r="4" fill="#fff"/></svg>')

FOOT_LOGO = LOGO.replace('id="lg"', 'id="lg2"').replace('url(#lg)', 'url(#lg2)')  # unique gradient id in footer

HERO_ART = '''<svg viewBox="0 0 440 340" role="img" aria-label="Illustration of a marketing dashboard with charts and a video tile">
<defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4338ca"/><stop offset="1" stop-color="#0891b2"/></linearGradient></defs>
<rect x="30" y="30" width="300" height="220" rx="22" style="fill:var(--card);stroke:var(--line)" stroke-width="2"/>
<rect x="54" y="56" width="90" height="12" rx="6" style="fill:var(--line)"/>
<rect x="54" y="78" width="140" height="8" rx="4" style="fill:var(--line)"/>
<rect x="60" y="170" width="28" height="56" rx="6" fill="url(#hg)" opacity=".45"/>
<rect x="100" y="146" width="28" height="80" rx="6" fill="url(#hg)" opacity=".65"/>
<rect x="140" y="126" width="28" height="100" rx="6" fill="url(#hg)" opacity=".8"/>
<rect x="180" y="100" width="28" height="126" rx="6" fill="url(#hg)"/>
<path d="M226 190c24-8 34-32 52-34s28 12 40-10" fill="none" stroke="#0891b2" stroke-width="5" stroke-linecap="round"/>
<circle cx="318" cy="146" r="7" fill="#0891b2"/>
<rect x="240" y="188" width="76" height="38" rx="10" style="fill:var(--soft)"/>
<rect x="250" y="199" width="40" height="8" rx="4" fill="#4338ca" opacity=".6"/>
<rect x="250" y="212" width="24" height="6" rx="3" fill="#4338ca" opacity=".35"/>
<rect x="250" y="196" width="170" height="110" rx="22" fill="url(#hg)"/>
<circle cx="335" cy="251" r="24" fill="#fff" opacity=".95"/>
<path d="M328 239l20 12-20 12z" fill="#4338ca"/>
<rect x="268" y="282" width="134" height="7" rx="3.5" fill="#fff" opacity=".5"/>
<circle cx="64" cy="286" r="20" style="fill:var(--card);stroke:var(--line)" stroke-width="2"/>
<path d="M56 286l6 6 10-12" fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="96" y="272" width="110" height="10" rx="5" style="fill:var(--line)"/>
<rect x="96" y="290" width="70" height="8" rx="4" style="fill:var(--line)"/>
</svg>'''


# ------------------------------------------------------------------ layout
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def page(path, title, desc, body, active="", noindex=False):
    depth = path.count("/")
    r = "../" * depth
    nav_items = [("Home", "index.html", "home"), ("Services", "services.html", "services"),
                 ("Careers", "careers.html", "careers"), ("About", "about.html", "about"),
                 ("Contact", "contact.html", "contact")]
    nav = "".join('<a href="%s%s"%s>%s</a>' % (r, href, ' class="on" aria-current="page"' if key == active else "", label)
                  for label, href, key in nav_items)
    nav += '<a class="btn btn-p btn-sm" href="%scontact.html">Get a quote</a>' % r
    full_title = title if title.startswith(BRAND) else "%s | %s" % (title, BRAND)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    svc_links = "".join('<li><a href="%sservices/%s.html">%s</a></li>' % (r, s["slug"], e(s["name"])) for s in SERVICES[:6])
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#4338ca">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:site_name" content="{BRAND}">
{robots}
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/css/style.css">
</head>
<body>
<header class="hdr"><div class="container">
<a class="logo" href="{r}index.html" aria-label="{BRAND} home">{LOGO}<span>Digi<b>Lab</b></span></a>
<button class="burger" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
<nav class="nav" aria-label="Main">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer class="ftr"><div class="container">
<div class="fgrid">
<div><a class="logo" href="{r}index.html">{FOOT_LOGO}<span>Digi<b>Lab</b></span></a>
<p style="margin-top:14px">A remote-first digital agency. Marketing, advertising, web design, AI, video and data, delivered by a global team of specialists.</p></div>
<div><h4>Services</h4><ul>{svc_links}<li><a href="{r}services.html">All services</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{r}about.html">About us</a></li><li><a href="{r}careers.html">Careers</a></li><li><a href="{r}apply.html">Apply now</a></li><li><a href="{r}contact.html">Contact</a></li></ul></div>
<div><h4>Legal</h4><ul><li><a href="{r}privacy.html">Privacy policy</a></li><li><a href="{r}terms.html">Terms of use</a></li></ul>
<p style="margin-top:12px">All prices are in US dollars (USD).</p></div>
</div>
<div class="legal"><span>&copy; <span class="yr">{datetime.date.today().year}</span> {BRAND}. All rights reserved.</span>
<span>This website displays advertising from third-party networks. <a href="{r}privacy.html">Learn more</a></span></div>
</div></footer>
<script src="{r}assets/js/config.js"></script>
<script src="{r}assets/js/main.js" defer></script>
<script src="{r}assets/js/ads.js" defer></script>
</body>
</html>
'''
    write(path, doc)
    if not noindex:
        PAGES.append(path)


def hero(h1, lead, crumbs="", extra=""):
    return f'''<section class="hero sm"><div class="container">{crumbs}
<h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>'''


def crumbs(r, trail):
    parts = ['<a href="%sindex.html">Home</a>' % r]
    for label, href in trail:
        parts.append('<a href="%s%s">%s</a>' % (r, href, e(label)) if href else e(label))
    return '<div class="crumbs">%s</div>' % " / ".join(parts)


def cta_band(title="Ready to start your project?", text="Book a free 30-minute discovery call. No pressure, just a clear plan and a written quote in USD.", r=""):
    return f'''<section class="section"><div class="container"><div class="band"><h2>{e(title)}</h2><p>{e(text)}</p>
<a class="btn btn-p" href="{r}contact.html">Get a free quote</a></div></div></section>'''


# ------------------------------------------------------------------ pages
def build_home():
    r = ""
    svc_cards = "".join(
        f'''<a class="card" href="services/{s["slug"]}.html">{icon(s["icon"])}<h3>{e(s["name"])}</h3><p>{e(s["tag"])}</p>
<span class="more">From {money(min_price(s))} &rarr;</span></a>''' for s in SERVICES)
    why = [("globe", "Global specialists", "We hire skilled people from around the world, so you get the right expert instead of whoever is free."),
           ("dollar", "Transparent USD pricing", "Every package shows its price. No hidden fees, and you approve a written quote before work starts."),
           ("clock", "Async-first, always on", "Shared boards and weekly updates mean progress is visible without endless meetings."),
           ("shield", "Confidential by default", "NDA on request, least-privilege access and clean hand-over of every file."),
           ("zap", "Fast turnaround", "Small tasks in days, full websites in weeks, with clear delivery dates."),
           ("users", "One point of contact", "A named project lead keeps everything organised, whatever the size of the team.")]
    why_html = "".join(f'<div class="card">{icon(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in why)
    steps = "".join(f'<div class="card"><div class="num">{i + 1}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(COMMON_PROCESS))
    feat_idx = [0, 5, 8, 13, 16, 19]
    jobs = "".join(job_card(JOBS[i], r) for i in feat_idx)
    body = f'''
<section class="hero"><div class="container split">
<div><span class="eyebrow">Remote-first digital agency</span>
<h1>Your complete digital team, <span>on demand.</span></h1>
<p class="lead">Marketing, advertising, web design, AI automation, video editing and data analysis, delivered by vetted remote specialists at clear USD prices.</p>
<div class="hero-cta"><a class="btn btn-p" href="contact.html">Get a free quote</a><a class="btn btn-o" href="services.html">Explore services</a></div>
<div class="pills"><span class="pill">10 services</span><span class="pill">Prices in USD</span><span class="pill">Fully remote</span><span class="pill">Free discovery call</span></div></div>
<div>{HERO_ART}</div></div></section>
<div class="container">{ad_banner()}</div>
<section class="section" id="services"><div class="container">
<div class="center"><span class="eyebrow">What we do</span><h2>Everything your business needs online</h2>
<p class="lead">Pick one service or combine several under one project lead.</p></div>
<div class="grid" style="margin-top:36px">{svc_cards}</div></div></section>
<section class="section alt"><div class="container">
<div class="center"><span class="eyebrow">Why DigiLab</span><h2>Agency quality without agency overhead</h2></div>
<div class="grid g3" style="margin-top:36px">{why_html}</div>
{ad_native()}</div></section>
<section class="section"><div class="container">
<div class="center"><span class="eyebrow">How it works</span><h2>From first call to launch in four steps</h2></div>
<div class="grid" style="margin-top:36px">{steps}</div>{ad_banner()}</div></section>
<section class="section alt" id="careers"><div class="container">
<div class="split" style="margin-bottom:32px"><div><span class="eyebrow">Careers</span><h2>Join our remote talent network</h2>
<p class="lead">We are building a global bench of freelancers and remote team members across 25 roles. Work from anywhere, get paid in USD.</p></div>
<div style="text-align:right"><a class="btn btn-p" href="careers.html">See all {len(JOBS)} roles</a></div></div>
<div class="grid g3">{jobs}</div></div></section>
<section class="section"><div class="container" style="max-width:820px">
<div class="center"><span class="eyebrow">FAQ</span><h2>Questions, answered</h2></div>
<div style="margin-top:28px">{faq_html(HOME_FAQ)}</div>{sponsor()}</div></section>
{cta_band(r=r)}
<div class="container">{ad_banner()}</div>
'''
    page("index.html", "DigiLab - Remote Digital Agency for Marketing, Web, AI & Video",
         "DigiLab is a remote-first digital agency offering digital marketing, paid ads, web design, AI automation, video editing, SEO and data analysis. Transparent USD pricing.",
         body, "home")


def build_services():
    r = ""
    cards = "".join(
        f'''<a class="card" href="services/{s["slug"]}.html">{icon(s["icon"])}<h3>{e(s["name"])}</h3><p>{e(s["intro"])}</p>
<span class="more">From {money(min_price(s))} &middot; View details &rarr;</span></a>''' for s in SERVICES)
    steps = "".join(f'<div class="card"><div class="num">{i + 1}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(COMMON_PROCESS))
    body = f'''
{hero("Digital services built around your growth", "Ten services, one remote team. Mix and match, or let us manage everything under a single lead.", crumbs(r, [("Services", None)]))}
<div class="container">{ad_banner()}</div>
<section class="section"><div class="container"><div class="grid">{cards}</div>{ad_native()}</div></section>
<section class="section alt"><div class="container"><div class="center"><h2>How every project runs</h2></div>
<div class="grid" style="margin-top:32px">{steps}</div>{ad_banner()}{sponsor()}</div></section>
{cta_band(r=r)}
<div class="container">{ad_banner()}</div>
'''
    page("services.html", "Services", "Explore DigiLab services: digital marketing, paid advertising, web design, AI automation, video editing, data analysis, SEO, social media, branding and IT support. Prices in USD.", body, "services")


def build_service(s):
    r = "../"
    pk = ""
    for name, price, unit, feats, hot in s["pk"]:
        pk += f'''<div class="card price{' hot' if hot else ''}"><h3>{e(name)}</h3>
<div class="amt">{money(price)}<small>{e(unit)}</small></div>{checks(feats)}
<a class="btn {'btn-p' if hot else 'btn-o'} btn-block" href="{r}contact.html">Get started</a></div>'''
    steps = "".join(f'<li><strong>{e(t)}.</strong> {e(d)}</li>' for t, d in COMMON_PROCESS)
    tools = "".join('<span class="tag">%s</span>' % e(t) for t in s["tools"])
    others = [x for x in SERVICES if x["slug"] != s["slug"]]
    start = SERVICES.index(s)
    rel = [SERVICES[(start + k) % len(SERVICES)] for k in (1, 2, 3)]
    rel_html = "".join(f'<a class="card" href="{x["slug"]}.html">{icon(x["icon"])}<h3>{e(x["name"])}</h3><p>{e(x["tag"])}</p></a>' for x in rel)
    body = f'''
<section class="hero sm"><div class="container">{crumbs(r, [("Services", "services.html"), (s["name"], None)])}
<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">{icon(s["icon"])}<h1 style="margin:0">{e(s["name"])}</h1></div>
<p class="lead" style="margin-top:14px">{e(s["tag"])}</p>
<div class="hero-cta" style="margin-top:22px"><a class="btn btn-p" href="{r}contact.html">Get a free quote</a><a class="btn btn-o" href="#pricing">See pricing</a></div></div></section>
<div class="container">{ad_banner()}</div>
<section class="section"><div class="container split" style="align-items:start">
<div><h2>What we do</h2><p class="lead" style="margin-bottom:22px">{e(s["intro"])}</p>{checks(s["does"])}</div>
<div class="card"><h3>What you get</h3>{checks(s["deliver"])}<h3 style="margin-top:22px">Tools we use</h3><div class="stack">{tools}</div></div></div></section>
<section class="section alt" id="pricing"><div class="container"><div class="center"><span class="eyebrow">Pricing in USD</span><h2>Simple, transparent packages</h2>
<p class="lead">Starting prices shown. Your final quote depends on scope and is confirmed in writing before we begin.</p></div>
<div class="grid g3" style="margin-top:40px">{pk}</div>{ad_native()}</div></section>
<section class="section"><div class="container split" style="align-items:start">
<div><h2>How it works</h2><ol class="steps">{steps}</ol>{ad_banner()}</div>
<div><h2>Frequently asked</h2>{faq_html(s["faq"])}{sponsor()}</div></div></section>
<section class="section alt"><div class="container"><h2>Related services</h2><div class="grid g3">{rel_html}</div></div></section>
{cta_band(r=r)}
<div class="container">{ad_banner()}</div>
'''
    page("services/%s.html" % s["slug"], s["name"] + " Services",
         "%s %s Packages from %s. Remote specialists, clear USD pricing." % (s["name"], s["tag"], money(min_price(s))), body, "services")


def job_card(j, r):
    text = " ".join([j["title"], j["dept"], j["type"]] + j["tools"]).lower()
    return f'''<a class="card job job-card" href="{r}jobs/{j["slug"]}.html" data-dept="{e(j["dept"])}" data-text="{e(text)}">
<div class="meta"><span class="tag">{e(j["dept"])}</span><span class="tag g">{e(j["type"])}</span></div>
<h3>{e(j["title"])}</h3><p style="margin:0">{e(j["summary"])}</p>
<div class="foot"><span>Remote &middot; {e(j["pay"])}</span><span class="more">View role &rarr;</span></div></a>'''


def build_careers():
    r = ""
    chips = '<button class="chip on" data-dept="all">All roles</button>' + "".join(
        '<button class="chip" data-dept="%s">%s</button>' % (e(d), e(d)) for d in DEPTS)
    cards = "".join(job_card(j, r) for j in JOBS)
    perks = [("globe", "Work from anywhere", "Fully remote roles open to candidates worldwide."),
             ("dollar", "Paid in USD", "Clear indicative rates for every role, paid by bank transfer, Wise or PayPal."),
             ("zap", "Real client projects", "Work on live projects with documented processes and a named project lead."),
             ("users", "Grow with us", "Strong performers receive more hours, bigger projects and lead roles.")]
    perks_html = "".join(f'<div class="card">{icon(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in perks)
    steps = "".join(f'<div class="card"><div class="num">{i + 1}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(HIRING_STEPS))
    body = f'''
{hero("Build your career with DigiLab", "Join our global remote talent network. Choose from %d roles across marketing, design, AI, video, data and operations." % len(JOBS), crumbs(r, [("Careers", None)]),
      '<div class="hero-cta"><a class="btn btn-p" href="#open-roles">Browse open roles</a><a class="btn btn-o" href="apply.html?role=general">Send open application</a></div>')}
<div class="container">{ad_banner()}</div>
<section class="section" id="open-roles"><div class="container">
<div class="note"><strong>How hiring works at DigiLab:</strong> we are a growing agency building a bench of remote specialists. Applications are reviewed on a rolling basis and we contact candidates when a matching client project starts. Pay ranges are indicative USD rates.</div>
<div class="toolbar"><input id="q" class="search" type="search" placeholder="Search roles, skills or tools..." aria-label="Search roles"><div class="chips">{chips}</div></div>
<p style="color:var(--muted)">Showing <strong id="count">{len(JOBS)}</strong> roles</p>
<div class="grid" id="jobs">{cards}</div>
<p class="empty" id="empty">No roles match your search. Try another keyword or send an open application.</p>
{ad_native()}</div></section>
<section class="section alt"><div class="container"><div class="center"><span class="eyebrow">Why work with us</span><h2>A better way to work remotely</h2></div>
<div class="grid" style="margin-top:32px">{perks_html}</div>{ad_banner()}</div></section>
<section class="section"><div class="container"><div class="center"><span class="eyebrow">Hiring process</span><h2>Four simple steps</h2></div>
<div class="grid" style="margin-top:32px">{steps}</div>{sponsor()}</div></section>
<section class="section"><div class="container"><div class="band"><h2>Don't see your exact role?</h2><p>Send us an open application with your portfolio. We keep strong profiles on file for upcoming projects.</p>
<a class="btn btn-p" href="apply.html?role=general">Send open application</a></div></div></section>
<div class="container">{ad_banner()}</div>
'''
    page("careers.html", "Careers - Remote Jobs",
         "Join DigiLab's remote talent network. %d roles in marketing, advertising, web design, AI, video editing, data and operations. Work from anywhere, paid in USD." % len(JOBS), body, "careers")


def build_job(j):
    r = "../"
    lst = lambda items: "<ul>%s</ul>" % "".join("<li>%s</li>" % e(i) for i in items)
    tools = "".join('<span class="tag">%s</span>' % e(t) for t in j["tools"])
    steps = "".join(f'<li><strong>{e(t)}.</strong> {e(d)}</li>' for t, d in HIRING_STEPS)
    same = [x for x in JOBS if x["dept"] == j["dept"] and x["slug"] != j["slug"]]
    pool = same + [x for x in JOBS if x["dept"] != j["dept"] and x["slug"] != j["slug"]]
    rel = "".join(job_card(x, r) for x in pool[:3])
    about = (f"DigiLab is a remote-first digital agency serving clients in marketing, advertising, web design, AI, video and data. "
             f"As a {j['title']}, you will work with a distributed team of specialists, a named project lead and documented processes, "
             f"so you can focus on doing excellent work instead of chasing context.")
    facts = [("Department", j["dept"]), ("Employment type", j["type"]), ("Location", "Remote (worldwide)"),
             ("Indicative pay", j["pay"]), ("Experience", j["exp"]), ("Language", "English"), ("Applications", "Rolling")]
    facts_html = "".join("<li><span>%s</span><span>%s</span></li>" % (e(a), e(b)) for a, b in facts)
    apply_url = "%sapply.html?role=%s" % (r, j["slug"])
    body = f'''
<section class="hero sm"><div class="container">{crumbs(r, [("Careers", "careers.html"), (j["title"], None)])}
<h1>{e(j["title"])}</h1>
<div class="meta" style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 16px"><span class="tag">{e(j["dept"])}</span><span class="tag g">{e(j["type"])}</span><span class="tag">Remote</span><span class="tag">{e(j["pay"])}</span></div>
<p class="lead">{e(j["summary"])}</p>
<div class="hero-cta" style="margin-top:22px"><a class="btn btn-p" href="{apply_url}">Apply for this role</a><a class="btn btn-o" href="{r}careers.html">All roles</a></div></div></section>
<div class="container">{ad_banner()}</div>
<section class="section" style="padding-top:36px"><div class="container job-layout">
<article class="jd">
<h2>About the role</h2><p>{e(about)}</p><p>{e(j["summary"])}</p>
<h2>What you will do</h2>{lst(j["resp"])}
<h2>What we are looking for</h2>{lst(j["req"])}
<h2>Nice to have</h2>{lst(j["nice"])}
<h2>Tools you will use</h2><div class="stack">{tools}</div>
{ad_native()}
<h2>What we offer</h2>{lst(COMMON_BENEFITS)}
<p style="color:var(--muted);font-size:.93rem">Pay shown is an indicative USD range. The final rate depends on your skills, trial-task results and project scope.</p>
<h2>Hiring process</h2><ol class="steps">{steps}</ol>
<div class="card" style="margin-top:28px"><h3>Ready to apply?</h3><p>It takes about five minutes. Share your portfolio and tell us why you are a great fit.</p>
<a class="btn btn-p" href="{apply_url}">Apply for this role</a></div>
</article>
<aside class="side">
<div class="card"><h3>Role summary</h3><ul class="facts">{facts_html}</ul>
<a class="btn btn-p btn-block" href="{apply_url}">Apply now</a></div>
{ad_banner()}
{sponsor()}
</aside></div></section>
<section class="section alt"><div class="container"><h2>Similar roles</h2><div class="grid g3">{rel}</div>{ad_banner()}</div></section>
'''
    page("jobs/%s.html" % j["slug"], "%s - Remote %s" % (j["title"], j["type"]),
         "%s at DigiLab. Remote, %s, %s. %s" % (j["title"], j["type"].lower(), j["pay"], j["summary"]), body, "careers")


def form_fields_hidden(kind):
    return ('<div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
            '<input type="hidden" name="form_type" value="%s">' % kind)


def before_submit():
    """Tips card + clearly labelled sponsored box, shown just above the Submit button."""
    return f'''<div class="pre"><h3>Before you submit: make your application stand out</h3>
<p>A complete application is quicker for us to review. These small details help the most:</p>
<ul class="checks"><li>Link your best work: portfolio, GitHub, Behance or LinkedIn</li>
<li>Add a CV link that opens without a login (Google Drive or Dropbox, set to "anyone with the link")</li>
<li>Mention two or three relevant projects or results in your message</li>
<li>Double-check your email address so we can reach you</li></ul></div>
<aside class="sponsor"><small>Sponsored &middot; Optional</small>
<h3 style="margin:0 0 6px;font-size:1.05rem">Tools and offers for remote professionals</h3>
<p>Our advertising partners share deals on tools and services popular with remote freelancers. Opening this link is optional and has no effect on how we review your application.</p>
<a class="btn btn-o btn-sm" href="{e(SMARTLINK)}" target="_blank" rel="sponsored nofollow noopener">Explore partner offers</a></aside>'''


def build_apply():
    r = ""
    groups = ""
    for d in DEPTS:
        opts = "".join('<option value="%s">%s</option>' % (j["slug"], e(j["title"])) for j in JOBS if j["dept"] == d)
        groups += '<optgroup label="%s">%s</optgroup>' % (e(d), opts)
    body = f'''
{hero("Apply to join DigiLab", "Tell us about yourself and your work. We review every application and reply by email when your profile matches a project.", crumbs(r, [("Careers", "careers.html"), ("Apply", None)]))}
<div class="container">{ad_banner()}</div>
<section class="section" style="padding-top:28px"><div class="container" style="max-width:820px">
<div class="card"><form class="form" data-form data-subject="New job application - DigiLab" data-ok="Thank you! Your application was received. We will email you if your profile matches a current or upcoming project.">
{form_fields_hidden("application")}
<label>Role you are applying for<select id="role" name="role" required><option value="general">General / open application</option>{groups}</select></label>
<div class="row2"><label>Full name<input name="full_name" required autocomplete="name"></label>
<label>Email address<input type="email" name="email" required autocomplete="email"></label></div>
<div class="row2"><label>Country<input name="country" required autocomplete="country-name"></label>
<label>Expected rate (USD)<input name="expected_rate_usd" placeholder="e.g. $12 / hour" required></label></div>
<div class="row2"><label>Portfolio / LinkedIn / GitHub link<input type="url" name="portfolio_link" placeholder="https://" required></label>
<label>Resume / CV link (Drive, Dropbox)<input type="url" name="cv_link" placeholder="https://"></label></div>
<label>Weekly availability<select name="availability"><option>10-20 hours</option><option>20-30 hours</option><option>30-40 hours</option><option>Full-time</option></select></label>
<label>Why are you a great fit?<textarea name="message" required placeholder="Briefly describe your experience, strongest projects and tools you use."></textarea></label>
<label class="ck"><input type="checkbox" name="consent" required><span>I agree that DigiLab may store my details to evaluate my application. See the <a href="privacy.html">privacy policy</a>.</span></label>
{before_submit()}
<button class="btn btn-p" type="submit">Submit application</button>
<div class="msg" role="status" aria-live="polite"></div></form></div></div></section>
<div class="container">{ad_native()}{sponsor()}{ad_banner()}</div>
'''
    page("apply.html", "Apply", "Apply for a remote role at DigiLab. Share your portfolio and expected rate in USD.", body, "careers")


def build_contact():
    r = ""
    opts = "".join("<option>%s</option>" % e(s["name"]) for s in SERVICES)
    body = f'''
{hero("Let's talk about your project", "Tell us what you need. We reply within one business day with next steps and a clear quote in US dollars.", crumbs(r, [("Contact", None)]))}
<div class="container">{ad_banner()}</div>
<section class="section" style="padding-top:28px"><div class="container split" style="align-items:start">
<div class="card"><form class="form" data-form data-subject="New project enquiry - DigiLab" data-ok="Thank you! We received your enquiry and will reply by email within one business day.">
{form_fields_hidden("contact")}
<div class="row2"><label>Your name<input name="name" required autocomplete="name"></label>
<label>Email address<input type="email" name="email" required autocomplete="email"></label></div>
<div class="row2"><label>Service needed<select name="service">{opts}<option>Not sure yet</option></select></label>
<label>Budget (USD)<select name="budget"><option>Under $500</option><option>$500 - $1,500</option><option>$1,500 - $5,000</option><option>$5,000+</option><option>Not sure yet</option></select></label></div>
<label>Project details<textarea name="message" required placeholder="What are you trying to achieve? Include links, deadlines or examples."></textarea></label>
<label class="ck"><input type="checkbox" name="consent" required><span>I agree to be contacted about my enquiry. See the <a href="privacy.html">privacy policy</a>.</span></label>
<button class="btn btn-p" type="submit">Send enquiry</button>
<div class="msg" role="status" aria-live="polite"></div></form></div>
<div><h2>What happens next</h2>
<ol class="steps"><li><strong>We review.</strong> A project lead reads your brief and prepares questions.</li>
<li><strong>Discovery call.</strong> A free 30-minute video call to align on goals.</li>
<li><strong>Written quote.</strong> A fixed or monthly price in USD with clear deliverables.</li>
<li><strong>Kick-off.</strong> Approve, and your specialist team starts.</li></ol>
{ad_banner()}{sponsor()}</div></div></section>
<div class="container">{ad_native()}{ad_banner()}</div>
'''
    page("contact.html", "Contact", "Contact DigiLab for a free quote. Marketing, web design, AI, video and data services with transparent USD pricing.", body, "contact")


def build_about():
    r = ""
    vals = [("shield", "Honest by default", "We tell you what will and will not work, and we never promise guaranteed rankings or results."),
            ("clock", "Clarity over noise", "Plain-English updates, shared boards and written scopes keep everyone aligned."),
            ("users", "Talent first", "We hire carefully, pay in USD and give specialists the briefs and tools they need to do great work."),
            ("zap", "Speed with quality", "Documented playbooks and templates let us deliver fast without cutting corners.")]
    vals_html = "".join(f'<div class="card">{icon(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in vals)
    body = f'''
{hero("A remote-first digital agency", "DigiLab connects businesses with skilled specialists around the world, so you get agency-level results without agency-level overhead.", crumbs(r, [("About", None)]))}
<div class="container">{ad_banner()}</div>
<section class="section"><div class="container split" style="align-items:start">
<div><h2>Our story</h2><p>Most small and mid-sized businesses need marketing, design, video, data and tech support, but cannot justify a full in-house team for each. Traditional agencies are expensive and slow, while freelance marketplaces leave you to manage everything alone.</p>
<p>DigiLab sits in the middle. We assemble a small team of specialists for your exact needs, put a project lead in charge, and keep everything transparent: scope, price in USD, progress and results.</p>
<p>Because our team works remotely, we can hire the best person for each job wherever they live, and pass the savings on in our pricing.</p></div>
<div class="card"><h3>How our remote model works</h3>{checks(["Named project lead on every engagement", "Specialists matched to your needs", "Shared task board and weekly updates", "Secure access with least privilege", "NDA available on request", "Written scope and USD quote before work starts"])}</div></div></section>
<section class="section alt"><div class="container"><div class="center"><span class="eyebrow">Our values</span><h2>What we stand for</h2></div>
<div class="grid" style="margin-top:32px">{vals_html}</div>{ad_native()}</div></section>
<section class="section"><div class="container"><div class="split"><div><h2>Want to work with us?</h2><p class="lead">We are growing our remote talent network across marketing, design, AI, video, data and operations.</p>
<a class="btn btn-p" href="careers.html">View careers</a></div>{sponsor()}</div>{ad_banner()}</div></section>
{cta_band(r=r)}
<div class="container">{ad_banner()}</div>
'''
    page("about.html", "About Us", "Learn about DigiLab, a remote-first digital agency delivering marketing, web, AI, video and data services through a global team.", body, "about")


def build_legal():
    r = ""
    today = datetime.date.today().strftime("%B %d, %Y")
    privacy = f'''
<section class="hero sm"><div class="container">{crumbs(r, [("Privacy Policy", None)])}<h1>Privacy Policy</h1><p class="lead">Last updated: {today}</p></div></section>
<div class="container">{ad_banner()}</div>
<section class="section" style="padding-top:20px"><div class="container prose">
<h2>Who we are</h2><p>DigiLab ("we", "us") operates this website. This policy explains what information we collect, why, and the choices you have.</p>
<h2>Information you give us</h2><p>When you use our contact or application forms, you provide details such as your name, email address, country, portfolio links and message. We use this information only to answer your enquiry or evaluate your application. Form submissions are delivered to us by email through a third-party form-handling service and are also recorded in a private spreadsheet (Google Sheets) that only the DigiLab team can access.</p>
<h2>Advertising and cookies</h2><p>This website displays advertising supplied by third-party advertising networks, including Adsterra. These networks may use cookies, device identifiers and similar technologies to show and measure ads and to limit how often you see them. Their handling of data is described in their own privacy policies. You can control cookies through your browser settings or use browser privacy tools to limit tracking.</p>
<h2>Analytics and logs</h2><p>Our hosting provider may record standard technical logs such as IP address, browser type and pages requested for security and performance purposes.</p>
<h2>How long we keep data</h2><p>We keep enquiries and applications only as long as needed to respond or to consider you for current and upcoming projects. You can ask us to delete your data at any time.</p>
<h2>Your rights</h2><p>You may request access to, correction of, or deletion of the personal data we hold about you. Contact us through the contact page and we will respond within a reasonable time.</p>
<h2>Children</h2><p>This website is not directed to children under 16 and we do not knowingly collect their personal data.</p>
<h2>Changes</h2><p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>
<h2>Contact</h2><p>Questions about this policy? Please use the <a href="contact.html">contact page</a>.</p>
{ad_native()}{sponsor()}
</div></section>
<div class="container">{ad_banner()}</div>
'''
    terms = f'''
<section class="hero sm"><div class="container">{crumbs(r, [("Terms of Use", None)])}<h1>Terms of Use</h1><p class="lead">Last updated: {today}</p></div></section>
<div class="container">{ad_banner()}</div>
<section class="section" style="padding-top:20px"><div class="container prose">
<h2>Using this website</h2><p>By using this website you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Services and quotes</h2><p>Information about services and prices on this website is for general guidance. All prices are shown in US dollars (USD) and are starting prices. A project begins only after you approve a written quote or agreement.</p>
<h2>Careers and applications</h2><p>Role listings describe the types of remote specialists DigiLab works with. Submitting an application does not guarantee an interview, a trial task or an engagement. Pay ranges are indicative and may change based on skills, project scope and trial results. Work is generally engaged on a contract basis unless stated otherwise in a written agreement.</p>
<h2>Third-party advertising and links</h2><p>This website displays third-party advertisements and sponsored links. We do not control and are not responsible for the content, products or services of advertisers or other external websites. Any dealings you have with advertisers are between you and them.</p>
<h2>Intellectual property</h2><p>The design, text and graphics on this website belong to DigiLab or its licensors and may not be copied without permission.</p>
<h2>No warranty</h2><p>This website is provided "as is". We work to keep information accurate but do not guarantee it is complete or error-free. To the extent permitted by law, we are not liable for losses arising from use of the website.</p>
<h2>Changes</h2><p>We may update these terms at any time. Continued use of the website means you accept the updated terms.</p>
<h2>Contact</h2><p>Questions? Please use the <a href="contact.html">contact page</a>.</p>
{ad_native()}{sponsor()}
</div></section>
<div class="container">{ad_banner()}</div>
'''
    page("privacy.html", "Privacy Policy", "How DigiLab collects, uses and protects your information, including advertising cookies.", privacy, "")
    page("terms.html", "Terms of Use", "Terms of use for the DigiLab website, services information and careers listings.", terms, "")


def build_404():
    body = f'''
<section class="hero"><div class="container center"><span class="eyebrow">Error 404</span><h1>Page not found</h1>
<p class="lead">The page you are looking for does not exist or was moved.</p>
<div class="hero-cta" style="justify-content:center"><a class="btn btn-p" href="index.html">Back to home</a><a class="btn btn-o" href="services.html">Our services</a></div></div></section>
<div class="container">{ad_banner()}{ad_native()}{sponsor()}{ad_banner()}</div>
'''
    page("404.html", "Page not found", "Page not found.", body, "", noindex=True)


def build_extras():
    write(".nojekyll", "")
    if SITE_URL:
        base = SITE_URL.rstrip("/")
        urls = "".join("<url><loc>%s/%s</loc></url>\n" % (base, p) for p in PAGES)
        write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
        write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % base)
    else:
        write("robots.txt", "User-agent: *\nAllow: /\n")


def main():
    build_home()
    build_services()
    for s in SERVICES:
        build_service(s)
    build_careers()
    for j in JOBS:
        build_job(j)
    build_apply()
    build_contact()
    build_about()
    build_legal()
    build_404()
    build_extras()
    print("Built %d pages (%d services, %d jobs)." % (len(PAGES) + 1, len(SERVICES), len(JOBS)))


if __name__ == "__main__":
    main()
