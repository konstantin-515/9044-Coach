#!/usr/bin/env python3
"""
Suggest the next practice track from recent workspace/archive metadata.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import dataclass


TRACK_RULES = {
    "file-directory": {
        "keywords": {
            "file",
            "files",
            "directory",
            "compare",
            "rename",
            "copy",
            "glob",
            "find",
            "mv",
            "cp",
            "image",
            "music",
            "tag",
            "jpg",
            "png",
        },
        "label": "file-directory",
    },
    "backup-snapshot": {
        "keywords": {"backup", "snapshot", "restore"},
        "label": "backup-snapshot",
    },
    "pipeline-text": {
        "keywords": {"pipeline", "table-processing", "sort", "uniq", "cut", "awk", "aggregation"},
        "label": "pipeline-text",
    },
    "regex-grep": {
        "keywords": {"regex", "grep", "re", "pattern", "filtering"},
        "label": "regex-grep",
    },
    "python-text": {
        "keywords": {"python", "dict", "set", "text-parsing", "counting"},
        "label": "python-text",
    },
    "shell-core": {
        "keywords": {"shell", "dash", "posix", "loop", "argument", "stdin", "stdout"},
        "label": "shell-core",
    },
}

SCENARIO_SUGGESTIONS = {
    "file-directory": [
        "批量改名或扩展名迁移",
        "两个目录的比较与差异汇总",
        "扫描文件树并处理带空格文件名",
        "按文件名规则筛选和复制文件",
    ],
    "backup-snapshot": [
        "隐藏编号备份文件",
        "目录快照保存与恢复",
        "忽略隐藏文件和工具脚本的快照题",
    ],
    "shell-core": [
        "参数驱动的小型自动化脚本",
        "stdin 过滤并格式化输出",
        "循环和条件判断结合的小程序",
    ],
    "pipeline-text": [
        "表格列提取和聚合",
        "分组计数与排序",
        "去重后再汇总",
    ],
    "regex-grep": [
        "日志过滤与锚定匹配",
        "源码扫描或 include 检查",
        "配置行校验",
    ],
    "python-text": [
        "文本归一化和计数",
        "保序去重",
        "提取数字后聚合",
    ],
}

CASE_MIX_SUGGESTIONS = {
    "file-directory": [
        "正常命中的文件",
        "不该被修改的文件",
        "带空格文件名",
        "目标已存在或命名冲突",
        "没有任何匹配文件",
    ],
    "backup-snapshot": [
        "第一次保存",
        "已有 .0 后继续编号",
        "恢复旧快照",
        "隐藏文件应忽略",
        "工具脚本本身不参与快照",
    ],
    "shell-core": [
        "正常输入",
        "参数不足或参数变化",
        "重复数据",
        "无匹配结果",
        "输出格式边界",
    ],
    "pipeline-text": [
        "正常聚合",
        "重复记录",
        "需要二级排序的并列情况",
        "应忽略的无效记录",
        "空结果或零结果",
    ],
    "regex-grep": [
        "正确匹配",
        "外观相似但不应匹配",
        "大小写陷阱",
        "额外标点或后缀陷阱",
        "完全无匹配",
    ],
    "python-text": [
        "正常统计",
        "重复和去重",
        "保序要求",
        "脏数据或空行",
        "并列排序",
    ],
}

SHELL_ROTATION_ORDER = [
    "file-directory",
    "backup-snapshot",
    "shell-core",
    "pipeline-text",
    "regex-grep",
]


@dataclass
class Entry:
    path: pathlib.Path
    track: str
    topic_hint: str
    topics: list[str]
    mtime: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--language", default="shell")
    parser.add_argument("--limit", type=int, default=6)
    return parser.parse_args()


def read_metadata(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def normalize_words(payload: dict) -> set[str]:
    words: set[str] = set()
    topic_hint = str(payload.get("topic_hint", "")).lower()
    title = str(payload.get("title", "")).lower()
    topics = payload.get("topics", [])
    words.update(part.strip() for part in topic_hint.replace("/", " ").replace("_", " ").split() if part.strip())
    words.update(part.strip() for part in title.replace("/", " ").replace("_", " ").replace("-", " ").split() if part.strip())
    if isinstance(topics, list):
        for item in topics:
            text = str(item).lower()
            words.update(part.strip() for part in text.replace("/", " ").replace("_", " ").replace("-", " ").split() if part.strip())
            words.add(text.strip())
    if "zid" in title or "学号" in title or "课程" in title or "学期" in title:
        words.add("regex")
        words.add("pipeline")
    return {word for word in words if word}


def classify_track(payload: dict) -> str:
    words = normalize_words(payload)
    for track_name in ("file-directory", "backup-snapshot", "pipeline-text", "regex-grep", "python-text", "shell-core"):
        rule = TRACK_RULES[track_name]
        if words & rule["keywords"]:
            return rule["label"]
    language = str(payload.get("language", "")).lower()
    if language == "python":
        return "python-text"
    return "shell-core"


def collect_entries(root: pathlib.Path) -> list[Entry]:
    entries: list[Entry] = []
    search_roots = [root / "exercises", root / "archives"]
    for base in search_roots:
        if not base.exists():
            continue
        for path in base.rglob("metadata.json"):
            payload = read_metadata(path)
            if not isinstance(payload, dict):
                continue
            entries.append(
                Entry(
                    path=path,
                    track=classify_track(payload),
                    topic_hint=str(payload.get("topic_hint", "")),
                    topics=[str(item) for item in payload.get("topics", [])] if isinstance(payload.get("topics", []), list) else [],
                    mtime=path.stat().st_mtime,
                )
            )
    entries.sort(key=lambda item: item.mtime, reverse=True)
    return entries


def recommend_shell_track(entries: list[Entry]) -> tuple[str, str]:
    recent_tracks = [entry.track for entry in entries[:4]]
    counts = {track: recent_tracks.count(track) for track in SHELL_ROTATION_ORDER}
    banned = set(recent_tracks[:2])
    for track in SHELL_ROTATION_ORDER:
        if track in banned:
            continue
        if counts.get(track, 0) == 0:
            return track, f"recent tracks are {recent_tracks or ['none']}; prefer an underused shell track"
    for track in SHELL_ROTATION_ORDER:
        if track not in banned:
            return track, f"recent tracks are {recent_tracks or ['none']}; avoid repeating the last two tracks"
    return "file-directory", "fallback to file-directory to avoid another regex/pipeline style question"


def main() -> int:
    args = parse_args()
    root = pathlib.Path(args.workspace_root).resolve()
    entries = collect_entries(root)
    recent = entries[: args.limit]
    if args.language.lower() == "shell":
        recommended_track, reason = recommend_shell_track(recent)
    else:
        recommended_track, reason = ("python-text", "non-shell request defaults to python-text rotation")

    result = {
        "workspace_root": str(root),
        "language": args.language,
        "recommended_track": recommended_track,
        "reason": reason,
        "strict_rotation": recommended_track in {"file-directory", "backup-snapshot"},
        "avoid_story_families": [
            "student records",
            "zid extraction",
            "course code / term parsing",
        ] if recommended_track in {"file-directory", "backup-snapshot", "shell-core"} else [],
        "suggested_scenarios": SCENARIO_SUGGESTIONS.get(recommended_track, []),
        "suggested_case_mix": CASE_MIX_SUGGESTIONS.get(recommended_track, []),
        "recent_entries": [
            {
                "path": str(entry.path),
                "track": entry.track,
                "topic_hint": entry.topic_hint,
                "topics": entry.topics,
            }
            for entry in recent
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
