#!/usr/bin/env python3
"""
Summarize archived notebook.md files into a revision report.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import sys


PLACEHOLDER_ITEMS = {
    "日期：",
    "题目：",
    "类型：",
    "我这次是否独立完成：",
    "`grep -E`：",
    "`grep -o`：",
    "`sed`：",
    "`awk`：",
    "`sort`：",
    "`uniq`：",
    "# 把你想记住的命令写在这里",
}

SECTION_LABELS = {
    "我卡住的点": "stuck_points",
    "我做错的点": "mistakes",
    "需要记住的命令/选项": "commands",
    "下次再做这题时要提醒自己的话": "reminders",
}


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def read_metadata(folder: pathlib.Path) -> dict:
    path = folder / "metadata.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def parse_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    in_code = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip()
            sections.setdefault(current, [])
            continue

        if current is None or not stripped:
            continue

        sections.setdefault(current, []).append(stripped)

    return sections


def clean_item(raw: str) -> str:
    item = raw.strip()
    if item.startswith("- "):
        item = item[2:].strip()
    item = item.strip()
    return item


def extract_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for raw in lines:
        item = clean_item(raw)
        if not item or item in PLACEHOLDER_ITEMS:
            continue
        if item.endswith("：") or item.endswith(":"):
            continue
        items.append(item)
    return items


def normalize_command(item: str) -> str:
    command = item.split("：", 1)[0].split(":", 1)[0].strip()
    command = command.strip("`").strip()
    return command or item


def topic_from_path(folder: pathlib.Path, archives_root: pathlib.Path) -> str:
    try:
        relative = folder.relative_to(archives_root)
    except ValueError:
        return "misc"
    parts = relative.parts
    if len(parts) >= 2 and parts[0] != "_summaries":
        return parts[0]
    return "misc"


def collect_entries(archives_root: pathlib.Path, topic_filter: str | None) -> list[dict]:
    entries: list[dict] = []
    if not archives_root.exists():
        return entries

    for notebook in sorted(archives_root.rglob("notebook.md")):
        folder = notebook.parent
        topic = topic_from_path(folder, archives_root)
        if topic == "_summaries":
            continue
        if topic_filter and topic != topic_filter:
            continue

        metadata = read_metadata(folder)
        sections = parse_sections(read_text(notebook))
        title = str(metadata.get("title", "")).strip() or folder.name
        exercise_name = folder.name

        entry = {
            "topic": str(metadata.get("topic_hint", "")).strip() or topic,
            "archive_topic": topic,
            "exercise": exercise_name,
            "title": title,
            "language": str(metadata.get("language", "")).strip(),
            "path": str(folder),
            "stuck_points": extract_items(sections.get("我卡住的点", [])),
            "mistakes": extract_items(sections.get("我做错的点", [])),
            "commands": extract_items(sections.get("需要记住的命令/选项", [])),
            "reminders": extract_items(sections.get("下次再做这题时要提醒自己的话", [])),
        }
        entries.append(entry)

    return entries


def bullet_lines(items: list[str], fallback: str) -> list[str]:
    if not items:
        return [f"- {fallback}"]
    return [f"- {item}" for item in items]


def top_counter_lines(counter: collections.Counter[str], limit: int, fallback: str) -> list[str]:
    if not counter:
        return [f"- {fallback}"]
    return [f"- {item} ({count})" for item, count in counter.most_common(limit)]


def build_markdown(entries: list[dict], topic_filter: str | None) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    title_suffix = f"（主题：{topic_filter}）" if topic_filter else ""

    topic_groups: dict[str, list[dict]] = collections.defaultdict(list)
    global_mistakes: collections.Counter[str] = collections.Counter()
    global_commands: collections.Counter[str] = collections.Counter()
    global_stuck: collections.Counter[str] = collections.Counter()
    global_reminders: collections.Counter[str] = collections.Counter()

    for entry in entries:
        topic_groups[entry["archive_topic"]].append(entry)
        global_mistakes.update(entry["mistakes"])
        global_stuck.update(entry["stuck_points"])
        global_reminders.update(entry["reminders"])
        global_commands.update(normalize_command(item) for item in entry["commands"])

    lines: list[str] = [
        f"# 归档错因总结{title_suffix}",
        "",
        f"- 生成时间：{now}",
        f"- 扫描的归档笔记数：{len(entries)}",
        f"- 涉及主题数：{len(topic_groups)}",
        "",
        "## 总览",
        "",
    ]

    if not entries:
        lines.extend(
            [
                "- 目前还没有可用的归档笔记。",
                "- 先把做完的练习归档，再在每题的 `notebook.md` 里记录卡点和错因。",
                "- 下次运行这个总结功能时，就会自动聚合这些内容。",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "| Topic | Notebook Count | Exercises |",
            "| --- | --- | --- |",
        ]
    )
    for topic in sorted(topic_groups):
        exercise_list = ", ".join(entry["exercise"] for entry in topic_groups[topic])
        lines.append(f"| `{topic}` | {len(topic_groups[topic])} | {exercise_list} |")

    lines.extend(
        [
            "",
            "## 高频卡点",
            "",
            *top_counter_lines(global_stuck + global_mistakes, 8, "目前还没有重复出现的卡点记录"),
            "",
            "## 最常需要复习的命令/选项",
            "",
            *top_counter_lines(global_commands, 8, "目前还没有记录命令/选项"),
        ]
    )

    if global_reminders:
        lines.extend(
            [
                "",
                "## 最常出现的提醒",
                "",
                *top_counter_lines(global_reminders, 8, "目前还没有记录提醒"),
            ]
        )

    for topic in sorted(topic_groups):
        topic_entries = topic_groups[topic]
        topic_stuck: collections.Counter[str] = collections.Counter()
        topic_mistakes: collections.Counter[str] = collections.Counter()
        topic_commands: collections.Counter[str] = collections.Counter()
        topic_reminders: collections.Counter[str] = collections.Counter()

        for entry in topic_entries:
            topic_stuck.update(entry["stuck_points"])
            topic_mistakes.update(entry["mistakes"])
            topic_commands.update(normalize_command(item) for item in entry["commands"])
            topic_reminders.update(entry["reminders"])

        lines.extend(
            [
                "",
                f"## 主题：`{topic}`",
                "",
                f"- 练习数：{len(topic_entries)}",
                f"- 练习列表：{', '.join(entry['exercise'] for entry in topic_entries)}",
                "",
                "### 常见卡点",
                "",
                *top_counter_lines(topic_stuck, 6, "这个主题下暂时没有记录卡点"),
                "",
                "### 常见错误",
                "",
                *top_counter_lines(topic_mistakes, 6, "这个主题下暂时没有记录做错点"),
                "",
                "### 需要复习的命令/选项",
                "",
                *top_counter_lines(topic_commands, 6, "这个主题下暂时没有记录命令/选项"),
                "",
                "### 下次提醒",
                "",
                *top_counter_lines(topic_reminders, 6, "这个主题下暂时没有记录提醒"),
                "",
                "### 来源",
                "",
            ]
        )

        for entry in topic_entries:
            lines.append(f"- `{entry['exercise']}`: {entry['title']} ({entry['path']})")

    lines.extend(
        [
            "",
            "## 下一轮复习建议",
            "",
            "- 先看高频卡点和高频命令，再决定下一题练什么。",
            "- 如果某个主题重复出现 2 次以上的错误，优先针对这个主题再做一题专项练习。",
            "- 如果提醒区经常出现“输出格式”或“换行”相关内容，下次做题先手动比对样例输出。",
        ]
    )

    return "\n".join(lines) + "\n"


def build_json(entries: list[dict]) -> str:
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "exercise_count": len(entries),
        "entries": entries,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True, help="Workspace root containing archives/")
    parser.add_argument("--topic", help="Optional archive topic filter such as re or shell")
    args = parser.parse_args()

    workspace_root = pathlib.Path(args.workspace_root).resolve()
    archives_root = workspace_root / "archives"
    summaries_root = archives_root / "_summaries"
    summaries_root.mkdir(parents=True, exist_ok=True)

    topic_filter = args.topic.strip() if args.topic else None
    entries = collect_entries(archives_root, topic_filter)

    suffix = f"-{topic_filter}" if topic_filter else ""
    markdown_path = summaries_root / f"mistake-summary{suffix}.md"
    json_path = summaries_root / f"mistake-summary{suffix}.json"

    markdown_path.write_text(build_markdown(entries, topic_filter), encoding="utf-8", newline="\n")
    json_path.write_text(build_json(entries), encoding="utf-8", newline="\n")

    print(f"SUMMARY_FILE={markdown_path}")
    print(f"JSON_FILE={json_path}")
    print(f"NOTEBOOK_COUNT={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
