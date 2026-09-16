#!/usr/bin/env python3
"""Nightly reconciliation sweep (Appendix A3). GitHub-event Routines have
an hourly firing cap during the research preview; events past the cap
are DROPPED, not queued. This script simulates the fix: list every open
PR, cross-reference against processed.json (the spine -- what the event
trigger actually caught), and catch anything the event trigger missed.

Safe to run every night, or twice in a row -- see the second run at the
bottom of README.md, which finds nothing left to do (idempotent, same
discipline as Project 7's ticket writes).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

PRS_PATH = Path(__file__).resolve().parent / "mock_open_prs.json"
PROCESSED_PATH = Path(__file__).resolve().parent / "processed.json"


def main():
    open_prs = json.loads(PRS_PATH.read_text(encoding="utf-8"))
    processed = json.loads(PROCESSED_PATH.read_text(encoding="utf-8"))

    missed = [pr for pr in open_prs if str(pr["number"]) not in processed]

    if not missed:
        print("Reconciliation sweep: nothing missed. All open PRs were "
              "already reviewed by the event trigger. [OK]")
        return

    print(f"Reconciliation sweep: {len(missed)} PR(s) the event trigger "
          f"never caught (likely dropped by the hourly cap):")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for pr in missed:
        print(f"  - #{pr['number']}: {pr['title']}  -> reviewing now via sweep")
        processed[str(pr["number"])] = {
            "reviewed_via": "reconciliation_sweep",
            "at": now,
        }

    PROCESSED_PATH.write_text(json.dumps(processed, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nprocessed.json updated. {len(processed)}/{len(open_prs)} open PRs now reviewed.")


if __name__ == "__main__":
    main()
