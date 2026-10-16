# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Academic integrity — explain-only

This is graded coursework. Do not write solution code, implement features, or edit files under `src/` unless the user explicitly asks for that specific edit. Instead: explain concepts, point out bugs and why they happen, suggest approaches, and link to docs. Small generic examples (not drop-in project code) are fine.

## Stack

- Python 3.13, FastAPI, server-rendered Jinja2 templates (not a JSON API). Package manager is **uv** (`uv sync`, `uv add <pkg>`, `uv run ...`) — don't use pip.
- Planned database: DynamoDB on AWS (boto3). Not wired in yet; no ORM/migrations.
- Lint/format with ruff (config in `pyproject.toml`): `uv run ruff check src`, `uv run ruff format src`. A hook auto-formats `.py` files after Claude edits them.
- No tests or CI exist yet.

## Running

Run from `src/expensetracker/` — `Jinja2Templates(directory="Views")` is resolved relative to the current working directory:

```
cd src/expensetracker && uv run fastapi dev main.py
```

## Known gotchas

- Template dir is `Views/` (capital V; Linux is case-sensitive).
- `[project.scripts] expensetracker = "expensetracker:main"` is broken — `__init__.py` defines no `main`.
- `routers/` and `models/` have no `__init__.py`; `routers/mainPage.py` is an unfinished split of routes out of `main.py`.
- `dockerfile` is lowercase and empty; `docker build` needs `-f dockerfile` unless renamed.
