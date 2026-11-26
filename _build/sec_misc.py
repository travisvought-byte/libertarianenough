"""Book, free sites, about, 404."""
from core import page, e, ic, ext, REPO, CHECKED
from quizdata import QUESTIONS


def build():
    book(); free_sites(); about(); notfound()


def book():
    body = """
<p class="lead">The Asymmetric Libertarian: A Field Manual for Winning in 2026, by Travis Jon Vought, is the backbone of this site. Its argument fits on a bumper sticker: <b>libertarians don't lose because they're wrong. They lose because they're not operational.</b></p>
<h2>The big ideas</h2>
<ul class="facts">
<li><b>From ideological to operational.</b> Stop arguing about what freedom means and start fixing the systems that block it. "If it does not work in reality, it does not count."</li>
<li><b>Freedom is capability, not permission.</b> A right you can't actually use is "not freedom. It is theory."</li>
<li><b>Systems decide outcomes.</b> Incentives, friction, information and the cost of failure decide what people actually do, more than any law's stated purpose.</li>
<li><b>You get what you reward.</b> Not what you design for.</li>
<li><b>Complexity is control.</b> Government rarely bans things outright anymore. It buries them in friction. The legibility test: can a normal person do this without hiring help?</li>
<li><b>Failure cost kills freedom.</b> When one mistake costs you your license, your savings or your kids, people stop trying. Lower the cost of failure and you widen freedom.</li>
<li><b>Voters ask four questions:</b> how long, how much, what if I mess up, and can I figure it out?</li>
<li><b>Clear beats clever.</b> The 10-second test, the one-sentence rule, and problem, pain, fix. <a href="organize/messaging.html">The full messaging playbook</a>.</li>
<li><b>Execution wins.</b> A daily loop of posting, replying, reaching out and showing real fixes. Consistency beats intensity. <a href="organize/field.html">The daily loop</a>.</li>
<li><b>Govern by fixing one thing completely.</b> Pick one system, fix it all the way, make it visible, repeat.</li>
<li><b>Scale what works.</b> Prove it, then repeat it.</li>
</ul>
<h2>Lines worth stealing</h2>
<blockquote><p>"If you need a lawyer just to open a door, you're not free."</p></blockquote>
<blockquote><p>"You cannot lecture a system into working."</p></blockquote>
<blockquote><p>"Libertarians speak in truth. Voters respond to lived experience."</p></blockquote>
<h2>Where it shows up on this site</h2>
<ul class="facts">
<li>The <a href="organize/index.html">organizing playbook</a> is built on its execution chapters.</li>
<li>Every <a href="causes/index.html">cause page</a> has a 10-second message in its four message types.</li>
<li>Every <a href="types/index.html">quiz type</a> ends with an operational tip for that kind of libertarian.</li>
<li>The <a href="learn/what-counts.html">what counts page</a> uses its stricter test.</li>
<li><a href="plan/index.html">The plan</a> uses its method to put reforms in order. The book doesn't set an order itself, so the order is ours.</li>
</ul>
<h2>About the book</h2>
<p>Written by Travis Jon Vought, published 2026. The author shares it under a non-commercial license: you're encouraged to share, quote and distribute it for non-commercial purposes, with attribution. Quotes on this site are used that way.</p>
"""
    page("book.html", "The Asymmetric Libertarian, the book behind this site", "Key ideas from The Asymmetric Libertarian by Travis Jon Vought: operational libertarianism, systems, friction, failure cost and messaging that lands.",
         "The Asymmetric Libertarian", body, kicker="The book behind the site", crumbs=[("The book", "")], wide=False)


def free_sites():
    built = [
        ("https://findbingo.org", "Find Bingo", "A national directory of bingo games."),
        ("https://ohiobingo.org", "Ohio Bingo", "Every bingo game in Ohio."),
        ("https://the-reefer.com", "The Reefer", "Cannabis law, state by state."),
        ("https://ohioweed.org", "OhioWeed.org", "Ohio's cannabis guide."),
        ("https://abuseofoffice.org", "Abuse of Office", "Public records on officials, lawmakers and lobbyists."),
    ]
    bl = "".join(f'<li>{ext(u, e(n))}: {e(d)}</li>' for u, n, d in built)
    body = f"""
<p class="lead">If you're a libertarian group or a candidate who needs a website, we'll build it free. You pay for your domain name, about the cost of a pizza a year, and nothing else.</p>
<h2>What you get</h2>
<ul class="facts">
<li><b>A fast, simple site</b> on your own domain, hosted free on GitHub Pages. No monthly hosting bill, no plugin updates, nothing to get hacked.</li>
<li><b>Accessible by default.</b> Built to WCAG AA: readable contrast, keyboard friendly, screen-reader friendly, big tap targets.</li>
<li><b>The pages that matter:</b> who you are, your causes, events, candidates, how to join, and a donate button that points to <em>your</em> processor and <em>your</em> account.</li>
<li><b>Privacy-friendly visitor counts</b> with no cookies.</li>
<li><b>You own it.</b> The code lives in a repository you can take anywhere.</li>
</ul>
<h2>Who qualifies</h2>
<ul class="facts">
<li>Libertarian state, county and campus groups, whatever their national affiliation.</li>
<li>Candidates running on libertarian ideas, in any party or none, especially for local and nonpartisan office.</li>
<li>Single-issue groups working on the <a href="causes/index.html">causes</a> on this site.</li>
</ul>
<h2>What we won't do</h2>
<ul class="facts">
<li>Handle your money. Donations go straight to your own account.</li>
<li>Write your platform or speak for you.</li>
<li>Build anything that targets people for who they are. Punch at ideas and behavior all you want.</li>
</ul>
<h2>What we've built</h2>
<p>These are run by the same builder. They're examples of the kind of site you'd get, not endorsements by them.</p>
<ul class="facts">{bl}</ul>
<h2>How to ask</h2>
<p>A request form is coming. For now, <a href="https://github.com/travisvought-byte/libertarianenough/issues/new?title=Free%20site%20request">open a request on GitHub</a> with your group's name, what you need, and a public way to confirm you're who you say you are.</p>
"""
    page("free-sites.html", "Free websites for libertarian groups and candidates", "Libertarian groups and candidates can get a fast, accessible website built free, hosted free, on their own domain.",
         "Free websites", body, crumbs=[("Free websites", "")], wide=False)


