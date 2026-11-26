"""Shared page shell and helpers for the Libertarian Enough site."""
import html, os, json, re
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://libertarianenough.org"
NAME = "Libertarian Enough"
CHECKED = "November 26, 2026"
REPO = "https://github.com/travisvought-byte/libertarianenough"
CONTACT = "veteranhomeguardians@gmail.com"


def mailto(subject):
    from urllib.parse import quote
    return f'<a href="mailto:{CONTACT}?subject={quote(subject)}">{CONTACT}</a>'

NAV = [("quiz.html", "Quiz"), ("learn/index.html", "Learn"), ("plan/index.html", "Plan"), ("causes/index.html", "Causes"),
       ("organize/index.html", "Organize"), ("fundraise/index.html", "Fundraise"), ("states/index.html", "States"),
       ("free-sites.html", "Free sites")]

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
        "docs.legis.wisconsin.gov": "Wisconsin Legislative Council", "foxnews.com": "Fox News"}


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
<link rel="stylesheet" href="{P}assets/site.css">{head_extra}{ld}{GC}
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="in"><a class="brand" href="{P}index.html">{LOGO}<span>{NAME}</span></a>
<nav class="main" aria-label="Main">{"".join(navh)}</nav></div></header>
<main id="main"{' class="narrow"' if not wide else ''}>{crumbs_html}{kick}{h1html}{head_lead}
{body}
</main>
<footer class="site"><div class="in"><div class="cols">
<div><p><b>{NAME}</b> is an independent libertarian organizing project. It is not a political party and is not affiliated with the Libertarian National Committee or any state party.</p>
<p>Made in Ohio by Travis Vought, author of <a href="{P}book.html">The Asymmetric Libertarian</a>. Every jab here is aimed from inside the tent.</p></div>
<div><p><b>The site</b></p><ul><li><a href="{P}quiz.html">Take the quiz</a></li><li><a href="{P}plan/index.html">The plan</a></li><li><a href="{P}spectrum.html">The spectrum</a></li><li><a href="{P}traps.html">Purity traps</a></li><li><a href="{P}types/index.html">All 15 types</a></li><li><a href="{P}book.html">The book</a></li></ul></div>
<div><p><b>About</b></p><ul><li><a href="{P}about.html">About, scoring and privacy</a></li><li><a href="{P}about.html#sources">Sources and data</a></li><li><a href="{P}free-sites.html">Free websites</a></li><li>{ext(REPO, "Code on GitHub")}</li></ul></div>
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


def px(v):
    return 60 + v * 5


def py(v):
    return 520 - v * 5


def chart_svg(refs, title="The libertarian spectrum", desc_extra=""):
    """Static chart of reference figures. Results page adds the reader's star with JavaScript."""
    q = []
    q.append('<rect x="310" y="20" width="250" height="250" fill="#fff7d1"/>')
    q.append('<rect x="60" y="20" width="250" height="250" fill="#eef1f8"/>')
    q.append('<rect x="310" y="270" width="250" height="250" fill="#f3eedc"/>')
    q.append('<rect x="60" y="270" width="250" height="250" fill="#f6e8e8"/>')
    q.append('<rect x="60" y="20" width="500" height="500" fill="none" stroke="#1a1a1a" stroke-width="2"/>')
    q.append('<path d="M310 20v500M60 270h500" stroke="#1a1a1a" stroke-width="1.5" stroke-dasharray="6 5"/>')
    for x, y, t in [(545, 40, "LIBERTARIAN"), (75, 40, "PROGRESSIVE"), (545, 508, "CONSERVATIVE"), (75, 508, "STATIST")]:
        anchor = "end" if x > 300 else "start"
        q.append(f'<text x="{x}" y="{y}" font-size="15" font-weight="800" fill="#1a1a1a" text-anchor="{anchor}" letter-spacing="1">{t}</text>')
    q.append('<text x="310" y="552" font-size="16" font-weight="700" text-anchor="middle" fill="#1a1a1a">Economic freedom →</text>')
    q.append('<text x="22" y="270" font-size="16" font-weight="700" text-anchor="middle" fill="#1a1a1a" transform="rotate(-90 22 270)">Personal freedom →</text>')
    for v in (0, 50, 100):
        q.append(f'<text x="{px(v)}" y="536" font-size="13" text-anchor="middle" fill="#333">{v}</text>')
        q.append(f'<text x="52" y="{py(v)+4}" font-size="13" text-anchor="end" fill="#333">{v}</text>')
    for i, r in enumerate(refs):
        x, y = px(r["e"]), py(r["p"])
        q.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#1f2a44"/><text x="{x}" y="{y+4.5}" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>')
    desc = ("A square chart. Left to right is economic freedom from 0 to 100. Bottom to top is personal freedom from 0 to 100. "
            "Top right is libertarian, top left progressive, bottom right conservative, bottom left statist. "
            "Numbered dots mark famous people and archetypes, listed in the table below." + desc_extra)
    return (f'<svg viewBox="0 0 600 570" role="img" aria-labelledby="ct cd"><title id="ct">{e(title)}</title><desc id="cd">{e(desc)}</desc>'
            + "".join(q) + '</svg>')


def ref_table(refs, you_row=False):
    rows = "".join(f'<tr><th scope="row">{i+1}. {e(r["n"])}</th><td>{r["e"]}</td><td>{r["p"]}</td><td>{e(r["note"])}</td></tr>' for i, r in enumerate(refs))
    you = '<tbody id="you-row"></tbody>' if you_row else ""
    return ('<div class="tablewrap"><table><caption>Who is on the chart (cheeky estimates, not measurements)</caption>'
            '<thead><tr><th scope="col">Who</th><th scope="col">Economic freedom</th><th scope="col">Personal freedom</th><th scope="col">Why there</th></tr></thead>'
            f'{you}<tbody>{rows}</tbody></table></div>')
