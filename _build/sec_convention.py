"""The national convention, decoded: rules, numbers, motions, people, and what went wrong before.
Every number comes from the LP's 2024 bylaws and convention rules, its 2024 manuals, official minutes, or news coverage,
gathered in /mnt/project-files/libertarianenough-research/convention.json (checked November 27, 2026)."""
from core import page, e, ic, ext, sources

CC = [("Convention guide", "convention/index.html")]

BYL = "https://lp.org/wp-content/uploads/2024/10/2024-Indexed-LP-Bylaws-and-Convention-Rules-w-2022-JC-Rules-1.pdf"
BYLW = "https://lpedia.org/wiki/Document:National_Bylaws_and_Convention_Rules_2024_with_2022_Judicial_Rules"
DM = "https://lpedia.org/w/images/0/0e/Delegate_Manual_2024_.pdf"
DCM = "https://lpedia.org/w/images/1/1a/Delegation_Chair_Manual_2024.pdf"
SECM = "https://lpedia.org/w/images/7/72/Secretary-Manual_2024-08-19.pdf"
AFT = "https://www.aft.org/sites/default/files/media/2022/parliamentary_motions_guide_12th_edition.pdf"
RRA = "https://robertsrules.com/frequently-asked-questions/"
M18 = "https://lp.org/wp-content/uploads/2024/10/2018_Convention_Minutes.pdf"
M20 = "https://lp.org/wp-content/uploads/2024/10/CONVENTION-MINUTES_2020_FINAL.pdf"
W24 = "https://en.wikipedia.org/wiki/2024_Libertarian_National_Convention"
BP24 = "https://ballotpedia.org/Libertarian_Party_presidential_nomination,_2024"
JOUR = "https://lpnc.org/lp_national_2024_convention_journal"
SAR = "https://nsarwark.substack.com/p/dispatch-from-dc-on-day-3"
BAN = "https://ballot-access.org/?p=86580"
NBC = "https://www.nbcnews.com/politics/2024-election/trump-doesnt-submit-paperwork-libertarian-party-nomination-soliciting-rcna154132"
R24 = "https://reason.com/2024/06/25/how-the-libertarian-party-lost-its-way/"
R22 = "https://reason.com/2022/05/29/mises-caucus-takes-control-of-libertarian-party/printer/"
WLNC = "https://en.wikipedia.org/wiki/Libertarian_National_Convention"
WLP = "https://en.wikipedia.org/wiki/Libertarian_Party_(United_States)"
W26 = "https://en.wikipedia.org/wiki/2026_Libertarian_National_Convention"
W26C = "https://en.wikipedia.org/wiki/2026_Libertarian_National_Committee_chair_election"
R26 = "https://reason.com/2026/05/29/the-libertarian-partys-new-leader-has-no-interest-in-playing-kingmaker/"
NHPR = "https://www.nhpr.org/nh-news/2026-05-28/nh-libertarians-newhampshire-ejected-party-jeremy-kauffman"
BR = "https://lp.org/wp-content/uploads/Bylaws_Report.pdf"
LPO = "https://lpo.org/understanding-delegate-eligibility-for-the-2026-libertarian-national-convention/"

BACK = '<p class="row"><a class="btn ghost" href="index.html">Back to the convention guide</a></p>'

CAVEAT = (f'<div class="warn"><p><b>These are the 2024 rules.</b> The 2026 convention in Grand Rapids voted on 22 bylaws changes, including ranked-choice voting '
          f'for officers, electronic ballots, 20 delegates to second a floor motion, and no more signature tokens for presidential nominations. '
          f'We couldn\'t confirm which passed. Before 2028, check the bylaws as amended in 2026. {sources([BR])}</p></div>')


def build():
    index(); motions(); people(); record()


# ---------- charts ----------

def stack_svg(uid="rb"):
    """Three rulebooks, top one wins. Drawn as stacked slabs, widest at the bottom."""
    rows = [("1. The bylaws", "Wins every conflict. Changing them takes 2/3.", 560, "#1f2a44", "#fff"),
            ("2. The convention rules", "Order of business, voting, time limits, tokens, nominations.", 640, "#3b4a6b", "#fff"),
            ("3. Robert's Rules of Order, 12th edition", "Everything the first two don't cover.", 720, "#f5c400", "#1a1a1a")]
    g = []
    for i, (t, s, w, fill, ink) in enumerate(rows):
        x = (760 - w) / 2
        y = 10 + i * 78
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="68" rx="10" fill="{fill}" stroke="#1a1a1a" stroke-width="1.5"/>'
                 f'<text x="380" y="{y + 30}" font-size="19" font-weight="800" text-anchor="middle" fill="{ink}">{e(t)}</text>'
                 f'<text x="380" y="{y + 54}" font-size="15" text-anchor="middle" fill="{ink}">{e(s)}</text>')
    return (f'<svg viewBox="0 0 760 248" role="img" aria-labelledby="{uid}t {uid}d"><title id="{uid}t">The three rulebooks, in order of authority</title>'
            f'<desc id="{uid}d">First the party bylaws, which win every conflict. Second the convention\'s special rules. Third Robert\'s Rules of Order '
            f'Newly Revised, 12th edition, which covers everything else.</desc>' + "".join(g) + '</svg>')


