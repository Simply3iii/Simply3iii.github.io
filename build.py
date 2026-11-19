"""Builds the site from the Markdown files in content/ into _site/.

You don't need to run this yourself: GitHub runs it every time you change a file.
To preview on your laptop:  pip install markdown pyyaml  then  python build.py
and open _site/index.html through a local server (python -m http.server -d _site).
"""
import datetime
import html
import pathlib
import re
import shutil

import markdown
import yaml

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "_site"


def load(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    meta = yaml.safe_load(m.group(1)) if m else {}
    body = m.group(2) if m else text
    return meta or {}, body


def md(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists", "attr_list"])


def esc(s):
    return html.escape(str(s or ""))


def fmt_date(d):
    if isinstance(d, str):
        d = datetime.date.fromisoformat(d)
    return d.strftime("%-d %B %Y")


SITE = load(CONTENT / "index.md")[0]


def page(title, body, active="", description=""):
    nav = "".join(
        f'<a href="{href}"{" class=on" if key == active else ""}>{label}</a>'
        for key, href, label in [("home", "/", "Home"), ("projects", "/projects/", "Projects"),
                                 ("log", "/log/", "Log"), ("cv", "/cv/", "CV")]
    )
    full_title = SITE["name"] if not title else f"{title} · {SITE['name']}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description or SITE.get('tagline', ''))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="topbar"><a class="brand" href="/">{esc(SITE['name'])}</a><nav>{nav}</nav></header>
<main class="page">
{body}
</main>
<footer class="foot">
  <span>{esc(SITE['name'])} · Edinburgh</span>
  <span>{" · ".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in SITE.get("links", []))}</span>
</footer>
<div class="lightbox" hidden><img alt=""><p></p></div>
<script src="/static/js/site.js"></script>
</body>
</html>"""


def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def gallery(items):
    if not items:
        return ""
    figs = "".join(
        f'<figure><img src="{esc(i["src"])}" alt="{esc(i.get("caption", ""))}" loading="lazy">'
        f'<figcaption>{esc(i.get("caption", ""))}</figcaption></figure>'
        for i in items
    )
    return f'<div class="gallery reveal">{figs}</div>'


def card(p):
    img = f'<div class="card-img"><img src="{esc(p["cover"])}" alt="" loading="lazy"></div>' if p.get("cover") else ""
    tags = "|".join(esc(t) for t in p.get("tags", []))
    chips = "".join(f"<span>{esc(t)}</span>" for t in p.get("tags", []))
    return f"""<a class="card reveal" href="/projects/{p['slug']}/" data-tags="{tags}">
  {img}
  <div class="card-text"><p class="kicker">{esc(p.get('when', ''))} · {esc(p.get('where_short', p.get('where', '')))}</p>
  <h3>{esc(p['title'])}</h3><p>{esc(p.get('summary', ''))}</p><div class="chips">{chips}</div></div>
</a>"""


# ---------- load everything ----------
projects = []
for f in sorted((CONTENT / "projects").glob("*.md")):
    meta, body = load(f)
    meta["slug"] = f.stem
    meta["body"] = body
    projects.append(meta)
projects.sort(key=lambda p: p.get("order", 99))

posts = []
for f in sorted((CONTENT / "log").glob("*.md")):
    meta, body = load(f)
    meta["slug"] = f.stem
    meta["body"] = body
    meta["date"] = meta.get("date") or datetime.date.fromisoformat(f.stem[:10])
    posts.append(meta)
posts.sort(key=lambda p: str(p["date"]), reverse=True)

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ROOT / "static", OUT / "static")
(OUT / ".nojekyll").write_text("")

# ---------- home ----------
home_meta, home_body = load(CONTENT / "index.md")
links = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in home_meta.get("links", []))
featured = [p for p in projects if p.get("featured")]
latest = posts[:3]
home = f"""
<section class="hero">
  <img class="photo" src="{esc(home_meta.get('photo', ''))}" alt="{esc(home_meta['name'])}">
  <h1>{esc(home_meta['name'])}</h1>
  <p class="tagline">{esc(home_meta.get('tagline', ''))}</p>
  <div class="links">{links}</div>
  <a class="scroll-cue" href="#now" aria-label="Scroll down">↓</a>
</section>
<section id="now" class="reveal prose"><h2>Right now</h2>{md(home_body)}</section>
<section class="reveal"><h2>Things I've made</h2><div class="cards">{''.join(card(p) for p in featured)}</div>
<p class="more"><a href="/projects/">All projects →</a></p></section>
<section class="reveal"><h2>From the log</h2><ol class="timeline">{''.join(
    f'<li><time>{fmt_date(p["date"])}</time><a href="/log/{p["slug"]}/">{esc(p["title"])}</a><p>{esc(p.get("summary", ""))}</p></li>' for p in latest)}</ol>
<p class="more"><a href="/log/">The whole log →</a></p></section>
<section class="reveal cta"><h2>The formal version</h2><p>Education, experience and skills, all in one place.</p><p><a class="button" href="/cv/">Read my CV</a></p></section>
"""
write("index.html", page("", home, "home"))

# ---------- projects ----------
all_tags = sorted({t for p in projects for t in p.get("tags", [])}, key=str.lower)
filters = '<button class="on" data-filter="*">All</button>' + "".join(
    f'<button data-filter="{esc(t)}">{esc(t)}</button>' for t in all_tags)
write("projects/index.html", page("Projects", f"""
<section class="intro"><h1>Projects</h1><p class="tagline">Things I've built, from university and on my own. Tap a tag to filter.</p>
<div class="filters">{filters}</div></section>
<div class="cards">{''.join(card(p) for p in projects)}</div>""", "projects"))

for i, p in enumerate(projects):
    nxt = projects[(i + 1) % len(projects)]
    cover = f'<img class="cover reveal" src="{esc(p["cover"])}" alt="">' if p.get("cover") and p.get("show_cover", True) else ""
    chips = "".join(f"<span>{esc(t)}</span>" for t in p.get("tags", []))
    body = f"""
<article class="prose">
  <p class="kicker"><a href="/projects/">← Projects</a></p>
  <h1>{esc(p['title'])}</h1>
  <p class="meta">{esc(p.get('when', ''))} · {esc(p.get('where', ''))}</p>
  <div class="chips">{chips}</div>
  {cover}
  <div class="reveal">{md(p['body'])}</div>
  {gallery(p.get('gallery'))}
</article>
<p class="next"><a href="/projects/{nxt['slug']}/">Next: {esc(nxt['title'])} →</a></p>"""
    write(f"projects/{p['slug']}/index.html", page(p["title"], body, "projects", p.get("summary", "")))

# ---------- log ----------
items = "".join(
    f'<li class="reveal"><time>{fmt_date(p["date"])}</time><a href="/log/{p["slug"]}/">{esc(p["title"])}</a>'
    f'<p>{esc(p.get("summary", ""))}</p></li>' for p in posts)
write("log/index.html", page("Log", f"""
<section class="intro"><h1>Log</h1><p class="tagline">What I'm working on, as it happens. Short notes, newest first.</p></section>
<ol class="timeline">{items}</ol>""", "log"))
for p in posts:
    write(f"log/{p['slug']}/index.html", page(p["title"], f"""
<article class="prose">
  <p class="kicker"><a href="/log/">← Log</a></p>
  <h1>{esc(p['title'])}</h1><p class="meta">{fmt_date(p['date'])}</p>
  <div class="reveal">{md(p['body'])}</div>{gallery(p.get('gallery'))}
</article>""", "log", p.get("summary", "")))

# ---------- cv ----------
cv_meta, cv_body = load(CONTENT / "cv.md")
pdf = '<p><a class="button" href="/static/cv.pdf">Download as PDF</a></p>' if (ROOT / "static" / "cv.pdf").exists() else ""
write("cv/index.html", page("CV", f"""
<article class="prose cv"><h1>CV</h1>{pdf}<div class="reveal">{md(cv_body)}</div>
<p class="updated">Last updated {esc(cv_meta.get('updated', ''))}</p></article>""", "cv"))

write("404.html", page("Not found", '<section class="intro"><h1>Nothing here</h1><p><a href="/">Back home</a></p></section>'))
print(f"Built {len(projects)} projects, {len(posts)} log entries into {OUT}")
