import { profile      } from '../../data/profile.js';
import { publications } from '../../data/publications.js';
import { renderNav, renderFooter, setPageTitle, mount, renderPublicationsHTML } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Publications');
  renderNav(profile, 'Publications');
  mount('publications-list', renderPublicationsHTML(publications));
  renderFooter(profile);
});
