# Workspace Rules

Use this file when the user wants a self-contained exercise folder to practice in.

## Goal

The user should be able to `cd` into one generated folder and practice there without extra setup.

That folder should contain:

- the problem statement
- the target solution filename
- sample or table-shaped data files
- expected outputs
- a runnable test script

Hard rule:

- for `workspace` mode, creating the folder and files on disk is mandatory
- if no files were created, the task is incomplete even if the question text in chat is good
- prefer using `scripts/init_workspace.py` to create the folder skeleton before filling in the real content

## Recommended Agent Ownership

When subagents are available, use this ownership split:

- main agent owns `README.md`, target filename choice, folder naming, and final validation
- main agent owns `metadata.json`, `README.md`, target filename choice, folder naming, and final validation
- data subagent owns `data/` and `expected/`
- test subagent owns `tests/`

Keep the write sets separate to avoid merge conflicts.

## Default Folder Naming

Use sequential short names:

- `test01`
- `test02`
- `test03`

Avoid long names and avoid spaces.

## Preferred Workspace Path

Unless the user asks for a different location, create practice folders under:

```text
exercises/testNN/
```

Examples:

- `exercises/test01/`
- `exercises/test02/`

Choose the next available number by scanning existing `testNN` folders.

For a new exercise:

- if no existing folder is present, create `test01`
- otherwise create the next number, for example after `test07` create `test08`

Create only one folder for each exercise. Do not create both a numbered folder and a descriptive alias folder.

If a specific `testNN` is requested and already exists:

- do not silently overwrite it
- create the next available `testNN`, unless the user explicitly asked to reuse the old folder

## Minimum File Set

For shell questions:

```text
testNN/
  metadata.json
  README.md
  notebook.md
  solution.sh
  data/
    sample01_input.txt
    sample02_input.txt
    sample03_input.txt
    edge01_input.txt
    edge02_input.txt
  expected/
    sample01_output.txt
    sample02_output.txt
    sample03_output.txt
    edge01_output.txt
    edge02_output.txt
  tests/run_tests.sh
```

Use `#!/bin/dash` or portable `sh`-compatible syntax for shell practice unless the user explicitly asks for another shell.

For Python questions:

```text
exercise-name/
  metadata.json
  README.md
  solution.py
  data/
  expected/
  tests/run_tests.py
```

## Placeholder Solution Files

If the user did not ask for a solution:

- create the target solution file as a placeholder
- include only a shebang and a short comment
- do not implement the answer

Example shell placeholder:

```sh
#!/bin/dash
# 在 Windows 上可以这样运行：
# 1. 在 PowerShell 中启动 WSL
# 2. cd 到这个练习目录
# 3. 执行：dash solution.sh < data/sample01_input.txt
# 4. 测试：dash tests/run_tests.sh
#
# 在下面写你的答案。
```

Example Python placeholder:

```python
#!/usr/bin/env python3
# Write your answer here.
```

## Test Design

Each workspace should have at least:

- three visible sample cases when feasible
- two visible edge cases when feasible

Prefer numbered filenames such as:

- `data/sample01_input.txt`
- `data/sample02_input.txt`
- `data/sample03_input.txt`
- `data/edge01_input.txt`
- `data/edge02_input.txt`

with matching files under `expected/`.

Good edge cases include:

- duplicate records
- empty input lines
- repeated values
- already sorted data
- mixed case
- extra spacing
- empty files

The test subagent should derive its checks from the final question contract, not invent a different task.

When a test fails, the runner should print a short reason, for example:

- wrong ordering
- duplicate handling incorrect
- output mismatch
- content matches but trailing newline is missing
- missing trailing line
- file not created
- command exited with non-zero status

Prefer this reporting order:

1. show `PASS` or `FAIL`
2. show one short human-readable reason
3. show a tiny summary such as expected lines vs actual lines when useful
4. only then show a short diff excerpt if the mismatch is not obvious

For study use, prefer keeping failed actual outputs under a stable path such as:

- `tests/.artifacts/sample01.actual.txt`
- `tests/.artifacts/sample02.actual.txt`
- `tests/.artifacts/edge01.actual.txt`

and print those paths when a case fails.

## Transparency Rules

This is a study workspace, not a hidden autograder. So:

- sample tests should be visible
- edge tests may be visible too
- you may add slightly stricter checks in the runner
- do not describe them as official or hidden school tests

## Data File Guidance

Prefer small hand-checkable data files.

Good formats:

- `.txt`
- `.tsv`
- `.psv`

Avoid large datasets unless the user explicitly asks for realistic scale.

## Legacy Sample Warning

Under `knowledge-base/sample_data/test05/`, prefer:

- `compare_directory1/`
- `compare_directory2/`

Ignore any legacy top-level files named `directory1` or `directory2` there. They are residue from an earlier bad copy and are not valid directory samples.

## Metadata Expectations

Each generated workspace should include `metadata.json`.

This file should be small and machine-readable. Include at least:

- `title`
- `language`
- `topic_hint`
- `topics`
- `status`

Example:

```json
{
  "title": "Regex practice",
  "language": "shell",
  "topic_hint": "re",
  "topics": ["regex", "grep"],
  "status": "active"
}
```

When the real topic is known, the main agent should update `topic_hint` before finishing.

## README Expectations

`README.md` should always answer:

- what file the user must edit
- how input is provided
- how output is checked
- how to run the tests
- what common mistakes to watch for

For this user, `README.md` should be written in Chinese.

For shell tasks, `README.md` should state clearly that the intended shell is `dash` or portable POSIX `sh`.

For this user on Windows, `README.md` should also include:

- the exact absolute Windows path of the exercise folder
- the exact converted WSL path
- a copyable `cd` command using the WSL path

Example:

```text
Windows 路径：F:\Codex\9044-skill\exercises\test01
WSL 路径：/mnt/f/Codex/9044-skill/exercises/test01
进入目录：
cd /mnt/f/Codex/9044-skill/exercises/test01
```

The main agent should write `README.md` after the data and test slices are stable so the instructions match the actual files.

## Notebook Expectations

Each generated workspace should include `notebook.md`.

This file is for the user's own revision notes. It should start as a template, not as a finished summary.

It should include sections such as:

- the date
- the question title
- what I got wrong
- commands or flags to remember
- examples such as `grep -o`, `grep -E`, `sort -u`
- retry notes
