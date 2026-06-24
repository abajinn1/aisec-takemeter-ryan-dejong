import argparse
import csv
import sys
from pathlib import Path

REQUIRED_COLUMNS = ["text", "label", "source", "source_url", "notes"]

ALLOWED_LABELS = {
    "concept_definition",
    "tool_or_control",
    "attack_or_testing_tactic",
    "low_signal_or_general",
}


def validate_dataset(csv_path, required_columns=None, allowed_labels=None):
    required_columns = required_columns or REQUIRED_COLUMNS
    allowed_labels = allowed_labels or ALLOWED_LABELS

    path = Path(csv_path)
    problems = []

    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 1

    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except UnicodeDecodeError:
        print(f"ERROR: Could not read {path}. File is not valid UTF-8.")
        return 1
    except csv.Error as e:
        print(f"ERROR: CSV parsing failed for {path}: {e}")
        return 1
    except OSError as e:
        print(f"ERROR: Could not open {path}: {e}")
        return 1

    columns = reader.fieldnames or []

    if columns != required_columns:
        problems.append(
            f"Columns do not match expected schema.\n"
            f"Expected: {required_columns}\n"
            f"Found:    {columns}"
        )

    seen_text = set()
    label_counts = {label: 0 for label in sorted(allowed_labels)}

    for row_number, row in enumerate(rows, start=2):
        text = (row.get("text") or "").strip()
        label = (row.get("label") or "").strip()
        source = (row.get("source") or "").strip()
        source_url = (row.get("source_url") or "").strip()
        notes = (row.get("notes") or "").strip()

        if not text:
            problems.append(f"Row {row_number}: missing text.")
        elif len(text.split()) < 5:
            problems.append(f"Row {row_number}: text is very short: {text}")

        if label not in allowed_labels:
            problems.append(f"Row {row_number}: invalid label: {label}")
        else:
            label_counts[label] += 1

        if not source:
            problems.append(f"Row {row_number}: missing source.")

        if not source_url:
            problems.append(f"Row {row_number}: missing source_url.")
        elif not source_url.startswith("https://www.reddit.com/"):
            problems.append(f"Row {row_number}: source_url is not a Reddit URL: {source_url}")

        if not notes:
            problems.append(f"Row {row_number}: missing notes.")

        normalized_text = " ".join(text.lower().split())
        if normalized_text in seen_text:
            problems.append(f"Row {row_number}: duplicate text.")
        else:
            seen_text.add(normalized_text)

    print("Dataset validation report")
    print("=" * 30)
    print(f"File: {path}")
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {columns}")
    print()

    print("Label distribution:")
    for label, count in sorted(label_counts.items()):
        print(f"- {label}: {count}")

    print()
    print("Problems found:")
    if problems:
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("No technical problems found.")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate the TakeMeter labeled dataset before training."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="data/labeled_examples.csv",
        help="Path to the CSV dataset. Defaults to data/labeled_examples.csv.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    exit_code = validate_dataset(args.csv_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()