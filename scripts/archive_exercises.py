#!/usr/bin/env python3
"""
Archive completed exercise folders into topic-based archive directories.

Examples:
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01-03
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01,test03-05
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01-03 --topic re
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys


TOPIC_PATTERNS = {
    "re": [
        r"\bregex\b",
        r"\bregular expression\b",
        r"\bpython re\b",
        r"\bre\.findall\b",
        r"\b正则\b",
    ],
    "grep": [
        r"\bgrep\b",
        r"\bgrep -e\b",
        r"\bgrep -o\b",
        r"\bgrep -v\b",
        r"\b模式匹配\b",
    ],
    "sed": [
        r"\bsed\b",
        r"\bstream editor\b",
    ],
    "awk": [
        r"\bawk\b",
    ],
    "pipeline": [
        r"\bpipeline\b",
        r"\bsort\b",
        r"\buniq\b",
        r"\bcut\b",
        r"\btr\b",
        r"\b列提取\b",
        r"\b去重\b",
        r"\b排序\b",
        r"\b统计\b",
    ],
    "shell": [
        r"\bdash\b",
        r"\bposix shell\b",
        r"\bshell\b",
        r"\bstdin\b",
        r"\bstdout\b",
        r"\b重定向\b",
        r"\b命令替换\b",
    ],
    "files": [
        r"\bdirectory\b",
        r"\brename\b",
        r"\bbackup\b",
        r"\bsnapshot\b",
        r"\bfind\b",
        r"\bcmp\b",
        r"\bdiff\b",
        r"\bglob\b",
        r"\b文件\b",
        r"\b目录\b",
        r"\b重命名\b",
        r"\b备份\b",
    ],
    "git": [
        r"\bgit\b",
        r"\bbranch\b",
        r"\bcommit\b",
        r"\bmerge request\b",
        r"\bissue\b",
        r"\blicense\b",
    ],
    "python": [
        r"\bpython\b",
        r"\bsys\.argv\b",
        r"\bdict\b",
        r"\bset\b",
        r"\b集合\b",
        r"\b字典\b",
    ],
}


def slugify_topic(raw: str) -> str:
    topic = raw.strip().lower()
    topic = re.sub(r"[^a-z0-9_-]+", "-", topic)
    topic = re.sub(r"-{2,}", "-", topic).strip("-")
    return topic or "misc"


def parse_spec(spec: str) -> list[str]:
    names: list[str] = []
    for chunk in [part.strip() for part in spec.split(",") if part.strip()]:
        match = re.fullmatch(r"test(\d+)-(\d+)", chunk)
        if match:
            start = int(match.group(1))
            end = int(match.group(2))
            if end < start:
                start, end = end, start
            for number in range(start, end + 1):
                names.append(f"test{number:02d}")
            continue
        match = re.fullmatch(r"test(\d+)", chunk)
        if match:
            names.append(f"test{int(match.group(1)):02d}")
            continue
        raise ValueError(f"unsupported exercise spec: {chunk}")
    deduped: list[str] = []
    seen: set[str] = set()
    for name in names:
        if name not in seen:
            seen.add(name)
            deduped.append(name)
    return deduped


def read_text_if_exists(path: pathlib.Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def read_metadata(path: pathlib.Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def infer_topic(folder: pathlib.Path) -> tuple[str, int, list[str]]:
    metadata = read_metadata(folder / "metadata.json")
    topic_hint = slugify_topic(str(metadata.get("topic_hint", "")).strip())
    if topic_hint and topic_hint != "misc":
        return topic_hint, 100, ["metadata topic_hint"]

    text_parts = [
        read_text_if_exists(folder / "README.md"),
        read_text_if_exists(folder / "notebook.md"),
        json.dumps(metadata, ensure_ascii=False),
    ]
    text = "\n".join(text_parts).lower()

    scores = {topic: 0 for topic in TOPIC_PATTERNS}
    reasons: list[str] = []

    if (folder / "solution.py").exists():
        scores["python"] += 2
        reasons.append("found solution.py")
    if (folder / "solution.sh").exists():
        scores["shell"] += 1
        reasons.append("found solution.sh")

    for topic, patterns in TOPIC_PATTERNS.items():
        for pattern in patterns:
            hits = len(re.findall(pattern, text))
            if hits:
                scores[topic] += hits

    best_topic = max(scores, key=scores.get)
    best_score = scores[best_topic]
    if best_score < 2:
        return "misc", best_score, reasons
    return best_topic, best_score, reasons


def archive_one(workspace_root: pathlib.Path, name: str, explicit_topic: str | None) -> tuple[bool, str]:
    source = workspace_root / "exercises" / name
    if not source.exists():
        return False, f"SKIP {name}: source folder not found"
    if not source.is_dir():
        return False, f"SKIP {name}: source exists but is not a directory"

    if explicit_topic:
        topic = slugify_topic(explicit_topic)
        score = -1
    else:
        topic, score, _ = infer_topic(source)

    archive_root = workspace_root / "archives" / topic
    archive_root.mkdir(parents=True, exist_ok=True)
    destination = archive_root / name
    if destination.exists():
        return False, f"SKIP {name}: destination already exists at {destination}"

    shutil.move(str(source), str(destination))
    if explicit_topic:
        return True, f"MOVED {name} -> archives/{topic}/{name} (topic set explicitly)"
    return True, f"MOVED {name} -> archives/{topic}/{name} (auto topic, score={score})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True, help="Workspace root containing exercises/ and archives/")
    parser.add_argument("--spec", required=True, help="Exercise selector such as test01 or test01-03")
    parser.add_argument("--topic", help="Optional topic override such as re, shell, python")
    args = parser.parse_args()

    workspace_root = pathlib.Path(args.workspace_root).resolve()
    if not workspace_root.exists():
        print(f"ERROR: workspace root not found: {workspace_root}", file=sys.stderr)
        return 2

    try:
        names = parse_spec(args.spec)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if not names:
        print("ERROR: no exercises resolved from spec", file=sys.stderr)
        return 2

    moved = 0
    for name in names:
        ok, message = archive_one(workspace_root, name, args.topic)
        print(message)
        if ok:
            moved += 1

    print(f"ARCHIVE_RESULT: moved {moved}/{len(names)} exercise(s)")
    return 0 if moved == len(names) else 1


if __name__ == "__main__":
    raise SystemExit(main())
