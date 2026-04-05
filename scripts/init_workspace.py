#!/usr/bin/env python3
"""
Create a numbered practice-workspace scaffold for 9044-coach.

This script creates the folder and baseline files so the skill can fill them
with question-specific content afterwards.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

SAMPLE_CASES = ("sample01", "sample02", "sample03")
EDGE_CASES = ("edge01", "edge02")


def windows_to_wsl(path: pathlib.Path) -> str:
    raw = str(path.resolve())
    match = re.match(r"^([A-Za-z]):\\(.*)$", raw)
    if not match:
        return raw.replace("\\", "/")
    drive = match.group(1).lower()
    rest = match.group(2).replace("\\", "/")
    return f"/mnt/{drive}/{rest}"


def next_test_name(root: pathlib.Path) -> str:
    max_num = 0
    pattern = re.compile(r"^test(\d+)$")
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        match = pattern.match(entry.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"test{max_num + 1:02d}"


def write_file(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build_metadata(title: str, lang: str) -> str:
    payload = {
        "title": title,
        "language": lang,
        "topic_hint": "",
        "topics": [],
        "status": "active",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def build_readme(
    title: str,
    win_path: str,
    wsl_path: str,
    solution_name: str,
    test_runner: str,
    run_command: str,
    test_command: str,
) -> str:
    return f"""# {title}

## 题目说明

请在这里填写题目说明。

## 输入

请在这里填写输入说明。

## 输出

请在这里填写输出说明。

## 要求与限制

- 默认按课程风格使用 `dash`
- 如果需要 `grep -E`、`sed`、`awk`，请在题目中补充具体要求

## 文件说明

| 路径 | 用途 |
| --- | --- |
| `{solution_name}` | 你要完成的答案文件 |
| `data/sample01_input.txt` | 基础样例 1 |
| `data/sample02_input.txt` | 基础样例 2 |
| `data/sample03_input.txt` | 格式或筛选样例 |
| `data/edge01_input.txt` | 边界样例 1 |
| `data/edge02_input.txt` | 边界样例 2 |
| `expected/` | 与每个输入文件对应的期望输出 |
| `tests/{test_runner}` | 测试脚本 |
| `notebook.md` | 你的复习笔记 |
| `metadata.json` | 练习元数据与归档主题提示 |

## 路径信息

- Windows 路径：`{win_path}`
- WSL 路径：`{wsl_path}`

进入目录：

```sh
cd {wsl_path}
```

## 样例测试

默认应至少提供 3 个可见样例：

- `sample01`
- `sample02`
- `sample03`

## 边界情况

默认应至少提供 2 个可见边界案例：

- `edge01`
- `edge02`

## 评分关注点

| 测试类别 | 目的 | 输入特征 | 常见错误 |
| --- | --- | --- | --- |
| 基础正确性 | 验证核心逻辑 | 规则、干净、格式正常的输入 | 只能通过最简单的 happy path |
| 多样例覆盖 | 验证是否适配不同输入形态 | 几个可见样例分别覆盖不同模式 | 只对一种样例写死处理 |
| 边界处理 | 验证边界和脏数据情况 | 空行、重复、额外空格、大小写混合 | 忽略特殊情况 |
| 输出格式 | 验证输出是否完全匹配 | 严格的逐行输出 | 多空格、顺序错误、漏换行 |

## 考点

- 

## 常见错误

- 

## 如何开始

请在 `{solution_name}` 中完成你的答案。

运行测试：

```sh
{test_command}
```

如果你在 Windows 下练习，推荐流程：

```text
1. 在 PowerShell 中启动 WSL
2. 执行上面的 cd 命令进入当前练习目录
3. 先用其中一个样例试跑：{run_command}
4. 再运行完整测试：{test_command}
```
"""


def build_notebook(title: str) -> str:
    return f"""# 学习笔记

## 基本信息

- 日期：
- 题目：{title}
- 类型：
- 我这次是否独立完成：

## 我一开始的思路

- 

## 我卡住的点

- 

## 我做错的点

- 

## 需要记住的命令/选项

- `grep -E`：
- `grep -o`：
- `sed`：
- `awk`：
- `sort`：
- `uniq`：

## 这题里值得复习的例子

```sh
# 把你想记住的命令写在这里
```

## 下次再做这题时要提醒自己的话

- 
"""


def build_solution_placeholder(folder_wsl_path: str) -> str:
    return f"""#!/bin/dash
# 在 Windows 上可以这样运行：
# 1. 在 PowerShell 中启动 WSL
# 2. cd 到这个练习目录
# 3. 执行：cd {folder_wsl_path}
# 4. 运行：dash solution.sh < data/sample01_input.txt
# 5. 测试：dash tests/run_tests.sh
#
# 在下面写你的答案。
"""


def build_python_placeholder(folder_wsl_path: str) -> str:
    return f"""#!/usr/bin/env python3
