"""Website help: pieces a group can drop into the site it already has, plus the embeds themselves."""
from core import page, embed_page, moved, e, ic, ext, sources, data, mailto, SITE, ROOT
from sec_causes import META
from sec_plan import STEPS, road_parts, ROAD_DESC
from quizdata import QUESTIONS
import os

N = len(QUESTIONS)
QUIZ_TITLE = "Are you libertarian enough? The Libertarian Enough quiz"
PLAN_ALT = ("The plan: a road from today to less government in six steps. 1 Stop the harm. 2 Tear up the permission slips. 3 Open the exits. "
            "4 Cap it and set a clock. 5 Push power down. 6 Hand it back. Then the road forks to a small state or no state.")

EVENTS = [
    ("Monthly meetup",
     "[Group name] meets [first Tuesday of the month] at [place], [time]. One hour, one decision, and everyone leaves with a job. Pizza's on us. New? Come say hi. We'll ask what brought you and help you work on it.",
     "Libertarian meetup [date], [time] at [place]. One hour, real work, free pizza. New faces welcome. [link]"),
    ("Quiz night",
     "Are you libertarian enough? Find out at [place] on [date], [time]. Take the 40-statement quiz on your phone, compare purity scores, and argue about private roads with people who agree with you on almost everything else. Free to get in.",
     "Quiz night: are you libertarian enough? [date], [time] at [place]. Bring your phone and your purity score. Free. [link]"),
    ("Spring dinner",
     "[Group name]'s annual dinner is [date] at [place]. [Speaker] speaks. Tickets are $[price], or $[price] for a table of ten. Every dollar pays for [the petition drive / our county candidates].",
     "Our annual dinner is [date] at [place], with [speaker]. Tickets $[price], tables of ten $[price]. It pays for [what it pays for]. [link]"),
    ("Fall cookout",
     "Free cookout, [date] at [place]. Bring the family. We've invited every candidate on the [county] ballot, whatever their party, so come meet them, eat something, and get on our list.",
     "Free cookout [date] at [place]. Every candidate on the [county] ballot is invited, every party. Bring the kids. [link]"),
    ("Candidate forum",
     "Meet the candidates for [offices] on [date] at [place], [time]. We invited everyone on the ballot, in every party. Same questions, same time limits, and questions from the audience.",
     "Candidate forum [date], [time] at [place]. Every candidate for [offices] invited, every party. Bring your questions. [link]"),
    ("Record-clearing clinic",
     "Free record-clearing clinic, [date] at [place], [time]. Volunteer attorneys walk you through [state]'s process for sealing or expunging old cannabis and low-level records. Bring any court paperwork you have. Walk-ins welcome.",
     "Old cannabis record holding you back? Free record-clearing clinic [date] at [place]. Volunteer attorneys, walk-ins welcome. [link]"),
    ("Candidate school",
     "Thinking about running for something? Candidate school is [date] at [place], [time]. In one Saturday: filing, signatures, a 10-second message, door knocking and a basic website, with every office in [county], its deadline and its forms.",
     "Ever thought about running for office? One-day candidate school [date] at [place]. Filing, signatures, message, doors. [link]"),
    ("Booth at the fair",
     "Find us at [fair or festival], [dates], booth [number]. Take the quiz, sign the petition for [issue], and grab a list of every office on the [county] ballot.",
     "We're at [fair or festival] all weekend, booth [number]. Take the quiz, sign for [issue], say hi. [link]"),
]

