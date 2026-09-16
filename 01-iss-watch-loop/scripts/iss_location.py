#!/usr/bin/env python3
"""Fetch the current location of the International Space Station and print
a plain-English one-line report. No API key, no third-party packages."""

import json
import urllib.request
from datetime import datetime, timezone

PRIMARY = "https://api.wheretheiss.at/v1/satellites/25544"
FALLBACK = "http://api.open-notify.org/iss-now.json"


def fetch(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode())


def hemisphere_desc(lat: float, lon: float) -> str:
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{abs(lat):.2f} deg {ns}, {abs(lon):.2f} deg {ew}"


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    try:
        data = fetch(PRIMARY)
        pos = hemisphere_desc(data["latitude"], data["longitude"])
        alt = data["altitude"]
        vel = data["velocity"]
        vis = data["visibility"]
        print(
            f"[{now}] ISS is at {pos}, altitude {alt:.0f} km, "
            f"speed {vel:.0f} km/h, currently in {vis}."
        )
    except Exception:
        data = fetch(FALLBACK)
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        pos = hemisphere_desc(lat, lon)
        print(f"[{now}] ISS is at {pos}. (fallback source, limited detail)")


if __name__ == "__main__":
    main()
