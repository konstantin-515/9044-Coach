# Scenario Bank

Use this file when the user asks for a generic shell or text-processing exercise and the skill needs to avoid repeating the same student-record / zID / term-style story.

## Goal

Separate the *operation pattern* from the *story scenario*.

If the recent exercises already used one story family repeatedly, keep the same skill level but switch the story and data world.

## Shell-Core Scenarios

- small command-line utility with positional arguments
- stdin-driven filter that prints a formatted summary
- source-code scanning task
- simple automation script with one clear side effect

## File-Directory Scenarios

- rename `.htm` to `.html`
- bulk rename report files by date or suffix
- compare two directories and report only specific differences
- scan a tree for files that break a naming rule
- copy selected files into a new folder while preserving constraints
- find files whose names encode metadata
- operate on files with spaces in names

## Backup-Snapshot Scenarios

- numbered hidden backups such as `.file.txt.0`
- `.snapshot.N` save and restore workflow
- ignore hidden files or tool scripts while saving
- restore a chosen snapshot after the working directory changed

## Pipeline-Text Scenarios

- class enrolment or timetable summaries
- delimited records such as PSV/TSV
- grouped counting and sorting reports
- normalization before aggregation

## Regex-Grep Scenarios

- log filtering
- code scanning
- ticket ID extraction
- config line validation
- anchored line selection from noisy text

## Python-Text Scenarios

- count and normalize text records
- preserve order while deduplicating
- extract numbers or tokens from messy lines
- aggregate then sort summaries

## File-Metadata Scenarios

- derive tags from music filenames and directories
- image timestamp or label processing
- parse artist / album / track from path segments
- build fake datasets with a required tree layout

## Anti-Repetition Rules

- if the last 2 or 3 exercises already used student records, zID-heavy tables, or term codes, do not use that story again for a generic shell request
- for generic shell practice, rotate through file-directory, backup-snapshot, shell-core, pipeline-text, and regex-grep
- use student/course/zID stories only when the user explicitly asks for them, or when the request is clearly about table/pipeline processing
- for a mixed or harder shell question, prefer file or directory scenarios regularly because they are a real course capability and otherwise get under-practiced

## Scenario Rotation Suggestions

When recent work is too text-heavy:

- switch to rename, compare, copy, or snapshot
- use filenames, directories, or media collections as the main data shape

When recent work is too file-heavy:

- switch back to pipeline, grep, or aggregation

When recent work is too regex-heavy:

- use a shell loop or directory traversal task where regex is only a helper, not the whole task

## Pairing Suggestions

- `file-directory` + `renaming` -> extension migration, collision checks, filenames with spaces
- `file-directory` + `comparison` -> same-name/different-content tasks, missing-file reporting
- `backup-snapshot` + `state restore` -> numbered saves, ignore hidden files, restore by index
- `shell-core` + `small automation` -> argument handling plus safe file updates
- `regex-grep` + `source scanning` -> `#include`, config files, logs, anchored matches
