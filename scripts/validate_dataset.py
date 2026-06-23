import csv
from collections import Counter

DATASET_PATH = "data/labeled_examples.csv"

REQUIRED_COLUMNS = ["text", "label", "source", "source_url", "notes"]

ALLOWED_LABELS = {
    "concept_definition",
    "tool_or_control",
    "attack_or_testing_tactic",
    "low_signal_or_general",
}


def main():
    with open(DATASET_PATH, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames

    print("Dataset validation report")
    print("=" * 30)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {columns}")

    labels = Counter((row.get("label") or "").strip() for row in rows)

    print("\nLabel distribution:")
    for label in sorted(ALLOWED_LABELS):
        print(f"- {label}: {labels.get(label, 0)}")

    print("\nProblems found:")
    problems = 0

    if columns != REQUIRED_COLUMNS:
        print(f"- Column mismatch. Expected {REQUIRED_COLUMNS}, got {columns}")
        problems += 1

    seen_texts = set()

    for line_number, row in enumerate(rows, start=2):
        extra_values = row.get(None)
        if extra_values:
            print(f"- Line {line_number}: extra CSV values found: {extra_values}")
            problems += 1

        text = (row.get("text") or "").strip()
        label = (row.get("label") or "").strip()
        source = (row.get("source") or "").strip()
        source_url = (row.get("source_url") or "").strip()
        notes = (row.get("notes") or "").strip()

        if not text:
            print(f"- Line {line_number}: missing text")
            problems += 1

        if label not in ALLOWED_LABELS:
            print(f"- Line {line_number}: invalid label: {label}")
            problems += 1

        if not source:
            print(f"- Line {line_number}: missing source")
            problems += 1

        if not source_url:
            print(f"- Line {line_number}: missing source_url")
            problems += 1
        elif not source_url.startswith("https://www.reddit.com/"):
            print(f"- Line {line_number}: source_url does not look like a Reddit URL: {source_url}")
            problems += 1

        if not notes:
            print(f"- Line {line_number}: missing notes")
            problems += 1

        if text and len(text.split()) < 5:
            print(f"- Line {line_number}: text may be too short: {text}")
            problems += 1

        normalized_text = text.lower()
        if normalized_text in seen_texts:
            print(f"- Line {line_number}: duplicate text found")
            problems += 1
        else:
            seen_texts.add(normalized_text)

    if problems == 0:
        print("No technical problems found.")
    else:
        print(f"{problems} possible problem(s) found.")


if __name__ == "__main__":
    main()