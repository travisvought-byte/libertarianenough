"""Shared page shell and helpers for the Libertarian Enough site."""
import html, os, json, re
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://libertarianenough.org"
NAME = "Libertarian Enough"
CHECKED = "November 26, 2026"
REPO = "https://github.com/travisvought-byte/libertarianenough"
CONTACT = "veteranhomeguardians@gmail.com"
# Google AdSense publisher ID. ads.txt is written from it, and Google's ad code goes on every content page.
ADSENSE = "ca-pub-9220804879239310"
# Pages that never load ad code: the 404, the about/privacy page, and the results page (its address carries the quiz answers).
NO_ADS = {"404.html", "about.html", "results.html"}
# IndexNow key. build.py publishes it as <key>.txt at the site root; .github/workflows/indexnow.yml sends changed pages with it.
INDEXNOW_KEY = "4a4ba9c20a8845af6ac3b35fa8b53183"


def mailto(subject):
    from urllib.parse import quote
    return f'<a href="mailto:{CONTACT}?subject={quote(subject)}">{CONTACT}</a>'

NAV = [("quiz.html", "Quiz"), ("learn/index.html", "Learn"), ("plan/index.html", "Plan"), ("causes/index.html", "Causes"),
       ("organize/index.html", "Organize"), ("fundraise/index.html", "Fundraise"), ("states/index.html", "States"),
       ("website-help.html", "Website help")]

PAGES = []  # (path) for sitemap

e = html.escape


def data(name):
    with open(os.path.join(ROOT, "data", name + ".json")) as f:
        return json.load(f)


def ic(name, cls="ico", size=44):
    return (f'<svg class="{cls}" viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
            f'<use href="{{P}}assets/icons.svg#{name}"/></svg>')


def ext(url, text):
    return f'<a href="{e(url)}" rel="noopener" target="_blank">{text}<span class="sr"> (opens in a new tab)</span></a>'


NICE = {"en.wikipedia.org": "Wikipedia", "wikipedia.org": "Wikipedia", "reason.com": "Reason", "lp.org": "Libertarian Party",
        "ballotpedia.org": "Ballotpedia", "ballot-access.org": "Ballot Access News", "pewresearch.org": "Pew Research Center",
        "cato.org": "Cato Institute", "ij.org": "Institute for Justice", "npr.org": "NPR", "apnews.com": "AP", "pbs.org": "PBS",
        "nytimes.com": "New York Times", "fec.gov": "FEC", "britannica.com": "Britannica", "libertarianism.org": "Libertarianism.org",
        "mises.org": "Mises Institute", "thenation.com": "The Nation", "bostonglobe.com": "Boston Globe", "nhpr.org": "NHPR",
        "patch.com": "Patch", "virginiamercury.com": "Virginia Mercury", "wdbj7.com": "WDBJ7", "prri.org": "PRRI",
        "news.gallup.com": "Gallup", "gallup.com": "Gallup", "yougov.com": "YouGov", "today.yougov.com": "YouGov",
        "codes.findlaw.com": "FindLaw (Ohio Revised Code)", "law.cornell.edu": "Cornell LII", "ecfr.gov": "eCFR", "ncsl.org": "NCSL",
        "gao.gov": "GAO", "congress.gov": "Congress.gov", "dea.gov": "DEA", "fda.gov": "FDA", "eff.org": "EFF",
        "prisonpolicy.org": "Prison Policy Initiative", "norml.org": "NORML", "mpp.org": "Marijuana Policy Project",
        "supremecourt.gov": "Supreme Court", "thirdpartywatch.com": "Third Party Watch", "axios.com": "Axios",
        "calmatters.org": "CalMatters", "isps.yale.edu": "Yale ISPS", "opensecrets.org": "OpenSecrets",
        "wikiwand.com": "Wikiwand", "cbsnews.com": "CBS News", "sos.wyo.gov": "Wyoming Secretary of State",
        "csgjusticecenter.org": "CSG Justice Center", "rollcall.com": "Roll Call", "sunset.texas.gov": "Texas Sunset Advisory Commission",
        "cleanslateinitiative.org": "Clean Slate Initiative", "fee.org": "Foundation for Economic Education", "econlib.org": "Econlib",
        "homebrewersassociation.org": "American Homebrewers Association", "wyoleg.gov": "Wyoming Legislature",
        "capitol.texas.gov": "Texas Legislature", "americanheritage.com": "American Heritage", "knau.org": "KNAU",
        "9news.com": "9News", "airandspace.si.edu": "Smithsonian Air and Space Museum", "sandyspringsga.gov": "City of Sandy Springs",
        "nvfc.org": "National Volunteer Fire Council", "fsp.org": "Free State Project", "theanarchistlibrary.org": "The Anarchist Library",
        "docs.legis.wisconsin.gov": "Wisconsin Legislative Council", "foxnews.com": "Fox News", "cdc.gov": "CDC", "w3.org": "W3C", "webaim.org": "WebAIM"}


