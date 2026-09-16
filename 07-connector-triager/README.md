# Project 7 — Connector-Powered Issue Triager

**Concept:** connectors / MCP-style actions (Concept 10)
**What it teaches:** a loop that can only read is a loop that can only
talk. The moment it can *act* — file a ticket, open a PR — two new rules
apply that don't matter for read-only work: writes must be safe to
repeat, and errors must say what to do next.

## What's in this folder

```
07-connector-triager/
├── mock_ticket_system.py    # stands in for a real MCP connector (Linear/Jira/etc.)
├── incoming_issues.json     # 4 fake overnight issues, one deliberately unfileable
├── triage.py                # the loop body
├── .claude/skills/issue-triager/SKILL.md
└── tickets.json             # created by running it (the "external system")
```

## Rule 1 — writes must be safe to repeat, proven

A loop retries. If "file this ticket" isn't safe to call twice, a retry
creates a duplicate. `create_or_update_ticket()` is keyed by a stable
`external_id`, so calling it once or a hundred times produces exactly one
ticket, updated in place.

**Proof, run twice on the same input:**
```
=== RUN 1 (fresh) ===
[created] gh-101: Login crashes on Android when token expires mid-session
[created] gh-102: Add dark mode toggle to settings page
[created] gh-103: Docs typo: 'recieve' should be 'receive'
[NEEDS A HUMAN] gh-104: ...
3 created, 0 updated, 1 need a human. Total tickets: 3

=== RUN 2 (same issues.json — simulating a retried beat) ===
[updated] gh-101: ... (already existed -- no duplicate)
[updated] gh-102: ... (already existed -- no duplicate)
[updated] gh-103: ... (already existed -- no duplicate)
[NEEDS A HUMAN] gh-104: ...
0 created, 3 updated, 1 need a human. Total tickets: 3
```

Ticket count: **3 after run 1, still 3 after run 2.** No duplicates.

**Contrast — the naive, unsafe way**, for comparison (not in the real
loop, just a demonstration of what "not idempotent" looks like):
```
2 tickets after 2 identical calls with the naive approach (should be 1 if safe)
 - {'title': 'Login crashes on Android...'}
 - {'title': 'Login crashes on Android...'}     <- duplicate
```
That's what happens without a stable key. Every retry, every
double-fired webhook, every re-run after a crash mid-loop would double
your ticket queue.

## Rule 2 — errors must say what to do next, proven

`gh-104` targets a project (`legacy-billing`) that's locked for automated
writes. The failure isn't a bare `403` — it's a message a *loop* (or a
human reading `progress.md` the next morning) can act on without
guessing:

```
[NEEDS A HUMAN] gh-104: Cannot file into project "legacy-billing": it is
locked for automated writes. Next step: ask a human to unlock it, or
route this ticket to "triage-inbox" instead and let a person move it
manually.
```

Compare that to what a real, badly-designed connector often returns:
`Error 403`. One of these wastes a beat. The other fixes itself on the
next run, or tells the human exactly what to do.

## How to run it yourself

```
cd "E:\Loop Engineering Projects\07-connector-triager"
python triage.py
```
Run it again — watch the counts shift from `created` to `updated`, and
the ticket count stay flat.

Via Claude Code:
```
claude
run the issue-triager skill
```

## Run it automatically

This one needs no LLM and no external credentials (the "connector" is a
local mock), so I ran the whole proof above for real — the idempotency
check, the locked-project error, and the unsafe-approach contrast are all
actual script output, not narrated. Nothing to schedule separately here:
this project is a building block (the "what a connector call inside a
beat should look like" building block) that Project 8 wires into a full
scheduled loop next.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "Writes must be safe to repeat" | `create_or_update_ticket`, keyed by `external_id`, proven with a 2x run |
| "Errors must say what to do next" | The `legacy-billing` `TicketError` message |
| Fewer, focused tools | This module exposes exactly one write operation, not a general-purpose "run any query" tool |
