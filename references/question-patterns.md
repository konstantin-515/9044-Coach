# Question Patterns

Use this file to generate fresh questions in the style of the local archive without copying old wording.

## Common Pattern Families

### 1. Field Extraction From Structured Text

Typical input:

- delimited lines such as `|`, `:`, tab, or whitespace separated records
- one record per line

Common tasks:

- print one field
- print derived fields such as first name or code prefix
- preserve duplicates from distinct records
- remove duplicates caused by repeated enrolments
- sort final output

Common traps:

- confusing record-level duplicates with value-level duplicates
- splitting names incorrectly
- forgetting sort order
- mishandling trailing spaces

### 2. Filtering And Formatting

Typical input:

- plain text lines with embedded patterns
- source code or logs

Common tasks:

- keep only matching lines
- exclude matches
- rewrite a substring
- print formatted summaries

Common traps:

- matching too broadly
- failing to anchor regexes
- keeping punctuation that should be stripped

### 3. Aggregation And Counting

Typical input:

- repeated categories across many lines
- quantity plus label

Common tasks:

- count observations
- sum totals
- produce grouped summary lines
- normalize case before grouping

Common traps:

- counting rows instead of individuals
- grouping before normalization
- singular/plural mismatches

### 4. Directory Comparison

Typical input:

- two directories with overlapping and distinct filenames

Common tasks:

- list same files
- list different files
- detect empty files
- compare contents not just names

Common traps:

- checking only filenames
- mishandling empty files
- ignoring files present in only one directory

### 5. File Renaming And Extension Migration

Typical input:

- many files in one directory
- filenames where suffix or pattern matters

Common tasks:

- rename `.htm` to `.html`
- rename by pattern
- skip collisions safely
- preserve unrelated files

Common traps:

- overwriting an existing target file
- weak quoting when filenames contain spaces
- renaming too broadly

### 6. File Tree Traversal And Safe Quoting

Typical input:

- one or more directories
- nested files
- filenames or directory names that contain spaces

Common tasks:

- walk a directory tree
- extract information from file or directory names
- apply a command to matching files
- compare path-derived metadata with file contents

Common traps:

- broken quoting
- relying on unsafe glob assumptions
- parsing filenames too rigidly

### 7. Backup And Snapshot Workflows

Typical input:

- the current directory state
- repeated saves or restores

Common tasks:

- create numbered backups
- create `.snapshot.N` directories
- ignore hidden or disallowed files
- restore a chosen snapshot safely

Common traps:

- wrong numbering logic
- backing up files that should be ignored
- calling scripts with `./` when the marking environment expects `$PATH`

### 8. Metadata From Filenames And Directory Names

Typical input:

- music collections
- images
- filenames that encode track numbers, artist names, dates, or tags

Common tasks:

- derive metadata from names
- repair tags
- label files using path-derived information
- build fake datasets with a required directory layout

Common traps:

- brittle splitting rules
- mishandling punctuation or spaces
- assuming every filename is perfectly clean

### 9. Small Python Text-Processing Programs

Typical input:

- one or more text files as command line arguments
- semi-structured text lines

Common tasks:

- parse records
- count matches
- aggregate by category
- print ordered summaries

Common traps:

- forgetting argument loops
- not normalizing data before grouping
- failing to sort output alphabetically

## Mutation Strategies

To make a new question:

- keep the same operation pattern but change the story or data domain
- combine two familiar operations into one question
- add one hidden constraint such as sorting, deduplication, or case normalization
- keep the input realistic and course-like
- rotate the story scenario as well as the operation pattern
- avoid reusing student-record, zID, course, or term stories repeatedly unless the user explicitly asks for them

## Coaching Variants

Use the same pattern family in different coaching modes:

- `question`: generate one polished problem
- `drill`: generate a smaller version with less story and tighter scope
- `mock-exam`: combine 2 to 4 patterns across multiple questions
- `checker`: derive likely hidden tests from the pattern and compare them against the user's answer
- `review`: explain why this pattern appears often in the course and how to recognize it quickly

## Good Question Shapes

- one clean operation plus one tricky formatting rule
- one aggregation task plus one normalization rule
- one directory task plus one edge-case requirement
- one rename or backup task plus one safety rule
- one file-tree task where quoting is essential
- one Python text-processing task with strict output format

## Rotation Guidance

When the user asks for generic `shell` practice or a mixed final-style shell question:

- do not keep repeating `zid`, `course code`, `term`, or other student-record style data
- if the recent exercises already emphasize regex, grep, or structured table parsing, rotate to one of:
  - file renaming
  - directory comparison
  - backups or snapshots
  - file-tree traversal with quoting
  - metadata derived from filenames or directory names
- prefer file and directory automation regularly because it is a real course capability, not an edge topic
- a "different question" means a different task family, not the same regex/pipeline idea with different labels
- generic shell practice should regularly surface folder/file tasks because many students under-practice them

## Sample Diversity Guidance

Do not generate visible cases that are all variants of the same regex/filter.

Prefer a visible case mix such as:

- one happy-path example
- one repeated or duplicate case
- one malformed or invalid-input case
- one ordering or tie-break case
- one no-match or ignore-this case

For file and directory questions, visible cases should often demonstrate:

- filenames with spaces
- existing targets or naming collisions
- files that should not be touched
- same-name / different-content comparisons

## Bad Question Shapes

- generic graph or DP problems
- puzzles unrelated to files, shell, or text
- overly long multi-part specifications
- novelty for its own sake
