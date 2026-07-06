/**
 * Contact form AJAX submission with UTM passthrough and consent checkbox.
 */
(function () {
  function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    const cookie = document.cookie
      .split(';')
      .map((c) => c.trim())
      .find((c) => c.startsWith('csrftoken='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  }

  function getUtmFields() {
    const params = new URLSearchParams(window.location.search);
    return {
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_term: params.get('utm_term') || '',
      utm_content: params.get('utm_content') || '',
    };
  }

  function showMessage(form, text, isError) {
    let box = form.querySelector('.form-message');
    if (!box) {
      box = document.createElement('div');
      box.className = 'form-message mt-4 p-4 rounded-xl text-sm font-medium';
      form.appendChild(box);
    }
    box.textContent = text;
    box.className = `form-message mt-4 p-4 rounded-xl text-sm font-medium ${
      isError
        ? 'bg-red-50 text-red-700 border border-red-200 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800'
        : 'bg-green-50 text-green-700 border border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800'
    }`;
  }

  function updateSubmitState(form) {
    const consent = form.querySelector('#consent-accepted');
    const submitBtn = form.querySelector('#contact-submit');
    if (!submitBtn) return;
    submitBtn.disabled = !(consent && consent.checked);
  }

  function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const consent = form.querySelector('#consent-accepted');
    if (consent) {
      consent.addEventListener('change', () => updateSubmitState(form));
      updateSubmitState(form);
    }

    form.addEventListener('focusin', () => {
      if (!form.dataset.started) {
        form.dataset.started = '1';
        if (typeof window.trackAnalyticsEvent === 'function') {
          window.trackAnalyticsEvent('form_start', { form: 'contact' });
        }
      }
    }, { once: true });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (!consent || !consent.checked) {
        showMessage(form, 'Необходимо дать согласие на обработку персональных данных.', true);
        return;
      }

      const submitBtn = form.querySelector('#contact-submit');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';
      }

      const formData = new FormData(form);
      const utm = getUtmFields();
      Object.entries(utm).forEach(([k, v]) => formData.append(k, v));

      try {
        const response = await fetch('/api/leads/contact/', {
          method: 'POST',
          headers: { 'X-CSRFToken': getCsrfToken() },
          body: formData,
          credentials: 'same-origin',
        });
        const data = await response.json();

        if (data.success) {
          showMessage(form, data.message, false);
          form.reset();
          delete form.dataset.started;
          updateSubmitState(form);
        } else {
          const firstError = data.errors
            ? Object.values(data.errors)[0]
            : 'Ошибка отправки. Попробуйте позже.';
          showMessage(form, firstError, true);
          updateSubmitState(form);
        }
      } catch {
        showMessage(form, 'Ошибка сети. Проверьте подключение и попробуйте снова.', true);
        updateSubmitState(form);
      } finally {
        if (submitBtn) {
          submitBtn.textContent = 'Отправить заявку';
        }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', initContactForm);
})();
