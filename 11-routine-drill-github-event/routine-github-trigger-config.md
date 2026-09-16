# GitHub-event Routine — trigger configuration

**Concept:** Appendix A3 (GitHub trigger). Fires a fresh session when a
matching event lands on a connected repo. Two event kinds: `pull_request`
and `release`.

## Prerequisite (the #1 setup failure per the course's own field notes)

The **Claude GitHub App** must be installed on the repository.
`/web-setup` only grants clone access — it does **not** install the app.
Confirm at `github.com/settings/installations` that "Claude" (or your
org's equivalent) is listed against this repo before configuring
anything below.

## Trigger configuration

| Field | Value | Why |
|---|---|---|
| Event kind | `pull_request` | reviewing PRs, not releases |
| Actions | `opened`, `synchronize` | fires on a new PR and on every push to it — there is no separate "on push" event; a push to a branch with an open PR counts as `synchronize` |
| Author filter | (none) | review everyone's PRs, not just one person's |
| Title filter | `contains` → *(none)* | not filtering by title for routine review |
| Draft state | exclude drafts | don't review work-in-progress |
| Base branch | `is one of` → `main` | only PRs targeting the trunk |
| Labels | (none) | review everything, not just labeled PRs |

**Regex gotcha to know before you type one:** `matches regex` tests the
**entire field**, not a substring. `hotfix` only matches a title that is
*exactly* `hotfix`. To match "contains hotfix anywhere," write
`.*hotfix.*`, or just use the `contains` operator instead.

## The prompt

```
Review this pull request. Read the diff and the project's CLAUDE.md
conventions. Look for real bugs and public-behavior changes -- not style
nits. Post one comment: a one-sentence summary, a bulleted list of
findings (file:line, most severe first, or "No correctness issues
found"), and a PASS/FAIL verdict. Never invent an issue to seem thorough.
```

## The known limit this project's other half addresses

During the research preview, GitHub events have **per-routine and
per-account hourly caps**. Events past the cap are **dropped, not
queued**. On a quiet repo this never matters. On a busy one — a big
open-source project, a hackathon, a bot pushing dozens of PRs — some
PRs will simply never trigger a review, silently.

The fix isn't a bigger cap. It's a second, different heartbeat: a nightly
**reconciliation sweep** that lists every open PR and catches whatever
the event trigger missed. See `reconcile.py` below — it's built and
proven, not just described.
