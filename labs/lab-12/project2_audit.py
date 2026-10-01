"""Mechanical Project 2 package audit script.

Author: Oladapo Olaniyan
Course: FIN 43900 - AI Finance Applications
Purdue University · Fall 2026
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


REQUIRED_COLUMNS = {
    "item",
    "required",
    "location_or_url",
    "title",
    "duration_or_as_of",
    "timestamp_index",
    "access_checked",
    "frozen_or_commit_id",
    "notes",
}
VIDEO_ITEMS = {"Video 1", "Video 2", "Video 3"}


def load(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path, keep_default_na=False)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if len(frame) != 12:
        raise ValueError(f"Expected 12 manifest rows; received {len(frame)}")
    return frame


def gaps(frame: pd.DataFrame) -> list[str]:
    missing_items: list[str] = []
    for row in frame.to_dict(orient="records"):
        if row["required"].lower() != "yes":
            continue
        base_ready = all(
            str(row[field]).strip() != ""
            for field in ("location_or_url", "access_checked", "frozen_or_commit_id")
        )
        video_ready = row["item"] not in VIDEO_ITEMS or all(
            str(row[field]).strip() != ""
            for field in ("title", "duration_or_as_of", "timestamp_index")
        )
        if not (base_ready and video_ready):
            missing_items.append(row["item"])
    return missing_items


def score_project(frame: pd.DataFrame) -> None:
    raise NotImplementedError("Completeness cannot establish finance quality or authorship")


def main() -> None:
    manifest_path = Path(__file__).with_name("project2_manifest_template.csv")
    print("=" * 70)
    print("FIN 43900 — PROJECT 2 MECHANICAL PACKAGE AUDIT")
    print(f"Student / Author: Oladapo Olaniyan")
    print(f"Target Manifest: {manifest_path.resolve()}")
    print("=" * 70)

    if not manifest_path.exists():
        print(f"ERROR: Manifest file not found at {manifest_path}")
        sys.exit(1)

    frame = load(manifest_path)
    missing = gaps(frame)

    print(f"Manifest Rows Inspected: {len(frame)}")
    print(f"Required Items Check:")

    if missing:
        print(f"\n[!] INCOMPLETE MANIFEST ({len(missing)} unresolved required items):")
        for item in missing:
            print(f"  - {item}")
        print("\nAction Required: Populate location/URL, access checks, frozen commit IDs, and video timestamps.")
    else:
        print("\n[✓] ALL 11 REQUIRED MANIFEST ITEMS ARE FULLY POPULATED AND VALIDATED!")

    print("=" * 70)


if __name__ == "__main__":
    main()
