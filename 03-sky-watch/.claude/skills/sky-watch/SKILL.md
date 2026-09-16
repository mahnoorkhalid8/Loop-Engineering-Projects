---
name: sky-watch
description: >-
  Reports today's near-Earth asteroid passes in plain English by running
  scripts/sky_watch.py. Use whenever the user asks what's passing Earth
  today/this week, or asks to watch/track asteroids.
---

# Sky Watch

1. Run `python scripts/sky_watch.py` from the project root (pass a
   `YYYY-MM-DD` argument for a specific day; default is today, UTC).
2. Turn the output into a short, calm forecast — most days it's "nothing
   to worry about." Only sound alarmed if something is actually flagged
   `is_potentially_hazardous_asteroid`.
3. Always report the day it ran for, not a stale earlier day. A daily
   scheduled run should describe *today*, so tomorrow's run says something
   different, not the same cached sentence.
4. This loop needs no memory between runs — reporting the same "all clear"
   every morning is correct, not a bug.
