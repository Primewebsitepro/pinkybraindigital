(function () {
  var body = document.body;
  var burger = document.querySelector('.pb-burger');
  var panel = document.querySelector('.pb-mobile-nav');
  var closeBtn = document.querySelector('.pb-mobile-nav__close');

  function setMobile(open) {
    body.classList.toggle('pb-nav-open', open);
    if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open && closeBtn) closeBtn.focus();
    if (!open && burger && document.activeElement && panel && panel.contains(document.activeElement)) burger.focus();
  }

  if (burger && panel) {
    burger.addEventListener('click', function () { setMobile(true); });
    if (closeBtn) closeBtn.addEventListener('click', function () { setMobile(false); });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMobile(false);
    });
  }

  var mega = document.querySelector('.pb-has-mega');
  var toggle = mega && mega.querySelector('.pb-nav__toggle');

  function setMega(open) {
    if (!mega) return;
    mega.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  if (toggle) {
    toggle.addEventListener('click', function () { setMega(!mega.classList.contains('is-open')); });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target)) setMega(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (body.classList.contains('pb-nav-open')) setMobile(false);
    if (mega && mega.classList.contains('is-open')) { setMega(false); toggle.focus(); }
  });

  // leaving the mobile layout (rotate / resize) should never leave the overlay stuck open
  window.addEventListener('resize', function () {
    if (window.innerWidth > 1024 && body.classList.contains('pb-nav-open')) setMobile(false);
  });
})();
