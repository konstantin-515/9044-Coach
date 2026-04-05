# Lightweight Path Rules

Use this file when the user asks for a single clear practice task and fast generation matters more than broad archive coverage.

## Goal

Reduce reference lookup cost for straightforward requests without sacrificing correctness.

This route is for:

- one exercise or one small drill
- one clearly named topic such as `grep`, `regex`, `shell`, `python`, `awk`, `sed`, `files`, or `git`
- no request for a mixed-topic set
- no request for a mock exam
- no request for deep archive comparison
- no request for heavy note/PDF alignment

## When To Use It

Prefer the lightweight path when:

- the main mode is `workspace`, `question`, or `drill`
- the user has already named the topic or tool family
- the user mainly wants speed and a directly usable folder

Do not use it when:

- the user wants multiple questions with variety
- the user wants a mock exam
- the user wants the task to combine multiple archive sources
- the user explicitly asks to align closely to personal notes or PDFs
- the first lightweight pass does not provide enough detail to write a solid spec

## Reading Budget

Before escalating to the full route, the lightweight path should read at most:

1. `references/topic-index.md`
2. `references/output-templates.md`
3. one of:
   - `references/question-patterns.md`
   - `references/data-shapes.md`
   - `references/workspace-rules.md`
4. optionally one detailed merged archive file if still needed

Hard budget:

- do not read more than 3 small reference files by default
- do not read more than 1 merged archive file unless the lightweight route is clearly insufficient
- do not open PDF notes in the lightweight path unless the user explicitly asks

## Fallback

If the question spec is still too weak after the lightweight budget:

- promote to the full route
- record in debug output that the lightweight route escalated

## Debug Expectations

When debug is enabled, record:

- `route_kind = lightweight`
- the exact reference files used
- whether the lightweight route succeeded or escalated to full
