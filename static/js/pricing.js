/**
 * Pricing tier filter and card rendering.
 * Filter buttons are built from admin data (pricing_tiers_json).
 */
(function () {
  function initPricing() {
    const dataEl = document.getElementById('pricing-data');
    const cardsEl = document.getElementById('pricing-cards');
    const noteEl = document.getElementById('pricing-note');
    const labelEl = document.getElementById('pricing-tier-label');
    const filterEl = document.getElementById('pricing-filter');
    if (!dataEl || !cardsEl || !filterEl) return;

    let tiers;
    try {
      tiers = JSON.parse(dataEl.textContent);
    } catch {
      return;
    }

    const tierKeys = Object.keys(tiers);
    if (!tierKeys.length) return;

    function renderCards(tierKey) {
      const tier = tiers[tierKey];
      if (!tier) return;

      if (labelEl) labelEl.textContent = tier.label;
      if (noteEl) noteEl.textContent = tier.note;

      cardsEl.innerHTML = tier.plans.map((plan) => {
        const hasDiscount = Boolean(plan.original);
        return `
          <article class="pricing-card">
            <div class="pricing-card__icon">${plan.icon}</div>
            <h3 class="pricing-card__title">${plan.title}</h3>
            ${hasDiscount ? `<p class="pricing-card__original">${plan.original} ₽</p><p class="pricing-card__label">Со скидкой</p>` : ''}
            <p class="pricing-card__price">${plan.price}</p>
            <p class="pricing-card__currency">рублей</p>
            ${hasDiscount ? '<span class="pricing-card__badge">Выгодно</span>' : ''}
          </article>
        `;
      }).join('');
    }

    filterEl.innerHTML = tierKeys.map((tierKey, index) => (
      `<button type="button" data-tier="${tierKey}" class="pricing-filter__btn${index === 0 ? ' is-active' : ''}">${tiers[tierKey].label}</button>`
    )).join('');

    filterEl.querySelectorAll('.pricing-filter__btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const tierKey = btn.dataset.tier;
        filterEl.querySelectorAll('.pricing-filter__btn').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        renderCards(tierKey);
        if (typeof window.trackAnalyticsEvent === 'function') {
          window.trackAnalyticsEvent('cta_click', { label: 'Цены: ' + tierKey });
        }
      });
    });

    renderCards(tierKeys[0]);
  }

  document.addEventListener('DOMContentLoaded', initPricing);
})();
