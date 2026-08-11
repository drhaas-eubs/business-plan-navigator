/* ═══════════════════════════════════════════════════════════
   EUBS Capstone Navigator — content protection layer
   Deterrent against casual copying. See README for limitations.
   © 2026 Prof. Dr. Hildegard Haas · EU Business School Munich
   ═══════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var MSG = "This material is protected. Please cite it rather than copy it \u2014 " +
            "the full Harvard reference is given beside every framework.";

  /* ── toast ─────────────────────────────────────────────── */
  var toast, timer;
  function notify(text) {
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "cp-toast";
      document.body.appendChild(toast);
    }
    toast.textContent = text || MSG;
    toast.classList.add("on");
    clearTimeout(timer);
    timer = setTimeout(function () { toast.classList.remove("on"); }, 3200);
  }

  /* ── allow interaction inside real form fields ─────────── */
  function isField(el) {
    if (!el || !el.tagName) return false;
    var t = el.tagName.toUpperCase();
    return t === "INPUT" || t === "TEXTAREA" || el.isContentEditable;
  }

  /* ── block selection ───────────────────────────────────── */
  document.addEventListener("selectstart", function (e) {
    if (!isField(e.target)) e.preventDefault();
  });
  document.addEventListener("mousedown", function (e) {
    if (e.detail > 1 && !isField(e.target)) e.preventDefault();
  });

  /* ── block copy, cut and drag ──────────────────────────── */
  ["copy", "cut"].forEach(function (ev) {
    document.addEventListener(ev, function (e) {
      if (isField(e.target)) return;
      e.preventDefault();
      if (e.clipboardData) e.clipboardData.setData("text/plain", "");
      notify();
    });
  });
  document.addEventListener("dragstart", function (e) { e.preventDefault(); });

  /* ── block context menu ────────────────────────────────── */
  document.addEventListener("contextmenu", function (e) {
    if (isField(e.target)) return;
    e.preventDefault();
    notify();
  });

  /* ── block keyboard shortcuts ──────────────────────────── */
  document.addEventListener("keydown", function (e) {
    var k = (e.key || "").toLowerCase();
    var meta = e.ctrlKey || e.metaKey;

    if (isField(e.target) && meta && (k === "c" || k === "x" || k === "v" || k === "a")) return;

    /* copy · cut · select all · save · view source · print */
    if (meta && !e.shiftKey && ["c", "x", "a", "s", "u", "p"].indexOf(k) > -1) {
      e.preventDefault(); notify(); return;
    }
    /* developer tools */
    if (k === "f12" || (meta && e.shiftKey && ["i", "j", "c"].indexOf(k) > -1)) {
      e.preventDefault(); notify("Developer tools are disabled on this site."); return;
    }
  });

  /* ── discourage print-to-PDF ───────────────────────────── */
  if (window.matchMedia) {
    var mq = window.matchMedia("print");
    if (mq.addEventListener) {
      mq.addEventListener("change", function (m) { if (m.matches) notify(); });
    }
  }
  window.addEventListener("beforeprint", function () { notify(); });

  /* ── strip any programmatic selection that slips through ─ */
  setInterval(function () {
    var s = window.getSelection && window.getSelection();
    if (s && s.rangeCount && String(s).length > 0 && !isField(document.activeElement)) {
      s.removeAllRanges();
    }
  }, 700);
})();
