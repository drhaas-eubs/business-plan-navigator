/* ============================================================
   The Business Plan Navigator · Framework Sheet Viewer
   Protected PDF rendering with page-anchored navigation
   © 2026 Dr. Hildegard Haas · EU Business School

   Usage:
     1. Load PDF.js (CDN) and this file on every unit page.
     2. Call FW.openPage(N) to open the modal at page N.
     3. Add data-fw-slug="..." to any thumbnail to make it clickable.
     4. The pill button uses class "fw-viewer-pill" + data-fw-slug
        or data-fw-page.
   ============================================================ */
(function () {
  'use strict';

  /* ----- Configuration ---------------------------------------- */
  const PDF_PATH = 'assets/pdf/framework-library.pdf';
  const PDFJS_VERSION = '3.11.174';
  const PDFJS_LIB = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${PDFJS_VERSION}/pdf.min.js`;
  const PDFJS_WORKER = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${PDFJS_VERSION}/pdf.worker.min.js`;

  /* ----- Page anchor mapping ---------------------------------- */
  /* Page formula: page = 8 + 5*(slibrary-1) + sheet
     (Cover=1, Master Index pp.2-7, "How to Use" p.8, sheets start p.9) */
  const FRAMEWORKS = [
    { page:1, name:'PESTEL Analysis', partname:'Part I · Proposal', chap:'Purpose & Objectives' },
    { page:2, name:'Porter\'s Five Forces', partname:'Part I · Proposal', chap:'Purpose & Objectives' },
    { page:3, name:'SWOT Analysis', partname:'Part I · Proposal', chap:'Purpose & Objectives' },
    { page:4, name:'TOWS Matrix', partname:'Part I · Proposal', chap:'Purpose & Objectives' },
    { page:5, name:'Value Proposition Canvas', partname:'Part I · Proposal', chap:'Product / Service Concept' },
    { page:6, name:'Jobs to Be Done', partname:'Part I · Proposal', chap:'Product / Service Concept' },
    { page:7, name:'TAM / SAM / SOM', partname:'Part I · Proposal', chap:'Market & Target Customer' },
    { page:8, name:'STP — Segmentation, Targeting, Positioning', partname:'Part I · Proposal', chap:'Market & Target Customer' },
    { page:9, name:'SMART Objectives', partname:'Part I · Proposal', chap:'Objectives' },
    { page:10, name:'Balanced Scorecard', partname:'Part I · Proposal', chap:'Objectives' },
    { page:11, name:'OKR', partname:'Part I · Proposal', chap:'Objectives' },
    { page:12, name:'Business Model Canvas', partname:'Part I · Proposal', chap:'Concept' },
    { page:13, name:'Lean Startup / MVP', partname:'Part I · Proposal', chap:'Concept' },
    { page:14, name:'Gantt Chart', partname:'Part I · Proposal', chap:'Timeline' },
    { page:15, name:'Risk Register (ISO 31000)', partname:'Part I · Proposal', chap:'Timeline' },
    { page:16, name:'Harvard Referencing', partname:'Part I · Proposal', chap:'Academic Standards' },
    { page:17, name:'Pyramid Principle', partname:'Part II · Business Plan', chap:'Executive Summary' },
    { page:18, name:'Golden Circle', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:19, name:'Vision, Mission & Core Values', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:20, name:'VRIO Framework', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:21, name:'Generic Competitive Strategies', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:22, name:'Ansoff Growth Matrix', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:23, name:'Blue Ocean / Strategy Canvas', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:24, name:'Competitor Analysis Framework', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:25, name:'Strategic Group Mapping', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:26, name:'Competitive Profile Matrix', partname:'Part II · Business Plan', chap:'Business Identity' },
    { page:27, name:'Benchmarking', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:28, name:'Perceptual Mapping', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:29, name:'Marketing Mix — 4Ps / 7Ps', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:30, name:'Positioning Statement', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:31, name:'Customer Journey Mapping', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:32, name:'AIDA Funnel', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:33, name:'AARRR Pirate Metrics', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:34, name:'CLV / CAC Ratio', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:35, name:'Value-Based Pricing', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:36, name:'Diffusion of Innovations', partname:'Part II · Business Plan', chap:'Marketing Plan' },
    { page:37, name:'Value Chain Analysis', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:38, name:'Service Blueprint', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:39, name:'Lean Thinking / Waste Elimination', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:40, name:'Capacity & Bottleneck Planning', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:41, name:'SCOR Model', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:42, name:'Quality Management (ISO 9001)', partname:'Part II · Business Plan', chap:'Operations Plan' },
    { page:43, name:'Mintzberg\'s Organisational Configurations', partname:'Part II · Business Plan', chap:'Organization Plan' },
    { page:44, name:'RACI Matrix', partname:'Part II · Business Plan', chap:'Organization Plan' },
    { page:45, name:'Belbin Team Roles', partname:'Part II · Business Plan', chap:'Organization Plan' },
    { page:46, name:'Tuckman Group Development', partname:'Part II · Business Plan', chap:'Organization Plan' },
    { page:47, name:'Schein\'s Levels of Culture', partname:'Part II · Business Plan', chap:'Organization Plan' },
    { page:48, name:'Five-Year P&L, Balance Sheet & Cash Flow', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:49, name:'Break-Even / CVP Analysis', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:50, name:'NPV, IRR & Payback', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:51, name:'WACC & Capital Structure', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:52, name:'Sensitivity & Scenario Analysis', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:53, name:'Legal Form & Statutory Reserve', partname:'Part II · Business Plan', chap:'Financial Plan' },
    { page:54, name:'Toulmin Model of Argument', partname:'Part II · Business Plan', chap:'Analytical Thinking' },
    { page:55, name:'The Logical Chain', partname:'Part II · Business Plan', chap:'Analytical Thinking' },
    { page:56, name:'Thumbnail Thinking', partname:'Part III · Defense', chap:'Storyboarding' },
    { page:57, name:'Message Strategy — one clear message', partname:'Part III · Defense', chap:'Message Strategy' },
    { page:58, name:'Assertion–Evidence Structure', partname:'Part III · Defense', chap:'Slide Design' },
    { page:59, name:'Sparkline / What Is — What Could Be', partname:'Part III · Defense', chap:'Narrative' },
    { page:60, name:'Pyramid Principle for Speaking', partname:'Part III · Defense', chap:'Narrative' },
    { page:61, name:'Multimedia & Cognitive Load Principles', partname:'Part III · Defense', chap:'Slide Design' },
    { page:62, name:'Question Anticipation Matrix', partname:'Part III · Defense', chap:'Q&A' },
    { page:63, name:'EUBS Defense Slide Requirements', partname:'Part III · Defense', chap:'Compliance' }
  ];

  /* Compute page anchors */
  /* pages are explicit */

  /* Build lookup map by slug */
  const SLUG_TO_FW = {};
  /* pages are explicit */

  /* Unit overview pages: jump to that unit's first sheet */
  const UNIT_PAGES = { 1: 1, 2: 17, 3: 56 };

  /* ----- Slibrary metadata (from Dr. Haas's actual unit files) - */
  const UNIT_TITLES = {
    1: 'The Proposal',
    2: 'The Final Business Plan',
    3: 'The Jury Defense'
  };

  const SLIBRARIES = [
    { num: 1, unit: 1, title: "Purpose & Objectives", color: '#1E40AF', firstPage: 1, count: 4 },
    { num: 2, unit: 1, title: "Product / Service Concept", color: '#1E40AF', firstPage: 5, count: 2 },
    { num: 3, unit: 1, title: "Market & Target Customer", color: '#1E40AF', firstPage: 7, count: 2 },
    { num: 4, unit: 1, title: "Objectives", color: '#1E40AF', firstPage: 9, count: 3 },
    { num: 5, unit: 1, title: "Concept", color: '#1E40AF', firstPage: 12, count: 2 },
    { num: 6, unit: 1, title: "Timeline", color: '#1E40AF', firstPage: 14, count: 2 },
    { num: 7, unit: 1, title: "Academic Standards", color: '#1E40AF', firstPage: 16, count: 1 },
    { num: 8, unit: 2, title: "Executive Summary", color: '#2563EB', firstPage: 17, count: 1 },
    { num: 9, unit: 2, title: "Business Identity", color: '#2563EB', firstPage: 18, count: 9 },
    { num: 10, unit: 2, title: "Operations Plan", color: '#2563EB', firstPage: 27, count: 7 },
    { num: 11, unit: 2, title: "Marketing Plan", color: '#2563EB', firstPage: 28, count: 9 },
    { num: 12, unit: 2, title: "Organization Plan", color: '#2563EB', firstPage: 43, count: 5 },
    { num: 13, unit: 2, title: "Financial Plan", color: '#2563EB', firstPage: 48, count: 6 },
    { num: 14, unit: 2, title: "Analytical Thinking", color: '#2563EB', firstPage: 54, count: 2 },
    { num: 15, unit: 3, title: "Storyboarding", color: '#B45309', firstPage: 56, count: 1 },
    { num: 16, unit: 3, title: "Message Strategy", color: '#B45309', firstPage: 57, count: 1 },
    { num: 17, unit: 3, title: "Slide Design", color: '#B45309', firstPage: 58, count: 2 },
    { num: 18, unit: 3, title: "Narrative", color: '#B45309', firstPage: 59, count: 2 },
    { num: 19, unit: 3, title: "Q&A", color: '#B45309', firstPage: 62, count: 1 },
    { num: 20, unit: 3, title: "Compliance", color: '#B45309', firstPage: 63, count: 1 }
  ];

  /* ----- State ----------------------------------------------- */
  let pdfDoc = null;
  let currentPage = 1;
  let totalPages = 128;
  let isRendering = false;
  let pdfjsReady = null; /* Promise */

  /* ----- DOM injection --------------------------------------- */
  function buildModalDOM() {
    if (document.getElementById('fw-viewer-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'fw-viewer-overlay';
    overlay.className = 'fw-viewer-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'fw-viewer-title');
    overlay.innerHTML = `
      <div class="fw-viewer-modal" id="fw-viewer-modal">
        <header class="fw-viewer-header">
          <div style="min-width:0; flex:1;">
            <h2 class="fw-viewer-title" id="fw-viewer-title">Framework Reference Sheet</h2>
            <span class="fw-viewer-title-meta" id="fw-viewer-meta">The Business Plan Navigator</span>
          </div>
          <div class="fw-viewer-controls">
            <div class="fw-search-wrap" id="fw-search-wrap">
              <svg class="fw-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
              <input type="search" id="fw-search-input" class="fw-search-input" placeholder="Search PDF…" aria-label="Search PDF text" autocomplete="off">
              <span class="fw-search-status" id="fw-search-status"></span>
              <button type="button" class="fw-search-nav-btn" id="fw-search-prev" aria-label="Previous match" title="Previous match (Shift+Enter)" disabled>‹</button>
              <button type="button" class="fw-search-nav-btn" id="fw-search-next" aria-label="Next match" title="Next match (Enter)" disabled>›</button>
              <button type="button" class="fw-search-clear-btn" id="fw-search-clear" aria-label="Clear search" title="Clear">×</button>
            </div>
            <button type="button" class="fw-btn" id="fw-btn-prev" aria-label="Previous sheet" title="Previous (←)">‹</button>
            <span class="fw-page-indicator" id="fw-page-indicator">– / –</span>
            <button type="button" class="fw-btn" id="fw-btn-next" aria-label="Next sheet" title="Next (→)">›</button>
            <button type="button" class="fw-btn" id="fw-btn-zoom-out" aria-label="Zoom out" title="Zoom out (−)">−</button>
            <button type="button" class="fw-btn" id="fw-btn-zoom-in" aria-label="Zoom in" title="Zoom in (+)">+</button>
            <button type="button" class="fw-btn-close" id="fw-btn-close" aria-label="Close (Esc)" title="Close (Esc)">×</button>
          </div>
        </header>
        <div class="fw-viewer-body" id="fw-viewer-body">
          <div class="fw-loading" id="fw-loading">Loading framework library…</div>
          <div class="fw-canvas-wrap" id="fw-canvas-wrap" style="display:none;">
            <canvas class="fw-canvas" id="fw-canvas"></canvas>
            <div class="fw-highlight-layer" id="fw-highlight-layer" aria-hidden="true"></div>
          </div>
        </div>
        <footer class="fw-viewer-footer">
          <strong>The Business Plan Navigator · Framework Reference Library</strong> · 63 Frameworks · 63 Reference Sheets · © 2026 Prof. Dr. Hildegard Haas · EU Business School · All rights reserved
        </footer>
      </div>
    `;
    document.body.appendChild(overlay);
  }

  /* ----- PDF.js loader --------------------------------------- */
  function loadPdfJs() {
    if (pdfjsReady) return pdfjsReady;
    pdfjsReady = new Promise((resolve, reject) => {
      if (window.pdfjsLib) { resolve(window.pdfjsLib); return; }
      const script = document.createElement('script');
      script.src = PDFJS_LIB;
      script.onload = () => {
        if (window.pdfjsLib) {
          window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER;
          resolve(window.pdfjsLib);
        } else {
          reject(new Error('PDF.js failed to load'));
        }
      };
      script.onerror = () => reject(new Error('PDF.js failed to load'));
      document.head.appendChild(script);
    });
    return pdfjsReady;
  }

  /* ----- Rendering -------------------------------------------- */
  let zoomScale = 1.0;
  const ZOOM_MIN = 0.6;
  const ZOOM_MAX = 2.5;
  const ZOOM_STEP = 0.2;

  async function renderPage(pageNum) {
    if (!pdfDoc || isRendering) return;
    if (pageNum < 1 || pageNum > totalPages) return;
    isRendering = true;
    currentPage = pageNum;

    const loading = document.getElementById('fw-loading');
    const wrap    = document.getElementById('fw-canvas-wrap');
    const canvas  = document.getElementById('fw-canvas');
    const ctx     = canvas.getContext('2d');

    try {
      const page = await pdfDoc.getPage(pageNum);
      const containerWidth = document.getElementById('fw-viewer-body').clientWidth - 40;
      const baseViewport   = page.getViewport({ scale: 1.0 });
      const fitScale       = Math.min(containerWidth / baseViewport.width, 1.6);
      const dpr            = window.devicePixelRatio || 1;
      const viewport       = page.getViewport({ scale: fitScale * zoomScale });

      canvas.width  = Math.floor(viewport.width  * dpr);
      canvas.height = Math.floor(viewport.height * dpr);
      canvas.style.width  = Math.floor(viewport.width)  + 'px';
      canvas.style.height = Math.floor(viewport.height) + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      await page.render({ canvasContext: ctx, viewport }).promise;

      loading.style.display = 'none';
      wrap.style.display    = 'block';

      updateMeta(pageNum);
      updateNavButtons();
      /* Redraw search highlights for the newly rendered page */
      if (searchQuery) drawHighlights();
    } catch (err) {
      console.error('FW viewer render error:', err);
      loading.textContent = 'Could not load the framework sheet. Please try again.';
    } finally {
      isRendering = false;
    }
  }

  function updateMeta(pageNum) {
    const fw = FRAMEWORKS.find(f => f.page === pageNum);
    const titleEl = document.getElementById('fw-viewer-title');
    const metaEl  = document.getElementById('fw-viewer-meta');
    const indEl   = document.getElementById('fw-page-indicator');
    if (fw) {
      titleEl.textContent = fw.name;
      metaEl.textContent  = fw.partname + ' \u00b7 ' + fw.chap;
    } else {
      titleEl.textContent = 'Framework Reference Sheet';
      metaEl.textContent  = 'The Business Plan Navigator';
    }
    indEl.textContent = pageNum + ' / ' + totalPages;
  }

  function updateNavButtons() {
    document.getElementById('fw-btn-prev').disabled = (currentPage <= 1);
    document.getElementById('fw-btn-next').disabled = (currentPage >= totalPages);
    document.getElementById('fw-btn-zoom-out').disabled = (zoomScale <= ZOOM_MIN + 0.01);
    document.getElementById('fw-btn-zoom-in').disabled  = (zoomScale >= ZOOM_MAX - 0.01);
  }

  /* ----- PDF text search ------------------------------------- */
  /* On-demand text indexing: extract page text via PDF.js getTextContent
     the first time the user searches, then cache. */
  const pageTextCache = new Map();   /* pageNum -> [{ str, transform, width, height, fontName }, ...] */
  let searchMatches   = [];          /* [{ pageNum, items: [{itemIdx, charStart, charEnd}], pageStr, pageMatchIdx }, ...]
                                        flattened: each match is one occurrence on one page */
  let currentMatchIdx = -1;
  let searchQuery     = '';
  let searchIndexing  = false;

  async function indexAllPages() {
    if (pageTextCache.size === totalPages) return;
    searchIndexing = true;
    setSearchStatus('Indexing…');
    /* Index in chunks so the UI stays responsive */
    for (let p = 1; p <= totalPages; p++) {
      if (pageTextCache.has(p)) continue;
      try {
        const page = await pdfDoc.getPage(p);
        const tc = await page.getTextContent();
        /* Build a contiguous text string for this page + map back to items */
        let pageStr = '';
        const itemRanges = [];
        for (let i = 0; i < tc.items.length; i++) {
          const it = tc.items[i];
          const start = pageStr.length;
          pageStr += it.str;
          itemRanges.push({ start, end: pageStr.length, item: it });
          /* Add a space between items if PDF.js indicates a hard break */
          if (it.hasEOL) pageStr += '\n';
          else pageStr += ' ';
        }
        pageTextCache.set(p, { pageStr, itemRanges });
      } catch (err) {
        console.warn('PDF index error on page', p, err);
        pageTextCache.set(p, { pageStr: '', itemRanges: [] });
      }
      /* Yield to browser every 16 pages */
      if (p % 16 === 0) await new Promise(r => setTimeout(r, 0));
    }
    searchIndexing = false;
  }

  function findAllMatches(query) {
    const matches = [];
    if (!query) return matches;
    const q = query.toLowerCase();
    for (let p = 1; p <= totalPages; p++) {
      const cache = pageTextCache.get(p);
      if (!cache || !cache.pageStr) continue;
      const lower = cache.pageStr.toLowerCase();
      let from = 0;
      while (true) {
        const idx = lower.indexOf(q, from);
        if (idx === -1) break;
        matches.push({ pageNum: p, charStart: idx, charEnd: idx + q.length });
        from = idx + q.length;
      }
    }
    return matches;
  }

  async function performSearch(query) {
    searchQuery = query.trim();
    if (!searchQuery) {
      searchMatches = [];
      currentMatchIdx = -1;
      setSearchStatus('');
      clearHighlights();
      updateSearchNavButtons();
      return;
    }
    if (!pdfDoc) return;
    if (!pageTextCache.size || pageTextCache.size < totalPages) {
      await indexAllPages();
    }
    searchMatches = findAllMatches(searchQuery);
    if (searchMatches.length === 0) {
      currentMatchIdx = -1;
      setSearchStatus('No matches');
      clearHighlights();
      updateSearchNavButtons();
      return;
    }
    /* Jump to first match's page */
    currentMatchIdx = 0;
    await jumpToMatch(0);
  }

  async function jumpToMatch(idx) {
    if (idx < 0 || idx >= searchMatches.length) return;
    currentMatchIdx = idx;
    const m = searchMatches[idx];
    setSearchStatus(`${idx + 1} of ${searchMatches.length}`);
    updateSearchNavButtons();
    if (currentPage !== m.pageNum) {
      await renderPage(m.pageNum);
      /* renderPage calls drawHighlights via the post-render hook below */
    } else {
      drawHighlights();
    }
  }

  function setSearchStatus(text) {
    const el = document.getElementById('fw-search-status');
    if (el) el.textContent = text;
  }

  function updateSearchNavButtons() {
    const prev = document.getElementById('fw-search-prev');
    const next = document.getElementById('fw-search-next');
    if (!prev || !next) return;
    const has = searchMatches.length > 0;
    prev.disabled = !has;
    next.disabled = !has;
  }

  function clearHighlights() {
    const layer = document.getElementById('fw-highlight-layer');
    if (layer) layer.innerHTML = '';
  }

  function drawHighlights() {
    const layer  = document.getElementById('fw-highlight-layer');
    const canvas = document.getElementById('fw-canvas');
    if (!layer || !canvas || !searchQuery) { clearHighlights(); return; }

    /* Match the highlight layer to canvas dimensions */
    layer.style.width  = canvas.style.width;
    layer.style.height = canvas.style.height;
    layer.innerHTML    = '';

    const cache = pageTextCache.get(currentPage);
    if (!cache) return;

    /* Get matches on the current page only */
    const pageMatchesGlobal = searchMatches
      .map((m, gi) => ({ ...m, gi }))
      .filter(m => m.pageNum === currentPage);
    if (pageMatchesGlobal.length === 0) return;

    /* For each match, find which text item(s) it overlaps and compute screen bbox */
    pdfDoc.getPage(currentPage).then(async page => {
      const baseViewport = page.getViewport({ scale: 1.0 });
      const containerWidth = document.getElementById('fw-viewer-body').clientWidth - 40;
      const fitScale = Math.min(containerWidth / baseViewport.width, 1.6);
      const viewport = page.getViewport({ scale: fitScale * zoomScale });

      pageMatchesGlobal.forEach(m => {
        for (const r of cache.itemRanges) {
          /* Check if this item intersects the match span */
          if (r.end <= m.charStart) continue;
          if (r.start >= m.charEnd) break;
          const item = r.item;
          if (!item.transform) continue;
          /* PDF.js transform: [scaleX, skewY, skewX, scaleY, x, y]
             where (x,y) is bottom-left of the text in PDF coords */
          const [a, b, c, d, e, f] = item.transform;
          const fontHeight = Math.hypot(c, d) || item.height || 12;
          const fontWidth  = Math.hypot(a, b) || 0;

          /* Compute the portion of the item that's matched */
          const overlapStart = Math.max(0, m.charStart - r.start);
          const overlapEnd   = Math.min(item.str.length, m.charEnd - r.start);
          if (overlapEnd <= overlapStart) continue;
          const fracStart = overlapStart / Math.max(1, item.str.length);
          const fracEnd   = overlapEnd   / Math.max(1, item.str.length);

          /* PDF coords → viewport coords */
          const pt1 = viewport.convertToViewportPoint(e + fracStart * (item.width || fontWidth), f);
          const pt2 = viewport.convertToViewportPoint(e + fracEnd   * (item.width || fontWidth), f);
          const left   = Math.min(pt1[0], pt2[0]);
          const right  = Math.max(pt1[0], pt2[0]);
          const top    = pt1[1] - fontHeight * fitScale * zoomScale;
          const width  = Math.max(2, right - left);
          const height = fontHeight * fitScale * zoomScale;

          const div = document.createElement('div');
          div.className = 'fw-highlight';
          if (m.gi === currentMatchIdx) div.classList.add('fw-highlight-current');
          div.style.left   = left   + 'px';
          div.style.top    = top    + 'px';
          div.style.width  = width  + 'px';
          div.style.height = height + 'px';
          layer.appendChild(div);
        }
      });
    });
  }

  /* ----- Open / close ---------------------------------------- */
  async function openPage(pageNum) {
    buildModalDOM();
    bindControlsOnce();
    const overlay = document.getElementById('fw-viewer-overlay');
    overlay.classList.add('fw-open');
    document.body.style.overflow = 'hidden';
    enableProtection();

    /* Reset to loading state */
    document.getElementById('fw-loading').style.display = 'block';
    document.getElementById('fw-loading').textContent = 'Loading framework library…';
    document.getElementById('fw-canvas-wrap').style.display = 'none';

    try {
      const pdfjsLib = await loadPdfJs();
      if (!pdfDoc) {
        const loadingTask = pdfjsLib.getDocument({
          url: PDF_PATH,
          /* Disable text/annotation extraction — we only render images */
          disableAutoFetch: false,
          disableStream: false
        });
        pdfDoc = await loadingTask.promise;
        totalPages = pdfDoc.numPages;
      }
      zoomScale = 1.0;
      await renderPage(pageNum || 1);
    } catch (err) {
      console.error('FW viewer open error:', err);
      document.getElementById('fw-loading').textContent =
        'Could not load the framework library. Check your connection and try again.';
    }
  }

  function close() {
    const overlay = document.getElementById('fw-viewer-overlay');
    if (overlay) overlay.classList.remove('fw-open');
    document.body.style.overflow = '';
    disableProtection();
    /* Reset search state so the next session starts clean */
    searchQuery = '';
    searchMatches = [];
    currentMatchIdx = -1;
    const si = document.getElementById('fw-search-input');
    if (si) si.value = '';
    setSearchStatus('');
    clearHighlights();
    updateSearchNavButtons();
  }

  function openSlug(slug) {
    const fw = SLUG_TO_FW[slug];
    if (fw) openPage(fw.page);
    else openPage(1);
  }

  function openUnit(unitNum) {
    const p = UNIT_PAGES[unitNum] || 1;
    openPage(p);
  }

  /* ----- Slibrary picker modal ------------------------------- */
  function buildPickerDOM() {
    if (document.getElementById('fw-picker-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'fw-picker-overlay';
    overlay.className = 'fw-picker-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'fw-picker-title');

    /* Group slibraries by unit */
    const byUnit = {};
    SLIBRARIES.forEach(s => {
      if (!byUnit[s.unit]) byUnit[s.unit] = [];
      byUnit[s.unit].push(s);
    });

    let unitsHTML = '';
    Object.keys(byUnit).sort().forEach(u => {
      const tilesHTML = byUnit[u].map(s => `
        <button type="button" class="fw-picker-tile"
                style="--tile-color:${s.color}"
                data-slibrary-page="${s.firstPage}"
                aria-label="Open ${s.title}">
          <span class="fw-picker-tile-num">Chapter ${String(s.num).padStart(2,'0')}</span>
          <span class="fw-picker-tile-title">${s.title}</span>
          <span class="fw-picker-tile-meta">${s.count} ${s.count===1?'sheet':'sheets'} · from p. ${s.firstPage}</span>
          <span class="fw-picker-tile-arrow">→</span>
        </button>`).join('');
      unitsHTML += `
        <section class="fw-picker-unit">
          <div class="fw-picker-unit-title"><strong>${['','Part I · Proposal','Part II · Business Plan','Part III · Defense'][u]}</strong>${UNIT_TITLES[u] ? ' · '+UNIT_TITLES[u] : ''}</div>
          <div class="fw-picker-grid">${tilesHTML}</div>
        </section>`;
    });

    overlay.innerHTML = `
      <div class="fw-picker-modal">
        <header class="fw-picker-header">
          <div>
            <h2 id="fw-picker-title">Framework Reference Library</h2>
            <span class="sub">63 Frameworks · 63 Reference Sheets · select a chapter to open</span>
          </div>
          <button type="button" class="fw-picker-close" id="fw-picker-close-btn"
                  aria-label="Close (Esc)" title="Close (Esc)">×</button>
        </header>
        <div class="fw-picker-body">${unitsHTML}</div>
        <footer class="fw-picker-footer">
          <strong>The Business Plan Navigator · Framework Reference Library</strong> · © 2026 Prof. Dr. Hildegard Haas · EU Business School
        </footer>
      </div>
    `;
    document.body.appendChild(overlay);

    /* Wire up tile clicks */
    overlay.querySelectorAll('.fw-picker-tile').forEach(btn => {
      btn.addEventListener('click', () => {
        const page = parseInt(btn.getAttribute('data-slibrary-page'), 10);
        closePicker();
        openPage(page);
      });
    });

    /* Close button */
    document.getElementById('fw-picker-close-btn').addEventListener('click', closePicker);

    /* Click outside modal closes */
    overlay.addEventListener('click', e => {
      if (e.target.id === 'fw-picker-overlay') closePicker();
    });
  }

  function openSlibraryPicker() {
    buildPickerDOM();
    const overlay = document.getElementById('fw-picker-overlay');
    overlay.classList.add('fw-open');
    document.body.style.overflow = 'hidden';
    /* Esc to close */
    document.addEventListener('keydown', onPickerKeydown, true);
  }

  function closePicker() {
    const overlay = document.getElementById('fw-picker-overlay');
    if (overlay) overlay.classList.remove('fw-open');
    /* Only restore body overflow if PDF viewer isn't open */
    const pdfOpen = document.getElementById('fw-viewer-overlay')?.classList.contains('fw-open');
    if (!pdfOpen) document.body.style.overflow = '';
    document.removeEventListener('keydown', onPickerKeydown, true);
  }

  function onPickerKeydown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      closePicker();
    }
  }

  /* ----- Controls -------------------------------------------- */
  let controlsBound = false;
  function bindControlsOnce() {
    if (controlsBound) return;
    controlsBound = true;

    document.getElementById('fw-btn-close').addEventListener('click', close);
    document.getElementById('fw-viewer-overlay').addEventListener('click', e => {
      if (e.target.id === 'fw-viewer-overlay') close();
    });
    document.getElementById('fw-btn-prev').addEventListener('click', () => {
      if (currentPage > 1) renderPage(currentPage - 1);
    });
    document.getElementById('fw-btn-next').addEventListener('click', () => {
      if (currentPage < totalPages) renderPage(currentPage + 1);
    });
    document.getElementById('fw-btn-zoom-in').addEventListener('click', () => {
      zoomScale = Math.min(ZOOM_MAX, zoomScale + ZOOM_STEP);
      renderPage(currentPage);
    });
    document.getElementById('fw-btn-zoom-out').addEventListener('click', () => {
      zoomScale = Math.max(ZOOM_MIN, zoomScale - ZOOM_STEP);
      renderPage(currentPage);
    });

    /* ---- Search controls ---- */
    const searchInput = document.getElementById('fw-search-input');
    const searchPrev  = document.getElementById('fw-search-prev');
    const searchNext  = document.getElementById('fw-search-next');
    const searchClear = document.getElementById('fw-search-clear');
    let searchDebounce = null;

    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => performSearch(searchInput.value), 220);
      });
      searchInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          e.preventDefault();
          if (searchMatches.length === 0) return;
          if (e.shiftKey) {
            const next = (currentMatchIdx - 1 + searchMatches.length) % searchMatches.length;
            jumpToMatch(next);
          } else {
            const next = (currentMatchIdx + 1) % searchMatches.length;
            jumpToMatch(next);
          }
        } else if (e.key === 'Escape') {
          if (searchInput.value) {
            e.stopPropagation();
            searchInput.value = '';
            performSearch('');
          }
        }
      });
    }
    if (searchPrev) {
      searchPrev.addEventListener('click', () => {
        if (searchMatches.length === 0) return;
        const next = (currentMatchIdx - 1 + searchMatches.length) % searchMatches.length;
        jumpToMatch(next);
      });
    }
    if (searchNext) {
      searchNext.addEventListener('click', () => {
        if (searchMatches.length === 0) return;
        const next = (currentMatchIdx + 1) % searchMatches.length;
        jumpToMatch(next);
      });
    }
    if (searchClear) {
      searchClear.addEventListener('click', () => {
        if (searchInput) {
          searchInput.value = '';
          searchInput.focus();
        }
        performSearch('');
      });
    }
  }

  /* ----- Protection layer ------------------------------------ */
  /* These handlers are attached only while the modal is open
     so they don't interfere with the rest of the site. */
  function onContextMenu(e) {
    if (e.target.closest('#fw-viewer-overlay')) {
      e.preventDefault();
      return false;
    }
  }
  function onSelectStart(e) {
    if (e.target && e.target.id === 'fw-search-input') return; /* allow in search */
    if (e.target.closest('#fw-viewer-overlay')) {
      e.preventDefault();
      return false;
    }
  }
  function onCopy(e) {
    if (e.target && e.target.id === 'fw-search-input') return; /* allow in search */
    if (document.getElementById('fw-viewer-overlay')?.classList.contains('fw-open')) {
      e.preventDefault();
      e.clipboardData?.setData('text/plain', '');
    }
  }
  function onKeyDown(e) {
    const overlay = document.getElementById('fw-viewer-overlay');
    if (!overlay || !overlay.classList.contains('fw-open')) return;

    /* Allow normal keyboard interaction inside the search input */
    const inSearch = e.target && e.target.id === 'fw-search-input';

    /* Esc closes (unless search is active and clearing it) */
    if (e.key === 'Escape' && !inSearch) { close(); return; }

    /* Arrow keys navigate (skip when typing in search) */
    if (!inSearch && e.key === 'ArrowLeft' && currentPage > 1) {
      e.preventDefault();
      renderPage(currentPage - 1);
      return;
    }
    if (!inSearch && e.key === 'ArrowRight' && currentPage < totalPages) {
      e.preventDefault();
      renderPage(currentPage + 1);
      return;
    }

    /* Inside search input: allow normal typing & basic keys */
    if (inSearch) return;

    /* Block save / print / find / view-source / dev-tools shortcuts */
    const ck = e.ctrlKey || e.metaKey;
    if (ck && ['s','p','c','x','a','f','u','j'].includes(e.key.toLowerCase())) {
      /* Cmd+F → focus our search input instead of native find */
      if (e.key.toLowerCase() === 'f') {
        e.preventDefault();
        e.stopPropagation();
        const si = document.getElementById('fw-search-input');
        if (si) { si.focus(); si.select(); }
        return false;
      }
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
    if (e.key === 'F12' || (ck && e.shiftKey && ['i','c','j'].includes(e.key.toLowerCase()))) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
  }
  function onDragStart(e) {
    if (e.target.closest('#fw-viewer-overlay')) {
      e.preventDefault();
      return false;
    }
  }
  function onBeforePrint() {
    document.body.classList.add('fw-printing-blocked');
    const overlay = document.getElementById('fw-viewer-overlay');
    if (overlay) overlay.style.display = 'none';
  }
  function onAfterPrint() {
    document.body.classList.remove('fw-printing-blocked');
    const overlay = document.getElementById('fw-viewer-overlay');
    if (overlay && overlay.classList.contains('fw-open')) overlay.style.display = '';
  }

  function enableProtection() {
    document.addEventListener('contextmenu', onContextMenu, true);
    document.addEventListener('selectstart',  onSelectStart, true);
    document.addEventListener('copy',         onCopy,        true);
    document.addEventListener('keydown',      onKeyDown,     true);
    document.addEventListener('dragstart',    onDragStart,   true);
    window.addEventListener('beforeprint',    onBeforePrint);
    window.addEventListener('afterprint',     onAfterPrint);
  }
  function disableProtection() {
    document.removeEventListener('contextmenu', onContextMenu, true);
    document.removeEventListener('selectstart',  onSelectStart, true);
    document.removeEventListener('copy',         onCopy,        true);
    document.removeEventListener('keydown',      onKeyDown,     true);
    document.removeEventListener('dragstart',    onDragStart,   true);
    window.removeEventListener('beforeprint',    onBeforePrint);
    window.removeEventListener('afterprint',     onAfterPrint);
  }

  /* ----- Auto-wire any element with [data-fw-slug] / [data-fw-page] / .fw-viewer-pill --- */
  function attachClickHandlers() {
    /* Pill buttons */
    document.querySelectorAll('.fw-viewer-pill').forEach(el => {
      if (el.dataset.fwBound) return;
      el.dataset.fwBound = '1';
      el.addEventListener('click', e => {
        e.preventDefault();
        const slug = el.getAttribute('data-fw-slug');
        const page = el.getAttribute('data-fw-page');
        const unit = el.getAttribute('data-fw-unit');
        if (slug)      openSlug(slug);
        else if (page) openPage(parseInt(page, 10));
        else if (unit) openUnit(parseInt(unit, 10));
        else           openPage(1);
      });
    });

    /* Framework thumbnails marked with data-fw-slug */
    document.querySelectorAll('[data-fw-slug]').forEach(el => {
      if (el.classList.contains('fw-viewer-pill')) return; /* already handled above */
      if (el.dataset.fwBound) return;
      el.dataset.fwBound = '1';
      el.classList.add('fw-clickable');
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      const handler = e => {
        e.preventDefault();
        openSlug(el.getAttribute('data-fw-slug'));
      };
      el.addEventListener('click', handler);
      el.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handler(e); }
      });
    });

    /* Anchored thumbnails by direct page */
    document.querySelectorAll('[data-fw-page]').forEach(el => {
      if (el.classList.contains('fw-viewer-pill')) return;
      if (el.dataset.fwBound) return;
      el.dataset.fwBound = '1';
      el.classList.add('fw-clickable');
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      const p = parseInt(el.getAttribute('data-fw-page'), 10);
      const handler = e => { e.preventDefault(); openPage(p); };
      el.addEventListener('click', handler);
      el.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handler(e); }
      });
    });
  }

  /* ----- Public API ------------------------------------------ */
  /* Namespace: window.FrameworkSheets (NOT window.FW — that name is
     already used by the existing per-unit framework data array). */
  window.FrameworkSheets = {
    openPage,
    openSlug,
    openUnit,
    openSlibraryPicker,
    close,
    closePicker,
    list: () => FRAMEWORKS.slice(),
    slibraries: () => SLIBRARIES.slice(),
    get: slug => SLUG_TO_FW[slug] || null
  };

  /* ----- Init on DOM ready ----------------------------------- */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachClickHandlers);
  } else {
    attachClickHandlers();
  }
  /* Re-scan when content is added dynamically (best effort) */
  if (window.MutationObserver) {
    const mo = new MutationObserver(() => attachClickHandlers());
    mo.observe(document.documentElement, { childList: true, subtree: true });
  }
})();
