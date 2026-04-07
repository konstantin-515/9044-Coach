# Case Design Rules

Use this file when generating `sample` and `edge` cases for a new exercise workspace.

## Goal

Make visible cases diverse enough that the user can understand the real contract of the question, not just one happy-path example.

## Minimum Diversity Rule

Do not generate a set of visible cases where all samples test the same behavior.

Visible cases should cover different categories such as:

- normal case
- duplicate or repeated input
- malformed or partially invalid input
- ordering / tie-breaking case
- no-match or empty-result case
- safety or filesystem edge case

## Generic Sample Mix

For a straightforward exercise, aim for at least:

- `sample01`: clean happy-path example
- `sample02`: repeated or duplicate data
- `sample03`: different valid pattern that still satisfies the rules
- `edge01`: malformed, invalid, or should-be-ignored records
- `edge02`: formatting, empty result, or boundary condition

For a harder integrated exercise, prefer adding:

- `sample04`: sorting or tie-breaking case
- `sample05`: mixed valid and invalid cases that test multiple filters together

## Track-Specific Guidance

### File-Directory

Prefer visible cases that include:

- files that should be changed
- files that should be left alone
- names with spaces
- existing target collisions
- no matching files

### Directory Comparison

Prefer visible cases that include:

- same name, same content
- same name, different content
- file only in left directory
- file only in right directory
- empty file

### Backup-Snapshot

Prefer visible cases that include:

- first backup or first snapshot
- next numbered backup
- restore from an older snapshot
- hidden files or ignored helper scripts

### Pipeline / Table Processing

Prefer visible cases that include:

- duplicate rows
- rows filtered out by a condition
- ties requiring a secondary sort
- malformed rows that should be ignored

### Regex / Grep

Prefer visible cases that include:

- correct anchored match
- visually similar line that should not match
- case-sensitivity trap
- punctuation or suffix trap

## README Requirement

The `README.md` should show explicit sample input/output blocks for the visible cases, not only filenames.

If a complex exercise has 4 or more visible sample files, the README should still show all of them.
