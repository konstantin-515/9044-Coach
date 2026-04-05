# Debug Rules

Use this file when the user wants the skill to produce a debug report alongside the normal result.

## Goal

Keep the main workflow unchanged, but also write a compact debug report that helps evaluate speed, token pressure, and workflow shape.

The human-facing Markdown report should be in Chinese.

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
- resolved route kind such as `lightweight` or `full`
- start time and end time
- total wall-clock duration
- short per-stage timing breakdown
- tool-call counts
- references used for the main task
- split reference files into content references, control-rule files, and debug-only files when possible
- retry count
- whether fallback or degradation was triggered
- permission-related errors when they happen
- stderr or shell-environment noise when it is relevant
- main write methods when they are known
- primary bottleneck and secondary bottleneck
- optimization hints
- non-debug files created or updated
- estimated non-debug token usage
- validation summary when a workspace validator was run

## Token Guidance

Unless exact billing counters are available from the platform, the debug report must say clearly that token numbers are estimates.

Preferred breakdown:

- estimated context tokens from content and control references used for the main task
- estimated non-debug output tokens from generated files
- total estimated non-debug tokens

Do not include the debug report files themselves in the token estimate.
Prefer not to count debug-only rule files as main-task context tokens.

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
- accept reference file lists and route kind
- optionally accept a validation JSON summary
- optionally accept retry, fallback, permission, stderr-noise, and write-method traces
- estimate tokens from text length heuristics
- identify the slowest stage as the bottleneck
- generate simple optimization hints from timing, token shape, and validation status
- distinguish content references from control/debug files in the report
- make it visible when spec-driven authoring was used instead of ad hoc file writes
- make it obvious whether slowness came from actual retries or just heavy authoring
- write both Markdown and JSON outputs
- stay deterministic and safe to run repeatedly
