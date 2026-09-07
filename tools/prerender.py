#!/usr/bin/env python3
"""Prerender the site into dist/ so every page has real HTML without JavaScript.

Mirrors the renderers in js/render.js and js/main.js: reads data/*.js, fills the
empty mount points in each .html file, and copies the static assets across. The
page scripts are kept in the output, so with JS enabled the pages still hydrate
exactly as before.

Usage:  python3 tools/prerender.py [--out dist]
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import jsdata  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Files and directories copied verbatim into the output.
COPY_DIRS = ['assets', 'images', 'js', 'data']
COPY_FILES = ['.nojekyll', 'CNAME', 'robots.txt', 'sitemap.xml']

# Working files that no page links to — kept out of the deployable output.
EXCLUDE = {'style_server.css'}

NAV = [
    ('/', 'Home'),
    ('education.html', 'Education'),
    ('publications.html', 'Publications'),
    ('projects.html', 'Projects'),
    ('experience.html', 'Experience'),
    ('skills.html', 'Skills'),
    ('certifications.html', 'Certifications'),
]

# Without JS the hamburger button does nothing, so show the links stacked.
NOSCRIPT = """  <noscript>
    <style>
      .nav-toggle { display: none !important; }
      @media (max-width: 720px) {
        .nav-inner { flex-wrap: wrap; height: auto; padding-top: 8px; padding-bottom: 8px; }
        .nav-links { display: flex !important; position: static; flex-direction: row;
                     flex-wrap: wrap; border-bottom: none; box-shadow: none; padding: 4px 0; }
        .nav-links li a { padding: 4px 10px; }
        .topnav { height: auto; }
      }
    </style>
  </noscript>
