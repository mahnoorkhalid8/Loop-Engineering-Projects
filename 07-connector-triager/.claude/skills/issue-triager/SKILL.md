---
name: issue-triager
description: >-
  Files incoming issues into the (mock) ticket system by running triage.py.
  Safe to re-run: it updates existing tickets by external_id instead of
  duplicating them. Use when asked to triage or file new issues.
---

# Issue Triager

1. Run `python triage.py` from the project root.
2. Report the summary line (created/updated/needs-a-human counts).
3. Anything printed as `[NEEDS A HUMAN]` is not a failure to retry — it's
   a permission boundary. Report it plainly with its suggested next step;
   do not attempt to work around a locked project.
4. Never write directly to `tickets.json`. Always go through
   `mock_ticket_system.create_or_update_ticket`, which is what keeps
   re-runs safe.
