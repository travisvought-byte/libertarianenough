"""The plan: a step-by-step road from more state to less state, and the debate over how fast."""
from core import page, e, ic, ext, sources

CR = [("The plan", "plan/index.html")]
BOOK = '<a href="../book.html">The Asymmetric Libertarian</a>'


def S(*urls):
    return sources(list(urls))


def bq(text, where):
    return f'<blockquote><p>"{text}"</p><p class="src">{BOOK}, {where}</p></blockquote>'


# Sources used more than once
PEW = "https://www.pewresearch.org/short-reads/2026/05/26/facts-about-marijuana/"
OH2 = "https://ballotpedia.org/Ohio_Marijuana_Legalization_Initiative_(2022)"
GALLUP_MJ = "https://news.gallup.com/poll/697445/americans-positive-progress-drugs.aspx"
NM = "https://ij.org/case/new-mexico-forfeiture/"
NE = "https://ij.org/press-release/institute-justice-applauds-nebraskas-sweeping-forfeiture-reforms/"
ME = "https://ij.org/press-release/maine-becomes-fourth-state-to-end-civil-forfeiture/"
CS = "https://www.cleanslateinitiative.org/states"
CS2 = "https://www.cleanslateinitiative.org/updates/states-of-clean-slate-end-of-year-wrap-up"
TX1 = "https://docs.legis.wisconsin.gov/misc/lc/study/2008/special_committee_on_justice_reinvestment_initiative_oversight/010_january_12_2009_meeting/texas_state_brief"
TX2 = "https://csgjusticecenter.org/?p=23861"
TX3 = "https://csgjusticecenter.org/wp-content/uploads/2020/10/TXJRStateReport32011v2.pdf"
FSA = "https://rollcall.com/2018/12/20/house-approves-criminal-justice-overhaul-sends-to-president/"
AZL = "https://ballotpedia.org/Arizona_becomes_the_first_state_to_recognize_out-of-state_occupational_licenses_(2019)"
L28 = "https://reason.com/2025/08/29/report-28-states-now-recognize-occupational-licenses-from-elsewhere"
WY = "https://www.wyoleg.gov/2015/Summaries/HB0056.pdf"
FOOD7 = "https://ij.org/report/new-data-show-homemade-food-for-sale-is-incredibly-safe/"
TXLEM = "https://capitol.texas.gov/tlodocs/86R/billtext/html/HB00234F.htm"
ILLEM = "https://reason.com/2021/07/23/new-hampshire-and-illinois-are-legalizing-unlicensed-lemonade-stands/"
BREW = "https://homebrewersassociation.org/homebrew-community-culture/homebrewing-is-legal-but-the-fight-continues/"
TRUCK = "https://www.econlib.org/library/Enc/TruckingDeregulation.html"
ESA = "https://www.knau.org/knau-and-arizona-news/2022-07-07/arizona-gov-doug-ducey-signs-private-school-voucher-expansion-bill-now-largest-in-u-s"
SC18 = "https://ballotpedia.org/States_with_and_without_universal_school_choice_programs"
RTT = "https://fee.org/articles/the-right-to-try-war-was-actually-won-on-the-state-level/"
AIR1 = "https://airandspace.si.edu/stories/editorial/airline-deregulation-when-everything-changed"
AIR2 = "https://gao.gov/assets/a250423.html"
TABOR = "https://ballotpedia.org/Colorado_Taxpayer's_Bill_of_Rights_(TABOR)"
TABOR24 = "https://9news.com/article/news/local/colorado-tabor-refunds/73-0eec6207-940f-43e7-954a-b22dc287fd32"
SUNTX = "https://www.sunset.texas.gov/about-us"
SUN36 = "https://www.ncsl.org/labor-and-employment/sunset-and-sunrise"
NY23 = "https://americanheritage.com/1923-seventy-five-years-ago-0"
REPEAL = "https://www.britannica.com/event/Prohibition-United-States-history-1920-1933/Repeal"
FSP = "https://www.fsp.org/?p=64"
FSP2 = "https://www.foxnews.com/us/20000-liberty-minded-people-pledge-to-move-to-new-hampshire"
FIRE = "https://www.nvfc.org/wp-content/uploads/2026/02/volunteer-fire-service-fact-sheet.pdf"
SANDY = "https://www.sandyspringsga.gov/public-private-partnership/"
NOZICK = "https://www.britannica.com/biography/Robert-Nozick"

