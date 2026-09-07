// Shared render helpers and section renderers used across all pages.

export function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function tags(arr) {
  return arr.map(t => `<span class="tag">${esc(t)}</span>`).join('');
}

export function mount(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

// ── Nav ──────────────────────────────────────────────────────────────────────

export function renderNav(profile, activePage) {
  mount('nav-brand', esc(profile.name));

  const links = [
    { href: '/',                   label: 'Home' },
    { href: 'education.html',      label: 'Education' },
    { href: 'publications.html',   label: 'Publications' },
    { href: 'projects.html',       label: 'Projects' },
    { href: 'experience.html',     label: 'Experience' },
    { href: 'skills.html',         label: 'Skills' },
    { href: 'certifications.html', label: 'Certifications' },
  ];

  const html = links.map(l => `
    <li><a href="${l.href}" ${l.label === activePage ? 'class="active"' : ''}>${l.label}</a></li>
  `).join('');
  mount('nav-links', html);

  // Mobile toggle
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.getElementById('nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      toggle.querySelector('i').className = open ? 'fas fa-times' : 'fas fa-bars';
    });
  }
}

// ── Footer ───────────────────────────────────────────────────────────────────

export function renderFooter(profile) {
  mount('footer-text',
    `${esc(profile.name)} &copy; ${new Date().getFullYear()} &nbsp;&middot;&nbsp;
     ${esc(profile.institution)} &nbsp;&middot;&nbsp;
     <a href="${esc(profile.contact[0].url)}">${esc(profile.contact[0].label)}</a>`
  );
}

// ── Page title helper ─────────────────────────────────────────────────────────

export function setPageTitle(profile, section) {
  document.title = section
    ? `${section} · ${profile.name}`
    : `${profile.name} — ${profile.role}, ${profile.institution}`;
}

// ── Section renderers ─────────────────────────────────────────────────────────

export function renderTimeline(items) {
  return items.map(item => `
    <div class="timeline-item">
      <div class="timeline-meta">
        <h3>${esc(item.institution)}</h3>
        <span class="tl-degree">${esc(item.degree ?? item.role)}</span>
        <span class="tl-period"><i class="far fa-calendar-alt"></i> ${esc(item.period)}</span>
        ${item.grade ? `<span class="tl-grade">${esc(item.grade)}</span>` : ''}
      </div>
      <div class="timeline-body">${esc(item.description)}</div>
    </div>
  `).join('');
}

export function renderNewsHTML(news) {
  return `<ul class="news-list">${news.map(item => `
    <li class="news-item">
      <span class="news-date">${esc(item.date)}</span>
      <span class="news-body">${item.html}</span>
    </li>
  `).join('')}</ul>`;
}

// Maps a link label to an icon + button style. "Paper" is the primary action.
// DOI is checked first: it would otherwise fall into the paper branch below.
function pubLinkMeta(label) {
  const l = String(label).toLowerCase();
  if (/\bdoi\b/.test(l))                          return { icon: 'fas fa-link',        primary: false };
  if (/paper|pdf|arxiv|publication/.test(l))      return { icon: 'fas fa-file-lines',  primary: true  };
  if (/code|github|repo|source/.test(l))          return { icon: 'fab fa-github',      primary: false };
  return { icon: 'fas fa-arrow-up-right-from-square', primary: false };
}

// Author byline. The site owner's own name is emphasised wherever it appears.
function renderAuthors(authors, selfName) {
  if (!authors || !authors.length) return '';
  const key = s => String(s).toLowerCase().replace(/[^a-z]/g, '');
  const self = key(selfName || '');
  const names = authors.map(a =>
    self && key(a) === self ? `<span class="pub-author-self">${esc(a)}</span>` : esc(a));
  return `<p class="pub-authors">${names.join(', ')}</p>`;
}

export function renderPublicationsHTML(publications, profile) {
  const selfName = profile && profile.name;
  return publications.map((pub, i) => `
    <div class="pub-card">
      ${pub.image
        ? `<div class="pub-thumb"><img src="${esc(pub.image)}"
             alt="${esc(pub.imageAlt || pub.title)}" loading="lazy" /></div>`
        : `<div class="pub-index">${String(i + 1).padStart(2, '0')}</div>`}
      <div class="pub-content">
        <h3 class="pub-title">${esc(pub.title)}</h3>
        ${renderAuthors(pub.authors, selfName)}
        <p class="pub-venue">
          <i class="fas fa-university"></i>
          <span>${esc(pub.venueFullName)} &mdash; <em>${esc(pub.venue)}</em>
          ${pub.year ? `<span class="pub-year">(${esc(pub.year)})</span>` : ''}</span>
        </p>
        ${pub.links && pub.links.length ? `
          <div class="pub-links">
            ${pub.links.map(l => {
              const { icon, primary } = pubLinkMeta(l.label);
              return `<a href="${esc(l.url)}" target="_blank" rel="noopener"
                         class="pub-link ${primary ? 'pub-link-primary' : 'pub-link-secondary'}">
                        <i class="${icon}"></i>${esc(l.label)}
                      </a>`;
            }).join('')}
          </div>` : ''}
      </div>
    </div>
  `).join('');
}

export function renderProjectsHTML(projects) {
  return projects.map(proj => `
    <div class="project-card">
      <div class="project-header">
        <h3>${esc(proj.title)}</h3>
        <span class="project-date">${esc(proj.date)}</span>
      </div>
      <p>${esc(proj.description)}</p>
      <div class="tag-row">${tags(proj.tags)}</div>
      ${proj.links && proj.links.length ? `
        <div class="pub-links">
          ${proj.links.map(l => `<a href="${esc(l.url)}" target="_blank" rel="noopener" class="pub-link">${esc(l.label)}</a>`).join('')}
        </div>` : ''}
    </div>
  `).join('');
}

export function renderSkillsHTML(skills) {
  return skills.map(row => `
    <div class="skill-row">
      <span class="skill-cat">${esc(row.category)}</span>
      <div class="tag-row">${tags(row.tags)}</div>
    </div>
  `).join('');
}

export function renderCertificationsHTML(certifications) {
  return certifications.map(cert => `
    <li class="cert-item">
      <div class="cert-icon"><i class="${esc(cert.icon)}"></i></div>
      <div class="cert-content">
        <strong>${esc(cert.title)}</strong>
        <span class="cert-meta">${esc(cert.meta)}</span>
      </div>
    </li>
  `).join('');
}
