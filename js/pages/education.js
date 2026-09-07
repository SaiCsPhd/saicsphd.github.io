import { profile   } from '../../data/profile.js';
import { education } from '../../data/education.js';
import { renderNav, renderFooter, setPageTitle, mount, renderTimeline } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Education');
  renderNav(profile, 'Education');
  mount('education-list', renderTimeline(education));
  renderFooter(profile);
});
