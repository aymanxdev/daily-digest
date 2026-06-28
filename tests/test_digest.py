from datetime import datetime, timezone

import build_site
import cleanup_news
import daily_fact_bot
import update_news

SAMPLE = """# Daily Dev News Summary

- [Orphan story](https://example.com/orphan)
## Morning Digest - 17-09-2023

- [Story A](https://a.example)
- [Story B](https://b.example)
## Afternoon/Evening Digest - 17-09-2023

- [Story C](https://c.example)
"""


def test_format_digest_morning():
    now = datetime(2026, 6, 28, 9, 0)
    out = update_news.format_digest([("Hello", "https://example.com")], now=now)
    assert out.startswith("## Morning Digest - 28-06-2026")
    assert "- [Hello](https://example.com)\n" in out


def test_format_digest_afternoon():
    now = datetime(2026, 6, 28, 15, 0)
    out = update_news.format_digest([("Title", "https://u.example")], now=now)
    assert "Afternoon/Evening Digest - 28-06-2026" in out


def test_parse_archive_groups_and_sorts():
    digests = build_site.parse_archive(SAMPLE)
    # Newest first: afternoon 17th, then morning 17th, then the undated orphan.
    assert digests[0]["period"].startswith("Afternoon")
    assert digests[0]["stories"][0]["title"] == "Story C"
    assert digests[-1]["period"] == "Earlier"
    titles = [s["title"] for d in digests for s in d["stories"]]
    assert "Orphan story" in titles


def test_build_writes_json(tmp_path):
    news = tmp_path / "news.md"
    news.write_text(SAMPLE, encoding="utf-8")
    facts = tmp_path / "facts.txt"
    facts.write_text("fact one\nfact two\n\n", encoding="utf-8")
    out = tmp_path / "site"
    now = datetime(2026, 6, 28, 12, 0, tzinfo=timezone.utc)

    stats = build_site.build(str(news), str(facts), str(out), now=now)

    assert stats["stories"] == 4
    assert stats["facts"] == 2
    assert stats["digests"] == 3
    assert stats["updated"] == "2026-06-28"
    assert (out / "data.json").exists()
    assert (out / "stats.json").exists()
    assert (out / "chart.svg").exists()


def test_top_domains_counts_and_strips_www():
    digests = build_site.parse_archive(
        "## Morning Digest - 20-06-2026\n\n"
        "- [One](https://www.example.com/a)\n"
        "- [Two](https://example.com/b)\n"
        "- [Three](https://other.org/c)\n"
    )
    counts = dict(build_site.top_domains(digests))
    assert counts["example.com"] == 2
    assert counts["other.org"] == 1


def test_render_chart_svg_is_wellformed():
    svg = build_site.render_chart_svg([("example.com", 3), ("other.org", 1)])
    assert svg.startswith("<svg") and svg.endswith("</svg>")
    assert "example.com" in svg


def test_write_fact(tmp_path):
    path = tmp_path / "facts.txt"
    daily_fact_bot.write_fact("Cats sleep a lot", str(path))
    assert path.read_text(encoding="utf-8") == "Cats sleep a lot\n"


def test_prune_keeps_recent_drops_old():
    now = datetime(2026, 6, 28, 12, 0)
    text = (
        "## Morning Digest - 01-01-2020\n\n- [Old](https://old.example)\n"
        "## Morning Digest - 20-06-2026\n\n- [Recent](https://recent.example)\n"
    )
    out = cleanup_news.prune(text, now=now)
    assert "Recent" in out and "20-06-2026" in out
    assert "Old" not in out and "01-01-2020" not in out


def test_prune_output_is_reparseable():
    now = datetime(2026, 6, 28, 12, 0)
    text = (
        "## Morning Digest - 20-06-2026\n\n"
        "- [A](https://a.example)\n- [B](https://b.example)\n"
    )
    digests = build_site.parse_archive(cleanup_news.prune(text, now=now))
    assert len(digests) == 1
    assert [s["title"] for s in digests[0]["stories"]] == ["A", "B"]
