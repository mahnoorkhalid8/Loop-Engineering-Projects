# Project 9 — Routine Drill: Basic Cloud Routine Setup

**Concept:** Appendix A1–A2, A6 — the fields of a real cloud Routine, and
a pre-flight checklist before you save one.

## Why this project looks different from 1–8

A cloud Routine runs on Anthropic's servers, tied to *your* claude.ai
account. I have no account to create one on, so I can't click "Save" for
you. What I built instead is the part that's genuinely yours to get
right regardless of who clicks the button: **a well-formed prompt, and an
automated check that it's actually ready** — because a bad prompt is the
single most common way a Routine wastes its first unattended run.

## What's in this folder

```
09-routine-drill-basic/
├── routine-prompt.md   # a real, complete prompt for an issue-triage Routine
├── checklist.py         # automates what Appendix A6's checklist can prove from text
└── bad-prompt.txt        # a deliberately weak prompt, for contrast (created by the test run)
```

## Proof: the checker actually discriminates

```
$ python checklist.py routine-prompt.md
[PASS] defines what 'done' looks like even for the empty case
[PASS] has an explicit limit (max items / stop condition)
[PASS] has at least one explicit boundary ('do not ...')
[PASS] names where output goes (a connector target)
[PASS] doesn't rely on missing prior context
[PASS] is substantial enough to be self-contained
[PASS] time-bounds the work it looks at
7/7

$ echo "check the issues and let me know if anything looks important" > bad-prompt.txt
$ python checklist.py bad-prompt.txt
[FAIL] defines what 'done' looks like even for the empty case
[FAIL] has an explicit limit (max items / stop condition)
[FAIL] has at least one explicit boundary ('do not ...')
[FAIL] names where output goes (a connector target)
[PASS] doesn't rely on missing prior context
[FAIL] is substantial enough to be self-contained
[FAIL] time-bounds the work it looks at
1/7
```

The bad prompt is exactly the kind of thing people paste into a Routine
form and walk away from — it reads fine to a human but gives an
unattended agent no stopping condition, no scope, and no idea where to
report. This is Concept 5's "the loop is only as good as its stopping
condition" applied to the Routine form specifically.

## The four fields, filled in for real (Appendix A2)

| Field | Value |
|---|---|
| **Prompt** | `routine-prompt.md` (7/7 on the checklist above) |
| **Repositories** | the one repo this triages — leave "Allow unrestricted branch pushes" **off** |
| **Connectors** | Slack only (the prompt posts to `#triage` and nothing else) — remove every other connector your account has linked |
| **Trigger** | Schedule, weekdays at 8:30am, so the summary is ready before standup |

## How to actually create it

1. Go to `claude.ai/code/routines` (or Desktop app → Routines → New
   routine → **Remote** — not Local, see the course's Appendix A1 on why
   that distinction matters), or use `/schedule` in the CLI if your build
   has it.
2. Paste `routine-prompt.md` as the prompt.
3. Fill in the repo/connector/trigger fields from the table above.
4. **Before saving:** re-run `python checklist.py routine-prompt.md` if
   you changed the prompt, then walk the four manual items the script
   prints at the bottom (repo scope, connector trim, secrets location,
   one-off test run).
5. Fire it once with "Run now" (or a one-off `/schedule in 2 minutes...`)
   before trusting the recurring schedule — one-off runs don't count
   against your daily cap, so there's no cost to testing first.

## Run it automatically

The checker itself is real and I ran it against both a good and bad
prompt above — that's the part of this drill that's actually executable
without your account. The Routine itself can't be created or fired by
me; § "How to actually create it" is the part that's yours.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "A routine is a saved configuration: prompt + repos + env + connectors + trigger" | The four-field table above |
| Pre-flight checklist (Appendix A6) | `checklist.py`, the checkable half of it, run for real |
| "A bad prompt wastes the first unattended run" | The 1/7 result on `bad-prompt.txt` |
