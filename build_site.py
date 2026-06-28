"""Generate the static GitHub Pages digest site data from the archives.

Parses ``daily_news.md`` into structured digests and writes the JSON files
that ``docs/index.html`` loads for browsing and search. Also emits a small
``stats.json`` consumed by the README "stories archived" badge.
"""

import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse
from xml.sax.saxutils import escape

NEWS_FILE_PATH = "daily_news.md"
FACTS_FILE_PATH = "facts.txt"
OUT_DIR = "docs"

HEADER_RE = re.compile(r"^##\s+(.*?)\s+Digest\s+-\s+(\d{2}-\d{2}-\d{4})\s*$")
STORY_RE = re.compile(r"^-\s+\[(.*)\]\((.*)\)\s*$")


def parse_archive(text):
    """Parse the news Markdown into a list of digest dicts (newest first).

    Each digest is ``{"period": str, "date": "DD-MM-YYYY"|None,
    "stories": [{"title", "url"}]}``. Stories that appear before the first
    dated header are grouped into an undated "Earlier" digest.
    """
    digests = []
    current = None

    def flush():
        if current and current["stories"]:
            digests.append(current)

    for line in text.splitlines():
        header = HEADER_RE.match(line)
        if header:
            flush()
            current = {"period": header.group(1), "date": header.group(2), "stories": []}
            continue
        story = STORY_RE.match(line)
        if story:
            if current is None:
                current = {"period": "Earlier", "date": None, "stories": []}
            current["stories"].append({"title": story.group(1), "url": story.group(2)})
    flush()

    def sort_key(digest):
        if not digest["date"]:
            return (datetime.min, 0)
        day = datetime.strptime(digest["date"], "%d-%m-%Y")
        # Keep the Morning digest above the Afternoon one within a single day.
        period_rank = 0 if digest["period"].lower().startswith("morning") else 1
        return (day, period_rank)

    digests.sort(key=sort_key, reverse=True)
    return digests


def top_domains(digests, limit=8):
    """Return the most-linked source domains as a list of (domain, count)."""
    counts = Counter()
    for digest in digests:
        for story in digest["stories"]:
            host = (urlparse(story["url"]).hostname or "").lower()
            if host.startswith("www."):
                host = host[4:]
            if host:
                counts[host] += 1
    return counts.most_common(limit)


def render_chart_svg(domains):
    """Render the top domains as a self-contained horizontal bar-chart SVG."""
    width, bar_h, gap, pad_left, pad_top = 720, 22, 12, 210, 46
    rows = max(len(domains), 1)
    height = pad_top + rows * (bar_h + gap) + 8
    bar_max = width - pad_left - 70
    busiest = max((count for _, count in domains), default=1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" font-family="-apple-system, Segoe UI, sans-serif" '
        f'font-size="13">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#0d1117"/>',
        f'<text x="20" y="28" font-size="15" font-weight="bold" '
        f'fill="#e6edf3">Most-linked sources</text>',
    ]
    for i, (host, count) in enumerate(domains):
        y = pad_top + i * (bar_h + gap)
        bar_w = int(bar_max * count / busiest)
        parts.append(
            f'<text x="{pad_left - 10}" y="{y + bar_h - 6}" text-anchor="end" '
            f'fill="#8b949e">{escape(host)}</text>'
        )
        parts.append(
            f'<rect x="{pad_left}" y="{y}" width="{bar_w}" height="{bar_h}" '
            f'rx="4" fill="#58a6ff"/>'
        )
        parts.append(
            f'<text x="{pad_left + bar_w + 8}" y="{y + bar_h - 6}" '
            f'fill="#e6edf3">{count}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def count_nonblank_lines(path):
    """Count non-blank lines in a file (0 if it does not exist)."""
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def build(news_path=NEWS_FILE_PATH, facts_path=FACTS_FILE_PATH, out_dir=OUT_DIR, now=None):
    """Write data.json and stats.json into ``out_dir`` and return the stats."""
    now = now or datetime.now(timezone.utc)
    with open(news_path, encoding="utf-8") as handle:
        digests = parse_archive(handle.read())

    story_count = sum(len(digest["stories"]) for digest in digests)
    fact_count = count_nonblank_lines(facts_path)

    os.makedirs(out_dir, exist_ok=True)

    data = {"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "digests": digests}
    with open(os.path.join(out_dir, "data.json"), "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, separators=(",", ":"))

    chart = render_chart_svg(top_domains(digests))
    with open(os.path.join(out_dir, "chart.svg"), "w", encoding="utf-8") as handle:
        handle.write(chart)

    # Shields.io endpoint badge schema, with extra fields the site can read.
    stats = {
        "schemaVersion": 1,
        "label": "stories archived",
        "message": str(story_count),
        "color": "blue",
        "stories": story_count,
        "facts": fact_count,
        "digests": len(digests),
        "updated": now.strftime("%Y-%m-%d"),
    }
    with open(os.path.join(out_dir, "stats.json"), "w", encoding="utf-8") as handle:
        json.dump(stats, handle, ensure_ascii=False, indent=2)

    return stats


if __name__ == "__main__":
    result = build()
    print(
        f"Built site: {result['stories']} stories across "
        f"{result['digests']} digests, {result['facts']} facts."
    )
