"""A page for every state and DC."""
import re
from core import page, e, ic, ext, sources, data, mailto

SC = [("States", "states/index.html")]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


SEXWORK = {
    "NV": "Licensed brothels are legal only in some rural counties. State law bars licensing them in any county of 700,000 or more people, which rules out Las Vegas. About 19 were open in 6 counties as of September 2023.",
    "ME": "Maine adopted the 'Nordic model' in June 2023: selling sex is no longer a crime, but buying it still is.",
}
SEXWORK_DEFAULT = "Buying and selling sex are both crimes statewide."

GAMING = {
    "OH": "Ohio licenses bingo only to charitable organizations, through the Attorney General, after two years of existence and with an IRS 501(c) letter. A party affiliate's route is a charity partner.",
    "NY": "New York's State Board of Elections has said political parties and committees are not authorized to run games of chance, raffles included.",
    "NM": "New Mexico's Gaming Control Board has said political organizations can't run raffles under the state's Bingo and Raffle Act.",
    "IL": "Illinois lets political committees run raffles with a license from the State Board of Elections.",
}
BALLOT = {"OH": "Ohio's vote test for keeping a party on the ballot is 3%."}


def build():
    st = data("states")
    cs = data("cannabis-status")
    rows = []
    for s in st["states"]:
        state_page(s, cs)
        c = cs["states"].get(s["code"], {}).get("adult-use")
        badge = []
        if s.get("notes"):
            badge.append('<span class="badge mid">Note</span>')
        if not s.get("on_lnc_list"):
            badge.append('<span class="badge">Not on LNC list yet</span>')
        aff = e(s["affiliate"]) if s.get("affiliate") else "Unknown"
        rows.append(f'<tr><th scope="row"><a href="{slug(s["name"])}.html">{e(s["name"])}</a></th><td>{aff} {"".join(badge)}</td>'
                    f'<td>{e(cs["statuses"].get(c["status"], c["status"])) if c else "Not yet reviewed"}</td></tr>')
    body = f"""
<p>Every state and DC has a page with its Libertarian Party affiliate, any public disputes about who that is, and where cannabis and sex work law stand. More is coming as states ask for it.</p>
<div class="note"><p><b>Listing isn't partnership.</b> We list each affiliate as public information, the same way for every state. No state party is a partner of Libertarian Enough until it says yes, and we'll say so on its page when it does.</p></div>
<h2>Is this your state party?</h2>
<p>Any state affiliate can claim its page. We'll turn it into your own section of this site, with your events, candidates and donate link (to your own account, not ours). For your own site, grab the quiz and issue pages from <a href="../website-help.html">Website help</a>. <a href="#claim">How to claim it</a>.</p>
<div class="tablewrap"><table><caption>State affiliates and adult-use cannabis status</caption>
<thead><tr><th scope="col">State</th><th scope="col">Libertarian affiliate</th><th scope="col">Adult-use cannabis</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<h2 id="claim">How to claim your state</h2>
<p>Someone authorized by the state affiliate (chair, vice chair or a board-approved webmaster) asks, and we confirm through the party's public contact before changing anything. To start, email {mailto("Claim a state page")} with your state, your role and where we can confirm it.</p>
<p class="src">Affiliate list: {ext(st["list_source"], "lp.org state affiliates")} (lists names and chairs, not websites). Websites found through public listings and opened one by one on {e(st["checked"])}. Cannabis status from {ext("https://the-reefer.com", "The Reefer")}'s state data, as of {e(cs["as_of"])}.</p>
"""
    page("states/index.html", "Libertarian state affiliates, state by state", "Every state's Libertarian Party affiliate, public disputes, and cannabis and sex work law status, with a page each state can claim.",
         "Find your state", body, lead="Fifty states and DC. The public facts, the drama, and a page your state can claim.", crumbs=[("States", "")])


def status_line(cs, code, q):
    c = cs["states"].get(code, {}).get(q)
    if not c:
        return "<p>Not yet reviewed.</p>"
    lab = cs["statuses"].get(c["status"], c["status"])
    tone = {"allowed": "yes", "not-permitted": "no"}.get(c["status"], "mid")
    return (f'<p><span class="badge {tone}">{e(lab)}</span> <b>{e(c["short"])}</b>. {e(c["detail"])} '
            f'<span class="src">Law: {e(c["citation"])}. Checked {e(c["reviewed_on"])}.</span> {sources(c["sources"])}</p>')


def state_page(s, cs):
    code = s["code"]
    if s.get("url") and s.get("url_verified"):
        aff = f'<p><b>{e(s["affiliate"])}</b>: {ext(s["url"], e(s["url"].replace("https://", "").replace("http://", "").rstrip("/")))}</p>'
    elif s.get("url"):
        aff = f'<p><b>{e(s["affiliate"])}</b>. We couldn\'t confirm its website when we checked, so we haven\'t linked one.</p>'
    else:
        aff = f'<p><b>{e(s["affiliate"] or "Unknown")}</b>. We couldn\'t find a working website when we checked.</p>'
    lnc = ("<p>Listed on the Libertarian National Committee's state affiliates page.</p>" if s.get("on_lnc_list")
           else "<p>Not on the Libertarian National Committee's state affiliates page as of our last check.</p>")
    note = f'<div class="note"><p><b>Worth knowing:</b> {e(s["notes"])}</p></div>' if s.get("notes") else ""
    sw = SEXWORK.get(code, SEXWORK_DEFAULT)
    extra = ""
    if code in GAMING or code in BALLOT:
        extra = "<h2>Organizing and fundraising notes</h2><ul class=\"facts\">" + "".join(
            f"<li>{e(x)}</li>" for x in [BALLOT.get(code), GAMING.get(code)] if x) + '</ul><p><a href="../fundraise/index.html">The fundraising playbook</a></p>'
    own = ""
    if code == "OH":
        own = f'<p>Ohio has its own cannabis guide from the same builders: {ext("https://ohioweed.org", "OhioWeed.org")}.</p>'
    body = f"""
<h2>The state affiliate</h2>
{aff}{lnc}{note}
<p class="src">Public information, listed the same way for every state. Not a partnership. {sources(s["sources"])}</p>
<h2>Cannabis</h2>
<h3>Adults 21 and older</h3>{status_line(cs, code, "adult-use")}
<h3>Medical</h3>{status_line(cs, code, "medical")}
<p>Full state-by-state rules on possession, home grow, driving and more: {ext("https://the-reefer.com", "The Reefer")}.</p>{own}
<h2>Sex work</h2><p>{e(sw)} <a href="../causes/sex-work.html">The libertarian case</a>.</p>
{extra}
<h2>Is this your state party?</h2>
<p>Claim this page and we'll turn it into your own section: events, candidates, causes and a donate link to your own account. Want the quiz or issue pages on your own site? <a href="../website-help.html">Website help</a>. <a href="index.html#claim">How to claim it</a>.</p>
<p class="row"><a class="btn ghost" href="index.html">All states</a><a class="btn gold" href="../organize/index.html">Organize in {e(s["name"])}</a></p>
"""
    page(f"states/{slug(s['name'])}.html", f"Libertarians in {s['name']}", f"{s['name']}'s Libertarian Party affiliate, public disputes, cannabis law and sex work law, with a page the state party can claim.",
         e(s["name"]), body, kicker="State", crumbs=SC + [(s["name"], "")], wide=False)
