# Project 11 — Routine Drill: GitHub-Event Routine + Reconciliation Sweep

**Concept:** Appendix A3's GitHub trigger, plus its least-obvious warning:
during the research preview, GitHub events are capped hourly per routine
and per account, and **events past the cap are dropped, not queued.** An
event-heavy design needs a second heartbeat — a nightly sweep — as a
safety net.

## What's in this folder

```
11-routine-drill-github-event/
├── routine-github-trigger-config.md   # the event-trigger filter fields, filled in
├── mock_open_prs.json                  # 12 "currently open" PRs
├── processed.json                      # THE SPINE — what's actually been reviewed, and how
├── reconcile.py                        # the nightly sweep
└── .claude/skills/reconciliation-sweep/SKILL.md
```

## The scenario, made concrete

A busy morning: 12 PRs open within the same hour. The event trigger has
an hourly cap — here simulated as 8 — so `processed.json` starts with
only PRs `#401`–`#408` marked `reviewed_via: github_event_trigger`.
`#409`–`#412` opened in the same busy window and were **silently
dropped**. Nobody gets an error. The PRs just never got reviewed.

## Proof it works — the sweep catches exactly what was dropped

```
$ python reconcile.py
Reconciliation sweep: 4 PR(s) the event trigger never caught (likely
dropped by the hourly cap):
  - #409: Migrate legacy reports to new schema  -> reviewing now via sweep
  - #410: Fix off-by-one in pagination helper  -> reviewing now via sweep
  - #411: Add integration test for webhook retries  -> reviewing now via sweep
  - #412: Bump internal SDK to v3.2  -> reviewing now via sweep

processed.json updated. 12/12 open PRs now reviewed.
```

Run it again the same night (or the next), and it correctly finds
nothing left — the same idempotency discipline as Project 7's ticket
writes and Project 4's "nothing new" spine check:

```
$ python reconcile.py
Reconciliation sweep: nothing missed. All open PRs were already
reviewed by the event trigger. [OK]
```

## The trigger config, and the regex trap worth knowing in advance

`routine-github-trigger-config.md` has the full field-by-field setup —
event kind, actions, filters — plus the one gotcha the course flags
explicitly: `matches regex` tests the **whole field**, not a substring.
Typing `hotfix` as a regex filter matches a title that is *exactly*
`hotfix`, nothing containing it. Use `.*hotfix.*`, or use `contains`
instead.

## How to make this real

1. Install the Claude GitHub App on your repo (confirmed separately from
   `/web-setup`, which only grants clone access — see the config file for
   why this trips people up).
2. Create a Routine with a GitHub trigger using the field values in
   `routine-github-trigger-config.md`.
3. **Also** create a second Routine — a *scheduled* one, nightly — whose
   prompt is: "List every open PR in this repo. For any not yet reviewed
   according to `processed.json` [or your real tracking mechanism], review
   it now and update the record." That's `reconcile.py`'s logic, handed
   to an actual agent instead of a mock JSON diff.

## Run it automatically

Fully run above, twice, with real (simulated) data — the dropped-PR
detection and the idempotent re-run are both genuine script output. The
one thing I can't do without your GitHub account is register the actual
event-trigger Routine; the config file has everything needed to do that
in a couple of minutes.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "Events past the cap are dropped, not queued" | The 4 missing PRs in the starting `processed.json` |
| "An event-heavy design needs a reconciliation sweep" | `reconcile.py`, run and proven |
| Spine (Concept 12), applied to a second heartbeat | `processed.json` tracks state across *two different* triggers (event + sweep), not just one |
| Safe to repeat (Concept 10 / Project 7) | Run 2 finds nothing left — no double-review |
