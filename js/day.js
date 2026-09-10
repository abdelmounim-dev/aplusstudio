/* "A day in the house": scroll-driven hero. Loaded on the home page only.
   Scroll progress through the 400vh section maps to the hour, 06:00 to 06:00.
   Everything here illustrates the principles; nothing is measured data. */
(function () {
  "use strict";
  var root = document.getElementById("day");
  if (!root) return;

  var $ = function (id) { return document.getElementById(id); };
  var sun = $("day-sun"), moon = $("day-moon"), ray = $("day-ray"), shade = $("day-shade"), timeEl = $("day-time");
  var barOut = $("day-barOut"), barIn = $("day-barIn"), progress = $("day-progress"), hint = $("day-hint"), end = $("day-end");
  var thermalBtn = $("day-thermal");
  var captions = Array.prototype.slice.call(root.querySelectorAll(".day__caption"));
  var pathA = $("day-pathA"), pathB = $("day-pathB");
  var partsA = Array.prototype.slice.call($("day-partA").children);
  var partsB = Array.prototype.slice.call($("day-partB").children);
  var lenA = pathA.getTotalLength(), lenB = pathB.getTotalLength();

  // Physics-shaped curves, all in [0, 1], hour h in [6, 30).
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var bell = function (h, peak, width) { return Math.exp(-Math.pow((h - peak) / width, 2)); };
  var smooth = function (a, b, x) { var t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  var altitude = function (h) { return h >= 6 && h <= 19 ? Math.sin(Math.PI * (h - 6) / 13) : 0; };
  var outside = function (h) { return 0.15 + 0.85 * bell(h, 15, 5.2); };
  var inside = function (h) { return 0.28 + 0.34 * bell(h, 20, 6.5); };      // damped and lagged
  var wallHeat = function (h) { return 0.08 + 0.92 * bell(h, 18, 5); };       // ~3 h behind outside
  var stack = function (h) { return 0.25 + 0.75 * bell(h, 24.5, 5.5); };     // night: inside warmer than outside
  var night = function (h) { return smooth(18.6, 20.6, h) - smooth(28.4, 30, h); };

  var current = 6;

  function fmt(h) {
    var hh = Math.floor(h) % 24;
    var mm = Math.floor((h % 1) * 60);
    return (hh < 10 ? "0" : "") + hh + ":" + (mm < 10 ? "0" : "") + mm;
  }

  function render(h, p) {
    current = h;
    var alt = altitude(h), n = night(h), out = outside(h), inn = inside(h), heat = wallHeat(h);

    // Sun and moon on their arcs
    if (alt > 0) {
      var t = (h - 6) / 13;
      var sx = 80 + 740 * t, sy = 432 - 330 * alt;
      sun.setAttribute("transform", "translate(" + sx.toFixed(1) + " " + sy.toFixed(1) + ")");
      sun.style.opacity = smooth(0.08, 0.3, alt).toFixed(2); // fades in above the horizon
      ray.setAttribute("x1", sx.toFixed(1)); ray.setAttribute("y1", sy.toFixed(1));
      ray.style.opacity = (clamp((alt - 0.12) * 1.6, 0, 1) * 0.8).toFixed(2);
    } else {
      sun.style.opacity = "0"; ray.style.opacity = "0";
    }
    var tm = (h - 19) / 11;
    if (tm > 0 && tm < 1) {
      moon.setAttribute("transform", "translate(" + (80 + 740 * tm).toFixed(1) + " " + (432 - 250 * Math.sin(Math.PI * tm)).toFixed(1) + ")");
      moon.style.opacity = (n * 0.9 * smooth(0.08, 0.3, Math.sin(Math.PI * tm))).toFixed(2);
    } else { moon.style.opacity = "0"; }

    // Brise-soleil: high sun is blocked, low sun reaches the glass
    shade.setAttribute("height", (95 * clamp(alt * 1.35, 0, 1)).toFixed(1));

    // Outside / inside bars
    barOut.setAttribute("y", (150 - 150 * out).toFixed(1)); barOut.setAttribute("height", (150 * out).toFixed(1));
    barIn.setAttribute("y", (150 - 150 * inn).toFixed(1)); barIn.setAttribute("height", (150 * inn).toFixed(1));

    // Colours via CSS variables
    if (!root.classList.contains("is-thermal")) {
      // Sky: paper -> warm dusk -> near-black. Ink flips to paper once the sky is dark enough.
      var sky = n < 0.5 ? mix([250, 250, 248], [214, 178, 150], n * 2) : mix([214, 178, 150], [20, 16, 13], (n - 0.5) * 2);
      root.style.setProperty("--sky", sky);
      root.style.setProperty("--scene-ink", mix([17, 17, 17], [243, 239, 232], smooth(0.5, 0.72, n)));
    }
    root.style.setProperty("--night", n.toFixed(3));
    root.style.setProperty("--heat", heat.toFixed(3));
    root.style.setProperty("--out", out.toFixed(3));
    root.style.setProperty("--in", inn.toFixed(3));

    timeEl.textContent = fmt(h);
    if (progress) progress.style.width = (p * 100).toFixed(1) + "%";

    // Caption: the latest one whose start hour has passed
    var active = null;
    captions.forEach(function (c) { if (h >= parseFloat(c.dataset.hour)) active = c; });
    captions.forEach(function (c) { c.classList.toggle("is-on", c === active); });

    if (hint) hint.classList.toggle("is-off", p > 0.04);
    if (end) end.classList.toggle("is-on", p > 0.9);
  }

  function mix(a, b, t) {
    return "rgb(" + a.map(function (v, i) { return Math.round(v + (b[i] - v) * t); }).join(" ") + ")";
  }

  // Particles ride the two air paths; speed follows stack strength.
  var offsets = partsA.map(function (_, i) { return (i / partsA.length) * lenA; })
    .concat(partsB.map(function (_, i) { return (i / partsB.length) * lenB; }));
  var last = 0, inView = false;
  function tick(now) {
    var dt = Math.min(48, now - last) / 1000; last = now;
    if (inView && !document.hidden) {
      var speed = 28 + 150 * stack(current);
      partsA.forEach(function (el, i) {
        offsets[i] = (offsets[i] + speed * dt) % lenA;
        var pt = pathA.getPointAtLength(offsets[i]);
        el.setAttribute("cx", pt.x.toFixed(1)); el.setAttribute("cy", pt.y.toFixed(1));
      });
      partsB.forEach(function (el, i) {
        var k = partsA.length + i;
        offsets[k] = (offsets[k] + speed * 0.85 * dt) % lenB;
        var pt = pathB.getPointAtLength(offsets[k]);
        el.setAttribute("cx", pt.x.toFixed(1)); el.setAttribute("cy", pt.y.toFixed(1));
      });
    }
    requestAnimationFrame(tick);
  }

  // Thermal toggle
  if (thermalBtn) {
    thermalBtn.addEventListener("click", function () {
      var on = !root.classList.contains("is-thermal");
      root.classList.toggle("is-thermal", on);
      thermalBtn.setAttribute("aria-pressed", String(on));
      thermalBtn.textContent = on ? thermalBtn.dataset.off : thermalBtn.dataset.on;
      root.style.removeProperty("--sky"); root.style.removeProperty("--scene-ink");
      render(current, lastP);
    });
  }

  function placeParticles() {
    partsA.forEach(function (el, i) { var pt = pathA.getPointAtLength(offsets[i]); el.setAttribute("cx", pt.x.toFixed(1)); el.setAttribute("cy", pt.y.toFixed(1)); });
    partsB.forEach(function (el, i) { var pt = pathB.getPointAtLength(offsets[partsA.length + i]); el.setAttribute("cx", pt.x.toFixed(1)); el.setAttribute("cy", pt.y.toFixed(1)); });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var lastP = 0;
  if (reduce) {
    root.classList.add("day--static");
    render(15, 1);
    placeParticles();
    return;
  }

  var header = document.querySelector(".site-header");
  function onScroll() {
    var rect = root.getBoundingClientRect();
    var top = header ? header.offsetHeight : 0;
    var travel = root.offsetHeight - window.innerHeight;
    var p = clamp((top - rect.top) / travel, 0, 1);
    lastP = p;
    render(6 + 24 * p, p);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { inView = entries[0].isIntersecting; }, { threshold: 0 }).observe(root);
  } else { inView = true; }

  placeParticles();
  onScroll();
  requestAnimationFrame(function (t) { last = t; tick(t); });
})();
