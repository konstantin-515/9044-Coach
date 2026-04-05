#!/usr/bin/env python3
"""
Fill a scaffolded 9044-coach workspace from a compact JSON spec.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from init_workspace import (
    EDGE_CASES,
    SAMPLE_CASES,
    build_notebook,
    build_python_placeholder,
    build_python_test,
    build_shell_test,
    build_solution_placeholder,
    windows_to_wsl,
    write_file,
)
from render_workspace_docs import build_readme, load_or_create_metadata


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--spec-json", required=True)
    parser.add_argument("--overwrite-notebook", action="store_true")
    parser.add_argument("--refresh-solution-placeholder", action="store_true")
    return parser.parse_args(argv)


def load_spec(path: pathlib.Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"failed to read spec json: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("spec json must be an object")
    return data


def text_value(payload: dict, key: str, fallback: str) -> str:
    value = payload.get(key, fallback)
    if value is None:
        return fallback
    return str(value).strip() or fallback


def list_value(payload: dict, key: str) -> list[str]:
    raw = payload.get(key, [])
    if not isinstance(raw, list):
        return []
    return [str(item).strip() for item in raw if str(item).strip()]


def normalize_cases(raw_cases: object, default_names: tuple[str, ...]) -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []
    items = raw_cases if isinstance(raw_cases, list) else []
    for index, raw in enumerate(items):
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name", "")).strip() or f"{default_names[0][:-2]}{index + 1:02d}"
        cases.append(
            {
                "name": name,
                "input": str(raw.get("input", "")),
                "expected": str(raw.get("expected", "")),
                "reason": str(raw.get("reason", "")).strip(),
            }
        )
    for index, name in enumerate(default_names):
        if index < len(cases):
            continue
        cases.append(
            {
                "name": name,
                "input": "",
                "expected": "",
                "reason": "",
            }
        )
    return cases


def remove_case_files(workspace: pathlib.Path) -> None:
    data_dir = workspace / "data"
    expected_dir = workspace / "expected"
    for pattern in ("sample*_input.txt", "edge*_input.txt"):
        for path in data_dir.glob(pattern):
            if path.is_file():
                try:
                    path.unlink()
                except OSError:
                    # Rewriting the canonical case files is enough for this workflow.
                    pass
    for pattern in ("sample*_output.txt", "edge*_output.txt"):
        for path in expected_dir.glob(pattern):
            if path.is_file():
                try:
                    path.unlink()
                except OSError:
                    pass


def write_cases(workspace: pathlib.Path, sample_cases: list[dict[str, str]], edge_cases: list[dict[str, str]]) -> int:
    remove_case_files(workspace)
    count = 0
    for case in [*sample_cases, *edge_cases]:
        write_file(workspace / "data" / f"{case['name']}_input.txt", case["input"])
        write_file(workspace / "expected" / f"{case['name']}_output.txt", case["expected"])
        count += 1
    return count


def refresh_solution_and_tests(
    workspace: pathlib.Path,
    *,
    language: str,
    refresh_solution_placeholder: bool,
) -> tuple[str, str, str]:
    wsl_path = windows_to_wsl(workspace)
    tests_dir = workspace / "tests"

    if language == "shell":
        solution_name = "solution.sh"
        test_name = "run_tests.sh"
        test_content = build_shell_test()
        solution_content = build_solution_placeholder(wsl_path)
        run_command = "dash solution.sh < data/sample01_input.txt"
        test_command = "dash tests/run_tests.sh"
        stale_paths = [workspace / "solution.py", tests_dir / "run_tests.py"]
    else:
        solution_name = "solution.py"
        test_name = "run_tests.py"
        test_content = build_python_test()
        solution_content = build_python_placeholder(wsl_path)
        run_command = "python3 solution.py < data/sample01_input.txt"
        test_command = "python3 tests/run_tests.py"
        stale_paths = [workspace / "solution.sh", tests_dir / "run_tests.sh"]

    for path in stale_paths:
        if path.exists():
            path.unlink()

    test_path = tests_dir / test_name
    write_file(test_path, test_content)

    solution_path = workspace / solution_name
    if refresh_solution_placeholder or not solution_path.exists():
        write_file(solution_path, solution_content)

    return solution_name, run_command, test_command


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    workspace = pathlib.Path(args.workspace).resolve()
    spec_path = pathlib.Path(args.spec_json).resolve()

    if not workspace.exists():
        print(f"ERROR: workspace not found: {workspace}", file=sys.stderr)
        return 2

    try:
        spec = load_spec(spec_path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    language = text_value(spec, "language", "shell")
    if language not in {"shell", "python"}:
        print(f"ERROR: unsupported language: {language}", file=sys.stderr)
        return 2

    title = text_value(spec, "title", "练习题")
    task = text_value(spec, "task", "请补充完整题面。")
    input_desc = text_value(spec, "input_desc", "请补充输入格式说明。")
    output_desc = text_value(spec, "output_desc", "请补充输出格式说明。")
    topic_hint = text_value(spec, "topic_hint", "")
    status = text_value(spec, "status", "active")

    constraints = list_value(spec, "constraints")
    knowledge_points = list_value(spec, "knowledge_points")
    common_mistakes = list_value(spec, "common_mistakes")
    topics = list_value(spec, "topics")

    sample_cases = normalize_cases(spec.get("sample_cases"), SAMPLE_CASES)
    edge_cases = normalize_cases(spec.get("edge_cases"), EDGE_CASES)

    solution_name, run_command, test_command = refresh_solution_and_tests(
        workspace,
        language=language,
        refresh_solution_placeholder=args.refresh_solution_placeholder,
    )

    case_count = write_cases(workspace, sample_cases, edge_cases)

    readme_path = workspace / "README.md"
    metadata_path = workspace / "metadata.json"
    notebook_path = workspace / "notebook.md"

    readme_text = build_readme(
        title=title,
        win_path=str(workspace),
        wsl_path=windows_to_wsl(workspace),
        solution_name=solution_name,
        test_command=test_command,
        run_command=run_command,
        task=task,
        input_desc=input_desc,
        output_desc=output_desc,
        constraints=constraints,
        knowledge_points=knowledge_points,
        common_mistakes=common_mistakes,
        sample_cases=sample_cases,
        edge_cases=edge_cases,
    )
    write_file(readme_path, readme_text)

    metadata = load_or_create_metadata(metadata_path, title=title, language=language)
    metadata["title"] = title
    metadata["language"] = language
    metadata["topic_hint"] = topic_hint or metadata.get("topic_hint", "")
    metadata["topics"] = topics or metadata.get("topics", [])
    metadata["status"] = status or metadata.get("status", "active")
    metadata["case_count"] = {
        "sample": len(sample_cases),
        "edge": len(edge_cases),
    }
    write_file(metadata_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")

    if args.overwrite_notebook or not notebook_path.exists():
        write_file(notebook_path, build_notebook(title))

    print(f"FILLED_WORKSPACE={workspace}")
    print(f"USED_SPEC={spec_path}")
    print(f"UPDATED_README={readme_path}")
    print(f"UPDATED_METADATA={metadata_path}")
    print(f"WROTE_CASES={case_count}")
    print(f"WRITE_METHOD=spec-driven")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
