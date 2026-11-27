#!/usr/bin/env python3
"""Builds the Libertarian Enough static site. Run from anywhere: python3 _build/build.py"""
import os, sys, json, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
from core import ROOT, SITE
import quizdata
import sec_quiz, sec_learn, sec_plan, sec_causes, sec_org, sec_states, sec_misc, sec_help, sec_life
import lifedata


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


LASTMOD = os.path.join(ROOT, "_build", "lastmod.json")


def lastmods(paths):
    """The date each page's content last changed, for the sitemap. _build/lastmod.json keeps a fingerprint and a date
    per page; a page whose title, description or main content changed since the last build gets today's date (UTC).
    Header, footer and script changes don't count, so a template change doesn't make every page look new."""
    try:
        with open(LASTMOD) as f:
            known = json.load(f)
    except FileNotFoundError:
        known = {}
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    out, keep = {}, {}
    for u in paths:
        with open(os.path.join(ROOT, u)) as f:
            key = core.content_key(f.read())
        old = known.get(u)
        date = old["date"] if old and old.get("key") == key else today
        keep[u] = {"key": key, "date": date}
        out[u] = date
    with open(LASTMOD, "w") as f:
        json.dump(keep, f, indent=1, sort_keys=True)
        f.write("\n")
    return out


def main():
    js = {
        "version": quizdata.VERSION,
        "answers": quizdata.ANSWERS,
        "hedge": quizdata.HEDGE,
        "verdicts": quizdata.VERDICTS,
        "questions": quizdata.QUESTIONS,
        "types": quizdata.TYPES,
        "refs": quizdata.REFS,
        "areas": quizdata.AREAS,
        "methods": quizdata.METHODS,
    }
    write("assets/data.js", "window.LE=" + json.dumps(js, ensure_ascii=False, separators=(",", ":")) + ";\n")
    life = {"version": lifedata.VERSION, "chapters": lifedata.CHAPTERS, "scenes": lifedata.SCENES, "order": lifedata.ORDER,
            "classes": lifedata.CLASSES, "hows": lifedata.HOWS, "areas": lifedata.LAREAS}
    write("assets/life-data.js", "window.LIFE=" + json.dumps(life, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for m in (sec_quiz, sec_learn, sec_plan, sec_causes, sec_org, sec_states, sec_misc, sec_help, sec_life):
        m.build()
    # 404 is served at any depth, so its links must be absolute.
    p = os.path.join(ROOT, "404.html")
    s = open(p).read()
    s = re.sub(r'(href|src)="(?!https?:|/|#|mailto:)([^"]*)"', r'\1="/\2"', s)
    open(p, "w").write(s)
    listed = [u for u in sorted(set(core.PAGES)) if u not in core.NO_INDEX]
    dates = lastmods(listed)
    urls = "".join(f"<url><loc>{SITE}/{'' if u == 'index.html' else u}</loc><lastmod>{dates[u]}</lastmod></url>" for u in listed)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1f2a44"/>'
          '<g stroke="#1a1a1a" stroke-width="2" stroke-linejoin="round"><path d="M10 40 6 26l9 6-1-14 8 10 2-14 6 12 5-12 3 13 7-10v14l8-6-3 14z" fill="#f5c400"/>'
          '<path d="M8 42c0-8 12-12 24-12s22 4 26 10c-2 6-10 10-24 10S8 48 8 42z" fill="#fff"/><circle cx="50" cy="40" r="1.8" fill="#1a1a1a" stroke="none"/></g></svg>\n')
    write("CNAME", "libertarianenough.org\n")
    write("ads.txt", f"google.com, {core.ADSENSE.replace('ca-pub-', 'pub-')}, DIRECT, f08c47fec0942fa0\n")
    write(f"{core.INDEXNOW_KEY}.txt", core.INDEXNOW_KEY + "\n")
    write(".nojekyll", "")
    print(f"Built {len(core.PAGES)} pages.")


if __name__ == "__main__":
    main()