"""


# ── helpers mirroring js/render.js ───────────────────────────────────────────

def esc(value):
    """Same character set as esc() in js/render.js."""
    return (str(value).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def tags(items):
    return ''.join(f'<span class="tag">{esc(t)}</span>' for t in items)


# ── section renderers ────────────────────────────────────────────────────────

def render_nav(active):
    return ''.join(
        f'\n    <li><a href="{href}" {"class=\"active\"" if label == active else ""}>{label}</a></li>\n  '
        for href, label in NAV)


def render_footer(profile, year):
    contact = profile['contact'][0]
    return (f'{esc(profile["name"])} &copy; {year} &nbsp;&middot;&nbsp;\n'
            f'     {esc(profile["institution"])} &nbsp;&middot;&nbsp;\n'
            f'     <a href="{esc(contact["url"])}">{esc(contact["label"])}</a>')


def render_hero_links(contacts):
    out = []
    for c in contacts:
        if c.get('unavailable'):
            out.append(f'<span class="hero-link-unavailable">'
                       f'<i class="{esc(c["icon"])}"></i> {esc(c["label"])}</span>')
        else:
            blank = 'target="_blank" rel="noopener"' if c['url'].startswith('http') else ''
            out.append(f'<a href="{esc(c["url"])}" {blank}>\n'
                       f'      <i class="{esc(c["icon"])}"></i> {esc(c["label"])}\n    </a>')
    return ''.join(out)


def render_news(news):
    items = ''.join(f'''
    <li class="news-item">
      <span class="news-date">{esc(n["date"])}</span>
      <span class="news-body">{n["html"]}</span>
    </li>
  ''' for n in news)
    return f'<ul class="news-list">{items}</ul>'


def render_timeline(items):
    return ''.join(f'''
    <div class="timeline-item">
      <div class="timeline-meta">
        <h3>{esc(item["institution"])}</h3>
        <span class="tl-degree">{esc(item.get("degree") or item.get("role"))}</span>
        <span class="tl-period"><i class="far fa-calendar-alt"></i> {esc(item["period"])}</span>
        {f'<span class="tl-grade">{esc(item["grade"])}</span>' if item.get("grade") else ''}
      </div>
      <div class="timeline-body">{esc(item["description"])}</div>
    </div>
  ''' for item in items)


def pub_link_meta(label):
    """Same label → icon mapping as pubLinkMeta() in js/render.js."""
    l = str(label).lower()
    if re.search(r'\bdoi\b', l):
        return 'fas fa-link', False
    if re.search(r'paper|pdf|arxiv|publication', l):
        return 'fas fa-file-lines', True
    if re.search(r'code|github|repo|source', l):
        return 'fab fa-github', False
    return 'fas fa-arrow-up-right-from-square', False


def pub_thumb(pub):
    """Same figure markup as pubThumb() in js/render.js."""
    if not pub.get('image'):
        return ''
    paper = next((l for l in pub.get('links') or []
                  if re.search(r'paper|pdf|arxiv|doi', l['label'], re.I)), None)
    img = (f'<img src="{esc(pub["image"])}"\n'
           f'             alt="{esc(pub.get("imageAlt") or pub["title"])}" loading="lazy" />')
    if paper:
        return (f'<a class="pub-thumb" href="{esc(paper["url"])}" target="_blank" rel="noopener"\n'
                f'             aria-label="{esc(pub["title"])}">{img}</a>')
    return f'<div class="pub-thumb">{img}</div>'


def render_authors(authors, self_name):
    """Same byline as renderAuthors() in js/render.js."""
    if not authors:
        return ''
    key = lambda s: re.sub(r'[^a-z]', '', str(s).lower())
    me = key(self_name or '')
    names = [f'<span class="pub-author-self">{esc(a)}</span>' if me and key(a) == me
             else esc(a) for a in authors]
    return f'<p class="pub-authors">{", ".join(names)}</p>'


def render_pub_links(links):
    if not links:
        return ''
    out = []
    for l in links:
        icon, primary = pub_link_meta(l['label'])
        cls = 'pub-link-primary' if primary else 'pub-link-secondary'
        out.append(f'<a href="{esc(l["url"])}" target="_blank" rel="noopener"\n'
                   f'                         class="pub-link {cls}">\n'
                   f'                        <i class="{icon}"></i>{esc(l["label"])}\n'
                   f'                      </a>')
    return f'''
          <div class="pub-links">
            {"".join(out)}
          </div>'''


def render_publications(publications, profile):
    self_name = profile.get('name') if profile else None
    out = []
    for i, pub in enumerate(publications, start=1):
        year = f'<span class="pub-year">({esc(pub["year"])})</span>' if pub.get('year') else ''
        thumb = pub_thumb(pub)
        out.append(f'''
    <div class="pub-card">
      <div class="pub-index">{i:02d}</div>
      {thumb}
      <div class="pub-content">
        <h3 class="pub-title">{esc(pub["title"])}</h3>
        {render_authors(pub.get("authors"), self_name)}
        <p class="pub-venue">
          <i class="fas fa-university"></i>
          <span>{esc(pub["venueFullName"])} &mdash; <em>{esc(pub["venue"])}</em>
          {year}</span>
        </p>
        {render_pub_links(pub.get("links"))}
      </div>
    </div>
  ''')
    return ''.join(out)


def render_projects(projects):
    out = []
    for proj in projects:
        out.append(f'''
    <div class="project-card">
      <div class="project-header">
        <h3>{esc(proj["title"])}</h3>
        <span class="project-date">{esc(proj["date"])}</span>
      </div>
      <p>{esc(proj["description"])}</p>
      <div class="tag-row">{tags(proj["tags"])}</div>
      {render_pub_links(proj.get("links"))}
    </div>
  ''')
    return ''.join(out)


def render_skills(skills):
    return ''.join(f'''
    <div class="skill-row">
      <span class="skill-cat">{esc(row["category"])}</span>
      <div class="tag-row">{tags(row["tags"])}</div>
    </div>
  ''' for row in skills)


def render_certifications(certs):
    return ''.join(f'''
    <li class="cert-item">
      <div class="cert-icon"><i class="{esc(c["icon"])}"></i></div>
      <div class="cert-content">
        <strong>{esc(c["title"])}</strong>
        <span class="cert-meta">{esc(c["meta"])}</span>
      </div>
    </li>
  ''' for c in certs)


# ── DOM-ish surgery on the source HTML ───────────────────────────────────────

def fill(page, element_id, inner):
    """Insert `inner` into the empty element carrying id="element_id"."""
    pattern = re.compile(
        r'(<(?P<tag>\w+)(?=[\s>])[^>]*\bid="' + re.escape(element_id) + r'"[^>]*>)'
        r'\s*(</(?P=tag)>)')
    new, n = pattern.subn(lambda m: m.group(1) + inner + m.group(3), page, count=1)
    if n != 1:
        raise SystemExit(f'  ! could not fill #{element_id} (matched {n} times)')
    return new


def set_photo(page, src, alt):
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'src="[^"]*"', f'src="{esc(src)}"', tag)
        tag = re.sub(r'alt="[^"]*"', f'alt="{esc(alt)}"', tag)
        return tag
    return re.sub(r'<img\b[^>]*\bid="profile-photo"[^>]*>', repl, page, count=1)


def add_noscript(page):
    return page.replace('</head>', NOSCRIPT + '</head>', 1)


# ── build ────────────────────────────────────────────────────────────────────

def build(out_dir, year):
    data = {name: jsdata.load(ROOT / 'data' / f'{name}.js', name) for name in
            ['profile', 'news', 'education', 'experience',
             'publications', 'projects', 'skills', 'certifications']}
    profile = data['profile']

    in_place = out_dir.resolve() == ROOT
    if not in_place:
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True)

        ignore = shutil.ignore_patterns(*EXCLUDE)
        for d in COPY_DIRS:
            src = ROOT / d
            if src.is_dir():
                shutil.copytree(src, out_dir / d, ignore=ignore)
        for f in COPY_FILES:
            if (ROOT / f).is_file():
                shutil.copy2(ROOT / f, out_dir / f)

    footer = render_footer(profile, year)

    pages = {
        'index.html': ('Home', lambda p: (
            fill(fill(fill(fill(fill(fill(
                set_photo(p, profile['photo'], profile['name']),
                'hero-name', esc(profile['name'])),
                'hero-role', f'{esc(profile["role"])} &nbsp;&middot;&nbsp; {esc(profile["institution"])}'),
                'hero-dept', esc(profile['department'])),
                'hero-links', render_hero_links(profile['contact'])),
                'hero-about', ''.join(f'<p>{para}</p>' for para in profile['about'])),
                'news-content', render_news(data['news'])),
        )),
        'education.html': ('Education', lambda p: (
            fill(p, 'education-list', render_timeline(data['education'])),)),
        'publications.html': ('Publications', lambda p: (
            fill(p, 'publications-list', render_publications(data['publications'], profile)),)),
        'projects.html': ('Projects', lambda p: (
            fill(p, 'projects-list', render_projects(data['projects'])),)),
        'experience.html': ('Experience', lambda p: (
            fill(p, 'experience-list', render_timeline(data['experience'])),)),
        'skills.html': ('Skills', lambda p: (
            fill(p, 'skills-list', render_skills(data['skills'])),)),
        'certifications.html': ('Certifications', lambda p: (
            fill(p, 'certifications-list', render_certifications(data['certifications'])),)),
    }

    templates = ROOT / 'templates'
    for filename, (active, transform) in pages.items():
        src = templates / filename if (templates / filename).is_file() else ROOT / filename
        if not src.is_file():
            print(f'  ~ skipped {filename} (not found)')
            continue
        page = src.read_text(encoding='utf-8')
        page = fill(page, 'nav-brand', esc(profile['name']))
        page = fill(page, 'nav-links', render_nav(active))
        page = fill(page, 'footer-text', footer)
        page = transform(page)[0]
        if filename == 'index.html':
            page = fill(page, 'interests-content',
                        f'<div class="tag-row">{tags(profile["researchInterests"])}</div>')
        page = add_noscript(page)
        (out_dir / filename).write_text(page, encoding='utf-8')
        print(f'  + {filename:22} {len(page):>7,} bytes')

    return out_dir


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default='dist', help='output directory (default: dist)')
    ap.add_argument('--year', type=int, default=None, help='footer copyright year')
    args = ap.parse_args()

    import datetime
    year = args.year or datetime.date.today().year

    out = ROOT / args.out
    print(f'Prerendering into {out.relative_to(ROOT)}/ …')
    build(out, year)
    print('Done.')


if __name__ == '__main__':
    main()
