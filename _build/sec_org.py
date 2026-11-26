"""Organize and fundraise playbooks."""
from core import page, e, ic, ext, sources, data

OC = [("Organize", "organize/index.html")]
FC = [("Fundraise", "fundraise/index.html")]


def pts(topic_id, idx=None):
    t = next(t for t in data("organizing")["topics"] if t["id"] == topic_id)
    ps = t["points"] if idx is None else [t["points"][i] for i in idx]
    return '<ul class="facts">' + "".join(f'<li>{e(p["text"])} {sources([p["source"]])}</li>' for p in ps) + "</ul>"


def build():
    org_index(); structure(); meetings(); field(); candidates(); ballot(); messaging(); steal()
    fund_index(); events(); small_dollar(); models(); rules()


def org_index():
    pages = [
        ("../plan/index.html", "road", "Start with the plan", "Six steps from more government to less, and what your group can do on each one."),
        ("structure.html", "people", "Build from the precinct up", "How the big parties are built, and the seats nobody runs for."),
        ("meetings.html", "clock", "Run a meeting people come back to", "Sixty minutes, one decision, one ask. No bylaws."),
        ("field.html", "map", "Talk to voters", "Door knocking works. Phone banking doesn't. Your friends are your best list."),
        ("candidates.html", "ballot", "Recruit and run candidates", "Most local races have nobody running. That's the opening."),
        ("ballot-access.html", "scroll", "Ballot access", "How parties get on the ballot, and why you should sign the petition."),
        ("messaging.html", "megaphone", "Messages that land", "The 10-second test, the one-sentence rule and the four kinds of message."),
        ("steal-this.html", "fight", "Steal from the big parties", "What Republicans and Democrats do that works, and how to copy it."),
    ]
    cards = "".join(f'<a class="card cardlink" href="{h}">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for h, i, t, d in pages)
    body = f"""
<p class="lead">Libertarians have the best ideas in American politics and the worst follow-through. We can explain monetary policy for three hours and can't find someone to file for the soil and water board. This is the fix.</p>

<h2>Things that are not organizing</h2>
<ul class="facts">
<li>Arguing about the platform. The platform has never knocked on a door.</li>
<li>A Facebook group with 3,000 members and four who show up.</li>
<li>A resolution condemning another state affiliate.</li>
<li>"Raising awareness." Everyone is aware. Nobody is organized.</li>
<li>Waiting for the national party to fix it.</li>
</ul>

<h2>The seven rules</h2>
<ol class="facts">
<li><b>Pick a system, not a philosophy.</b> One broken process in your county, fixed completely and made visible, beats a hundred essays.</li>
<li><b>Fill seats, not chat rooms.</b> Committee seats, board seats, appointed seats. Power is a list of chairs. Count them.</li>
<li><b>Run for what nobody else wants.</b> In 2024, 70% of the races Ballotpedia tracked had no more candidates than seats.</li>
<li><b>Meet for an hour, act for a month.</b> Every meeting ends with names next to tasks and dates next to names.</li>
<li><b>Talk about pain, not principles.</b> Time, cost, risk. Voters respond to lived experience.</li>
<li><b>Do the daily loop.</b> One clear post, every reply answered, ten new people, one real conversation. Consistency beats intensity.</li>
<li><b>Prove it, then repeat it.</b> When something works in one county, write it down and hand it to the next one.</li>
</ol>
<p>Rules 1, 5, 6 and 7 come straight from <a href="../book.html">The Asymmetric Libertarian</a>. Rules 2 and 3 come from watching the other two parties win for 150 years.</p>

<h2>The playbook</h2>
<div class="grid">{cards}</div>
"""
    page("organize/index.html", "How libertarians can actually organize", "A practical organizing playbook for libertarians: precinct seats, meetings, field, candidates, ballot access and messaging.",
         "Libertarians can't organize. Let's fix that.", body, kicker="The organizing playbook", crumbs=[("Organize", "")])


def structure():
    body = f"""
<p>The Republican and Democratic parties aren't really national organizations. They're thousands of county committees stacked on top of each other, and each county committee is a list of precinct seats. Whoever fills those seats picks the leaders, writes the rules and, in some states, fills empty public offices. Here's how it works, using Ohio and two other states as examples.</p>
<h2>How it's built</h2>
{pts("structure")}
<h2>What a libertarian affiliate should do with this</h2>
<ol class="facts">
<li><b>Map your seats.</b> List every precinct in your county. That's your org chart. A name goes next to each one, even if it's "open."</li>
<li><b>Recruit a precinct captain before a county chair.</b> A county chair with no precinct captains is a person with a title.</li>
<li><b>Know your state's minor-party rules.</b> In Ohio, minor parties pick committees under their own rules, so you can build the structure now without waiting for a ballot.</li>
<li><b>If you're a liberty Republican or Democrat,</b> file for your precinct seat. In some places three votes wins it. Nobody will stop you, because nobody else filed.</li>
</ol>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/structure.html", "Build from the precinct up", "How major parties are built from precinct seats, why those seats matter, and how a libertarian group can copy it.",
         "Build from the precinct up", body, crumbs=OC + [("Precinct up", "")], wide=False)


def meetings():
    body = """
<p>Most libertarian meetings fail the same way: no agenda, a three-hour argument, nobody leaves with a job. People come once and never come back. Here's the meeting people return to.</p>
<h2>The 60-minute meeting</h2>
<ol class="facts">
<li><b>0 to 5 minutes: welcome the new people by name.</b> Ask what brought them. Write it down. That's their cause and your recruiting data.</li>
<li><b>5 to 15: one win since last time.</b> Something real: a permit fee repealed, a candidate filed, a petition turned in. If there's no win, that's the agenda.</li>
<li><b>15 to 40: the one decision.</b> One question on the table, decided by the end. Everything else goes to a committee or the next meeting.</li>
<li><b>40 to 55: assignments.</b> Every task gets a name and a date. If nobody takes it, it isn't a priority, so drop it.</li>
<li><b>55 to 60: the ask.</b> One concrete ask for the month: knock 50 doors, get 200 signatures, bring one friend.</li>
</ol>
<h2>House rules</h2>
<ul class="facts">
<li><b>Bylaws never come to a monthly meeting.</b> They go to a committee that reports once a year.</li>
<li><b>Feed people.</b> Pizza costs less than a lost volunteer.</li>
<li><b>Start on time, end on time.</b> Respect for people's time is a libertarian value. Act like it.</li>
<li><b>Follow up within 24 hours.</b> Send the decisions and the assignments. If it isn't written down, it didn't happen.</li>
<li><b>Debate club is a separate night.</b> Philosophy is fun. Schedule it at the bar after the work's assigned.</li>
</ul>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/meetings.html", "Run a meeting people come back to", "A 60-minute meeting format for libertarian groups: one win, one decision, assignments, one ask.",
         "Run a meeting people come back to", body, crumbs=OC + [("Meetings", "")], wide=False)


