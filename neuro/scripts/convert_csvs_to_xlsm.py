#!/usr/bin/env python3
"""
Convert all CSV files under apps/tests/wais3/tabelas to .xlsm files
preserving the directory structure under neuro/tmp.

Usage: python neuro/scripts/convert_csvs_to_xlsm.py
"""
import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]  # repo root -> neuro/
SRC_DIR = ROOT / "apps" / "tests" / "wais3" / "tabelas"
DEST_BASE = ROOT / "tmp"


def convert_one(src_path: Path, dest_path: Path):
    # Read CSV with pandas and write to .xlsm using openpyxl engine.
    # Try a strict fast C-engine read first, fall back to python engine with
    # sep=None (auto-detect) and permissive bad-line handling.
    # Use dtype=str to avoid type inference surprises.
    try:
        df = pd.read_csv(src_path, dtype=str)
    except Exception:
        df = pd.read_csv(src_path, dtype=str, sep=None, engine='python', on_bad_lines='warn')
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    # Use engine openpyxl and save with .xlsm extension
    with pd.ExcelWriter(dest_path, engine="openpyxl") as w:
        # write dataframe to sheet named after file stem, truncated if too long
        sheet_name = src_path.stem[:31]
        df.to_excel(w, index=False, sheet_name=sheet_name)


def main():
    if not SRC_DIR.exists():
        print(f"Source directory not found: {SRC_DIR}")
        sys.exit(1)

    csv_files = list(SRC_DIR.rglob("*.csv"))
    if not csv_files:
        print("No CSV files found.")
        return

    for src in csv_files:
        rel = src.relative_to(SRC_DIR)
        dest = DEST_BASE / rel.with_suffix('.xlsm')
        try:
            convert_one(src, dest)
            print(f"Converted: {src} -> {dest}")
        except Exception as e:
            print(f"Failed: {src}: {e}")


if __name__ == '__main__':
    main()
