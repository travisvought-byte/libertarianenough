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

## Search engines, ads and counting

- **Sitemap dates.** Each `<lastmod>` in `sitemap.xml` is the day that page's title, description or main content last changed. `_build/lastmod.json` keeps a fingerprint and a date for every page; the build gives a page today's date (UTC) only when its fingerprint changes, so a header, footer or script change doesn't make every page look new. Commit the file with the pages.
- **IndexNow.** `.github/workflows/indexnow.yml` sends Bing, Yandex and the other IndexNow engines the address of every sitemap page a push to `main` changed, after giving GitHub Pages two minutes to publish. The key is `INDEXNOW_KEY` in `_build/core.py`, published by the build as `<key>.txt` at the site root. Run the workflow by hand with "all" ticked to send every page.
- **Google AdSense.** `ADSENSE` in `_build/core.py` holds the publisher ID. The build writes `ads.txt` from it and puts Google's code in the head of every content page, asking for non-personalized ads only. `NO_ADS` lists the pages that never load it: the 404, About (which holds the privacy notes) and Results, whose address carries the visitor's answers. The quiz embed carries no ads. There are no hand-placed ad slots, so ads appear only where Auto ads is switched on for this site in the AdSense account.
- **Visit counter.** GoatCounter (`GC` in `_build/core.py`) is on every page and the quiz embed, counted under `/libertarianenough.org/...` on the shared counter. It sets no cookie.

## Corrections

Spot something wrong, or want your state's page claimed? Open an issue.
