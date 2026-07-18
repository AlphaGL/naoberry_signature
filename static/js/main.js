/* ============================================================
   NAOBERRY SIGNATURE — main.js
   ============================================================ */

/* ------------------------------------------------------------
   SITE DATA
   Everything below is managed from the /dashboard/ admin and
   rendered into the page as JSON by Django (see index.html).
   ------------------------------------------------------------ */
const SITE = JSON.parse(document.getElementById("site-data").textContent);
const IG = SITE.instagram;
const WHATSAPP = SITE.whatsappNumber;

const WORKS = SITE.works;       // [{src, cat, cap, ar, link}] — managed in the dashboard
const PRODUCTS = SITE.products; // [imageUrl, …]
const STUDENTS = SITE.students; // [imageUrl, …]

const CAT_LABEL = {
  bridal: "Bridal",
  owanbe: "Owanbe",
  glam: "Glam",
  transform: "Before / After",
  studio: "Studio",
};

/* ------------------------------------------------------------ helpers */
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];

/* ------------------------------------------------------------ preloader */
window.addEventListener("load", () => {
  setTimeout(() => $("#preloader").classList.add("is-done"), 1100);
});
/* safety: never trap the visitor if load hangs */
setTimeout(() => $("#preloader").classList.add("is-done"), 4000);

/* ------------------------------------------------------------ header hide/show */
const header = $("#header");
let lastY = 0;
window.addEventListener("scroll", () => {
  const y = window.scrollY;
  header.classList.toggle("is-scrolled", y > 40);
  header.classList.toggle("is-hidden", y > 500 && y > lastY && !menu.classList.contains("is-open"));
  lastY = y;
}, { passive: true });

/* ------------------------------------------------------------ mobile menu */
const burger = $("#burger");
const menu = $("#menu");
function setMenu(open) {
  menu.classList.toggle("is-open", open);
  burger.classList.toggle("is-open", open);
  header.classList.toggle("menu-open", open);
  if (open) header.classList.remove("is-hidden"); // keep the ✕ reachable
  burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  document.body.style.overflow = open ? "hidden" : "";
}
burger.addEventListener("click", () => setMenu(!menu.classList.contains("is-open")));
$$(".menu__link, .menu .btn").forEach((a) =>
  a.addEventListener("click", () => setMenu(false))
);

/* ------------------------------------------------------------ build gallery */
const gallery = $("#gallery");
WORKS.forEach((w) => {
  const item = document.createElement("article");
  item.className = "work-item";
  item.dataset.cat = w.cat;
  item.innerHTML = `
    <figure style="--ar:${w.ar}">
      <img src="${w.src}" alt="${w.cap} — Naoberry Signature" loading="lazy"
           onerror="this.closest('figure').classList.add('is-empty')" />
      <figcaption class="ph" aria-hidden="true">
        <span class="ph__mono">N·S</span>
        <span class="ph__hint">Naoberry Signature</span>
      </figcaption>
    </figure>
    <div class="work-item__meta">
      <span class="work-item__cap">${w.cap}</span>
      <span class="work-item__tag">${CAT_LABEL[w.cat]}</span>
    </div>`;
  item.addEventListener("click", () => openLightbox(w));
  gallery.appendChild(item);
});

/* ------------------------------------------------------------ build beauty bar */
const shopGrid = $("#products");
PRODUCTS.forEach((src, i) => {
  const num = String(i + 1).padStart(2, "0");
  // Cloudinary URLs are public, so the enquiry message links the exact photo —
  // WhatsApp previews it and she sees which product the customer means.
  const photoLink = /^https?:\/\//.test(src) ? ` Photo: ${src}` : "";
  const msg = `Hi Naoberry Signature! I'm interested in product No. ${num} in the Beauty Bar on your website. How much is it?${photoLink}`;
  const card = document.createElement("a");
  card.className = "product reveal";
  card.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;
  card.target = "_blank";
  card.rel = "noopener";
  card.setAttribute("data-cursor", "");
  card.innerHTML = `
    <figure>
      <img src="${src}" alt="Naoberry Signature beauty product ${num}" loading="lazy"
           onerror="this.closest('figure').classList.add('is-empty')" />
      <figcaption class="ph" aria-hidden="true">
        <span class="ph__mono">N·S</span>
        <span class="ph__hint">№ ${num}</span>
      </figcaption>
    </figure>
    <div class="product__bar">
      <span class="product__num">№ ${num}</span>
      <span class="product__order">DM for price <span>↗</span></span>
    </div>`;
  shopGrid.appendChild(card);
});

