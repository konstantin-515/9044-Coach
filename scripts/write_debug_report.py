#!/usr/bin/env python3
"""
Write a debug report for a 9044-coach execution.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys


STAGE_HINTS = {
    "planning": "把更多请求解析和默认参数判断规则化，减少临场思考。",
    "route": "把 mode 判断和轻量/完整路径判断更早规则化，减少前置决策耗时。",
    "reference_lookup": "优先走轻量检索路径，限制 reference 数量，避免过早打开详细知识库。",
    "references": "优先读压缩索引文件，只在必要时打开一份详细 merged 资料。",
    "workspace_creation": "把目录骨架和固定模板更多下放给脚本，减少生成阶段的重复组织。",
    "scaffold": "把骨架生成固定交给脚本，避免模型重复组织固定文件结构。",
    "authoring": "压缩 README 和样例组织步骤，更多复用模板和固定表格。",
    "validation": "合并重复校验，优先只检查关键一致性点。",
    "debug_report": "debug 输出已经偏重，必要时进一步压缩调试字段。",
}


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


def percentage_map(stage_timings: dict[str, int], total_duration_ms: int) -> dict[str, float]:
    if total_duration_ms <= 0:
        return {name: 0.0 for name in stage_timings}
    return {
        name: round((value / total_duration_ms) * 100, 1)
        for name, value in stage_timings.items()
    }


def pick_bottlenecks(stage_timings: dict[str, int]) -> tuple[dict | None, dict | None]:
    if not stage_timings:
        return None, None
    ordered = sorted(stage_timings.items(), key=lambda item: item[1], reverse=True)
    primary = {"stage": ordered[0][0], "duration_ms": ordered[0][1]}
    secondary = {"stage": ordered[1][0], "duration_ms": ordered[1][1]} if len(ordered) > 1 else None
    return primary, secondary


def build_optimization_hints(payload: dict) -> list[str]:
    hints: list[str] = []
    token_info = payload["estimated_non_debug_tokens"]
    context_estimate = token_info["context_estimate"]
    output_estimate = token_info["output_estimate"]
    reference_count = len(payload["reference_files"])
    route_kind = payload["route_kind"]
    primary = payload["primary_bottleneck"]
    secondary = payload["secondary_bottleneck"]

    if route_kind != "lightweight":
        hints.append("这次没有走轻量路径；如果是单题且主题明确，优先改成 lightweight route。")
    if primary:
        hint = STAGE_HINTS.get(primary["stage"])
        if hint:
            hints.append(f"当前主瓶颈在 `{primary['stage']}`；{hint}")
    if secondary and secondary["duration_ms"] >= 1000:
        hint = STAGE_HINTS.get(secondary["stage"])
        if hint:
            hints.append(f"次要瓶颈在 `{secondary['stage']}`；{hint}")
    if reference_count > 3:
        hints.append("参考文件数量偏多；普通单题建议把 reference 文件控制在 2 到 3 个。")
    if context_estimate > output_estimate * 2:
        hints.append("输入上下文 token 明显高于输出 token；优先压缩 reference 注入而不是压缩最终产物。")
    if not hints:
        hints.append("这次链路已经比较轻；下一步优先关注稳定性和题目质量，而不是继续压缩。")
    return hints


def build_markdown(payload: dict) -> str:
    stage_timings = payload["stage_timings_ms"]
    stage_percentages = payload["stage_percentages"]
    tool_counts = payload["tool_counts"]
    reference_files = payload["reference_files"]
    primary = payload["primary_bottleneck"]
    secondary = payload["secondary_bottleneck"]
    lines = [
        "# Skill 调试报告",
        "",
        f"- 请求：{payload['request']}",
        f"- 主模式：{payload['mode']}",
        f"- 执行路径：{payload['route_kind']}",
        f"- 目标路径：{payload['target_path'] or '-'}",
        f"- 开始时间：{payload['started_at']}",
        f"- 结束时间：{payload['ended_at']}",
        f"- 总耗时（毫秒）：{payload['total_duration_ms']}",
        "",
        "## 阶段耗时",
        "",
        "| 阶段 | 耗时（毫秒） | 占比 |",
        "| --- | --- | --- |",
    ]
    for name, value in stage_timings.items():
        lines.append(f"| `{name}` | {value} | {stage_percentages.get(name, 0.0)}% |")

    lines.extend(
        [
            "",
            "## 工具调用",
            "",
            "| 工具 | 次数 |",
            "| --- | --- |",
        ]
    )
    if tool_counts:
        for name, value in tool_counts.items():
            lines.append(f"| `{name}` | {value} |")
    else:
        lines.append("| `-` | 0 |")

    lines.extend(
        [
            "",
            "## 使用的参考文件",
            "",
            f"- 数量：{len(reference_files)}",
        ]
    )
    if reference_files:
        for item in reference_files:
            lines.append(f"- `{item['path']}`（估算 {item['estimated_tokens']} tokens）")
    else:
        lines.append("- 这次没有单独记录参考文件。")

    lines.extend(["", "## 主要瓶颈", ""])
    if primary:
        lines.append(
            f"- 主瓶颈：`{primary['stage']}`，耗时 {primary['duration_ms']} ms，占比 {primary['percentage']}%"
        )
    else:
        lines.append("- 主瓶颈：未记录")
    if secondary:
        lines.append(
            f"- 次要瓶颈：`{secondary['stage']}`，耗时 {secondary['duration_ms']} ms，占比 {secondary['percentage']}%"
        )

    lines.extend(["", "## 优化建议", ""])
    for hint in payload["optimization_hints"]:
        lines.append(f"- {hint}")

    token_info = payload["estimated_non_debug_tokens"]
    lines.extend(
        [
            "",
            "## 估算的非 Debug Token 消耗",
            "",
            f"- 上下文估算：{token_info['context_estimate']}",
            f"- 输出估算：{token_info['output_estimate']}",
            f"- 总估算：{token_info['total_estimate']}",
            f"- 说明：{token_info['note']}",
        ]
    )

    files = payload["files_touched"]
    lines.extend(
        [
            "",
            "## 变更文件",
            "",
            f"- 数量：{files['count']}",
        ]
    )
    for item in files["paths"]:
        lines.append(f"- `{item}`")

    if payload["missing_context_paths"] or payload["missing_generated_paths"]:
        lines.extend(["", "## 缺失路径", ""])
        for item in payload["missing_context_paths"]:
            lines.append(f"- 缺失的上下文文件：`{item}`")
        for item in payload["missing_generated_paths"]:
            lines.append(f"- 缺失的生成文件：`{item}`")

    if payload["notes"]:
        lines.extend(["", "## 备注", ""])
        for note in payload["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--route-kind", default="full")
    parser.add_argument("--target-path", default="")
    parser.add_argument("--started-at", required=True, help="ISO timestamp")
    parser.add_argument("--ended-at", default="", help="ISO timestamp; defaults to now")
    parser.add_argument("--stage", action="append", default=[], help="Repeated stage timing as name=ms")
    parser.add_argument("--tool", action="append", default=[], help="Repeated tool count as name=count")
    parser.add_argument("--context-file", action="append", default=[], help="File used as non-debug context")
    parser.add_argument("--reference-file", action="append", default=[], help="Reference file used for the main task")
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
    reference_paths = normalize_paths(args.reference_file)
    generated_paths = normalize_paths(args.generated_file)

    if not reference_paths:
        reference_paths = context_paths

    context_estimate, context_details, missing_context = estimate_paths(context_paths)
    reference_estimate, reference_details, missing_references = estimate_paths(reference_paths)
    output_estimate, output_details, missing_generated = estimate_paths(generated_paths)

    total_duration_ms = max(0, int((ended_at - started_at).total_seconds() * 1000))
    stage_percentages = percentage_map(stage_timings, total_duration_ms)
    primary, secondary = pick_bottlenecks(stage_timings)
    if primary is not None:
        primary["percentage"] = stage_percentages.get(primary["stage"], 0.0)
    if secondary is not None:
        secondary["percentage"] = stage_percentages.get(secondary["stage"], 0.0)

    md_path, json_path = resolve_report_paths(workspace_root, target_path, args.mode, ended_at)

    payload = {
        "request": args.request,
        "mode": args.mode,
        "route_kind": args.route_kind,
        "target_path": str(target_path) if target_path else "",
        "started_at": started_at.isoformat(timespec="seconds"),
        "ended_at": ended_at.isoformat(timespec="seconds"),
        "total_duration_ms": total_duration_ms,
        "stage_timings_ms": stage_timings,
        "stage_percentages": stage_percentages,
        "tool_counts": tool_counts,
        "estimated_non_debug_tokens": {
            "context_estimate": context_estimate,
            "reference_estimate": reference_estimate,
            "output_estimate": output_estimate,
            "total_estimate": context_estimate + output_estimate,
            "note": "按文本长度估算，不是平台 billing 的精确 token；默认不包含 debug 文件本身。",
        },
        "context_files": context_details,
        "reference_files": reference_details,
        "generated_files": output_details,
        "files_touched": {
            "count": len(generated_paths),
            "paths": [str(path) for path in generated_paths],
        },
        "missing_context_paths": missing_context,
        "missing_reference_paths": missing_references,
        "missing_generated_paths": missing_generated,
        "primary_bottleneck": primary,
        "secondary_bottleneck": secondary,
        "notes": args.note,
    }
    payload["optimization_hints"] = build_optimization_hints(payload)

    md_path.write_text(build_markdown(payload), encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"DEBUG_REPORT_MD={md_path}")
    print(f"DEBUG_REPORT_JSON={json_path}")
    print(f"DEBUG_TOTAL_MS={total_duration_ms}")
    print(f"DEBUG_TOKEN_ESTIMATE={payload['estimated_non_debug_tokens']['total_estimate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