STEPS = [
    dict(
        slug="stop-the-harm", icon="key", title="Stop the harm",
        short="End punishments for peaceful choices: jail for a plant, cops taking cash without a conviction, old records that follow people forever.",
        covers="Cannabis, civil forfeiture, clean records, sentencing",
        lead="Start by ending the punishments that wreck lives over peaceful choices. These reforms have the widest support and the clearest wins.",
        why=("<p>This is where government does the most damage to the most people, and where the most voters already agree with us. "
             "A cannabis charge or a seized car can cost someone their job, their savings and their kids. The book judges a system by what happens when someone fails, "
             "and it puts it simply: \"People will not take risks they cannot survive.\" A criminal record is a failure that never ends.</p>"
             "<p>It comes first because it hurts the most, and because winning it shows people that less government can mean more safety, not less. "
             "It also fixes bad incentives. When police keep what they seize, the system rewards taking. Require a conviction and that reward goes away.</p>"),
        quote=("One mistake should not define a lifetime.", "chapter 5"),
        proof=[
            ("In 2012, Colorado and Washington became the first states to legalize marijuana for adults. As of 2026, 24 states and D.C. allow it, and 53% of Americans live where it's legal.", [PEW]),
            ("Ohio voters passed Issue 2 in November 2023 with 57.19% of the vote, making Ohio the 24th state to legalize recreational marijuana.", [OH2]),
            ("In an October 2025 Gallup poll, 64% of U.S. adults said marijuana should be legal, including 40% of Republicans.", [GALLUP_MJ]),
            ("In 2015, New Mexico's legislature voted unanimously to abolish civil forfeiture. The state can now take property only after a criminal conviction, and the money goes into the general fund.", [NM]),
            ("Nebraska required a conviction for most forfeitures in 2016, by a 38 to 8 vote. In 2021, Maine became the fourth state to end civil forfeiture, after New Mexico, Nebraska and North Carolina.", [NE, ME]),
            ("Pennsylvania passed the first Clean Slate law in 2018, which seals old records automatically. By 2026, 14 states and D.C. had passed one, putting more than 18 million people on a path to full or partial sealing.", [CS, CS2]),
            ("In 2007, facing a forecast of 14,000 more inmates in five years, Texas spent $241 million on treatment and diversion instead of new prisons. Since then its prison population has fallen by more than 34,000 people and it has closed 16 prison facilities. "
             "The Council of State Governments Justice Center, which helped design the plan, reports more than $1.6 billion saved or avoided. Texas's crime rate in 2009 was its lowest since 1974, though the numbers don't prove the reform caused that.", [TX1, TX2, TX3]),
            ("In December 2018, Congress passed the First Step Act 87 to 12 in the Senate and 358 to 36 in the House. It lets judges go below some mandatory minimums and expands job training and drug treatment in federal prison.", [FSA]),
        ],
        town=[
            "Your county prosecutor decides which cases get charged. Ask every candidate whether they'll charge simple cannabis possession, and vote on the answer.",
            "Find out if your county runs a record-sealing clinic. If it doesn't, ask the clerk of courts or a legal aid group to start one.",
            "Ask your sheriff and police chief, at a public meeting, how much property they took last year from people who were never convicted.",
        ],
        party=[
            "Pick one bill, like a Clean Slate law or a conviction requirement for forfeiture, and make it your affiliate's signature issue for a whole session.",
            "Testify at every committee hearing on it. Bring a person it happened to, not a white paper.",
            "Thank every lawmaker who votes yes, by name and in public, whatever their party. The First Step Act passed with both parties.",
        ],
        you=[
            "Volunteer at a record-sealing or expungement clinic. Legal aid groups need help with paperwork.",
            "Sign the next ballot petition on cannabis or sentencing in your state.",
            "Write down one story in five sentences: someone who lost a job or a car over a charge that went nowhere. Send it to your state representative.",
        ],
        msg="Right now police can take your cash without charging you, and you have to sue to get it back. We require a conviction first. No conviction, no taking.",
        trap=("Legal, but only for the well connected.", "Ending a ban by handing out a few expensive licenses swaps one wall for another. The book's warning is that removing rules without redesigning the system creates \"new gatekeepers.\" Push for a market anyone can enter."),
        related=[("../causes/cannabis.html", "Cannabis"), ("../causes/criminal-justice.html", "Criminal justice"), ("../causes/forfeiture.html", "Civil forfeiture")],
    ),
    dict(
        slug="permission-slips", icon="stamp", title="Tear up the permission slips",
        short="Cut the licenses, permits and fees that stand between people and a job, a side business or a lemonade stand.",
        covers="Job licenses, home food sales, permits, kids' stands",
        lead="Next, cut the licenses, permits and fees that make ordinary work hard. These wins are cheap, fast and popular, and they show people what less friction feels like.",
        why=("<p>Most of the government people run into isn't a ban. It's a form. The book says freedom usually disappears \"Not through force. Through friction.\" "
             "A permit that takes six months is a ban for anyone who can't wait six months.</p>"
             "<p>These fixes cost the state almost nothing, pay off right away, and win votes from people who'd never call themselves libertarian. "
             "That's why they come second: they build trust fast, and trust is what pays for the bigger steps.</p>"),
        quote=("Can a normal person navigate this without hiring help?", "chapter 4"),
        proof=[
            ("On April 10, 2019, Arizona became the first state to recognize out-of-state job licenses, so licensed newcomers can keep working without redoing Arizona's training. By 2025, 28 states had some form of it.", [AZL, L28]),
            ("Wyoming's Food Freedom Act took effect in 2015. It frees homemade food sold directly to an informed buyer from state and local licenses, permits and inspection.", [WY]),
            ("Seven states now allow sales of most homemade foods, including perishable ones. None of them found a foodborne illness caused by food sold under those laws.", [FOOD7]),
            ("Since 2019, Texas cities and counties can't ban kids' lemonade stands or charge a permit fee for them, on private property or in public parks. Illinois stopped health departments from regulating lemonade sales by kids under 16 in 2021.", [TXLEM, ILLEM]),
            ("Homebrewing beer became legal under federal law in 1979. States kept their own bans, and Alabama and Mississippi were the last to legalize it, in 2013.", [BREW]),
            ("Federal regulators once controlled who could haul freight by truck and what they could charge. After trucking was decontrolled, ending with the Motor Carrier Act of 1980, truckload rates fell about 25% after inflation from 1977 to 1982, and licensed carriers topped 40,000 by 1990. Supporters ranged from Gerald Ford and Jimmy Carter to Ted Kennedy.", [TRUCK]),
        ],
        town=[
            "Count the steps. Pick one thing, like opening a home bakery or adding a deck, and write down every form, fee and day it takes. The book says to measure friction in time, cost and steps.",
            "Ask your council for a shot clock: if the city doesn't answer a permit request in 30 days, it's approved. The book's rule is \"If the system cannot respond, the answer becomes yes.\"",
            "Check your town's rules on kids' stands, home businesses and food trucks. Any permit you find is your first ordinance to repeal.",
        ],
        party=[
            "If your state doesn't recognize out-of-state licenses yet, make it a bill. Arizona's 2019 law is the model.",
            "Push a food freedom bill modeled on Wyoming's.",
            "Ask for a sunrise review: before the state licenses a new job, it has to show what harm the license prevents.",
        ],
        you=[
            "Ask three people who work with their hands which license or permit made their life harder. Write down their words. That's your message.",
            "If you're licensed and moved states, send your story to your state representative.",
            "Buy from a home baker or a kid's stand, and tell them why you're glad it's legal.",
        ],
        msg="If another state says you're qualified, you can work here immediately.",
        msg_note="That line is straight from the book, chapter 8.",
        trap=("A new form for the old form.", "A \"streamlined\" process with a new office and a new fee isn't less government. Measure it: fewer steps, less time and lower cost, or it didn't count."),
        related=[("../causes/licensing.html", "Licensing"), ("../causes/food.html", "Food freedom"), ("../causes/housing.html", "Housing")],
    ),
    dict(
        slug="exits", icon="door", title="Open the exits",
        short="Let people leave systems that fail them before you shut anything down: school choice, the right to try, real competition.",
        covers="School choice, right to try, open markets",
        lead="Before you shut down any government service, give people a way out of it. When people can leave, the system has to get better or get smaller.",
        why=("<p>Cutting a program people rely on, with nothing in its place, feels like loss. The book is blunt about it: \"Even good policy can feel like loss. And voters reject loss.\" "
             "An exit flips that. Nobody loses anything. People who are happy stay, and people who aren't can leave.</p>"
             "<p>Every person who leaves and does better is proof the alternative works, and that proof makes the later steps possible. "
             "An exit gives people the ability to act, not just permission on paper.</p>"),
        quote=("Permission without capability is theater.", "chapter 2"),
        proof=[
            ("In July 2022, Arizona made every K-12 student eligible for its education savings accounts, worth more than $6,500 a year per child. About 12,000 students used them before. Over 1 million could qualify after.", [ESA]),
            ("As of December 2025, 18 states have universal private school choice programs. West Virginia launched the first universal education savings account in 2021.", [SC18]),
            ("Colorado passed the first state Right to Try law in 2014, letting patients try experimental treatments. By the time the federal Right to Try Act was signed on May 30, 2018, patients in 40 states already had access.", [RTT]),
            ("President Carter signed the Airline Deregulation Act in 1978 with support from both parties. From 1980 to 2005, the median U.S. airfare fell almost 40% after inflation, and passenger boardings grew from 254 million in 1978 to 670 million in 2005. Fares fell less on short routes and in small markets.", [AIR1, AIR2]),
        ],
        town=[
            "Look for local monopolies, like a single trash hauler, ambulance company or towing company, and ask why residents can't choose.",
            "Start or support a learning pod, co-op or microschool. Every one that works is a new exit.",
            "Ask your school board how many students transfer in and out each year, and why they leave.",
        ],
        party=[
            "If your state isn't one of the 18 with universal school choice, make that the ask. If it is, push to cut the paperwork families face to use it.",
            "Back right-to-try expansions, so more patients can try more treatments.",
            "Fight every new government-granted monopoly, from cable franchises to towing contracts.",
        ],
        you=[
            "Talk to one family that left a school that wasn't working for their kid. Ask what made it hard, and write it down.",
            "Find out whether your state has an education savings account, and tell one family who could use it.",
            "Use a choice you already have, then tell people how it went.",
        ],
        msg="If the public school works for your kid, stay. If it doesn't, take the money with you. Nobody loses a thing.",
        trap=("Exits with strings.", "An exit buried in so many rules that every option looks the same isn't an exit. Hold schools to results, not to running things the state's way."),
        related=[("../causes/schooling.html", "Schooling"), ("../causes/bodily-autonomy.html", "Bodily autonomy")],
    ),
    dict(
        slug="cap-and-sunset", icon="clock", title="Cap it and set a clock",
        short="Lock in each win so government can't quietly grow back: spending limits, and laws that end unless lawmakers renew them.",
        covers="Spending caps, sunset reviews",
        lead="Every win can be undone a little at a time. Spending caps and expiration dates make government ask permission to grow, instead of you asking permission to live.",
        why=("<p>Government rarely grows in one big vote. The book: \"Complexity rarely arrives all at once. It accumulates.\" So the fix has to be automatic too. "
             "A spending cap stops the state from quietly spending every new dollar. A sunset clause means a law or agency ends on a set date unless lawmakers vote to keep it, so the burden of proof flips.</p>"
             "<p>These come fourth because they protect what steps 1 to 3 won, and because voters accept limits more easily once they've seen less government work.</p>"),
        quote=("Remove rules as aggressively as they are added.", "chapter 4"),
        proof=[
            ("In 1992, Colorado voters approved the Taxpayer's Bill of Rights, 53.7% to 46.3%. It caps what the state can collect and spend, requires voter approval for new taxes, and refunds money collected above the cap.", [TABOR]),
            ("In fiscal year 2024 alone, Colorado owed taxpayers about $1.7 billion in refunds under that cap.", [TABOR24]),
            ("Since 1977, Texas's sunset process has abolished 95 state agencies, 42 of them completely. Agencies under review end automatically unless lawmakers vote to keep them. Reviews from 1985 to 2023 produced about $1 billion in savings and revenue.", [SUNTX]),
            ("Colorado, Texas and Alabama were among the first states to adopt sunset reviews, in the 1970s. By the 1980s, 36 states had them.", [SUN36]),
        ],
        town=[
            "Ask for a sunset on every new city board, fee and program: it ends in five years unless the council votes to keep it.",
            "Read your city or county budget. Find the three lines that grew fastest over five years and ask why at the next meeting.",
            "When a levy or tax comes up for a vote, ask when it ends. If the answer is never, that's your argument.",
        ],
        party=[
            "Push a sunset review law if your state doesn't have one, or put more agencies under it if it does. Texas is the model.",
            "In states where citizens can put measures on the ballot, take a spending limit straight to voters. Colorado's passed with 53.7%.",
            "Ask every candidate one question: name one state program you'd let expire.",
        ],
        you=[
            "Go to one budget hearing. Sit in the front. Ask one question.",
            "Look up how much your state's budget grew in the last ten years, and share that one number with three people who complain about taxes.",
            "When anyone proposes a new program, ask them in public when it ends.",
        ],
        msg="Every new program gets an expiration date. If it works, lawmakers can vote to keep it. If it doesn't, it ends on its own.",
        trap=("Caps with an escape hatch.", "A limit lawmakers can waive with a simple majority is a suggestion. Look for limits that take a vote of the people, or a supermajority, to break."),
        related=[("../organize/candidates.html", "Recruit and run candidates"), ("../organize/messaging.html", "Messages that land")],
    ),
    dict(
        slug="push-power-down", icon="layers", title="Push power down",
        short="Move what's left from Washington to the state, the town and the neighborhood, where people can see it and fix it.",
        covers="Federal to state to local, with rights protected at every level",
        lead="Move what's left out of Washington and into the state, the town and the neighborhood. The closer a decision is to you, the faster you can see it fail and fix it.",
        why=("<p>A bad federal law can last for decades because there's nothing to compare it to and no easy way out. The book says what separates markets from politics is "
             "feedback speed, not perfection. Fifty states and thousands of towns are thousands of experiments, and people can move to the ones that work. "
             "Many of the wins on steps 1 to 3 started in one state before the rest caught up.</p>"
             "<p>But local isn't automatically free. The book warns that \"Local politics rewards opposition,\" which is how a neighborhood board can block every new house. "
             "So push power down and protect individual rights at every level. Sometimes the state should stop a town from banning something peaceful, the way Texas did for kids' lemonade stands.</p>"),
        quote=("Not perfection— but feedback speed.", "chapter 3"),
        proof=[
            ("In 1923, New York repealed its state Prohibition enforcement law, leaving enforcement to about 250 federal agents. Supporters of repeal said 13,000 indictments had produced only 18 convictions.", [NY23]),
            ("National Prohibition ended a decade later, on December 5, 1933, when the 21st Amendment was ratified. States could still keep their own bans.", [REPEAL]),
            ("Colorado and Washington legalized cannabis for adults in 2012 while the federal ban stood. As of 2026, 24 states and D.C. allow it.", [PEW]),
            ("Patients in 40 states had a state right-to-try law before Congress passed one in 2018.", [RTT]),
            ("Moving power down cuts both ways. Homebrewing became legal under federal law in 1979, but Alabama and Mississippi kept their bans until 2013.", [BREW]),
            ("The Free State Project started in 2001 with a goal of getting 20,000 liberty-minded people to move to one small state. It announced 20,000 pledges to move to New Hampshire on February 3, 2016. About 2,000 members had already moved by then.", [FSP, FSP2]),
        ],
        town=[
            "Run for the seats that decide things close to home: township trustee, school board, zoning board, soil and water. Many have nobody running.",
            "Show up when a neighbor wants to build. Zoning boards hear from the people who say no. Make them hear from the people who say yes.",
            "Learn which decisions your town can make on its own and which ones the state took away. Each one is a fight you can pick.",
        ],
        party=[
            "Find one federal ban your state spends its own police time enforcing, and push your state to stop, the way New York did with Prohibition in 1923.",
            "Write a rights floor: a state law that stops towns from banning peaceful things, like Texas did for lemonade stands.",
            "Build county and township groups, not just a state committee. Power you push down needs people there to use it.",
        ],
        you=[
            "Write down who represents you at every level: township or city, county, school board and state.",
            "Go to one local meeting where a decision gets made, not a party meeting.",
            "If you're moving anyway, look at which states have done the most on steps 1 to 4.",
        ],
        msg="Washington can't see your street. Your town can. Make decisions where people can see them and fix them.",
        trap=("Trading a big boss for a small one.", "A county that bans what the state allows isn't progress. Push power down and protect individual rights at every level, or you just move the problem closer to home."),
        related=[("../states/index.html", "Find your state"), ("../organize/structure.html", "Build from the precinct up"), ("../causes/housing.html", "Housing")],
    ),
    dict(
        slug="hand-it-back", icon="heart", title="Hand it back",
        short="Let people run services they already run well on their own, and test every handoff before the state lets go.",
        covers="Volunteers, mutual aid, contract cities",
        lead="Last, hand services back to people who'll run them voluntarily. This step comes last on purpose: it only works when the replacement is already standing.",
        why=("<p>This is the step people picture when they hear \"libertarian,\" and it's the one most likely to fail if you rush it. The book's warning fits here better than anywhere: "
             "take rules away without redesigning the system, and you get new gatekeepers instead of freedom.</p>"
             "<p>So build first. Grow the volunteer, charity and private options until the government version isn't needed, then let it go. "
             "Test every handoff, measure it, publish the results and be ready to change course. This is the least tested step on the road, which is exactly why it comes after the tested ones.</p>"),
        quote=("Remove constraints without redesigning the system, and you amplify asymmetry, selection pressure, and new gatekeepers—not autonomy.", "chapter 2"),
        proof=[
            ("Volunteers make up 62% of U.S. firefighters, and 18,873 of the nation's 29,452 fire departments are all volunteer. Their donated time saves local governments an estimated $46.9 billion a year.", [FIRE]),
            ("In 2005, Sandy Springs, Georgia, started running most city services through private contractors. Around 2010, splitting the work among several firms was expected to save about $7 million a year. In 2019 the city moved to a mix of contractors and city staff, and it reports savings from bringing some services back in-house too. Treat it as an experiment with a lesson: test, measure and keep what works.", [SANDY]),
            ("Steps 2 and 3 already handed some things back. Seven states let neighbors sell most homemade food without a state inspection, and 18 states let families take education money to the school they choose.", [FOOD7, SC18]),
        ],
        town=[
            "Join or give to your volunteer fire department, food bank or mutual aid group. They're the replacement, and they need people now.",
            "Ask your city which services it already contracts out, what it pays, and how that compares with doing it in-house.",
            "Start something small that government does badly: a neighborhood cleanup, a tool library, rides to appointments for seniors.",
        ],
        party=[
            "Run a pilot, not a purge. Pick one service, hand it to a contractor or nonprofit for two years with clear measures, and publish the results either way.",
            "Look for state rules that block volunteers, like permits for charity events or limits on who can give rides or share food, and work to remove them.",
            "Celebrate the people already doing it. Name the best volunteer group in each county every year.",
        ],
        you=[
            "Volunteer two hours with a group that does something government also does.",
            "Ask that group which rule or permit slows them down most, and bring the answer to your state party.",
            "Pay a neighbor for something they do well instead of waiting for a program.",
        ],
        msg="Most fire departments in America already run on volunteers. People take care of each other when government gets out of the way.",
        trap=("Pulling the rug.", "Ending a service before the replacement can carry the load hurts the people who depend on it, and it hands the other side its best argument."),
        related=[("../causes/index.html", "All causes"), ("../organize/field.html", "Talk to voters"), ("../fundraise/models.html", "Charity and giving models")],
    ),
]

