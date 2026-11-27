"""Charts built from sourced numbers: how Americans split, the leaky funnel, and party membership over time.
Every number here is in data/demographics.json or data/history.json with its source."""
from core import e, ext, sources

PRRI = "https://prri.org/press-release/2013-avs-2/"
GALLUP = "https://reason.com/2016/03/08/the-libertarian-moment-is-so-over-that-l/"
PEW = "https://www.pewresearch.org/short-reads/2014/08/25/in-search-of-libertarians"
BAN = "https://ballot-access.org/2024/11/29/november-2024-ballot-access-news-print-edition/"
OLIVER = "https://en.wikipedia.org/wiki/History_of_the_Libertarian_Party_(United_States)"
TPW = "https://thirdpartywatch.com/?p=3569"
REASON17 = "https://reason.com/2017/09/15/the-libertarian-partys-paid-membership-n/"


def prri_chart(uid="prri"):
    """PRRI 2013 Libertarian Orientation Scale. A diverging scale: communalist (slate) to libertarian (gold), gray middle."""
    rows = [("Consistent communalist", 7, "#3b4a6b"), ("Lean communalist", 17, "#8f9bb8"), ("Mixed", 54, "#b9b4a6"),
            ("Lean libertarian", 15, "#e0b400"), ("Consistent libertarian", 7, "#8a6a00")]
    bw, top, rh = 560, 10, 46
    g = []
    for i, (lab, v, c) in enumerate(rows):
        y = top + i * rh
        w = round(v / 60 * bw, 1)
        g.append(f'<text x="210" y="{y + 25}" font-size="15" text-anchor="end" fill="#1a1a1a">{lab}</text>'
                 f'<rect x="222" y="{y + 8}" width="{w}" height="26" rx="4" fill="{c}"><title>{lab}: {v}%</title></rect>'
                 f'<text x="{222 + w + 8}" y="{y + 26}" font-size="16" font-weight="800" fill="#1a1a1a">{v}%</text>')
    svg = (f'<svg viewBox="0 0 820 {top + 5 * rh + 6}" role="img" aria-labelledby="{uid}t {uid}d"><title id="{uid}t">How Americans split on PRRI\'s libertarian scale, 2013</title>'
           f'<desc id="{uid}d">Bar chart. Consistent communalist 7 percent, lean communalist 17 percent, mixed 54 percent, lean libertarian 15 percent, consistent libertarian 7 percent.</desc>'
           + "".join(g) + '</svg>')
    return (f'<figure class="fig"><figcaption><b>Most Americans are mixed.</b> Only 7% are consistent libertarians, but another 15% lean that way. PRRI calls the opposite pole communalist: people who want government and community to take a bigger role.</figcaption>'
            f'<div class="figsvg">{svg}</div><p class="src">PRRI, 2013 American Values Survey, 2,317 adults. {sources([PRRI])}</p></figure>')


def funnel():
    steps = [("27%", "of Americans hold libertarian views", "Gallup's ideology groups, 2015", GALLUP),
             ("11%", "call themselves libertarian and know what it means", "Pew Research Center, 2014", PEW),
             ("0.60%", "of registered voters are registered Libertarian", "Ballot Access News, 2024", BAN),
             ("0.42%", "voted for the Libertarian nominee for president", "2024 election", OLIVER),
             ("9,954", "people pay dues to the national party", "March 2025", TPW)]
    lis = "".join(f'<li><span class="fn">{n}</span><span class="ft">{e(t)}</span><span class="src">{e(w)}. {sources([u])}</span></li>' for n, t, w, u in steps)
    return (f'<figure class="fig"><figcaption><b>The leaky funnel.</b> Tens of millions of Americans lean libertarian. About ten thousand pay dues. '
            f'Everything between those two numbers is an organizing problem.</figcaption><ol class="funnel">{lis}</ol>'
            f'<p class="src">Different surveys and years, so read it as orders of magnitude, not one clean pipeline.</p></figure>')


