# Mistake Summary Rules

Use this file when the user wants to review past mistakes, summarize archived notebooks, or identify weak points from completed exercises.

## Goal

Turn archived `notebook.md` files into a compact revision summary.

This mode should:

- scan `archives/**/notebook.md`
- read `metadata.json` when present
- group notes by archive topic
- summarize repeated stuck points, mistakes, commands to revisit, and reminders
- write the result to `archives/_summaries/`

## Trigger Examples

Use this mode for requests such as:

- "我想复习一下我之前的错因"
- "总结一下归档里的 notebook"
- "帮我看我最常错什么"
- "按归档笔记给我做一份复习总结"

If the user simply says "我想复习" and archived notebooks exist, prefer this mode before generating a new question.

## Inputs

Primary sources:

- `archives/<topic>/<testNN>/notebook.md`
- `archives/<topic>/<testNN>/metadata.json`

Helpful fields:

- `我卡住的点`
- `我做错的点`
- `需要记住的命令/选项`
- `下次再做这题时要提醒自己的话`

## Output

Write at least:

- `archives/_summaries/mistake-summary.md`
- `archives/_summaries/mistake-summary.json`

If the user asks for one topic only, allow:

- `mistake-summary-<topic>.md`
- `mistake-summary-<topic>.json`

## Summary Content

The markdown summary should contain:

1. total notebook count
2. topic overview table
3. repeated stuck points and mistakes
4. repeated commands or options to review
5. per-topic grouped notes
6. a short next-step revision suggestion

## Fallbacks

- if there are no archived notebooks, still create a summary file that says so clearly
- if a notebook exists but sections are empty, count it but note that its content is sparse
- if metadata is missing, infer the topic from the archive folder name
- if topic inference is missing, use `misc`

## Implementation

Prefer using:

- `scripts/summarize_archived_notebooks.py`

The script should be deterministic and safe to run repeatedly.
