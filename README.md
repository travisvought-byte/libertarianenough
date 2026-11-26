# Libertarian Enough

The site behind [libertarianenough.org](https://libertarianenough.org): a cheeky "are you libertarian enough?" quiz up front, and behind it a plain-English guide to the libertarian movement plus organizing and fundraising playbooks for state affiliates, local groups and candidates.

An independent libertarian organizing project. Not affiliated with the Libertarian National Committee or any state party.

## How it's built

Plain static HTML on GitHub Pages. No server, no database, no accounts. The quiz scores in the visitor's browser and never sends answers anywhere.

- `_build/` holds the Python generator. Run `python3 _build/build.py` from the repo root and it rewrites every page, `assets/data.js`, `sitemap.xml`, `robots.txt` and `CNAME`.
- `_build/quizdata.py` holds the questions, types, verdicts and the reference people on the chart.
- `data/` holds the sourced research (states, history, voices, factions, controversies, demographics, causes, cannabis law) the pages are built from.
- `assets/` holds the stylesheet, icons, quiz and results scripts.

Edit the generator or the data, then rebuild. Don't hand-edit the generated HTML.

## Corrections

Spot something wrong, or want your state's page claimed? Open an issue.
