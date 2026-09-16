# Project 6 — The Doorbell

**Heartbeat type:** event-driven (Concept 7)
**What it teaches:** a loop that reacts the instant something happens —
a pull request opens — on a computer that was never yours, whether your
laptop is open or shut. No clock, no polling: nothing happens until
someone presses the doorbell.

## What's in this folder

```
06-the-doorbell/
├── .github/workflows/claude-pr-review.yml   # the actual GitHub Actions workflow
├── review-prompt.md                          # the reviewer's instructions
└── demo-repo/
    ├── cart.py                     # a file with two real, planted bugs
    └── review-output-example.md    # a REAL review of those bugs (see below)
```

## Why this project is split into "what I could run" and "what's yours"

The real Doorbell needs a GitHub repository, a push, and a repo secret —
three things that only exist on *your* GitHub account, not mine. I can't
fabricate those. What I *can* do, and did, is:

1. Build the real, working GitHub Actions workflow (below).
2. Prove the reviewer's instructions actually catch real bugs, by running
   them against real (verified, executable) broken code, locally.

That second part is the part worth reading closely — it's not a mockup.

## Proof it works: two real bugs, caught for real

I created a local git repo with a "PR": a branch (`feature/bulk-discount`)
that adds three functions to `cart.py`. Two of them are buggy. I did not
just eyeball the diff — I ran the code first, exactly the discipline
`review-prompt.md` demands ("don't invent an issue, and don't approve
based on a skim"):

```
$ python -c "from cart import total; print(total([10, 20, 30]))"
30                          # should be 60 -- off-by-one, drops the last item

$ python -c "..."           # mutable default argument test
['apple', 'banana']         # should be ['banana'] -- state leaked across calls
```

Both are real, common Python bugs. Then I performed the actual review,
following `review-prompt.md` exactly as `claude-code-action` would when it
fires. The output is `demo-repo/review-output-example.md`:

> **Findings:**
> - `cart.py:14` (`total`) — off-by-one bug... returns `30` instead of `60`.
> - `cart.py:20` (`add_item`) — mutable default argument... `'apple'`
>   leaks into the second call's result.
>
> **Verdict:** FAIL — two real bugs, both verified by running the code.

This is exactly what would land as a PR comment automatically, the moment
you push this branch and open a real pull request — the only thing
missing is GitHub actually being the one to trigger it.

## How to make it real (the steps only you can do)

1. **Push this folder to a GitHub repo you own**, with `.github/workflows/claude-pr-review.yml` in it.
2. **Get a token**, from your own machine (this uses your Pro/Max plan usage, not an API key):
   ```
   claude setup-token
   ```
3. **Add it as a repo secret**: Settings → Secrets and variables → Actions
   → New repository secret → name it `CLAUDE_CODE_OAUTH_TOKEN`, paste the
   token.
4. **Open a real pull request** with a real bug in it (or push
   `demo-repo/cart.py` as a branch in your new repo — the bugs are
   already there and verified).
5. Watch a review comment appear, unprompted, about a minute later.
6. **Close the laptop.** Have someone else open a PR. The review still
   appears — it's running on GitHub's runners, not yours. That's the
   whole concept, made visible.

## The one failure mode worth knowing about in advance

The course's own field notes on this flag it clearly, and it cost real
debugging time to learn: **a green checkmark on the Action run does not
mean a review got posted.** Miss one permission (`pull-requests: write` in
the workflow's `permissions:` block, shown above) or a misconfigured
token, and the job can complete "successfully" while posting nothing at
all. If you set this up and see green but no comment, check the job's own
logs (not just the checkmark) and re-verify the `permissions:` block and
the secret name match exactly.

## Run it automatically

I can't fire real GitHub Actions runners without your GitHub account, so
instead I ran the actual reviewing *logic* for real, against actual
(verified) bugs, and saved the unedited output — see
`demo-repo/review-output-example.md`. That is the same work
`claude-code-action` does; only the trigger (GitHub's servers noticing a
PR) is outside what I can execute here.

## The concept, made concrete

| In the course | In this project |
|---|---|
| Event-driven heartbeat | `on: pull_request: types: [opened, synchronize, reopened]` |
| "Runs on a computer that was never yours" | GitHub's own runners, once pushed — proven by the course's own doorbell project working with the laptop closed |
| A green checkmark isn't proof (Concept 14) | The permissions/token failure mode above |
| The checker doesn't invent issues | `review-prompt.md`: "Never invent an issue to seem thorough" |
