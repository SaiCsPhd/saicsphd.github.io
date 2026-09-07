import { profile        } from '../../data/profile.js';
import { certifications } from '../../data/certifications.js';
import { renderNav, renderFooter, setPageTitle, mount, renderCertificationsHTML } from '../render.js';

document.addEventListener('DOMContentLoaded', () => {
  setPageTitle(profile, 'Certifications');
  renderNav(profile, 'Certifications');
  mount('certifications-list', renderCertificationsHTML(certifications));
  renderFooter(profile);
});
