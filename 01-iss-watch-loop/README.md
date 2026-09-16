# Project 1 — Watch the Space Station

**Heartbeat type:** in-session `/loop` (Concept 4)
**What it teaches:** the cheapest possible heartbeat — a timer that lives inside
your open Claude Code session. Close the session, the loop dies. That's the
whole lesson.

## What's in this folder

```
01-iss-watch-loop/
├── .claude/skills/iss-watch/SKILL.md   # tells Claude how to answer "where is the ISS"
├── scripts/iss_location.py             # zero-dependency script, hits a public API
└── README.md
```

`scripts/iss_location.py` calls `https://api.wheretheiss.at/v1/satellites/25544`
(falls back to `api.open-notify.org` if that's unreachable) and prints one
plain-English line: position, altitude, speed, day/night.

## Proof it works (already run for you)

```
$ python scripts/iss_location.py
[12:14:04 UTC] ISS is at 46.31 deg S, 95.36 deg W, altitude 435 km, speed 27540 km/h, currently in daylight.
```

Real data, fetched live, no API key needed.

## How to run it yourself

1. Open a terminal in this folder:
   ```
   cd "E:\Loop Engineering Projects\01-iss-watch-loop"
   claude
   ```
2. Say yes when it asks whether you trust the folder (this is what lets the
   skill run without asking permission every time).
3. Type exactly one line:
   ```
   /loop show me the location of the ISS every minute
   ```
4. Watch a fresh position arrive every minute. Do something else in the
   meantime — that's the point.
5. To stop it cleanly:
   ```
   show my running loops
   cancel the iss loop
   ```
   or just close the terminal — the loop dies with the session (that's the
   concept, not a bug).

You can also skip the LLM entirely and watch it fire on its own with plain
Python — see "Run it automatically" below.

## Run it automatically (no Claude session required)

Because this loop needs nothing but a script and a clock, we can prove the
*mechanics* of "repeat every N seconds" without spending any tokens. This is
literally what `/loop` does under the hood: re-run a command on a timer.

PowerShell, repeats every 60s until you press Ctrl+C:
```powershell
while ($true) {
  python scripts\iss_location.py
  Start-Sleep -Seconds 60
}
```

Bash / Git Bash, same idea:
```bash
while true; do python scripts/iss_location.py; sleep 60; done
```

## The concept, made concrete

| In the course | In this project |
|---|---|
| Heartbeat | `/loop`'s internal timer, or the `while` loop above |
| "Repeats while you watch" | Close the terminal → the `while` loop / `/loop` both die |
| No spine needed | Each report stands alone; nothing is remembered between beats |

This is the only project in the course where "no memory" is correct by
design — contrast with Project 4 (Paper Watch), which breaks without one.