def bar_svg(rows, title, desc, uid, maxv, fmt=lambda v: f"{v:,}", lw=300, marks=()):
    """Horizontal bars, one series. rows: (label, value, fill, note). marks: (value, label) dashed reference lines."""
    X0, X1, rh, top = lw + 12, 800, 52, 14
    h = top + len(rows) * rh + (30 if marks else 6)

    def X(v):
        return round(X0 + v / maxv * (X1 - X0 - 70), 1)
    g = []
    for i, (lab, v, fill, note) in enumerate(rows):
        y = top + i * rh
        g.append(f'<text x="{lw}" y="{y + 22}" font-size="15" font-weight="700" text-anchor="end" fill="#1a1a1a">{e(lab)}</text>')
        if note:
            g.append(f'<text x="{lw}" y="{y + 40}" font-size="13" text-anchor="end" fill="#4a4a4a">{e(note)}</text>')
        g.append(f'<rect x="{X0}" y="{y + 6}" width="{X(v) - X0}" height="28" rx="4" fill="{fill}"><title>{e(lab)}: {fmt(v)}</title></rect>'
                 f'<text x="{X(v) + 8}" y="{y + 26}" font-size="16" font-weight="800" fill="#1a1a1a">{fmt(v)}</text>')
    for v, lab in marks:
        g.append(f'<path d="M{X(v)} {top - 4}V{top + len(rows) * rh}" stroke="#1a1a1a" stroke-width="2" stroke-dasharray="5 4" opacity=".6"/>'
                 f'<text x="{X(v)}" y="{top + len(rows) * rh + 20}" font-size="13" text-anchor="middle" fill="#4a4a4a">{e(lab)}</text>')
    return (f'<svg viewBox="0 0 820 {h}" role="img" aria-labelledby="{uid}t {uid}d"><title id="{uid}t">{e(title)}</title>'
            f'<desc id="{uid}d">{e(desc)}</desc>' + "".join(g) + '</svg>')


def thresholds_fig():
    rows = [("Majority", 50, "#8f9bb8", "main motions, deleting a plank, officers"),
            ("Two-thirds", 66.7, "#3b4a6b", "bylaws, new planks, ending debate"),
            ("Three-quarters", 75, "#1f2a44", "overriding a Judicial Committee veto"),
            ("Seven-eighths", 87.5, "#a4161a", "the Principles, of all registered")]
    svg = bar_svg(rows, "Yes votes needed, by kind of question", "Bar chart. A majority means more than half of those voting: main motions, deleting a platform plank and electing officers. "
                  "Two-thirds of those voting: bylaws, adding or amending planks, resolutions, suspending the rules and ending debate. Three-quarters: overriding a Judicial "
                  "Committee veto. Seven-eighths of all registered delegates, not just those voting: amending the Statement of Principles.",
                  "thr", 100, fmt=lambda v: {50: "over 1/2", 66.7: "2/3", 75: "3/4", 87.5: "7/8"}[v])
    return (f'<figure class="fig"><figcaption><b>Know the number before you vote.</b> Most questions are decided by those present and voting, so abstaining doesn\'t count as a no. '
            f'The Statement of Principles is the exception: it takes 7/8 of every registered delegate.</figcaption><div class="figsvg">{svg}</div>'
            f'<p class="src">Bylaws Art. 3 and 17, Convention Rules 4 to 6. {sources([BYL, DM])}</p></figure>')


def seveneighths_fig():
    rows = [("Delegates registered", 1051, "#8f9bb8", "2024, Washington"),
            ("Yes votes to change the Principles", 920, "#a4161a", "7/8 of 1,051"),
            ("Most ballots cast on anything", 919, "#1f2a44", "first presidential ballot")]
    svg = bar_svg(rows, "Why the Statement of Principles almost can't change", "Bar chart using 2024 numbers. 1,051 delegates registered. Changing the Statement of "
                  "Principles would have needed 920 yes votes. The most ballots cast on any vote was 919, on the first presidential ballot.", "sev", 1100)
    return (f'<figure class="fig"><figcaption><b>920 is more than 919.</b> In 2024, changing the Statement of Principles needed more yes votes than the convention ever '
            f'cast on anything, including picking a presidential nominee.</figcaption><div class="figsvg">{svg}</div>'
            f'<p class="src">{sources([BYL, W24, BP24])}</p></figure>')


# ---------- pages ----------

