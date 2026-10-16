/* ═══════════════════════════════════════════════
   sotrudniki.js — Страница «Сотрудники»
   IT COLLEGE — 2025
   ═══════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ══════════════════════════════════════════════
     STAFF DATA
  ══════════════════════════════════════════════ */
  document.addEventListener('DOMContentLoaded', function () {

  /* данные сотрудников приходят из админки через {{ staff_data|json_script }} */
  var dataEl = document.getElementById('staff-data');
  var STAFF  = dataEl ? JSON.parse(dataEl.textContent) : {};
  var modalEl = document.getElementById('staffModal');
  var DEFAULT_PHOTO = modalEl ? modalEl.dataset.defaultPhoto : '';

  /* ══════════════════════════════════════════════
     MODAL LOGIC
  ══════════════════════════════════════════════ */
  var overlay      = document.getElementById('staffModal');
  var panel        = document.getElementById('smodal-panel');
  var closeBtn     = document.getElementById('smodal-close');
  var lightbox     = document.getElementById('staffLightbox');
  var lightboxImg  = document.getElementById('staffLightboxImg');

  function openModal(id) {
    var d = STAFF[id];
    if (!d) return;

    /* photo */
    var photo = document.getElementById('smodal-main-photo');
    photo.src = d.photo || DEFAULT_PHOTO;
    photo.alt = d.name;

    /* name & position */
    document.getElementById('smodal-name').textContent     = d.name;
    document.getElementById('smodal-pos-badge').textContent = d.position;

    /* pills */
    var pillsEl = document.getElementById('smodal-pills');
    pillsEl.innerHTML =
      (d.exp ? pill('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>', 'Стаж: ' + d.exp) : '') +
      (d.edu ? pill('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>', d.edu) : '') +
      pill('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>', d.dept);

    /* bio */
    document.getElementById('smodal-bio').textContent = d.bio;

    /* courses */
    var coursesEl  = document.getElementById('smodal-courses');
    var coursesSec = document.getElementById('smodal-courses-section');
    if (d.courses && d.courses.length) {
      coursesEl.innerHTML = d.courses.map(function (c) {
        return '<span class="smodal-course-tag">' + esc(c) + '</span>';
      }).join('');
      coursesSec.style.display = '';
    } else {
      coursesSec.style.display = 'none';
    }

    /* achievements */
    var achEl = document.getElementById('smodal-achievements');
    achEl.innerHTML = (d.achievements || []).map(function (a) {
      return '<li>' + esc(a) + '</li>';
    }).join('');
    toggleSection('smodal-achievements-section', d.achievements);

    /* gallery */
    var galEl = document.getElementById('smodal-gallery');
    galEl.innerHTML = (d.gallery || []).map(function (src) {
      return '<img src="' + esc(src) + '" alt="Фото" class="smodal-gallery-img" loading="lazy">';
    }).join('');
    galEl.querySelectorAll('.smodal-gallery-img').forEach(function (img) {
      img.addEventListener('click', function () { openLightbox(img.src); });
    });
    toggleSection('smodal-gallery-section', d.gallery);

    /* contacts */
    var conEl = document.getElementById('smodal-contacts');
    conEl.innerHTML = '';
    if (d.email) {
      conEl.innerHTML +=
        '<a href="mailto:' + esc(d.email) + '" class="smodal-contact-link">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>' +
        esc(d.email) + '</a>';
    }
    if (d.phone) {
      var tel = d.phone.replace(/[^\d+]/g, '');
      conEl.innerHTML +=
        '<a href="tel:' + tel + '" class="smodal-contact-link">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.55 3.4 2 2 0 0 1 3.52 1.21h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.2a16 16 0 0 0 6 6l.87-.87a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.46 15.73z"/></svg>' +
        esc(d.phone) + '</a>';
    }

    /* open */
    panel.scrollTop = 0;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function openLightbox(src) {
    lightboxImg.src = src;
    lightbox.classList.add('open');
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    lightboxImg.src = '';
  }

  /* helpers */
  function toggleSection(id, items) {
    var el = document.getElementById(id);
    if (el) el.style.display = items && items.length ? '' : 'none';
  }
  function pill(iconSvg, text) {
    return '<span class="smodal-pill">' + iconSvg + esc(text) + '</span>';
  }
  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* event listeners */
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (overlay) overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  if (lightbox) lightbox.addEventListener('click', closeLightbox);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (lightbox && lightbox.classList.contains('open')) closeLightbox();
      else closeModal();
    }
  });

  /* bind cards */
  document.querySelectorAll('[data-staff-id]').forEach(function (card) {
    card.addEventListener('click', function (e) {
      /* don't open modal if user clicked a link inside the card */
      if (e.target.closest('a')) return;
      openModal(card.dataset.staffId);
    });
  });

  /* ══════════════════════════════════════════════
     PAGE UTILS
  ══════════════════════════════════════════════ */

  /* Progress bar + BTT + navbar scroll */
  var pb  = document.getElementById('progress-bar');
  var btt = document.getElementById('btt');
  var nb  = document.querySelector('.navbar');

  window.addEventListener('scroll', function () {
    var s = window.scrollY;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (pb)  pb.style.width = (h ? (s / h * 100) : 0) + '%';
    if (btt) btt.classList.toggle('visible', s > 400);
    if (nb)  nb.classList.toggle('scrolled', s > 60);
  }, { passive: true });

  if (btt) btt.onclick = function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  /* Scroll reveal */
  function revealEl(el) { el.classList.add('revealed'); }

  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        revealEl(e.target);
        revealObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });

  document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right').forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight + 80) {
      revealEl(el);
    } else {
      revealObserver.observe(el);
    }
  });

  /* Animated counters */
  function animateCounter(el) {
    var target   = parseInt(el.dataset.count, 10);
    var duration = 1400;
    var start    = null;
    function step(ts) {
      if (!start) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(ease * target);
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target;
    }
    requestAnimationFrame(step);
  }

  var counterObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        animateCounter(e.target);
        counterObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.4 });

  document.querySelectorAll('[data-count]').forEach(function (el) {
    counterObserver.observe(el);
  });

  /* Staff filter + search */
  var filterBtns   = document.querySelectorAll('.staff-filter-btn');
  var staffCards   = document.querySelectorAll('.staff-card[data-dept]');
  var searchInput  = document.getElementById('staffSearch');
  var noResults    = document.getElementById('staffNoResults');
  var activeFilter = 'all';

  function applyFilters() {
    var query   = searchInput ? searchInput.value.trim().toLowerCase() : '';
    var visible = 0;

    staffCards.forEach(function (card) {
      var dept    = card.dataset.dept || '';
      var name    = (card.querySelector('.staff-name')     || {}).textContent || '';
      var pos     = (card.querySelector('.staff-position') || {}).textContent || '';
      var deptTxt = (card.querySelector('.staff-dept')     || {}).textContent || '';

      var matchFilter = (activeFilter === 'all' || dept === activeFilter);
      var matchSearch = !query ||
        name.toLowerCase().includes(query) ||
        pos.toLowerCase().includes(query) ||
        deptTxt.toLowerCase().includes(query);

      var show = matchFilter && matchSearch;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      activeFilter = btn.dataset.filter;
      applyFilters();
    });
  });

  if (searchInput) searchInput.addEventListener('input', applyFilters);

  /* ══════════════════════════════════════════════
     LEADERSHIP CAROUSEL
  ══════════════════════════════════════════════ */
  (function () {
    var track   = document.getElementById('lcTrack');
    var btnPrev = document.getElementById('lcPrev');
    var btnNext = document.getElementById('lcNext');
    var dotsEl  = document.getElementById('lcDots');
    if (!track) return;

    var cards = track.querySelectorAll('.leadership-card');
    var total = cards.length;

    /* ── How many cards fit per view ── */
    function perView() {
      var w = track.parentElement.offsetWidth;
      if (w < 640)  return 1;
      if (w < 1024) return 2;
      return 3;
    }

    /* ── Total scrollable pages ── */
    function pageCount() { return Math.ceil(total / perView()); }

    /* ── Current page (0-based) based on scrollLeft ── */
    function currentPage() {
      if (!track.scrollWidth || !track.clientWidth) return 0;
      var card     = cards[0];
      var cardW    = card.offsetWidth + 24; /* 24 = gap */
      var pv       = perView();
      var pageW    = cardW * pv;
      return Math.round(track.scrollLeft / pageW);
    }

    /* ── Scroll to page ── */
    function scrollTo(page) {
      var card  = cards[0];
      var cardW = card.offsetWidth + 24;
      var pv    = perView();
      track.scrollTo({ left: page * cardW * pv, behavior: 'smooth' });
    }

    /* ── Build dots ── */
    function buildDots() {
      dotsEl.innerHTML = '';
      var pc = pageCount();
      for (var i = 0; i < pc; i++) {
        var btn = document.createElement('button');
        btn.className = 'lc-dot' + (i === 0 ? ' active' : '');
        btn.setAttribute('aria-label', 'Слайд ' + (i + 1));
        btn.dataset.page = i;
        btn.addEventListener('click', function () {
          scrollTo(parseInt(this.dataset.page, 10));
        });
        dotsEl.appendChild(btn);
      }
    }

    /* ── Update active dot & button states ── */
    function updateUI() {
      var pg = currentPage();
      var pc = pageCount();
      dotsEl.querySelectorAll('.lc-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === pg);
      });
      if (btnPrev) btnPrev.disabled = (pg === 0);
      if (btnNext) btnNext.disabled = (pg >= pc - 1);
    }

    /* ── Nav button clicks ── */
    if (btnPrev) btnPrev.addEventListener('click', function () {
      scrollTo(Math.max(0, currentPage() - 1));
    });
    if (btnNext) btnNext.addEventListener('click', function () {
      scrollTo(Math.min(pageCount() - 1, currentPage() + 1));
    });

    /* ── Scroll listener ── */
    var scrollTimer;
    track.addEventListener('scroll', function () {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(updateUI, 80);
    }, { passive: true });

    /* ── Rebuild on resize ── */
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        buildDots();
        updateUI();
      }, 150);
    });

    /* ── Init ── */
    buildDots();
    updateUI();
  })();

  /* Language switcher */
  var T = {
    ru: { nav_abit:'Абитуриентам', nav_programs:'Программы', nav_students:'Студентам', nav_news:'Новости', nav_contacts:'Контакты', btn_apply:'Поступить' },
    ky: { nav_abit:'Абитуриенттерге', nav_programs:'Программалар', nav_students:'Студенттерге', nav_news:'Жаңылыктар', nav_contacts:'Байланыш', btn_apply:'Тапшыруу' },
    en: { nav_abit:'For Applicants', nav_programs:'Programs', nav_students:'For Students', nav_news:'News', nav_contacts:'Contacts', btn_apply:'Apply' }
  };

  /* eslint-disable no-unused-vars */
  window.setLang = function (lang) {
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      b.classList.toggle('active', b.dataset.lang === lang);
    });
    var dict = T[lang] || T.ru;
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key]) el.textContent = dict[key];
    });
    try { localStorage.setItem('itcollege_lang', lang); } catch (e) { /* noop */ }
  };

  (function () {
    try {
      var s = localStorage.getItem('itcollege_lang');
      if (s && s !== 'ru' && T[s]) window.setLang(s);
    } catch (e) { /* noop */ }
  })();

  }); /* end DOMContentLoaded */

}());
