/**
 * Mobile navigation drawer.
 */
(function () {
  function initMobileNav() {
    const toggle = document.getElementById('mobile-nav-toggle');
    const menu = document.getElementById('mobile-nav-menu');
    const overlay = document.getElementById('mobile-nav-overlay');
    const closeBtn = document.getElementById('mobile-nav-close');

    if (!toggle || !menu) return;

    function openMenu() {
      menu.classList.remove('translate-x-full');
      menu.classList.add('translate-x-0');
      overlay?.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
      toggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
      menu.classList.add('translate-x-full');
      menu.classList.remove('translate-x-0');
      overlay?.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', openMenu);
    closeBtn?.addEventListener('click', closeMenu);
    overlay?.addEventListener('click', closeMenu);

    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMenu);
    });
  }

  document.addEventListener('DOMContentLoaded', initMobileNav);
})();
