# Project 2 — Build Your Portfolio

**Heartbeat type:** conditional / run-until-done, `/goal` (Concept 5)
**What it teaches:** a loop that stops because a checked condition is true,
not because a timer says so — and that "done" needs two different kinds of
checker: a script for what's provable, a second agent for what's a
judgment call.

## What's in this folder

```
02-portfolio-builder/
├── my-cv.md                       # sample CV — replace with your own
├── spec.md                        # the stopping condition, Part A + Part B
├── check.py                       # 22 mechanical checks, stdlib only
├── .claude/agents/reviewer.md     # the checker for the 6 judgment promises
└── site/
    ├── index.html                 # a passing demo build (see below)
    └── style.css
```

## Proof it works (already run for you)

I built `site/` from `my-cv.md` by hand and ran the checker:

```
$ python check.py site
[PASS] site/index.html exists
...
22/22
```

All 22 mechanical checks pass. While building this I actually found **two
real bugs in `check.py` itself** — worth knowing about, because it's the
exact "don't edit the checker" trap the spec warns about, from the other
side:

1. The color-contrast check's regex matched `background-color:` when
   looking for plain `color:`, so it always compared the background
   against itself. Fixed with a negative lookbehind (`(?<!-)\bcolor`).
2. The About-section word-count regex stopped capturing at the section's
   *own* `<h2>` heading, so it always measured 0 words. Fixed by capturing
   up to the matching `</section>` instead.

Both were fixed in `check.py` — not by loosening a rule, but because the
checks were provably wrong (a human reading the CSS/HTML could see the
regex logic didn't match what the English description promised). That
distinction — fix the checker because it's buggy vs. fix it because it's
inconvenient — is the whole lesson of "never edit check.py to make it
pass."

I also proved the checker actually discriminates, not just rubber-stamps,
by running it against a deliberately broken stub page:

```
$ python check.py <broken-stub>
[FAIL] file is non-trivial (>2000 bytes)
[FAIL] "about" section present
[FAIL] no leftover placeholder text     <- caught "Lorem ipsum... TODO"
...
10/22
```

**Part B (judgment).** I also self-reviewed the demo site against the six
promises in `spec.md`, since I (the model) built it with the CV in hand:

| Promise | Verdict |
|---|---|
| 1. Traceable to the CV | PASS — every number (800ms→120ms, 2M tx/day, ~400 stars) is from `my-cv.md`, nothing invented |
| 2. Designed, not formatted | PASS — custom palette, serif/sans pairing, pill-shaped skill tags, deliberate spacing scale |
| 3. More than a PDF | PASS, with a caveat — clean and hierarchical, but conservative; a stronger build could lean harder into layout |
| 4. Consistent voice | PASS — About is first-person/conversational by design, Experience is resume-style by convention; not accidental mixing |
| 5. Clear hierarchy | PASS — name/tagline first, then sections in a deliberate order |
| 6. Nothing embarrassing | PASS |

**Important honesty note:** this Part B verdict is a *self-review* — I
was both the maker and the checker, which is exactly the setup Concept 11
warns against ("a model that checks its own output often approves it too
easily"). It's good enough to prove the rubric is answerable, but it is
**not** a substitute for the real loop. When you run this for real,
`/goal` hands Part B to a fresh model instance via `.claude/agents/reviewer.md`,
which has never seen the site being built and has no reason to be lenient.

## How to run it yourself

1. Replace `my-cv.md` with your own CV (plain text/markdown is easiest;
   a PDF works too if you tell Claude to read it).
2. ```
   cd "E:\Loop Engineering Projects\02-portfolio-builder"
   claude
   ```
3. Paste the `/goal` command from the bottom of `spec.md`:
   ```
   /goal Build my portfolio in site/ from my-cv.md, following spec.md. Done
   when `python check.py site` prints 22/22 and the reviewer agent replies
   PASS on all six judgment promises in spec.md — show me both results. Stop
   after 15 check attempts or 3 review rounds and write what is still failing
   to progress.md.
   ```
4. Walk away. It will read your CV, design a page, write it, run
   `check.py`, read its own failures, and retry — until both bars clear or
   it hits the cap.

**Note:** `/goal` is a research-preview command. If it doesn't exist in
your installed CLI version, run `/help` inside a `claude` session to check
— the same result is achievable by hand: build, run `python check.py site`,
fix what fails, repeat, then separately ask a fresh Claude session to grade
against the six promises in `spec.md`.

## Run it automatically (why I didn't spend your Claude usage on it)

The mechanical half (`check.py`) needs no LLM at all — I ran it for real,
twice, above (pass case and fail case), with zero tokens spent. That's the
part any CI system could run unattended forever.

The generative half (writing the site, and the six-promise review) is
inherently an LLM doing judgment work. I did one real pass of both by
hand — building the demo site as "maker" and grading it as "checker" —
using capability I already have in this conversation, at no extra cost to
you. What I deliberately *didn't* do is shell out to a second, separate
`claude` process on your machine to run the full `/goal` retry loop,
because that spends your actual Claude Code usage/quota. That step is
yours to kick off in step 2 above, so you can watch it work and control
the cost.

## The concept, made concrete

| In the course | In this project |
|---|---|
| Success condition | `check.py` prints 22/22 |
| Limit | "stop after 15 check attempts or 3 review rounds" in the `/goal` command |
| No-progress check | (not built in here — `/goal` has no automatic one; the attempt cap substitutes for it) |
| Checker ≠ maker | `.claude/agents/reviewer.md` runs as a separate agent instance |
| Checker ladder (Concept 2) | Part A = proof (a command), Part B = a claim (a model's judgment) |
