#!/usr/bin/env python3
"""Part A checker for the portfolio project. Stdlib only, no deps.

Usage: python check.py <site-dir>
Prints one line per check plus a final N/20 summary and exits 1 on any
failure (so it can be used as a loop stopping condition).

Never edit this file to make it pass. If a check feels wrong, fix the
site, or say so and stop.
"""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["about", "experience", "skills", "projects", "contact"]
PLACEHOLDER_MARKERS = [
    "lorem ipsum", "todo", "[your name]", "[insert", "placeholder",
    "your email here", "example.com/you",
]


def load(site_dir: Path):
    index = site_dir / "index.html"
    css_candidates = list(site_dir.glob("*.css"))
    html = index.read_text(encoding="utf-8") if index.exists() else ""
    css = ""
    if css_candidates:
        css = css_candidates[0].read_text(encoding="utf-8")
    else:
        # allow embedded <style> as a substitute for a separate file
        m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
        if m:
            css = m.group(1)
    return index, html, css


def run_checks(site_dir: Path):
    index, html, css = load(site_dir)
    low = html.lower()
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, ok, detail))

    check("site/index.html exists", index.exists())
    check("file is non-trivial (>2000 bytes)", len(html) > 2000)
    check("file isn't bloated (<500000 bytes)", len(html) < 500_000)
    check("has <!DOCTYPE html>", low.strip().startswith("<!doctype html"))
    check("has <html> and </html>", "<html" in low and "</html>" in low)
    check("has non-empty <title>", bool(re.search(r"<title>\s*\S+.*?</title>", html, re.I)))
    check("has a responsive viewport meta tag",
          bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.I)))
    check("has at least one <h1>", bool(re.search(r"<h1[\s>]", low)))

    for section in REQUIRED_SECTIONS:
        check(f'"{section}" section present',
              section in low)

    check("contact section includes an email address",
          bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", html)))

    check("no leftover placeholder text",
          not any(marker in low for marker in PLACEHOLDER_MARKERS))

    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    imgs_with_alt = [i for i in imgs if re.search(r'alt\s*=\s*"[^"]+"', i, re.I)]
    check("every <img> has a non-empty alt attribute",
          len(imgs) == len(imgs_with_alt), f"{len(imgs_with_alt)}/{len(imgs)} images have alt text")

    check("stylesheet present (external or embedded)", len(css.strip()) > 0)

    body_color = re.search(r"body\s*{[^}]*(?<!-)\bcolor\s*:\s*([^;]+);", css, re.I)
    body_bg = re.search(r"body\s*{[^}]*\bbackground(?:-color)?\s*:\s*([^;]+);", css, re.I)
    same_color = False
    if body_color and body_bg:
        c1 = body_color.group(1).strip().lower()
        c2 = body_bg.group(1).strip().lower()
        same_color = c1 == c2
    check("body text color != body background color", not same_color)

    check("no script tags pointing at arbitrary external hosts",
          not re.search(r'<script[^>]+src=["\']https?://(?!fonts\.|cdn\.jsdelivr\.net)', html, re.I))

    about_match = re.search(r'id=["\']about["\'][^>]*>(.*?)</section>', html, re.I | re.S)
    about_text = re.sub("<[^>]+>", " ", about_match.group(1)) if about_match else ""
    word_count = len(about_text.split())
    check("about section has 15-400 words", 15 <= word_count <= 400, f"{word_count} words")

    internal_links = re.findall(r'href=["\']#([\w-]+)["\']', html)
    ids_present = set(re.findall(r'id=["\']([\w-]+)["\']', html))
    broken = [l for l in internal_links if l not in ids_present]
    check("no broken internal anchor links", len(broken) == 0, f"broken: {broken}" if broken else "")

    check("has a meaningful <meta name=\"description\">",
          bool(re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']{20,}', html, re.I)))

    return checks


def main():
    if len(sys.argv) != 2:
        print("usage: python check.py <site-dir>")
        sys.exit(2)
    site_dir = Path(sys.argv[1])
    checks = run_checks(site_dir)
    passed = 0
    for name, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        line = f"[{mark}] {name}"
        if detail:
            line += f" — {detail}"
        print(line)
        if ok:
            passed += 1
    print(f"\n{passed}/{len(checks)}")
    sys.exit(0 if passed == len(checks) else 1)


if __name__ == "__main__":
    main()
