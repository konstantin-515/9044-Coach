# Data Shapes

Use this file before opening raw sample files. It summarizes the common input structures found in the local archive.

## Enrolment Records

Seen in:

- `knowledge-base/sample_data/test03/*`
- `knowledge-base/sample_data/lab02/enrolments.psv`

Typical structure:

- one enrolment per line
- course code
- student id
- surname and given names
- program or stream code
- gender or other trailing field

Typical question use:

- first-name extraction
- course-based filtering
- deduplication by student or by output field
- sorting alphabetically

## Class TSV Data

Seen in:

- `knowledge-base/sample_data/lab02/classes.tsv`

Typical structure:

- tab-separated fields
- class or course related rows

Typical question use:

- field selection
- sorting by column
- grouping or counting by one field

## Whale Observation Data

Seen in:

- `knowledge-base/sample_data/lab07/whales0.txt`
- `knowledge-base/sample_data/lab07/whales1.txt`
- `knowledge-base/sample_data/lab07/whales2.txt`
- `knowledge-base/sample_data/lab07/messy_whales0.txt`
- `knowledge-base/sample_data/lab07/messy_whales1.txt`

Typical structure:

- date
- pod size as an integer
- whale species name

Typical question use:

- counting individuals not rows
- grouping by species
- lowercasing
- singularization by trimming trailing `s`
- handling messy spacing

## Small C Source Trees

Seen in:

- `knowledge-base/sample_data/test04/*`
- `knowledge-base/sample_data/lab02/program.c`

Typical structure:

- short `.c` and `.h` files
- include statements
- filenames with simple relationships

Typical question use:

- grep or regex over source files
- finding included headers
- filename-based filtering

## Compare-Directory Samples

Seen in:

- `knowledge-base/sample_data/test05/compare_directory1/*`
- `knowledge-base/sample_data/test05/compare_directory2/*`

Ignore:

- legacy top-level file `knowledge-base/sample_data/test05/directory1`
- legacy top-level file `knowledge-base/sample_data/test05/directory2`

Typical structure:

- matching filenames in two directories
- some files identical
- some files different
- some files empty
- some files only on one side in related question variants

Typical question use:

- compare file contents
- report same or different names
- detect zero-length files
- script loops over directory entries safely