CHECKS = [
    ("Every picture says what it shows.",
     "Give each image alt text that says what's in it, like \"Volunteers tabling at the county fair.\" Logos and decorations get empty alt text so screen readers skip them.",
     "Turn images off, or run WAVE. Anything that loses meaning needs alt text."),
    ("Text is dark enough to read.",
     "Body text needs a contrast ratio of at least 4.5 to 1 against its background. Gold or light gray text on white almost never passes.",
     "Put your text and background colors into WebAIM's contrast checker."),
    ("Headings are in order.",
     "One main heading per page, then sections under it. Don't pick a heading because of how big it looks; screen reader users jump by headings.",
     "Read only your headings, top to bottom. They should read like an outline."),
    ("Links say where they go.",
     "\"Donate to the [state] party\" works. \"Click here\" and \"read more\" don't, because many people hear links read out with nothing around them.",
     "Read each link on its own. If you can't tell where it goes, rewrite it."),
    ("It all works with a keyboard.",
     "Every menu, button and form field has to work with Tab, Enter and Space, and you have to be able to see which one you're on.",
     "Put the mouse away and Tab through the page, including the donate form."),
    ("Every form field has a label.",
     "Use visible labels, not gray placeholder text that disappears when you type. Error messages should say what's wrong in words.",
     "Click each field's label. The cursor should land in that field."),
    ("Color isn't the only signal.",
     "If red means \"required\" or a chart uses only color, add words or symbols too. Plenty of people can't tell red from green.",
     "Look at the page in grayscale. Everything should still make sense."),
    ("Videos have captions.",
     "Use real captions, not just the auto-generated ones left unchecked, and post a transcript for audio and podcasts.",
     "Watch one of your videos on mute."),
    ("It works on a phone and zoomed in.",
     "Text should zoom to 200% without breaking the page or making people scroll sideways.",
     "Zoom your browser to 200%, then open the page on a phone."),
    ("Embeds have titles.",
     "Every iframe, like a map, a video or our quiz, needs a title attribute that says what it is. The snippets on this page already have one.",
     "Look for title=\"...\" inside each iframe tag in your page's code."),
    ("Nothing flashes or plays by itself.",
     "No autoplay video with sound, and nothing that flashes more than three times a second.",
     "Load the page with the sound up. It should stay quiet until someone presses play."),
    ("Your PDFs aren't the only copy.",
     "Put the platform, the agenda and the voter guide on the page as text. A scanned PDF is a picture of words, and screen readers can't read it.",
     "Try to select the text in your PDF. If you can't, neither can a screen reader."),
]

TOOLS = [
    ("https://wave.webaim.org/", "WAVE", "paste in your address and it marks problems on the page"),
    ("https://webaim.org/resources/contrastchecker/", "WebAIM contrast checker", "tells you whether two colors pass"),
    ("https://www.w3.org/WAI/WCAG22/quickref/", "WCAG 2.2 quick reference", "the full standard, searchable"),
]


def build():
    road_asset()
    embed_quiz()
    help_page()
    moved("free-sites.html", "website-help.html", "Website help")


def road_asset():
    """The plan graphic as a file other sites can show with an img tag."""
    labels = []
    for i, s in enumerate(STEPS):
        col, row = divmod(i, 3)
        x, y = 40 + col * 420, 268 + row * 40
        labels.append(f'<circle cx="{x}" cy="{y - 7}" r="15" fill="#f5c400" stroke="#1a1a1a" stroke-width="2"/>'
                      f'<text x="{x}" y="{y}" font-size="17" font-weight="800" text-anchor="middle" fill="#1a1a1a">{i + 1}</text>'
                      f'<text x="{x + 26}" y="{y}" font-size="20" font-weight="700" fill="#ffffff">{e(s["title"])}</text>')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 410" width="880" height="410" role="img" aria-labelledby="t d" '
           'font-family="system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif">'
           '<title id="t">The plan: from today to less government</title>'
           f'<desc id="d">{e(PLAN_ALT)}</desc>'
           '<rect width="880" height="410" rx="18" fill="#1f2a44"/>'
           '<g transform="translate(0 8)">' + "".join(road_parts()) + '</g>'
           + "".join(labels) +
           '<text x="850" y="392" font-size="15" font-weight="700" text-anchor="end" fill="#f5c400">libertarianenough.org/plan</text>'
           '</svg>\n')
    with open(os.path.join(ROOT, "assets", "plan-road.svg"), "w") as f:
        f.write(svg)


