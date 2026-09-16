#!/usr/bin/env python3
"""Paper Watch: reports NEW arXiv papers on a topic since the last run.
Stdlib only. This is the spine (Concept 12) made concrete: progress.md is
the loop's only memory. Delete it and the loop forgets everything --
every paper comes back as "new". That's not a bug, it's the demo.

Usage:
    python scripts/paper_watch.py "LLM agents"
"""

import re
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

ATOM_NS = "{http://www.w3.org/2005/Atom}"
API = "https://export.arxiv.org/api/query"
PROGRESS_FILE = Path(__file__).resolve().parent.parent / "progress.md"


def fetch(topic: str, max_results: int = 10):
    query = urllib.parse.urlencode({
        "search_query": f"all:{topic}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    })
    with urllib.request.urlopen(f"{API}?{query}", timeout=20) as resp:
        xml_bytes = resp.read()
    root = ET.fromstring(xml_bytes)
    papers = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        arxiv_id = entry.find(f"{ATOM_NS}id").text.strip()
        short_id = re.search(r"abs/([\w.]+)", arxiv_id).group(1)
        title = entry.find(f"{ATOM_NS}title").text.strip().replace("\n", " ")
        title = re.sub(r"\s+", " ", title)
        papers.append({"id": short_id, "title": title})
    return papers


def load_seen() -> set:
    if not PROGRESS_FILE.exists():
        return set()
    text = PROGRESS_FILE.read_text(encoding="utf-8")
    section = re.search(r"## Already shown\n(.*?)(?=\n## |\Z)", text, re.S)
    if not section:
        return set()
    return set(re.findall(r"^- (\S+)", section.group(1), re.M))


def save_state(topic: str, seen: set, new_papers: list):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Paper Watch — memory (the spine)", ""]
    lines.append("This file is the loop's only memory. Delete it and every")
    lines.append("paper comes back as \"new\" on the next run.")
    lines.append("")
    lines.append("## Already shown")
    for pid in sorted(seen):
        lines.append(f"- {pid}")
    lines.append("")
    lines.append("## Log")
    if PROGRESS_FILE.exists():
        old = PROGRESS_FILE.read_text(encoding="utf-8")
        old_log = re.search(r"## Log\n(.*)", old, re.S)
        prior_log_lines = old_log.group(1).rstrip("\n") if old_log else ""
    else:
        prior_log_lines = ""
    if new_papers:
        lines.append(f"- {now}: reported {len(new_papers)} new paper(s) for \"{topic}\"")
    else:
        lines.append(f"- {now}: nothing new for \"{topic}\"")
    if prior_log_lines:
        lines.append(prior_log_lines)
    PROGRESS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "LLM agents"
    papers = fetch(topic)
    seen = load_seen()
    new_papers = [p for p in papers if p["id"] not in seen]

    if not new_papers:
        print(f'Paper Watch - "{topic}": nothing new since last run [OK]')
    else:
        print(f'Paper Watch — "{topic}": {len(new_papers)} new paper(s):')
        for p in new_papers:
            print(f"  - [{p['id']}] {p['title']}")

    seen.update(p["id"] for p in papers)
    save_state(topic, seen, new_papers)


if __name__ == "__main__":
    main()
