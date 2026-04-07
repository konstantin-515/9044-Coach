# Shell Diversity Rules

Use this file when the user asks for generic shell practice without explicitly naming a narrow topic.

## What "Diversity" Means Here

Diversity does **not** mean changing `zid` to another code while keeping the same text-processing pattern.

It means rotating across genuinely different shell task families, such as:

- file renaming
- directory comparison
- backups and snapshots
- file-tree traversal
- quoting-sensitive filename handling
- regex/log filtering
- pipeline/table processing

## Hard Anti-Repetition Rules

- if the recent shell exercises already repeated student-record, zID, course-code, or term-style parsing, do not use that story again for the next generic shell request
- if the recent 3 shell exercises are mostly regex/pipeline style, the next generic shell exercise should prefer `file-directory` or `backup-snapshot`
- generic shell practice must include file or directory automation regularly; it is a core course capability, not an optional extra
- do not treat "shell practice" as synonymous with "structured text parsing"

## Preferred Rotation

For generic shell requests, rotate in this order when possible:

1. file-directory
2. backup-snapshot
3. shell-core
4. pipeline-text
5. regex-grep

If recent work already covered the current track heavily, skip ahead instead of repeating it.

## Story Families To Avoid Repeating

Avoid repeating these story families in back-to-back generic shell exercises:

- student records
- zID extraction
- course code filtering
- term-code parsing
- generic log filtering with only small regex changes

## Story Families To Reintroduce

Prefer reintroducing these underused shell worlds:

- web files and extension migration
- mirrored directories
- snapshots and hidden numbered backups
- media collections and filenames with spaces
- source trees and include/config scanning
- folder cleanup or safe file copying

## Sample Expectations For File Tasks

For file/directory exercises, visible cases should often include:

- filenames with spaces
- files that should stay unchanged
- existing target collisions
- no-match situations
- left-only / right-only file cases
- same-name / different-content cases

## Review Question

Before finalizing a generic shell exercise, ask:

- is this genuinely a different shell task family from the recent ones?

If the honest answer is no, rotate the track or the story scenario before generating the workspace.
