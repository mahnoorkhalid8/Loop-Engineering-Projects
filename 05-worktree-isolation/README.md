# Project 5 — Worktree Isolation Demo

**Concept:** isolation via `git worktree` (Concept 8)
**What it teaches:** the moment a loop runs more than one agent at once,
they start overwriting each other's uncommitted work — unless each one
gets its own checkout.

## What's in this folder

```
05-worktree-isolation/
├── run_demo.sh      # rebuilds everything from scratch and runs the full demo
└── demo-repo/        # a tiny git repo with two independently-broken functions
```

`run_demo.sh` is idempotent — delete `demo-repo/` and any `wt-*` folders,
or just re-run it; it always starts from a clean slate.

## The setup

`bugs.py` has two unrelated bugs, standing in for "two overnight CI
failures":

```python
def add(a, b):
    return a - b        # BUG: should be a + b

def is_even(n):
    return n % 2 == 1   # BUG: inverted logic
```

Two "agents" each need to fix one function.

## Step A — no isolation (the failure this concept exists to prevent)

Both agents work in the **same checkout**. Agent A reads the file, computes
its fix, and writes it back. Agent B *also* read the file **before** A
wrote back (this is what "running in parallel" actually means), computes
its own fix from the stale original, and writes its version back —
silently erasing Agent A's fix, because A's edit was never committed to
disk in a way B's write could respect.

**Proof, actually run:**
```
Agent A wrote its fix.
Agent B (started from the stale original) wrote its fix, overwriting A's.

--- result: Agent A's fix is gone ---
AssertionError: add(2,3) should be 5, got -1
(tests fail -- add() is still broken, proving the collision)
```

Real data loss, from a real race, not a hypothetical.

## Step B — isolated worktrees (the fix)

```bash
git worktree add -b claude/fix-add  ../wt-fix-add
git worktree add -b claude/fix-even ../wt-fix-even
```

Now each agent has its **own directory** and its **own branch**. Agent A
edits `wt-fix-add/bugs.py`; Agent B edits `wt-fix-even/bugs.py`. These are
different files on disk — there is no write for either agent to clobber.
Each commits independently:

```
git log --oneline --graph
*   6539078 merge: fix-even
|\
| * c1ad80a fix: is_even() had inverted logic
* | 53639c2 fix: add() should sum, not subtract
|/
* a564c06 initial: two broken functions, two failing tests
```

Merging both branches back into `master` (the human-review step, in a
real loop — this is where a PR would be opened per branch instead) gives
a file with **both** fixes:

```
--- merged bugs.py: both fixes present ---
def add(a, b):
    return a + b  # fixed by Agent A, in its own worktree

def is_even(n):
    return n % 2 == 0  # fixed by Agent B, in its own worktree

--- running tests on the merged result ---
ALL TESTS PASSED
```

Same two fixes as Step A. Only the isolation changed. That's the entire
concept.

## How to run it yourself

```bash
cd "E:\Loop Engineering Projects\05-worktree-isolation"
bash run_demo.sh
```

Takes a few seconds, no dependencies beyond git and Python (both already
confirmed installed on this machine).

## Run it automatically

I ran it for you, twice — once step by step to build the walkthrough
above, and once via the packaged `run_demo.sh` from a totally clean slate
to prove the script itself (not just my manual commands) reproduces the
result. Both runs are real git history, real file collisions, real merges
— nothing here is simulated or narrated.

There's no heartbeat to schedule in this project — worktrees are a
*within-beat* mechanism (they isolate work inside one run of a loop), not
a heartbeat themselves. This is infrastructure the loops in Projects 6 and
8 depend on, not a standalone loop.

## How this maps to Claude Code / OpenCode

**Claude Code:**
```
claude --worktree     # open a session in its own checkout
```
Or on a subagent definition: `isolation: worktree` — each helper gets a
fresh checkout that cleans itself up when it finishes. A scheduled task
can also turn on worktree isolation per run.

**OpenCode:** the same `git worktree` commands used in this demo — the
CLI doesn't wrap them in a flag the way Claude Code does, so you drive
`git worktree add` / `remove` directly, exactly as `run_demo.sh` does.

## The concept, made concrete

| In the course | In this project |
|---|---|
| "Two agents working at once overwrite each other's files" | Step A, proven with a real failing assertion |
| Worktree = separate checkout, same repo history | `wt-fix-add` and `wt-fix-even`, both branched from the same `master` |
| Isolation lets parallel work merge cleanly | The diamond merge in `git log --graph`, both fixes present |
