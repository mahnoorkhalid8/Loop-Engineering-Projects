---
name: reconciliation-sweep
description: >-
  Nightly safety net for a GitHub-event Routine. Lists every open PR and
  reviews any that the event trigger never caught (dropped by the hourly
  cap), using processed.json as the spine. Use for the nightly sweep run.
---

# Reconciliation sweep

1. Run `python reconcile.py` from the project root.
2. For each PR it reports as newly caught, actually review it (per
   `routine-github-trigger-config.md`'s prompt) before considering the
   sweep done — the script only tracks *which* PRs need review, it
   doesn't review them itself.
3. Report the summary line. If nothing was missed, say so plainly.
4. Never hand-edit `processed.json`. It's the only record of what's
   already been reviewed and by which path (event trigger vs. sweep).
