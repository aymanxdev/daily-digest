"""Prune daily_news.md to roughly the most recent month of digests.

Run monthly by .github/workflows/cleanup.yml. Digests older than the cutoff
are dropped from the news file; build_site.py then regenerates the site, so
the published archive tracks the same rolling window.
"""

from datetime import datetime, timedelta

from build_site import parse_archive

NEWS_FILE_PATH = "daily_news.md"
KEEP_DAYS = 31


def render(digests):
    """Render digests (oldest first) back into the news Markdown format."""
    blocks = []
    for digest in digests:
        if not digest["date"]:
            continue
        block = f"## {digest['period']} Digest - {digest['date']}\n\n"
        block += "".join(f"- [{s['title']}]({s['url']})\n" for s in digest["stories"])
        blocks.append(block)
    return "".join(blocks)


def prune(text, now=None, keep_days=KEEP_DAYS):
    """Return the news text with digests older than ``keep_days`` removed."""
    now = now or datetime.now()
    cutoff = now.date() - timedelta(days=keep_days)
    digests = parse_archive(text)  # newest first
    kept = [
        d
        for d in digests
        if d["date"] and datetime.strptime(d["date"], "%d-%m-%Y").date() >= cutoff
    ]
    kept.reverse()  # oldest first, matching how the file is appended
    return render(kept)


def main():
    with open(NEWS_FILE_PATH, encoding="utf-8") as handle:
        text = handle.read()
    pruned = prune(text)
    with open(NEWS_FILE_PATH, "w", encoding="utf-8") as handle:
        handle.write(pruned)


if __name__ == "__main__":
    main()