def field():
    body = f"""
<p>Elections are won by talking to voters. The research on how is clear, and the big parties built whole data systems around it.</p>
<h2>What the evidence and the big parties show</h2>
{pts("field")}
<h2>The libertarian version</h2>
<ol class="facts">
<li><b>Knock doors.</b> Face to face is the one tactic the research backs. Do it in pairs, two hours on a Saturday, in one precinct you mapped.</li>
<li><b>Get the voter file.</b> Most states sell or provide their voter list to parties and candidates through the secretary of state or county boards. It's the cheapest data you'll ever buy.</li>
<li><b>Start with who you know.</b> Every member makes a list of 20 people. That list is better than any purchased one, and it's free.</li>
<li><b>Skip the phone bank.</b> Nobody answers, and the research says it doesn't move turnout anyway.</li>
</ol>
<h2>The daily loop</h2>
<p>From chapter 8 of <a href="../book.html">The Asymmetric Libertarian</a>. Do this every day and you'll outwork most campaigns in your state.</p>
<ol class="facts">
<li>Post one clear message.</li>
<li>Reply to every meaningful comment.</li>
<li>Reach out to 10 new people.</li>
<li>Have one real conversation.</li>
<li>Turn that conversation into content.</li>
<li>Share across your platforms.</li>
<li>Show one real-world problem and its fix.</li>
</ol>
<p><b>Consistency beats intensity.</b> A month of this beats one heroic weekend.</p>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/field.html", "Talk to voters: field, data and the daily loop", "What the research says about canvassing, how the big parties use voter data, relational organizing and a daily routine for libertarian organizers.",
         "Talk to voters", body, crumbs=OC + [("Field", "")], wide=False)


def candidates():
    body = f"""
