# saicomsci.github.io

Personal academic site — Saikat Mondal, PhD Scholar, IIT Jodhpur.

Static HTML, no build dependencies, no framework. Content lives in plain data
files; the pages are prerendered so they work with JavaScript disabled.

## Layout

```
index.html, education.html, …   ← prerendered pages (what GitHub Pages serves)
templates/                      ← the same pages with empty mount points (source)
data/                           ← all site content — edit these
js/                             ← client-side renderers (hydration)
assets/style.css                ← all styling
images/
tools/                          ← the prerender build
```

## Editing content

Everything you'd normally want to change is in `data/`:

| File | Contents |
|---|---|
| `profile.js` | Name, role, photo, contact links, bio, research interests |
| `news.js` | Home-page news items (newest first) |
| `publications.js` | Papers |
| `projects.js` | Projects |
| `education.js` | Degrees |
| `experience.js` | Positions |
| `skills.js` | Skill categories |
| `certifications.js` | Certifications and honours |

After editing any of them, rebuild:

```bash
python3 tools/prerender.py --out .
```

That regenerates the seven HTML pages in place. Python 3 standard library only —
nothing to install. **If you skip this step your edits won't appear** for
visitors whose browser doesn't run the scripts, and the page source will be
stale.

### Adding a publication

```js
{
  title:        'Paper Title Here',
  image:        'images/pubs/teaser.png',                          // optional
  authors:      ['Saikat Mondal', 'Co Author', 'Third Author'],
  venue:        'EMNLP 2026',
  venueFullName:'Conference on Empirical Methods in Natural Language Processing',
  year:         '2026',
  links: [
    { label: 'Paper', url: 'https://...' },
    { label: 'Code',  url: 'https://...' },
    { label: 'DOI',   url: 'https://doi.org/...' },
  ],
},
```

A card shows the teaser figure, the title, the author byline, the venue and
year, and the link buttons — in that order.

`image`, `authors`, `year` and `links` are all optional; leave any of them out
and that part simply isn't rendered.

Put teaser figures in `images/pubs/`. They render into a fixed 200px 4:3 plate
and are *contained*, never cropped, so any aspect ratio is safe — the column
stays even however the source figures are proportioned. Roughly 480px wide is
plenty (the plate is 200 CSS px, so that covers retina); shrink anything larger
before committing it. Cards without a figure just show the index number.

Authors are listed verbatim, in order, separated by commas. Any entry matching
the `name` in `profile.js` is bolded and underlined automatically, so there's
nothing to mark up by hand.

Link labels choose their own icon: *DOI* gets a link icon, *Paper/PDF/arXiv* a
document icon and the filled primary button, *Code/GitHub/repo* the GitHub mark,
anything else an external-link arrow.

## Why prerendered

The pages used to be empty shells filled in by JavaScript at runtime. That meant
crawlers and link-preview bots saw nothing, and one JS error blanked the whole
site. Now the markup is written into the HTML ahead of time, and the scripts
still run on top of it — so the page works either way.

See `tools/README.md` for how the build works.

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. A server is required — the ES modules won't
load over `file://`.

## Deploying

GitHub Pages serves this from the repository root:

```bash
git add -A
git commit -m "Update site"
git push
```
