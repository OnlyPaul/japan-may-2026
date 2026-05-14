#!/usr/bin/env python3
"""Fetch real OSRM polylines for every ground segment + compute great-circle for flights.
Writes assets/routes.js with embedded polylines.

Run once locally. Not used at runtime.
"""
import json
import math
import time
import urllib.request
from urllib.parse import quote

OSRM = "http://router.project-osrm.org/route/v1/driving"

# ---- Per-day waypoints + segments ------------------------------------------------
# Each segment: (from_idx, to_idx, mode) where mode in {ground, transit, flight}

DAYS = {
    "day1": {
        "center": [13.69, 100.75], "zoom": 6,
        "points": [
            {"n":1, "lat":13.7563, "lng":100.5018, "label":"Car Hub Bangkok",        "time":"Day"},
            {"n":2, "lat":13.6900, "lng":100.7501, "label":"Suvarnabhumi (BKK)",     "time":"20:00"},
            {"n":3, "lat":35.7647, "lng":140.3863, "label":"Narita (NRT) — overnight","time":"23:35 dep"},
        ],
        "segments": [(1,2,"ground"), (2,3,"flight")],
    },
    "day2": {
        "center": [35.470, 138.770], "zoom": 10,
        "points": [
            {"n":1, "lat":35.7647, "lng":140.3863, "label":"Narita Airport — land","time":"07:45"},
            {"n":2, "lat":35.7693, "lng":140.3922, "label":"Nippon Rent-a-Car (NRT)","time":"~09:30"},
            {"n":3, "lat":35.4186, "lng":138.8775, "label":"Lake Yamanaka","time":"~12:00"},
            {"n":4, "lat":35.4601, "lng":138.8325, "label":"Oshino Hakkai","time":"13:00"},
            {"n":5, "lat":35.5229, "lng":138.7458, "label":"Fuji Oishi Park","time":"16:00"},
            {"n":6, "lat":35.4986, "lng":138.7672, "label":"Lawson Kawaguchiko","time":"~17:15"},
            {"n":7, "lat":35.4947, "lng":138.7761, "label":"Fujikawaguchiko Resort Hotel","time":"~17:30"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground"),(6,7,"ground")],
    },
    "day3": {
        "center": [35.380, 138.700], "zoom": 10,
        "points": [
            {"n":1, "lat":35.4947, "lng":138.7761, "label":"Fujikawaguchiko Resort Hotel","time":"~07:00"},
            {"n":2, "lat":35.5014, "lng":138.8016, "label":"Chureito Pagoda","time":"~07:30"},
            {"n":3, "lat":35.5309, "lng":138.7745, "label":"Tenku-no Torii (Kawaguchi Asama Shrine)","time":"10:00"},
            {"n":4, "lat":35.4991, "lng":138.6865, "label":"Lake Saiko","time":"11:00"},
            {"n":5, "lat":35.3437, "lng":138.5606, "label":"Lake Tanuki","time":"11:45"},
            {"n":6, "lat":35.2248, "lng":138.6101, "label":"Fujinomiya yakisoba","time":"13:00"},
            {"n":7, "lat":35.2275, "lng":138.6100, "label":"Fujisan Hongu Sengen Taisha","time":"14:00"},
            {"n":8, "lat":35.3129, "lng":138.5874, "label":"Shiraito Falls","time":"15:00"},
            {"n":9, "lat":35.5129, "lng":138.7741, "label":"Hotel Mifujien","time":"Evening"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground"),(6,7,"ground"),(7,8,"ground"),(8,9,"ground")],
    },
    "day4": {
        "center": [35.470, 139.350], "zoom": 10,
        "points": [
            {"n":1, "lat":35.5129, "lng":138.7741, "label":"Hotel Mifujien (depart)","time":"~09:00"},
            {"n":2, "lat":35.2436, "lng":139.0197, "label":"Owakudani","time":"10:00"},
            {"n":3, "lat":35.2028, "lng":139.0257, "label":"Lake Ashi · Hakone Shrine torii","time":"13:00"},
            {"n":4, "lat":35.7281, "lng":139.7086, "label":"Nippon Ikebukuro West Exit","time":"~18:30"},
            {"n":5, "lat":35.7300, "lng":139.7115, "label":"Tokyu Stay Ikebukuro","time":"Evening"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground")],
    },
    "day5": {
        "center": [35.720, 139.770], "zoom": 14,
        "points": [
            {"n":1, "lat":35.7270, "lng":139.7676, "label":"Yanaka Ginza","time":"Morning"},
            {"n":2, "lat":35.7202, "lng":139.7619, "label":"Yuyake Dandan","time":"Morning"},
            {"n":3, "lat":35.7203, "lng":139.7614, "label":"Nezu Shrine","time":"Late AM"},
            {"n":4, "lat":35.7222, "lng":139.7611, "label":"Kamachiku (udon)","time":"Lunch"},
            {"n":5, "lat":35.7156, "lng":139.7745, "label":"Ueno Park","time":"Afternoon"},
            {"n":6, "lat":35.7075, "lng":139.7745, "label":"Ameya-Yokocho","time":"Afternoon"},
            {"n":7, "lat":35.6975, "lng":139.7731, "label":"Akihabara · 2k540","time":"Evening"},
            {"n":8, "lat":35.6985, "lng":139.7731, "label":"Tonkatsu Marugo","time":"Dinner"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground"),(6,7,"ground"),(7,8,"ground")],
    },
    "day6": {
        "center": [35.318, 139.546], "zoom": 13,
        "points": [
            {"n":1, "lat":35.7300, "lng":139.7115, "label":"Ikebukuro (depart)","time":"Morning"},
            {"n":2, "lat":35.3192, "lng":139.5468, "label":"Kamakura Station","time":"Morning"},
            {"n":3, "lat":35.3169, "lng":139.5359, "label":"Hase Station (Enoden)","time":"Morning"},
            {"n":4, "lat":35.3169, "lng":139.5358, "label":"Great Buddha (Kotoku-in)","time":"Morning"},
            {"n":5, "lat":35.3122, "lng":139.5358, "label":"Hasedera Temple","time":"Morning"},
            {"n":6, "lat":35.3148, "lng":139.5363, "label":"Akatsuki (reserved lunch)","time":"Lunch"},
            {"n":7, "lat":35.3211, "lng":139.5519, "label":"Komachi-dori","time":"Afternoon"},
            {"n":8, "lat":35.3050, "lng":139.5290, "label":"Shichirigahama Beach","time":"Afternoon"},
        ],
        "segments": [(1,2,"transit"),(2,3,"transit"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground"),(6,7,"ground"),(7,8,"ground")],
    },
    "day7": {
        "center": [35.650, 139.780], "zoom": 13,
        "points": [
            {"n":1, "lat":35.6655, "lng":139.7707, "label":"Tsukiji Outer Market","time":"Early AM"},
            {"n":2, "lat":35.6450, "lng":139.7787, "label":"Toyosu Market","time":"Late AM"},
            {"n":3, "lat":35.6478, "lng":139.7872, "label":"teamLab Planets Toyosu","time":"Afternoon"},
            {"n":4, "lat":35.6256, "lng":139.7755, "label":"Odaiba · DiverCity Gundam","time":"Late PM"},
            {"n":5, "lat":35.6363, "lng":139.7637, "label":"Rainbow Bridge","time":"Late PM"},
            {"n":6, "lat":35.6256, "lng":139.7755, "label":"Daiba Itchome Shotengai","time":"Dinner"},
        ],
        "segments": [(1,2,"transit"),(2,3,"ground"),(3,4,"transit"),(4,5,"ground"),(5,6,"ground")],
    },
    "day8": {
        "center": [35.668, 139.760], "zoom": 14,
        "points": [
            {"n":1, "lat":35.6603, "lng":139.7637, "label":"Hamarikyu Gardens","time":"Morning"},
            {"n":2, "lat":35.6812, "lng":139.7671, "label":"Tokyo Station (red brick)","time":"Late AM"},
            {"n":3, "lat":35.6800, "lng":139.7651, "label":"Kitte Garden 6F rooftop","time":"Late AM"},
            {"n":4, "lat":35.6717, "lng":139.7657, "label":"Ginza · Itoya · Ginza Six","time":"Afternoon"},
            {"n":5, "lat":35.6586, "lng":139.7454, "label":"Zojoji + Tokyo Tower","time":"~18:00"},
            {"n":6, "lat":35.6712, "lng":139.7656, "label":"Toritama Ginza","time":"Dinner"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground")],
    },
    "day9": {
        "center": [35.680, 139.700], "zoom": 13,
        "points": [
            {"n":1, "lat":35.6852, "lng":139.7100, "label":"Shinjuku Gyoen","time":"Morning"},
            {"n":2, "lat":35.6710, "lng":139.7050, "label":"Takeshita-dori","time":"Late AM"},
            {"n":3, "lat":35.6660, "lng":139.7115, "label":"Onodera Honten","time":"Lunch"},
            {"n":4, "lat":35.6648, "lng":139.7011, "label":"Cat Street walk","time":"Afternoon"},
            {"n":5, "lat":35.6595, "lng":139.7004, "label":"Shibuya Crossing · Hachiko","time":"Late PM"},
            {"n":6, "lat":35.6595, "lng":139.7036, "label":"Shibuya Hikarie 11F","time":"Late PM"},
            {"n":7, "lat":35.6896, "lng":139.6917, "label":"Tocho Observation Deck","time":"Evening"},
        ],
        "segments": [(1,2,"ground"),(2,3,"ground"),(3,4,"ground"),(4,5,"ground"),(5,6,"ground"),(6,7,"transit")],
    },
    "day10": {
        "center": [35.730, 140.080], "zoom": 6,
        "points": [
            {"n":1, "lat":35.7300, "lng":139.7115, "label":"Tokyu Stay Ikebukuro","time":"~10:30"},
            {"n":2, "lat":35.6812, "lng":139.7671, "label":"Tokyo Station (ekiben)","time":"AM"},
            {"n":3, "lat":35.7647, "lng":140.3863, "label":"Narita Airport (N'EX)","time":"13:30"},
            {"n":4, "lat":13.6900, "lng":100.7501, "label":"BKK — home 22:15","time":"17:30 dep"},
        ],
        "segments": [(1,2,"transit"),(2,3,"transit"),(3,4,"flight")],
    },
}

def fetch_osrm(p1, p2):
    """Return list of [lat, lng] following real roads."""
    url = f"{OSRM}/{p1['lng']},{p1['lat']};{p2['lng']},{p2['lat']}?overview=simplified&geometries=geojson"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = json.loads(r.read())
        if data.get("code") != "Ok":
            print("  WARN osrm code:", data.get("code"), "for", p1["label"], "->", p2["label"])
            return [[p1["lat"], p1["lng"]], [p2["lat"], p2["lng"]]]
        coords = data["routes"][0]["geometry"]["coordinates"]
        # GeoJSON is [lng, lat], we want [lat, lng] for Leaflet
        return [[c[1], c[0]] for c in coords]
    except Exception as e:
        print("  ERR osrm:", e)
        return [[p1["lat"], p1["lng"]], [p2["lat"], p2["lng"]]]

def great_circle(p1, p2, n=40):
    """Interpolate n points along the great-circle from p1 to p2. [lat, lng] output."""
    lat1, lon1 = math.radians(p1["lat"]), math.radians(p1["lng"])
    lat2, lon2 = math.radians(p2["lat"]), math.radians(p2["lng"])
    d = 2 * math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2))
    out = []
    for i in range(n+1):
        f = i / n
        A = math.sin((1-f)*d) / math.sin(d)
        B = math.sin(f*d) / math.sin(d)
        x = A*math.cos(lat1)*math.cos(lon1) + B*math.cos(lat2)*math.cos(lon2)
        y = A*math.cos(lat1)*math.sin(lon1) + B*math.cos(lat2)*math.sin(lon2)
        z = A*math.sin(lat1) + B*math.sin(lat2)
        lat = math.atan2(z, math.sqrt(x*x + y*y))
        lon = math.atan2(y, x)
        out.append([math.degrees(lat), math.degrees(lon)])
    return out

# ---- Process all days -----------------------------------------------------------
result = {}
for day_key, day in DAYS.items():
    print(f"\n== {day_key} ==")
    polylines = []
    points_by_n = {p["n"]: p for p in day["points"]}
    for (a, b, mode) in day["segments"]:
        p1 = points_by_n[a]; p2 = points_by_n[b]
        if mode == "ground":
            print(f"  ground {a}->{b}  {p1['label']} -> {p2['label']}")
            line = fetch_osrm(p1, p2)
            time.sleep(0.2)  # be nice to demo server
        elif mode == "flight":
            print(f"  flight {a}->{b}  {p1['label']} -> {p2['label']}")
            line = great_circle(p1, p2, n=40)
        else:  # transit
            print(f"  transit {a}->{b}  {p1['label']} -> {p2['label']}")
            line = [[p1["lat"], p1["lng"]], [p2["lat"], p2["lng"]]]
        polylines.append({"from": a, "to": b, "mode": mode, "coords": line})
    result[day_key] = {
        "center": day["center"],
        "zoom": day["zoom"],
        "points": day["points"],
        "polylines": polylines,
    }

# Write routes.js
body = "window.ROUTES = " + json.dumps(result, indent=2, ensure_ascii=False) + ";\n"
with open("assets/routes.js", "w") as f:
    f.write("/* Auto-generated from build_routes.py — OSRM polylines + great-circle flights */\n")
    f.write(body)

print("\nWrote assets/routes.js")