<p>Here's the number that should end every "we can't win" conversation: most races in America don't have a contest at all.</p>
<h2>How many seats, and how many are empty of competition</h2>
{pts("candidates", [6, 7])}
<h2>Where Libertarians already win</h2>
{pts("third-party", [3, 4, 5])}
<p>Read that again: most Libertarian officeholders hold nonpartisan seats, and most city races are nonpartisan. The path is already marked. It goes through school boards, township trustees, soil and water boards and city councils, not the White House.</p>
<h2>How the big parties build candidates</h2>
{pts("candidates", [0, 1, 2, 3, 4, 5])}
<h2>Build your own candidate school</h2>
<ol class="facts">
<li><b>Make the binder.</b> Every office in your county, its filing deadline, the forms, the signature count, the fee. One page per office. This is the thing the California GOP handed out, and it's the thing most people never get.</li>
<li><b>Keep a bench list.</b> Every member who might run someday, what they care about and what they'd run for.</li>
<li><b>Recruit by cause.</b> The person fighting a zoning board is your planning commission candidate. The parent fighting the school is your school board candidate.</li>
<li><b>Train in one Saturday.</b> Filing, signatures, a 10-second message, door knocking, a basic website. We'll <a href="../free-sites.html">build the website free</a>.</li>
<li><b>Run a slate.</b> Five candidates in one county share volunteers, literature and a launch event.</li>
</ol>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/candidates.html", "Recruit and run libertarian candidates", "How many offices exist, how many go uncontested, where Libertarians win, and how to build a candidate school.",
         "Recruit and run candidates", body, crumbs=OC + [("Candidates", "")], wide=False)


def ballot():
    body = f"""
<p>A party that isn't on the ballot is a club. Ballot access rules are written by the parties already on the ballot, which tells you how friendly they are.</p>
<h2>How it works</h2>
{pts("third-party", [0, 1, 2])}
<h2>What to do</h2>
<ol class="facts">
<li><b>Know your state's rule cold.</b> Vote test, registration count or petition, and what keeps you on.</li>
<li><b>Plan petition season like a campaign.</b> Count the signatures, add a 30% cushion for bad ones, and set weekly targets.</li>
<li><b>Petition where people already are.</b> Farmers markets, festivals, polling places on election day where allowed.</li>
<li><b>Sign the petition, purists.</b> Yes, even if you think voting legitimizes the state. Signing a petition so other people get a choice is about as voluntary as politics gets.</li>
</ol>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/ballot-access.html", "Ballot access for libertarian and third parties", "How parties qualify for the ballot, how petition requirements vary, and how to plan petition season.",
         "Ballot access", body, crumbs=OC + [("Ballot access", "")], wide=False)


def messaging():
    body = """
