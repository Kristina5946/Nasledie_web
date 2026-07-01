/**
 * Theme toggle: light (default) / dark.
 * Persists choice in localStorage and tracks analytics event.
 */
(function () {
  const STORAGE_KEY = 'nasledie-theme';
  const DEFAULT_THEME = 'light';

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'dark' || stored === 'light') return stored;
    return DEFAULT_THEME;
  }

  function applyTheme(theme) {
    const html = document.documentElement;
    if (theme === 'dark') {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
    localStorage.setItem(STORAGE_KEY, theme);
    updateToggleUI(theme);
  }

  function updateToggleUI(theme) {
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    const label = document.getElementById('theme-toggle-label');

    if (sunIcon && moonIcon) {
      sunIcon.classList.toggle('hidden', theme === 'dark');
      moonIcon.classList.toggle('hidden', theme !== 'dark');
    }
    if (label) {
      label.textContent = theme === 'dark' ? 'Светлая' : 'Тёмная';
    }
  }

  function trackThemeToggle(theme) {
    if (typeof window.trackAnalyticsEvent !== 'function') return;
    window.trackAnalyticsEvent('theme_toggle', { theme });
  }

  function initTheme() {
    applyTheme(getPreferredTheme());

    document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const next = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        applyTheme(next);
        trackThemeToggle(next);
      });
    });
  }

  // Prevent flash of wrong theme
  applyTheme(getPreferredTheme());
  document.addEventListener('DOMContentLoaded', initTheme);
})();
