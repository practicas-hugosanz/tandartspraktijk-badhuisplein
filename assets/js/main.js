/* Tandartspraktijk Badhuisplein — interactie (geen afhankelijkheden) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Openingstijden (Europe/Amsterdam) ---------- */
  // [dag 0=zo..6=za]: lijst van [open, dicht] in minuten
  var HOURS = {
    1: [[480, 720], [780, 990]],
    2: [[480, 720], [780, 990]],
    3: [[480, 720], [780, 990]],
    4: [[480, 720], [780, 990]],
    5: [[510, 750], [780, 990]]
  };
  var DAYS = ["zondag", "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag"];

  function nowNL() {
    try {
      var p = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Amsterdam", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
      var o = {};
      p.forEach(function (x) { o[x.type] = x.value; });
      var d = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(o.weekday);
      return { day: d, min: (+o.hour % 24) * 60 + +o.minute };
    } catch (e) {
      var n = new Date();
      return { day: n.getDay(), min: n.getHours() * 60 + n.getMinutes() };
    }
  }
  function fmt(m) { return Math.floor(m / 60) + ":" + ("0" + (m % 60)).slice(-2); }

  function status() {
    var n = nowNL(), today = HOURS[n.day] || [];
    for (var i = 0; i < today.length; i++) {
      if (n.min >= today[i][0] && n.min < today[i][1]) return { open: true, text: "Nu open tot " + fmt(today[i][1]) + " uur" };
      if (n.min < today[i][0]) return { open: false, text: (i ? "Pauze, weer open om " : "Gesloten, vandaag open om ") + fmt(today[i][0]) + " uur" };
    }
    for (var k = 1; k <= 7; k++) {
      var d = (n.day + k) % 7;
      if (HOURS[d]) return { open: false, text: "Gesloten, " + (k === 1 ? "morgen" : DAYS[d]) + " open om " + fmt(HOURS[d][0][0]) + " uur" };
    }
    return { open: false, text: "Gesloten" };
  }
  var st = status();
  document.querySelectorAll("[data-status]").forEach(function (el) {
    el.textContent = st.text;
    el.classList.toggle("is-open", st.open);
  });
  var today = nowNL().day;
  document.querySelectorAll("[data-day='" + today + "']").forEach(function (el) { el.classList.add("is-today"); });

  /* ---------- Masthead: bovenste rij scrolt weg, de navigatiebalk blijft staan ---------- */
  var mast = document.querySelector(".mast");
  var mastTop = mast && mast.querySelector(".mast__top");
  var mbar = document.querySelector(".mbar");
  var wasStuck = null;
  function onScroll() {
    var y = window.scrollY;
    if (mast && mastTop) {
      var stuck = y > mastTop.offsetHeight && getComputedStyle(mast.querySelector(".mast__bar")).display !== "none";
      if (stuck !== wasStuck) {
        mast.classList.toggle("is-stuck", stuck);
        // de verkorte link is alleen bereikbaar als hij zichtbaar is
        mast.querySelector(".mast__quick").tabIndex = stuck ? 0 : -1;
        wasStuck = stuck;
      }
    }
    if (mbar) mbar.classList.toggle("is-on", y > 420 && !doc.classList.contains("menu-open"));
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Achtergrondvideo in de hero ---------- */
  var video = document.querySelector("[data-hero-video]");
  var pauseBtn = document.querySelector("[data-hero-pause]");
  if (video && pauseBtn) {
    var userPaused = reduce;
    var label = pauseBtn.querySelector("span");
    var setState = function () {
      pauseBtn.setAttribute("aria-pressed", String(userPaused));
      label.textContent = userPaused ? "Video afspelen" : "Video pauzeren";
      pauseBtn.querySelector("path").setAttribute("d", userPaused ? "M8 5l11 7-11 7z" : "M8 5v14M16 5v14");
    };
    if (reduce) video.pause();
    setState();
    pauseBtn.addEventListener("click", function () {
      userPaused = !userPaused;
      if (userPaused) video.pause(); else video.play().catch(function () {});
      setState();
    });
    // buiten beeld stilzetten, scheelt batterij
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        if (userPaused) return;
        if (en[0].isIntersecting) video.play().catch(function () {}); else video.pause();
      }).observe(video);
    }
  }

  /* ---------- Teamstrook: pijlknoppen naast het vegen ---------- */
  document.querySelectorAll("[data-rail]").forEach(function (btn) {
    var strip = document.getElementById(btn.getAttribute("aria-controls"));
    if (!strip) return;
    btn.addEventListener("click", function () {
      strip.scrollBy({ left: +btn.getAttribute("data-rail") * strip.clientWidth * 0.8, behavior: reduce ? "auto" : "smooth" });
    });
  });
  document.querySelectorAll(".team-strip").forEach(function (strip) {
    var prev = document.querySelector('[data-rail="-1"][aria-controls="' + strip.id + '"]');
    var next = document.querySelector('[data-rail="1"][aria-controls="' + strip.id + '"]');
    if (!prev || !next) return;
    var update = function () {
      prev.disabled = strip.scrollLeft <= 4;
      next.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 4;
    };
    strip.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ---------- Desktop dropdowns ---------- */
  var items = document.querySelectorAll(".nav__item.has-drop");
  function closeAll(except) {
    items.forEach(function (it) {
      if (it !== except) {
        it.classList.remove("is-open");
        var b = it.querySelector("button");
        if (b) b.setAttribute("aria-expanded", "false");
      }
    });
  }
  items.forEach(function (it) {
    var btn = it.querySelector("button");
    var t;
    btn.addEventListener("click", function () {
      var open = !it.classList.contains("is-open");
      closeAll(it);
      it.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
    it.addEventListener("mouseenter", function () {
      if (!window.matchMedia("(hover: hover)").matches) return;
      clearTimeout(t); closeAll(it);
      it.classList.add("is-open"); btn.setAttribute("aria-expanded", "true");
    });
    it.addEventListener("mouseleave", function () {
      if (!window.matchMedia("(hover: hover)").matches) return;
      t = setTimeout(function () { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }, 160);
    });
    it.addEventListener("focusout", function (e) {
      if (!it.contains(e.relatedTarget)) { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeAll(); toggleMenu(false); }
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav__item.has-drop")) closeAll();
  });

  /* ---------- Mobiel menu ---------- */
  var burger = document.querySelector(".burger");
  var drawer = document.getElementById("drawer");
  function toggleMenu(force) {
    if (!burger) return;
    var open = typeof force === "boolean" ? force : !doc.classList.contains("menu-open");
    doc.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
    if (drawer) drawer.inert = !open;
    onScroll();
  }
  if (burger) {
    if (drawer) drawer.inert = true;
    burger.addEventListener("click", function () { toggleMenu(); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1024) toggleMenu(false); });
  }

  /* ---------- Reveal bij scrollen ---------- */
  // Alleen elementen onder de vouw verbergen; zichtbaar maken zodra ze in beeld scrollen
  if (!reduce) {
    var pending = [].slice.call(document.querySelectorAll(".rv")).filter(function (el) {
      return el.getBoundingClientRect().top > window.innerHeight;
    });
    if (pending.length) {
      var ticking = false;
      var reveal = function () {
        ticking = false;
        var h = window.innerHeight * 0.92;
        pending = pending.filter(function (el) {
          if (el.getBoundingClientRect().top < h) { el.classList.add("in"); return false; }
          return true;
        });
        if (!pending.length) window.removeEventListener("scroll", onReveal);
      };
      var onReveal = function () { if (!ticking) { ticking = true; setTimeout(reveal, 50); } };
      document.querySelectorAll(".rv").forEach(function (el) { if (pending.indexOf(el) < 0) el.classList.add("in"); });
      window.addEventListener("scroll", onReveal, { passive: true });
      window.addEventListener("resize", onReveal);
      setTimeout(reveal, 60);
    }
  }

  /* ---------- Kaart pas laden na klik (privacy: geen Google-cookies vooraf) ---------- */
  document.querySelectorAll("[data-map]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".map");
      var f = document.createElement("iframe");
      f.src = btn.getAttribute("data-map");
      f.title = "Kaart: Tandartspraktijk Badhuisplein, Badhuisplein 6 Hardenberg";
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      f.allowFullscreen = true;
      box.appendChild(f);
      box.classList.add("is-loaded");
    });
  });

  /* ---------- Formulieren ---------- */
  var params = new URLSearchParams(location.search);
  document.querySelectorAll("[data-param]").forEach(function (el) {
    var v = (params.get(el.getAttribute("data-param")) || "").replace(/[^a-z0-9-]/gi, "");
    if (!v) return;
    if (el.tagName === "SELECT") { if (el.querySelector("option[value='" + v + "']")) el.value = v; return; }
    var r = el.querySelector("input[value='" + v + "']");
    if (r) r.checked = true;
  });

  var MAIL = "info@praktijkbadhuisplein.nl";
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    function check(field) {
      var wrap = field.closest(".field");
      if (!wrap) return true;
      var ok = field.checkValidity();
      if (ok && field.type === "tel") ok = !field.value || /^[+()\d\s-]{10,}$/.test(field.value);
      wrap.classList.toggle("is-invalid", !ok);
      field.setAttribute("aria-invalid", String(!ok));
      return ok;
    }
    form.addEventListener("blur", function (e) {
      if (e.target.matches("input,select,textarea")) check(e.target);
    }, true);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fields = form.querySelectorAll("input,select,textarea");
      var first = null;
      fields.forEach(function (f) { if (!check(f) && !first) first = f; });
      if (first) { first.focus(); return; }

      var data = new FormData(form);
      var lines = [];
      form.querySelectorAll(".field").forEach(function (w) {
        var lab = w.querySelector("label,legend");
        var inp = w.querySelector("input,select,textarea");
        if (!lab || !inp || inp.type === "checkbox" && inp.name === "akkoord") return;
        var vals = (inp.type === "radio" || inp.type === "checkbox")
          ? [].map.call(w.querySelectorAll("input:checked"), function (i) { return i.closest("label").textContent.trim(); })
          : data.getAll(inp.name).filter(Boolean);
        if (vals.length) lines.push(lab.textContent.replace(/\s*\(optioneel\)/, "").trim() + ": " + vals.join(", "));
      });
      var subject = form.getAttribute("data-form");
      var endpoint = form.getAttribute("data-endpoint");

      function done() {
        form.classList.add("is-sent");
        var ok = form.querySelector(".form__ok");
        if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
      }
      if (endpoint) {
        // Koppel hier een eigen verwerker (bijv. PHP-mailer of Formspree) via data-endpoint
        fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (r) { if (!r.ok) throw new Error(); done(); form.reset(); })
          .catch(function () {
            var err = form.querySelector(".form__err");
            if (err) err.hidden = false;
          });
      } else {
        location.href = "mailto:" + MAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
        done();
      }
    });
  });

  /* ---------- Jaar in footer ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
