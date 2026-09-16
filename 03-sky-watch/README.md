# Project 3 — The Sky Watch

**Heartbeat type:** scheduled, unattended (Concept 6)
**What it teaches:** the heartbeat that runs while your laptop is asleep,
and the one honest exception to "always add a spine" — this loop is
*correct* to have no memory, because it reports the whole day fresh every
time.

## What's in this folder

```
03-sky-watch/
├── .claude/skills/sky-watch/SKILL.md   # Claude-facing wrapper (plain-English report)
├── scripts/sky_watch.py                # zero-dependency script, hits NASA's public API
├── scripts/run_and_log.ps1             # wrapper the scheduled task actually calls
└── logs/sky-watch.log                  # append-only run log
```

Data source: NASA's NeoWs (Near Earth Object Web Service),
`https://api.nasa.gov/neo/rest/v1/feed`. Works out of the box with the
public `DEMO_KEY` (rate-limited to 30 req/hr, 50/day). For heavier use,
get a free key at https://api.nasa.gov and set `NASA_API_KEY`.

## Proof it works (already run for you, live data)

```
$ python scripts/sky_watch.py
[2026-09-16 12:42 UTC] Sky Watch for 2026-09-16: 8 tracked object(s) passing today.
  Nothing flagged as potentially hazardous. All clear.

Closest pass: (2007 QE3) -- 34.6x the distance to the Moon, estimated 267-597m across, at 65481 km/h.

...and 7 more, in order of distance:
  - (2007 GU4): 54.4x the distance to the Moon
  ...
```

Real NASA tracking data for today, fetched live.

## Run it automatically — this one is *actually* scheduled, right now

Unlike Projects 1 and 2, this loop needs no LLM and no credentials beyond
the public API key, so I registered a **real Windows Scheduled Task** on
this machine:

```
Task name:  LoopEngineering-SkyWatch
Schedule:   daily at 8:00 AM
Action:     scripts/run_and_log.ps1  →  appends to logs/sky-watch.log
```

I proved it end-to-end, not just by running the script directly, but by
firing it *through Task Scheduler itself*:

```
Start-ScheduledTask -TaskName "LoopEngineering-SkyWatch"
...
LastRunTime           LastTaskResult
16/09/2026 5:46:46 PM  0                    <- 0 = success
```

`logs/sky-watch.log` now has two independent run entries — one from me
calling the script directly, one from Task Scheduler firing it on its
own. That second entry is the actual proof: nothing I typed ran it: the
OS did.

**To check on it yourself:**
```powershell
Get-ScheduledTask -TaskName "LoopEngineering-SkyWatch" | Get-ScheduledTaskInfo
Get-Content "E:\Loop Engineering Projects\03-sky-watch\logs\sky-watch.log" -Tail 20
```

**To remove it** (it will otherwise run every day at 8am indefinitely):
```powershell
Unregister-ScheduledTask -TaskName "LoopEngineering-SkyWatch" -Confirm:$false
```

**To change the time:**
```powershell
Set-ScheduledTask -TaskName "LoopEngineering-SkyWatch" -Trigger (New-ScheduledTaskTrigger -Daily -At 7:30AM)
```

## How to run it via Claude Code instead (the course's intended path)

The course teaches this through Claude Code's own `/schedule` (or a cloud
Routine). If your CLI build has it:

```
cd "E:\Loop Engineering Projects\03-sky-watch"
claude
/schedule every day at 8am, run the sky-watch skill and write me the forecast
```

If `/schedule` isn't registered in your build (same caveat as `/goal` in
Project 2), the Windows Scheduled Task above achieves the identical
result — this is exactly the point made in Concept 3 and Concept 6: a
heartbeat is a heartbeat, whether it's a managed Routine, `/schedule`, or
one line in cron/Task Scheduler.

## Why this loop is allowed to have no spine

Every other scheduled project in this series (4, 8, 11, 12) reads and
writes a memory file. This one deliberately doesn't, and that's correct:
the report always covers *today*, so running it twice in a row should
print the same thing (modulo NASA revising its own data) — there's
nothing to "remember," because there's no notion of "new since last time."
Compare this directly with Project 4 (Paper Watch), which breaks without
memory, to feel the difference.

## The concept, made concrete

| In the course | In this project |
|---|---|
| Heartbeat | Windows Scheduled Task, daily at 8am (stand-in for a Routine / `/schedule`) |
| "Runs while you sleep" | Proven: fired through Task Scheduler, not through me |
| Log / observability | `logs/sky-watch.log`, append-only, one entry per run |
| No spine needed | The report is stateless by design — see above |
