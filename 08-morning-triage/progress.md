# Morning Triage — memory (the spine)

Read this file first on every run. Write to it last.

## Done

- 2026-09-16: fixed `apply_tax` in discount.py (was adding rate instead
  of multiplying) — branch `claude/fix-tax`, reviewer PASS, merged to
  master. test_discount.py passes.
- 2026-09-16: fixed `last_restocked` off-by-one in inventory.py — branch
  `claude/fix-restock`, reviewer PASS, merged to master. test_inventory.py
  passes.

## In progress

(none)

## Open / needs a human

- 2026-09-16: `pricing-string-format` advisory (see advisory.md). Drafted
  on branch `claude/pricing-string-format` — changes `serialize_price()`
  from returning `int` cents to a formatted `str`. Reviewer verdict: FAIL.
  Reason: `serialize_price` is documented as used by the mobile app and
  the partner integration; changing its return type is a public behavior
  change, not a safe internal fix. Branch left unmerged for a human to
  decide (e.g. version the API, or coordinate the change with both
  consumers) — do not merge automatically.
