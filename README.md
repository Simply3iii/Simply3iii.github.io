# simply3iii.github.io

My site: what I'm working on, my projects, and my CV. Live at **https://simply3iii.github.io**.

## Editing (no installing needed)

Everything you'd want to change is a Markdown file in **`content/`**:

| To change | Edit |
|---|---|
| Name, tagline, photo, links, and the "Right now" text | `content/index.md` |
| The CV page | `content/cv.md` |
| A project | `content/projects/<name>.md` |
| Add a log entry | add `content/log/YYYY-MM-DD-short-title.md` (copy an existing one) |
| Add a project | add `content/projects/short-name.md` (copy an existing one) |

On github.com: open the file, click the pencil, edit, **Commit changes**. The site rebuilds
itself in about a minute (watch the **Actions** tab).

### The top of each file

The block between the two `---` lines sets things like the title, summary, tags, cover picture
and whether it's featured on the home page. Below it is normal Markdown:
`## Heading`, `- bullet`, `**bold**`, `[link](url)`, `![caption](/static/img/...)`.

### Pictures

Put them in `static/img/<project>/` (upload through github.com: **Add file → Upload files**)
and refer to them as `/static/img/<project>/name.jpg`. Keep them under ~1600 px wide.
Remove location data from phone photos first.

### Videos

Paste this into a page, with your video's ID:

    <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" allowfullscreen></iframe></div>

## Keep off this site

Phone number, home address, date of birth, student numbers, participants' data, coursework
code, and anything from the PhD that Adam hasn't said is fine to make public.

## Previewing on your laptop (optional)

    pip install markdown pyyaml
    python build.py
    python -m http.server -d _site
