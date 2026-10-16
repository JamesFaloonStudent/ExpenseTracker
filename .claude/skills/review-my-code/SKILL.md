---
name: review-my-code
description: Review the student's uncommitted changes (or a given file) and explain issues without rewriting their code. Use when asked to review, check, or give feedback on work in this repo.
---

This is explain-only coursework (see CLAUDE.md). Do not edit files or hand over corrected code.

1. Gather the changes: `git diff` and `git status` (include untracked files under `src/`). If `$ARGUMENTS` names a file or path, review that instead.
2. For each finding, give:
   - `file:line` and a one-line description of the problem
   - why it's wrong or risky (what breaks, and when)
   - a hint toward the fix, or a link to the relevant FastAPI / Jinja2 / boto3 / uv docs
3. Order findings by severity: bugs → things that will break later (paths, imports, packaging) → style/structure.
4. Keep it brief. Snippets only to illustrate a concept, never a drop-in replacement for their code.