<p>This page is the messaging core of <a href="../book.html">The Asymmetric Libertarian</a>. The short version: <b>libertarians speak in truth, and voters respond to lived experience.</b> Being right isn't the same as being heard.</p>
<h2>The 10-second test</h2>
<p>If a voter can't understand your point in ten seconds, it doesn't exist for them. Not "can they understand it after the third paragraph." Ten seconds.</p>
<h2>The one-sentence rule</h2>
<p>Every issue gets one sentence that a tired person can repeat to their spouse. If you need two, you haven't figured out what you're saying yet.</p>
<h2>The structure</h2>
<ol class="facts">
<li><b>Name the problem.</b> One real thing, in plain words.</li>
<li><b>Show the pain.</b> In time, cost or risk. How long it takes, what it costs, what happens if you mess up.</li>
<li><b>Give the fix.</b> One specific change someone could actually make.</li>
</ol>
<h2>The four questions every voter is really asking</h2>
<ul class="facts">
<li>How long will this take?</li>
<li>How much will it cost me?</li>
<li>What happens if I mess up?</li>
<li>Can I figure it out without hiring help?</li>
</ul>
<p>The book's legibility test is the last one: if a normal person needs a lawyer to open a door, they're not free.</p>
<h2>The four kinds of message</h2>
<ul class="facts">
<li><b>Pain relief:</b> "Start your business in 30 days, or it's automatically approved."</li>
<li><b>Risk reduction:</b> "One paperwork mistake shouldn't cost you your license."</li>
<li><b>Access expansion:</b> "If another state says you're qualified, you can work here immediately."</li>
<li><b>Control exposure:</b> "Governments have taken at least $82 billion through forfeiture since 2000, and where the data exists, nearly half the time nobody was convicted."</li>
</ul>
<h2>Before and after</h2>
<div class="tablewrap"><table><caption>The same idea, said two ways</caption><thead><tr><th scope="col">Says it like a libertarian</th><th scope="col">Says it like a neighbor</th></tr></thead><tbody>
<tr><td>Occupational licensing is a rent-seeking barrier to entry.</td><td>It takes a year of classes to braid hair here. That's a year you can't earn a living.</td></tr>
<tr><td>Civil asset forfeiture violates due process.</td><td>Police can keep your cash without charging you with anything.</td></tr>
<tr><td>Zoning distorts the housing market.</td><td>You can't build a small house for your mom on your own lot. That's why rent is high.</td></tr>
<tr><td>Taxation is theft.</td><td>How many weeks did you work this year just to pay your taxes? What did you get for it?</td></tr>
</tbody></table></div>
<p><b>Clear beats clever. Every time.</b></p>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/messaging.html", "Libertarian messaging that lands in 10 seconds", "The 10-second test, the one-sentence rule, problem-pain-fix, the four voter questions and four kinds of message, from The Asymmetric Libertarian.",
         "Messages that land", body, crumbs=OC + [("Messaging", "")], wide=False)


def steal():
    rows = [
        ("Fill every precinct seat", "Both parties are built from precinct and county committees, and those seats can fill vacant offices.", "structure.html"),
        ("One signature dinner a year", "County Lincoln Day and state Jefferson-Jackson style dinners are often a party's biggest fundraiser.", "../fundraise/events.html"),
        ("A cheap event beside the pricey one", "Clyburn's fish fry started for people who couldn't afford the big dinner, and became the bigger draw.", "../fundraise/events.html"),
        ("One-click recurring giving", "ActBlue and WinRed made giving $10 a month as easy as liking a post.", "../fundraise/small-dollar.html"),
        ("A shared voter file", "VAN and GOP Data Center give every county the same list and tools.", "field.html"),
        ("Candidate schools", "Leadership Institute, Run for Something and Emerge recruit and train at scale.", "candidates.html"),
        ("Relational organizing", "Paying and training people to reach their own friends and family.", "field.html"),
    ]
    tr = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td><a href="{h}">How to copy it</a></td></tr>' for a, b, h in rows)
    body = f"""
<p>Libertarians love to say both parties are the same. On organizing, they're not the same as us: they're better. Steal everything that works and leave the rest.</p>
<div class="tablewrap"><table><caption>What works, and where to learn to copy it</caption><thead><tr><th scope="col">The move</th><th scope="col">Who does it and how</th><th scope="col">Copy it</th></tr></thead><tbody>{tr}</tbody></table></div>
<h2>What not to steal</h2>
<ul class="facts">
<li><b>Pay-to-play.</b> A $15,000 sponsor table buys access. We'd rather it bought a petition drive.</li>
<li><b>Running everything from the top.</b> Our advantage is that nobody's waiting for permission. Keep it that way.</li>
<li><b>Fundraising emails that scream.</b> "FINAL NOTICE" for a $5 ask burns trust. Tell people what the money did.</li>
</ul>
<p class="row"><a class="btn ghost" href="index.html">Back to the playbook</a></p>"""
    page("organize/steal-this.html", "What libertarians should steal from Republicans and Democrats", "The organizing and fundraising moves the major parties use that work, and how a libertarian group can copy them.",
         "Steal from the big parties", body, crumbs=OC + [("Steal this", "")], wide=False)


