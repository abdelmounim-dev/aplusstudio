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
        if (status) status.textContent = shown + " project" + (shown === 1 ? "" : "s") + " shown";
      });
    });
  }

  // Contact form: validate on submit, show status. Replace the action in contact.html to wire a backend.
  var form = document.getElementById("contact-form");
  if (form) {
    var statusBox = document.getElementById("form-status");
    var fields = form.querySelectorAll("[required]");
    function validate(input) {
      var wrap = input.closest(".field");
      var ok = input.checkValidity();
      if (wrap) wrap.dataset.invalid = String(!ok);
      return ok;
    }
    fields.forEach(function (f) { f.addEventListener("blur", function () { validate(f); }); });
    form.addEventListener("submit", function (e) {
      var firstBad = null;
      fields.forEach(function (f) { if (!validate(f) && !firstBad) firstBad = f; });
      if (firstBad) {
        e.preventDefault();
        firstBad.focus();
        return;
      }
      if (form.dataset.demo === "true") {
        e.preventDefault();
        statusBox.hidden = false;
        statusBox.textContent = "Thank you. This prototype does not send messages yet; once the form action is connected, your request will reach the studio.";
        form.reset();
        statusBox.focus();
      }
    });
  }
})();
