"""The guide for normies: what counts, factions, controversies, history, voices, demographics."""
from core import page, e, ic, ext, sources, data, clean_url

CR = [("Learn", "learn/index.html")]


def build():
    index()
    what_counts()
    factions()
    controversies()
    history()
    voices()
    demographics()


def index():
    cards = [
        ("what-counts.html", "scroll", "What counts, and what doesn't", "The short definition, the half-credit cases, and the stuff that wears a Gadsden flag but isn't libertarian at all."),
        ("factions.html", "people", "The factions", "Minarchists, ancaps, paleos, left-libertarians, the Mises Caucus and the rest: what each believes and wants."),
        ("controversies.html", "fight", "The fights", "Immigration, abortion, the Civil Rights Act, the 2022 takeover, the state splits: who's on each side and why it won't die."),
        ("history.html", "clock", "The history", "From Locke in 1689 to the 2025 party chair race, in 45 dated events."),
        ("voices.html", "megaphone", "The voices", "Thinkers, institutions, officeholders, podcasts and shows worth knowing."),
        ("demographics.html", "chart", "The numbers", "How many libertarians there are, who they are, and why every survey gets a different answer."),
    ]
    cardh = "".join(f'<a class="card cardlink" href="{h}">{ic(i)}<h2 style="font-size:1.2rem">{t}</h2><p>{d}</p></a>' for h, i, t, d in cards)
    body = f"""
<h2>The 60-second version</h2>
<p>Libertarians agree on one big thing: you own yourself, and nobody, including the government, gets to use force on peaceful people. That gets you legal weed, legal guns, low taxes, no draft, fewer cops in your business and fewer permits for your business. So far so good.</p>
<p>Then they fight about everything else, and the fights come down to three questions:</p>
<ul class="facts">
<li><b>How far?</b> Keep a small government (minarchists) or none at all (anarcho-capitalists and agorists)?</li>
<li><b>With whom?</b> Ally with the left on drugs, war and policing, or with the right on guns, taxes and lockdowns? Every faction answers this differently, and most of the yelling is really about this.</li>
<li><b>How to win?</b> Run normal-sounding candidates (pragmatists), say the whole message no matter what (purists), or go loud and populist (the Mises Caucus)?</li>
</ul>
<p>If you've ever watched libertarians and thought "why are they like this," the answer is usually one of those three. Everything below is sourced, so you can check us.</p>
<div class="grid">{cardh}</div>
"""
    page("learn/index.html", "The libertarian guide for normies", "What libertarians believe, the factions, the fights, the history and the numbers, explained for people who aren't in the movement.",
         "The guide for normies", body, lead="Everything you need to understand why libertarians act the way they do. Their agendas, in plain words.",
         crumbs=[("Learn", "")])