def fund_index():
    cards = [
        ("events.html", "people", "Events and dinners", "The ticket ladder, the cheap alternative and the signature event."),
        ("small-dollar.html", "coins", "Small-dollar and recurring", "One page, monthly by default, thank people within a day."),
        ("models.html", "browser", "Models we built", "Directories, charity partners and campaigns from our own sites."),
        ("rules.html", "scroll", "The rules", "Treasurers, FEC thresholds and why your state's rules come first."),
    ]
    ch = "".join(f'<a class="card cardlink" href="{h}">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for h, i, t, d in cards)
    body = f"""
<h2>How the money works</h2>
<div class="grid">
<div class="card"><h3>We don't take donations</h3><p>There's no donate button on this site and there won't be one until we've said exactly where the money goes. Right now, Libertarian Enough runs on volunteer time.</p></div>
<div class="card"><h3>We don't hand out money</h3><p>No national pot, no pass-through. Money raised in Ohio should be spent by Ohioans, and the same goes for every other state.</p></div>
<div class="card"><h3>We give states the tools</h3><p>Playbooks, templates, event kits and free websites, so each state affiliate can raise its own money, under its own state's rules, from its own people.</p></div>
</div>
<h2>What's coming</h2>
<ul class="facts">
<li>Event kits: a dinner and a cheap cookout, with ticket ladders, run-of-show and sponsor sheets.</li>
<li>Donate pages built into the <a href="../free-sites.html">free websites</a>, pointing at each group's own processor.</li>
<li>A state-by-state sheet of the basic fundraising rules, starting with the states that ask first.</li>
</ul>
<h2>The playbook</h2>
<div class="grid">{ch}</div>
<h2>The one-sentence version</h2>
<p>Ask often, ask small, ask monthly, say exactly what the money will do, then show that it did it. Every party that raises real money does those five things. Most libertarian groups do none of them.</p>
"""
    page("fundraise/index.html", "How libertarian state affiliates can raise money", "How the money works at Libertarian Enough, and a fundraising playbook for state and county libertarian groups.",
         "Raise money in your own state", body, kicker="The fundraising playbook", lead="We don't take your money or hand it out. We show state affiliates how to raise their own.",
         crumbs=[("Fundraise", "")])


def events():
    body = f"""
<p>Every major party has a signature dinner. Most libertarian groups have a meetup at a brewery where everyone pays for their own beer. Here's what the big events look like, and how to run a version that fits a small group.</p>
<h2>How the big parties do it</h2>
{pts("dinners")}
<h2>Run your own: two events a year</h2>
<h3>The dinner (spring)</h3>
<ul class="facts">
<li><b>Build a ladder, not a price.</b> A single ticket, a table of ten at a small discount, and two or three sponsor levels with clear perks: a reception before, a program ad, a name on the table.</li>
<li><b>Get one draw.</b> A speaker people will drive an hour to see. It doesn't have to be famous. It has to be interesting.</li>
<li><b>Sell tables, not seats.</b> Ten table captains who each fill a table is easier than 100 strangers.</li>
<li><b>Say what it pays for.</b> "This dinner pays for the petition drive" beats "support liberty."</li>
</ul>
<h3>The cookout (fall)</h3>
<ul class="facts">
<li><b>Cheap or free to get in.</b> The fish fry lesson: the cheap event beside the pricey one often becomes the bigger draw.</li>
<li><b>Make it the place candidates show up.</b> Invite everyone on the ballot in your county, any party. Libertarians hosting the event everyone attends is a power move.</li>
<li><b>Collect names, not just money.</b> Every guest leaves on your list. That list is the next year's dinner.</li>
</ul>
<p class="row"><a class="btn ghost" href="index.html">Back to fundraising</a></p>"""
    page("fundraise/events.html", "Fundraising dinners and events for libertarian groups", "How party dinners and signature events raise money, and how a small libertarian affiliate can run a dinner and a cookout.",
         "Events and dinners", body, crumbs=FC + [("Events", "")], wide=False)


def small_dollar():
    body = f"""
<p>Small-dollar online giving is how modern campaigns pay the bills. The two big parties each have a one-click platform. Libertarians mostly have a PayPal link from 2014.</p>
<h2>How the big parties do it</h2>
{pts("small-dollar")}
<h2>The small-dollar setup</h2>
<ol class="facts">
<li><b>One donate page.</b> On your own site, on a processor that handles political or nonprofit giving the way your state requires. One link, everywhere.</li>
<li><b>Monthly by default.</b> A $10 monthly gift is $120 a year from someone who'd have given $25 once.</li>
<li><b>Ask with a reason and a number.</b> "We need $1,200 for petition printing by June 1" beats "please donate."</li>
<li><b>Show a progress bar.</b> People give to finish things.</li>
<li><b>Thank within a day.</b> A real note from a real person. Then, a month later, show what the money did.</li>
<li><b>Ask your list monthly.</b> Not daily. Not in all caps.</li>
</ol>
<p class="row"><a class="btn ghost" href="index.html">Back to fundraising</a></p>"""
    page("fundraise/small-dollar.html", "Small-dollar and recurring giving for libertarian groups", "How ActBlue and WinRed changed small-dollar fundraising, and a simple recurring-giving setup for libertarian affiliates.",
         "Small-dollar and recurring", body, crumbs=FC + [("Small-dollar", "")], wide=False)


def models():
    body = f"""
<p>We build websites that people use every week, and those sites are how the causes behind them raise money. Here's what we've learned, so your state can copy it.</p>
<h2>Model 1: build something useful, and the audience follows</h2>
<p>{ext("https://findbingo.org", "Find Bingo")} and {ext("https://ohiobingo.org", "Ohio Bingo")} list bingo games so players can find one tonight. {ext("https://the-reefer.com", "The Reefer")} and {ext("https://ohioweed.org", "OhioWeed.org")} answer what cannabis law allows, state by state. None of them ask for anything up front. They're useful, so people come back, and an audience that trusts you is the start of every donor list.</p>
<p><b>Copy it:</b> pick a question people in your state ask every week and nobody answers well. Where can I find a gun range? Which licenses does my trade need? What did my county commission vote on? Build the answer. We'll <a href="../free-sites.html">build the site free</a>.</p>
<h2>Model 2: free for everyone, with a way to give back</h2>
<p>The bingo sites run on a simple deal: listings are free for every hall, halls that want extra services can pay for them, and halls that want to can give back a share of their net proceeds. Nobody's locked out for not paying.</p>
<p><b>Copy it:</b> give the service away, offer paid extras to the people who want them, and make giving back to the cause easy and optional.</p>
<h2>Model 3: one goal, one deadline, one page</h2>
<p>The campaigns that work have one dollar goal, one date and one page, and every site you run links to that page from its footer until the date passes.</p>
<p><b>Copy it:</b> pick one number and one date, like a filing deadline or the end of a finance quarter, build one page on your own processor, and link it from everything you run.</p>
<h2>Bingo and raffles: partner with a charity</h2>
<p>Charity gaming is usually licensed to charities, not parties, so the move is to partner with one.</p>
{pts("charity-gaming")}
<p class="row"><a class="btn ghost" href="index.html">Back to fundraising</a></p>"""
    page("fundraise/models.html", "Fundraising models we built", "How useful directory sites, free listings with optional giving, and one-goal campaigns raise money, from the sites behind Libertarian Enough.",
         "Models we built", body, crumbs=FC + [("Models", "")], wide=False)


def rules():
    body = f"""
<p>The fastest way to kill a small party is a campaign-finance mess. The rules aren't hard, but they're real, and the first one is that you need a treasurer before you raise a dollar.</p>
<h2>The basics</h2>
{pts("finance-rules")}
<h2>The checklist</h2>
<ol class="facts">
<li>Name a treasurer and an assistant treasurer.</li>
<li>Open a bank account in the committee's name. Never mix it with anyone's personal money.</li>
<li>Find your state's campaign-finance office (usually the secretary of state or an ethics or elections commission) and read its guide for party committees.</li>
<li>Track every dollar in and out, with names and addresses for donors, from day one.</li>
<li>Calendar every filing deadline for the year in January.</li>
<li>If you'll touch federal races, read the FEC's party guide before you spend a cent on them.</li>
</ol>
<p class="row"><a class="btn ghost" href="index.html">Back to fundraising</a></p>"""
    page("fundraise/rules.html", "Campaign finance basics for small party affiliates", "Treasurers, FEC registration thresholds for state and local parties, and why state law comes first.",
         "The rules", body, crumbs=FC + [("Rules", "")], wide=False)