# 在 Windows 上可以这样运行：
# 1. 在 PowerShell 中启动 WSL
# 2. cd 到这个练习目录
# 3. 执行：cd {folder_wsl_path}
# 4. 运行：python3 solution.py < data/sample01_input.txt
# 5. 测试：python3 tests/run_tests.py
#
# 在下面写你的答案。
"""


def build_shell_test() -> str:
    return """#!/bin/dash

target="./solution.sh"
artifact_dir="./tests/.artifacts"

if [ ! -f "$target" ]; then
    echo "Missing $target"
    exit 1
fi

mkdir -p "$artifact_dir"

pass_count=0
test_count=0

print_line_count() {
    file="$1"
    awk 'END { print NR }' "$file"
}

has_trailing_newline() {
    file="$1"
    [ ! -s "$file" ] && return 0
    last_char="$(tail -c 1 "$file" 2>/dev/null)"
    [ -z "$last_char" ]
}

show_diff_excerpt() {
    expected_file="$1"
    actual_file="$2"
    diff -u "$expected_file" "$actual_file" | sed -n '1,12p'
}

compare_without_final_newline() {
    expected_file="$1"
    actual_file="$2"
    expected_tmp="$(mktemp)"
    actual_tmp="$(mktemp)"

    awk '{ print }' "$expected_file" > "$expected_tmp"
    awk '{ print }' "$actual_file" > "$actual_tmp"

    if cmp -s "$expected_tmp" "$actual_tmp"; then
        result=0
    else
        result=1
    fi

    rm -f "$expected_tmp" "$actual_tmp"
    return "$result"
}

run_case() {
    name="$1"
    input_file="$2"
    expected_file="$3"
    reason="$4"

    test_count=$((test_count + 1))
    actual_file="$artifact_dir/$name.actual.txt"
    rm -f "$actual_file"

    if ! dash "$target" < "$input_file" > "$actual_file"; then
        echo "FAIL: $name"
        echo "Reason: command exited with non-zero status"
        echo "Actual output path: $actual_file"
        return
    fi

    if diff -u "$expected_file" "$actual_file" > /dev/null 2>&1; then
        echo "PASS: $name"
        pass_count=$((pass_count + 1))
        rm -f "$actual_file"
    else
        echo "FAIL: $name"
        expected_lines="$(print_line_count "$expected_file")"
        actual_lines="$(print_line_count "$actual_file")"

        if compare_without_final_newline "$expected_file" "$actual_file"; then
            echo "Reason: content matches but trailing newline handling is different"
        elif [ "$expected_lines" != "$actual_lines" ]; then
            echo "Reason: line count differs"
            echo "Expected lines: $expected_lines"
            echo "Actual lines:   $actual_lines"
        else
            echo "Reason: $reason"
        fi

        if has_trailing_newline "$expected_file" && ! has_trailing_newline "$actual_file"; then
            echo "Hint: expected output ends with a newline, but your output does not"
        elif ! has_trailing_newline "$expected_file" && has_trailing_newline "$actual_file"; then
            echo "Hint: your output ends with an extra trailing newline"
        fi

        echo "Expected output path: $expected_file"
        echo "Actual output path:   $actual_file"
        echo "Diff excerpt:"
        show_diff_excerpt "$expected_file" "$actual_file"
    fi
}

run_case_group() {
    prefix="$1"
    reason="$2"

    for input_file in data/${prefix}[0-9][0-9]_input.txt; do
        [ -f "$input_file" ] || continue
        file_name="${input_file##*/}"
        case_name="${file_name%_input.txt}"
        expected_file="expected/${case_name}_output.txt"

        if [ ! -f "$expected_file" ]; then
            echo "SKIP: $case_name"
            echo "Reason: missing expected file $expected_file"
            continue
        fi

        run_case "$case_name" "$input_file" "$expected_file" "$reason"
    done
}

run_case_group "sample" "output mismatch on a visible sample case"
run_case_group "edge" "edge-case handling is incorrect"

echo "$pass_count/$test_count tests passed"
"""


def build_python_test() -> str:
    return """#!/usr/bin/env python3
from __future__ import annotations

import difflib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "solution.py"
ARTIFACT_DIR = ROOT / "tests" / ".artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def has_trailing_newline(text: str) -> bool:
    return text == "" or text.endswith("\\n")


