# Project 12 — Weekly Capstone: the Dreaming / Improvement Loop

**Concept:** Concept 12's interlude — "dreaming." Not a new heartbeat
shape, but the six-part loop pointed at *itself*: instead of fixing code,
this loop reads what other loops did, finds a mistake that keeps
repeating, and proposes a rule to stop it — as a PR only a human can
merge. This is the last, and most powerful, loop in the whole series,
which is exactly why it's the one built to never run without its gate.

## Why this project needed synthetic history (and why that's disclosed, not hidden)

The course is explicit about this limit: *"a dream needs material... a
loop with three runs of history has no patterns to find."* Project 8 has
only actually run twice in this session — nowhere near enough real
history for a genuine pattern to emerge. Rather than fake a "finding"
from insufficient data (which the course specifically warns produces
"plausible-sounding lessons from noise"), I built **7 nights of clearly
synthetic run logs** (`logs/run-2026-09-10.md` … `run-2026-09-16.md`),
seeded with one deliberate, realistic recurring problem, so the pattern
detection itself could be proven against real, working code instead of
narrated. Everything downstream of those logs — the counting, the
threshold, the branch, the commit, the merge — is genuine, not staged.

## What's in this folder

```
12-dreaming-capstone/
├── logs/run-2026-09-*.md     # a week of (synthetic) nightly triage-run summaries
├── dream.py                   # the analysis + proposal script
├── dreaming-state.md          # THE SPINE — last batch date reviewed
└── target-repo/                # a git repo holding the skill file dreaming proposes changes to
    └── .claude/skills/daily-triage/SKILL.md
```

## The seeded pattern

Across the 7 nights, different CI-failure fixes get proposed and merged
every night (never repeating — normal, healthy loop behavior). But one
candidate, `pricing-string-format` (the same risky public-API change
from Project 8), gets **drafted and rejected 5 separate nights** — a real
waste: a worktree opened, a reviewer invoked, a FAIL logged, every single
time, for a fix that was always going to fail for the same reason.

## Proof it works — the full lifecycle, actually run

**Run 1 — finds the pattern, drafts a proposal:**
```
$ python dream.py
Dreaming: reading 7 new run log(s) (since 0000-00-00)...

FAIL frequency across the batch:
  pricing-string-format: 5x  <- repeated pattern

1 repeated pattern(s) found. Drafting a proposal as a PR branch...
Proposal committed to branch 'claude/dreaming-update-2026-09-16' in target-repo/.
This branch is NOT merged. A human must review it.
```

**Verified — `master` was never touched:**
```
$ cd target-repo && git branch --show-current
master
$ grep -c "Learned from repeated failures" .claude/skills/daily-triage/SKILL.md
0                                          <- correct: not on master
```

**The proposal itself, with cited evidence** (not "trust me," actual
file names):
```
dreaming: stop re-attempting known-doomed candidates

Evidence (from 7 nightly runs, 2026-09-10 to 2026-09-16):
  - `pricing-string-format`: failed 5x across run-2026-09-10.md,
    run-2026-09-12.md, run-2026-09-13.md, run-2026-09-15.md,
    run-2026-09-16.md

This is a PROPOSAL. A human must review and merge this branch -- the
dreaming loop does not merge its own changes.

+ ## Learned from repeated failures (added by dreaming, 2026-09-16)
+
+ - `pricing-string-format` is a known-doomed candidate (public API
+   change...). Do not draft a fix for it. Escalate directly to "Open /
+   needs a human" without opening a worktree -- it will fail review
+   every time and wastes a beat.
```

**Run 2 (same day) — the dreaming loop's own spine stops it from
re-analyzing the same week twice:**
```
$ python dream.py
Dreaming: no new run logs since last review. Nothing to do.
```

**Then, the human gate — I played the human, reviewed the branch,
agreed, and merged it:**
```
$ git merge claude/dreaming-update-2026-09-16
$ tail -6 .claude/skills/daily-triage/SKILL.md
## Learned from repeated failures (added by dreaming, 2026-09-16)
- `pricing-string-format` is a known-doomed candidate... Do not draft a
  fix for it. Escalate directly...
```

The next time Project 8's loop runs for real, it reads this updated
skill file and stops wasting a beat on a fix that was always going to
fail — exactly the mechanism Concept 13 credits with making loops both
more accurate *and* cheaper over time.

## How to run it yourself

```
cd "E:\Loop Engineering Projects\12-dreaming-capstone"
python dream.py                    # finds the pattern, drafts the branch
cd target-repo && git show claude/dreaming-update-2026-09-16   # review it
git merge claude/dreaming-update-2026-09-16                     # approve it (or don't)
```

## Run it automatically

I ran the entire lifecycle for real — pattern detection, evidenced
proposal, untouched-`master` verification, spine-based no-op on a second
run, and a human-approved merge — with actual git commits and actual
file diffs, not narration. The one thing deliberately **not** automated
is the merge step itself: `dream.py` cannot and will not merge its own
proposal. That decision is the human gate, on purpose, every time.

**On a weekly heartbeat**, this would be wired the same way as Project 3
and 4's Windows Scheduled Tasks — a task that runs `dream.py` every
Sunday night against that week's real `logs/`. I didn't register that
task here, because doing so against *real* Project 8/9 logs (once they
accumulate genuine history, not this project's disclosed synthetic
seed) is the point at which this stops being a demo and starts being a
rule that actually governs your other loops — worth turning on
deliberately, with your eyes open, not by a course finishing its list.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "Evidence, always" | Every proposal cites the exact log files, not just a count |
| "The human gate, always" | `dream.py` drafts and commits to a branch; a separate, manual step merges |
| "Propose small diffs, never full rewrites" (brevity bias / context collapse) | The proposal is a 4-line addition, not a rewrite of `SKILL.md` |
| The dreaming loop's own spine | `dreaming-state.md`, proven by the no-op second run |
| "A dream needs material" | This README's disclosure of synthetic seed data, instead of overclaiming a finding from 2 real runs |
