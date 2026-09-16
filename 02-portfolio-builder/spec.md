# Spec: build a one-page portfolio site from a CV

## Goal

Read `my-cv.md` (or `my-cv.pdf` if you dropped one in) and build a single
polished HTML portfolio page at `site/index.html`, with styling at
`site/style.css`. This is the stopping condition for the `/goal` loop.

## Part A — mechanical checks (a machine can prove these)

Run `python check.py site` from this folder. It runs 22 checks against
`site/index.html` and `site/style.css`. Done means it prints `22/22`.

**Never edit `check.py` to make it pass.** If a check feels wrong, that is
a signal to fix the site, or to say so and stop — not to weaken the check.
Editing the checker to chase a green result is exactly the failure mode
this project exists to teach you to notice in yourself.

## Part B — judgment (a second agent must grade these; a script cannot)

A reviewer agent (see `.claude/agents/reviewer.md`) must reply PASS on all
six of the following. This is the real bar — 22/22 on Part A is necessary
but not sufficient:

1. **Traceable.** Every claim on the page is traceable to something in the
   CV. Nothing is invented, exaggerated, or padded.
2. **Designed, not formatted.** The visual design (typography, spacing,
   color, layout) reflects deliberate choices, not default browser styling
   with a font swap.
3. **More than a PDF.** The page uses the medium — hierarchy, layout,
   maybe light interactivity — to communicate better than a linear CV
   document would. If it reads like a PDF pasted into HTML, it fails this.
4. **Consistent voice.** The writing doesn't read like copy-pasted CV
   bullet fragments stitched to generic filler sentences.
5. **Clear hierarchy.** The most important information (who this person
   is, what they're best at) is visually first. Not everything has equal
   weight.
6. **Nothing embarrassing.** No awkward phrasing, broken layout, unfinished
   section, or placeholder text a stranger would notice in five seconds.

## Stopping condition

Not every Claude Code build ships the `/goal` slash command (it's a
research preview and may not be registered in your session — if you type
`/goal` and it says the command doesn't exist, use the plain-language
version below; both express the exact same success condition, limit, and
maker-checker split, just one is a wrapper and the other is spelled out).

**Plain language (works everywhere — paste as a normal message):**

```
Build my portfolio in site/ from my-cv.md, following spec.md in this folder.

Work in a loop:
1. Draft or update site/index.html and site/style.css.
2. Run `python check.py site` yourself and read the output.
3. Fix whatever fails, and run it again.
4. Repeat until it prints 22/22.

Then, once it's 22/22: re-read my-cv.md and site/ fresh, and grade the
result against the six judgment promises in spec.md, as a strict reviewer
would — reply PASS or FAIL on each of the six, with a reason.

If any promise fails, fix the site and re-check both check.py and the
promises again.

Stop after at most 15 check-script attempts or 3 full review rounds. If
you still haven't reached 22/22 + all-PASS by then, write exactly what's
still failing to progress.md and stop there — don't keep retrying past
the cap.
```

**If `/goal` exists in your CLI:**

```
/goal Build my portfolio in site/ from my-cv.md, following spec.md. Done
when `python check.py site` prints 22/22 and the reviewer agent replies
PASS on all six judgment promises in spec.md — show me both results. Stop
after 15 check attempts or 3 review rounds and write what is still failing
to progress.md.
```

## Rules

- Do not fabricate experience, numbers, or projects not present in the CV.
- Do not edit `check.py`.
- Keep it to one page. No build tooling, no framework — plain HTML/CSS is
  enough and keeps Part A checks simple to reason about.
