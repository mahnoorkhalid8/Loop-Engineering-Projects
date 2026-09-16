#!/usr/bin/env python3
"""Reads incoming_issues.json and files each into the (mock) ticket
system via mock_ticket_system.create_or_update_ticket. Safe to run
repeatedly -- see README.md for the actual proof.
"""

import json
import sys
from pathlib import Path

from mock_ticket_system import create_or_update_ticket, TicketError

ISSUES_PATH = Path(__file__).resolve().parent / "incoming_issues.json"


def main():
    issues = json.loads(ISSUES_PATH.read_text(encoding="utf-8"))
    created, updated, failed = 0, 0, 0

    for issue in issues:
        try:
            result = create_or_update_ticket(
                external_id=issue["external_id"],
                project=issue["project"],
                title=issue["title"],
                labels=issue["labels"],
                urgent=issue.get("urgent", False),
            )
            if result["action"] == "created":
                created += 1
                print(f'[created] {issue["external_id"]}: {issue["title"]}')
            else:
                updated += 1
                print(f'[updated] {issue["external_id"]}: {issue["title"]} (already existed -- no duplicate)')
        except TicketError as e:
            failed += 1
            print(f'[NEEDS A HUMAN] {issue["external_id"]}: {e}')

    print(f"\n{created} created, {updated} updated, {failed} need a human. "
          f"Total tickets in the system: {len(json.loads(Path('tickets.json').read_text()))}"
          if Path("tickets.json").exists() else "")


if __name__ == "__main__":
    main()
