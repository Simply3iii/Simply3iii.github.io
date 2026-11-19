// Small touches: fade-in on scroll, reading-progress bar, image lightbox, project filters.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Fade things in as they scroll into view.
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.1 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  // Reading-progress bar, and a shadow under the top bar once you scroll.
  var bar = document.querySelector(".progress span");
  var photo = document.querySelector(".hero .photo");
  function onScroll() {
    var h = document.documentElement;
    bar.style.width = (h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight) * 100) + "%";
    document.body.classList.toggle("scrolled", h.scrollTop > 40);
    if (photo && !reduce) photo.style.transform = "translateY(" + Math.min(h.scrollTop * 0.08, 40) + "px)";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Click any picture in a project or log entry to see it full size.
  var box = document.querySelector(".lightbox");
  document.querySelectorAll(".prose img, .gallery img").forEach(function (img) {
    img.addEventListener("click", function () {
      box.querySelector("img").src = img.src;
      box.querySelector("p").textContent = img.alt || "";
      box.hidden = false;
    });
  });
  if (box) {
    box.addEventListener("click", function () { box.hidden = true; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") box.hidden = true; });
  }

  // Tag filters on the Projects page.
  var buttons = document.querySelectorAll(".filters button");
  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      buttons.forEach(function (x) { x.classList.toggle("on", x === b); });
      var f = b.getAttribute("data-filter");
      document.querySelectorAll(".cards .card").forEach(function (c) {
        var tags = (c.getAttribute("data-tags") || "").split("|");
        c.classList.toggle("hide", f !== "*" && tags.indexOf(f) === -1);
      });
    });
  });
})();
