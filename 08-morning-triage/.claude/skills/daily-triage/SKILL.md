---
name: daily-triage
description: >-
  Runs the morning maintenance pass on demo-repo/. Reads progress.md,
  gathers overnight CI failures and advisories, drafts safe fixes (each
  checked by a separate reviewer agent) in isolated git worktrees, opens
  a pull-request-ready branch for what passes, and writes anything risky
  to progress.md for a human. Use this for the scheduled morning
  maintenance loop.
---

# Daily triage

You are the morning maintenance loop. Work through these steps in order.
Do not skip the progress file — it is your only memory between runs.

## 1. Read your memory first

Open `progress.md`. Read "In progress" and "Open / needs a human". Do not
redo anything already listed under "Done".

## 2. Find the work

In `demo-repo/`: failing tests (run `python tests.py`), and anything
flagged in `advisory.md`. Cap at 5 candidates per run.

## 3. Work each candidate

- Create an isolated worktree: `git worktree add -b claude/<slug> ../wt-<slug>`.
- Draft the smallest fix that solves the one problem. Do not bundle changes.
- Send the diff to the reviewer subagent. Wait for its verdict.

## 4. Decide from the verdict

- PASS and low risk (no public API change, no data migration, no file
  deletion): commit on the `claude/<slug>` branch. That branch is the
  "PR" — ready for a human to open/merge.
- FAIL, or the change touches anything risky: do NOT commit it as a
  ready branch. Add a short entry to "Open / needs a human" in
  `progress.md` instead.

## 5. Update your memory last

Move finished items to "Done" with today's date. Save `progress.md`.

## Rules

- Never touch `master` directly. Only `claude/*` branches.
- When in doubt, escalate. A flagged item a human checks is always safer
  than a wrong fix shipped while no one was watching.
