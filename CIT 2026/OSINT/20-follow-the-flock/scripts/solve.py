# /// script
# requires-python = ">=3.11"
# ///
"""Forward-geocode 420 Orange Ave, West Haven — Photon matches OSM camera ~50m (see writeup.md)."""

from __future__ import annotations

import json
import math
import sys
import urllib.parse
import urllib.request

CAM_LAT, CAM_LON = 41.2909719, -72.9636546
FLAG = "CIT{420_Orange_Avenue_West_Haven_CT}"

QUERY = "420 Orange Avenue West Haven CT"


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def main() -> None:
    url = "https://photon.komoot.io/api?" + urllib.parse.urlencode(
        {"q": QUERY, "limit": 1},
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CIT-follow-the-flock-solve/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    feats = data.get("features") or []
    if not feats:
        print("photon: empty", file=sys.stderr)
        sys.exit(1)
    f0 = feats[0]
    p = f0.get("properties", {})
    geom = f0.get("geometry") or {}
    coords = geom.get("coordinates") or [0, 0]
    lon, lat = float(coords[0]), float(coords[1])
    print(
        f"photon: housenumber={p.get('housenumber')!r} street={p.get('street')!r} "
        f"city={p.get('city')!r} state={p.get('state')!r}",
        file=sys.stderr,
    )
    if p.get("housenumber") != "420":
        print("unexpected housenumber (expected 420)", file=sys.stderr)
        sys.exit(1)
    if p.get("street") != "Orange Avenue":
        print("unexpected street (expected Orange Avenue)", file=sys.stderr)
        sys.exit(1)
    if p.get("city") != "West Haven":
        print("unexpected city (expected West Haven)", file=sys.stderr)
        sys.exit(1)
    if p.get("state") != "CT":
        print("unexpected state (expected CT)", file=sys.stderr)
        sys.exit(1)
    dist = _haversine_m(CAM_LAT, CAM_LON, lat, lon)
    print(f"photon: distance to OSM camera node: {dist:.0f}m", file=sys.stderr)
    if dist > 120:
        print("hit too far from camera node", file=sys.stderr)
        sys.exit(1)
    print(FLAG)


if __name__ == "__main__":
    main()
