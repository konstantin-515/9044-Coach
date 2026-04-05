# Source Map

This skill uses a copied local knowledge base stored inside the skill folder.

## Preferred Sources

Use these first because they are already merged into readable summaries and stored inside the skill:

- `knowledge-base/lab_output/lab01_merged.md` to `knowledge-base/lab_output/lab07_merged.md`
- `knowledge-base/test_output/test03_merged.md` to `knowledge-base/test_output/test07_merged.md`

These files are the best first-pass source for:

- topic detection
- question wording style
- common file formats
- sample constraints
- likely exam expectations

## Supporting Sources

Use these when you need realistic input file formats or example datasets:

- `knowledge-base/sample_data/lab02/*`
- `knowledge-base/sample_data/lab07/*`
- `knowledge-base/sample_data/test03/*`
- `knowledge-base/sample_data/test04/*`
- `knowledge-base/sample_data/test05/compare_directory1/*`
- `knowledge-base/sample_data/test05/compare_directory2/*`

Examples:

- enrollment records
- C source and header files
- nested directories
- whale observation data

## User Notes

The user may store personal revision notes here:

- `user-notes/md/`
- `user-notes/pdf/`

Use these when:

- the user has uploaded or written their own summaries
- the user wants generated questions to match their own study focus
- you want to mirror the terms or reminders the user already uses

Prefer Markdown notes first. Use PDFs when important notes only exist in PDF form.

## Recommended Reading Strategy

When generating a question:

1. Read `topic-index.md` first and match the request to a course capability.
2. Read one or two merged summaries that best match that capability.
3. Read copied support files only if you need concrete sample data shapes.
4. Avoid scanning the whole archive unless the user asks for a mixed-topic set.

When the request is a single clear-topic workspace or drill:

1. Try the lightweight path first.
2. Start with `topic-index.md`.
3. Then read only one of `question-patterns.md`, `data-shapes.md`, or `workspace-rules.md`.
4. Open one merged archive file only if the small references are still insufficient.

When summarizing past mistakes:

1. Read `archives/**/metadata.json` when present.
2. Read `archives/**/notebook.md` next.
3. Group by the archive topic folder before trying broader heuristics.
4. Write the compact result to `archives/_summaries/`.

## Topic Hints

- regex and grep foundations: `lab01`
- pipeline and structured text processing: `lab02`, `test03`
- POSIX shell scripting: `lab03`, `test04`, `test06`
- file and directory processing: `lab04`, `test05`
- snapshots and workflow: `lab05`
- Python text processing: `lab07`, `test07`

## Anti-Patterns

- Do not copy large chunks of the original task wording.
- Do not reuse the same sample input/output unless the user explicitly wants archive review.
- Do not drift into unrelated contest-style algorithms.
- Do not read the entire archive by default; start from the small reference files first.
