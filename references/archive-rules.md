# Archive Rules

Use this file when the user wants to archive completed exercises out of `exercises/`.

## Goal

Separate the active practice area from the finished archive area.

Default layout:

```text
exercises/
  test01/
  test02/

archives/
  re/
    test07/
  shell/
    test03/
  python/
    test09/
  misc/
    test11/
```

## Archive Mode

When the user asks to archive one or more exercises:

- move the folders out of `exercises/`
- place them under `archives/<topic>/`
- do not leave a second live copy behind in `exercises/`

This is a move, not a copy.

## Input Style

Support:

- a single exercise such as `test01`
- a range such as `test01-03`
- a comma-separated list such as `test01,test03-05`

Interpret `test01-03` as a range:

- `test01`
- `test02`
- `test03`

## Topic Selection

If the user explicitly gives a topic, use that topic.

If the user does not give a topic, infer one automatically for each exercise.

Topic inference should look at:

- `metadata.json`
- `README.md`
- `notebook.md`
- whether the target file is `solution.sh` or `solution.py`
- course keywords such as `regex`, `grep`, `sed`, `awk`, `pipeline`, `shell`, `git`, `directory`, `python`

If `metadata.json` contains a non-empty `topic_hint`, prefer it over heuristic inference.

Preferred archive folder names are short:

- `re`
- `grep`
- `sed`
- `awk`
- `pipeline`
- `shell`
- `files`
- `git`
- `python`
- `misc`

If the inference is weak, archive to `misc`.

## Safety Rules

- never overwrite an existing archived folder silently
- if `archives/<topic>/testNN` already exists, skip that exercise and report it
- if `exercises/testNN` does not exist, report it clearly
- if the user gives a range and only some folders exist, archive the ones that exist and report the skipped ones

## User Experience

The result summary should say:

- which exercises were moved
- which topic folder each one went to
- which ones were skipped, if any

Examples:

- `MOVED test01 -> archives/re/test01`
- `MOVED test02 -> archives/shell/test02`
- `SKIP test03: source folder not found`

## Implementation

Prefer using:

- `scripts/archive_exercises.py`

The script should:

- create `archives/<topic>/` when missing
- infer topic automatically when topic is not supplied
- move folders with a filesystem move
- return a non-zero exit code if any requested folder could not be archived
