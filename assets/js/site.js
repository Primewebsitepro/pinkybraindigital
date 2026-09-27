document.addEventListener('DOMContentLoaded', function () {
  var burger = document.querySelector('.pb-burger');
  var closeBtn = document.querySelector('.pb-mobile-nav__close');
  var mobileNav = document.querySelector('.pb-mobile-nav');
  if (burger && mobileNav) {
    burger.addEventListener('click', function () {
      document.body.classList.add('pb-nav-open');
    });
  }
  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      document.body.classList.remove('pb-nav-open');
    });
  }
  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('pb-nav-open');
      });
    });
  }
});
