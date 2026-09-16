#!/usr/bin/env python3
"""Sky Watch: reports near-Earth asteroid passes for a given day (default:
today, UTC) in plain English. Stdlib only. Uses NASA's public NeoWs API.

Set NASA_API_KEY to your own free key from https://api.nasa.gov for higher
rate limits (DEMO_KEY works but is capped at 30 requests/hour, 50/day).

This is a *scheduled* loop with no memory: every run reports the whole day
fresh, on purpose. Running it twice in one day should print the same
report both times (modulo NASA revising its data) -- that's correct
behaviour for a "watch", not a bug. Contrast with Paper Watch (Project 4),
which must NOT repeat itself and therefore needs a spine.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

API_BASE = "https://api.nasa.gov/neo/rest/v1/feed"


def fetch(date_str: str, api_key: str) -> dict:
    url = f"{API_BASE}?start_date={date_str}&end_date={date_str}&api_key={api_key}"
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.loads(resp.read().decode())


def lunar_distance_desc(miss_km: float) -> str:
    LUNAR_KM = 384_400
    ld = miss_km / LUNAR_KM
    return f"{ld:.1f}x the distance to the Moon"


def main() -> None:
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")

    try:
        data = fetch(date_str, api_key)
    except urllib.error.HTTPError as e:
        print(f"[sky-watch] NASA API error for {date_str}: HTTP {e.code}. "
              f"If this is a 429, you've hit the DEMO_KEY rate limit -- get "
              f"a free key at https://api.nasa.gov and set NASA_API_KEY.")
        sys.exit(1)
    except Exception as e:
        print(f"[sky-watch] Could not reach NASA's API for {date_str}: {e}")
        sys.exit(1)

    objects = data.get("near_earth_objects", {}).get(date_str, [])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not objects:
        print(f"[{now}] Sky Watch for {date_str}: no tracked close approaches today. All clear.")
        return

    objects_sorted = sorted(
        objects,
        key=lambda o: float(o["close_approach_data"][0]["miss_distance"]["kilometers"]),
    )

    hazardous = [o for o in objects_sorted if o["is_potentially_hazardous_asteroid"]]

    print(f"[{now}] Sky Watch for {date_str}: {len(objects)} tracked object(s) passing today.")
    if hazardous:
        print(f"  ⚠ {len(hazardous)} flagged as potentially hazardous by NASA's size/distance criteria.")
    else:
        print("  Nothing flagged as potentially hazardous. All clear.")

    print()
    closest = objects_sorted[0]
    cad = closest["close_approach_data"][0]
    miss_km = float(cad["miss_distance"]["kilometers"])
    diam = closest["estimated_diameter"]["meters"]
    speed_kmh = float(cad["relative_velocity"]["kilometers_per_hour"])
    print(
        f"Closest pass: {closest['name']} -- {lunar_distance_desc(miss_km)}, "
        f"estimated {diam['estimated_diameter_min']:.0f}-{diam['estimated_diameter_max']:.0f}m "
        f"across, at {speed_kmh:.0f} km/h."
    )

    if len(objects_sorted) > 1:
        print(f"\n...and {len(objects_sorted) - 1} more, in order of distance:")
        for o in objects_sorted[1:6]:
            cad = o["close_approach_data"][0]
            miss_km = float(cad["miss_distance"]["kilometers"])
            flag = " [potentially hazardous]" if o["is_potentially_hazardous_asteroid"] else ""
            print(f"  - {o['name']}: {lunar_distance_desc(miss_km)}{flag}")
        if len(objects_sorted) > 6:
            print(f"  ...and {len(objects_sorted) - 6} more not shown.")


if __name__ == "__main__":
    main()
