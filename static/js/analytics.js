/**
 * Client-side analytics event tracking.
 */
(function () {
  function getCsrfToken() {
    const cookie = document.cookie
      .split(';')
      .map((c) => c.trim())
      .find((c) => c.startsWith('csrftoken='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  }

  window.trackAnalyticsEvent = function (eventType, metadata) {
    fetch('/api/analytics/track/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({
        event_type: eventType,
        path: window.location.pathname,
        metadata: metadata || {},
      }),
      credentials: 'same-origin',
    }).catch(() => {});
  };

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-track-cta]').forEach((el) => {
      el.addEventListener('click', () => {
        window.trackAnalyticsEvent('cta_click', {
          label: el.dataset.trackCta || el.textContent?.trim(),
        });
      });
    });
  });
})();