/* ------------------------------------------------------------ build certified students */
const alumniGrid = $("#alumni");
STUDENTS.forEach((src) => {
  const card = document.createElement("figure");
  card.className = "alum";
  card.innerHTML = `
    <img src="${src}" alt="Certified Naoberry Academy graduate holding her certificate" loading="lazy"
         onerror="this.closest('figure').classList.add('is-empty')" />
    <figcaption class="ph" aria-hidden="true">
      <span class="ph__mono">N·S</span>
      <span class="ph__hint">Naoberry Academy</span>
    </figcaption>
    <span class="alum__badge">✦ Certified · Naoberry Academy</span>`;
  alumniGrid.appendChild(card);
});

/* ------------------------------------------------------------ gallery filter + show more
   The "All" view shows GALLERY_PREVIEW items first; the button
   reveals the rest. Category views always show everything in
   that category. Add as many WORKS as you like — the first
   GALLERY_PREVIEW entries are the storefront, order them best-first. */
const GALLERY_PREVIEW = 12;
const showMoreBtn = $("#showMore");
let currentFilter = "all";
let galleryExpanded = false;

function updateGallery() {
  let matched = 0;
  $$(".work-item").forEach((item) => {
    const matches = currentFilter === "all" || item.dataset.cat === currentFilter;
    const capped =
      matches && currentFilter === "all" && !galleryExpanded && matched >= GALLERY_PREVIEW;
    if (matches) matched++;
    item.classList.toggle("is-filtered-out", !matches || capped);
  });
  const hiddenCount =
    currentFilter === "all" && !galleryExpanded ? Math.max(0, matched - GALLERY_PREVIEW) : 0;
  showMoreBtn.style.display = hiddenCount > 0 ? "" : "none";
  showMoreBtn.querySelector("span").textContent = `Show ${hiddenCount} more look${hiddenCount === 1 ? "" : "s"}`;
}

$("#filters").addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  $$(".chip").forEach((c) => c.classList.remove("is-active"));
  chip.classList.add("is-active");
  currentFilter = chip.dataset.filter;
  updateGallery();
});

showMoreBtn.addEventListener("click", () => {
  galleryExpanded = true;
  updateGallery();
});

updateGallery();

/* ------------------------------------------------------------ lightbox / gallery viewer
   Professional viewer: ←/→ arrows, keyboard, swipe on touch,
   counter, category tag. Navigation stays inside the active
   filter (browsing "Bridal" only pages through bridal looks). */
const lightbox = $("#lightbox");
const lightboxImg = $("#lightboxImg");
const lightboxCap = $("#lightboxCap");
const lightboxTag = $("#lightboxTag");
const lightboxCount = $("#lightboxCount");
const lightboxLink = $("#lightboxLink");

let lbList = [];
let lbIdx = 0;

function renderLightbox() {
  const w = lbList[lbIdx];
  lightboxImg.style.opacity = 0;
  const pre = new Image();
  pre.onload = () => {
    lightboxImg.src = w.src;
    lightboxImg.alt = w.cap;
    lightboxImg.style.opacity = 1;
  };
  pre.src = w.src;
  lightboxCap.textContent = w.cap;
  lightboxTag.textContent = CAT_LABEL[w.cat];
  lightboxCount.textContent =
    `${String(lbIdx + 1).padStart(2, "0")} / ${String(lbList.length).padStart(2, "0")}`;
  lightboxLink.href = w.link;
}

function openLightbox(w) {
  lbList = WORKS.filter((x) => currentFilter === "all" || x.cat === currentFilter);
  lbIdx = Math.max(0, lbList.indexOf(w));
  renderLightbox();
  lightbox.classList.add("is-open");
  document.body.style.overflow = "hidden";
}
function stepLightbox(dir) {
  lbIdx = (lbIdx + dir + lbList.length) % lbList.length;
  renderLightbox();
}
function closeLightbox() {
  lightbox.classList.remove("is-open");
  document.body.style.overflow = "";
}

