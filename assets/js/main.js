/* DigiLab - tiny vanilla JS (no libraries). */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // mobile menu
  var burger = $(".burger"), nav = $(".nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // footer year
  $$(".yr").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  // careers filter + search
  var list = $("#jobs"), search = $("#q"), chips = $$(".chip");
  if (list) {
    var cards = $$(".job-card", list), empty = $("#empty"), dept = "all";
    var count = $("#count");
    var apply = function () {
      var q = (search.value || "").trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (dept === "all" || c.dataset.dept === dept) &&
                 (!q || c.dataset.text.indexOf(q) > -1);
        c.style.display = ok ? "" : "none";
        if (ok) shown++;
      });
      if (empty) empty.style.display = shown ? "none" : "block";
      if (count) count.textContent = shown;
    };
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        chips.forEach(function (x) { x.classList.remove("on"); });
        ch.classList.add("on"); dept = ch.dataset.dept; apply();
      });
    });
    if (search) search.addEventListener("input", apply);
    apply();
  }

  // preselect role on apply page (?role=slug)
  var roleSel = $("#role");
  if (roleSel) {
    var m = /[?&]role=([^&]+)/.exec(location.search);
    if (m) { try { roleSel.value = decodeURIComponent(m[1]); } catch (e) {} }
  }

  // ---------------------------------------------------------------- forms
  // Google Sheet (Apps Script web app). "no-cors" means the browser cannot read the reply,
  // but the row is still saved. Resolves true unless the network itself failed.
  function sendSheet(cfg, fd) {
    var body = new URLSearchParams();
    fd.forEach(function (v, k) { if (typeof v === "string") body.append(k, v); });
    return fetch(cfg.sheetUrl, { method: "POST", mode: "no-cors", body: body })
      .then(function () { return true; }, function () { return false; });
  }

  // Email through Web3Forms / Formspree. Resolves true only if the service says "success".
  function sendMail(cfg, fd, form) {
    var d = new FormData();
    fd.forEach(function (v, k) { d.append(k, v); });
    if (cfg.accessKey) {
      d.append("access_key", cfg.accessKey);
      d.append("subject", form.dataset.subject || "New DigiLab submission");
      d.append("from_name", "DigiLab Website");
    }
    return fetch(cfg.formEndpoint, { method: "POST", body: d, headers: { Accept: "application/json" } })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) { return r.ok && j.success !== false; });
      })
      .catch(function () { return false; });
  }

  $$("form[data-form]").forEach(function (form) {
    var box = $(".msg", form);
    var show = function (cls, text) {
      box.className = "msg " + cls; box.textContent = text;
      box.scrollIntoView({ block: "nearest", behavior: "smooth" });
    };
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var cfg = window.DIGILAB || {};
      var fd = new FormData(form);
      if (fd.get("website")) return; // honeypot (bots fill it)
      fd.delete("website");
      // send the readable role name (not the url slug) to email and sheet
      var rs = $("#role", form);
      if (rs && rs.selectedIndex > -1) fd.set("role", rs.options[rs.selectedIndex].text);

      var hasMail = !!(cfg.accessKey || (cfg.formEndpoint && cfg.formEndpoint.indexOf("web3forms") === -1));
      var hasSheet = !!cfg.sheetUrl;
      var btn = $("button[type=submit]", form);

      if (hasMail || hasSheet) {
        var old = btn.textContent;
        btn.disabled = true; btn.textContent = "Sending...";
        var jobs = [];
        if (hasSheet) jobs.push(sendSheet(cfg, fd));
        if (hasMail) jobs.push(sendMail(cfg, fd, form));
        Promise.all(jobs).then(function (res) {
          if (res.some(Boolean)) {
            form.reset();
            show("ok", form.dataset.ok || "Thank you! We received your message and will reply by email soon.");
          } else {
            show("err", "Sorry, something went wrong. Please try again in a moment.");
          }
          btn.disabled = false; btn.textContent = old;
        });
        return;
      }
      if (cfg.email) { // last fallback: open visitor's email app
        var body = [];
        fd.forEach(function (v, k) { if (k !== "consent" && k !== "form_type" && v) body.push(k.replace(/_/g, " ") + ": " + v); });
        location.href = "mailto:" + cfg.email + "?subject=" + encodeURIComponent(form.dataset.subject || "DigiLab enquiry") + "&body=" + encodeURIComponent(body.join("\n"));
        show("ok", "Your email app should open now. Please press Send there to complete your submission.");
        return;
      }
      show("err", "This form is not connected yet. (Site owner: open assets/js/config.js and add your Web3Forms key and/or Google Sheet link.)");
    });
  });
})();
