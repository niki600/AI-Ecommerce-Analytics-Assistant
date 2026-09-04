import pandas as pd
from pathlib import Path

# Project ke data folder ka path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Saari CSV files find karo
csv_files = list(DATA_DIR.glob("*.csv"))

print("=" * 60)
print("E-COMMERCE DATASET PROFILING")
print("=" * 60)

for file in csv_files:

    print(f"\n{'=' * 60}")
    print(f"TABLE: {file.name}")
    print(f"{'=' * 60}")

    # CSV read
    df = pd.read_csv(file)

    # Basic information
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

print("\n" + "=" * 60)
print("PROFILING COMPLETED")
print("=" * 60)