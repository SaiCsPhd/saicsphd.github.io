import { profile  } from '../../data/profile.js';
import { projects } from '../../data/projects.js';
import { renderNav, renderFooter, setPageTitle, mount, renderProjectsHTML } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Projects');
  renderNav(profile, 'Projects');
  mount('projects-list', renderProjectsHTML(projects));
  renderFooter(profile);
});