def embed_quiz():
    body = f"""
<div class="quiz" id="quiz" data-results="{SITE}/results.html">
<div id="quiz-intro">
<p class="kicker">The quiz</p>
<h1>Are you libertarian enough?</h1>
<p>{N} statements, about five minutes. Find your libertarian type, a purity score out of 100, and your spot on the spectrum. Your answers stay in your browser.</p>
<div class="row"><button class="btn gold" id="quiz-start" type="button">Start the quiz</button><button class="btn ghost" id="quiz-restart" type="button" hidden>Start over</button></div>
<noscript><p class="warn">The quiz needs JavaScript. You can take it on {ext(SITE + "/quiz.html", "Libertarian Enough")} instead.</p></noscript>
</div>
<div id="quiz-prog" hidden><div class="progress" aria-hidden="true"><span id="quiz-bar"></span></div><p class="sr" id="quiz-status" aria-live="polite"></p></div>
<div id="quiz-stage" hidden></div>
</div>
"""
    embed_page("embed/quiz.html", "Are you libertarian enough?", "quiz.html", body, scripts=("assets/data.js", "assets/quiz.js"))


def snippet(sid, label, text, rows=6):
    return (f'<div class="snip"><label for="{sid}">{label}</label>'
            f'<textarea id="{sid}" rows="{rows}" readonly spellcheck="false">{e(text)}</textarea>'
            f'<div class="row"><button type="button" class="btn ghost small" data-copy="{sid}" hidden>Copy</button>'
            f'<span class="copied" id="{sid}-s" role="status"></span></div></div>')


def issue_text(cid, name, pitch, msg, acts):
    url = f"{SITE}/causes/{cid}.html"
    plain = (f"{name}\n\n{pitch}\n\nIn 10 seconds: \"{msg}\"\n\nWhat we can do here in [your county]:\n"
             + "".join(f"- {a}\n" for a in acts)
             + f"\nWant in? [How to join or reach us.]\n\nWhere things stand today, with sources: {url}\n")
    html = (f"<h2>{e(name)}</h2>\n<p>{e(pitch)}</p>\n<p><strong>In 10 seconds:</strong> \"{e(msg)}\"</p>\n"
            f"<h3>What we can do here in [your county]</h3>\n<ul>\n"
            + "".join(f"  <li>{e(a)}</li>\n" for a in acts)
            + f"</ul>\n<p>Want in? [How to join or reach us.]</p>\n"
            f"<p>Where things stand today, with sources: <a href=\"{url}\">{e(name)} on Libertarian Enough</a>.</p>\n")
    return plain, html


