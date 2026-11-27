"""Herding Porcupines, the coalition RPG: rpg/index.html. The game itself is assets/rpg.js; its content is rpgdata.py."""
from core import page, e, ic
import rpgdata as G


def spoilers():
    rows = "".join(
        f'<tr><th scope="row">{e(f["who"])}<br><span class="sm">{e(f["org"])}</span></th><td>{"Left" if f["side"] == "left" else "Right"}</td>'
        f'<td>{", ".join(G.LENSES[c]["name"] for c in f["cares"])}</td><td>{G.LENSES[f["cold"]]["name"]}</td></tr>'
        for f in G.FACTIONS)
    return ('<details class="rpg-spoil"><summary>Spoilers: what every group cares about</summary><div class="tablewrap"><table>'
            '<caption>The eight groups in Porter County</caption><thead><tr><th scope="col">Group</th><th scope="col">Side of the aisle</th>'
            '<th scope="col">Cares about</th><th scope="col">Falls flat</th></tr></thead><tbody>' + rows + '</tbody></table></div></details>')


def build():
    n = len(G.FACTIONS)
    body = f"""
<h2 class="sr" id="play">Play the game</h2>
<div class="rpg" id="rpg">
<noscript><p class="warn">Herding Porcupines needs JavaScript to run. Everything it teaches is written out below, and the rest of the site works without it.</p></noscript>
</div>

<h2 id="how">How to play</h2>
<ol class="steps mini">
<li><span class="stepnum">1</span><div><b>Pick a measure and a character.</b> Your character comes from <a href="../life/index.html">the real-life quiz</a> if you've taken it, and your party's starting trust in you comes from <a href="../quiz.html">the purity test</a>.</div></li>
<li><span class="stepnum">2</span><div><b>Walk around town.</b> Arrow keys or W A S D, tap the map, use the arrow buttons, or pick a place from the list. Step into a door to go inside.</div></li>
<li><span class="stepnum">3</span><div><b>Talk people around.</b> Each conversation uses one of your {G.DAYS} days. Listen, make your case, find common ground, offer a deal, or ask for their support.</div></li>
<li><span class="stepnum">4</span><div><b>Keep your party together.</b> Deals cost party unity. Slogans buy it back and cost you everyone else. Under {G.LIN_RULE["unity"]} unity, your own side campaigns against you.</div></li>
<li><span class="stepnum">5</span><div><b>Count to three.</b> Five council members vote. The County Building shows the whip count any time, for free.</div></li>
</ol>
<p class="sm">Nothing is hidden: the game shows every number it uses, and the odds it shows are the odds you roll. Your game is saved in this browser only.</p>

<h2 id="teaches">What it teaches</h2>
<div class="grid">
<div class="card">{ic("people")}<h3>Listen before you argue</h3><p>Every group cares about a few things. An argument aimed at what they care about hits much harder. One aimed at what you care about can fall flat.</p></div>
<div class="card">{ic("handshake")}<h3>Answer the worry they raised</h3><p>Objections are tied to a value. Answer that value and you stay steady. Change the subject to your favorite point and you lose composure.</p></div>
<div class="card">{ic("layers")}<h3>Coalitions live where values overlap</h3><p>The tenants and the veterans both care about fairness. The church and the Grange both care about family. The end screen shows the overlap you built on.</p></div>
<div class="card">{ic("scales")}<h3>Every deal costs something</h3><p>Concessions win votes, can lose you other groups, cost you party unity and water down the liberty in the measure. You decide what's worth it.</p></div>
<div class="card">{ic("ballot")}<h3>Count votes, not likes</h3><p>Each ward member answers to two groups. One ally and nobody fighting you gets their vote. The at-large member wants a coalition from both sides of the aisle.</p></div>
<div class="card">{ic("porcupine")}<h3>Your own side counts too</h3><p>The purity caucus wants slogans. The classical liberals want good arguments. The campaign committee wants breadth. Ignore any of them and it shows up at the vote.</p></div>
</div>
<p>Porter County and everyone in it are made up. The moves aren't. For the real thing, read <a href="../organize/index.html">how to organize</a>, <a href="../organize/messaging.html">how to talk to people who don't agree with you yet</a>, and <a href="../convention/index.html">the convention guide</a>.</p>
{spoilers()}
"""
    page("rpg/index.html", "Herding Porcupines: a coalition RPG",
         f"A free retro RPG about building a coalition. Win over {n} groups across the aisle, keep your own party together, and pass a local measure in {G.DAYS} days.",
         "Herding Porcupines", body, kicker="The coalition game",
         lead="An old-school RPG about the hardest part of politics: getting people who disagree about almost everything to vote for the same thing.",
         crumbs=[("Herding Porcupines", "")], scripts=("assets/rpg-data.js", "assets/rpg.js"), wide=False)