def run_case(case_name: str, input_path: pathlib.Path, expected_path: pathlib.Path, reason: str) -> bool:
    actual_path = ARTIFACT_DIR / f"{case_name}.actual.txt"
    if actual_path.exists():
        actual_path.unlink()

    try:
        completed = subprocess.run(
            ["python3", str(TARGET)],
            input=input_path.read_text(encoding="utf-8"),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        print(f"FAIL: {case_name}")
        print(f"Reason: could not start python3: {error}")
        return False

    actual_path.write_text(completed.stdout, encoding="utf-8", newline="")

    if completed.returncode != 0:
        print(f"FAIL: {case_name}")
        print("Reason: command exited with non-zero status")
        print(f"Actual output path: {actual_path}")
        if completed.stderr:
            print("stderr:")
            print(completed.stderr.rstrip())
        return False

    expected = expected_path.read_text(encoding="utf-8")
    actual = completed.stdout

    if actual == expected:
        print(f"PASS: {case_name}")
        actual_path.unlink(missing_ok=True)
        return True

    print(f"FAIL: {case_name}")
    expected_lines = len(expected.splitlines())
    actual_lines = len(actual.splitlines())

    if expected.rstrip("\\n") == actual.rstrip("\\n"):
        print("Reason: content matches but trailing newline handling is different")
    elif expected_lines != actual_lines:
        print("Reason: line count differs")
        print(f"Expected lines: {expected_lines}")
        print(f"Actual lines:   {actual_lines}")
    else:
        print(f"Reason: {reason}")

    if has_trailing_newline(expected) and not has_trailing_newline(actual):
        print("Hint: expected output ends with a newline, but your output does not")
    elif not has_trailing_newline(expected) and has_trailing_newline(actual):
        print("Hint: your output ends with an extra trailing newline")

    print(f"Expected output path: {expected_path}")
    print(f"Actual output path:   {actual_path}")
    print("Diff excerpt:")
    diff_lines = list(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=str(expected_path),
            tofile=str(actual_path),
            n=2,
        )
    )
    for line in diff_lines[:12]:
        sys.stdout.write(line)
    if diff_lines and not diff_lines[-1].endswith("\\n"):
        print()
    return False


def run_group(prefix: str, reason: str) -> tuple[int, int]:
    passed = 0
    total = 0
    for input_path in sorted((ROOT / "data").glob(f"{prefix}[0-9][0-9]_input.txt")):
        case_name = input_path.name.removesuffix("_input.txt")
        expected_path = ROOT / "expected" / f"{case_name}_output.txt"
        if not expected_path.exists():
            print(f"SKIP: {case_name}")
            print(f"Reason: missing expected file {expected_path}")
            continue
        total += 1
        if run_case(case_name, input_path, expected_path, reason):
            passed += 1
    return passed, total


def main() -> int:
    if not TARGET.exists():
        print(f"Missing {TARGET}")
        return 1

    sample_pass, sample_total = run_group("sample", "output mismatch on a visible sample case")
    edge_pass, edge_total = run_group("edge", "edge-case handling is incorrect")
    passed = sample_pass + edge_pass
    total = sample_total + edge_total
    print(f"{passed}/{total} tests passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Parent directory that contains testNN folders")
    parser.add_argument("--name", help="Exact folder name, default is next available testNN")
    parser.add_argument("--lang", choices=("shell", "python"), default="shell")
    parser.add_argument("--title", default="练习题")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=True)

    name = args.name or next_test_name(root)
    folder = root / name
    if folder.exists():
        print(f"ERROR: target folder already exists: {folder}", file=sys.stderr)
        return 2

    data_dir = folder / "data"
    expected_dir = folder / "expected"
    tests_dir = folder / "tests"
    artifacts_dir = tests_dir / ".artifacts"
    for path in (data_dir, expected_dir, tests_dir, artifacts_dir):
        path.mkdir(parents=True, exist_ok=True)

    windows_path = str(folder)
    wsl_path = windows_to_wsl(folder)

    if args.lang == "shell":
        solution_name = "solution.sh"
        test_runner = "run_tests.sh"
        solution_content = build_solution_placeholder(wsl_path)
        test_content = build_shell_test()
        run_command = "dash solution.sh < data/sample01_input.txt"
        test_command = "dash tests/run_tests.sh"
    else:
        solution_name = "solution.py"
        test_runner = "run_tests.py"
        solution_content = build_python_placeholder(wsl_path)
        test_content = build_python_test()
        run_command = "python3 solution.py < data/sample01_input.txt"
        test_command = "python3 tests/run_tests.py"

    write_file(
        folder / "README.md",
        build_readme(
            args.title,
            windows_path,
            wsl_path,
            solution_name,
            test_runner,
            run_command,
            test_command,
        ),
    )
    write_file(folder / "metadata.json", build_metadata(args.title, args.lang))
    write_file(folder / "notebook.md", build_notebook(args.title))
    write_file(folder / solution_name, solution_content)
    write_file(tests_dir / test_runner, test_content)
    for case_name in SAMPLE_CASES:
        write_file(data_dir / f"{case_name}_input.txt", "")
        write_file(expected_dir / f"{case_name}_output.txt", "")
    for case_name in EDGE_CASES:
        write_file(data_dir / f"{case_name}_input.txt", "")
        write_file(expected_dir / f"{case_name}_output.txt", "")

    print(f"CREATED_FOLDER={folder}")
    print(f"WSL_PATH={wsl_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