def what_counts():
    body = f"""
<h2>The short definition</h2>
<p>Libertarianism says each person owns their own life, and that starting force or fraud against peaceful people is wrong, whether a mugger does it or a government does. Libertarians want government shrunk to protecting rights (police, courts, defense) or, for the anarchist wing, gone. That one idea covers your wallet <em>and</em> your bedroom. If you only want one of the two freed, you're half way there.</p>

<h2>Counts</h2>
<ul class="facts">
<li><b>Minarchists.</b> Small state, only for protecting rights. The original Libertarian Party majority. <a href="factions.html#minarchists">More</a>.</li>
<li><b>Anarcho-capitalists.</b> No state at all, markets for everything including courts. Fully counts, roads question included. <a href="factions.html#anarcho-capitalists">More</a>.</li>
<li><b>Classical liberals.</b> Free markets, free speech, rule of law, a modest state. The grandparents of the whole movement. <a href="factions.html#classical-liberals">More</a>.</li>
<li><b>Left-libertarians, agorists and voluntaryists.</b> Anti-state with a different list of villains, or a different strategy. Counts. <a href="factions.html#left-libertarians">More</a>.</li>
<li><b>Bleeding-heart libertarians.</b> Free markets justified partly by how they help the poor. Counts, and they'll send you a paper about it. <a href="factions.html#bleeding-heart-libertarians">More</a>.</li>
<li><b>Paleolibertarians.</b> Counts on policy. Their strategy fights are on <a href="controversies.html#paleo-strategy-ron-paul-newsletters">the controversies page</a>, and the "liberty for my people only" corner of it doesn't count at all (see below). <a href="factions.html#paleolibertarians">More</a>.</li>
<li><b>Objectivists.</b> Adjacent. Ayn Rand recruited half the movement and rejected the label anyway. <a href="controversies.html#objectivists-vs-libertarians">The feud</a>.</li>
</ul>

<h2>Half credit</h2>
<ul class="facts">
<li><b>Wallet libertarians.</b> Hate taxes, love the drug war. That's a conservative who likes the word "liberty."</li>
<li><b>Bedroom libertarians.</b> Love legal weed, want a license for everything else. That's a progressive with a dispensary card.</li>
<li><b>"Fiscally conservative, socially liberal."</b> Counts if you mean it all the way through: guns, licensing, school choice, sex work, all of it. Usually people mean "I don't want to talk about politics at work."</li>
</ul>

<h2>Doesn't count, and why</h2>
<ul class="facts">
<li><b>"Liberty for my people only."</b> Rights belong to individuals, every one of them. Anyone who wants liberty for their own group and checkpoints for everyone else is a collectivist in a Gadsden flag. Even the Libertarian Party's current platform says it defends "the rights of every person, regardless of their race, ethnicity, or any other aspect of their identity" (plank 3.5, {ext("https://lp.org/platform-page/", "LP platform")}).</li>
<li><b>Wanting a king, even a privately owned one.</b> Swapping an elected government for an owner who can't be voted out is not less state. It's more state with a crown on it.</li>
<li><b>Sovereign citizens.</b> A legal theory, not a philosophy, and courts reject it every time. Declaring your car a "private conveyance" won't get you out of a traffic ticket. It will get you a longer hearing.</li>
<li><b>Crony capitalism.</b> Pro-market is not pro-business. A company lobbying for a license rule that keeps competitors out is using the state as a weapon. Libertarians are against that, even when the company sponsors the event.</li>
<li><b>Using the state on your enemies.</b> If your plan needs government to punish people you don't like, it isn't a libertarian plan, however many Mises quotes are in the thread.</li>
<li><b>"Free speech" as a shield for being a jerk.</b> Free speech means the government can't jail you for what you say. It doesn't mean nobody gets to call you a jerk, block you or decline to book you.</li>
</ul>

<h2>Still argued about, and that's fine</h2>
<p>Abortion, immigration, intellectual property, voting, war, and yes, the roads. Libertarians can land on either side of these and still count. <a href="controversies.html">Here's who's on each side and why</a>.</p>

<h2>The stricter test</h2>
<p><a href="../book.html">The Asymmetric Libertarian</a> adds one more: "If it does not work in reality, it does not count." A position you can defend in a comment section but can't explain to a voter in ten seconds isn't a policy yet. It's a hobby.</p>
"""
    page("learn/what-counts.html", "What counts as libertarian, and what doesn't", "The short definition of libertarianism, the half-credit cases, and the things that use the label but aren't libertarian.",
         "What counts, and what doesn't", body, lead="Libertarian is one of the most borrowed labels in politics. Here's the line, and the people standing on the wrong side of it.",
         crumbs=CR + [("What counts", "")], wide=False)


def factions():
    d = data("factions")
    toc = "".join(f'<li><a href="#{f["id"]}">{e(f["name"])}</a></li>' for f in d["factions"])
    parts = []
    for f in d["factions"]:
        figs = "".join(f"<li>{e(x)}</li>" for x in f["institutions_or_figures"])
        parts.append(f'<section class="card" id="{f["id"]}" style="margin:1rem 0"><h2 style="margin-top:.2em">{e(f["name"])}</h2>'
                     f'<p><b>What they believe:</b> {e(f["belief"])}</p><p><b>What they want:</b> {e(f["agenda"])}</p>'
                     f'<p><b>Who and what:</b></p><ul>{figs}</ul><p><b>Who they fight with:</b> {e(f["clashes_with"])}</p>'
                     f'<p>{sources(f["sources"])}</p></section>')
    body = f"""<p>Fourteen factions, fairly described. Not every libertarian fits one box, and plenty fit three. Take <a href="../quiz.html">the quiz</a> to see which one claims you.</p>
<nav aria-label="Factions on this page"><ul class="statelist">{toc}</ul></nav>
{"".join(parts)}"""
    page("learn/factions.html", "Libertarian factions explained", "Minarchists, anarcho-capitalists, classical liberals, left-libertarians, paleolibertarians, the Mises Caucus and more: beliefs, agendas and feuds.",
         "The factions", body, lead="Who's who in the libertarian movement, what each group wants, and who they're mad at.", crumbs=CR + [("Factions", "")])


def fmt_date(d):
    return e(str(d)) if d else ""


def controversies():
    d = data("controversies")
    toc = "".join(f'<li><a href="#{c["id"]}">{e(c["title"])}</a></li>' for c in d["controversies"])
    parts = []
    for c in d["controversies"]:
        sides = "".join(f'<li><b>{e(s["position"])}</b><br>Who says so: {e(s["who"])}</li>' for s in c["sides"])
        evs = "".join(f'<li><b>{fmt_date(ev["date"])}:</b> {e(ev["text"])} {sources([ev["source"]]) if ev.get("source") else ""}</li>' for ev in c["events"])
        parts.append(f'<section id="{c["id"]}" style="margin:2rem 0"><h2>{e(c["title"])}</h2><p class="lead" style="font-size:1.05rem">{e(c["what"])}</p>'
                     f'<h3>The sides, and who makes it a fight</h3><ul class="facts">{sides}</ul>'
                     f'<h3>Why it won\'t die</h3><p>{e(c["why_it_persists"])}</p>'
                     f'<h3>What happened</h3><ul class="facts">{evs}</ul><p>{sources(c["sources"], "More sources")}</p></section>')
    body = f"""<p>Every movement has fights. Libertarians just hold theirs at the microphone, on C-SPAN, during the nominating convention. Here are the {len(d["controversies"])} that matter, with each side stated the way its own people would state it.</p>
<nav aria-label="Fights on this page"><ul class="facts">{toc}</ul></nav>
{"".join(parts)}"""
    page("learn/controversies.html", "Libertarian controversies: who's fighting and why", "Immigration, abortion, the Civil Rights Act, the Ron Paul newsletters, the 2022 Mises Caucus takeover, state party splits and the 2024 convention.",
         "The fights", body, lead="What libertarians fight about, who's on each side, and who keeps the fight going.", crumbs=CR + [("Controversies", "")], wide=False)