N = len(STEPS)


def build():
    index()
    for i, s in enumerate(STEPS):
        step_page(i, s)
    debate()


def road_svg():
    """Decorative-plus: a road with six numbered stops that forks into two destinations. The list below repeats every word."""
    stops = [(68, 141), (165, 112), (260, 150), (355, 112), (450, 150), (545, 112)]
    q = ['<path d="M10 160 C 60 160, 100 100, 165 112 S 230 160, 260 150 S 320 100, 355 112 S 420 160, 450 150 S 520 100, 560 112 C 600 118, 610 120, 630 120" '
         'fill="none" stroke="#fffdf5" stroke-width="30" stroke-linecap="round"/>',
         '<path d="M10 160 C 60 160, 100 100, 165 112 S 230 160, 260 150 S 320 100, 355 112 S 420 160, 450 150 S 520 100, 560 112 C 600 118, 610 120, 630 120" '
         'fill="none" stroke="#f5c400" stroke-width="3" stroke-dasharray="10 9"/>',
         '<path d="M630 120 C 660 120, 670 70, 712 62" fill="none" stroke="#fffdf5" stroke-width="22" stroke-linecap="round"/>',
         '<path d="M630 120 C 660 120, 670 170, 712 178" fill="none" stroke="#fffdf5" stroke-width="22" stroke-linecap="round"/>']
    for i, (x, y) in enumerate(stops):
        q.append(f'<circle cx="{x}" cy="{y}" r="19" fill="#f5c400" stroke="#1a1a1a" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 7}" font-size="20" font-weight="800" text-anchor="middle" fill="#1a1a1a">{i + 1}</text>')
    q.append('<text x="14" y="206" font-size="20" font-weight="800" fill="#ffffff">Today</text>')
    q.append('<text x="726" y="58" font-size="20" font-weight="800" fill="#ffffff">A small state</text>')
    q.append('<text x="726" y="184" font-size="20" font-weight="800" fill="#ffffff">No state</text>')
    desc = ("A winding road starts at Today and passes six numbered stops: 1 Stop the harm, 2 Tear up the permission slips, 3 Open the exits, "
            "4 Cap it and set a clock, 5 Push power down, 6 Hand it back. After stop 6 the road forks. One branch leads to A small state, the other to No state.")
    return ('<svg viewBox="0 0 880 230" role="img" aria-labelledby="road-t road-d"><title id="road-t">The road from today to less government</title>'
            f'<desc id="road-d">{e(desc)}</desc>' + "".join(q) + '</svg>')


