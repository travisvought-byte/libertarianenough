"""Home, quiz, results, types, spectrum and traps."""
import copy
from core import page, e, ic, ext, chart_svg, ref_table
import sec_stats
from sec_plan import mini_road
from quizdata import QUESTIONS, TYPES, REFS, VERDICTS, ANSWERS, HEDGE

N = len(QUESTIONS)


def build():
    home()
    quiz()
    results()
    types()
    spectrum()
    traps()


def home():
    doors = [
        ("learn/index.html", "book", "Learn the scene", "Who's who, what counts as libertarian, what doesn't, and why everyone at the convention is yelling."),
        ("causes/index.html", "torch", "Pick a cause", "Cannabis, sex work, bodily autonomy and nine more fights, with facts and things to do this month."),
        ("organize/index.html", "megaphone", "Actually organize", "The playbook libertarians keep skipping: precinct seats, candidates, messages that land in 10 seconds."),
        ("fundraise/index.html", "dollar", "Raise money in your state", "Dinners, small-dollar giving and charity models, stolen shamelessly from Republicans, Democrats and nonprofits."),
        ("states/index.html", "map", "Find your state", "Every state affiliate, the public facts, the drama, and a page your state can claim."),
        ("website-help.html", "browser", "Website help", "Put the quiz, the plan and ready-made issue pages on the site your group already has."),
    ]
    cards = "".join(f'<a class="card door cardlink" href="{h}">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for h, i, t, d in doors)
    body = f"""
<section class="hero">
<div>
<p class="kicker">The libertarian purity test, finally</p>
<h1>Are you libertarian enough?</h1>
<p class="lead">{N} statements. Roads, driver's licenses, Grand Theft Auto, heroin and, for the final boss, nukes. Find out what kind of libertarian you are, where you sit on the spectrum, and how many purity traps you walked straight into.</p>
<div class="row"><a class="btn gold" href="quiz.html">Take the quiz</a><a class="btn ghost" href="spectrum.html">See the spectrum</a></div>
<p class="src">About five minutes. Your answers stay in your browser. We never see them.</p>
</div>
<figure class="art heroart" id="homechart">{home_chart()}
<figcaption id="homecap">Where would you land? <a href="quiz.html">Take the quiz</a> and your gold star shows up here.</figcaption></figure>
</section>

<h2>The numbers behind the movement</h2>
<p>Lots of Americans lean libertarian. Very few of them join anything. That gap is the whole reason this site exists.</p>
{sec_stats.funnel()}
<p class="row"><a class="btn ghost" href="spectrum.html#numbers">More charts</a></p>

<h2>Being libertarian enough is the easy part</h2>
<p class="lead">Getting anything done is where the movement keeps tripping over its own bylaws. We've spent fifty years arguing about whether roads should be private while the other two parties quietly filled every county committee seat in America. This site is the fix: a guide for normies, a playbook for organizers, and tools for every state.</p>
<div class="grid">{cards}</div>

<h2>The plan: from more state to less</h2>
<p>"No government" is a destination, not a plan. Here's the road instead: six steps, in order, and every one of them has already been done somewhere in America.</p>
{mini_road("plan/")}
<p class="row"><a class="btn gold" href="plan/index.html">See the whole plan</a><a class="btn ghost" href="plan/gradual-or-abolish.html">The fight over how fast</a></p>

<h2>What this is, and what it isn't</h2>
<div class="grid">
<div class="card"><h3>An organizing body, not a party</h3><p>No ballot line, no national committee, no nine-hour bylaws debate. Libertarian Enough builds tools and playbooks for the people doing the work. It isn't affiliated with the Libertarian National Committee or any state party.</p></div>
<div class="card"><h3>We don't take your money</h3><p>No donations, no dues, no pass-through fund. State affiliates raise their own money in their own states, and we show them how. <a href="fundraise/index.html">How the money works</a>.</p></div>
<div class="card"><h3>Facts first, sass second</h3><p>Every fact on this site has a source and a date. The jokes are aimed at behavior and ideas, never at who people are. If we got something wrong, <a href="about.html#fix">tell us</a>.</p></div>
</div>

<h2>Signs your local group is a debate club</h2>
<ul class="facts">
<li>Your last meeting ran three hours and ended with a motion to table the motion to table.</li>
<li>You have more people who can explain the Austrian business cycle than people who can name your county auditor.</li>
<li>Your candidate list for next year is "whoever shows up."</li>
<li>You lost a precinct seat that took 3 votes to win. Nobody filed.</li>
</ul>
<p>If two of those landed, start with <a href="organize/index.html">the organizing playbook</a>. If all four did, start with <a href="book.html">the book</a>.</p>
"""
    page("index.html", "Are you libertarian enough? The quiz, the guide and the organizing playbook | Libertarian Enough",
         "Take the cheeky libertarian purity test, see where you land on the political spectrum, and learn how to actually organize and fundraise in your state.",
         "", body, scripts=("assets/data.js", "assets/score.js", "assets/home.js"))


def home_chart():
    R = copy.deepcopy(REFS)
    by = {r["n"]: r for r in R}
    by["Ayn Rand"]["side"] = "start"
    by["The 'liberty for me' guy"]["side"] = "start"
    by["The 'liberty for me' guy"]["n"] = "'Liberty for me' guy"
    pick = [i for i, r in enumerate(REFS) if r["n"] in ("Murray Rothbard", "Ayn Rand", "John Stuart Mill", "Karl Marx", "Thomas Hobbes",
                                                         "The DMV", "Franklin D. Roosevelt", "The 'liberty for me' guy")]
    return chart_svg(R, "The libertarian spectrum, with a few famous neighbors", names=True, pick=pick, uid="h")


def quiz():
    body = f"""
<div class="quiz" id="quiz">
<div id="quiz-intro">
<p class="lead">{N} statements, five answers each, about five minutes. At the end you get your libertarian type, a purity score out of 100, your spot on the spectrum next to Rothbard, Marx and your HOA, and receipts for every purity trap.</p>
<ul class="facts">
<li><b>No sign-up, no tracking of answers.</b> Your answers stay in this browser. The results link holds them, so you only share them if you send it.</li>
<li><b>"Not sure" is a real answer.</b> The purity police will notice, but it's allowed.</li>
<li><b>It's a joke with a real spectrum underneath.</b> <a href="about.html#scoring">How scoring works</a>.</li>
</ul>
<div class="row"><button class="btn gold" id="quiz-start" type="button">Start the quiz</button><button class="btn ghost" id="quiz-restart" type="button" hidden>Start over</button></div>
<noscript><p class="warn">The quiz needs JavaScript to score your answers. Everything else on the site works without it. You can read <a href="traps.html">the purity traps</a> and <a href="types/index.html">all 15 types</a> right now.</p></noscript>
</div>
<div id="quiz-prog" hidden><div class="progress" aria-hidden="true"><span id="quiz-bar"></span></div><p class="sr" id="quiz-status" aria-live="polite"></p></div>
<div id="quiz-stage" hidden></div>
</div>
"""
    page("quiz.html", "The quiz: are you libertarian enough?", f"{N} statements on roads, licenses, drugs, guns, voting and nukes. Find your libertarian type and purity score.",
         "Are you libertarian enough?", body, kicker="The quiz", scripts=("assets/data.js", "assets/quiz.js"), wide=False)


def results():
    body = f"""
<div id="result" aria-live="polite"><p>Scoring your answers...</p><noscript><p class="warn">Results need JavaScript. <a href="types/index.html">Browse all 15 types</a> instead.</p></noscript></div>
<div id="after" hidden>
<div class="chart" id="chart">{chart_svg(REFS, "Your spot on the libertarian spectrum")}</div>
<p class="src">Up is more liberty, down more authority, left and right as usual. <a href="spectrum.html#how">How to read this chart</a>.</p>
<h2>Your stat sheet</h2>
<div id="statsheet"></div>
<h2>How you prioritize</h2>
<div id="theory"></div>
<h3>Your closest neighbors on the chart</h3>
<div id="neighbors"></div>
<h2>Your purity trap receipts</h2>
<p>The questions the purity police actually care about, and how you did.</p>
<div id="receipts"></div>
<h2>Share it, start a fight</h2>
<p>Your link holds your answers, so anyone who opens it sees this result. If they've taken the quiz in their own browser, they'll see who's more libertarian enough.</p>
<div class="copyrow"><label class="sr" for="share-url">Your results link</label><input id="share-url" readonly><button class="btn" id="copy-btn" type="button">Copy link</button><button class="btn ghost" id="share-native" type="button" hidden>Share</button></div>
<p id="copy-msg" aria-live="polite"></p>
<h2>Now do something with it</h2>
<div class="grid">
<a class="card cardlink" href="causes/index.html">{ic("torch")}<h3>Pick a cause</h3><p>Cannabis, sex work, bodily autonomy, licensing and more.</p></a>
<a class="card cardlink" href="organize/index.html">{ic("megaphone")}<h3>Organize</h3><p>The playbook for getting something done locally.</p></a>
<a class="card cardlink" href="learn/factions.html">{ic("people")}<h3>Meet the factions</h3><p>Who you'd sit with at the convention, and who'd boo you.</p></a>
</div>
<h2>Everyone on the chart</h2>
{ref_table(REFS, you_row=True)}
<p class="row"><a class="btn ghost" href="quiz.html">Retake the quiz</a></p>
</div>
"""
    page("results.html", "Your results", "Your libertarian type, purity score and spot on the spectrum.", "", body,
         scripts=("assets/data.js", "assets/score.js", "assets/results.js"), crumbs=[("Your results", "")])


def type_page(t):
    kin = f'<p>Real-world kin: <a href="../learn/factions.html#{t["kin"]}">the {e(t["kin"].replace("-", " "))} on the factions page</a>.</p>' if t["kin"] else ""
    return f"""
<div class="result-head">{ic(t["icon"], "typeic", 88)}<div><p class="lead"><b>{e(t["tagline"])}</b></p></div></div>
<h2>Who you are</h2><p>{e(t["short"])}</p>
<h2>The roast</h2><p class="sass">{e(t["roast"])}</p>
{kin}
<h2>If you want to actually get something done</h2><p>{e(t["tip"])}</p>
<p class="row"><a class="btn gold" href="../quiz.html">Take the quiz</a><a class="btn ghost" href="index.html">All 15 types</a></p>
"""


def types():
    for t in TYPES:
        page(f"types/{t['id']}.html", f"{t['name']}: libertarian type", f"{t['name']}. {t['tagline']} {t['short']}", e(t["name"]),
             type_page(t), kicker="Libertarian type", crumbs=[("Types", "types/index.html"), (t["name"], "")], wide=False)
    cards = "".join(f'<a class="card cardlink typecard" href="{t["id"]}.html">{ic(t["icon"])}<h2 style="font-size:1.2rem">{e(t["name"])}</h2><p><b>{e(t["tagline"])}</b></p><p>{e(t["short"])}</p></a>' for t in TYPES)
    body = f"""<div class="grid">{cards}</div>
<h2>How you get sorted</h2>
<p>First the quiz finds your spot on two axes, economic freedom and personal freedom. Land in the top right and it looks at your answers on anarchy, voting, tradition, the Fed, the Constitution and the rest to pick which flavor of libertarian you are. Land anywhere else and you're a progressive, conservative, statist or centrist. One answer overrides everything: say liberty only works for people who share your heritage, and you're a Collectivist in a Gadsden Flag no matter what else you said. <a href="../about.html#scoring">Full scoring details</a>.</p>"""
    page("types/index.html", "All 15 libertarian types", "Minarchist, ancap, agorist, left-libertarian, paleo, Mises Caucus energy, purist, pragmatist and more.",
         "All 15 types", body, lead="Nine kinds of libertarian, four kinds of not, one centrist and one collectivist hiding in a Gadsden flag.",
         crumbs=[("Types", "")])


def spectrum():
    body = f"""
<div class="chart">{chart_svg(REFS)}</div>
{ref_table(REFS)}
<h2 id="how">How the chart works</h2>
<p>It's a cross. <b>Up and down</b> is liberty against authority: how much the state runs your life and your money combined. <b>Left and right</b> is the usual left-right split: progressives want the bedroom free and the economy managed, conservatives the reverse.</p>
<p>The diamond is built from two scores. <b>Economic freedom</b> runs up the lower-right edge: taxes, minimum wage, licensing, tariffs, bailouts, the Fed. <b>Personal freedom</b> runs up the lower-left edge: drugs, sex work, speech, guns, marriage, immigration, warrants. Max out both and you're at the top. Zero out both and you're at the bottom with the DMV.</p>
<div class="grid">
<div class="card"><h3>Libertarian, top</h3><p>Free wallet, free life. Both scores over 50.</p></div>
<div class="card"><h3>Progressive, left</h3><p>Free life, managed wallet.</p></div>
<div class="card"><h3>Conservative, right</h3><p>Free wallet, managed life.</p></div>
<div class="card"><h3>Statist, bottom</h3><p>The state runs both. The small square in the middle is centrist.</p></div>
</div>
<p>This is the Nolan Chart. David Nolan, who helped found the Libertarian Party, published it in January 1971, and the party's own quiz still uses the diamond ({ext("https://en.wikipedia.org/wiki/Nolan_Chart", "Wikipedia on the Nolan Chart")}). Ours adds a purity score, because of course it does.</p>
<h2 id="numbers">By the numbers</h2>
<p>We don't collect quiz answers, so there's no live leaderboard. These come from national surveys and party counts instead.</p>
{sec_stats.block()}
<h2>Why no live leaderboard?</h2>
<p>We don't collect your answers, so there's nothing to average. You're compared with famous people, archetypes and any friend who sends you their link. The positions on the chart are our cheeky estimates, not survey data. If you think we put Hayek in the wrong spot, you're probably right and also exactly the kind of person who'd say so.</p>
<p class="row"><a class="btn gold" href="quiz.html">Find your spot</a></p>
"""
    page("spectrum.html", "The libertarian spectrum", "The Nolan Chart as a cross: liberty against authority, left against right, with Rothbard, Marx, your HOA and real survey numbers.",
         "The spectrum", body, lead="A real cross: liberty against authority, left against right. Twenty reference points, three charts of real numbers, and a gold star with your name on it once you take the quiz.",
         crumbs=[("The spectrum", "")])


def traps():
    items = []
    for q in QUESTIONS:
        if not q.get("trap"):
            continue
        want = "Agree" if q["trap"] == "agree" else "Disagree"
        items.append(f'<div class="card"><h2 style="font-size:1.2rem">{e(q["t"])}</h2>'
                     f'<p><span class="badge">Purity answer: {want}</span></p>'
                     f'<p><b>Pass:</b> {e(q["pass_"])}</p><p><b>Fail:</b> {e(q["fail"])}</p></div>')
    body = f"""<div class="grid">{"".join(items)}</div>
<h2>Why we roast purity tests while giving you one</h2>
<p>Because the purity test is the movement's favorite hobby and its worst habit. A movement that boos driver's licenses on live TV is not a movement that's going to win your county commission. Pass every trap and you're libertarian enough. Then read <a href="organize/index.html">the organizing playbook</a> and figure out what to do with it.</p>
<p>The driver's license moment is real: at the Libertarian Party's 2016 presidential debate, a candidate who said he supported driver's licenses got booed. <a href="learn/controversies.html#purity-tests-2016">The story is on the controversies page</a>.</p>
<p class="row"><a class="btn gold" href="quiz.html">Take the quiz</a></p>"""
    page("traps.html", "The purity traps", "Taxation, roads, driver's licenses, heroin, tanks, voting, kings and private nukes: the questions the purity police care about.",
         "The purity traps", body, lead=f"{sum(1 for q in QUESTIONS if q.get('trap'))} questions where the answer libertarians are 'supposed' to give and the answer normal people give are very far apart.",
         crumbs=[("Purity traps", "")])
