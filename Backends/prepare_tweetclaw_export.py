"""Convert TweetClaw tweet exports into this project's CSV schema."""

from __future__ import annotations

import argparse
import csv
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any


OUTPUT_COLUMNS = ("Date", "user_name", "user_friends", "user_location", "text")

FIELD_ALIASES = {
    "Date": (
        "date",
        "created_at",
        "createdAt",
        "timestamp",
        "time",
        "published_at",
    ),
    "user_name": (
        "user_name",
        "username",
        "screen_name",
        "author_username",
        "author_name",
        "name",
    ),
    "user_friends": (
        "user_friends",
        "friends_count",
        "following_count",
        "user_following_count",
        "author_following_count",
    ),
    "user_location": (
        "user_location",
        "location",
        "author_location",
    ),
    "text": (
        "text",
        "full_text",
        "tweet_text",
        "content",
        "body",
    ),
}

NESTED_ALIASES = {
    "user_name": (
        ("user", "name"),
        ("user", "username"),
        ("user", "screen_name"),
        ("author", "name"),
        ("author", "username"),
        ("author", "screen_name"),
    ),
    "user_friends": (
        ("user", "friends_count"),
        ("user", "following_count"),
        ("author", "friends_count"),
        ("author", "following_count"),
    ),
    "user_location": (
        ("user", "location"),
        ("author", "location"),
    ),
}


def read_input(path: Path) -> list[Mapping[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as source:
            return list(csv.DictReader(source))

    text = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]

    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, Mapping)]

    if isinstance(parsed, Mapping):
        for key in ("tweets", "data", "items", "results"):
            value = parsed.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, Mapping)]
        return [parsed]

    return []


def first_present(record: Mapping[str, Any], aliases: Iterable[str]) -> Any:
    for alias in aliases:
        if alias in record and record[alias] not in (None, ""):
            return record[alias]
    return ""


def nested_present(record: Mapping[str, Any], aliases: Iterable[Sequence[str]]) -> Any:
    for path in aliases:
        current: Any = record
        for key in path:
            if not isinstance(current, Mapping) or key not in current:
                current = ""
                break
            current = current[key]
        if current not in (None, ""):
            return current
    return ""


def normalize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def normalize_record(record: Mapping[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for column in OUTPUT_COLUMNS:
        value = first_present(record, FIELD_ALIASES[column])
        if not value:
            value = nested_present(record, NESTED_ALIASES.get(column, ()))
        normalized[column] = normalize_value(value)
    return normalized


def write_output(records: Iterable[Mapping[str, Any]], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for record in records:
            row = normalize_record(record)
            if not row["text"]:
                continue
            writer.writerow(row)
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert TweetClaw JSON, JSONL, or CSV exports for this sentiment pipeline.",
    )
    parser.add_argument("input", type=Path, help="TweetClaw export file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("ChatGPT tweets.csv"),
        help="CSV path consumed by Backends/main.py and Backends/analyze_all.py.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_input(args.input)
    count = write_output(records, args.output)
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
