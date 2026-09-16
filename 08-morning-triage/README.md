# Project 8 — Full Morning-Triage Loop

**This is Part 5 of the course, built for real.** Every other project in
this series builds one piece of a loop in isolation. This one wires all
five working parts plus the spine together into the single loop the
course centers on: heartbeat → skill → worktree isolation → maker-checker
→ connector-style write → spine.

## What's in this folder

```
08-morning-triage/
├── .claude/skills/daily-triage/SKILL.md   # the loop body, one line of triggers away
├── .claude/agents/reviewer.md              # the checker -- separate from the maker
├── progress.md                             # THE SPINE
├── run_loop.sh                             # rebuilds demo-repo and runs one full beat
└── demo-repo/
    ├── discount.py, inventory.py    # two real overnight CI failures
    ├── pricing.py, advisory.md      # one risky "safe fix" that should be rejected
    └── test_discount.py, test_inventory.py, tests.py
```

## The three candidates, and why each one matters

| Candidate | What it is | Verdict | Why |
|---|---|---|---|
| `apply_tax` bug | `return amount + rate` instead of `amount * (1 + rate)` | **PASS → merged** | Fixes exactly one bug, no public API touched |
| `last_restocked` bug | off-by-one `IndexError` | **PASS → merged** | Same — smallest possible fix |
| `serialize_price` "readability fix" | changes return type `int` → `str` | **FAIL → escalated** | `serialize_price` is documented as used by the mobile app and the partner integration — this is exactly the "no public API change" rule from `SKILL.md` |

That third one is the point of the whole project. It *looks* like a
harmless improvement. A checker that only runs the test suite would miss
it (nothing asserts the return type). The reviewer catches it because its
instructions explicitly check for public-behavior changes, not just test
pass/fail — this is the checker ladder from the course (Concept 2) doing
real work: a passing test is proof of one thing; "did this change public
behavior" needed a second, different kind of check.

## Proof it works — one full beat, actually run

```
### STEP 2: draft each candidate in its own worktree ###
(git worktree add -b claude/fix-tax, claude/fix-restock, claude/pricing-string-format)

### STEP 3: reviewer verdicts ###
-- claude/fix-tax --
test_discount: PASSED
-- claude/fix-restock --
test_inventory: PASSED
-- claude/pricing-string-format --
serialize_price(108) = '$1.08' | type: str -- return type changed on a
documented public API -> FAIL

### STEP 4: merge PASS, leave FAIL unmerged ###
full suite on master:
ALL TESTS PASSED
pricing.py on master (untouched -- FAIL branch never merged):
108 int

### final history ###
*   d2817fc merge: fix-restock (reviewer: PASS)
|\
| * 749a16b fix: last_restocked off-by-one
* | 23384ea fix: apply_tax should multiply, not add
|/
* 117b6c2 initial: two overnight CI failures, one stable public API, plus tests
```

Both safe fixes are on `master`, isolated in their own worktrees the
whole time they were being drafted (Project 5's mechanism, reused for
real here). The risky one sits on `claude/pricing-string-format`,
unmerged, exactly where a human would find it to review.

## The spine — read at the start, written at the end

`progress.md` after this run:

```markdown
## Done
- 2026-09-16: fixed `apply_tax` ... reviewer PASS, merged to master.
- 2026-09-16: fixed `last_restocked` ... reviewer PASS, merged to master.

## Open / needs a human
- 2026-09-16: `pricing-string-format` advisory ... Reviewer verdict: FAIL.
  Reason: public behavior change. Branch left unmerged for a human to
  decide — do not merge automatically.
```

This is what you'd read at 9:30am instead of the full run transcript —
two things shipped, one thing needs five minutes of your judgment, and
*why* is written down, not just *what*.

## How to run it yourself

```bash
cd "E:\Loop Engineering Projects\08-morning-triage"
bash run_loop.sh
```
Rebuilds `demo-repo/` from scratch and replays the entire beat — the
exact commands above, not a re-narration of them.

Via Claude Code, once you've pointed it at a real repo with real failing
tests instead of `demo-repo`'s planted ones:
```
claude
run the daily-triage skill
```
The `daily-triage` skill is already loaded in this session too (visible
in the skills list) since its `SKILL.md` lives under this folder's
`.claude/skills/`.

## Run it automatically

I ran the entire loop for real — three worktrees, three real diffs, one
real reviewer verdict on public-API risk, two real merges, and a spine
write — using `Bash`/git directly, which is the same mechanism `/loop`,
`/goal`, and a Routine all reduce to under the hood. I did not spend your
Claude Code usage doing it, because none of this actually required an
LLM call: the "reviewer" step here is deterministic (run the test, check
the docstring for "public API"), which is realistic for a first version
of a checker — plenty of real checkers start exactly this mechanical
before judgment calls get layered in (see Project 2's Part A/B split, and
the verification-skills interlude in the course).

To wire this to a real heartbeat unattended, see Project 9 — it's the
same shape as Sky Watch/Paper Watch's Scheduled Task, just pointed at
`run_loop.sh` (or, for a real repo, at `claude -p "run the daily-triage
skill"`, which *does* spend your usage — worth doing deliberately, not
by accident on a timer).

## The concept, made concrete

| In the course | In this project |
|---|---|
| Heartbeat | not wired here (this project isolates "what happens in one beat"; Project 9 shows the scheduling) |
| Worktree | `git worktree add -b claude/<slug>`, one per candidate |
| Skill | `.claude/skills/daily-triage/SKILL.md` |
| Maker-checker | drafts in a worktree, reviewer checks the diff before it's allowed to merge |
| Connector-style write | merging to `master` only on PASS, mirroring Project 7's "only write when it's safe" rule |
| Spine | `progress.md`, read first, written last |
| Human gate | the unmerged `claude/pricing-string-format` branch + its `progress.md` entry |
