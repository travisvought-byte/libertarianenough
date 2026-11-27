"""The real-life quiz: what you'd actually do, scored, explained and argued with. Pages: life/index.html and life/result.html."""
import copy
from core import page, e, ic, chart_svg, halo
from quizdata import REFS
import lifedata as L

MAIN = len(L.ORDER)


def build():
    play()
    result()


def class_map():
    """Liberty (across) against care (up), split into the five characters. The Fixer is the band down the middle.
    assets/life.js adds a gold star for the player. Must match the class rules in life.js."""
    X0, Y0, SZ = 70, 30, 420
    def X(v): return X0 + v / 100 * SZ
    def Y(v): return Y0 + (100 - v) / 100 * SZ
    q = [f'<rect x="0" y="0" width="560" height="520" fill="#fffdf5"/>']
    def box(x1, y1, x2, y2, fill):  # liberty x1..x2, care y1..y2
        return f'<rect x="{X(x1)}" y="{Y(y2)}" width="{X(x2) - X(x1)}" height="{Y(y1) - Y(y2)}" fill="{fill}"/>'
    q += [box(55, 55, 100, 100, "#fff1b8"), box(55, 0, 100, 45, "#efe6cc"), box(0, 55, 45, 100, "#e3e8f4"), box(0, 0, 45, 45, "#f4dede")]
    q.append(f'<rect x="{X0}" y="{Y0}" width="{SZ}" height="{SZ}" fill="none" stroke="#1a1a1a" stroke-width="2"/>')
    q.append(f'<path d="M{X(50)} {Y0}V{Y0 + SZ}M{X0} {Y(50)}H{X0 + SZ}" stroke="#1a1a1a" stroke-dasharray="5 5" opacity=".5"/>')
    for (x, y, anchor, name, sub) in [(X(100) - 10, Y(100) + 28, "end", "The Good Neighbor", "free and kind"),
                                      (X(100) - 10, Y(0) - 30, "end", "The Lone Wolf", "free and alone"),
                                      (X(0) + 10, Y(100) + 28, "start", "The Caretaker", "kind, by the rules"),
                                      (X(0) + 10, Y(0) - 30, "start", "The Hall Monitor", "by the rules")]:
        q.append(halo(x, y, name, 17, 800, anchor))
        q.append(halo(x, y + 20, sub, 14, 600, anchor, "#333"))
    q.append(halo(X(50), Y(50) - 8, "The Fixer", 15, 800, "middle"))
    q.append(halo(X(50), Y(50) + 10, "case by case", 13, 600, "middle", "#333"))
    q.append(f'<text x="{X0 + SZ / 2}" y="{Y0 + SZ + 34}" font-size="16" font-weight="700" text-anchor="middle" fill="#1a1a1a">Liberty in what you did →</text>')
    q.append(f'<text font-size="16" font-weight="700" text-anchor="middle" fill="#1a1a1a" transform="translate({X0 - 30} {Y0 + SZ / 2}) rotate(-90)">Care for the people involved →</text>')
    q.append(f'<text x="{X0}" y="{Y0 + SZ + 18}" font-size="13" fill="#333" text-anchor="middle">0</text><text x="{X0 + SZ}" y="{Y0 + SZ + 18}" font-size="13" fill="#333" text-anchor="middle">100</text>')
    desc = ("A square map of the five characters. Across is how much liberty your choices left people, from 0 to 100. Up is how well your choices "
            "looked after the people involved. Top right is the Good Neighbor, bottom right the Lone Wolf, top left the Caretaker, bottom left "
            "the Hall Monitor, and the band through the middle is the Fixer.")
    return ('<svg viewBox="0 0 560 520" role="img" aria-labelledby="cmt cmd"><title id="cmt">The five characters</title>'
            f'<desc id="cmd">{e(desc)}</desc>' + "".join(q) + '</svg>')


