import { profile    } from '../../data/profile.js';
import { experience } from '../../data/experience.js';
import { renderNav, renderFooter, setPageTitle, mount, renderTimeline } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Experience');
  renderNav(profile, 'Experience');
  mount('experience-list', renderTimeline(experience));
  renderFooter(profile);
});
