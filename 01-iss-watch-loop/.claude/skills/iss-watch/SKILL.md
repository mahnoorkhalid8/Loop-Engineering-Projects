---
name: iss-watch
description: >-
  Reports the current location of the International Space Station in plain
  English by running scripts/iss_location.py. Use this whenever the user
  asks where the ISS is, or asks to watch/track the ISS repeatedly.
---

# ISS Watch

1. Run `python scripts/iss_location.py` from the project root (use `python3`
   if `python` is not found).
2. Read its one-line output and repeat it back to the user in a friendly
   sentence — do not just paste the raw line. Mention position, altitude,
   speed, and whether the station is in daylight or night.
3. Do not explain how the script works unless asked. Just report the
   location.
