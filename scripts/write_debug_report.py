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
    "authoring": "把题面、样例和 expected 收成 spec 驱动，一次性交给 fill_workspace_from_spec.py 渲染。",
    "validation": "合并重复校验，优先只检查关键一致性点。",
    "debug_report": "debug 输出已经偏重，必要时进一步压缩调试字段。",
}

CONTROL_REFERENCE_NAMES = {
    "lightweight-path-rules.md",
    "workspace-rules.md",
    "question-quality-checklist.md",
    "source-map.md",
    "archive-rules.md",
    "mistake-summary-rules.md",
}
DEBUG_REFERENCE_NAMES = {"debug-rules.md"}


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


def parse_text_kv_list(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"expected name=value, got: {raw}")
        name, value = raw.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError(f"missing name in pair: {raw}")
        result[name] = value.strip()
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


def classify_reference(detail: dict) -> str:
    name = pathlib.Path(detail["path"]).name
    if name in DEBUG_REFERENCE_NAMES:
        return "debug"
    if name in CONTROL_REFERENCE_NAMES:
        return "control"
    return "content"


def split_reference_groups(reference_details: list[dict]) -> dict[str, list[dict]]:
    groups = {"content": [], "control": [], "debug": []}
    for detail in reference_details:
        groups[classify_reference(detail)].append(detail)
    return groups


def token_sum(items: list[dict]) -> int:
    return sum(item.get("estimated_tokens", 0) for item in items)


def load_validation_summary(path_str: str) -> dict | None:
    if not path_str:
        return None
    path = pathlib.Path(path_str).resolve()
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


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
    return {name: round((value / total_duration_ms) * 100, 1) for name, value in stage_timings.items()}


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
    content_reference_count = len(payload["reference_groups"]["content"])
    route_kind = payload["route_kind"]
    primary = payload["primary_bottleneck"]
    secondary = payload["secondary_bottleneck"]
    validation = payload.get("validation")
    retry_count = payload["retry_count"]
    permission_errors = payload["permission_errors"]
    stderr_noise = payload["stderr_noise"]

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
    if content_reference_count > 3:
        hints.append("内容参考文件偏多；普通单题建议把内容 reference 控制在 2 到 3 个。")
    if context_estimate > output_estimate * 2:
        hints.append("输入上下文 token 明显高于输出 token；优先压缩 reference 注入而不是压缩最终产物。")
    if validation and not validation.get("ok", False):
        hints.append("校验未通过；优先修复 README 中文性、路径信息或样例成对关系，再继续做性能优化。")
    if retry_count > 0:
        hints.append(f"这次发生了 {retry_count} 次重试；优先把对应步骤脚本化，减少二次写入或编码修复。")
    if permission_errors:
        hints.append("这次记录到了权限相关错误；优先避免需要删除/覆盖锁定文件的写法，并在必要时单独提权清理。")
    if stderr_noise and not permission_errors:
        hints.append("有环境噪音但没有真正的权限失败；后续优先用 -NoProfile 或更安静的 shell 启动方式。")
    if not hints:
        hints.append("这次链路已经比较轻；下一步优先关注稳定性和题目质量，而不是继续压缩。")
    return hints


def append_reference_section(lines: list[str], title: str, items: list[dict], empty_text: str) -> None:
    lines.extend(["", f"## {title}", ""])
    lines.append(f"- 数量：{len(items)}")
    if items:
        for item in items:
            lines.append(f"- `{item['path']}`（估算 {item['estimated_tokens']} tokens）")
    else:
        lines.append(f"- {empty_text}")