def history():
    d = data("history")
    items = []
    for ev in d["events"]:
        when = ev["date"] or str(ev["year"])
        items.append(f'<li><p><b>{e(when)}: {e(ev["title"])}</b><br>{e(ev["text"])}<br>{sources(ev["sources"])}</p></li>')
    body = f"""<ol class="facts" reversed style="list-style:none;padding-left:0">{"".join(reversed(items))}</ol>
<p class="src">Newest first. Dates are when the thing happened; where only the year is known, only the year is shown.</p>"""
    page("learn/history.html", "Libertarian history timeline", "From Locke and Paine to the founding of the Libertarian Party, Ron Paul, the Mises Caucus and the 2024 convention.",
         "The history", body, lead=f'{len(d["events"])} moments, from John Locke in 1689 to the party chair race in 2025.', crumbs=CR + [("History", "")], wide=False)


def voices():
    d = data("voices")["groups"]
    def card(x, extra=""):
        link = ext(x["url"], e(x["name"])) if x.get("url") else e(x["name"])
        return f'<div class="card"><h3 style="margin-top:.2em">{link}</h3>{extra}<p>{e(x["line"])}</p><p>{sources(x["sources"])}</p></div>'
    th = "".join(card(x, f'<p class="src">{e(x.get("years",""))}</p>' if x.get("years") else "") for x in d["thinkers"])
    ins = "".join(card(x) for x in d["institutions"])
    off = "".join(card(x, f'<p><span class="badge">{e(x["party"])}</span> <span class="badge">{"In office" if x.get("status")=="current" else "Former" if x.get("status")=="former" else e(x.get("status",""))}</span></p><p class="src">{e(x["office"])}</p>') for x in d["officeholders"])
    med = "".join(card(x, f'<p><span class="badge">{e(x.get("kind",""))}</span></p>') for x in d["media"])
    body = f"""<p>Listing someone here means they matter to the movement, not that we agree with them or that they agree with each other. Several of them would rather not share a page.</p>
<h2>Thinkers</h2><div class="grid">{th}</div>
<h2>Institutions</h2><div class="grid">{ins}</div>
<h2>Officeholders</h2><p>Elected people who call themselves libertarian or libertarian-leaning, or who hold the libertarian line on enough votes that the movement claims them. Party labels are theirs.</p><div class="grid">{off}</div>
<h2>Shows, podcasts and books</h2><div class="grid">{med}</div>"""
    page("learn/voices.html", "Libertarian voices: thinkers, institutions, officeholders and media", "The thinkers, think tanks, officeholders, shows and podcasts that shape the libertarian movement.",
         "The voices", body, lead="Who to read, who to watch, and who keeps getting quoted at meetings.", crumbs=CR + [("Voices", "")])


def demographics():
    d = data("demographics")
    rows = "".join(f'<tr><td>{e(f["stat"])}</td><td><b>{e(f["value"])}</b></td><td>{e(str(f["year"]))}</td><td>{ext(clean_url(f["url"]), e(f["source_name"]))}{("<br><span class=src>" + e(f["note"]) + "</span>") if f.get("note") else ""}</td></tr>' for f in d["findings"])
    cav = "".join(f"<li>{e(c)}</li>" for c in d["caveats"])
    body = f"""<h2>Why the numbers disagree</h2><ul class="facts">{cav}</ul>
<h2>The findings</h2>
<div class="tablewrap"><table><caption>Libertarian numbers from surveys, party records and research</caption>
<thead><tr><th scope="col">What</th><th scope="col">Number</th><th scope="col">Year</th><th scope="col">Source</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>What it means</h2>
<p>Lots of Americans hold libertarian-ish views, far fewer call themselves libertarian, and a tiny slice pay dues to the party. That gap is the whole opportunity. The people are out there. The organizing isn't. <a href="../organize/index.html">Fix that</a>.</p>"""
    page("learn/demographics.html", "How many libertarians are there? Demographics and surveys", "Survey counts of libertarians, who they are, party registration and membership, and why each survey defines libertarian differently.",
         "The numbers", body, lead="Somewhere between 7% and 27% of Americans, depending on who asks and how. Here's every number and why they don't match.",
         crumbs=CR + [("Demographics", "")])
