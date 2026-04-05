#!/usr/bin/env python3
"""
Archive completed exercise folders into topic-based archive directories.

This script uses a safer two-phase archive flow:

1. Copy relevant files into `archives/<topic>/testNN`
2. Verify the archive copy matches the source tree for relevant entries
3. Delete the source directory

If step 3 fails because of permissions or locked files, the script reports a
verified copy plus a cleanup failure instead of leaving a traceback as the main
result.

Examples:
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01-03
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01,test03-05
    python archive_exercises.py --workspace-root F:\\Codex\\9044 --spec test01-03 --topic re
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import shutil
import sys


IGNORE_DIR_NAMES = {".artifacts", "__pycache__"}
IGNORE_FILE_SUFFIXES = {".pyc", ".pyo"}

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


def write_metadata(path: pathlib.Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def should_ignore_relative(relative: pathlib.Path) -> bool:
    if any(part in IGNORE_DIR_NAMES for part in relative.parts):
        return True
    if relative.name in IGNORE_DIR_NAMES:
        return True
    return relative.suffix.lower() in IGNORE_FILE_SUFFIXES


def ignore_for_copy(source_root: pathlib.Path):
    def _ignore(current_dir: str, names: list[str]) -> list[str]:
        ignored: list[str] = []
        current = pathlib.Path(current_dir)
        for name in names:
            try:
                relative = (current / name).relative_to(source_root)
            except ValueError:
                relative = pathlib.Path(name)
            if should_ignore_relative(relative):
                ignored.append(name)
        return ignored

    return _ignore


def collect_relative_entries(root: pathlib.Path) -> set[str]:
    entries: set[str] = set()
    if not root.exists():
        return entries
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if should_ignore_relative(relative):
            continue
        entries.add(relative.as_posix())
    return entries


def verify_copy(source: pathlib.Path, destination: pathlib.Path) -> dict:
    source_entries = collect_relative_entries(source)
    destination_entries = collect_relative_entries(destination)
    missing = sorted(source_entries - destination_entries)
    extra = sorted(destination_entries - source_entries)
    return {
        "ok": not missing and not extra,
        "source_count": len(source_entries),
        "destination_count": len(destination_entries),
        "missing": missing,
        "extra": extra,
    }


def preview_items(items: list[str], limit: int = 5) -> str:
    if not items:
        return "-"
    head = items[:limit]
    text = ", ".join(head)
    if len(items) > limit:
        text += f", ... (+{len(items) - limit} more)"
    return text


def remove_ignored_paths(source: pathlib.Path) -> None:
    ignored_paths: list[pathlib.Path] = []
    for path in source.rglob("*"):
        if should_ignore_relative(path.relative_to(source)):
            ignored_paths.append(path)
    for path in sorted(ignored_paths, key=lambda item: len(item.relative_to(source).parts), reverse=True):
        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        except OSError:
            continue


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


def sync_copy(source: pathlib.Path, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        str(source),
        str(destination),
        dirs_exist_ok=True,
        ignore=ignore_for_copy(source),
    )


def archive_one(workspace_root: pathlib.Path, name: str, explicit_topic: str | None) -> tuple[str, str]:
    source = workspace_root / "exercises" / name
    if not source.exists():
        return "SKIP", f"SKIP {name}: source folder not found"
    if not source.is_dir():
        return "SKIP", f"SKIP {name}: source exists but is not a directory"

    if explicit_topic:
        topic = slugify_topic(explicit_topic)
        score = -1
        topic_note = "topic set explicitly"
    else:
        topic, score, _ = infer_topic(source)
        topic_note = f"auto topic, score={score}"

    archive_root = workspace_root / "archives" / topic
    archive_root.mkdir(parents=True, exist_ok=True)
    destination = archive_root / name
    if destination.exists() and not destination.is_dir():
        return "SKIP", f"SKIP {name}: destination exists but is not a directory at {destination}"

    destination_preexisted = destination.exists()

    try:
        sync_copy(source, destination)
    except OSError as error:
        return "COPY_FAILED", f"COPY_FAILED {name} -> archives/{topic}/{name} ({topic_note}): {error}"

    verification = verify_copy(source, destination)
    if not verification["ok"]:
        return (
            "VERIFY_FAILED",
            "VERIFY_FAILED "
            f"{name} -> archives/{topic}/{name} ({topic_note}): "
            f"src={verification['source_count']} dst={verification['destination_count']} "
            f"missing=[{preview_items(verification['missing'])}] "
            f"extra=[{preview_items(verification['extra'])}]",
        )

    metadata_path = destination / "metadata.json"
    metadata = read_metadata(metadata_path)
    metadata["status"] = "archived"
    metadata["topic_hint"] = topic
    metadata["archived_at"] = dt.datetime.now().isoformat(timespec="seconds")
    metadata["archived_from"] = str(source)
    write_metadata(metadata_path, metadata)

    try:
        remove_ignored_paths(source)
        shutil.rmtree(source)
    except OSError as error:
        return (
            "CLEANUP_FAILED",
            "COPIED_OK CLEANUP_FAILED "
            f"{name} -> archives/{topic}/{name} ({topic_note}; verified={verification['source_count']}; "
            f"destination_preexisted={destination_preexisted}): "
            f"archive copy is complete but deleting the source folder failed: {error}. "
            "Request escalated cleanup.",
        )

    action = "ARCHIVED" if not destination_preexisted else "ARCHIVED_RESUMED"
    return (
        "ARCHIVED",
        f"{action} {name} -> archives/{topic}/{name} ({topic_note}; verified={verification['source_count']})",
    )


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

    archived = 0
    cleanup_failed = 0
    failed = 0

    for name in names:
        status, message = archive_one(workspace_root, name, args.topic)
        print(message)
        if status == "ARCHIVED":
            archived += 1
        elif status == "CLEANUP_FAILED":
            cleanup_failed += 1
        else:
            failed += 1

    print(
        "ARCHIVE_RESULT: "
        f"archived {archived}/{len(names)} exercise(s); "
        f"cleanup_failed={cleanup_failed}; "
        f"other_failures={failed}"
    )
    return 0 if archived == len(names) else 1


if __name__ == "__main__":
    raise SystemExit(main())
