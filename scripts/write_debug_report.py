#!/usr/bin/env python3
"""
Write a debug report for a 9044-coach execution.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import sys


def parse_kv_list(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"expected name=value, got: {raw}")
        name, value = raw.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"missing name in pair: {raw}")
        result[name] = int(value.strip())
    return result


def normalize_paths(paths: list[str]) -> list[pathlib.Path]:
    normalized: list[pathlib.Path] = []
    seen: set[str] = set()
    for raw in paths:
        path = pathlib.Path(raw).resolve()
        key = str(path)
        if key not in seen:
            seen.add(key)
            normalized.append(path)
    return normalized


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def estimate_tokens(text: str) -> int:
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    non_cjk = re.sub(r"[\u4e00-\u9fff]", "", text)
    return cjk_count + max(0, len(non_cjk) // 4)


def estimate_paths(paths: list[pathlib.Path]) -> tuple[int, list[dict], list[str]]:
    total = 0
    details: list[dict] = []
    missing: list[str] = []
    for path in paths:
        if not path.exists():
            missing.append(str(path))
            continue
        text = read_text(path)
        tokens = estimate_tokens(text)
        total += tokens
        details.append(
            {
                "path": str(path),
                "chars": len(text),
                "estimated_tokens": tokens,
            }
        )
    return total, details, missing


def resolve_report_paths(
    workspace_root: pathlib.Path, target_path: pathlib.Path | None, mode: str, ended_at: dt.datetime
) -> tuple[pathlib.Path, pathlib.Path]:
    if target_path is not None:
        base = target_path if target_path.is_dir() else target_path.parent
        report_dir = base / "debug"
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir / "debug-report.md", report_dir / "debug-report.json"

    report_dir = workspace_root / "debug-reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = ended_at.strftime("%Y%m%d-%H%M%S")
    stem = f"debug-{mode}-{stamp}"
    return report_dir / f"{stem}.md", report_dir / f"{stem}.json"


def build_markdown(payload: dict) -> str:
    stage_timings = payload["stage_timings_ms"]
    tool_counts = payload["tool_counts"]
    lines = [
        "# Skill Debug Report",
        "",
        f"- Request: {payload['request']}",
        f"- Mode: {payload['mode']}",
        f"- Target Path: {payload['target_path'] or '-'}",
        f"- Started At: {payload['started_at']}",
        f"- Ended At: {payload['ended_at']}",
        f"- Total Duration Ms: {payload['total_duration_ms']}",
        "",
        "## Stage Timings",
        "",
        "| Stage | Duration Ms |",
        "| --- | --- |",
    ]
    for name, value in stage_timings.items():
        lines.append(f"| `{name}` | {value} |")

    lines.extend(
        [
            "",
            "## Tool Calls",
            "",
            "| Tool | Count |",
            "| --- | --- |",
        ]
    )
    if tool_counts:
        for name, value in tool_counts.items():
            lines.append(f"| `{name}` | {value} |")
    else:
        lines.append("| `-` | 0 |")

    token_info = payload["estimated_non_debug_tokens"]
    lines.extend(
        [
            "",
            "## Estimated Non-Debug Tokens",
            "",
            f"- Context Estimate: {token_info['context_estimate']}",
            f"- Output Estimate: {token_info['output_estimate']}",
            f"- Total Estimate: {token_info['total_estimate']}",
            f"- Note: {token_info['note']}",
        ]
    )

    files = payload["files_touched"]
    lines.extend(
        [
            "",
            "## Files Touched",
            "",
            f"- Count: {files['count']}",
        ]
    )
    for item in files["paths"]:
        lines.append(f"- `{item}`")

    if payload["missing_context_paths"] or payload["missing_generated_paths"]:
        lines.extend(["", "## Missing Paths", ""])
        for item in payload["missing_context_paths"]:
            lines.append(f"- Missing context file: `{item}`")
        for item in payload["missing_generated_paths"]:
            lines.append(f"- Missing generated file: `{item}`")

    if payload["notes"]:
        lines.extend(["", "## Notes", ""])
        for note in payload["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--target-path", default="")
    parser.add_argument("--started-at", required=True, help="ISO timestamp")
    parser.add_argument("--ended-at", default="", help="ISO timestamp; defaults to now")
    parser.add_argument("--stage", action="append", default=[], help="Repeated stage timing as name=ms")
    parser.add_argument("--tool", action="append", default=[], help="Repeated tool count as name=count")
    parser.add_argument("--context-file", action="append", default=[], help="File used as non-debug context")
    parser.add_argument("--generated-file", action="append", default=[], help="Non-debug generated or updated file")
    parser.add_argument("--note", action="append", default=[], help="Repeated note lines")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    workspace_root = pathlib.Path(args.workspace_root).resolve()
    if not workspace_root.exists():
        print(f"ERROR: workspace root not found: {workspace_root}", file=sys.stderr)
        return 2

    try:
        started_at = dt.datetime.fromisoformat(args.started_at)
    except ValueError:
        print(f"ERROR: invalid started-at timestamp: {args.started_at}", file=sys.stderr)
        return 2

    if args.ended_at:
        try:
            ended_at = dt.datetime.fromisoformat(args.ended_at)
        except ValueError:
            print(f"ERROR: invalid ended-at timestamp: {args.ended_at}", file=sys.stderr)
            return 2
    else:
        ended_at = dt.datetime.now()

    try:
        stage_timings = parse_kv_list(args.stage)
        tool_counts = parse_kv_list(args.tool)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    target_path = pathlib.Path(args.target_path).resolve() if args.target_path else None
    context_paths = normalize_paths(args.context_file)
    generated_paths = normalize_paths(args.generated_file)
    context_estimate, context_details, missing_context = estimate_paths(context_paths)
    output_estimate, output_details, missing_generated = estimate_paths(generated_paths)

    total_duration_ms = max(0, int((ended_at - started_at).total_seconds() * 1000))
    md_path, json_path = resolve_report_paths(workspace_root, target_path, args.mode, ended_at)

    payload = {
        "request": args.request,
        "mode": args.mode,
        "target_path": str(target_path) if target_path else "",
        "started_at": started_at.isoformat(timespec="seconds"),
        "ended_at": ended_at.isoformat(timespec="seconds"),
        "total_duration_ms": total_duration_ms,
        "stage_timings_ms": stage_timings,
        "tool_counts": tool_counts,
        "estimated_non_debug_tokens": {
            "context_estimate": context_estimate,
            "output_estimate": output_estimate,
            "total_estimate": context_estimate + output_estimate,
            "note": "Estimated from text length only; this is not a billing-accurate token count.",
        },
        "context_files": context_details,
        "generated_files": output_details,
        "files_touched": {
            "count": len(generated_paths),
            "paths": [str(path) for path in generated_paths],
        },
        "missing_context_paths": missing_context,
        "missing_generated_paths": missing_generated,
        "notes": args.note,
    }

    md_path.write_text(build_markdown(payload), encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"DEBUG_REPORT_MD={md_path}")
    print(f"DEBUG_REPORT_JSON={json_path}")
    print(f"DEBUG_TOTAL_MS={total_duration_ms}")
    print(f"DEBUG_TOKEN_ESTIMATE={payload['estimated_non_debug_tokens']['total_estimate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
