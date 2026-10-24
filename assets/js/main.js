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

  // fast-track checklist on the apply page: each item ticks as the visitor completes it
  var ft = $("[data-ft-box]");
  if (ft && ft.closest("form")) {
    var ftForm = ft.closest("form");
    var ftItems = $$("[data-ft-for]", ft), ftStatus = $("[data-ft-status]", ft);
    var ftUpdate = function () {
      var done = 0;
      ftItems.forEach(function (li) {
        var el = ftForm.elements[li.getAttribute("data-ft-for")];
        var ok = !!(el && el.value.trim() && el.checkValidity());
        li.classList.toggle("done", ok);
        if (ok) done++;
      });
      if (ftStatus) {
        var all = done === ftItems.length;
        ftStatus.textContent = all ? "Fast-track unlocked" : done + " of " + ftItems.length + " done";
        ftStatus.classList.toggle("ok", all);
      }
    };
    ftForm.addEventListener("input", ftUpdate);
    ftUpdate();
  }

  // optional extra button just above "Submit application" (apply page only).
  // Its text, link and note live in assets/js/button.js (a separate file, so a typo there cannot break the forms).
  var xMark = $("form[data-form] input[name=form_type][value=application]");
  var xSubmit = xMark && xMark.form && $("button[type=submit]", xMark.form);
  if (xSubmit) {
    var xScript = document.createElement("script");
    xScript.src = "assets/js/button.js";
    xScript.onload = function () {
      var c = window.DIGILAB_BUTTON || {};
      var label = String(c.label || "").trim(), link = String(c.link || "").trim();
      var note = String(c.note || "").trim();
      var tag = c.tag === undefined ? "Sponsored" : String(c.tag).trim();
      if (!label || !link || /^\s*(javascript|data|vbscript):/i.test(link) || $(".extra-cta")) return;
      var box = document.createElement("div");
      box.className = "extra-cta";
      box.style.textAlign = "center";
      if (tag) {
        var t = document.createElement("small");
        t.textContent = tag;
        t.style.cssText = "display:block;text-transform:uppercase;letter-spacing:.1em;font-size:.68rem;color:var(--muted);margin-bottom:8px";
        box.appendChild(t);
      }
      var a = document.createElement("a");
      a.className = "btn btn-block";
      a.href = link;
      a.target = "_blank";
      a.rel = "sponsored nofollow noopener";
      a.textContent = label;
      a.style.background = "var(--brand2)";
      a.style.boxShadow = "0 8px 20px -8px var(--brand2)";
      a.style.setProperty("color", "#0b1220", "important");
      box.appendChild(a);
      if (note) {
        var p = document.createElement("p");
        p.textContent = note;
        p.style.cssText = "margin:10px 0 0;font-size:.92rem;color:var(--muted)";
        box.appendChild(p);
      }
      xSubmit.parentNode.insertBefore(box, xSubmit);
    };
    document.head.appendChild(xScript);
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
            form.dispatchEvent(new Event("input", { bubbles: true })); // refresh the fast-track ticks
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
