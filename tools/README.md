# Prerender build

Generates a fully static copy of the site, so every page ships real HTML instead
of an empty shell that only fills in once JavaScript runs.

## Why

The pages in the repo root are templates: `<div id="publications-list"></div>`
and friends are empty until `js/render.js` populates them in the browser. That
means crawlers and link-preview bots that don't execute JS see a blank page, and
a single JS error blanks the whole site.

The build reads the same `data/*.js` files and writes the markup into the HTML
ahead of time. The page scripts stay in the output, so with JS enabled the pages
still hydrate exactly as before — the render is idempotent, producing the same
markup that's already there.

## Usage

```bash
python3 tools/prerender.py --out .      # rebuild the pages in place (usual case)
python3 tools/prerender.py              # → dist/, leaving the sources untouched
python3 tools/prerender.py --year 2026  # pin the footer copyright year
```

Templates are read from `templates/` when that directory exists, otherwise from
the repo root. `--out .` rewrites the pages beside them and copies nothing.

No dependencies — standard library only. Rerun it after **any** edit to
`data/*.js`, `js/render.js`, or the HTML templates.

## What it does

1. Parses `export const … = …` out of each `data/*.js` (`tools/jsdata.py`).
2. Renders each section with Python functions mirroring `js/render.js`.
3. Injects the markup into the empty `id="…"` mount points in each page.
4. Sets the profile photo's `src`/`alt`, which `js/main.js` normally assigns.
5. Adds a `<noscript>` block so the mobile nav is usable without JS — the
   hamburger button needs a JS listener, so the links are shown inline instead.
6. Copies `assets/`, `images/`, `js/`, `data/` and `.nojekyll` across.

## Keeping it in sync

`tools/prerender.py` duplicates the renderers in `js/render.js`. If you change
the markup in one, change it in the other, or the prerendered HTML and the
hydrated HTML will disagree. The renderers are small and the function names
match one-to-one (`renderTimeline` → `render_timeline`, and so on).

## Deploying

GitHub Pages serves from either the repo root or `/docs` — not `/dist`. So:

```bash
python3 tools/prerender.py --out docs
git add docs && git commit -m "Rebuild static site"
git push
```

Then set **Settings → Pages → Source** to `main` / `/docs`.
