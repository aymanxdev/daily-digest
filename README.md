# 📰 Daily Digest

A self-updating archive of the tech world's daily highlights. Twice a day a
GitHub Action grabs the top stories from the [Hacker News](https://news.ycombinator.com)
front page; once a day another adds a random cat fact. Everything is committed
back to this repo and published to a small, searchable website — so the repo
stays alive on its own.

[![CI](https://github.com/aymanxdev/daily-digest/actions/workflows/ci.yml/badge.svg)](https://github.com/aymanxdev/daily-digest/actions/workflows/ci.yml)
[![Daily Dev News](https://github.com/aymanxdev/daily-digest/actions/workflows/news_updater.yml/badge.svg)](https://github.com/aymanxdev/daily-digest/actions/workflows/news_updater.yml)
[![Daily Fact Bot](https://github.com/aymanxdev/daily-digest/actions/workflows/daily_fact_workflow.yml/badge.svg)](https://github.com/aymanxdev/daily-digest/actions/workflows/daily_fact_workflow.yml)
[![Last commit](https://img.shields.io/github/last-commit/aymanxdev/daily-digest)](https://github.com/aymanxdev/daily-digest/commits/main)
[![Stories archived](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/aymanxdev/daily-digest/main/docs/stats.json)](https://aymanxdev.github.io/daily-digest/)

### 🔎 [Browse & search the archive →](https://aymanxdev.github.io/daily-digest/)

## How it works

| Piece | What it does |
| --- | --- |
| `update_news.py` | Fetches the top Hacker News stories and appends a dated digest to `daily_news.md`. |
| `daily_fact_bot.py` | Fetches a short cat fact and appends it to `facts.txt`. |
| `build_site.py` | Parses the whole archive into `docs/data.json` + `docs/stats.json` that power the site. |
| `cleanup_news.py` | Prunes `daily_news.md` to roughly the last month so it doesn't grow forever. |
| `docs/` | A dependency-free static site (GitHub Pages) with live client-side search over every headline. |

The workflows authenticate using the built-in, repo-scoped `GITHUB_TOKEN`
(`contents: write`) — there are no personal access tokens to expire or rotate.

## Schedule

| Workflow | When (UTC) |
| --- | --- |
| Daily Dev News | 09:00 and 15:00 |
| Daily Fact Bot | 16:00 |
| Monthly News Cleanup | 05:00 on the 1st of each month |

Both can also be run on demand from the **Actions** tab.

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python update_news.py      # append today's stories
python daily_fact_bot.py   # append a cat fact
python build_site.py       # rebuild the site data

pytest                     # run the tests
```

## Enabling the website

The site is served from the `docs/` folder. Under **Settings → Pages**, set the
source to **Deploy from a branch**, branch **`main`**, folder **`/docs`**. It
will appear at `https://aymanxdev.github.io/daily-digest/`.
