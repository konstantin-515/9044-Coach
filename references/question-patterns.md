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

### 5. Small Python Text-Processing Programs

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
- one Python text-processing task with strict output format

## Bad Question Shapes

- generic graph or DP problems
- puzzles unrelated to files, shell, or text
- overly long multi-part specifications
- novelty for its own sake
