document.addEventListener('DOMContentLoaded', () => {
  initScrollProgress();
  initNavbar();
  initMobileMenu();
  initLangSwitcher();
  initMultiStepForm();
  initFileUploads();
  initRevealAnimations();
});


/* ─── Scroll Progress Bar ─── */
function initScrollProgress() {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const total = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (total > 0 ? (scrolled / total) * 100 : 0) + '%';
  }, { passive: true });
}

/* ─── Navbar Scroll ─── */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });
}

/* ─── Mobile Menu ─── */
function initMobileMenu() {
  const toggle   = document.getElementById('nav-toggle');
  const mobile   = document.getElementById('nav-mobile');
  const closeBtn = document.getElementById('nav-mobile-close');
  if (!toggle || !mobile) return;

  const open  = () => { mobile.classList.add('open'); toggle.classList.add('open'); document.body.style.overflow = 'hidden'; };
  const close = () => { mobile.classList.remove('open'); toggle.classList.remove('open'); document.body.style.overflow = ''; };

  toggle.addEventListener('click', () => mobile.classList.contains('open') ? close() : open());
  if (closeBtn) closeBtn.addEventListener('click', close);

  // Закрытие по клику на тёмный overlay (фон), но не на сам drawer
  mobile.addEventListener('click', (e) => {
    if (e.target === mobile) close();
  });
}

/* ─── Language Switcher ─── */
function initLangSwitcher() {
  const ls = document.getElementById('lang-switcher');
  const lb = document.getElementById('lang-btn');
  if (!lb || !ls) return;

  lb.addEventListener('click', (e) => { e.stopPropagation(); ls.classList.toggle('open'); });
  document.addEventListener('click', () => ls.classList.remove('open'));
}

function setLang(lang) {
  const FLAGS = { ru: '🇷🇺', ky: '🇰🇬', en: '🇬🇧' };
  const CODES  = { ru: 'RU',   ky: 'KY',   en: 'EN' };
  const T = {
    ru: { nav_abit: 'Абитуриентам', nav_programs: 'Программы', nav_students: 'Студентам', nav_news: 'Новости', nav_contacts: 'Контакты', btn_apply: 'Поступить' },
    ky: { nav_abit: 'Абитуриенттерге', nav_programs: 'Программалар', nav_students: 'Студенттерге', nav_news: 'Жаңылыктар', nav_contacts: 'Байланыш', btn_apply: 'Тапшыруу' },
    en: { nav_abit: 'For Applicants', nav_programs: 'Programs', nav_students: 'For Students', nav_news: 'News', nav_contacts: 'Contacts', btn_apply: 'Apply' }
  };
  const flagEl = document.getElementById('lang-flag');
  const codeEl = document.getElementById('lang-code');
  if (flagEl) flagEl.textContent = FLAGS[lang];
  if (codeEl) codeEl.textContent = CODES[lang];
  document.querySelectorAll('.lang-option').forEach(o => o.classList.toggle('active', o.dataset.lang === lang));
  const ls = document.getElementById('lang-switcher');
  if (ls) ls.classList.remove('open');
  const dict = T[lang] || T.ru;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) el.textContent = dict[key];
  });
  try { localStorage.setItem('itcollege_lang', lang); } catch(e) {}
}

// Restore saved language
(function() {
  try {
    const saved = localStorage.getItem('itcollege_lang');
    if (saved && saved !== 'ru') setLang(saved);
  } catch(e) {}
})();

/* ─── Multi-step Form ─── */
function initMultiStepForm() {
  const form = document.getElementById('applicationForm');
  if (!form) return;

  const steps  = form.querySelectorAll('.form-step');
  const pSteps = [
    document.getElementById('pStep1'),
    document.getElementById('pStep2'),
    document.getElementById('pStep3'),
  ];
  const pLines = [
    document.getElementById('pLine1'),
    document.getElementById('pLine2'),
  ];
  let current = 0;

  function showStep(idx) {
    steps.forEach((s, i) => s.classList.toggle('active', i === idx));
    pSteps.forEach((s, i) => {
      if (!s) return;
      s.classList.toggle('active', i === idx);
      s.classList.toggle('done',   i < idx);
    });
    pLines.forEach((l, i) => {
      if (!l) return;
      l.classList.toggle('done', i < idx);
    });
    window.scrollTo({ top: form.parentElement.offsetTop - 100, behavior: 'smooth' });
  }

  function validateStep(stepEl) {
    let isValid = true;
    const fields = stepEl.querySelectorAll('input[required], select[required], textarea[required]');

    fields.forEach(field => {
      field.style.borderColor = '';
      const existingMsg = field.parentElement.querySelector('.field-error');
      if (existingMsg) existingMsg.remove();

      let empty = field.type === 'file' ? field.files.length === 0 : !field.value.trim();

      if (empty) {
        isValid = false;
        field.style.borderColor = '#ef4444';
        const msg = document.createElement('span');
        msg.className = 'field-error';
        msg.style.cssText = 'color:#ef4444;font-size:12px;margin-top:4px;display:block;';
        msg.textContent = 'Это поле обязательно для заполнения';
        field.parentElement.appendChild(msg);

        field.addEventListener('input', () => {
          field.style.borderColor = '';
          const m = field.parentElement.querySelector('.field-error');
          if (m) m.remove();
        }, { once: true });

        field.addEventListener('change', () => {
          field.style.borderColor = '';
          const m = field.parentElement.querySelector('.field-error');
          if (m) m.remove();
        }, { once: true });
      }
    });

    if (!isValid) {
      const firstError = stepEl.querySelector('input[style*="border-color"], select[style*="border-color"]');
      if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return isValid;
  }

  form.querySelectorAll('[data-next]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const currentStepEl = steps[current];
      if (!validateStep(currentStepEl)) return;
      if (current < steps.length - 1) { current++; showStep(current); }
    });
  });

  form.querySelectorAll('[data-prev]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (current > 0) { current--; showStep(current); }
    });
  });

  const confirmScreen = document.getElementById('confirmationScreen');
  const progressWrap  = document.getElementById('progressBar');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const currentStepEl = steps[current];
    if (!validateStep(currentStepEl)) return;

    const formData = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
    })
    .then(res => { if (!res.ok) return res.json().then(d => Promise.reject(d)); return res.json(); })
    .then(data => {
      if (data.status === 'success') {
        form.style.display = 'none';
        if (progressWrap) progressWrap.style.display = 'none';
        if (confirmScreen) {
          confirmScreen.classList.add('active');
          confirmScreen.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      } else {
        alert(data.message || 'Ошибка при отправке');
      }
    })
    .catch(err => { console.error(err); alert(err.message || 'Ошибка при отправке формы'); });
  });

  showStep(0);
}

/* ─── File Uploads ─── */
function initFileUploads() {
  document.querySelectorAll('input[type="file"]').forEach(function(input) {
    input.addEventListener('change', function() {
      const label = input.closest('.form-group')?.querySelector('.file-label');
      if (label && input.files.length > 0) {
        label.textContent = input.files[0].name;
      }
    });
  });
}

/* ─── Reveal Animations ─── */
function initRevealAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
    observer.observe(el);
  });
}