def help_page():
    quiz_src = f"{SITE}/embed/quiz.html"
    quiz_iframe = (f'<iframe src="{quiz_src}" title="{QUIZ_TITLE}" '
                   'style="width:100%;max-width:760px;height:760px;border:0" loading="lazy"></iframe>')
    quiz_auto = (f'<iframe data-le-embed src="{quiz_src}" title="{QUIZ_TITLE}" '
                 'style="width:100%;max-width:760px;height:760px;border:0" loading="lazy"></iframe>\n'
                 f'<script src="{SITE}/assets/embed.js" async></script>')
    plan_img = (f'<figure style="margin:0">\n<img src="{SITE}/assets/plan-road.svg" width="880" height="410" style="max-width:100%;height:auto" '
                f'alt="{PLAN_ALT}">\n'
                f'<figcaption>Six steps from more government to less. <a href="{SITE}/plan/index.html">Read the plan on Libertarian Enough</a>.</figcaption>\n</figure>')

    causes = data("causes")["causes"]
    order = ["cannabis", "sex-work", "bodily-autonomy"]
    causes.sort(key=lambda c: (order.index(c["id"]) if c["id"] in order else 99))
    issues = []
    for c in causes:
        name, icon, pitch, msg, kind = META[c["id"]]
        plain, html = issue_text(c["id"], name, pitch, msg, c["local_actions"])
        issues.append(f'<details class="kit"><summary>{e(name)}</summary>'
                      + snippet(f"i-{c['id']}-t", "Plain text, for any editor", plain, 12)
                      + snippet(f"i-{c['id']}-h", "HTML, for an HTML or code block", html, 12) + '</details>')

    events = []
    for i, (title, long, short) in enumerate(EVENTS):
        events.append(f'<details class="kit"><summary>{e(title)}</summary>'
                      + snippet(f"ev{i}-l", "For your event page or newsletter", long, 4)
                      + snippet(f"ev{i}-s", "For a social post", short, 3) + '</details>')

    checks = "".join(f'<li><b>{e(t)}</b> {e(d)} <span class="how">How to check: {e(h)}</span></li>' for t, d, h in CHECKS)
    tools = "".join(f"<li>{ext(u, e(n))}: {e(d)}.</li>" for u, n, d in TOOLS)

    doors = [("#quiz", "quiz", "The quiz", "Put the whole quiz on your site. Results open on ours."),
             ("#plan", "road", "The plan graphic", "Six steps from more government to less, with alt text built in."),
             ("#issues", "torch", "Issue pages", "Twelve causes, ready to paste, with a link to the sourced version."),
             ("#events", "people", "Event blurbs", "Meetups, dinners, forums and clinics. Fill in the brackets."),
             ("#access", "circles", "Accessibility checklist", "Twelve checks anyone can run in an afternoon.")]
    cards = "".join(f'<a class="card cardlink" href="{h}">{ic(i)}<h3>{t}</h3><p>{d}</p></a>' for h, i, t, d in doors)

    body = f"""
<p class="lead">Your group probably has a website already. Here are pieces you can drop into it. They're free, there's nothing to sign up for, and you can change them however you like. A link back is nice but not required.</p>
<h2>Pick what you need</h2>
<div class="grid">{cards}</div>

<h2 id="quiz">Put the quiz on your site</h2>
<p>Paste this into any page that takes an HTML or embed block. Visitors take all {N} statements on your page. Their answers stay in their own browser, and their results open on Libertarian Enough in a new tab.</p>
{snippet("q-basic", "Quiz embed code", quiz_iframe, 3)}
<p>If your site lets you add a script, use this version instead. It grows and shrinks to fit each question, so there's no scroll bar inside the box.</p>
{snippet("q-auto", "Quiz embed code that fits itself", quiz_auto, 4)}
<details class="kit"><summary>See what it looks like</summary>
<iframe data-le-embed src="embed/quiz.html" title="{QUIZ_TITLE}" style="width:100%;height:760px;border:0" loading="lazy"></iframe>
</details>

<h2 id="plan">Add the plan graphic</h2>
<p>A picture of <a href="plan/index.html">the plan</a>, with the six steps written into it and alt text that reads them all out. It stays sharp at any size.</p>
<div class="planart plain"><img src="assets/plan-road.svg" width="880" height="410" alt="{e(PLAN_ALT)}"></div>
{snippet("p-img", "Plan graphic code", plan_img, 6)}

<h2 id="issues">Issue pages, ready to paste</h2>
<p>Each one has the cause in a sentence, a 10-second message, three things a county group can actually do, and a link to <a href="causes/index.html">the full cause page</a>, which keeps the facts and sources current so you don't have to. Swap the parts in [brackets] for your own.</p>
{"".join(issues)}

<h2 id="events">Event blurbs</h2>
<p>Each comes in two lengths: one for your event page or newsletter, one short enough for a social post. The formats come from <a href="organize/meetings.html">the meeting playbook</a> and <a href="fundraise/events.html">events and dinners</a>.</p>
{"".join(events)}

<h2 id="access">Accessibility checklist</h2>
<p>More than 1 in 4 American adults reported a disability in 2022. A site they can't use shuts out a lot of voters before anyone reads a word. {sources(["https://www.cdc.gov/media/releases/2024/s0716-Adult-disability.html"])}</p>
<ol class="facts checks">{checks}</ol>
<h3>Free tools</h3>
<ul class="facts">{tools}</ul>

<h2 id="whole-site">Need a whole site?</h2>
<p>Email {mailto("Website request")} and we'll build one free. Examples of our work: {ext("https://findbingo.org", "Find Bingo")}, {ext("https://the-reefer.com", "The Reefer")} and {ext("https://abuseofoffice.org", "Abuse of Office")}.</p>
"""
    page("website-help.html", "Website help for libertarian groups", "Free pieces for the site your libertarian group already has: an embeddable quiz, the plan graphic, ready-to-paste issue pages, event blurbs and an accessibility checklist.",
         "Website help", body, crumbs=[("Website help", "")], scripts=("assets/copy.js", "assets/embed.js"), wide=False)
