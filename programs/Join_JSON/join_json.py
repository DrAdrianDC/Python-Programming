"""
Join the `text` field of a JSON "part 2" file onto the `text` field of
its corresponding "part 1" file while keeping all other metadata from
part 1 unchanged. Designed for cases where a single PDF was split into
two JSON parts.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict


def load_json(path: Path) -> Dict[str, Any]:
    """Load a JSON file, exiting with a readable error on failure."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise SystemExit(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def strip_markdown_prefix(text: str) -> str:
    """
    Remove a leading markdown='…' / markdown="…" marker if present.
    Also trims a trailing matching quote if it exists.
    """
    lowered = text.lstrip()
    for prefix in ("markdown='", 'markdown="'):
        if lowered.startswith(prefix):
            stripped = lowered[len(prefix) :]
            if stripped.endswith(prefix[-1]):
                stripped = stripped[:-1]
            return stripped
    return text


def join_text(data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
    """
    Combine `text` fields, keeping the markdown prefix only from part 1.
    - Part 1: text is used as-is (keeps its leading markdown marker).
    - Part 2: text is stripped of any leading markdown marker.
    """
    text1 = data1.get("text") or ""
    text2 = strip_markdown_prefix(data2.get("text") or "")
    pieces = [part for part in (text1, text2) if part]
    return "\n\n".join(pieces)


def strip_debug_markers(text: str) -> str:
    """
    Remove debug_data_path markers that were embedded inside the text payload
    (e.g., \"'debug_data_path': 'debug_data/b-cell_Part2'}\"). These come from
    upstream extraction metadata and are not part of the content.
    """
    pattern = r",?\s*'debug_data_path': 'debug_data/[^']*'\}?"
    return re.sub(pattern, "", text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Join the text from part 2 into part 1 while keeping part 1 metadata."
        )
    )
    parser.add_argument(
        "--part1",
        default="b-cell_Part1.json",
        help="Path to the part 1 JSON file (metadata is taken from here).",
    )
    parser.add_argument(
        "--part2",
        default="b-cell_Part2.json",
        help="Path to the part 2 JSON file (only its text is appended).",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="b-cell_Combined.json",
        help="Where to write the combined JSON file.",
    )
    args = parser.parse_args()

    part1_path = Path(args.part1).expanduser()
    part2_path = Path(args.part2).expanduser()
    output_path = Path(args.output).expanduser()

    data1 = load_json(part1_path)
    data2 = load_json(part2_path)

    combined_data = dict(data1)  # keep all metadata/fields from part 1
    combined_data["text"] = strip_debug_markers(join_text(data1, data2))

    # Drop debug_data_path; not part of content/metadata needed downstream.
    combined_data.pop("debug_data_path", None)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f_out:
        json.dump(combined_data, f_out, indent=4, ensure_ascii=False)

    print(f"Combined content saved to {output_path}")


if __name__ == "__main__":
    main()