$("#lightboxClose").addEventListener("click", closeLightbox);
$("#lightboxPrev").addEventListener("click", () => stepLightbox(-1));
$("#lightboxNext").addEventListener("click", () => stepLightbox(1));
lightbox.addEventListener("click", (e) => { if (e.target === lightbox) closeLightbox(); });

document.addEventListener("keydown", (e) => {
  if (!lightbox.classList.contains("is-open")) return;
  if (e.key === "Escape") closeLightbox();
  if (e.key === "ArrowLeft") stepLightbox(-1);
  if (e.key === "ArrowRight") stepLightbox(1);
});

/* swipe to browse on touch screens */
let touchX = null;
lightbox.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
lightbox.addEventListener("touchend", (e) => {
  if (touchX === null) return;
  const dx = e.changedTouches[0].clientX - touchX;
  if (Math.abs(dx) > 45) stepLightbox(dx < 0 ? 1 : -1);
  touchX = null;
}, { passive: true });

/* ------------------------------------------------------------ scroll reveal */
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      io.unobserve(entry.target);
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
);
$$(".reveal, .work-item").forEach((el, i) => {
  el.style.transitionDelay = `${(i % 4) * 70}ms`;
  io.observe(el);
});

/* ------------------------------------------------------------ counters */
const counterIO = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = +el.dataset.count;
      const t0 = performance.now();
      const dur = 1600;
      (function tick(now) {
        const p = Math.min((now - t0) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))); // ease-out cubic
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
      counterIO.unobserve(el);
    });
  },
  { threshold: 0.6 }
);
$$("[data-count]").forEach((el) => counterIO.observe(el));

/* ------------------------------------------------------------ testimonial slider */
const voices = $$(".voice");
const dotsWrap = $("#dots");
let voiceIdx = 0;
let voiceTimer;

voices.forEach((_, i) => {
  const dot = document.createElement("button");
  dot.setAttribute("aria-label", `Testimonial ${i + 1}`);
  if (i === 0) dot.classList.add("is-active");
  dot.addEventListener("click", () => { showVoice(i); restartVoiceTimer(); });
  dotsWrap.appendChild(dot);
});
const dots = $$("button", dotsWrap);

function showVoice(i) {
  voiceIdx = i;
  voices.forEach((v, j) => v.classList.toggle("is-active", j === i));
  dots.forEach((d, j) => d.classList.toggle("is-active", j === i));
}
function restartVoiceTimer() {
  clearInterval(voiceTimer);
  voiceTimer = setInterval(() => showVoice((voiceIdx + 1) % voices.length), 5500);
}
if (voices.length > 1) restartVoiceTimer();

/* ------------------------------------------------------------ soft parallax on photos */
const parallaxEls = $$("[data-parallax]");
if (parallaxEls.length && matchMedia("(prefers-reduced-motion: no-preference)").matches) {
  window.addEventListener("scroll", () => {
    const vh = window.innerHeight;
    parallaxEls.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const progress = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 … 0.5
      const img = el.querySelector("img");
      if (img) img.style.transform = `translateY(${progress * -26}px) scale(1.08)`;
    });
  }, { passive: true });
}

/* ------------------------------------------------------------ custom cursor */
if (matchMedia("(pointer: fine)").matches) {
  const cursor = $("#cursor");
  const ring = $("#cursorRing");
  let mx = 0, my = 0, rx = 0, ry = 0;

  window.addEventListener("mousemove", (e) => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx + "px";
    cursor.style.top = my + "px";
  });
  (function follow() {
    rx += (mx - rx) * 0.16;
    ry += (my - ry) * 0.16;
    ring.style.left = rx + "px";
    ring.style.top = ry + "px";
    requestAnimationFrame(follow);
  })();

  document.addEventListener("mouseover", (e) => {
    ring.classList.toggle(
      "is-hover",
      !!e.target.closest("a, button, .work-item, [data-cursor]")
    );
  });
}

/* ------------------------------------------------------------ footer year */
$("#year").textContent = new Date().getFullYear();
