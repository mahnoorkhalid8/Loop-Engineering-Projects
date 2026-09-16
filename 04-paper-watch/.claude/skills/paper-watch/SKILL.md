---
name: paper-watch
description: >-
  Reports NEW arXiv papers on a topic since the last run, using progress.md
  as memory. Use when the user asks what's new on arXiv about a topic.
---

# Paper Watch

1. Run `python scripts/paper_watch.py "<topic>"` from the project root.
2. Read `progress.md` first if you want to know what's already been shown
   before deciding how to phrase the answer — the script itself already
   does this deduplication, you don't need to redo it by hand.
3. Report only what the script prints. If it says nothing new, say that
   plainly — don't re-list old papers to seem more useful.
4. Never delete or hand-edit `progress.md`'s "Already shown" list. That is
   the loop's only memory; editing it defeats the point.
