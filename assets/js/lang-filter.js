/**
 * MACH Playbook - Global i18n & Post Filter Engine
 * Handles site-wide Spanish/English language switching, UI localization,
 * bilingual static page toggle, and home post feed filtering.
 */
(function() {
  'use strict';

  var PAGE_SIZE = 10;
  var currentPage = 1;
  var currentLang = 'es'; // Spanish is default

  var TAB_LOCALIZATIONS = {
    'home': { es: 'Inicio', en: 'Home' },
    'categories': { es: 'Categorías', en: 'Categories' },
    'tags': { es: 'Etiquetas', en: 'Tags' },
    'archives': { es: 'Archivo', en: 'Archives' },
    'resources': { es: 'Recursos', en: 'Resources' },
    'glossary': { es: 'Glosario', en: 'Glossary' },
    'about': { es: 'Acerca de', en: 'About' },
    'contact': { es: 'Contacto', en: 'Contact' },
    'privacy': { es: 'Privacidad', en: 'Privacy Policy' },
    'terms': { es: 'Términos', en: 'Terms' }
  };

  function getUrlParam(param) {
    try {
      var urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    } catch (e) {
      return null;
    }
  }

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

  function unpackRemainingPostsIfNeeded() {
    var dataEl = document.getElementById('remaining-posts-data');
    if (!dataEl) return;
    try {
      var posts = JSON.parse(dataEl.textContent);
      var postList = document.getElementById('post-list');
      if (postList && Array.isArray(posts)) {
        posts.forEach(function(post) {
          var article = document.createElement('article');
          article.className = 'card-wrapper card post-card-item';
          article.setAttribute('data-post-lang', post.lang || 'es');
          article.style.display = 'none';

          var categoriesHtml = '';
          if (post.categories && post.categories.length) {
            categoriesHtml = '<i class="far fa-folder-open fa-fw me-1"></i><span class="categories">' +
              post.categories.join(', ') + '</span>';
          }

          var badgeHtml = post.lang === 'es' ?
            '<span class="badge border border-primary text-primary ms-2" style="font-weight: 500; font-size: 0.75rem; padding: 0.2em 0.55em; border-radius: 4px;">🇲🇽/🇪🇸 Español</span>' :
            '<span class="badge border border-secondary text-muted ms-2" style="font-weight: 500; font-size: 0.75rem; padding: 0.2em 0.55em; border-radius: 4px;">🇺🇸 English</span>';

          var imgHtml = '';
          if (post.image && post.image.src) {
            imgHtml = '<div class="col-md-5">' +
              '<div class="preview-img shimmer">' +
                '<picture>' +
                  '<source srcset="' + (post.image.webp || post.image.src) + '" type="image/webp">' +
                  '<img src="' + (post.image.webp || post.image.src) + '" alt="' + (post.image.alt || 'Preview Image') + '" width="400" height="225" loading="lazy" decoding="async" style="aspect-ratio: 16/9; object-fit: cover;">' +
                '</picture>' +
              '</div>' +
            '</div>';
          }

          var bodyCol = imgHtml ? '7' : '12';

          article.innerHTML = '<a href="' + post.url + '" class="post-preview row g-0 flex-md-row-reverse">' +
            imgHtml +
            '<div class="col-md-' + bodyCol + '">' +
              '<div class="card-body d-flex flex-column">' +
                '<h1 class="card-title my-2 mt-md-0">' + post.title + '</h1>' +
                '<div class="card-text content mt-0 mb-3"><p>' + (post.summary || '') + '</p></div>' +
                '<div class="post-meta flex-grow-1 d-flex align-items-end">' +
                  '<div class="me-auto">' +
                    '<i class="far fa-calendar fa-fw me-1"></i>' +
                    '<span>' + post.date + '</span>' +
                    categoriesHtml +
                    badgeHtml +
                  '</div>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</a>';

          postList.appendChild(article);
        });
      }
    } catch (e) {
      console.error('Error unpacking remaining posts:', e);
    }
    dataEl.remove();
  }

  function goToPage(page) {
    unpackRemainingPostsIfNeeded();
    currentPage = page;
    updatePostCardsView();
    var postList = document.getElementById('post-list');
    if (postList) {
      postList.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function updatePostCardsView() {
    if (currentPage > 1 || currentLang === 'all' || currentLang === 'en') {
      unpackRemainingPostsIfNeeded();
    }

    var cards = Array.from(document.querySelectorAll('.post-card-item'));
    if (!cards.length) return;

    // 1. Filter matching cards
    var matchingCards = cards.filter(function(card) {
      var cardLang = card.getAttribute('data-post-lang') || 'es';
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
        statusEl.textContent = 'Mostrando ' + totalMatching + ' artículo' + (totalMatching === 1 ? '' : 's') + ' en Español';
      } else if (currentLang === 'en') {
        statusEl.textContent = 'Showing ' + totalMatching + ' English post' + (totalMatching === 1 ? '' : 's');
      } else {
        statusEl.textContent = 'Mostrando todos los ' + totalMatching + ' artículos / Showing all posts';
      }
    }

    // 5. Render dynamic pagination
    renderPagination(totalMatching, currentPage);
  }

  function applyLocalization(lang) {
    var isEnglish = (lang === 'en');

    // 1. Localize all data-i18n elements (sidebar, menu links, breadcrumbs)
    document.querySelectorAll('[data-i18n-es]').forEach(function(el) {
      var esText = el.getAttribute('data-i18n-es');
      var enText = el.getAttribute('data-i18n-en') || esText;
      el.textContent = isEnglish ? enText : esText;
    });

    // 2. Localize bilingual content blocks on static pages (About, Contact, Privacy, Terms)
    document.querySelectorAll('.lang-block.lang-es').forEach(function(el) {
      if (isEnglish) {
        el.classList.add('d-none');
      } else {
        el.classList.remove('d-none');
      }
    });

    document.querySelectorAll('.lang-block.lang-en').forEach(function(el) {
      if (isEnglish) {
        el.classList.remove('d-none');
      } else {
        el.classList.add('d-none');
      }
    });

    // 3. Update topbar title & breadcrumb if on a tab page
    var currentPath = window.location.pathname.replace(/^\/|\/$/g, '');
    if (TAB_LOCALIZATIONS[currentPath]) {
      var localizedTabName = isEnglish ? TAB_LOCALIZATIONS[currentPath].en : TAB_LOCALIZATIONS[currentPath].es;
      var topbarTitle = document.getElementById('topbar-title');
      if (topbarTitle) {
        topbarTitle.textContent = localizedTabName;
      }
      var breadcrumb = document.getElementById('breadcrumb');
      if (breadcrumb) {
        var lastSpan = breadcrumb.querySelector('span:last-child');
        if (lastSpan) {
          lastSpan.textContent = localizedTabName;
        }
      }
    }
  }

  function setLanguage(lang) {
    currentLang = lang || 'es';
    currentPage = 1;

    try {
      localStorage.setItem('mach_playbook_lang', currentLang);
    } catch (e) {}

    // Update Topbar Dropdown UI
    var flagEl = document.getElementById('current-lang-flag');
    var textEl = document.getElementById('current-lang-text');
    if (flagEl && textEl) {
      if (currentLang === 'es') {
        flagEl.textContent = '🇲🇽';
        textEl.textContent = 'ES';
      } else if (currentLang === 'en') {
        flagEl.textContent = '🇺🇸';
        textEl.textContent = 'EN';
      } else {
        flagEl.textContent = '🌐';
        textEl.textContent = 'ALL';
      }
    }

    document.querySelectorAll('.lang-select-opt').forEach(function(opt) {
      if (opt.getAttribute('data-lang') === currentLang) {
        opt.classList.add('active');
      } else {
        opt.classList.remove('active');
      }
    });

    // Update Home Filter Pills UI
    document.querySelectorAll('.lang-pill').forEach(function(pill) {
      if (pill.getAttribute('data-lang-target') === currentLang) {
        pill.classList.add('active', 'btn-primary');
        pill.classList.remove('btn-outline-secondary');
      } else {
        pill.classList.remove('active', 'btn-primary');
        pill.classList.add('btn-outline-secondary');
      }
    });

    // Apply translations across UI and static page blocks
    applyLocalization(currentLang);

    // Apply card filtering on home feed
    updatePostCardsView();
  }

  window.setLanguageFilter = setLanguage;
  window.setGlobalLanguage = setLanguage;

  function init() {
    var urlLang = getUrlParam('lang');
    var savedLang = null;
    try {
      savedLang = localStorage.getItem('mach_playbook_lang');
    } catch (e) {}

    // Priority: URL query param > LocalStorage > Default 'es'
    var initialLang = urlLang || savedLang || 'es';

    // Setup click listeners on topbar options
    document.querySelectorAll('.lang-select-opt').forEach(function(opt) {
      opt.addEventListener('click', function(e) {
        e.preventDefault();
        var selected = this.getAttribute('data-lang');
        setLanguage(selected);
      });
    });

    // Setup click listeners on home pills
    document.querySelectorAll('.lang-pill').forEach(function(pill) {
      pill.addEventListener('click', function(e) {
        e.preventDefault();
        var selected = this.getAttribute('data-lang-target');
        setLanguage(selected);
      });
    });

    setLanguage(initialLang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
