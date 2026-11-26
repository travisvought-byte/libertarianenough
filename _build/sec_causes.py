"""Causes: the fights that get people off the couch."""
from core import page, e, ic, ext, sources, data

LINK_STRIPCLUB = False  # set True once stripclubguide.org is confirmed live

META = {
    "cannabis": ("Cannabis", "torch", "The plant is legal in half the country and still a felony in the other half. That's not federalism, that's a lottery.",
                 "Nobody should lose their job, their kids or their freedom over a plant that's legal one state over.", "Pain relief"),
    "sex-work": ("Sex work", "heart", "Consenting adults, private transactions, and a government that still sends vice squads. Core libertarian ground, and the movement gets shy about it.",
                 "Adults should be able to work safely without getting arrested for it.", "Risk reduction"),
    "bodily-autonomy": ("Bodily autonomy", "halo", "Self-ownership starts at your skin. What you put in your body, what treatment you try, and how you face the end belong to you.",
                        "Your body, your decisions, from the medicine you try to the care you choose at the end.", "Control exposure"),
    "licensing": ("Permission to work", "stamp", "Hair braiders, florists and movers shouldn't need a year of classes and a state board's blessing to earn a living.",
                  "If another state says you're qualified, you can work here immediately.", "Access expansion"),
    "forfeiture": ("Civil asset forfeiture", "dollar", "Police can take your cash or car without charging you with a crime, and you have to sue to get it back. Read that twice.",
                   "Police shouldn't keep your money when nobody was charged with a crime.", "Control exposure"),
    "housing": ("Housing and zoning", "fence", "Rent is high because building homes is mostly illegal. Zoning boards are the most powerful government most people never think about.",
                "If you own the lot, you should be able to build a home for your mom on it.", "Access expansion"),
    "speech-privacy": ("Speech and privacy", "lantern", "Agencies buy your data from brokers instead of getting warrants. Say what you want, keep what's yours private.",
                       "If the government wants your data, it should get a warrant, not a credit card.", "Control exposure"),
    "guns": ("Guns", "scroll", "The right to defend yourself shouldn't depend on your zip code or a permit office's mood.",
             "A peaceful adult shouldn't need a permission slip to protect their family.", "Risk reduction"),
    "war": ("War and foreign policy", "megaphone", "War is the health of the state. One 2001 vote is still being used to justify fights Congress never debated.",
            "Congress votes on wars. A vote from 2001 doesn't cover every war after it.", "Control exposure"),
    "schooling": ("Schooling", "book", "Parents, not zip codes, should decide where kids learn.",
                  "School money should follow the kid, not the building.", "Access expansion"),
    "food": ("Food freedom", "coins", "If your neighbor can sell you a pie at the bake sale, they can sell it to you on a Tuesday.",
             "You should be able to buy food from your neighbor without a state inspector in the middle.", "Access expansion"),
    "criminal-justice": ("Criminal justice", "clock", "Lock up people who hurt people. Stop filling cells with people who didn't.",
                         "Jail should be for people who hurt people, not people who annoyed a statute.", "Pain relief"),
}

OWN = {
    "cannabis": [("https://the-reefer.com", "The Reefer"), ("https://ohioweed.org", "OhioWeed.org")],
}


def build():
    d = data("causes")["causes"]
    for c in d:
        cause_page(c)
    index(d)


def cause_page(c):
    name, icon, pitch, msg, kind = META[c["id"]]
    facts = "".join(f'<li>{e(f["text"])} <span class="src">As of {e(str(f["as_of"]))}.</span> {sources([f["source"]])}</li>' for f in c["facts"])
    orgs = "".join(f'<li>{ext(o["url"], e(o["name"]))}: {e(o["line"])}</li>' for o in c["organizations"])
    acts = "".join(f"<li>{e(a)}</li>" for a in c["local_actions"])
    own = ""
    links = list(OWN.get(c["id"], []))
    if c["id"] == "sex-work" and LINK_STRIPCLUB:
        links.append(("https://stripclubguide.org", "Strip Club Guide"))
    if links:
        own = ('<h2>Built by the same people</h2><p>Our sister sites do the state-by-state work on this one: '
               + ", ".join(ext(u, t) for u, t in links) + ".</p>")
    body = f"""
<p class="lead">{e(pitch)}</p>
<div class="note"><p><b>Say it in 10 seconds:</b> "{e(msg)}"</p><p class="src">A {kind.lower()} message, in the language of <a href="../organize/messaging.html">the messaging playbook</a>.</p></div>
<h2>Where things stand</h2>
<ul class="facts">{facts}</ul>
<h2>Do this locally</h2>
<ol class="facts">{acts}</ol>
<p>Each one is a real-world win you can show voters. That's the whole <a href="../book.html">Asymmetric Libertarian</a> idea: pick one system, fix it, make it visible.</p>
<h2>Who's already fighting</h2>
<ul class="facts">{orgs}</ul>
<p class="src">Listing an organization isn't an endorsement or a partnership. It's who's doing the work.</p>
{own}
<p class="row"><a class="btn ghost" href="index.html">All causes</a><a class="btn gold" href="../organize/index.html">Organize around it</a></p>
"""
    page(f"causes/{c['id']}.html", f"{name}: the libertarian case and what to do", f"{name}: where things stand, a 10-second message, three things to do locally and who's already fighting.",
         e(name), body, kicker="Cause", crumbs=[("Causes", "causes/index.html"), (name, "")], wide=False)


def index(d):
    order = ["cannabis", "sex-work", "bodily-autonomy"]
    rest = [c["id"] for c in d if c["id"] not in order]
    def card(cid):
        name, icon, pitch, msg, kind = META[cid]
        return f'<a class="card cardlink" href="{cid}.html">{ic(icon)}<h3>{e(name)}</h3><p>{e(pitch)}</p></a>'
    body = f"""
<h2>The core three</h2>
<p>Rights above the state, starting with your own body. These are the issues where libertarians are right, the public is moving our way, and the other two parties are too scared to finish the job.</p>
<div class="grid">{"".join(card(c) for c in order)}</div>
<h2>Nine more fights worth picking</h2>
<div class="grid">{"".join(card(c) for c in rest)}</div>
<h2>How to pick one</h2>
<p>Don't pick the cause you can argue about longest. Pick the one where a real person in your town is getting hurt right now and a local office could fix it. The book calls this pain relief: name the problem, show the cost in time, money or risk, and give the fix. People don't join movements because of a syllogism. They join because somebody fixed something.</p>
"""
    page("causes/index.html", "Libertarian causes: cannabis, sex work, bodily autonomy and more", "Twelve causes with current facts, a 10-second message and three things to do locally for each.",
         "Causes", body, lead="Twelve fights with facts, a message that lands, and three things to do in your own town.", crumbs=[("Causes", "")])
