/* ============================================================
   Japan '26 — Animations, observers, map helper
   ============================================================ */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // -------- Reveal on scroll --------
  function initReveals() {
    if (prefersReducedMotion) {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }

  // -------- Animated counters --------
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const decimals = parseInt(el.dataset.decimals || '0', 10);
    const duration = parseInt(el.dataset.duration || '1400', 10);
    const start = performance.now();
    function step(now) {
      const t = Math.min(1, (now - start) / duration);
      const v = target * easeOutCubic(t);
      el.textContent = decimals ? v.toFixed(decimals) : Math.round(v).toLocaleString();
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = decimals ? target.toFixed(decimals) : target.toLocaleString();
    }
    requestAnimationFrame(step);
  }
  function initCounters() {
    const targets = document.querySelectorAll('[data-counter]');
    if (!targets.length) return;
    if (prefersReducedMotion) {
      targets.forEach(el => {
        const v = parseFloat(el.dataset.target);
        const decimals = parseInt(el.dataset.decimals || '0', 10);
        el.textContent = decimals ? v.toFixed(decimals) : v.toLocaleString();
      });
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    targets.forEach(el => io.observe(el));
  }

  // -------- Leaflet map helper --------
  // Pass an element id and a route object from window.ROUTES.
  // Expects route.polylines = [{ from, to, mode, coords: [[lat,lng], ...] }, ...]
  // mode: 'ground' (real road/walk) | 'transit' (train/bus, dashed) | 'flight' (great-circle, dashed)
  window.initDayMap = function (elementId, routeKey) {
    const route = window.ROUTES && window.ROUTES[routeKey];
    if (!route || typeof L === 'undefined') return;
    const map = L.map(elementId, {
      center: route.center,
      zoom: route.zoom,
      scrollWheelZoom: false,
      zoomSnap: 0.5,
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap',
      maxZoom: 19,
    }).addTo(map);

    // Draw polylines first so markers sit on top
    const allCoords = [];
    if (route.polylines && route.polylines.length) {
      route.polylines.forEach(seg => {
        const style = polylineStyle(seg.mode);
        const layer = L.polyline(seg.coords, style).addTo(map);
        // Mode label on hover
        layer.bindTooltip(modeLabel(seg.mode), { sticky: true, className: 'route-tooltip' });
        seg.coords.forEach(c => allCoords.push(c));
      });
    }

    // Markers (numbered)
    route.points.forEach((p) => {
      const icon = L.divIcon({
        className: '',
        html: `<div class="route-marker">${p.n}</div>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });
      const m = L.marker([p.lat, p.lng], { icon }).addTo(map);
      m.bindPopup(`<strong>${p.label}</strong><br><span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.5px;text-transform:uppercase;opacity:.65;">${p.time}</span>`);
      allCoords.push([p.lat, p.lng]);
    });

    if (allCoords.length > 1) {
      map.fitBounds(allCoords, { padding: [40, 40] });
    }
  };

  function polylineStyle(mode) {
    if (mode === 'flight') {
      return { color: '#1A1A1A', weight: 2, opacity: 0.55, dashArray: '2 8', lineCap: 'round' };
    }
    if (mode === 'transit') {
      return { color: '#1A1A1A', weight: 3, opacity: 0.75, dashArray: '6 8', lineCap: 'round' };
    }
    // ground (driving / walking — real OSRM-routed)
    return { color: '#E04848', weight: 4.5, opacity: 0.88, lineCap: 'round', lineJoin: 'round' };
  }

  function modeLabel(mode) {
    if (mode === 'flight') return 'Flight · great-circle';
    if (mode === 'transit') return 'Train / transit';
    return 'Road / walking route';
  }

  // -------- Keyboard prev/next (day pages only) --------
  function initKeyboardNav() {
    const prev = document.querySelector('[data-prev-day]');
    const next = document.querySelector('[data-next-day]');
    document.addEventListener('keydown', (e) => {
      if (e.target.matches('input, textarea')) return;
      if (e.key === 'ArrowLeft' && prev) prev.click();
      if (e.key === 'ArrowRight' && next) next.click();
    });
  }

  // -------- Today badge (highlight current day) --------
  function highlightToday() {
    // Today's date — May 15, 2026 = day 1
    const tripStart = new Date('2026-05-15T00:00:00');
    const now = new Date();
    const dayIndex = Math.floor((now - tripStart) / 86400000) + 1;
    if (dayIndex >= 1 && dayIndex <= 10) {
      const target = document.querySelector(`[data-day="${dayIndex}"]`);
      if (target) target.classList.add('is-today');
    }
  }

  // -------- Init on DOM ready --------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  function boot() {
    initReveals();
    initCounters();
    initKeyboardNav();
    highlightToday();
    // Init day map if present
    const mapEl = document.querySelector('[data-map]');
    if (mapEl) {
      window.initDayMap(mapEl.id, mapEl.dataset.map);
    }
  }
})();