def about():
    dims = [("Economic freedom", "taxes, minimum wage, licensing, tariffs, bailouts, the Fed, school money, raw milk"),
            ("Personal freedom", "drugs, sex work, speech, guns, marriage, immigration, warrants, seatbelts, abortion"),
            ("Radical", "anarchy, private roads, abolishing patents, secession, private nukes"),
            ("Left-libertarian", "co-ops, unions, landlords, corporate cronyism"),
            ("Traditional", "families and churches, secession, kings, heritage, and tariffs and immigration in reverse"),
            ("Pragmatism", "wearing a suit and trying to win"),
            ("Constitutional", "the Constitution as written, warrants, licensing"),
            ("Mises Caucus energy", "the Fed, the wars, politeness, lockdowns"),
            ("Voluntaryist", "not voting, crypto and the gray market")]
    dl = "".join(f"<li><b>{a}:</b> {b}.</li>" for a, b in dims)
    body = f"""
<h2>What this is</h2>
<p>Libertarian Enough is an independent libertarian organizing project. It is not a political party, has no ballot line, takes no donations, and is not affiliated with the Libertarian National Committee or any state party. It's a cheeky quiz on top of a serious toolkit: a guide to the movement for people outside it, and organizing and fundraising playbooks for people inside it.</p>
<p>It's made in Ohio by Travis Vought, a libertarian organizer and the author of <a href="book.html">The Asymmetric Libertarian</a>. Every jab on this site is aimed from inside the tent.</p>

<h2 id="scoring">How the quiz scores you</h2>
<p>There are {len(QUESTIONS)} statements. Each answer counts from -2 (strongly disagree) to +2 (strongly agree). Each statement feeds one or more of these scores, some in reverse:</p>
<ul class="facts">{dl}</ul>
<p>Each score is scaled from -1 to +1. Your spot on the chart is economic freedom and personal freedom, each turned into 0 to 100.</p>
<p><b>Purity score</b> = 40% economic freedom + 40% personal freedom + 20% radical. If you say liberty only works for people who share your heritage, it's zero, and you're a Collectivist in a Gadsden Flag.</p>
<p><b>Your type:</b> within 10 points of the middle on both axes, you're a centrist. Top right with both scores 60 or more, the quiz picks the libertarian flavor your other scores point to strongest: anarcho-capitalist, agorist, left-libertarian, paleo, Mises Caucus energy, classical liberal, pragmatist, purist (purity 90 or higher, with little pragmatism) or minarchist. If none of those pulls strongly, or you're top right but under 60 on either axis, you're a small-l libertarian. The other corners are progressive, conservative and statist.</p>
<p>The famous people and archetypes on the chart are our estimates, for fun. They didn't take the quiz.</p>

<h2 id="privacy">Privacy</h2>
<ul class="facts">
<li><b>No accounts, no sign-in.</b></li>
<li><b>Your quiz answers stay in your browser.</b> They're saved there so you can come back, and they're written into your results link after the # sign. Browsers don't send that part of a link to any server, so we never see your answers unless you send someone your link.</li>
<li><b>Visitor counts:</b> we use GoatCounter, which counts page views without cookies and doesn't store your IP address. It sees which page you opened, never your answers.</li>
<li><b>Hosting:</b> the site is hosted on GitHub Pages, which keeps standard server logs.</li>
</ul>

<h2 id="sources">Sources and data</h2>
<p>Every fact on the site has a source link next to it. The research behind the learn, causes, organize, fundraise and state pages is published as plain data files, so anyone can check or reuse it: {ext(REPO + "/tree/main/data", "the data folder on GitHub")}. Facts were checked {CHECKED}. Cannabis status comes from {ext("https://the-reefer.com", "The Reefer")}'s state data.</p>

<h2 id="fix">Found a mistake?</h2>
<p>Tell us and we'll fix it. {ext(REPO + "/issues/new?title=Correction", "Report a correction on GitHub")}, with the page and a source. A simpler form is coming.</p>
"""
    page("about.html", "About, scoring and privacy", "What Libertarian Enough is, how the quiz scores you, what happens to your answers, and where the facts come from.",
         "About Libertarian Enough", body, crumbs=[("About", "")], wide=False)


def notfound():
    body = """<p class="lead">This page doesn't exist. Much like a libertarian with a ballot-access plan.</p>
<p class="row"><a class="btn gold" href="/quiz.html">Take the quiz</a><a class="btn ghost" href="/">Home</a></p>"""
    page("404.html", "Page not found", "This page doesn't exist.", "Not found", body, wide=False)
