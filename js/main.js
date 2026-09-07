import { profile } from '../data/profile.js';
import { news } from '../data/news.js';
import { renderNav, renderFooter, setPageTitle, mount, esc, tags, renderNewsHTML } from './render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, null);
  renderNav(profile, 'Home');

  const photo = document.getElementById('profile-photo');
  if (photo) { photo.src = profile.photo; photo.alt = profile.name; }

  mount('hero-name', esc(profile.name));
  mount('hero-role', `${esc(profile.role)} &nbsp;&middot;&nbsp; ${esc(profile.institution)}`);
  mount('hero-dept', esc(profile.department));
  mount('hero-about', profile.about.map(p => `<p>${p}</p>`).join(''));

  mount('hero-links', profile.contact.map(c => {
    if (c.unavailable) {
      return `<span class="hero-link-unavailable"><i class="${esc(c.icon)}"></i> ${esc(c.label)}</span>`;
    }
    return `<a href="${esc(c.url)}" ${c.url.startsWith('http') ? 'target="_blank" rel="noopener"' : ''}>
      <i class="${esc(c.icon)}"></i> ${esc(c.label)}
    </a>`;
  }).join(''));

  mount('news-content', renderNewsHTML(news));

  mount('interests-content', `<div class="tag-row">${tags(profile.researchInterests)}</div>`);

  renderFooter(profile);
});
