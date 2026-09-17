# How to run every project

Baseline, already confirmed installed on this machine: Python 3.13.2,
Node 22, git, Claude Code CLI 2.1.214, curl. Nothing else needs
installing unless a project below says so.

Two commands you'll see repeated: `/goal` and `/schedule` are research-preview
Claude Code slash commands that may not exist in your CLI build (confirmed
missing in this session). Every project that uses them gives a
plain-language fallback that does the identical thing — use whichever
your `claude` session actually accepts; type `/help` in a session to check.

---

## Project 1 — ISS Watch
**Requirements:** none extra.
**Steps:**
1. `cd "E:\Loop Engineering Projects\01-iss-watch-loop"`
2. `claude`
3. Say yes when asked to trust the folder.
4. Type: `/loop show me the location of the ISS every minute`
5. To stop: type `cancel the iss loop`, or just close the terminal.

**Quick manual check (no Claude needed):** `python scripts/iss_location.py`

---

## Project 2 — Portfolio Builder
**Requirements to add before running:** replace `my-cv.md` with your own
CV (plain text/markdown is easiest; a PDF works too — just tell Claude to
read it). The sample CV works fine if you just want to see the loop run.
**Steps:**
1. `cd "E:\Loop Engineering Projects\02-portfolio-builder"`
2. `claude`
3. Paste the plain-language block at the top of the "Stopping condition"
   section in `spec.md` (or the `/goal ...` version if your build has it).
4. Walk away — it drafts `site/`, runs `python check.py site` itself,
   fixes failures, and separately grades the six judgment promises.

**Quick manual check:** `python check.py site` (currently shows 22/22 on
the demo site I built).

---

## Project 3 — Sky Watch
**Requirements:** none — your personal NASA API key is already wired in
(set as a persistent env var and hardcoded as a fallback in
`run_and_log.ps1`), no longer on the shared `DEMO_KEY`.
**Note:** a real Windows Scheduled Task is already registered and firing
daily at 8:00 AM on this machine, confirmed working with your key
(`LastTaskResult 0`).
**Steps:**
1. Manual run: `cd "E:\Loop Engineering Projects\03-sky-watch"` then
   `python scripts\sky_watch.py`
2. Check the live schedule:
   ```powershell
   Get-ScheduledTask -TaskName "LoopEngineering-SkyWatch" | Get-ScheduledTaskInfo
   Get-Content "E:\Loop Engineering Projects\03-sky-watch\logs\sky-watch.log" -Tail 20
   ```
3. To remove the scheduled task:
   ```powershell
   Unregister-ScheduledTask -TaskName "LoopEngineering-SkyWatch" -Confirm:$false
   ```
4. Via Claude Code instead: `claude` then
   `/schedule every day at 8am, run the sky-watch skill and write me the forecast`

---

## Project 4 — Paper Watch
**Requirements:** none extra.
**Note:** a second real Scheduled Task is already registered, firing
daily at 8:15 AM.
**Steps:**
1. `cd "E:\Loop Engineering Projects\04-paper-watch"`
2. `python scripts\paper_watch.py "LLM agents"` — run it twice to see it
   say "nothing new" the second time.
3. To watch it forget: `rm progress.md` (or delete the file in Explorer),
   then run the script again — everything comes back as "new".
4. Check the live schedule / remove it: same commands as Project 3, with
   `-TaskName "LoopEngineering-PaperWatch"`.

---

## Project 5 — Worktree Isolation Demo
**Requirements:** none extra (git already installed).
**Steps:**
1. `cd "E:\Loop Engineering Projects\05-worktree-isolation"`
2. `bash run_demo.sh`
3. Read the output top to bottom — Step A shows a real fix getting lost,
   Step B shows the same two fixes surviving via worktrees.

Safe to re-run any time; it rebuilds `demo-repo/` from scratch each time.

---

## Project 6 — The Doorbell
**Requirements:** `CLAUDE_CODE_OAUTH_TOKEN` is already set as a repo
secret on your GitHub repo (confirmed the workflow file references the
exact same name). Only remaining step is pushing the code and opening a PR.

**Steps:**
1. Push this folder's contents (including `.github/workflows/claude-pr-review.yml`)
   to the GitHub repo where you set the secret, if not already done.
2. Open a real pull request (the bugs in `demo-repo/cart.py` are already
   there and verified — push that as a branch and open a PR against it,
   or use your own code).
