---
name: explain
description: Explain a concept, error message, or piece of this codebase (FastAPI, Jinja2 templates, DynamoDB/boto3, uv) without writing solution code. Use when the student asks how or why something works or what an error means.
---

This is explain-only coursework (see CLAUDE.md).

Topic: $ARGUMENTS

1. If it relates to code in this repo, read the relevant files first and ground the explanation in them (`file:line`).
2. For an error: say what it means, the likely cause here, and how to confirm it — let the student apply the fix.
3. Use small, generic examples (different names/domain than this project) rather than code that could be pasted into `src/`.
4. Keep it brief and end with a link to the official docs section.
