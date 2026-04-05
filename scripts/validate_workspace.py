#!/usr/bin/env python3
"""
Validate a generated 9044-coach workspace.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


CHINESE_HEADINGS = (
    "## 题目说明",
    "## 输入",
    "## 输出",
    "## 文件说明",
    "## 路径信息",
    "## 考点",
    "## 常见错误",
    "## 如何开始",
)


def check(condition: bool, name: str, success: str, failure: str) -> dict:
    return {
        "name": name,
        "ok": bool(condition),
        "message": success if condition else failure,
    }


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def required_pairs(kind: str) -> list[tuple[str, str]]:
    pairs = [
        (f"data/sample0{i}_input.txt", f"expected/sample0{i}_output.txt")
        for i in range(1, 4)
    ]
    pairs.extend(
        (f"data/edge0{i}_input.txt", f"expected/edge0{i}_output.txt")
        for i in range(1, 3)
    )
    return pairs


def validate_workspace(workspace: pathlib.Path, language: str) -> dict:
    checks: list[dict] = []
    solution_name = "solution.sh" if language == "shell" else "solution.py"
    test_name = "tests/run_tests.sh" if language == "shell" else "tests/run_tests.py"

    readme = workspace / "README.md"
    metadata = workspace / "metadata.json"
    notebook = workspace / "notebook.md"
    solution = workspace / solution_name
    test_runner = workspace / test_name

    required_paths = [readme, metadata, notebook, solution, test_runner]
    for left, right in required_pairs(language):
        required_paths.append(workspace / left)
        required_paths.append(workspace / right)

    missing_paths = [str(path) for path in required_paths if not path.exists()]
    checks.append(
        check(
            not missing_paths,
            "required_paths",
            "工作区必需文件齐全。",
            "工作区缺少必需文件。",
        )
    )

    readme_text = read_text(readme) if readme.exists() else ""
    metadata_text = read_text(metadata) if metadata.exists() else "{}"
    test_text = read_text(test_runner) if test_runner.exists() else ""

    checks.append(
        check(
            readme_text and not readme_text.startswith("\ufeff"),
            "readme_utf8",
            "README 使用无 BOM 的 UTF-8。",
            "README 编码异常，可能含 BOM 或为空。",
        )
    )
    checks.append(
        check(
            all(heading in readme_text for heading in CHINESE_HEADINGS),
            "readme_chinese_headings",
            "README 包含规定的中文标题。",
            "README 缺少规定的中文标题。",
        )
    )
    checks.append(
        check(
            chinese_char_count(readme_text) >= 80,
            "readme_chinese_content",
            "README 中文内容充足。",
            "README 中文内容过少，可能仍然偏英文或模板未填完整。",
        )
    )
    checks.append(
        check(
            "WSL 路径" in readme_text and "cd /mnt/" in readme_text,
            "readme_wsl_path",
            "README 包含 WSL 路径与 cd 命令。",
            "README 缺少 WSL 路径或 cd 命令。",
        )
    )
    checks.append(
        check(
            solution_name in readme_text and solution_name in test_text,
            "solution_linkage",
            "README 和测试脚本都指向正确的答案文件。",
            "README 或测试脚本没有指向正确的答案文件。",
        )
    )

    try:
        metadata_json = json.loads(metadata_text)
    except json.JSONDecodeError:
        metadata_json = {}
    checks.append(
        check(
            isinstance(metadata_json, dict)
            and {"title", "language", "topic_hint", "topics", "status"} <= set(metadata_json.keys()),
            "metadata_shape",
            "metadata.json 结构完整。",
            "metadata.json 缺少必要字段。",
        )
    )

    pairs_ok = True
    bad_pairs: list[str] = []
    for left, right in required_pairs(language):
        left_path = workspace / left
        right_path = workspace / right
        if left_path.exists() != right_path.exists():
            pairs_ok = False
            bad_pairs.append(f"{left} <-> {right}")
    checks.append(
        check(
            pairs_ok,
            "case_pairs",
            "data/ 与 expected/ 的样例文件成对存在。",
            "data/ 与 expected/ 存在不成对的样例文件。",
        )
    )

    ok = all(item["ok"] for item in checks)
    errors = [item["message"] for item in checks if not item["ok"]]
    summary = "工作区校验通过。" if ok else "工作区校验未通过。"
    if bad_pairs:
        errors.append("不成对样例：" + ", ".join(bad_pairs))

    return {
        "workspace": str(workspace),
        "language": language,
        "ok": ok,
        "summary": summary,
        "checks": checks,
        "missing_paths": missing_paths,
        "errors": errors,
        "readme_chinese_chars": chinese_char_count(readme_text),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--language", choices=("shell", "python"), default="shell")
    parser.add_argument("--json-out", default="")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    workspace = pathlib.Path(args.workspace).resolve()
    if not workspace.exists():
        print(f"ERROR: workspace not found: {workspace}", file=sys.stderr)
        return 2

    result = validate_workspace(workspace, args.language)
    if args.json_out:
        json_out = pathlib.Path(args.json_out).resolve()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"VALIDATION_JSON={json_out}")

    print(f"VALIDATION_OK={'1' if result['ok'] else '0'}")
    print(f"VALIDATION_SUMMARY={result['summary']}")
    for check_item in result["checks"]:
        status = "PASS" if check_item["ok"] else "FAIL"
        print(f"VALIDATION_CHECK={status}:{check_item['name']}:{check_item['message']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
