"""Summarize missing values in a comma-delimited CSV file."""

import argparse
import csv
from pathlib import Path


def profile(source):
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        headers = next(reader, None)
        if not headers:
            raise ValueError("Expected a CSV header row.")

        missing = [0] * len(headers)
        rows = 0
        for row in reader:
            if not row:
                continue
            if len(row) != len(headers):
                raise ValueError(
                    f"Row ending on line {reader.line_num} has {len(row)} fields; "
                    f"expected {len(headers)}."
                )
            rows += 1
            for index, value in enumerate(row):
                missing[index] += not value.strip()

    return headers, rows, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="UTF-8 CSV with a header row")
    parser.add_argument("report", type=Path, help="New CSV report path")
    args = parser.parse_args()

    try:
        headers, rows, missing = profile(args.source)
        with args.report.open("x", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["Column", "Rows", "Missing", "Populated"])
            for index, (header, count) in enumerate(zip(headers, missing), start=1):
                writer.writerow([f"Column {index}: {header}", rows, count, rows - count])
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
