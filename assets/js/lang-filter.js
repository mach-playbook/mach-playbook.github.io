(function() {
  var PAGE_SIZE = 10;
  var currentPage = 1;
  var currentLang = 'all';

  function renderPagination(totalItems, activePage) {
    var container = document.getElementById('dynamic-paginator');
    if (!container) return;

    var totalPages = Math.ceil(totalItems / PAGE_SIZE);
    if (totalPages <= 1) {
      container.innerHTML = '';
      return;
    }

    var html = '<nav aria-label="Page Navigation"><ul class="pagination align-items-center justify-content-center mb-0">';

    // Previous button
    if (activePage > 1) {
      html += '<li class="page-item"><a class="page-link btn-box-shadow" href="#" data-page="' + (activePage - 1) + '" aria-label="Previous">&laquo;</a></li>';
    } else {
      html += '<li class="page-item disabled"><span class="page-link">&laquo;</span></li>';
    }

    // Page numbers
    for (var p = 1; p <= totalPages; p++) {
      if (p === activePage) {
        html += '<li class="page-item active"><span class="page-link btn-box-shadow">' + p + '</span></li>';
      } else {
        html += '<li class="page-item"><a class="page-link btn-box-shadow" href="#" data-page="' + p + '">' + p + '</a></li>';
      }
    }

    // Next button
    if (activePage < totalPages) {
      html += '<li class="page-item"><a class="page-link btn-box-shadow" href="#" data-page="' + (activePage + 1) + '" aria-label="Next">&raquo;</a></li>';
    } else {
      html += '<li class="page-item disabled"><span class="page-link">&raquo;</span></li>';
    }

    html += '</ul></nav>';
    container.innerHTML = html;

    // Attach click handlers
    container.querySelectorAll('a.page-link[data-page]').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        var targetPage = parseInt(this.getAttribute('data-page'), 10);
        goToPage(targetPage);
      });
    });
  }

  function goToPage(page) {
    currentPage = page;
    updateView();
    var postList = document.getElementById('post-list');
    if (postList) {
      postList.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function updateView() {
    var cards = Array.from(document.querySelectorAll('.post-card-item'));
    if (!cards.length) return;

    // 1. Filter matching cards
    var matchingCards = cards.filter(function(card) {
      var cardLang = card.getAttribute('data-post-lang');
      return currentLang === 'all' || cardLang === currentLang;
    });

    var totalMatching = matchingCards.length;
    var totalPages = Math.ceil(totalMatching / PAGE_SIZE) || 1;
    if (currentPage > totalPages) {
      currentPage = 1;
    }

    var startIndex = (currentPage - 1) * PAGE_SIZE;
    var endIndex = startIndex + PAGE_SIZE;

    // 2. Hide all cards first
    cards.forEach(function(card) {
      card.style.display = 'none';
    });

    // 3. Show only cards on current page of the filter
    matchingCards.slice(startIndex, endIndex).forEach(function(card) {
      card.style.display = '';
    });

    // 4. Status and Empty state
    var noResults = document.getElementById('no-lang-results');
    if (noResults) {
      if (totalMatching === 0) {
        noResults.classList.remove('d-none');
      } else {
        noResults.classList.add('d-none');
      }
    }

    var statusEl = document.getElementById('lang-filter-status');
    if (statusEl) {
      if (currentLang === 'es') {
        statusEl.textContent = 'Filtered: ' + totalMatching + ' Spanish post' + (totalMatching === 1 ? '' : 's');
      } else if (currentLang === 'en') {
        statusEl.textContent = 'Filtered: ' + totalMatching + ' English post' + (totalMatching === 1 ? '' : 's');
      } else {
        statusEl.textContent = 'Showing all ' + totalMatching + ' posts';
      }
    }

    // 5. Render dynamic pagination
    renderPagination(totalMatching, currentPage);
  }

  function setLanguageFilter(lang) {
    currentLang = lang;
    currentPage = 1;

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

    updateView();
  }

  window.setLanguageFilter = setLanguageFilter;

  function initLangFilter() {
    var savedLang = 'all';
    try {
      savedLang = localStorage.getItem('mach_playbook_lang') || 'all';
    } catch(e) {}

    // Setup click listeners on options and pills
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

    setLanguageFilter(savedLang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLangFilter);
  } else {
    initLangFilter();
  }
})();
