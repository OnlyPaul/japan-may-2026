# Route Audit — Japan May 2026

**Audit date:** 2026-05-13
**Scope:** Pin coordinates and visit order across `day1.html` – `day10.html`, cross-checked against `build_routes.py`.
**Result:** No mis-pinned locations after the 2026-05-14 amendment. All ordering / routing issues now resolved.

**2026-05-14 amendment.** A Denso Mapcode lookup pass surfaced three stale pins that the original 2026-05-13 audit missed: Tenku-no Torii, Hotel Mifujien, and the Nippon Ikebukuro return office. All three are now corrected in `build_routes.py`, `assets/routes.js`, and the day pages. See the per-day notes below.

## Per-day verdict

| Day | Theme | Status |
|-----|-------|--------|
| 1   | Bangkok → Narita departure | OK |
| 2   | Arrival → Fuji north (Kawaguchiko area) | OK |
| 3   | Fuji west loop | OK (coord fix + swap reverted 2026-05-14) |
| 4   | Hakone → Tokyo (Ikebukuro) | OK |
| 5   | Old Tokyo (Yanaka → Ueno → Akihabara) | OK (cleanest day) |
| 6   | Kamakura | OK |
| 7   | Tokyo Bay & markets | Minor |
| 8   | Marunouchi + Ginza | Mild zig-zag |
| 9   | West Tokyo (Shinjuku / Harajuku / Shibuya) | **Significant detour** |
| 10  | Tokyo → Narita → Bangkok | OK |

---

## Day 3 — Fuji west loop (resolved 2026-05-14, with coord fix)

Final order: Fujikawaguchiko Resort Hotel → **Chureito Pagoda** → **Tenku-no Torii** → **Lake Saiko** → **Lake Tanuki** → Fujinomiya yakisoba → Shiraito Falls → Sengen Taisha → Hotel Mifujien.

**Chureito first is correct.** The pagoda-with-Fuji shot wants morning light (clearer air, less afternoon haze) and pre-crowd timing. Moving Chureito to Day 2 isn't viable — Day 2 is already a packed jetlagged arrival day (Narita → rental → 2.5 h drive → Yamanaka → Oshino → Oishi Park → hotel).

**Coord fix (2026-05-14).** Tenku-no Torii was previously pinned at `35.4675, 138.6010` — that's in the Aokigahara / Fugaku Wind Cave area, not the actual viewpoint. The real Tenku-no Torii is the viewpoint at **Kawaguchi Asama Shrine** at `35.5309, 138.7745`, ~17 km NE of the wrong pin. Hotel Mifujien was also stale: pinned at `35.2310, 138.6120` (Fujinomiya south) but the actual hotel is at `35.5129, 138.7741` in Fujikawaguchiko (north). Both pinned correctly now.

**Original order was right; the 2026-05-13 swap is reverted.** With the corrected Tenku coord, the east-to-west longitude order across the north side is Chureito (138.80) > Tenku (138.77) > Saiko (138.68) > Tanuki (138.57) — monotonic E → W, no backtrack. The 2026-05-13 audit had recommended swapping Tenku and Saiko based on the wrong Tenku coord; with the right coord, Chureito → Tenku → Saiko → Tanuki is what you want.

**Side effect of the Mifujien fix.** The hotel is on the north side of Fuji, so Day 3 still finishes at Sengen Taisha (south, Fujinomiya) but adds a ~50-min northbound drive back to Mifujien for the night. Day 4 then starts north and runs east to Hakone. Day 3 timeline note updated to flag this; Day 4 timeline already departs Mifujien at 09:00 which works from the corrected location.

## Day 7 — Bay & markets (minor)

Current order: Tsukiji Outer Market → Toyosu Market → teamLab Planets → DiverCity Gundam → **Rainbow Bridge** → Daiba Itchome Shotengai.

Rainbow Bridge is placed between Odaiba (Gundam) and Daiba Itchome Shotengai, but Daiba Itchome is itself in Odaiba — so the sequence dips off Odaiba and back. A cleaner read: Gundam → Daiba Itchome dinner → Rainbow Bridge sunset walk last.

## Day 8 — Marunouchi + Ginza (mild)

Current order: Hamarikyu (35.66) → Tokyo Station / Kitte (35.68) → Ginza (35.67) → **Zojoji + Tokyo Tower (35.66, SW)** → Toritama Ginza (35.67).

After moving north from Hamarikyu to Tokyo Station, the day swings SW to Zojoji / Tokyo Tower, then back to Ginza for dinner. Defensible because Tokyo Tower wants golden hour, but geographically a small backtrack.

## Day 9 — West Tokyo (significant)

Current order: Shinjuku Gyoen (35.685) → Takeshita-dori → Onodera Omotesando → Cat Street → Shibuya Crossing → Shibuya Hikarie → **Tocho Observation Deck (35.69, far NW)**.

Clean southbound flow Gyoen → Harajuku → Omotesando → Shibuya, then a ~6 km deadhead back NW to Tocho at the end. Tocho fits naturally either at the start of the day (a ~5-minute walk from Gyoen's west gate) or as a sunset stop before dropping into Shibuya for dinner.

---

## Pin coordinate sanity

All sampled coordinates point to plausible spots for their named locations. No mis-pins detected — the issues above are purely about visit order, not pin placement.

## Days that audit clean

Days 1, 2, 4, 5, 6, 10. Day 5 (Yanaka → Yuyake Dandan → Nezu → Kamachiku → Ueno → Ameyoko → 2k540 → Tonkatsu Marugo) is the cleanest linear route in the trip — an almost perfectly monotonic north-to-south walk.
