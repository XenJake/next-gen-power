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

  const gallery = document.querySelector('[data-gallery]');
  const galleryDialog = document.querySelector('[data-gallery-dialog]');
  const galleryButtons = [...(gallery?.querySelectorAll('[data-gallery-open]') ?? [])];
  const galleryImage = galleryDialog?.querySelector('[data-gallery-viewer-image]');
  const galleryCaption = galleryDialog?.querySelector('[data-gallery-viewer-caption]');

  if (galleryDialog && galleryImage && galleryCaption && galleryButtons.length) {
    let activePhoto = 0;

    const showPhoto = (index) => {
      activePhoto = (index + galleryButtons.length) % galleryButtons.length;
      const button = galleryButtons[activePhoto];
      galleryImage.src = button.dataset.fullSrc;
      galleryImage.alt = button.dataset.alt ?? '';
      galleryCaption.textContent = [
        button.dataset.credit ? `Photo by ${button.dataset.credit}` : '',
        button.dataset.license ?? '',
      ].filter(Boolean).join(' · ');
    };

    galleryButtons.forEach((button, index) => {
      button.addEventListener('click', () => {
        showPhoto(index);
        galleryDialog.showModal();
      });
    });

    galleryDialog.querySelector('[data-gallery-close]')?.addEventListener('click', () => galleryDialog.close());
    galleryDialog.querySelector('[data-gallery-previous]')?.addEventListener('click', () => showPhoto(activePhoto - 1));
    galleryDialog.querySelector('[data-gallery-next]')?.addEventListener('click', () => showPhoto(activePhoto + 1));
    galleryDialog.addEventListener('click', (event) => {
      if (event.target === galleryDialog) galleryDialog.close();
    });
    galleryDialog.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') showPhoto(activePhoto - 1);
      if (event.key === 'ArrowRight') showPhoto(activePhoto + 1);
    });
  }
})();
