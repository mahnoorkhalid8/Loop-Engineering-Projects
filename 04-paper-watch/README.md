# Project 4 — Paper Watch

**Heartbeat type:** scheduled, unattended, **with memory** (Concept 6 + Concept 12)
**What it teaches:** the spine. This is the project the whole "no spine, no
loop" lesson is built around — delete `progress.md` and the loop forgets
everything it has ever shown you.

## What's in this folder

```
04-paper-watch/
├── .claude/skills/paper-watch/SKILL.md
├── scripts/paper_watch.py       # fetches arXiv, dedupes against progress.md
├── scripts/run_and_log.ps1      # wrapper the scheduled task calls
├── progress.md                  # THE SPINE — created/updated by the script
└── logs/paper-watch.log
```

Data source: arXiv's public Atom API (`export.arxiv.org/api/query`). No
key, no auth, no rate-limit hassle for reasonable use.

## Proof it works (already run for you, three real runs)

```
=== RUN 1 (fresh, no progress.md) ===
Paper Watch - "LLM agents": 10 new paper(s):
  - [2609.17527v1] Agentic Societies Need a Social Harness
  - [2609.17523v1] ScienceBuddy: Recursive-in-Recursive Self-Improvement...
  ...

=== RUN 2 (same query, memory present) ===
Paper Watch - "LLM agents": nothing new since last run [OK]

=== DELETE progress.md, RUN 3 ===
Paper Watch - "LLM agents": 10 new paper(s):     <- same 10, all "new" again
  - [2609.17527v1] Agentic Societies Need a Social Harness
  ...
```

That middle-to-last transition is the whole concept in one command:
`rm progress.md` and the loop forgets every paper it has ever shown you.
No spine, no memory — full stop, not "degraded memory."

## How `progress.md` works as the spine

```markdown
# Paper Watch — memory (the spine)

## Already shown
- 2609.17527v1
- 2609.17523v1
...

## Log
- 2026-09-16 17:52 UTC: nothing new for "LLM agents"
- 2026-09-16 12:xx UTC: reported 10 new paper(s) for "LLM agents"
```

The script reads `## Already shown` at the start of every run and writes
to it at the end — exactly the read-first, write-last discipline from
Concept 12.

## Run it automatically — real Windows Scheduled Task, verified

```
Task name:  LoopEngineering-PaperWatch
Schedule:   daily at 8:15 AM
Action:     scripts/run_and_log.ps1 → logs/paper-watch.log
```

Fired once through Task Scheduler itself to prove it, not just by me
calling the script directly:

```
LastRunTime           LastTaskResult
16/09/2026 5:52:52 PM  0                     <- success
```

```
----- run at 2026-09-16 17:52:10 -----
Paper Watch - "LLM agents": nothing new since last run [OK]
```

Correctly says "nothing new" — because my manual test runs already logged
these papers into the spine before the scheduled task fired. That's not
a coincidence, that's the mechanism working.

**To check on it / remove it / change the time:** same commands as
Project 3, just with `-TaskName "LoopEngineering-PaperWatch"`.

```powershell
Get-Content "E:\Loop Engineering Projects\04-paper-watch\logs\paper-watch.log" -Tail 20
Unregister-ScheduledTask -TaskName "LoopEngineering-PaperWatch" -Confirm:$false
```

## How to run it via Claude Code instead

```
cd "E:\Loop Engineering Projects\04-paper-watch"
claude
show me what's new on arXiv about "LLM agents"
```

Ask the exact same thing again in the same session — it will say nothing
new. Then `rm progress.md` and ask a third time to watch it forget live.
To make it a real Routine: `/schedule every weekday at 9am, run the
paper-watch skill and show me what's new` (falls back to plain-language
scheduling instructions the same way Projects 2 and 3 do, if `/schedule`
isn't registered in your build).

## The concept, made concrete

| In the course | In this project |
|---|---|
| Spine | `progress.md`, read first, written last, every run |
| "No spine, no loop" | Proven by deleting it and watching full amnesia |
| Contrast with Project 3 | Sky Watch is *correctly* stateless; this one is *correctly* stateful — the difference is whether "new since last time" is a meaningful question |
