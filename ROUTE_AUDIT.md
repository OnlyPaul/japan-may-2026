# Route Audit — Japan May 2026

**Audit date:** 2026-05-13
**Scope:** Pin coordinates and visit order across `day1.html` – `day10.html`, cross-checked against `build_routes.py`.
**Result:** No mis-pinned locations. All issues found are ordering / routing, not bad coordinates.

## Per-day verdict

| Day | Theme | Status |
|-----|-------|--------|
| 1   | Bangkok → Narita departure | OK |
| 2   | Arrival → Fuji north (Kawaguchiko area) | OK |
| 3   | Fuji west loop | Minor (single swap fixes it) |
| 4   | Hakone → Tokyo (Ikebukuro) | OK |
| 5   | Old Tokyo (Yanaka → Ueno → Akihabara) | OK (cleanest day) |
| 6   | Kamakura | OK |
| 7   | Tokyo Bay & markets | Minor |
| 8   | Marunouchi + Ginza | Mild zig-zag |
| 9   | West Tokyo (Shinjuku / Harajuku / Shibuya) | **Significant detour** |
| 10  | Tokyo → Narita → Bangkok | OK |

---

## Day 3 — Fuji west loop (minor)

Current order: Hotel Mifujien → **Chureito Pagoda** → Tenku-no Torii → Lake Saiko → Lake Tanuki → Fujinomiya yakisoba → Shiraito Falls → Sengen Taisha → Mifujien.

**Chureito first is correct.** The pagoda-with-Fuji shot wants morning light (clearer air, less afternoon haze) and pre-crowd timing, so the ~45 km drive north from Mifujien is a deliberate anchor, not a wasted detour. Moving Chureito to Day 2 isn't viable — Day 2 is already a packed jetlagged arrival day (Narita → rental → 2.5 h drive → Yamanaka → Oshino → Oishi Park → hotel).

**The actual fix is a single swap.** Northern stops in east-to-west longitude order: Chureito (138.80) > Saiko (138.68) > Tenku-no Torii (138.60) > Tanuki (138.57). The current sequence Chureito → Tenku → Saiko → Tanuki goes E → W → middle → W, which means a small backtrack east from Tenku to Saiko before heading west again. Swapping Tenku-no Torii and Lake Saiko gives Chureito → Saiko → Tenku → Tanuki = E → middle → W → W, monotonic east-to-west across the north side before the southern leg.

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
