---
name: 9044-coach
description: Coach the user for COMP2041 or COMP9044 style shell and text-processing exams using the local archived labs and weekly tests as a knowledge base. Use this when the user wants fresh practice questions, mini-mock exams, hints, worked solutions, marking tables, sample tests, edge cases, revision drills, or topic-targeted training based on the local course archive rather than generic algorithm puzzles.
metadata:
  short-description: COMP9044 exam coach using the local archive
---

# 9044 Coach

Use this skill when the user wants help preparing for a COMP2041 or COMP9044 style exam in this workspace.

This skill acts like a revision coach, not just a question generator. It should:

- generate fresh practice questions in the style of the local archive
- choose topics based on the user's weak areas or revision goals
- include sample tests, edge cases, and marking tables
- create a self-contained practice folder when the user wants a hands-on exercise workspace
- control how much help is revealed: question only, hints, outline, or full answer
- explain what the question is testing and what mistakes are likely
- coordinate subagents when available so question design, data generation, and test generation are separated cleanly

Do not simply restate old lab or weekly test questions. Infer patterns from the archive and create new, course-authentic practice.

## Knowledge Base

Start from the copied knowledge base inside this skill:

- `references/knowledge-base/lab_output/*.md`
- `references/knowledge-base/test_output/*.md`

Use the copied support files when useful for realistic input formats:

- `references/knowledge-base/sample_data/**`

Also use the user's own notes when present:

- `references/user-notes/md/**/*.md`
- `references/user-notes/pdf/**/*.pdf`

When both archive material and user notes are available, use this preference order:

1. the user's current request
2. the user's Markdown notes
3. the compact reference files in `references/`
4. the user's PDF notes
5. the detailed copied archive under `references/knowledge-base/`

If you need more detail about how to use these sources, read [references/source-map.md](references/source-map.md).

Before opening the larger knowledge-base files, prefer this fast path:

1. [references/topic-index.md](references/topic-index.md)
2. [references/question-patterns.md](references/question-patterns.md)
3. [references/output-templates.md](references/output-templates.md)
4. [references/data-shapes.md](references/data-shapes.md)
5. [references/workspace-rules.md](references/workspace-rules.md) when creating folders on disk
6. [references/question-quality-checklist.md](references/question-quality-checklist.md) before finalizing a generated exercise
7. inspect `references/user-notes/` when the user has stored personal notes there
8. open files under `references/knowledge-base/` only as needed

## Supported Modes

Choose the lightest mode that satisfies the user:

- `question`: generate one or more new practice questions
- `drill`: generate short focused drills on one topic
- `mock-exam`: generate a small exam-style set with difficulty progression
- `workspace`: generate a practice folder with prompt, data files, and tests
- `review`: explain what a topic or archive pattern is testing
- `hint`: give staged hints for a question
- `solution`: give a solution outline or full worked answer
- `checker`: review the user's answer and point out likely issues

## Agent Split

When subagents are available and the task is to generate a practice workspace, use this split:

- main agent: choose topic, difficulty, wording, output contract, folder structure, and final integration
- subagent 1: create the data files under `data/` and `expected/`
- subagent 2: create the runnable test script under `tests/`

The main agent remains responsible for:

- making sure the question, data, and tests agree
- checking filenames and paths
- deciding whether the target should be `solution.sh` or `solution.py`
- writing the final `README.md`

The subagents should not change the question spec. They only implement their owned slice.

Important platform constraint:

- only spawn subagents when the user explicitly asks for subagents, delegation, or parallel agent work
- otherwise keep the same ownership split conceptually, but perform the work in one agent

## Default Behavior

If the user does not specify constraints, default to:

- mode: `workspace`
- count: `1`
- difficulty: `exam-style`
- scope: `dash shell, grep -E, sed, awk, regex, text processing`
- help level: `hints only`
- output: `practice folder + README + data files + test script + sample tests + edge cases + marking table + knowledge points`

Prefer course-authentic questions over generic computer science puzzles.

## What To Generate

For each generated question, include these sections in order:

1. `Title`
2. `Task`
3. `Input`
4. `Output`
5. `Constraints`
6. `Sample Tests`
7. `Edge Cases`
8. `Marking Focus`
9. `Knowledge Points`
10. `Common Mistakes`
11. `Hint` or `Hints`

If the user asks for a solution, add:

12. `Solution Outline`
13. `Reference Answer`

If the user asks for a mock exam, also add:

- a short time suggestion
- a marks allocation per question

If the mode is `workspace`, generate a folder on disk containing at least:

1. `README.md` with the full problem statement
2. `notebook.md` as a study-notes template for the user
3. `tests/` with at least one runnable test script
4. `data/` with sample input files or table-shaped data
5. `expected/` with expected outputs for the sample and edge tests
6. a placeholder target filename the user is expected to implement, such as `solution.sh` or `solution.py`

Use ASCII filenames and keep the folder self-contained.

For shell tasks in this course, default to:

- `dash` / POSIX `sh` style, not Bash-specific features
- tools commonly seen in course work such as `grep -E`, `sed`, `awk`, `sort`, `uniq`, `cut`, `tr`, and `find`
- portable syntax that should run under `dash`

## Help Levels

Match the response to the user's learning goal:

- `question only`: no hint, no answer
- `guided`: question plus 1 to 3 hints
- `outline`: include solution strategy but no final code
- `full solution`: include reference code and explanation
- `mark my answer`: compare the user's work against likely requirements and edge cases

Default to `guided` unless the user clearly asks for a full solution.

When generating a practice workspace, default to `question only` inside the files:

- the generated folder should not contain the final solution unless the user explicitly asks
- hints may go in `README.md`
- hidden or stricter tests may go in the test script, but do not falsely present them as official course tests

## Required Output Structure