def steps_list(prefix="", mini=False):
    items = []
    for i, s in enumerate(STEPS):
        href = f"{prefix}{s['slug']}.html"
        if mini:
            items.append(f'<li><span class="stepnum" aria-hidden="true">{i + 1}</span>'
                         f'<a href="{href}"><span class="sr">Step {i + 1}: </span>{e(s["title"])}</a></li>')
        else:
            items.append(f'<li><span class="stepnum" aria-hidden="true">{i + 1}</span>'
                         f'<a class="card cardlink" href="{href}">{ic(s["icon"])}<p class="kicker">Step {i + 1} of {N}</p>'
                         f'<h3>{e(s["title"])}</h3><p>{e(s["short"])}</p><p class="src">Starts with: {e(s["covers"])}</p></a></li>')
    cls = "steps mini" if mini else "steps"
    return f'<ol class="{cls}" role="list">' + "".join(items) + '</ol>'


def mini_road(prefix):
    """Used on the home, Learn and Organize pages."""
    return steps_list(prefix, mini=True)


def index():
    proof_rows = [
        (1, "Ohio voters legalized cannabis for adults in 2023 with 57.19% of the vote.", OH2),
        (1, "New Mexico's legislature voted unanimously in 2015 to end civil forfeiture without a criminal conviction.", NM),
        (2, "Arizona became the first state to recognize out-of-state job licenses in 2019. By 2025, 28 states had some form of it.", AZL),
        (2, "Wyoming let people sell most homemade food to informed buyers without a license in 2015.", WY),
        (3, "Arizona opened education savings accounts to every K-12 student in 2022.", ESA),
        (3, "After airline deregulation in 1978, the median airfare fell almost 40% after inflation from 1980 to 2005.", AIR2),
        (4, "Colorado voters capped state spending in 1992, and taxpayers get refunds when the state collects too much.", TABOR),
        (4, "Texas has abolished 95 state agencies through sunset reviews since 1977.", SUNTX),
        (5, "New York stopped enforcing Prohibition in 1923, a decade before national repeal.", NY23),
        (6, "Volunteers make up 62% of U.S. firefighters.", FIRE),
    ]
    rows = "".join(f'<tr><td><a href="{STEPS[n - 1]["slug"]}.html">{n}. {e(STEPS[n - 1]["title"])}</a></td><td>{e(t)}</td><td>{S(u)}</td></tr>'
                   for n, t, u in proof_rows)
    body = f"""
<div class="planart">{road_svg()}</div>

<h2>The 60-second version</h2>
<p>"No government" isn't a plan. It's a destination. A plan says what you do first, what you do next, and how you keep what you win.</p>
<p>Start with the harm people feel today, like jail for a plant or police keeping cash from people never charged. Then clear the permission slips that make normal life hard. Then give people a way out of the systems that fail them. Lock in every win with spending caps and expiration dates. Push what's left down to the state, the town and the neighborhood. Last, hand it back to people who'll do it voluntarily. Each step makes the next one easier, because people trust what they can see.</p>

<h2 id="road">The road, step by step</h2>
{steps_list()}

<h2 id="end">Where the road ends</h2>
<p>Libertarians split on the last mile. That's fine, because the first five steps are the same either way.</p>
<div class="grid">
<div class="card">{ic("signpost")}<h3>A small state</h3><p>Government shrinks to courts, police and defense, and stops there. In his 1974 book Anarchy, State, and Utopia, philosopher Robert Nozick argued for this kind of minimal state: a "night watchman" that protects people against violence, theft and fraud, and does nothing else. Most minarchists and classical liberals stop here.</p><p>{S(NOZICK)}</p></div>
<div class="card">{ic("road")}<h3>No state</h3><p>Anarcho-capitalists and agorists keep going until courts, security and everything else run on voluntary deals. It's the least tested stretch of road, which is one more reason to walk the tested part first and learn on the way.</p><p><a href="../learn/factions.html">More on the factions</a></p></div>
</div>
<h3>What both ends share</h3>
<p>Either way, the place we're heading has the same shape. Nobody, not a king, a mayor or a majority, gets to use force on peaceful people, and the rules are the same for everyone. That's the balance point: equal rights, nobody picking winners, and mistakes that teach instead of ruin. The book puts that last part as "Consequences that teach—not consequences that end participation."</p>

<h2 id="why">Why this order</h2>
<ol class="facts">
<li><b>Start where people are stuck.</b> The book's first question is "Where are voters technically free—but practically stuck? That's where you start." Steps 1 and 2 are where people are most stuck.</li>
<li><b>Win what people can feel.</b> "Voters trust what they can see." Someone whose record got sealed, or whose license now works across the state line, believes the next step will work too.</li>
<li><b>Build the exit before you close the door.</b> The book says libertarianism "removes constraints— but fails to redesign the system that remains." Taking away a program with nothing in its place feels like loss, "And voters reject loss." So exits come at step 3 and handoffs wait until step 6.</li>
<li><b>Lock in every win.</b> Rules creep back. Caps and sunsets at step 4 keep the road from washing out behind you.</li>
<li><b>Move decisions closer to people.</b> Small units find and fix mistakes faster, as long as individual rights hold at every level.</li>
<li><b>Alignment over purity.</b> You don't need everyone to agree on the end of the road to walk the next mile together. "Agreement is total. Alignment is partial—and enough to win."</li>
</ol>
<div class="note"><p><b>Whose order is this?</b> {BOOK} is a campaign manual. It gives the method: start where people are stuck, win what they can see, make failure survivable, and build alignment over purity. It doesn't set an order for reforms. The order on this page is ours, built on that method. If you think step 4 should come first, make the case. <a href="../about.html#fix">Tell us</a>, and we'll change it if you're right.</p></div>

<h2 id="proof">Every step has been done somewhere</h2>
<div class="tablewrap"><table><caption>Real reforms, one or two for each step</caption>
<thead><tr><th scope="col">Step</th><th scope="col">What happened</th><th scope="col">Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p>Each step's page has more, with what it looks like where you live and what you can do this week.</p>

<h2 id="debate">The fight over how fast</h2>
<p>Some libertarians would end the state tomorrow if they could. Some want to stop at a small one. Some would rather go around it. And plenty agree with most of it but won't spend a Saturday fighting for it. Here's the whole debate, fairly, with who said what.</p>
<p class="row"><a class="btn gold" href="gradual-or-abolish.html">Push the button, or take the loaf?</a></p>

<h2 id="start">Where to start this week</h2>
<ul class="facts">
<li><b>If you have an hour:</b> pick the step that makes you angriest and read its page. Each one ends with three things to do this week.</li>
<li><b>If you run a state party or county group:</b> pick one bill from step 1 or 2, where support is widest, and make it the thing your group is known for. The <a href="../organize/index.html">organizing playbook</a> shows how.</li>
<li><b>If you're running for office:</b> use the 10-second message on each step page. Voters ask how long, how much and what happens if they mess up, and every step answers one of those. More in <a href="../organize/messaging.html">messages that land</a>.</li>
</ul>
"""
    page("plan/index.html", "The plan: how we get from more government to less",
         "A practical, step-by-step road from today's government to a much smaller one: what comes first and why, real reforms that worked, and what you can do this week.",
         "The plan: from more state to less, one step at a time", body,
         lead="Nobody gets to push a button and end the state. So here's the road instead: six steps, in order, each one already done somewhere in America. Walk it with us whether you want a small government or none.",
         kicker="The plan", crumbs=[("The plan", "")])