def stats():
    tiles = [("40%", "of registered delegates is a quorum", "Recounted as people register. It gets challenged."),
             ("20", "delegates force a counted vote", "After a standing vote, if 20 object to the chair's call."),
             ("30", "delegate tokens to nominate for president or VP", "15 for an at-large seat. One nominee per office per delegate."),
             ("5", "platform deletion tokens each", "A plank hit by 20% of delegates gets a deletion vote first, with no debate."),
             ("10%", "of delegates can challenge a plank", "Or a resolution, to the Judicial Committee, in writing, during the convention."),
             ("2", "levels of amendment, max", "An amendment, and an amendment to that. A third is out of order.")]
    lis = "".join(f'<li><span class="fn">{n}</span><span class="ft">{e(t)}</span><span class="how">{e(h)}</span></li>' for n, t, h in tiles)
    return f'<ul class="tiles">{lis}</ul><p class="src">Bylaws Art. 10, Convention Rules 2, 5, 7 and 8, and Robert\'s Rules. {sources([BYL, DM, AFT])}</p>'


def index():
    order = ["Call to order", "Credentials report", "Adopt the agenda", "Treasurer's report", "Audit report", "Bylaws and rules",
             "Judicial Committee (non-presidential years)", "Officers and at-large seats", "Platform", "President and VP (presidential years)",
             "Resolutions", "Other business"]
    ol = "".join(f'<li><span class="stepnum">{i}</span><span>{e(t)}</span></li>' for i, t in enumerate(order, 1))
    fails = [
        ("Not being on the list.", "Your state sends its delegate list a month before the convention. No list, no delegation. Confirm you're on it before you buy a plane ticket."),
        ("Leaving early.", "In 2024 ballots cast fell from 919 to 820 over seven presidential ballots, and the VP race was decided with 723 votes out of 1,051. Your state's votes leave with you."),
        ("Sitting with your friends.", "Ballots go through your delegation chair. Sit with your delegation or your vote gets lost in the shuffle."),
        ("Spoiling your ballot.", "Mark a candidate and None of the Above on the same ballot and it doesn't count."),
        ("Shouting \"Question!\"", "It does nothing. To end debate you get recognized at a microphone and move the previous question, which takes 2/3."),
        ("Using \"point of information\" to give a speech.", "It's now called a request for information, and it has to be a question."),
        ("Abusing point of order and personal privilege to cut the mic line.", "The manuals name this one. The room notices, and it costs you every vote you'll need later."),
        ("Appealing every ruling.", "In 2020 delegates appealed the chair at least nine times. The chair won all but one."),
        ("Motion to suspend the rules, again.", "It takes 2/3 and usually fails. Each try burns clock that real business needed."),
        ("Thinking abstaining is a no.", "Thresholds count those present and voting. Not voting just removes you. The Statement of Principles is the one exception."),
        ("Not reading the reports.", "Bylaws and platform proposals get 2 minutes of explanation. If you're reading them for the first time on the floor, you're voting blind."),
        ("Adjourning carelessly.", "A 2018 adjournment left the party with no Judicial Committee until the next convention. A motion that ends the convention is debatable. Debate it."),
    ]
    fl = "".join(f'<li><b>{e(t)}</b> {e(d)}</li>' for t, d in fails)
    pages = [("motions.html", "gavel", "Make a motion, appeal the chair", "What to say at the mic, the 23 motions you'll hear, and which ones outrank which."),
             ("people.html", "people", "Who runs the room", "The chair, the parliamentarian, the committees, the tellers, and how your ballot gets counted."),
             ("record.html", "chart", "What went wrong before", "Five conventions, 2018 to 2026: the numbers, the fights, and what a delegate should take from each.")]
    cards = "".join(f'<a class="card cardlink" href="{h}">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for h, i, t, d in pages)
    body = f"""
<p class="lead">A national convention isn't chaos. It's a structure most delegates were never shown. The 50 people who know the rules run the floor, and everyone else votes on whatever reaches them. This guide is the rules, the numbers and the people, so you walk in as one of the 50.</p>

<h2>In this guide</h2>
<div class="grid">{cards}</div>

<h2>Three rulebooks, one order</h2>
<p>Everything on the floor is decided by three documents, and when they disagree the higher one wins. The party bylaws can't be suspended. The convention rules can, by 2/3. Robert's Rules fills every gap.</p>
<figure class="fig"><div class="figsvg">{stack_svg()}</div><p class="src">Bylaws Art. 16 adopts "the current edition" of Robert's Rules, which is the 12th, from 2020. {sources([BYL, RRA, DCM])}</p></figure>

<h2>The numbers that run the floor</h2>
{stats()}
<div class="figs">{thresholds_fig()}{seveneighths_fig()}</div>

<h2>How you become a delegate</h2>
<ol class="steps">
<li><span class="stepnum">1</span><div class="card"><h3>Be a member</h3><p>Delegates must be members of the national party or a state affiliate. Your state sets its own bar. Ohio's for 2026: an Ohio resident who's a Supporting member ($25) or Lifetime member, who signs the pledge and applies by the state's deadline, which was February 10, 2026. {sources([BYL, LPO])}</p></div></li>
<li><span class="stepnum">2</span><div class="card"><h3>Your state gets its seats</h3><p>One delegate for every 0.14% of national sustaining members who live in your state, plus one for every 0.35% of the Libertarian presidential vote your state cast. Members are counted seven months before the convention, and the national secretary tells states their numbers a month after that. Grow your state's membership and you grow its voice. {sources([BYL, SECM])}</p></div></li>
<li><span class="stepnum">3</span><div class="card"><h3>Get on the list</h3><p>Your state picks its delegates under its own rules and sends the list to the Credentials Committee a month before the convention. Alternates are capped at 50 or your state's delegate count, whichever is bigger. Alternates are seated by lot unless your state ranks them. {sources([BYL, DCM])}</p></div></li>
<li><span class="stepnum">4</span><div class="card"><h3>Credential when you arrive</h3><p>Registration gets you a badge. Credentialing gets you a vote and your tokens. If you're only there for part of the weekend, credential when you arrive, not before, so you don't inflate the quorum count. {sources([DM])}</p></div></li>
<li><span class="stepnum">5</span><div class="card"><h3>Sit with your delegation and stay</h3><p>Your state chair runs your delegation unless the delegation picks someone else. Ballots go through them. Unit voting is banned: every delegate votes their own ballot. {sources([BYL, DCM])}</p></div></li>
</ol>

<h2>The order of business</h2>
<p>This is the standing agenda. Delegates regularly try to suspend the rules to move things around. It takes 2/3 and usually fails.</p>
<ol class="steps mini">{ol}</ol>
<p class="src">Convention Rule 1. {sources([BYL, M18])}</p>

<h2>Where people fail</h2>
<p>Most of this list comes from the party's own 2024 delegate manuals. The rest comes from the minutes.</p>
<ol class="facts">{fl}</ol>
<p class="src">{sources([DM, DCM, M20, W24, M18])}</p>

<h2>Before you go</h2>
<ul class="checks">
<li><b>Read the bylaws and convention rules.</b> They're one PDF. {sources([BYL])}</li>
<li><b>Read the committee reports</b> the week they come out. Bylaws and platform proposals get 2 minutes of explanation on the floor.</li>
<li><b>Bring a copy of Robert's Rules In Brief.</b> The party's manual recommends it, and it fits in a bag.</li>
<li><b>Book through the last day.</b> In 2024 the convention ran to about 1:30 a.m. Monday. {sources([JOUR])}</li>
<li><b>Know who you agree with.</b> Close votes are won by blocs that hold together across ballots. See <a href="record.html#chair2026">the 2026 chair race</a>.</li>
</ul>

{CAVEAT}
"""
    page("convention/index.html", "The national convention, decoded", "A delegate's guide to the Libertarian national convention: the three rulebooks, vote thresholds, quorum, tokens, how to become a delegate, and the mistakes first-timers make.",
         "Walk into the national convention knowing what's going on", body, kicker="The convention guide", crumbs=[("Convention guide", "")])


SAY = [
    ("Bring up something new", "Chair, Jane Smith, delegate from Ohio. I move that…", "Needs a second. Majority, except bylaws, new planks and resolutions, which take 2/3."),
    ("Change the wording", "I move to amend by striking “…” and inserting “…”.", "Needs a second. Majority, even when the motion itself needs 2/3. Two levels of amendment, max."),
    ("End debate and vote now", "I move the previous question.", "Needs a second. No debate. Takes 2/3. Shouting “Question!” from your seat does nothing."),
    ("The chair broke a rule", "Point of order!", "You can say it from your seat and interrupt. No second. The chair rules. Raise it when it happens or it's too late, unless it breaks the bylaws."),
    ("You think the chair ruled wrong", "I appeal from the decision of the chair.", "Right after the ruling. Needs a second. A majority against the chair overturns it. A tie keeps the ruling."),
    ("You doubt a voice vote", "Division!", "From your seat. Forces a standing vote. If 20 delegates object to the chair's call on that, it gets counted."),
    ("You don't know how to do something", "Parliamentary inquiry: how would I…?", "The chair answers. No vote. This is the one nobody uses and everybody should."),
    ("You need a fact", "Request for information: does this amendment change…?", "It has to be a question. If a speaker yields to answer, it comes out of their time."),
    ("Take something out of order", "I move to suspend the rules and take up…", "Needs a second. No debate. Takes 2/3. Can't suspend the bylaws. Usually fails."),
    ("Kill it without a straight vote", "I move to postpone indefinitely.", "Needs a second. Debatable, including the main motion's merits. Majority."),
    ("Redo a vote", "I move to reconsider the vote on…", "Only if you voted on the winning side, the same day or the next business day. Majority."),
    ("Get back on schedule", "I call for the orders of the day.", "One person can demand it. Setting the schedule aside takes 2/3."),
]

LADDER = ["Adjourn", "Recess", "Raise a question of privilege", "Call for the orders of the day", "Lay on the table", "Previous question (end debate)",
          "Limit or extend debate", "Postpone to a certain time", "Refer to a committee", "Amend", "Postpone indefinitely", "Main motion"]

MOTIONS = [
    ("Main motion", "Brings new business.", "No", "Yes", "Yes", "Yes", "Majority (2/3 for bylaws, new planks, resolutions)"),
    ("Amend", "Changes a pending motion's wording. Must be on topic.", "No", "Yes", "Yes", "Yes, one level", "Majority"),
    ("Previous question", "Ends debate and amendments. Forces the vote.", "No", "Yes", "No", "No", "2/3"),
    ("Limit or extend debate", "Changes speaking time.", "No", "Yes", "No", "Yes", "2/3"),
    ("Lay on the table", "Sets a question aside for something urgent. Using it to kill a motion is improper.", "No", "Yes", "No", "No", "Majority"),
    ("Take from the table", "Brings a tabled question back.", "No", "Yes", "No", "No", "Majority"),
    ("Postpone to a certain time", "Moves the question later.", "No", "Yes", "Yes", "Yes", "Majority"),
    ("Postpone indefinitely", "Kills the main motion without a direct vote.", "No", "Yes", "Yes", "No", "Majority"),
    ("Refer to a committee", "Sends the question to a committee.", "No", "Yes", "Only whether to refer", "Yes", "Majority"),
    ("Point of order", "Flags a rules violation. The chair rules.", "Yes", "No", "No", "No", "Chair rules"),
    ("Appeal the chair", "Asks the delegates to overrule the chair. Only at the time of the ruling.", "Yes", "Yes", "Usually", "No", "Majority against the chair reverses; a tie sustains"),
    ("Parliamentary inquiry", "Asks how the rules work.", "If urgent", "No", "No", "No", "Chair answers"),
    ("Request for information", "Asks a factual question. Must be a question.", "If urgent", "No", "No", "No", "None"),
    ("Division of the assembly", "Demands a standing vote. 20 objecting delegates force a count.", "Yes", "No", "No", "No", "None"),
    ("Division of a question", "Splits a motion into separate votes.", "No", "Yes", "No", "Yes", "Majority"),
    ("Suspend the rules", "Lets the convention break its own rules for one item. Never the bylaws.", "No", "Yes", "No", "No", "2/3"),
    ("Objection to consideration", "Blocks a main motion before debate starts.", "Yes", "No", "No", "No", "2/3 against considering it"),
    ("Reconsider", "Revotes something from the same or previous day. Winning side only.", "Can be made, not taken up", "Yes", "If the original was", "No", "Majority"),
    ("Rescind or amend something adopted", "Repeals or changes an earlier decision.", "No", "Yes", "Yes", "Yes", "Majority with notice; 2/3 without"),
    ("Recess", "A short break.", "No", "Yes", "No", "Length only", "Majority"),
    ("Adjourn", "Ends the meeting. Ending the whole convention is debatable.", "No", "Yes", "No", "No", "Majority"),
    ("Orders of the day", "Demands a return to the agenda.", "Yes", "No", "No", "No", "None (2/3 to set aside)"),
    ("Question of privilege", "An urgent comfort or rights issue: can't hear, too hot. Not for jumping the mic line.", "Yes", "No", "No", "No", "Chair rules"),
]


def motions():
    cards = "".join(f'<div class="card say"><h3>{e(g)}</h3><p class="line">{e(s)}</p><p>{e(n)}</p></div>' for g, s, n in SAY)
    lad = "".join(f'<li><span class="stepnum">{len(LADDER) - i}</span><span>{e(t)}</span></li>' for i, t in enumerate(LADDER))
    rows = "".join(f'<tr><th scope="row">{e(n)}</th><td>{e(w)}</td><td>{e(i)}</td><td>{e(s)}</td><td>{e(d)}</td><td>{e(a)}</td><td>{e(v)}</td></tr>' for n, w, i, s, d, a, v in MOTIONS)
    body = f"""
<p class="lead">You don't need to memorize Robert's Rules. You need about a dozen sentences, the order motions outrank each other, and the nerve to walk to a microphone.</p>

<h2>How a motion moves</h2>
<ol class="steps">
<li><span class="stepnum">1</span><div class="card"><h3>Get the floor</h3><p>Go to a floor microphone and wait to be recognized. Microphones are marked pro, con, or other. Start with your name and state: "Chair, Jane Smith, delegate from Ohio." Only urgent calls, like "Point of order!" or "Division!", come from your seat. {sources([DM])}</p></div></li>
<li><span class="stepnum">2</span><div class="card"><h3>Make the motion</h3><p>"I move that…" Say exactly what you want done, in one sentence. The chair can require it in writing, so have it written. {sources([BYL])}</p></div></li>
<li><span class="stepnum">3</span><div class="card"><h3>Someone seconds it</h3><p>A second only means one other delegate wants it discussed. No second, no motion. Line up your second before you walk to the mic.</p></div></li>
<li><span class="stepnum">4</span><div class="card"><h3>The chair states it</h3><p>Once the chair repeats it, it belongs to the convention, not you. You need permission to withdraw it.</p></div></li>
<li><span class="stepnum">5</span><div class="card"><h3>Debate, on a clock</h3><p>Speakers alternate for and against. Bylaws proposals get 2 minutes of explanation and 8 of debate. Platform proposals get 2 and 15. {sources([BYL])}</p></div></li>
<li><span class="stepnum">6</span><div class="card"><h3>The vote</h3><p>The chair takes a voice vote. Doubt it? "Division!" gets a standing vote, and if 20 delegates object to the chair's call on that, it's counted. {sources([BYL, DM])}</p></div></li>
</ol>
<p class="src">Steps follow Robert's Rules, 12th edition, as summarized in {ext(AFT, "Jim Slaughter's chart of motions")}.</p>

<h2>What to say</h2>
<p>Pick what you want to happen. Say the line. The note under it is what happens next.</p>
<div class="grid">{cards}</div>
<p class="src">{sources([AFT, BYL, DM, RRA])}</p>

<h2>What outranks what</h2>
<p>While a motion is on the floor, you can only make a motion that ranks higher. That's precedence. If someone moves to amend, you can move to end debate on it, but you can't bring up new business. Votes go from the top down: the highest-ranking pending motion gets decided first.</p>
<ol class="ladder">{lad}</ol>
<p>Point of order, appeal, inquiries, division and suspending the rules sit outside the ladder. They come up whenever they're needed and get handled right away.</p>
<p class="src">{sources([AFT])}</p>

<h2>Appealing the chair, step by step</h2>
<ol class="facts">
<li><b>Wait for a ruling.</b> You can only appeal a decision the chair actually made. If they haven't ruled, raise a point of order first and make them rule.</li>
<li><b>Appeal immediately.</b> "I appeal from the decision of the chair." If other business starts, you've lost it.</li>
<li><b>Get a second.</b> Have one ready.</li>
<li><b>The chair explains first and last.</b> Usually the appeal is debatable. It isn't when it's about decorum, the order of business, or a question that can't be debated.</li>
<li><b>The question is "Shall the decision of the chair stand?"</b> A majority voting no overturns it. A tie keeps it.</li>
<li><b>Expect to lose.</b> In 2020 delegates appealed at least nine times and won once, 550 to 353. Save it for a ruling that's clearly wrong, and talk to the parliamentarian at the head table first. {sources([M20])}</li>
</ol>
<p class="src">{sources([AFT])}</p>

<h2>When the chair counts wrong</h2>
<p>The party's own manual warns that chairs sometimes apply thresholds to everyone present instead of those present and voting. If a 2/3 vote is ruled failed and the yes votes were 2/3 of the votes actually cast, raise a point of order right then. {sources([DCM])}</p>

<h2>All 23 motions</h2>
<div class="tablewrap"><table><caption>Motions under Robert's Rules, 12th edition, with LP convention rules where they differ</caption>
<thead><tr><th scope="col">Motion</th><th scope="col">What it does</th><th scope="col">Interrupt a speaker?</th><th scope="col">Second?</th><th scope="col">Debatable?</th><th scope="col">Amendable?</th><th scope="col">Vote</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="src">{sources([AFT, BYL, DCM])}</p>
{CAVEAT}
{BACK}"""
    page("convention/motions.html", "How to make a motion and appeal the chair", "What to say at the microphone at a Libertarian national convention: making motions, points of order, appeals, division, and a table of all 23 motions under Robert's Rules.",
         "Make a motion, appeal the chair, and know what outranks what", body, crumbs=CC + [("Motions", "")])


def people():
    roles = [
        ("gavel", "The chair", "The national party chair presides. Recognizes speakers, rules on points of order, puts questions to a vote. Every ruling can be appealed."),
        ("book", "The parliamentarian", "Advises the chair on the rules. Doesn't rule. The bylaws don't create the job. Richard Brown served in 2020 and 2024. If you're about to appeal, ask the parliamentarian first."),
        ("scroll", "The secretary", "The national secretary takes the minutes, receives nominating tokens and delegation tallies, trains the tellers, declares voting closed, and owes draft minutes within 60 days."),
        ("stamp", "Credentials Committee", "10 members: 5 picked by the national committee, 5 from the five largest states. Decides who's seated and hands out tokens. Its report is the first fight of the weekend."),
        ("layers", "Bylaws and Rules Committee", "10 members appointed by the national committee a year out, no more than 5 of them national committee members. Writes the bylaws proposals."),
        ("map", "Platform Committee", "20 members: one from each of the five states with the most members per capita, one from each of the next 10 largest, and 5 picked by the national committee."),
        ("scales", "Judicial Committee", "7 members, elected only in non-presidential years. Nobody on the national committee. Four years of membership required. Reviews challenged planks and resolutions and can void national committee decisions."),
        ("ballot", "Tellers", "Volunteers trained by the secretary, usually 10 to 12 with a head teller. They sit apart from their own states, check every delegation's tally and cosign it."),
        ("flag", "Your delegation chair", "Your state chair, unless your delegation picks someone else. Collects your ballot, tallies the state, and turns in a signed sheet and sealed envelope."),
        ("fence", "Sergeant-at-arms", "Keeps order on the floor. The rules don't define the job, and in 2024 a delegate was reportedly removed during Friday's session."),
    ]
    cards = "".join(f'<div class="card">{ic(i)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in roles)
    flow = ["You mark a paper ballot", "Your delegation chair collects and tallies", "Signed tally and sealed envelope go to the tellers",
            "Tellers check and cosign", "The secretary closes voting and reports", "The chair announces the result"]
    fl = "".join(f'<li><span class="stepnum">{i}</span><span>{e(t)}</span></li>' for i, t in enumerate(flow, 1))
    body = f"""
<p class="lead">A convention is run by a few dozen people at the head table and on four committees, and by a delegation chair in every state. Know who does what and you know who to talk to before something goes wrong.</p>

<h2>The people</h2>
<div class="grid">{cards}</div>
<p class="src">Bylaws Art. 6, 8, 10 and 11, Convention Rules 3 and 10. {sources([BYL, SECM, DCM, DM, M20, JOUR])}</p>

<h2>The national committee</h2>
<p>Between conventions the party is run by the Libertarian National Committee: the four officers (chair, vice-chair, secretary, treasurer), five at-large members the convention elects, and regional representatives, one for every 10% of national members a state or region holds. The 2026 bylaws report proposed seven at-large seats and no regional representatives. When the chair resigned in January 2025, the national committee, not delegates, picked the replacement, 9 to 6. {sources([BYL, BR, "https://www.yahoo.com/news/libertarian-party-gets-national-chair-181551250.html"])}</p>

<h2>How your ballot gets counted</h2>
<ol class="steps mini">{fl}</ol>
<p>After the first presidential ballot, delegation chairs announce their state's totals out loud, alphabetically, from a randomly drawn starting state. In 2020 the first presidential ballot took about an hour and 20 minutes to count. {sources([DM, M20])}</p>

<h2>How elections work</h2>
<ul class="facts">
<li><b>President and VP:</b> 30 delegates must sign for a candidate with their tokens to get them nominated. Winning takes a majority. After each ballot, the last-place candidate and anyone under 5% are dropped. {sources([BYL])}</li>
<li><b>None of the Above</b> is always on the ballot. If it wins for president or VP, nobody is nominated. If it wins a party office, the office is vacant and the losers can't fill it. {sources([BYL, WLNC])}</li>
<li><b>Officers</b> need a majority. The last-place candidate drops each round. {sources([BYL])}</li>
<li><b>At-large and Judicial Committee seats:</b> vote for as many candidates as you like. The top finishers with a majority of ballots win. At-large nominations take 15 delegates. {sources([BYLW])}</li>
<li><b>Speeches are timed:</b> 16 minutes total of nominating and seconding speeches for president, 11 for VP, 10 for chair, 5 for other offices. {sources([BYL, DM])}</li>
</ul>
{CAVEAT}
{BACK}"""
    page("convention/people.html", "Who runs the national convention", "The chair, parliamentarian, secretary, tellers, committees and delegation chairs at a Libertarian national convention, and how your ballot is counted.",
         "Who runs the room", body, crumbs=CC + [("People", "")])


def chair26_fig():
    rounds = [("Round 1", [("Ostrowski", 195), ("McMahon", 187), ("Benedict", 125), ("Yates", 42), ("Kauffman", 31)]),
              ("Round 2", [("McMahon", 241), ("Ostrowski", 236), ("Benedict", 110)]),
              ("Round 3", [("McMahon", 320), ("Ostrowski", 265)])]
    X0, X1, rh = 130, 520, 34
    g, y = [], 8
    for name, cs in rounds:
        g.append(f'<text x="0" y="{y + 20}" font-size="17" font-weight="800" fill="#1a1a1a">{name}</text>')
        y += 30
        for c, v in cs:
            fill = "#f5c400" if c == "McMahon" else "#3b4a6b"
            w = round(v / 340 * (X1 - X0), 1)
            g.append(f'<text x="{X0 - 10}" y="{y + 20}" font-size="15" text-anchor="end" fill="#1a1a1a">{c}</text>'
                     f'<rect x="{X0}" y="{y + 5}" width="{w}" height="22" rx="4" fill="{fill}" stroke="#1a1a1a" stroke-width="{1 if fill == "#f5c400" else 0}"><title>{name}, {c}: {v}</title></rect>'
                     f'<text x="{X0 + w + 8}" y="{y + 22}" font-size="15" font-weight="800" fill="#1a1a1a">{v}</text>')
            y += rh
        y += 14
    svg = (f'<svg viewBox="0 0 600 {y}" role="img" aria-labelledby="c26t c26d"><title id="c26t">2026 national chair race, votes by round</title>'
           f'<desc id="c26d">Round 1: Ostrowski 195, McMahon 187, Benedict 125, Yates 42, Kauffman 31. Round 2: McMahon 241, Ostrowski 236, Benedict 110. '
           f'Round 3: McMahon 320, Ostrowski 265. McMahon won with 53.5 percent.</desc>' + "".join(g) + '</svg>')
    return (f'<figure class="fig" id="chair2026"><figcaption><b>The third-place candidate\'s voters picked the chair.</b> Ostrowski led round 1. When Benedict dropped after round 2, '
            f'McMahon gained 79 votes to Ostrowski\'s 29, net. That\'s coalition math: whoever can be everyone\'s second choice wins a multi-round election.</figcaption>'
            f'<div class="figsvg">{svg}</div><p class="src">Grand Rapids, May 2026. McMahon is shown in gold. {sources([W26C, W26, R26])}</p></figure>')


def attrition_fig():
    rows = [("Delegates", 1051, "#8f9bb8", ""), ("1st presidential ballot", 919, "#3b4a6b", ""),
            ("7th presidential ballot", 820, "#3b4a6b", "decided the nominee"), ("Deciding VP ballot", 723, "#a4161a", "about 1:30 a.m. Monday")]
    svg = bar_svg(rows, "2024: delegates versus votes cast", "Bar chart. 1,051 delegates. 919 votes cast on the first presidential ballot, 820 on the seventh, "
                  "which decided the nominee, and 723 on the deciding vice-presidential ballot.", "att", 1100, marks=((526, "526 = majority of all delegates"),))
    return (f'<figure class="fig"><figcaption><b>The people who stay decide.</b> By the deciding VP vote, nearly a third of the delegates didn\'t vote, and the winner got 371 votes, '
            f'fewer than half of the 1,051 seated.</figcaption><div class="figsvg">{svg}</div><p class="src">{sources([W24, BP24, JOUR])}</p></figure>')


def record():
    body = f"""
<p class="lead">The minutes tell you more than the speeches. Here's what happened at the last five conventions, with the numbers, and what a delegate should take from each.</p>

<div class="figs">{chair26_fig()}{attrition_fig()}</div>

<h2>2026, Grand Rapids</h2>
<p>May 21 to 25. Evan McMahon, Indiana's state chair, won national chair in the third round, 320 to Jim Ostrowski's 265, after trailing in round 1. The incumbent, Steven Nekhaila, didn't run. The New Hampshire affiliate was disaffiliated around the convention: NHPR reports a 15 to 2 national committee vote, and Reason describes it as a delegate vote. Delegates also took up 22 bylaws proposals. {sources([W26, W26C, R26, NHPR, BR])}</p>
<p><b>The lesson:</b> leading round 1 means nothing if nobody else's voters will come to you.</p>

<h2>2024, Washington</h2>
<p>1,051 delegates. The first three hours of Friday went to seating contested delegates from Michigan and Oklahoma; a Michigan court had ordered state officers to reinstate dropped delegates two days earlier, and delegates voted to seat them. Donald Trump spoke Saturday, asked for the nomination and was booed. He never filed nominating paperwork, so a floor nomination of him was ruled invalid. RFK Jr. was eliminated on the first ballot with 19 votes. Michael Rectenwald led the first five presidential ballots and lost. Chase Oliver won on the seventh, 497 to None of the Above's 300. Delegates suspended the rules to drop VP candidates under 15%. Angela McArdle was re-elected chair on the second ballot with 53%. {sources([W24, BP24, NBC, BAN, SAR, R24, JOUR])}</p>
<p><b>The lesson:</b> credentials fights eat the clock, and a first-ballot lead isn't a coalition. It was the first time since 2004 the first-ballot leader lost.</p>

<h2>2022, Reno</h2>
<p>The Mises Caucus took control. McArdle won chair on the first ballot with 692 votes, over 69%, and the caucus won the other top posts. The abortion plank was deleted from the platform, which takes only a majority. {sources([R22, WLNC, WLP])}</p>
<p><b>The lesson:</b> the faction that organized its delegates months ahead won everything on the first ballot. Deleting a plank takes half the room; writing one takes two-thirds.</p>

<h2>2020</h2>
<p>Jo Jorgensen won the presidential nomination on the fourth ballot with 524 of 1,026 votes, 51%. Delegates appealed the chair at least nine times and won once. Ending debate passed by margins like 819 to 78. Most motions to suspend the rules failed, including one to adopt a porcupine mascot, which lost 411 to 410. {sources([M20])}</p>
<p><b>The lesson:</b> the room backs the chair and wants to vote. Use procedure to move things, not to stall them.</p>

<h2>2018</h2>
<p>Registered delegates ran from 692 at the opening to about 813. Quorum was challenged at least twice and ruled present. The minutes are full of motions to suspend the rules, appeals, divisions and calls for the orders of the day. An adjournment error left the party with no Judicial Committee until the next convention. {sources([M18, DCM])}</p>
<p><b>The lesson:</b> the last vote of the weekend matters as much as the first. Don't let anyone rush the adjournment.</p>

{CAVEAT}
{BACK}"""
    page("convention/record.html", "What went wrong at past Libertarian conventions", "Five Libertarian national conventions, 2018 to 2026: vote counts, credentials fights, appeals, attrition, the 2026 chair race, and lessons for delegates.",
         "What went wrong before, and what to take from it", body, crumbs=CC + [("The record", "")])
