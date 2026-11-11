(() => {
  const header = document.querySelector('[data-header]');
  const menuToggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.primary-nav');

  const syncHeader = () => {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 24);
  };

  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  menuToggle?.addEventListener('click', () => {
    const isOpen = navigation?.classList.toggle('is-open') ?? false;
    menuToggle.setAttribute('aria-expanded', String(isOpen));
    menuToggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
  });

  navigation?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navigation.classList.remove('is-open');
      menuToggle?.setAttribute('aria-expanded', 'false');
    });
  });
})();
