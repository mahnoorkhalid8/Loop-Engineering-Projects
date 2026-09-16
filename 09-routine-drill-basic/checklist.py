#!/usr/bin/env python3
"""Automates as much of the Appendix A6 pre-flight checklist as text
alone can prove, against a routine prompt file. This can't check
connectors/repos/env (those are form fields, not text) -- see README.md
for the parts that stay manual. Stdlib only.

Usage: python checklist.py routine-prompt.md
"""

import re
import sys
from pathlib import Path

CHECKS = [
    ("defines what 'done' looks like even for the empty case",
     lambda t: bool(re.search(r"no new|none found|nothing to|if there (are|is) no", t, re.I))),
    ("has an explicit limit (max items / stop condition)",
     lambda t: bool(re.search(r"\bstop after\b|\bat most\b|\bmaximum\b|\bno more than\b|\bcap(ped)? at\b", t, re.I))),
    ("has at least one explicit boundary ('do not ...')",
     lambda t: len(re.findall(r"\bdo not\b|\bnever\b", t, re.I)) >= 1),
    ("names where output goes (a connector target)",
     lambda t: bool(re.search(r"slack|email|linear|jira|github|post to|send to|#\w+", t, re.I))),
    ("doesn't rely on missing prior context ('as discussed', 'continue from', 'like before')",
     lambda t: not re.search(r"as discussed|continue from (where|last)|like (we|i) (did|discussed)|as mentioned earlier", t, re.I)),
    ("is substantial enough to be self-contained (not a one-liner)",
     lambda t: len(t.split()) >= 25),
    ("time-bounds the work it looks at (e.g. 'last 24 hours', 'today', 'this week')",
     lambda t: bool(re.search(r"last \d+ hours?|last \d+ days?|\btoday\b|\bthis week\b|overnight", t, re.I))),
]


def main():
    if len(sys.argv) != 2:
        print("usage: python checklist.py <prompt-file>")
        sys.exit(2)
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    passed = 0
    for name, fn in CHECKS:
        ok = fn(text)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += ok
    print(f"\n{passed}/{len(CHECKS)}")
    print(
        "\nNOT checkable from text alone -- verify these by hand against\n"
        "Appendix A2/A6 before you save the Routine:\n"
        "  - repositories list is the correct repo only, unrestricted pushes OFF\n"
        "  - connectors list has been trimmed to only what this job needs\n"
        "  - secrets (if any) are in the environment panel, not a .env file\n"
        "  - you fired it once with Run now / a one-off schedule and read the transcript"
    )
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
