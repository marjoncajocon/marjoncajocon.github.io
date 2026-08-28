/* Progressive enhancement only: every feature here degrades to plain HTML.
   The gallery links go straight to the full image without JS, and the About
   panel is a <dialog> that simply does not open. */
(function () {
  // Theme. Kept compatible with the previous site's localStorage key.
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('theme');
    if (saved) root.setAttribute('data-theme', saved);
    else if (window.matchMedia('(prefers-color-scheme: light)').matches)
      root.setAttribute('data-theme', 'light');
  } catch (e) { /* private mode: fall through to the dark default */ }

  var t = document.getElementById('themeToggle');
  if (t) t.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // About overlay.
  var dlg = document.getElementById('aboutDlg');
  var open = document.getElementById('aboutBtn');
  var close = document.getElementById('aboutClose');
  if (dlg && open && typeof dlg.showModal === 'function') {
    open.addEventListener('click', function () { dlg.showModal(); });
    if (close) close.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  } else if (open) {
    open.hidden = true; // no <dialog> support: do not offer a button that does nothing
  }

  // Lightbox.
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  var lbCap = document.getElementById('lbCap');
  var lbClose = document.getElementById('lbClose');
  if (!lb) return;
  function show(href, cap, alt) {
    lbImg.src = href; lbImg.alt = alt || ''; lbCap.textContent = cap || '';
    lb.classList.add('is-open'); lbClose.focus();
  }
  function hide() { lb.classList.remove('is-open'); lbImg.src = ''; }
  document.querySelectorAll('a.shot').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      show(a.getAttribute('href'), a.dataset.cap, a.querySelector('img').alt);
    });
  });
  lbClose.addEventListener('click', hide);
  lb.addEventListener('click', function (e) { if (e.target === lb) hide(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lb.classList.contains('is-open')) hide();
  });
})();