def members_chart(uid="mem"):
    """National dues-paying members. Points on a true time scale; one series, so no legend."""
    pts = [(2017.0, 18908, "January 2017", REASON17), (2017.67, 14321, "August 2017", REASON17), (2024.67, 11461, "September 2024", TPW),
           (2025.12, 10177, "February 2025", TPW), (2025.21, 9954, "March 2025", TPW)]
    x0, x1, X0, X1 = 2016.8, 2025.5, 70, 790
    y0, y1, Y0, Y1 = 0, 20000, 250, 20

    def X(t):
        return round(X0 + (t - x0) / (x1 - x0) * (X1 - X0), 1)

    def Y(v):
        return round(Y0 - (v - y0) / (y1 - y0) * (Y0 - Y1), 1)
    g = []
    for v in (0, 5000, 10000, 15000, 20000):
        g.append(f'<path d="M{X0} {Y(v)}H{X1}" stroke="#d9d3bf" stroke-width="1"/><text x="{X0 - 8}" y="{Y(v) + 5}" font-size="14" text-anchor="end" fill="#4a4a4a">{v:,}</text>')
    for yr in range(2017, 2026):
        g.append(f'<text x="{X(yr)}" y="{Y0 + 24}" font-size="14" text-anchor="middle" fill="#4a4a4a">{yr}</text>')
    g.append(f'<path d="M{X(2017.67)} {Y(14321)}L{X(2024.67)} {Y(11461)}" stroke="#1f2a44" stroke-width="2" stroke-dasharray="4 5" fill="none"/>')
    g.append(f'<path d="M{X(2017.0)} {Y(18908)}L{X(2017.67)} {Y(14321)}M{X(2024.67)} {Y(11461)}L{X(2025.12)} {Y(10177)}L{X(2025.21)} {Y(9954)}" stroke="#1f2a44" stroke-width="2.5" fill="none"/>')
    for t, v, lab, _ in pts:
        g.append(f'<circle cx="{X(t)}" cy="{Y(v)}" r="6" fill="#1f2a44" stroke="#fffdf5" stroke-width="2"><title>{lab}: {v:,} members</title></circle>')
    g.append(f'<text x="{X(2017.0) + 12}" y="{Y(18908) - 8}" font-size="15" font-weight="800" fill="#1a1a1a">18,908</text>')
    g.append(f'<text x="{X(2025.21) + 6}" y="{Y(9954) + 28}" font-size="15" font-weight="800" fill="#1a1a1a" text-anchor="end">9,954</text>')
    g.append(f'<text x="{(X(2017.67) + X(2024.67)) / 2}" y="{Y(13000) - 12}" font-size="13" fill="#4a4a4a" text-anchor="middle">no counts found for these years</text>')
    svg = (f'<svg viewBox="0 0 820 290" role="img" aria-labelledby="{uid}t {uid}d"><title id="{uid}t">Libertarian Party dues-paying members, 2017 to 2025</title>'
           f'<desc id="{uid}d">Line chart. 18,908 in January 2017, 14,321 in August 2017, 11,461 in September 2024, 10,177 in February 2025 and 9,954 in March 2025. '
           f'The years between 2017 and 2024 have no published counts, so that stretch is dashed.</desc>' + "".join(g) + '</svg>')
    rows = "".join(f'<tr><th scope="row">{lab}</th><td>{v:,}</td></tr>' for _, v, lab, _ in pts)
    return (f'<figure class="fig"><figcaption><b>The party is shrinking.</b> National dues-paying membership fell by about half from its 2017 high.</figcaption>'
            f'<div class="figsvg">{svg}</div>'
            f'<details><summary>See the numbers</summary><div class="tablewrap"><table><thead><tr><th scope="col">When</th><th scope="col">Members</th></tr></thead><tbody>{rows}</tbody></table></div></details>'
            f'<p class="src">{sources([REASON17, TPW])}</p></figure>')


def block():
    return f'<div class="figs">{prri_chart()}{members_chart()}</div>{funnel()}'
