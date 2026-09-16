"""A tiny stand-in for a real connector (Linear, Jira, GitHub Issues...)
talking to an outside system over MCP. Stores tickets in tickets.json.

The two rules this module exists to demonstrate (Concept 10):
  1. Writes must be safe to repeat -- create_or_update_ticket() is keyed
     by a stable external ID, so calling it twice with the same ID
     UPDATES, never duplicates.
  2. Errors must say what to do next -- TicketError messages always name
     the fix, not just the failure.
"""

import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tickets.json"

LOCKED_PROJECTS = {"legacy-billing"}  # simulates a permission boundary


class TicketError(Exception):
    """Raised with a message that always says what to do next."""


def _load() -> dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text(encoding="utf-8"))
    return {}


def _save(db: dict) -> None:
    DB_PATH.write_text(json.dumps(db, indent=2, sort_keys=True), encoding="utf-8")


def create_or_update_ticket(external_id: str, project: str, title: str,
                             labels: list, urgent: bool = False) -> dict:
    """Idempotent by external_id. Call this 1 time or 100 times with the
    same external_id + fields -- the result is always exactly one ticket,
    updated in place, never duplicated. This is what makes it safe for a
    retrying loop to call."""
    if project in LOCKED_PROJECTS:
        raise TicketError(
            f'Cannot file into project "{project}": it is locked for '
            f'automated writes. Next step: ask a human to unlock it, or '
            f'route this ticket to "triage-inbox" instead and let a '
            f'person move it manually.'
        )

    db = _load()
    existing = db.get(external_id)
    action = "updated" if existing else "created"
    db[external_id] = {
        "external_id": external_id,
        "project": project,
        "title": title,
        "labels": sorted(set(labels)),
        "urgent": urgent,
    }
    _save(db)
    return {"action": action, "ticket": db[external_id]}


def all_tickets() -> dict:
    return _load()
