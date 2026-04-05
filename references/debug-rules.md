# Debug Rules

Use this file when the user wants the skill to produce a debug report alongside the normal result.

## Goal

Keep the main workflow unchanged, but also write a compact debug report that helps evaluate speed, token pressure, and workflow shape.

Debug is a modifier:

- do the normal task first
- then write debug artifacts
- do not replace the normal output with a debug-only response

## Trigger Examples

Use debug when the user says things like:

- "生成一个 grep 练习，并启动 debug"
- "Create a practice workspace and enable debug"
- "Debug this skill while generating the exercise"
- "我想看这个 skill 的执行时间和 token 消耗"

## What Debug Should Measure

At minimum, capture:

- request text
- resolved main mode
- start time and end time
- total wall-clock duration
- short per-stage timing breakdown
- tool-call counts
- non-debug files created or updated
- estimated non-debug token usage

## Token Guidance

Unless exact billing counters are available from the platform, the debug report must say clearly that token numbers are estimates.

Preferred breakdown:

- estimated context tokens from skill files and reference files used
- estimated non-debug output tokens from generated files
- total estimated non-debug tokens

Do not include the debug report files themselves in the token estimate.

## Output Location

If the main task created a workspace folder:

- write `debug/debug-report.md`
- write `debug/debug-report.json`

inside that folder.

Otherwise write under the workspace root:

- `debug-reports/debug-<mode>-<timestamp>.md`
- `debug-reports/debug-<mode>-<timestamp>.json`

## Implementation

Prefer using:

- `scripts/write_debug_report.py`

The script should:

- accept timestamps, stage timings, and file lists
- estimate tokens from text length heuristics
- write both Markdown and JSON outputs
- stay deterministic and safe to run repeatedly
