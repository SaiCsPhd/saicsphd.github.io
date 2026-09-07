import { profile } from '../../data/profile.js';
import { skills  } from '../../data/skills.js';
import { renderNav, renderFooter, setPageTitle, mount, renderSkillsHTML } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Skills');
  renderNav(profile, 'Skills');
  mount('skills-list', renderSkillsHTML(skills));
  renderFooter(profile);
});
