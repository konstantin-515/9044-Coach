#!/usr/bin/env python3
"""
Render Chinese workspace docs for a generated 9044-coach exercise.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from init_workspace import windows_to_wsl, write_file


SAMPLE_CASES = ("sample01", "sample02", "sample03")
EDGE_CASES = ("edge01", "edge02")


def bullet_lines(items: list[str], fallback: str) -> str:
    clean = [item.strip() for item in items if item.strip()]
    if not clean:
        clean = [fallback]
    return "\n".join(f"- {item}" for item in clean)


def build_readme(
    *,
    title: str,
    win_path: str,
    wsl_path: str,
    solution_name: str,
    test_command: str,
    run_command: str,
    task: str,
    input_desc: str,
    output_desc: str,
    constraints: list[str],
    knowledge_points: list[str],
    common_mistakes: list[str],
) -> str:
    return f"""# {title}

## 题目说明

{task}

## 输入

{input_desc}

## 输出

{output_desc}

## 要求与限制

{bullet_lines(constraints, "按题目要求精确处理输入输出格式。")}

## 文件说明

| 路径 | 用途 |
| --- | --- |
| `{solution_name}` | 你要完成的答案文件 |
| `data/sample01_input.txt` | 基础样例 1 |
| `data/sample02_input.txt` | 基础样例 2 |
| `data/sample03_input.txt` | 基础样例 3 |
| `data/edge01_input.txt` | 边界样例 1 |
| `data/edge02_input.txt` | 边界样例 2 |
| `expected/` | 与输入文件对应的期望输出 |
| `tests/run_tests.sh` | 测试脚本 |
| `notebook.md` | 你的复习笔记 |
| `metadata.json` | 主题与归档提示 |

## 路径信息

- Windows 路径：`{win_path}`
- WSL 路径：`{wsl_path}`

进入目录：

```sh
cd {wsl_path}
```

## 可见样例

{bullet_lines(list(SAMPLE_CASES), "sample01")}

## 可见边界案例

{bullet_lines(list(EDGE_CASES), "edge01")}

## 评分关注点

| 测试类别 | 目的 | 输入特征 | 常见错误 |
| --- | --- | --- | --- |
| 基础正确性 | 验证核心逻辑 | 正常、干净、格式规则的输入 | 只处理最简单情况 |
| 多样例覆盖 | 验证是否适配多种可见样例 | 不同模式的几组输入 | 针对某个样例写死逻辑 |
| 边界处理 | 验证特殊情况 | 空行、重复、额外空格、大小写混合 | 漏掉特殊情况 |
| 输出格式 | 验证精确输出 | 严格逐行比对 | 顺序错、空格错、漏换行 |

## 考点

{bullet_lines(knowledge_points, "补充这一题重点训练的语法点。")}

## 常见错误

{bullet_lines(common_mistakes, "补充这题最容易做错的地方。")}

## 如何开始

请在 `{solution_name}` 中完成你的答案。

先试跑一个样例：

```sh
{run_command}
```

再运行完整测试：

```sh
{test_command}
```

如果你在 Windows 下练习，推荐流程：

```text
1. 在 PowerShell 中启动 WSL
2. 执行上面的 cd 命令进入当前练习目录
3. 先用一个样例试跑
4. 再运行完整测试
```
"""


def load_or_create_metadata(path: pathlib.Path, *, title: str, language: str) -> dict:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "title": title,
        "language": language,
        "topic_hint": "",
        "topics": [],
        "status": "active",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--language", choices=("shell", "python"), default="shell")
    parser.add_argument("--title", required=True)
    parser.add_argument("--topic-hint", default="")
    parser.add_argument("--status", default="active")
    parser.add_argument("--task", default="请补充完整题面。")
    parser.add_argument("--input-desc", default="请补充输入格式说明。")
    parser.add_argument("--output-desc", default="请补充输出格式说明。")
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--knowledge-point", action="append", default=[])
    parser.add_argument("--common-mistake", action="append", default=[])
    parser.add_argument("--topic", action="append", default=[])
    parser.add_argument("--overwrite-notebook", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    workspace = pathlib.Path(args.workspace).resolve()
    if not workspace.exists():
        print(f"ERROR: workspace not found: {workspace}", file=sys.stderr)
        return 2

    win_path = str(workspace)
    wsl_path = windows_to_wsl(workspace)
    solution_name = "solution.sh" if args.language == "shell" else "solution.py"
    run_command = (
        f"dash {solution_name} < data/sample01_input.txt"
        if args.language == "shell"
        else f"python3 {solution_name} < data/sample01_input.txt"
    )
    test_command = (
        "dash tests/run_tests.sh"
        if args.language == "shell"
        else "python3 tests/run_tests.py"
    )

    readme_path = workspace / "README.md"
    metadata_path = workspace / "metadata.json"
    notebook_path = workspace / "notebook.md"

    should_write_notebook = args.overwrite_notebook or not notebook_path.exists()

    readme_text = build_readme(
        title=args.title,
        win_path=win_path,
        wsl_path=wsl_path,
        solution_name=solution_name,
        test_command=test_command,
        run_command=run_command,
        task=args.task,
        input_desc=args.input_desc,
        output_desc=args.output_desc,
        constraints=args.constraint,
        knowledge_points=args.knowledge_point,
        common_mistakes=args.common_mistake,
    )
    write_file(readme_path, readme_text)

    metadata = load_or_create_metadata(metadata_path, title=args.title, language=args.language)
    metadata["title"] = args.title
    metadata["language"] = args.language
    metadata["topic_hint"] = args.topic_hint or metadata.get("topic_hint", "")
    metadata["topics"] = [topic for topic in args.topic if topic.strip()] or metadata.get("topics", [])
    metadata["status"] = args.status or metadata.get("status", "active")
    write_file(metadata_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")

    if should_write_notebook:
        notebook = (
            "# 学习笔记\n\n"
            "## 基本信息\n\n"
            f"- 日期：\n- 题目：{args.title}\n- 类型：\n- 我这次是否独立完成：\n\n"
            "## 我一开始的思路\n\n- \n\n"
            "## 我卡住的点\n\n- \n\n"
            "## 我做错的点\n\n- \n\n"
            "## 需要记住的命令/选项\n\n"
            "- `grep -E`：\n- `grep -o`：\n- `sed`：\n- `awk`：\n- `sort`：\n- `uniq`：\n\n"
            "## 这题里值得复习的例子\n\n```sh\n# 把你想记住的命令写在这里\n```\n\n"
            "## 下次再做这题时要提醒自己的话\n\n- \n"
        )
        write_file(notebook_path, notebook)

    print(f"RENDERED_README={readme_path}")
    print(f"UPDATED_METADATA={metadata_path}")
    if should_write_notebook:
        print(f"UPDATED_NOTEBOOK={notebook_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
