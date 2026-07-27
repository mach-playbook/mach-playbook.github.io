(function() {
  function setLanguageFilter(lang) {
    try {
      localStorage.setItem('mach_playbook_lang', lang);
    } catch(e) {}
    
    // Update Topbar Dropdown UI
    var currentText = document.getElementById('current-lang-text');
    if (currentText) {
      if (lang === 'es') currentText.textContent = 'Español';
      else if (lang === 'en') currentText.textContent = 'English';
      else currentText.textContent = 'All';
    }

    document.querySelectorAll('.lang-select-opt').forEach(function(opt) {
      if (opt.getAttribute('data-lang') === lang) {
        opt.classList.add('active');
      } else {
        opt.classList.remove('active');
      }
    });

    // Update Home Filter Pills UI
    document.querySelectorAll('.lang-pill').forEach(function(pill) {
      if (pill.getAttribute('data-lang-target') === lang) {
        pill.classList.add('active', 'btn-primary');
        pill.classList.remove('btn-outline-secondary');
      } else {
        pill.classList.remove('active', 'btn-primary');
        pill.classList.add('btn-outline-secondary');
      }
    });

    var statusEl = document.getElementById('lang-filter-status');
    if (statusEl) {
      if (lang === 'es') statusEl.textContent = 'Filtered: Spanish posts';
      else if (lang === 'en') statusEl.textContent = 'Filtered: English posts';
      else statusEl.textContent = 'Showing all posts';
    }

    // Filter Post Cards
    var cards = document.querySelectorAll('.post-card-item');
    var visibleCount = 0;

    cards.forEach(function(card) {
      var cardLang = card.getAttribute('data-post-lang');
      if (lang === 'all' || cardLang === lang) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    var noResults = document.getElementById('no-lang-results');
    if (noResults) {
      if (visibleCount === 0 && cards.length > 0) {
        noResults.classList.remove('d-none');
      } else {
        noResults.classList.add('d-none');
      }
    }
  }

  window.setLanguageFilter = setLanguageFilter;

  function initLangFilter() {
    var savedLang = 'all';
    try {
      savedLang = localStorage.getItem('mach_playbook_lang') || 'all';
    } catch(e) {}
    
    setLanguageFilter(savedLang);

    document.querySelectorAll('.lang-select-opt').forEach(function(opt) {
      opt.addEventListener('click', function(e) {
        e.preventDefault();
        var selected = this.getAttribute('data-lang');
        setLanguageFilter(selected);
      });
    });

    document.querySelectorAll('.lang-pill').forEach(function(pill) {
      pill.addEventListener('click', function(e) {
        e.preventDefault();
        var selected = this.getAttribute('data-lang-target');
        setLanguageFilter(selected);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLangFilter);
  } else {
    initLangFilter();
  }
})();
