/*
  DigiLab - Adsterra loader.
  Ads load AFTER the page is ready (page load or first scroll/touch), and banners only
  load when they come near the screen. This keeps the site fast (good PageSpeed score).
  Your ad codes are stored in the CFG block below.
*/
(function () {
  "use strict";
  var CFG = {
    banner: {
      key: "c15b716148d184fd66a15d94a502edc7", width: 320, height: 50,
      src: "https://www.highrevenueformat.com/c15b716148d184fd66a15d94a502edc7/invoke.js"
    },
    native: {
      src: "https://pl31534811.profitableratecpmnetwork.com/ee2cdecf3c964b907fd537f1f4bb4642/invoke.js"
    },
    social: "https://pl31534812.profitableratecpmnetwork.com/95/18/6c/95186cff315ddff9b3bd3e431d9ee60a.js"
  };

  var started = false;

  function addScript(src, parent, attrs, done) {
    var s = document.createElement("script");
    s.src = src; s.async = true;
    if (attrs) for (var k in attrs) s.setAttribute(k, attrs[k]);
    if (done) { s.onload = done; s.onerror = done; }
    (parent || document.body).appendChild(s);
    return s;
  }

  // banners must load one at a time (the code reads a shared "atOptions" setting)
  var queue = [], busy = false;
  function nextBanner() {
    if (busy || !queue.length) return;
    busy = true;
    var slot = queue.shift();
    window.atOptions = { key: CFG.banner.key, format: "iframe", height: CFG.banner.height, width: CFG.banner.width, params: {} };
    addScript(CFG.banner.src, slot, null, function () { busy = false; setTimeout(nextBanner, 200); });
  }

  // if an ad never shows (ad blocker, no fill), hide its empty space after a few seconds
  function collapseIfEmpty(box, probe) {
    setTimeout(function () {
      if (!probe()) box.style.display = "none";
    }, 6000);
  }

  function watch(el, fn) {
    if (!("IntersectionObserver" in window)) { fn(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); fn(); } });
    }, { rootMargin: "400px 0px" });
    io.observe(el);
  }

  function start() {
    if (started) return; started = true;
    // 1) Social bar (one per page)
    addScript(CFG.social, document.body);
    // 2) Native banner (one container per page)
    var nat = document.getElementById("container-ee2cdecf3c964b907fd537f1f4bb4642");
    if (nat) watch(nat, function () {
      addScript(CFG.native.src, nat.parentNode, { "data-cfasync": "false" });
      collapseIfEmpty(nat.parentNode, function () { return nat.children.length > 0; });
    });
    // 3) Banner slots (320x50)
    Array.prototype.forEach.call(document.querySelectorAll('[data-ad="banner"]'), function (slot) {
      watch(slot, function () {
        queue.push(slot); nextBanner();
        collapseIfEmpty(slot, function () { return !!slot.querySelector("iframe"); });
      });
    });
  }

  function arm() {
    var go = function () { start(); };
    ["scroll", "pointerdown", "keydown", "touchstart"].forEach(function (ev) {
      window.addEventListener(ev, go, { once: true, passive: true });
    });
    setTimeout(go, 2500); // also start by itself after 2.5 s
  }
  if (document.readyState === "complete") arm();
  else window.addEventListener("load", arm);
})();
