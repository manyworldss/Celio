// Celio marketing site: moving ASCII, the sideways tour, and parallax.
// No dependencies. Everything animated here has a static fallback, and
// nothing moves when the visitor has Reduce Motion switched on.
(function () {
  "use strict";

  var reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  // The stream every ASCII texture is made from: yes / no / unsure in the
  // five launch languages.
  var STREAM = "yes · no · unsure · sí · no · no lo sé · sim · não · não sei · oui · non · je ne sais pas · ja · nein · weiß nicht · ";
  var SL = STREAM.length;
  function streamChar(i) { return STREAM[((i % SL) + SL) % SL]; }

  // ---------- ASCII generators (all take a phase, so they can move) ----------

  // A plate: a ramp-shaded rim, with the answers travelling across the inside
  // in alternating directions.
  function plate(phase) {
    var W = 120, H = 62, ramp = " .:-=+*#%@", out = [];
    for (var y = 0; y < H; y++) {
      var row = "", dir = (y % 4 === 0) ? 1 : -1;
      for (var x = 0; x < W; x++) {
        var dx = (x - W / 2) / (W / 2), dy = (y - H / 2) / (H / 2);
        var r = Math.sqrt(dx * dx + dy * dy);
        if (r < 0.6) {
          row += (y % 2 === 0) ? streamChar(x + y * 11 + dir * phase) : " ";
          continue;
        }
        var v = 0;
        v += Math.max(0, 1 - Math.abs(r - 0.92) / 0.05);
        v += 0.75 * Math.max(0, 1 - Math.abs(r - 0.66) / 0.025);
        if (r > 0.96 && r < 1.1) v += 0.25 * (1 - (r - 0.96) / 0.14) * (((x * 7 + y * 13) % 5) / 4);
        v = clamp(v, 0, 0.999);
        row += ramp[Math.floor(v * ramp.length)];
      }
      out.push(row);
    }
    return out.join("\n");
  }

  // Broken signal rings that turn with the phase.
  function rings(phase) {
    var W = 90, H = 46, out = [], turn = phase * 0.02;
    for (var y = 0; y < H; y++) {
      var row = "";
      for (var x = 0; x < W; x++) {
        var dx = (x - W / 2) / 45, dy = (y - H / 2) / 23;
        var r = Math.sqrt(dx * dx + dy * dy), a = Math.atan2(dy, dx);
        var ch = " ";
        for (var k = 1; k <= 5; k++) {
          if (Math.abs(r - k * 0.19) < 0.022) {
            var spin = (k % 2 ? turn : -turn) / k;
            var gap = Math.sin((a + spin) * (3 + k) + k) > 0.55 - k * 0.12;
            ch = gap ? " " : (k < 3 ? "o" : k < 5 ? "." : "·");
          }
        }
        if (r < 0.06) ch = "@";
        row += ch;
      }
      out.push(row);
    }
    return out.join("\n");
  }

  // Rows of answers passing each other: the backdrop of the tour.
  function flow(phase) {
    var out = [];
    for (var y = 0; y < 15; y++) {
      var row = "", dir = y % 2 ? 1 : -1;
      for (var x = 0; x < 330; x++) row += streamChar(x + y * 23 + dir * phase);
      out.push(row);
    }
    return out.join("\n");
  }

  var GEN = { plate: plate, rings: rings, flow: flow };
  var asciiEls = $$("[data-ascii]").map(function (el) {
    return { el: el, gen: GEN[el.getAttribute("data-ascii")], phase: null };
  });

  function paintAscii(phase, force) {
    var vh = window.innerHeight;
    for (var i = 0; i < asciiEls.length; i++) {
      var a = asciiEls[i];
      if (!a.gen || a.phase === phase) continue;
      if (!force) {
        var r = a.el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) continue;
      }
      a.phase = phase;
      a.el.textContent = a.gen(phase);
    }
  }
  paintAscii(0, true);

  // ---------- Exchange: one text turning into another ----------

  var NOISE = "abcdefghijklmnopqrstuvwxyz¿?·";
  // p: 0 shows `a`, 1 shows `b`; in between, a wave of noise sweeps left to right.
  function mix(a, b, p, tick) {
    if (p <= 0) return a;
    if (p >= 1) return b;
    var len = Math.max(a.length, b.length), out = "";
    for (var i = 0; i < len; i++) {
      var start = (i / len) * 0.6;
      if (p < start) out += a[i] || " ";
      else if (p >= start + 0.4) out += b[i] || " ";
      else out += (a[i] === " " && b[i] === " ") ? " " : NOISE[(i * 7 + tick) % NOISE.length];
    }
    return out;
  }

  function swapText(el, to, ms) {
    if (!el) return;
    var from = el.textContent, t0 = null;
    if (reduce || from === to) { el.textContent = to; return; }
    function step(t) {
      if (t0 === null) t0 = t;
      var p = clamp((t - t0) / ms, 0, 1);
      el.textContent = mix(from, to, p, Math.floor(t / 40)).replace(/\s+$/, "");
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // Hero: the card's greeting and language change places every few seconds.
  var LANGS = [
    { flag: "en", code: "EN", name: "English", greet: "Enjoy your meal." },
    { flag: "es", code: "ES", name: "Español", greet: "Buen provecho." },
    { flag: "fr", code: "FR", name: "Français", greet: "Bon appétit." },
    { flag: "pt", code: "PT", name: "Português", greet: "Bom apetite." },
    { flag: "de", code: "DE", name: "Deutsch", greet: "Guten Appetit." }
  ];
  if (!reduce && $("[data-greet]")) {
    var li = 0;
    setInterval(function () {
      if (document.hidden) return;
      li = (li + 1) % LANGS.length;
      var l = LANGS[li];
      swapText($("[data-greet]"), l.greet, 700);
      swapText($("[data-lang]"), l.name, 500);
      swapText($("[data-code]"), l.code, 300);
      swapText($("[data-flag]"), l.flag, 300);
    }, 3200);
  }

  // Tour: the question travels to the kitchen in Spanish, the answer comes back.
  var QA = [
    { en: "contains wheat, barley, rye or oats?", es: "¿contiene trigo, cebada, centeno o avena?", ans: "[ no ]  -> no" },
    { en: "clean utensils and surface?", es: "¿utensilios y superficie limpios?", ans: "[ sí ]  -> yes" },
    { en: "shared fryer?", es: "¿freidora compartida?", ans: "[ no lo sé ]  -> unsure, ask the chef" }
  ];
  var receiptEl = $("[data-receipt]"), receiptP = -1;
  function paintReceipt(p) {
    if (!receiptEl) return;
    p = Math.round(clamp(p, 0, 1) * 200) / 200;
    if (p === receiptP) return;
    receiptP = p;
    var lines = [], tick = Math.floor(p * 90);
    for (var k = 0; k < QA.length; k++) {
      var sub = clamp((p - k * 0.24) / 0.36, 0, 1);
      lines.push("> " + mix(QA[k].en, QA[k].es, sub, tick + k * 5));
      lines.push(sub >= 1 ? "  " + QA[k].ans : "");
      lines.push("");
    }
    lines.push(p >= 0.97 ? "confirmed: 2   unknown: 1" : "");
    receiptEl.textContent = lines.join("\n");
  }
  paintReceipt(reduce ? 1 : 0);

  // ---------- Ticker ----------

  var ticker = $("[data-ticker]"), tickWidth = 0;
  if (ticker) {
    var unit = document.createElement("span");
    unit.textContent = STREAM;
    ticker.appendChild(unit);
    for (var i = 0; i < 7; i++) ticker.appendChild(unit.cloneNode(true));
    tickWidth = unit.getBoundingClientRect().width;
  }

  // ---------- Footer: the wordmark, written in answers ----------

  var DENSE = STREAM.replace(/ /g, ""), DL = DENSE.length; // no gaps, so the letterforms hold
  var markEl = $("[data-mark]"), mask = null, MC = 104, MR = 24;
  function buildMask() {
    var S = 6, c = document.createElement("canvas");
    c.width = MC * S; c.height = MR * S;
    var ctx = c.getContext("2d");
    if (!ctx) return;
    var size = MR * S * 0.98, stretch = 1 / 0.6; // a mono cell is ~0.6 as wide as it is tall
    ctx.font = "600 " + size + "px Poppins, Inter, sans-serif";
    ctx.textBaseline = "alphabetic";
    var w = ctx.measureText("Celio").width * stretch;
    ctx.setTransform(stretch, 0, 0, 1, (c.width - w) / 2, 0);
    ctx.fillText("Celio", 0, MR * S * 0.84);
    var data = ctx.getImageData(0, 0, c.width, c.height).data;
    mask = [];
    for (var y = 0; y < MR; y++) {
      var row = [];
      for (var x = 0; x < MC; x++) row.push(data[((y * S + 3) * c.width + x * S + 3) * 4 + 3] > 110);
      mask.push(row);
    }
  }
  function paintMark(t) {
    if (!markEl || !mask) return;
    var out = [];
    for (var y = 0; y < MR; y++) {
      var row = "", dir = y % 2 ? 1 : -1;
      for (var x = 0; x < MC; x++) row += mask[y][x] ? DENSE[(((x + y * 13 + dir * t) % DL) + DL) % DL] : " ";
      out.push(row);
    }
    markEl.textContent = out.join("\n");
  }
  function startMark() {
    buildMask();
    paintMark(0);
    if (reduce || !markEl || !("IntersectionObserver" in window)) return;
    var t = 0, timer = null;
    new IntersectionObserver(function (entries) {
      var on = entries[0].isIntersecting;
      if (on && !timer) timer = setInterval(function () { paintMark(++t); }, 260);
      if (!on && timer) { clearInterval(timer); timer = null; }
    }).observe(markEl);
  }

  // ---------- Tour: vertical scroll becomes sideways travel ----------

  var tour = $("#exchange"), track = $("[data-track]"), flowLayer = $("[data-flow-layer]");
  var panels = $$("[data-panel]"), navBtns = $$("[data-tour-nav] button");
  var pinned = false, maxShift = 0, travel = 0, centers = [], drifts = [];
  var SPEED = 2.4; // sideways pixels per pixel scrolled: keeps the section short

  function setActive(idx) {
    for (var i = 0; i < navBtns.length; i++) {
      if (i === idx) navBtns[i].setAttribute("aria-current", "true");
      else navBtns[i].removeAttribute("aria-current");
    }
    // Keep the active step visible when the step menu itself has to scroll.
    var b = navBtns[idx], nav = b && b.parentElement;
    if (nav && nav.scrollWidth > nav.clientWidth) {
      nav.scrollLeft = b.offsetLeft - (nav.clientWidth - b.offsetWidth) / 2;
    }
  }

  function layoutTour() {
    if (!tour || !track) return;
    // Pinning is for mouse and trackpad. Touch screens get the swipe carousel,
    // where sideways movement follows the thumb directly.
    var fine = !window.matchMedia || window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    var want = !reduce && fine && window.innerWidth >= 900 && window.innerHeight >= 560;
    pinned = want;
    tour.classList.toggle("is-pinned", pinned);
    if (!pinned) {
      tour.style.height = "";
      track.style.transform = "";
      if (flowLayer) flowLayer.style.transform = "";
      drifts.forEach(function (d) { d.el.style.transform = ""; });
      return;
    }
    tour.style.setProperty("--ps", clamp((window.innerHeight - 190) / 600, 0.6, 1).toFixed(3));
    maxShift = Math.max(0, track.offsetWidth - window.innerWidth);
    travel = maxShift / SPEED;
    tour.style.height = Math.round(window.innerHeight + travel) + "px";
    centers = panels.map(function (p) { return p.offsetLeft + p.offsetWidth / 2; });
    drifts = [];
    panels.forEach(function (p, i) {
      var el = $("[data-drift]", p);
      if (el) drifts.push({ el: el, i: i });
    });
  }

  function nearest(shift) {
    var mid = shift + window.innerWidth / 2, best = 0, bd = Infinity;
    for (var i = 0; i < centers.length; i++) {
      var d = Math.abs(centers[i] - mid);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }

  function updateTour() {
    if (!pinned) return;
    var top = tour.getBoundingClientRect().top;
    if (top > window.innerHeight || top < -(travel + window.innerHeight)) return;
    var shift = clamp(-top / travel, 0, 1) * maxShift, vw = window.innerWidth;
    track.style.transform = "translate3d(" + (-shift).toFixed(1) + "px,0,0)";
    if (flowLayer) flowLayer.style.transform = "translate3d(" + (-shift * 0.3).toFixed(1) + "px,0,0)";
    for (var i = 0; i < drifts.length; i++) {
      var off = centers[drifts[i].i] - shift - vw / 2;
      drifts[i].el.style.transform = "translate3d(" + (off * 0.12).toFixed(1) + "px,0,0)";
    }
    // The receipt translates itself as its panel travels to the middle.
    var rOff = centers[3] - shift - vw / 2;
    paintReceipt(1 - rOff / (vw * 0.55));
    setActive(nearest(shift));
  }

  navBtns.forEach(function (btn, i) {
    btn.addEventListener("click", function () {
      if (pinned) {
        var shift = clamp(centers[i] - window.innerWidth / 2, 0, maxShift);
        var y = tour.getBoundingClientRect().top + window.scrollY + shift / SPEED;
        window.scrollTo({ top: y, behavior: reduce ? "auto" : "smooth" });
      } else if (panels[i]) {
        panels[i].scrollIntoView({ behavior: reduce ? "auto" : "smooth", inline: "center", block: "nearest" });
      }
    });
  });

  // Swipe mode (phones, Reduce Motion): track which panel is centred, and let
  // the receipt play once when it comes into view.
  if (track) {
    track.addEventListener("scroll", function () {
      if (pinned) return;
      var mid = track.scrollLeft + track.clientWidth / 2, best = 0, bd = Infinity;
      panels.forEach(function (p, i) {
        var d = Math.abs(p.offsetLeft + p.offsetWidth / 2 - mid);
        if (d < bd) { bd = d; best = i; }
      });
      setActive(best);
      if (flowLayer && !reduce) flowLayer.style.transform = "translate3d(" + (-track.scrollLeft * 0.3).toFixed(1) + "px,0,0)";
    }, { passive: true });
  }
  if (receiptEl && !reduce && "IntersectionObserver" in window) {
    var played = false;
    new IntersectionObserver(function (entries) {
      if (pinned || played || !entries[0].isIntersecting) return;
      played = true;
      var t0 = null;
      requestAnimationFrame(function step(t) {
        if (t0 === null) t0 = t;
        var p = (t - t0) / 3200;
        paintReceipt(p);
        if (p < 1 && !pinned) requestAnimationFrame(step);
      });
    }, { threshold: 0.6 }).observe(receiptEl);
  }
  setActive(0);

  // ---------- Scroll loop ----------

  var layers = $$("[data-speed]").map(function (el) {
    return {
      el: el,
      root: el.closest("[data-px-root]") || el.parentElement,
      speed: parseFloat(el.getAttribute("data-speed")) || 0,
      top: el.getAttribute("data-anchor") === "top"
    };
  });

  var queued = false;
  function update() {
    queued = false;
    var vh = window.innerHeight, y = window.scrollY;
    for (var i = 0; i < layers.length; i++) {
      var l = layers[i], r = l.root.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) continue;
      var d = l.top ? -r.top : vh / 2 - (r.top + r.height / 2);
      l.el.style.transform = "translate3d(0," + (d * l.speed).toFixed(1) + "px,0)";
    }
    if (ticker && tickWidth) {
      ticker.style.transform = "translate3d(" + (-((y * 0.45) % tickWidth) - 200).toFixed(1) + "px,0,0)";
    }
    paintAscii(Math.floor(y / 16), false);
    updateTour();
  }
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(update);
  }
  function onResize() { layoutTour(); onScroll(); }

  layoutTour();
  window.addEventListener("resize", onResize, { passive: true });

  var ready = (document.fonts && document.fonts.ready) || Promise.resolve();
  ready.then(function () {
    if (ticker) tickWidth = ticker.firstChild.getBoundingClientRect().width;
    startMark();
    layoutTour();
    if (!reduce) update();
  });

  if (reduce) return; // static page: no scroll-driven motion at all
  window.addEventListener("scroll", onScroll, { passive: true });
  update();
})();