3. Wait about a minute — a review comment appears automatically.
4. Optional proof of the "event-driven, laptop-closed" concept: close
   your laptop and have someone else open a PR. The review still appears.

**If you just want to see the review logic without any of the above:**
read `demo-repo/review-output-example.md` — a real review I already
performed against the real (verified) bugs in that file.

**Known gotcha:** a green Action checkmark doesn't guarantee a comment
posted — check the `permissions:` block in the workflow file and the
secret name match exactly if nothing shows up.

---

## Project 7 — Connector-Powered Issue Triager
**Requirements:** none extra.
**Steps:**
1. `cd "E:\Loop Engineering Projects\07-connector-triager"`
2. `python triage.py`
3. Run it again — watch `created` become `updated` and the ticket count
   stay flat (proof of idempotency).
4. Optional: inspect `tickets.json` to see the stored state.

---

## Project 8 — Full Morning-Triage Loop
**Requirements:** none extra for the scripted version. For the real
Claude Code version, just a working `claude` session (uses your usage).
**Steps (scripted, free, already proven):**
1. `cd "E:\Loop Engineering Projects\08-morning-triage"`
2. `bash run_loop.sh`
3. Read `progress.md` afterward — two "Done" entries, one "needs a human".

**Steps (via Claude Code, on a real repo):**
1. Point `.claude/skills/daily-triage/SKILL.md` and
   `.claude/agents/reviewer.md` at your actual repo (replace `demo-repo`
   references).
2. `claude` → `run the daily-triage skill`

---

## Project 9 — Routine Drill: Basic Cloud Routine
**Requirements to add before running (for the real Routine only):** a
claude.ai account with Routines access (research preview).
**Steps (the automated part, no account needed):**
1. `cd "E:\Loop Engineering Projects\09-routine-drill-basic"`
2. `python checklist.py routine-prompt.md` → should print 7/7.

**Steps (to actually create the Routine):**
1. Go to `claude.ai/code/routines` (or Desktop app → Routines → New
   routine → **Remote**).
2. Paste `routine-prompt.md` as the prompt.
3. Fill in repo / connector / trigger using the table in this project's
   `README.md`.
4. Fire it once with "Run now" before trusting the schedule.

---

## Project 10 — Routine Drill: API-Triggered Routine
**Requirements:** none extra — runs entirely on `127.0.0.1`.
**Steps:**
1. `cd "E:\Loop Engineering Projects\10-routine-drill-api"`
2. `python demo.py`
3. Read the three parts in the output: bad-token error, retry storm
   (3 wasted runs), and caller-side dedup (1 run, as it should be).

---

## Project 11 — Routine Drill: GitHub-Event Routine + Reconciliation Sweep
**Requirements to add before running (for the real trigger only):**
install the Claude GitHub App on your repo (Settings → Integrations —
**not** the same as `/web-setup`, which only grants clone access).
**Steps (the automated part, no account needed):**
1. `cd "E:\Loop Engineering Projects\11-routine-drill-github-event"`
2. `python reconcile.py` → catches 4 "dropped" PRs.
3. Run it again → "nothing missed" (idempotent).

**Steps (to actually create the trigger):** use the field table in
`routine-github-trigger-config.md`.

---

## Project 12 — Weekly Capstone: Dreaming / Improvement Loop
**Requirements:** none extra.
**Steps:**
1. `cd "E:\Loop Engineering Projects\12-dreaming-capstone"`
2. `python dream.py` → finds the seeded pattern, drafts a proposal branch
   in `target-repo/` (does NOT merge it).
3. Review it: `cd target-repo && git show claude/dreaming-update-2026-09-16`
4. Approve it (or don't): `git merge claude/dreaming-update-2026-09-16`
5. Run `python dream.py` again from the parent folder → confirms its own
   spine (`dreaming-state.md`) stops it from re-analyzing the same week.

---

## Summary: what needs YOUR input before it'll do something new

| Project | What only you can provide |
|---|---|
| 2 | Your real CV (optional — sample works) |
| 3 | ~~NASA API key~~ done |
| 6 | ~~GitHub secret~~ done — just push + open a PR |
| 8 (real version) | Point it at your actual repo |
| 9 | A claude.ai account with Routines access, to create the real Routine |
| 11 (real version) | Claude GitHub App installed on your repo |

Everything else runs as-is, right now, with what's already in each folder.