def play():
    body = f"""
<div class="quiz" id="life">
<div id="life-intro">
<p class="lead">Nobody asks what you believe. A year of ordinary life happens to you: a lemonade stand, a rooster at 5 a.m., a roofer who wants cash, a jury summons. You decide what to do. At the end you get your character, what your choices say about you, the best case against every one of them, and a link to start an argument.</p>
<ul class="facts">
<li><b>{MAIN} situations, about ten minutes.</b> Some choices come back on you, and you'll have to deal with what happens next.</li>
<li><b>No right answers.</b> Every choice is scored three ways: how you handle money and business, how much you leave people to run their own lives, and how the choice treats the people involved.</li>
<li><b>Nothing leaves your browser.</b> Your choices are saved on this device so you can stop and pick up later. The result link holds them, so you only share them if you send it.</li>
</ul>
<div class="row"><button class="btn gold" id="life-start" type="button">Start your year</button><button class="btn ghost" id="life-restart" type="button" hidden>Start over</button></div>
<noscript><p class="warn">The real-life quiz needs JavaScript to keep track of your choices. Everything else on the site works without it, including <a href="../traps.html">the purity traps</a>.</p></noscript>
</div>
<div id="life-prog" hidden><div class="progress" aria-hidden="true"><span id="life-bar"></span></div><p class="sr" id="life-status" aria-live="polite"></p></div>
<div id="life-stage" hidden></div>
</div>

<h2>Why this one is different</h2>
<div class="grid">
<div class="card">{ic("quiz")}<h3>The purity test asks what you think</h3><p>Agree or disagree with 40 statements. It's the easy version: everyone is a libertarian about things that never happen to them.</p><p><a href="../quiz.html">Take the purity test</a></p></div>
<div class="card">{ic("handshake")}<h3>This one asks what you'd do</h3><p>Your neighbor, your cousin, your kid, your jury. Real choices cost something, and the cost is where your actual beliefs live.</p></div>
<div class="card">{ic("scales")}<h3>Then it compares the two</h3><p>Take both and your result puts what you say and what you do on the same chart. The gap is usually the interesting part.</p></div>
</div>
"""
    page("life/index.html", "What would you actually do? The real-life libertarian quiz",
         f"{MAIN} everyday situations: a lemonade stand, a cash roofer, a jury, a homeless camp. Find out what your choices say about what you believe.",
         "What would you actually do?", body, kicker="The real-life quiz", crumbs=[("The real-life quiz", "")],
         scripts=("assets/life-data.js", "assets/life.js"), wide=False)


def result():
    R = copy.deepcopy(REFS)
    by = {r["n"]: r for r in R}
    pick = [i for i, r in enumerate(REFS) if r["n"] in ("Karl Marx", "Thomas Hobbes", "The DMV")]
    chart = chart_svg(R, "What you say and what you do, on the libertarian spectrum", names=True, pick=pick, uid="l")
    body = f"""
<div id="lres" aria-live="polite"><p>Reading your year...</p><noscript><p class="warn">Your result needs JavaScript. <a href="index.html">The real-life quiz</a> explains what it measures.</p></noscript></div>
<div id="lafter" hidden>
<h2>Your character sheet</h2>
<div id="lsheet"></div>
<figure class="fig"><figcaption>Where your choices put you among the five characters. The gold star is the result on this page.</figcaption><div class="chart" id="lmap">{class_map()}</div></figure>
<h2>What you say, and what you do</h2>
<div class="chart" id="lchart">{chart}</div>
<p class="src">Up is more liberty, down more authority, left and right as usual. <a href="../spectrum.html#how">How to read this chart</a>.</p>
<div id="lsaydo"></div>
<h2>How you fix things</h2>
<div id="lhow"></div>
<h2>Your theory of change</h2>
<div id="ltheory"></div>
<h2 id="journal">Your year, choice by choice</h2>
<p>What each choice shows, and the best case someone could make against it. You don't have to agree. You do have to answer it.</p>
<div id="ljournal"></div>
<h2>Start the argument</h2>
<p>Your link holds your choices. Send it to someone who'd choose differently. If they've played in their own browser, they'll see every situation where you two split.</p>
<div class="copyrow"><label class="sr" for="lshare">Your result link</label><input id="lshare" readonly><button class="btn" id="lcopy" type="button">Copy link</button><button class="btn ghost" id="lnative" type="button" hidden>Share</button></div>
<p id="lcopymsg" aria-live="polite"></p>
<h2>Now do something with it</h2>
<div class="grid">
<a class="card cardlink" href="../quiz.html">{ic("quiz")}<h3>Take the purity test</h3><p>What you say you believe, to put next to what you do.</p></a>
<a class="card cardlink" href="../causes/index.html">{ic("torch")}<h3>Pick a cause</h3><p>Cannabis, sex work, bodily autonomy, licensing and more.</p></a>
<a class="card cardlink" href="../organize/index.html">{ic("megaphone")}<h3>Organize</h3><p>Being a good neighbor, at the scale of a county.</p></a>
<a class="card cardlink" href="../rpg/index.html">{ic("porcupine")}<h3>Play your character</h3><p>Herding Porcupines: take this character into a town that disagrees with you and build a coalition.</p></a>
</div>
<p class="row"><a class="btn ghost" href="index.html">Play again</a></p>
</div>
"""
    page("life/result.html", "Your real-life result", "Your character, what your choices say about you, and the case against each one.", "", body,
         crumbs=[("The real-life quiz", "life/index.html"), ("Your result", "")], scripts=("assets/life-data.js", "assets/life.js"))
