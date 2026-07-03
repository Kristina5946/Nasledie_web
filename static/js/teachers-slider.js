/**
 * Teachers carousel with touch scroll and arrow controls.
 */
(function () {
  function initTeachersSlider() {
    const viewport = document.getElementById('teachers-viewport');
    const track = document.getElementById('teachers-track');
    const dotsContainer = document.getElementById('teachers-dots');
    if (!viewport || !track) return;

    const slides = Array.from(track.querySelectorAll('.teachers-slider__slide'));
    if (!slides.length) return;

    const prevButtons = [
      document.getElementById('teachers-prev'),
      document.getElementById('teachers-prev-mobile'),
    ].filter(Boolean);
    const nextButtons = [
      document.getElementById('teachers-next'),
      document.getElementById('teachers-next-mobile'),
    ].filter(Boolean);

    let activeIndex = 0;

    function getSlideStep() {
      const slide = slides[0];
      const style = window.getComputedStyle(track);
      const gap = parseFloat(style.columnGap || style.gap || '16');
      return slide.offsetWidth + gap;
    }

    function scrollToIndex(index) {
      activeIndex = Math.max(0, Math.min(index, slides.length - 1));
      viewport.scrollTo({ left: activeIndex * getSlideStep(), behavior: 'smooth' });
      updateDots();
    }

    function updateDots() {
      if (!dotsContainer) return;
      dotsContainer.querySelectorAll('.teachers-slider__dot').forEach((dot, i) => {
        dot.classList.toggle('is-active', i === activeIndex);
      });
    }

    function buildDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'teachers-slider__dot' + (i === 0 ? ' is-active' : '');
        dot.setAttribute('aria-label', 'Слайд ' + (i + 1));
        dot.addEventListener('click', () => scrollToIndex(i));
        dotsContainer.appendChild(dot);
      });
    }

    prevButtons.forEach((btn) => btn.addEventListener('click', () => scrollToIndex(activeIndex - 1)));
    nextButtons.forEach((btn) => btn.addEventListener('click', () => scrollToIndex(activeIndex + 1)));

    viewport.addEventListener('scroll', () => {
      const step = getSlideStep();
      if (!step) return;
      activeIndex = Math.round(viewport.scrollLeft / step);
      updateDots();
    }, { passive: true });

    buildDots();
    window.addEventListener('resize', updateDots);
  }

  document.addEventListener('DOMContentLoaded', initTeachersSlider);
})();
