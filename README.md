# Japan '26 · May 15–24

A static, single-page travel guide for a 10-day trip across **Tokyo, Lake Kawaguchi, Fujinomiya, Hakone, Kamakura, and Ikebukuro** (15–24 May 2026).

🌐 **Live site:** https://onlypaul.github.io/japan-may-2026/

## What's inside

- [`index.html`](index.html) — overview, hero, bookings, and links to each day
- `day1.html` … `day10.html` — per-day itinerary pages (transit, food, sights)
- [`japan_trip_summary.html`](japan_trip_summary.html) — printable summary
- [`assets/`](assets/) — `app.js`, `routes.js`, `styles.css`, plus location photos
- [`build_routes.py`](build_routes.py) — regenerates `assets/routes.js` from source data
- [`DESIGN.md`](DESIGN.md) — design notes and visual system

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Regenerate routes

```sh
python3 build_routes.py
```

## Deployment

Deployed via GitHub Pages from the `main` branch root.