def stepnav(cur):
    items = []
    for i, s in enumerate(STEPS):
        a = ' aria-current="page"' if i == cur else ""
        items.append(f'<li><a href="{s["slug"]}.html"{a}><span class="dot" aria-hidden="true">{i + 1}</span>'
                     f'<span class="lbl"><span class="sr">Step {i + 1}: </span>{e(s["title"])}</span></a></li>')
    return f'<nav class="stepnav" aria-label="Steps on the road"><ol role="list">{"".join(items)}</ol></nav>'


def step_page(i, s):
    proof = "".join(f'<li>{e(t)} {S(*u)}</li>' for t, u in s["proof"])
    town = "".join(f"<li>{e(x)}</li>" for x in s["town"])
    party = "".join(f"<li>{e(x)}</li>" for x in s["party"])
    you = "".join(f"<li>{e(x)}</li>" for x in s["you"])
    rel = ", ".join(f'<a href="{h}">{e(t)}</a>' for h, t in s["related"])
    note = s.get("msg_note", 'Built on the book\'s pattern: what the system does, why it hurts you, what you get when it\'s gone. More in <a href="../organize/messaging.html">messages that land</a>.')
    prev_b = (f'<a class="btn ghost" href="{STEPS[i - 1]["slug"]}.html">Back: step {i}, {e(STEPS[i - 1]["title"])}</a>' if i > 0
              else '<a class="btn ghost" href="index.html">Back to the plan</a>')
    next_b = (f'<a class="btn gold" href="{STEPS[i + 1]["slug"]}.html">Next: step {i + 2}, {e(STEPS[i + 1]["title"])}</a>' if i < N - 1
              else '<a class="btn gold" href="index.html#end">Next: where the road ends</a>')
    tt, td = s["trap"]
    body = f"""
{stepnav(i)}
<p class="lead">{e(s["lead"])}</p>
<h2>Why it comes here</h2>
{s["why"]}
{bq(e(s["quote"][0]), s["quote"][1])}
<h2>Proof it works</h2>
<ul class="facts">{proof}</ul>
<h2>What it looks like where you live</h2>
<div class="grid stack">
<div class="card">{ic("map")}<h3>In your town</h3><ul class="facts">{town}</ul></div>
<div class="card">{ic("people")}<h3>Your state party</h3><ul class="facts">{party}</ul></div>
<div class="card">{ic("clock")}<h3>You, this week</h3><ul class="facts">{you}</ul></div>
</div>
<div class="note"><p><b>Say it in 10 seconds:</b> "{e(s["msg"])}"</p><p class="src">{note}</p></div>
<h2>Watch out for</h2>
<p><b>{e(tt)}</b> {e(td)}</p>
<p>Related: {rel}.</p>
<p class="row">{prev_b}{next_b}</p>
"""
    page(f"plan/{s['slug']}.html", f"Step {i + 1}: {s['title']}",
         f"Step {i + 1} of the plan for less government: {s['short']}",
         f"Step {i + 1}: {e(s['title'])}", body, kicker=f"The plan, step {i + 1} of {N}",
         crumbs=CR + [(f"Step {i + 1}", "")], wide=False)