Each generated question must contain at least:

- one realistic sample input and output pair
- one edge case input and output pair
- one short marking table
- one short knowledge-point list
- one short common-mistakes list

Use at least one Markdown table per question. Prefer this table shape:

| Test Category | Purpose | Input Characteristic | Common Mistake |
| --- | --- | --- | --- |

If helpful, add a second table:

| Check Item | Requirement |
| --- | --- |

For `workspace` mode, the `README.md` must also include:

- the exact filename the user should write
- how to run the tests
- which files are safe to inspect
- whether input comes from stdin, command line arguments, or data files
- the exact WSL path for this exercise folder
- a ready-to-copy `cd` command using that WSL path

For this user, prefer:

- Chinese `README.md`
- short workspace names such as `test01`, `test02`, `test03`
- exactly one generated workspace folder per exercise, not both a dated folder and a slug folder

## Generation Rules

- Keep the style close to the local course material.
- Do not copy original question text verbatim.
- Do not reuse the exact original example data unless the user explicitly asks for archive-based review.
- Combine or mutate patterns from multiple local questions when that creates better practice.
- When the user has added personal notes, align emphasis, terminology, and revision hints with those notes.
- Prefer the user's Markdown notes over PDFs when both cover the same topic.
- If a PDF is present but its contents are not directly readable in the current workflow, use its filename/topic as a hint but do not invent details from it.
- Make input and output rules precise. If sorting, deduplication, case handling, or formatting matters, say so explicitly.
- Prefer text-processing tasks over abstract algorithm puzzles.
- If the user asks for "algorithm questions", interpret that in the context of this course: pipelines, regex, file parsing, aggregation, filtering, formatting, and small scripting tasks.
- If the user asks for shell-only practice, do not generate Python tasks.
- If the user asks for Python practice, keep it aligned with the course's small text-processing style.
- Prefer realistic exam traps over novelty. Hidden difficulty should come from edge cases and output precision, not from obscure tricks.
- If generating files, make them immediately usable from the created folder without extra setup.
- Keep test scripts simple and transparent enough for study use.
- Prefer portable shell or Python test scripts that print pass/fail per case.
- Test scripts should explain why a case failed, not just that it failed.
- For shell tasks, avoid Bash-only syntax in both the question and the test runner unless the user explicitly asks for Bash.

## Difficulty Guidance

- `easy`: one main idea, little ambiguity, simple input format
- `medium`: two operations or one tricky formatting rule
- `hard`: multiple constraints, edge cases, or mixed parsing and aggregation
- `exam-style`: realistic constraints, strict output format, hidden pitfalls, and no unnecessary novelty

## Workflow

1. Determine the user's mode: question, drill, mock exam, review, hint, solution, or checker.
2. Inspect the fast reference files to identify likely matching topics and data shapes.
3. Open detailed archive files only if needed for style or format fidelity.
4. Create a fresh question or explanation that matches the local course style without copying.
5. If the mode is `workspace`, create a self-contained exercise folder on disk.
6. If subagents are available, assign one subagent to generate data files and one subagent to generate the test runner.
7. Integrate both outputs into the final folder.
8. Add a marking table, knowledge-point summary, and common-mistakes list.
9. Reveal only the amount of help the user asked for.
10. Before finishing, run the validation checklist below mentally.
11. If a workspace was created, ensure the folder name follows the workspace naming rule.

## Workspace Folder Contract

When generating a practice folder, prefer this structure:

```text
testNN/
  README.md
  notebook.md
  solution.sh or solution.py
  data/
    sample_input.txt
    edge_input.txt
    optional table data such as .tsv, .psv, or .txt
  expected/
    sample_output.txt
    edge_output.txt
  tests/
    run_tests.sh or run_tests.py
```

Guidelines:

- use sequential short names such as `test01`, `test02`, `test03`
- create exactly one workspace folder for the exercise
- choose `solution.sh` for shell tasks and `solution.py` for Python tasks
- include at least one normal case and one edge case
- keep generated data small enough to inspect manually
- if table-like data helps, create it as `.tsv`, `.psv`, or `.txt`
- make the test runner executable in a normal local workflow
- do not include the final answer file contents unless the user asks
- it is acceptable to create an empty placeholder solution file with a short comment header
- if subagents are used, keep write ownership separate: one owns `data/` and `expected/`, the other owns `tests/`
- for shell tasks, write the placeholder and tests to be compatible with `dash`

## Validation Checklist

Before returning a generated question, make sure:

- it is not too close to a single original archive question
- the task is solvable from the written specification
- the sample tests match the stated rules
- the edge case actually tests a plausible mistake
- the expected ordering and formatting are explicit
- the question fits the requested language and difficulty
- the answer level matches what the user asked for
- if a workspace was generated, all referenced files actually exist and the test runner points to the correct target filename
- only one exercise folder was created for this exercise
- if the workspace is on Windows, `README.md` includes the actual converted WSL path such as `/mnt/f/...`
- if the test runner writes failure artifacts, the printed paths match the created files

## When The User Is Vague

If the request is vague, do not stop to ask broad questions unless needed. Make a reasonable assumption and continue.

Good defaults:

- "give me a question": one medium or exam-style shell practice folder
- "give me final practice": one exam-style shell or text-processing question
- "give me 3 questions": mix pipeline, regex, and file-processing styles
- "quiz me": one question first, then wait
- "help me revise": provide a short topic menu plus one starter question

## Safety And Integrity

- Do not pretend a generated question is an official school exam question.
- Do not claim hidden test cases are real course test cases.
- If you are heavily inspired by one local source, say it is "in the style of the local archive".
- If the user appears to be asking for direct submission help on a live assessed task, pivot to explanation, hints, and study support instead of presenting the output as a ready-to-submit answer.
