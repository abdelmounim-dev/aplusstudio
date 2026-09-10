/* A+ Studio — shared behaviour. No dependencies. */
(function () {
  "use strict";

  // Mobile navigation drawer
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("nav-drawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      drawer.dataset.open = String(!open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.dataset.open === "true") {
        toggle.setAttribute("aria-expanded", "false");
        drawer.dataset.open = "false";
        toggle.focus();
      }
    });
  }

  // Mark the current page in every nav list
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-list a, .drawer a").forEach(function (a) {
    var target = a.getAttribute("href").split("#")[0] || "index.html";
    if (target === here) a.setAttribute("aria-current", "page");
  });

  // Project filters
  var filters = document.querySelectorAll(".filter[data-filter]");
  if (filters.length) {
    var projects = document.querySelectorAll(".project[data-type]");
    var status = document.getElementById("filter-status");
    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        filters.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        var key = btn.dataset.filter;
        var shown = 0;
        projects.forEach(function (p) {
          var match = key === "all" || p.dataset.type === key;
          p.hidden = !match;
          if (match) shown++;
        });
        if (status) status.textContent = (status.dataset.statusTemplate || "{n} shown").replace("{n}", shown);
      });
    });
  }

  // Contact form: validate, then POST to the Pages Function at /api/contact.
  // Without JS the browser posts the form itself and the function redirects back with ?sent=1 or ?error=...
  var form = document.getElementById("contact-form");
  if (form) {
    var statusBox = document.getElementById("form-status");
    var submitBtn = form.querySelector('button[type="submit"]');
    var fields = form.querySelectorAll("[required]");
    function validate(input) {
      var wrap = input.closest(".field");
      var ok = input.checkValidity();
      if (wrap) wrap.dataset.invalid = String(!ok);
      return ok;
    }
    function showStatus(text, isError) {
      statusBox.hidden = false;
      statusBox.textContent = text;
      statusBox.dataset.state = isError ? "error" : "ok";
      statusBox.focus();
    }
    function markServerErrors(names) {
      (names || []).forEach(function (n) {
        var el = form.elements[n];
        var wrap = el && el.closest(".field");
        if (wrap) wrap.dataset.invalid = "true";
      });
    }
    fields.forEach(function (f) { f.addEventListener("blur", function () { validate(f); }); });

    // Result of a no-JS submission, delivered as a query string by the function.
    var params = new URLSearchParams(location.search);
    if (params.get("sent") === "1") showStatus(form.dataset.sent, false);
    else if (params.get("error")) showStatus(form.dataset.networkError, true);

    form.addEventListener("submit", function (e) {
      var firstBad = null;
      fields.forEach(function (f) { if (!validate(f) && !firstBad) firstBad = f; });
      if (firstBad) { e.preventDefault(); firstBad.focus(); return; }
      if (!window.fetch || !window.FormData) return; // plain POST, function redirects back
      e.preventDefault();
      var label = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.textContent = form.dataset.sending;
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json", "X-Requested-With": "fetch" }
      }).then(function (res) {
        return res.json().then(function (json) { return { status: res.status, json: json }; });
      }).then(function (r) {
        if (r.json.ok) { form.reset(); showStatus(r.json.message, false); }
        else { markServerErrors(r.json.errors); showStatus(r.json.message, true); }
      }).catch(function () {
        showStatus(form.dataset.networkError, true);
      }).then(function () {
        submitBtn.disabled = false;
        submitBtn.innerHTML = label;
        if (window.turnstile) { try { window.turnstile.reset(); } catch (err) {} }
      });
    });
  }
})();

/* Motion: scroll reveal and stat count-up. Skipped entirely under prefers-reduced-motion. */
(function () {
  "use strict";
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) return;

  var groups = [".grid > *", ".project-grid > *", ".notes-strip > *", ".steps > *", ".principles > *", ".stats > *", ".notes-list > *", ".faq > details", ".footer-grid > *"];
  var singles = [".section-head", ".prose", ".figure", ".callout", ".quote", ".cta > *", ".contact-list", ".form", ".map", ".spec-list", ".split > *:not(.figure)"];

  groups.forEach(function (sel) {
    var items = document.querySelectorAll(sel);
    var i = 0;
    items.forEach(function (el) {
      if (el.closest(".hero, .page-hero")) return;
      el.setAttribute("data-reveal", "");
      el.style.setProperty("--reveal-delay", Math.min(i, 7) * 70 + "ms");
      i++;
    });
  });
  singles.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      if (el.closest(".hero, .page-hero") || el.hasAttribute("data-reveal") || el.querySelector("[data-reveal]")) return;
      el.setAttribute("data-reveal", "");
    });
  });

  function countUp(el) {
    var raw = el.textContent.trim();
    var m = raw.match(/\d+/);
    if (!m) return;
    var target = parseInt(m[0], 10);
    var prefix = raw.slice(0, m.index), suffix = raw.slice(m.index + m[0].length);
    var start = performance.now(), dur = 900;
    function tick(now) {
      var p = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      var v = entry.target.querySelector(".stat__value");
      if (v && !v.dataset.counted) { v.dataset.counted = "1"; countUp(v); }
      io.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });

  document.querySelectorAll("[data-reveal]").forEach(function (el) { io.observe(el); });

  // Safety net: if observers have not fired (hidden tab, throttled browser), reveal what is on screen.
  function sweep() {
    document.querySelectorAll("[data-reveal]:not(.is-in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom > 0 && r.top < window.innerHeight) { el.classList.add("is-in"); io.unobserve(el); }
    });
  }
  setTimeout(sweep, 1500);
  window.addEventListener("scroll", function () { setTimeout(sweep, 400); }, { passive: true });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) setTimeout(sweep, 100); });
})();