def build_markdown(payload: dict) -> str:
    stage_timings = payload["stage_timings_ms"]
    stage_percentages = payload["stage_percentages"]
    tool_counts = payload["tool_counts"]
    reference_groups = payload["reference_groups"]
    primary = payload["primary_bottleneck"]
    secondary = payload["secondary_bottleneck"]
    validation = payload.get("validation")
    write_methods = payload["write_methods"]
    fallback_steps = payload["fallback_steps"]
    permission_errors = payload["permission_errors"]
    stderr_noise = payload["stderr_noise"]

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

    lines.extend(["", "## 工具调用", "", "| 工具 | 次数 |", "| --- | --- |"])
    if tool_counts:
        for name, value in tool_counts.items():
            lines.append(f"| `{name}` | {value} |")
    else:
        lines.append("| `-` | 0 |")

    append_reference_section(lines, "内容参考文件", reference_groups["content"], "这次没有单独记录内容参考文件。")
    append_reference_section(lines, "控制规则文件", reference_groups["control"], "这次没有单独记录控制规则文件。")
    append_reference_section(lines, "Debug 专用文件", reference_groups["debug"], "这次没有额外使用 debug 专用文件。")

    lines.extend(["", "## 重试与降级", ""])
    lines.append(f"- 重试次数：{payload['retry_count']}")
    lines.append(f"- 是否触发降级：{'是' if fallback_steps else '否'}")
    if fallback_steps:
        lines.append("- 降级步骤：")
        for step in fallback_steps:
            lines.append(f"  - {step}")
    else:
        lines.append("- 降级步骤：无")
    if write_methods:
        lines.append("- 主要写入方式：")
        for name, method in write_methods.items():
            lines.append(f"  - `{name}`：{method}")
    else:
        lines.append("- 主要写入方式：未单独记录")

    lines.extend(["", "## 异常与噪音", ""])
    lines.append(f"- 权限错误数：{len(permission_errors)}")
    if permission_errors:
        for item in permission_errors:
            lines.append(f"  - {item}")
    lines.append(f"- stderr / 环境噪音条数：{len(stderr_noise)}")
    if stderr_noise:
        for item in stderr_noise:
            lines.append(f"  - {item}")

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

    if validation:
        lines.extend(["", "## 校验结果", ""])
        lines.append(f"- 总结：{validation.get('summary', '未提供')}")
        lines.append(f"- 是否通过：{'是' if validation.get('ok') else '否'}")
        if "readme_chinese_chars" in validation:
            lines.append(f"- README 中文字符数：{validation['readme_chinese_chars']}")
        failed_checks = [item for item in validation.get("checks", []) if not item.get("ok")]
        if failed_checks:
            lines.append("- 未通过项：")
            for item in failed_checks:
                lines.append(f"  - `{item['name']}`：{item['message']}")

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
            f"- 其中内容参考估算：{token_info['content_reference_estimate']}",
            f"- 其中控制规则估算：{token_info['control_reference_estimate']}",
            f"- 输出估算：{token_info['output_estimate']}",
            f"- 总估算：{token_info['total_estimate']}",
            f"- 说明：{token_info['note']}",
        ]
    )

    files = payload["files_touched"]
    lines.extend(["", "## 变更文件", "", f"- 数量：{files['count']}"])
    for item in files["paths"]:
        lines.append(f"- `{item}`")

    if payload["missing_context_paths"] or payload["missing_reference_paths"] or payload["missing_generated_paths"]:
        lines.extend(["", "## 缺失路径", ""])
        for item in payload["missing_context_paths"]:
            lines.append(f"- 缺失的上下文文件：`{item}`")
        for item in payload["missing_reference_paths"]:
            lines.append(f"- 缺失的参考文件：`{item}`")
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
    parser.add_argument("--validation-json", default="", help="Optional JSON summary from validate_workspace.py")
    parser.add_argument("--retry-count", type=int, default=0)
    parser.add_argument("--fallback-step", action="append", default=[], help="Repeated fallback step descriptions")
    parser.add_argument("--permission-error", action="append", default=[], help="Repeated permission-related errors")
    parser.add_argument("--stderr-note", action="append", default=[], help="Repeated stderr or environment noise notes")
    parser.add_argument("--write-method", action="append", default=[], help="Repeated write method as name=value")
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
        write_methods = parse_text_kv_list(args.write_method)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    target_path = pathlib.Path(args.target_path).resolve() if args.target_path else None
    context_paths = normalize_paths(args.context_file)
    reference_paths = normalize_paths(args.reference_file)
    generated_paths = normalize_paths(args.generated_file)
    if not reference_paths:
        reference_paths = context_paths

    _, context_details, missing_context = estimate_paths(context_paths)
    _, reference_details, missing_references = estimate_paths(reference_paths)
    output_estimate, output_details, missing_generated = estimate_paths(generated_paths)
    reference_groups = split_reference_groups(reference_details)
    content_reference_estimate = token_sum(reference_groups["content"])
    control_reference_estimate = token_sum(reference_groups["control"])
    debug_reference_estimate = token_sum(reference_groups["debug"])
    context_estimate = content_reference_estimate + control_reference_estimate

    total_duration_ms = max(0, int((ended_at - started_at).total_seconds() * 1000))
    if total_duration_ms == 0 and stage_timings:
        total_duration_ms = sum(max(0, value) for value in stage_timings.values())
    stage_percentages = percentage_map(stage_timings, total_duration_ms)
    primary, secondary = pick_bottlenecks(stage_timings)
    if primary is not None:
        primary["percentage"] = stage_percentages.get(primary["stage"], 0.0)
    if secondary is not None:
        secondary["percentage"] = stage_percentages.get(secondary["stage"], 0.0)

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
            "content_reference_estimate": content_reference_estimate,
            "control_reference_estimate": control_reference_estimate,
            "debug_reference_estimate": debug_reference_estimate,
            "output_estimate": output_estimate,
            "total_estimate": context_estimate + output_estimate,
            "note": "按文本长度估算，不是平台 billing 的精确 token；默认不包含 debug 文件本身，也不把 debug 专用规则文件算进主任务上下文。",
        },
        "context_files": context_details,
        "reference_files": reference_details,
        "reference_groups": reference_groups,
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
        "validation": load_validation_summary(args.validation_json),
        "retry_count": max(0, args.retry_count),
        "fallback_steps": args.fallback_step,
        "permission_errors": args.permission_error,
        "stderr_noise": args.stderr_note,
        "write_methods": write_methods,
        "notes": args.note,
    }
    payload["optimization_hints"] = build_optimization_hints(payload)

    md_path, json_path = resolve_report_paths(workspace_root, target_path, args.mode, ended_at)
    md_path.write_text(build_markdown(payload), encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"DEBUG_REPORT_MD={md_path}")
    print(f"DEBUG_REPORT_JSON={json_path}")
    print(f"DEBUG_TOTAL_MS={total_duration_ms}")
    print(f"DEBUG_TOKEN_ESTIMATE={payload['estimated_non_debug_tokens']['total_estimate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