def debate():
    READ1 = "https://fee.org/articles/id-push-the-buttonto-establish-freedom-right-now/"
    READ2 = "https://fee.org/ebooks/id-push-the-button"
    ROTH = "https://mises.org/mises-daily/do-you-hate-state"
    ROTH2 = "https://reason.com/2015/07/19/murray-rothbard-on-libertarian-strategy"
    RICH = "https://reason.com/2015/07/12/sheldon-richman-on-libertarian-strategy/"
    ESP = "https://mises.org/mises-wire/gradualism-or-abolitionism"
    KON = "https://theanarchistlibrary.org/library/samuel-edward-konkin-iii-new-libertarian-manifesto.html"
    SSM = "https://news.gallup.com/poll/691139/record-party-divide-years-sex-marriage-ruling.aspx"
    MIP = "https://news.gallup.com/file/poll/659009/2025_04_09%20Energy%20Topline%20and%20Tabs_MIP.pdf"
    DFP = "https://reason.com/2020/02/06/what-americans-think-about-prostitution-laws/"
    rows = [
        ("Abolitionists", "No state", "Any step that takes force away and doesn't create new power", "Keep the goal honest and the pressure on"),
        ("Minarchists and gradualists", "A small state for courts, police and defense", "Steps 1 to 5, and much of step 6", "Write the bills and win the votes"),
        ("Agorists", "Around the state, not through it", "Steps that make legal what people already do", "Build the alternatives step 6 needs"),
        ("The movers", "A free state first, then more", "Anything that works locally", "Put enough people in one place to win local seats"),
        ("The \"you do you\" crowd", "Wherever life gets easier", "Steps that make their own life easier", "The votes that pass ballot measures"),
    ]
    trows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in rows)
    types = [("purist", "Purist"), ("ancap", "Anarcho-Capitalist"), ("agorist", "Agorist"), ("minarchist", "Minarchist"),
             ("pragmatist", "Pragmatist"), ("smalll", "Small-l Libertarian")]
    tlinks = ", ".join(f'<a href="../types/{t}.html">{n}</a>' for t, n in types)
    body = f"""
<h2 id="button">The button: end it now</h2>
<p>In April 1946, Leonard Read gave a talk in Detroit called "I'd Push the Button," a month after he founded the Foundation for Economic Education. He opened with a picture: "If there were a button on this rostrum, the pressing of which would release all wage and price controls instantaneously," he said, "I would put my finger on it and push!" {S(READ1, READ2)}</p>
<p>In 1977, Murray Rothbard made the button the test of a real abolitionist: someone who "would blister his thumb pushing a button that would abolish the State immediately, if such a button existed." You'll often see it quoted as "blister my thumb." His actual words were "his thumb." {S(ROTH)}</p>
<p><b>Their case:</b> if the state is wrong, it's wrong today. Going slow means more people jailed, taxed and pushed around while you wait. And people who get comfortable with small steps tend to stop pushing.</p>

<h2 id="loaf">The loaf: take what you can get, never lose the goal</h2>
<p>Even Rothbard didn't sit and wait for a button. In the same essay, he said the abolitionist "will take a bit of the loaf if necessary—while always preferring the whole loaf if he can achieve it." {S(ROTH)}</p>
<p>In his book For a New Liberty, he set the rule for which partial steps count: "A short-run demand may not go as far as we would like, but it should always be consistent with the final end." {S(ROTH2)}</p>
<p>A 2006 Mises Institute essay by Albert Esplugas put the middle ground plainly: "Where it is not possible to take giant leaps it is not condemnable but preferable to take small ones." {S(ESP)}</p>

<h2 id="small">The small state: stop at the night watchman</h2>
<p>Robert Nozick's 1974 book Anarchy, State, and Utopia argued for a minimal state, one that protects people against violence, theft and fraud, and not for no state at all. {S(NOZICK)}</p>
<p>Writer Sheldon Richman argued that limited reforms, like the trucking deregulation of the 1970s, were worth doing even though they fell far short of libertarian goals. {S(RICH)}</p>
<p><b>Their case:</b> every step that works earns trust for the next one. You can't sell a stateless society to people who have never seen a permit office that works. And a small state is a real place to stop, not just a rest area.</p>

<h2 id="around">Around the state: the agorists</h2>
<p>In his New Libertarian Manifesto (1980), Samuel Edward Konkin III called for counter-economics, living around the state instead of working through it. He mocked the effort to win liberty through political parties as "Partyarchy." "Agorism" comes from agora, the Greek word for an open marketplace. In his words: "The actual practice of human actions that evade, avoid, and defy the State is counter-economic activity." {S(KON)}</p>
<p><b>Their case:</b> you don't need a vote to live free. Every private deal, homeschooled kid and neighbor-to-neighbor trade shrinks the state's reach today.</p>
<p><b>The catch:</b> going around the state can mean breaking laws, and the people who get caught pay the price. This site doesn't tell anyone to do that. The legal parts of the agorist toolkit, like co-ops, private arbitration and mutual aid, are exactly what step 6 needs.</p>

<h2 id="movers">The movers: pick one place and win it</h2>
<p>The Free State Project started in 2001 with a goal of getting 20,000 liberty-minded people to move to one small state. It announced 20,000 pledges to move to New Hampshire on February 3, 2016, and about 2,000 members had already moved by then. {S(FSP, FSP2)}</p>
<p><b>Their case:</b> spread thin, libertarians lose everywhere. Packed into one place, they can win local seats and show the rest of the country what works. That's step 5 with a moving truck.</p>

<h2 id="you-do-you">The "you do you" crowd</h2>
<p>Plenty of people agree with libertarians on a lot and still won't spend a Saturday on it. The numbers show the gap. In an October 2025 Gallup poll, 64% of U.S. adults said marijuana should be legal. In May 2025, 68% supported same-sex marriage. But in Gallup's March 2025 poll, only 1% named drugs, and 1% named LGBTQ rights, as the country's most important problem. {S(GALLUP_MJ, SSM, MIP)}</p>
<p>Even sex work, the cause most politicians won't touch, had 52% support for decriminalizing it and 35% against in a November 2019 poll by Data for Progress, a progressive think tank. It's the newest national poll we found. {S(DFP)}</p>
<p><b>Their case:</b> live and let live is the whole point. Not everyone has to be an activist, and freedom includes the freedom not to care about politics.</p>
<p><b>How to work with them:</b> don't ask them to fight. Ask them to sign one petition, cast one vote, or just not stand in the way. The book splits any coalition into rings: the committed core, people who agree on outcomes, and an outer ring who mostly want relief. Its rule is "You win by expanding outward— not arguing inward."</p>

<h2 id="together">How they all fit on one road</h2>
<div class="tablewrap"><table><caption>Five camps, one road</caption>
<thead><tr><th scope="col">Who</th><th scope="col">Where they'd stop</th><th scope="col">What they'll say yes to</th><th scope="col">How they help</th></tr></thead>
<tbody>{trows}</tbody></table></div>

<h2 id="test">One test everybody can use</h2>
<p>Rothbard's rule and the book's rule land in the same place. Before you back a reform, ask one question: does this take force out of someone's life, or does it just move the force to a different office?</p>
<ul class="facts">
<li><b>If it takes force out,</b> it's on the road, whatever you think the end looks like. Back it.</li>
<li><b>If it adds a new agency, fee or gatekeeper,</b> it's a detour, however libertarian it sounds.</li>
</ul>
{bq("Agreement is total. Alignment is partial—and enough to win.", "chapter 10")}
{bq("Purity feels good. Alignment wins.", "chapter 10")}

<h2 id="which">Which one are you?</h2>
<p>The <a href="../quiz.html">quiz</a> sorts you into one of 15 types, and several of them line up with the camps here: {tlinks}. Take it, then come back and pick your step.</p>
<p class="row"><a class="btn gold" href="index.html">Back to the plan</a><a class="btn ghost" href="../quiz.html">Take the quiz</a></p>
"""
    page("plan/gradual-or-abolish.html", "Push the button or take the loaf? The fight over how fast",
         "Abolitionists, gradualists, minarchists, agorists, the movers and the \"you do you\" crowd: how libertarians disagree about how fast to shrink the state, in their own words.",
         "Push the button, or take the loaf?", body,
         lead="Libertarians agree on less government. They fight about how fast, how far, and whether politics is even the way to get there. Here's every side, fairly, in their own words.",
         kicker="The plan: the debate", crumbs=CR + [("The debate", "")], wide=False)
