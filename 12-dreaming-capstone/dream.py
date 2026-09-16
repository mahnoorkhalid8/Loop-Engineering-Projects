#!/usr/bin/env python3
"""The dreaming / improvement loop (Concept 12's interlude), built for
real: reads a batch of nightly run logs, finds patterns that repeat
across multiple nights, and proposes a rule change to the target
project's skill file -- as a PR-ready git branch, NEVER a direct edit.
A human must merge it. This script cannot merge its own proposal.

Threshold: a candidate that FAILed 3+ times in the batch is a signal a
single run can't see, but a week of logs can. One FAIL is noise. Three
is a missing lesson.

Usage: python dream.py
"""

import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS_DIR = ROOT / "logs"
STATE_FILE = ROOT / "dreaming-state.md"
TARGET_REPO = ROOT / "target-repo"
SKILL_FILE = TARGET_REPO / ".claude" / "skills" / "daily-triage" / "SKILL.md"
THRESHOLD = 3

FAIL_RE = re.compile(r"^- FAIL: ([\w-]+) — (.+)$", re.M)


def load_last_reviewed() -> str:
    if not STATE_FILE.exists():
        return "0000-00-00"
    text = STATE_FILE.read_text(encoding="utf-8")
    m = re.search(r"last_reviewed:\s*(\d{4}-\d{2}-\d{2})", text)
    return m.group(1) if m else "0000-00-00"


def save_state(last_reviewed: str, batch_size: int):
    STATE_FILE.write_text(
        f"# Dreaming loop — memory (the spine)\n\n"
        f"last_reviewed: {last_reviewed}\n"
        f"last_batch_size: {batch_size}\n"
        f"\nThis file is what stops the dreaming loop from re-analyzing\n"
        f"the same nights of logs every time it runs.\n",
        encoding="utf-8",
    )


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def main():
    last_reviewed = load_last_reviewed()
    log_files = sorted(LOGS_DIR.glob("run-*.md"))
    new_logs = [f for f in log_files if f.stem.replace("run-", "") > last_reviewed]

    if not new_logs:
        print("Dreaming: no new run logs since last review. Nothing to do.")
        return

    print(f"Dreaming: reading {len(new_logs)} new run log(s) "
          f"(since {last_reviewed})...")

    fail_counter = Counter()
    fail_evidence = {}
    for f in new_logs:
        text = f.read_text(encoding="utf-8")
        for slug, reason in FAIL_RE.findall(text):
            fail_counter[slug] += 1
            fail_evidence.setdefault(slug, []).append((f.name, reason))

    print("\nFAIL frequency across the batch:")
    for slug, count in fail_counter.most_common():
        flag = "  <- repeated pattern" if count >= THRESHOLD else ""
        print(f"  {slug}: {count}x{flag}")

    repeated = {s: c for s, c in fail_counter.items() if c >= THRESHOLD}
    latest_date = new_logs[-1].stem.replace("run-", "")

    if not repeated:
        print(f"\nNo pattern crossed the threshold ({THRESHOLD}+ occurrences). "
              f"One FAIL is noise -- nothing proposed this batch.")
        save_state(latest_date, len(new_logs))
        return

    print(f"\n{len(repeated)} repeated pattern(s) found. Drafting a proposal "
          f"as a PR branch (never a direct edit)...")

    branch = f"claude/dreaming-update-{date.today().isoformat()}"
    run(["git", "checkout", "-q", "-b", branch], cwd=TARGET_REPO)

    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    new_rules = []
    evidence_lines = []
    for slug, count in repeated.items():
        reason = fail_evidence[slug][0][1]
        new_rules.append(
            f"- `{slug}` is a known-doomed candidate ({reason}). Do not "
            f"draft a fix for it. Escalate directly to \"Open / needs a "
            f"human\" without opening a worktree -- it will fail review "
            f"every time and wastes a beat."
        )
        cited = ", ".join(f[0] for f in fail_evidence[slug])
        evidence_lines.append(f"  - `{slug}`: failed {count}x across {cited}")

    updated = skill_text.rstrip("\n") + "\n\n## Learned from repeated failures (added by dreaming, " + date.today().isoformat() + ")\n\n" + "\n".join(new_rules) + "\n"
    SKILL_FILE.write_text(updated, encoding="utf-8")

    commit_msg = (
        f"dreaming: stop re-attempting known-doomed candidates\n\n"
        f"Evidence (from {len(new_logs)} nightly runs, "
        f"{new_logs[0].stem.replace('run-','')} to {latest_date}):\n"
        + "\n".join(evidence_lines)
        + "\n\nThis is a PROPOSAL. A human must review and merge this "
          "branch -- the dreaming loop does not merge its own changes."
    )
    run(["git", "add", "-A"], cwd=TARGET_REPO)
    run(["git", "commit", "-q", "-m", commit_msg], cwd=TARGET_REPO)
    run(["git", "checkout", "-q", "master"], cwd=TARGET_REPO)

    print(f"\nProposal committed to branch '{branch}' in target-repo/.")
    print("This branch is NOT merged. A human must review it:")
    print(f"  cd target-repo && git show {branch}")
    print(f"  cd target-repo && git merge {branch}   # only if you agree")

    save_state(latest_date, len(new_logs))


if __name__ == "__main__":
    main()
