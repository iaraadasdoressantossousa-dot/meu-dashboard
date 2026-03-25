/* eslint-disable no-undef */
(function () {
  "use strict";

  function initSwiper() {
    const swiperRoot = document.querySelector(".hero-swiper");
    if (!swiperRoot || typeof Swiper === "undefined") return;

    // Swiper hero full experience
    // Note: uses global Swiper from CDN script.
    // eslint-disable-next-line no-new
    new Swiper(swiperRoot, {
      loop: true,
      speed: 900,
      autoplay: {
        delay: 6500,
        disableOnInteraction: false,
      },
      keyboard: {
        enabled: true,
        onlyInViewport: true,
      },
      slidesPerView: 1,
      spaceBetween: 16,
      pagination: {
        el: swiperRoot.querySelector(".swiper-pagination"),
        clickable: true,
      },
      navigation: {
        nextEl: swiperRoot.querySelector(".swiper-button-next"),
        prevEl: swiperRoot.querySelector(".swiper-button-prev"),
      },
      a11y: {
        enabled: true,
      },
    });
  }

  function getFocusableElements(root) {
    const selectors = [
      "a[href]",
      "button:not([disabled])",
      "textarea:not([disabled])",
      "input:not([disabled])",
      "select:not([disabled])",
      "[tabindex]:not([tabindex='-1'])",
    ];
    return Array.from(root.querySelectorAll(selectors.join(","))).filter((el) => {
      const style = window.getComputedStyle(el);
      return style.visibility !== "hidden" && style.display !== "none";
    });
  }

  function initDrawer() {
    const toggleBtn = document.querySelector(".nav-toggle");
    const drawer = document.getElementById("mobile-drawer");
    const overlay = document.getElementById("drawer-overlay");
    const closeBtn = document.querySelector(".drawer-close");
    if (!toggleBtn || !drawer || !overlay || !closeBtn) return;

    let lastFocusedEl = null;

    function setOpen(isOpen) {
      if (isOpen) {
        lastFocusedEl = document.activeElement;
        drawer.classList.add("is-open");
        overlay.classList.add("is-open");
        document.body.style.overflow = "hidden";
        toggleBtn.setAttribute("aria-expanded", "true");

        // Focus first meaningful element
        closeBtn.focus();
        // Improve SR experience
        drawer.setAttribute("aria-hidden", "false");
      } else {
        drawer.classList.remove("is-open");
        overlay.classList.remove("is-open");
        document.body.style.overflow = "";
        toggleBtn.setAttribute("aria-expanded", "false");
        drawer.setAttribute("aria-hidden", "true");

        if (lastFocusedEl && typeof lastFocusedEl.focus === "function") {
          lastFocusedEl.focus();
        }
      }
    }

    // Default SR state
    drawer.setAttribute("aria-hidden", "true");
    overlay.classList.remove("is-open");
    toggleBtn.setAttribute("aria-expanded", "false");

    function openDrawer() {
      if (drawer.classList.contains("is-open")) return;
      setOpen(true);
    }

    function closeDrawer() {
      if (!drawer.classList.contains("is-open")) return;
      setOpen(false);
    }

    toggleBtn.addEventListener("click", () => {
      const isOpen = drawer.classList.contains("is-open");
      if (isOpen) closeDrawer();
      else openDrawer();
    });

    closeBtn.addEventListener("click", closeDrawer);
    overlay.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (e) => {
      if (!drawer.classList.contains("is-open")) return;

      if (e.key === "Escape") {
        e.preventDefault();
        closeDrawer();
        return;
      }

      if (e.key !== "Tab") return;

      const focusable = getFocusableElements(drawer);
      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
        return;
      }

      if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    // Close drawer after navigation
    drawer.addEventListener("click", (e) => {
      const link = e.target.closest("a[href]");
      if (!link) return;
      closeDrawer();
    });
  }

  function initFooterYear() {
    const yearEl = document.getElementById("year");
    if (!yearEl) return;
    yearEl.textContent = String(new Date().getFullYear());
  }

  function initContactForm() {
    const form = document.getElementById("contact-form");
    if (!form) return;
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      // Demo only: integrate with your API/endpoint when needed.
    });
  }

  function initHashScroll() {
    function forceCloseDrawerIfOpen() {
      const drawer = document.getElementById("mobile-drawer");
      const overlay = document.getElementById("drawer-overlay");
      if (!drawer || !drawer.classList.contains("is-open")) return;

      drawer.classList.remove("is-open");
      if (overlay) overlay.classList.remove("is-open");
      drawer.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";

      const toggleBtn = document.querySelector(".nav-toggle");
      if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
    }

    document.addEventListener("click", (e) => {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;

      const href = link.getAttribute("href") || "";
      if (href === "#" || href.trim().length <= 1) return;

      const id = href.slice(1);
      const target = document.getElementById(id);
      if (!target) return;

      // Prevent default hash jump; we handle smooth scroll + focus.
      e.preventDefault();
      forceCloseDrawerIfOpen();

      target.scrollIntoView({ behavior: "smooth", block: "start" });

      // Move focus for accessibility without yanking the page again.
      try {
        const prevTabIndex = target.getAttribute("tabindex");
        target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
        target.addEventListener(
          "blur",
          () => {
            if (prevTabIndex === null) target.removeAttribute("tabindex");
            else target.setAttribute("tabindex", prevTabIndex);
          },
          { once: true }
        );
      } catch {
        // Ignore focus errors (older browsers).
      }

      // Keep URL hash in sync.
      history.replaceState(null, "", href);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initSwiper();
    initDrawer();
    initFooterYear();
    initContactForm();
    initHashScroll();
  });
})();

