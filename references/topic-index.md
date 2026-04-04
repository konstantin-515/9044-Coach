# Topic Index

Use this file as the first lookup point before reading the larger knowledge base.

This is not just a source list. It is a course capability map.

When generating new practice, prefer matching the user's requested skill to:

1. syntax and tools
2. the underlying programming ability
3. the likely mistake pattern
4. the most representative archive sources

## Weekly Tests

| Source | Syntax And Tools | Core Ability | Typical Mistakes | Good Follow-up Question Types | Representative Data |
| --- | --- | --- | --- | --- | --- |
| `test03` | `cut`, `sed`, `awk`, `sort`, `uniq`, pipelines | split structured text by columns, extract fields, group, sort, deduplicate | mixing record-level deduplication with value-level deduplication; splitting names incorrectly; forgetting final sort order | first-name extraction, grouped reporting, filtered course summaries, count-by-field questions | `enrollments.txt` |
| `test04` | shell loops, arithmetic, renaming, regex, parsing `#include` lines | move from one-liner pipelines to small shell programs that inspect and transform files | brittle regexes, bad rename loops, weak filename handling, incomplete include parsing | rename scripts, source scanning, include analysis, loop-based file tasks | `a.c` and other small C files |
| `test05` | loops, `wc`, `diff`, `cmp`, directory traversal | compare directories and files systematically, reason about content equality and per-file processing | only comparing names, not contents; mishandling empty files; skipping missing-file cases | directory comparison, file-count reports, same-vs-different summaries, content-equality tasks | `compare_directory1/`, `compare_directory2/` |
| `test06` | `tr`, `cp`, loops, argument handling, in-place edits | strengthen shell scripting fluency for bulk edits, copying, filtering, and simple text conditions | unsafe replacement logic, incorrect loop handling, sloppy argument parsing, wrong filter conditions | batch copy tasks, conditional text edits, counting/filtering drills, small automation scripts | weekly test archive summary |
| `test07` | Python loops, dict/set counting, extraction, order preservation | transfer shell text-processing thinking into Python: extract, count, compare, preserve useful order | losing input order, counting incorrectly, failing to normalize before grouping, weak digit extraction | Python counting drills, ordered-summary questions, extraction-plus-aggregation tasks | weekly test archive summary |

## Labs

| Source | Syntax And Tools | Core Ability | Typical Mistakes | Good Follow-up Question Types | Representative Data |
| --- | --- | --- | --- | --- | --- |
| `lab01` | regex basics, `grep`, line filtering | recognise text patterns quickly and select the right lines from noisy text | matching too broadly, weak anchoring, misunderstanding what part of the line matters | grep drills, pattern-matching warmups, line-selection questions | dictionary-style text, parliament/member lists |
| `lab02` | `sort`, `uniq`, `cut`, `tr`, `sed`, pipelines | do structured-table processing with classic Unix text tools: column extraction, sorting, deduplication, counting, replacement | wrong column selection, deduping at the wrong stage, losing sort requirements, replacing too aggressively | PSV/TSV processing, summary tables, batch replacements, grouped counts | `enrolments.psv`, `classes.tsv`, `program.c` |
| `lab03` | `$1`, `$#`, `if`, `while`, `for`, `[ ]`, redirection, stdin/stdout, `$()` | write complete POSIX shell programs, not just one-liners; combine tools into a coherent script | weak parameter handling, incorrect test conditions, quoting mistakes, broken command substitution, confused stdin vs argv | POSIX shell scripts, API/data-fetch wrappers, argument-driven automation tasks | shell-programming labs and JSON/API exercises |
| `lab04` | file traversal, globbing, quoting, external programs, filename parsing | handle real file systems safely and automate bulk file/media processing | broken quoting for spaces, fragile filename parsing, unsafe glob assumptions, poor extraction from names or paths | rename-by-pattern tasks, metadata scripts, timestamp extraction, file-tree processing | `lab04.zip` and extracted media/archive content |
| `lab05` | file copies, snapshots, hidden naming rules, `git`, `gitlab` workflow | reason about versioned state, backups, snapshots, and basic collaboration workflow | incorrect snapshot naming, forgetting hidden-file rules, misunderstanding git basics or workflow order | backup/snapshot scripts, file-state tracking, workflow review questions, git process checks | lab05 shell and workflow material |
| `lab06` | sparse local summary | low-confidence source; do not rely on it heavily without opening the detailed archive | unknown due to limited local summary | low priority unless the user explicitly asks | sparse local summary only |
| `lab07` | `sys.argv`, file IO, string cleaning, dict/set counts, sorting, `re.findall`, simple code generation | do clearer text parsing and aggregation in Python; normalize messy data and print ordered summaries | counting rows instead of quantities, missing normalization, forgetting sorted output, weak regex extraction | whale summaries, count-vs-sum drills, regex extraction, normalization questions, Python text reports | `whales0.txt`, `A-Tale-of-Two-Cities.txt`, and related text files |

## Course Capability Summary

Compressed into one sentence, this course trains the user to:

- use regex and Unix tools to understand text formats quickly
- use pipelines to filter, sort, count, deduplicate, and rewrite data
- write small POSIX shell programs rather than isolated commands
- handle real files, directories, renames, backups, and bulk processing safely
- cope with messy data and tricky filenames such as names with spaces
- move text-extraction and aggregation thinking from shell into Python
- understand basic collaboration workflow using Git, branches, issues, and project docs

## Topic-To-Source Map

| Topic | Best Sources | Notes |
| --- | --- | --- |
| regex basics and grep | `lab01`, then `test04` and later mixed tests | start with selection and anchoring, then move to extraction and parsing |
| pipeline and structured text processing | `lab02`, then `test03` | best fit for PSV/TSV and enrolment-style data |
| POSIX shell scripting | `lab03`, then `test04` and `test06` | use for `$1`, loops, conditions, redirection, and command substitution |
| file and directory handling | `lab04`, `test05` | best fit for quoting, traversal, compare, and bulk file actions |
| snapshots and workflow | `lab05` | mix shell automation with git and collaboration fundamentals |
| Python text processing | `lab07`, `test07` | use for extraction, normalization, counting, and ordered summaries |
| final-style mixed practice | `test03`, `test05`, `lab07`, optionally `test06` | gives a realistic spread across shell, files, and Python |

## Revision Menus

Use these menu labels when the user wants guided revision:

- `regex and grep foundations`
- `pipelines and table processing`
- `POSIX shell scripting`
- `file and directory automation`
- `backup, snapshots, and git workflow`
- `Python text parsing and aggregation`
- `mixed final-practice set`

## Reading Strategy

1. Read this file first.
2. Match the user request to a course capability, not just to a week number.
3. Read [question-patterns.md](question-patterns.md).
4. Read [output-templates.md](output-templates.md).
5. Open detailed files in `knowledge-base/` only for style, exact data shapes, or extra fidelity.