def srcname(url):
    try:
        h = urlparse(url).netloc.lower()
    except Exception:
        return "Source"
    if h.startswith("www."):
        h = h[4:]
    if h in NICE:
        return NICE[h]
    for k, v in NICE.items():
        if h.endswith("." + k):
            return v
    return h


def clean_url(u):
    return re.sub(r"/markdown$", "", u)


def sources(urls, label="Sources"):
    urls = [clean_url(u) for u in (urls if isinstance(urls, list) else [urls]) if u]
    if not urls:
        return ""
    seen, parts = set(), []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        parts.append(ext(u, e(srcname(u))))
    lab = label if len(parts) > 1 else label.rstrip("s")
    return f'<span class="src">{lab}: ' + ", ".join(parts) + '</span>'


GC = ('<script>window.goatcounter={path:function(){return "/libertarianenough.org"+location.pathname},'
      'referrer:function(){try{var u=new URL(document.referrer);return u.origin+u.pathname}catch(e){return ""}}};</script>'
      '<script data-goatcounter="https://vhg-guide.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>')

ADS = (f'<meta name="google-adsense-account" content="{ADSENSE}">'
       '<script>(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1;</script>'
       f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>')


def content_key(text):
    """A fingerprint of what a page says: its title, description and main content, not the shared header, footer or scripts.
    The sitemap's lastmod moves only when this changes."""
    import hashlib
    parts = [re.search(r"<title>(.*?)</title>", text, re.S), re.search(r'<meta name="description" content="([^"]*)"', text),
             re.search(r"<main\b.*?</main>", text, re.S)]
    return hashlib.sha256("\n".join(m.group(0) if m else "" for m in parts).encode("utf-8")).hexdigest()[:16]


LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><use href="{P}assets/icons.svg#porcupine"/></svg>')


def page(path, title, desc, h1, body, lead="", kicker="", crumbs=None, scripts=(), wide=True, head_extra=""):
    depth = path.count("/")
    P = "../" * depth
    url = SITE + "/" + ("" if path == "index.html" else path)
    section = path.split("/")[0] if "/" in path else path
    navh = []
    for h, t in NAV:
        cur = (h == path) or ("/" in h and h.split("/")[0] == section)
        navh.append(f'<a href="{P}{h}"' + (' aria-current="page"' if cur else '') + f'>{t}</a>')
    full_title = title if title.endswith(NAME) or path == "index.html" else f"{title} | {NAME}"
    crumbs_html = ""
    ld = ""
    if crumbs:
        items = [(NAME, "index.html")] + crumbs
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
            (f'<a href="{P}{h}">{e(n)}</a>' if h else f'<span aria-current="page">{e(n)}</span>') for n, h in items) + '</nav>'
        ldo = {"@context": "https://schema.org", "@type": "BreadcrumbList",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                    "item": SITE + "/" + (h if h and h != "index.html" else ("" if h == "index.html" else path))}
                                   for i, (n, h) in enumerate(items)]}
        ld = f'<script type="application/ld+json">{json.dumps(ldo)}</script>'
    scr = "".join(f'<script src="{P}{s}"></script>' for s in scripts)
    head_lead = f'<p class="lead">{lead}</p>' if lead else ""
    kick = f'<p class="kicker">{kicker}</p>' if kicker else ""
    h1html = f"<h1>{h1}</h1>" if h1 else ""
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#1f2a44">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{P}assets/site.css">{head_extra}{ld}{"" if path in NO_ADS else ADS}{GC}
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="in"><a class="brand" href="{P}index.html">{LOGO}<span>{NAME}</span></a>
<nav class="main" aria-label="Main">{"".join(navh)}</nav></div></header>
<main id="main"{' class="narrow"' if not wide else ''}>{crumbs_html}{kick}{h1html}{head_lead}
{body}
</main>
<footer class="site"><div class="in"><div class="cols">
<div><p><b>{NAME}</b> is an independent libertarian organizing project. It is not a political party and is not affiliated with the Libertarian National Committee or any state party.</p>
<p>Made in Ohio by <a href="https://travisvought.com/">Travis Vought</a>, author of <a href="{P}book.html">The Asymmetric Libertarian</a>. Every jab here is aimed from inside the tent.</p></div>
<div><p><b>The site</b></p><ul><li><a href="{P}quiz.html">Take the quiz</a></li><li><a href="{P}plan/index.html">The plan</a></li><li><a href="{P}spectrum.html">The spectrum</a></li><li><a href="{P}traps.html">Purity traps</a></li><li><a href="{P}types/index.html">All 15 types</a></li><li><a href="{P}book.html">The book</a></li></ul></div>
<div><p><b>About</b></p><ul><li><a href="{P}about.html">About, scoring and privacy</a></li><li><a href="{P}about.html#sources">Sources and data</a></li><li><a href="{P}website-help.html">Website help</a></li><li>{ext(REPO, "Code on GitHub")}</li></ul></div>
<div><p><b>Related</b></p><ul><li><a href="https://the-reefer.com/">The Reefer</a>: cannabis law in every state</li><li><a href="https://abuseofoffice.org/">Abuse of Office</a>: public officials who broke the public's trust</li></ul></div>
</div><p>Facts checked {CHECKED}. Quiz answers never leave your browser.</p></div></footer>
{scr}
</body></html>
"""
    out = out.replace("{P}", P)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(out)
    if path != "404.html":
        PAGES.append(path)


# The Nolan chart, drawn as a diamond. Economic freedom (E) and personal freedom (P) run 0-100.
# The cross: left to right is the left-right split (progressive to conservative), bottom to top is authority to liberty.
CX, CY, S = 430, 296, 240
W, H = 860, 600


def dx(E, P):
    return round(CX + (E - P) / 100 * S, 1)


def dy(E, P):
    return round(CY - (E + P - 100) / 100 * S, 1)


def _pt(E, P):
    return f"{dx(E, P)},{dy(E, P)}"


def _poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(_pt(a, b) for a, b in pts)}" fill="{fill}"{extra}/>'


def halo(x, y, txt, size=14, weight=700, anchor="start", fill="#1a1a1a", extra=""):
    """Text with a cream outline drawn as a separate copy, so labels stay readable over lines and fills."""
    a = f'x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{extra}'
    return (f'<text {a} fill="#fffdf5" stroke="#fffdf5" stroke-width="5" stroke-linejoin="round" aria-hidden="true">{txt}</text>'
            f'<text {a} fill="{fill}">{txt}</text>')


def chart_svg(refs, title="The libertarian spectrum", desc_extra="", names=False, pick=None, uid="c"):
    """Nolan chart drawn as a diamond with a real cross through it. names=True writes names beside the dots (home page);
    otherwise the dots are numbered and the table below names them. pick limits which refs show (indexes into refs)."""
    q = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fffdf5"/>']
    # Four regions, split where E=50 and P=50, plus the centrist middle where both are within 10 of 50.
    q.append(_poly([(50, 50), (100, 50), (100, 100), (50, 100)], "#fff1b8"))   # libertarian, top
    q.append(_poly([(0, 50), (50, 50), (50, 100), (0, 100)], "#e3e8f4"))       # progressive, left
    q.append(_poly([(50, 0), (100, 0), (100, 50), (50, 50)], "#efe6cc"))       # conservative, right
    q.append(_poly([(0, 0), (50, 0), (50, 50), (0, 50)], "#f4dede"))           # statist, bottom
    q.append(_poly([(40, 40), (60, 40), (60, 60), (40, 60)], "#ffffff", ' stroke="#1a1a1a" stroke-width="1.2"'))
    q.append(_poly([(0, 0), (100, 0), (100, 100), (0, 100)], "none", ' stroke="#1a1a1a" stroke-width="2.5"'))
    q.append(f'<path d="M{_pt(50, 0)}L{_pt(50, 100)}M{_pt(0, 50)}L{_pt(100, 50)}" stroke="#1a1a1a" stroke-width="1" stroke-dasharray="5 5" opacity=".55"/>')
    # The cross: left-right across, authority-liberty up and down.
    q.append(f'<defs><marker id="{uid}ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f2a44"/></marker></defs>')
    q.append(f'<path d="M{CX - S + 6} {CY}H{CX + S - 6}M{CX} {CY + S - 6}V{CY - S + 6}" stroke="#1f2a44" stroke-width="2.5" marker-start="url(#{uid}ah)" marker-end="url(#{uid}ah)"/>')
    q.append(halo(CX - 34, CY - 8, "CENTRIST", 13, 800, "end", "#333"))
    # Region names sit outside each tip of the diamond, with the direction of the cross under them.
    q.append(f'<text x="{CX}" y="22" font-size="20" font-weight="800" text-anchor="middle" fill="#1a1a1a" letter-spacing="1">LIBERTARIAN</text>'
             f'<text x="{CX}" y="42" font-size="15" font-weight="700" text-anchor="middle" fill="#1f2a44">↑ more liberty</text>')
    q.append(f'<text x="{CX}" y="{CY + S + 28}" font-size="20" font-weight="800" text-anchor="middle" fill="#1a1a1a" letter-spacing="1">STATIST</text>'
             f'<text x="{CX}" y="{CY + S + 48}" font-size="15" font-weight="700" text-anchor="middle" fill="#1f2a44">↓ more authority</text>')
    q.append(f'<text x="{CX - S - 12}" y="{CY - 6}" font-size="20" font-weight="800" text-anchor="end" fill="#1a1a1a" letter-spacing="1">PROGRESSIVE</text>'
             f'<text x="{CX - S - 12}" y="{CY + 16}" font-size="15" font-weight="700" text-anchor="end" fill="#1f2a44">← left</text>')
    q.append(f'<text x="{CX + S + 12}" y="{CY - 6}" font-size="20" font-weight="800" text-anchor="start" fill="#1a1a1a" letter-spacing="1">CONSERVATIVE</text>'
             f'<text x="{CX + S + 12}" y="{CY + 16}" font-size="15" font-weight="700" text-anchor="start" fill="#1f2a44">right →</text>')
    # Edge labels: the two freedoms the diamond is built from.
    q.append(f'<text font-size="16" font-weight="700" fill="#333" text-anchor="middle" transform="translate({(dx(100, 0) + dx(0, 0)) / 2 + 20} {(dy(100, 0) + dy(0, 0)) / 2 + 20}) rotate(-45)">Economic freedom →</text>')
    q.append(f'<text font-size="16" font-weight="700" fill="#333" text-anchor="middle" transform="translate({(dx(0, 100) + dx(0, 0)) / 2 - 20} {(dy(0, 100) + dy(0, 0)) / 2 + 20}) rotate(45)">← Personal freedom</text>')
    idx = list(range(len(refs))) if pick is None else pick
    for i in idx:
        r = refs[i]
        x, y = dx(r["e"], r["p"]), dy(r["e"], r["p"])
        tip = f'<title>{e(r["n"])}: economic freedom {r["e"]}, personal freedom {r["p"]}</title>'
        if names:
            side = r.get("side") or ("end" if x > CX else "start")
            q.append(f'<g>{tip}<circle cx="{x}" cy="{y}" r="8" fill="#1f2a44" stroke="#fffdf5" stroke-width="2"/>'
                     + halo(x + (-13 if side == "end" else 13), y + 6, e(r["n"]), 17, 700, side) + '</g>')
        else:
            q.append(f'<g>{tip}<circle cx="{x}" cy="{y}" r="13" fill="#1f2a44" stroke="#fffdf5" stroke-width="2"/>'
                     f'<text x="{x}" y="{y + 5}" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">{i + 1}</text></g>')
    desc = ("A diamond-shaped Nolan chart with a cross through the middle. Left to right runs from progressive on the left to conservative on the right. "
            "Bottom to top runs from authority, where the statists sit, to liberty, where the libertarians sit. "
            "The lower-right edge measures economic freedom and the lower-left edge personal freedom. A small square in the middle is centrist. "
            + ("Dots mark famous people and archetypes, named beside them." if names else "Numbered dots mark famous people and archetypes, listed in the table below.") + desc_extra)
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{uid}t {uid}d"><title id="{uid}t">{e(title)}</title><desc id="{uid}d">{e(desc)}</desc>'
            + "".join(q) + '</svg>')


def ref_table(refs, you_row=False):
    rows = "".join(f'<tr><th scope="row">{i+1}. {e(r["n"])}</th><td>{r["e"]}</td><td>{r["p"]}</td><td>{e(r["note"])}</td></tr>' for i, r in enumerate(refs))
    you = '<tbody id="you-row"></tbody>' if you_row else ""
    return ('<div class="tablewrap"><table><caption>Who is on the chart (cheeky estimates, not measurements)</caption>'
            '<thead><tr><th scope="col">Who</th><th scope="col">Economic freedom</th><th scope="col">Personal freedom</th><th scope="col">Why there</th></tr></thead>'
            f'{you}<tbody>{rows}</tbody></table></div>')


# Embeds run inside other people's sites, so they carry no header, menu or footer, and they ask search engines not to index them.
EMBED_HEIGHT = ('<script>(function(){if(window.parent===window)return;function s(){window.parent.postMessage({le:"height",h:Math.ceil(document.body.getBoundingClientRect().height)},"*")}'
                'window.addEventListener("load",s);window.addEventListener("resize",s);if(window.ResizeObserver)new ResizeObserver(s).observe(document.body);s();})();</script>')


def embed_page(path, title, canonical, body, scripts=()):
    depth = path.count("/")
    P = "../" * depth
    scr = "".join(f'<script src="{P}{s}"></script>' for s in scripts)
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {NAME}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/{canonical}">
<link rel="stylesheet" href="{P}assets/site.css">{GC}
</head><body class="embed">
<main id="main">
{body}
</main>
<footer class="embedfoot"><p>From {ext(SITE + "/", NAME)}</p></footer>
{scr}{EMBED_HEIGHT}
</body></html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(out)


def moved(path, to, title):
    """A page that moved. GitHub Pages can't send real redirects, so this one sends people on at once."""
    out = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {NAME}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}/{to}">
<meta http-equiv="refresh" content="0; url={to}">
<link rel="stylesheet" href="assets/site.css">
</head><body><main id="main" class="narrow"><h1>{e(title)}</h1><p>This page moved to <a href="{to}">{e(title)}</a>.</p></main></body></html>
"""
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(out)
