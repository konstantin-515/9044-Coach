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

The final result should behave like a move, but the implementation should be:

1. copy
2. verify
3. delete source

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
- ignore low-value transient paths such as `tests/.artifacts/` and `__pycache__/` during archive copy and verification
- before deleting the source, verify that the archive copy is complete
- if copying succeeds but deleting fails, do not hide that state behind a traceback

## User Experience

The result summary should say:

- which exercises were moved
- which topic folder each one went to
- which ones were skipped, if any

Examples:

- `ARCHIVED test01 -> archives/re/test01`
- `ARCHIVED test02 -> archives/shell/test02`
- `SKIP test03: source folder not found`
- `COPIED_OK CLEANUP_FAILED test04 -> archives/python/test04`

## Implementation

Prefer using:

- `scripts/archive_exercises.py`

The script should:

- create `archives/<topic>/` when missing
- infer topic automatically when topic is not supplied
- copy relevant files first, then verify, then delete the source
- compare at least the relevant relative path set before deleting the source
- tolerate partial previous archive attempts by resuming copy into an existing destination directory when appropriate
- report `COPIED_OK CLEANUP_FAILED` when the destination copy is verified but deleting the source folder fails
- return a non-zero exit code if any requested folder could not be archived

If elevated cleanup is needed after a verified copy:

- request escalated cleanup instead of retrying blindly
- prefer a non-login shell or PowerShell `-NoProfile` style invocation to reduce shell startup noise
