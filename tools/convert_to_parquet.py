# tools/convert_to_parquet.py
import pandas as pd
from pathlib import Path

pairs = [
    ("data/raw/RAW_recipes.csv", "RAW_recipes.parquet"),
    ("data/raw/RAW_interactions.csv", "RAW_interactions.parquet"),
    ("data/processed/recipes_cleaned.csv", "recipes_cleaned.parquet"),
    ("data/processed/interactions_cleaned.csv", "interactions_cleaned.parquet"),
    ("data/processed/merged_cleaned.csv", "merged_cleaned.parquet"),
]

for src, dst in pairs:
    p = Path(src)
    if not p.exists():
        print(f"⚠️ Skip (missing): {src}")
        continue

    print(f"Converting {src} -> {dst} ...")
    # lecture robuste des gros CSV
    df = pd.read_csv(p, low_memory=False, on_bad_lines="skip")
    df.to_parquet(p.with_name(dst), index=False, engine="pyarrow")
    print(f"✅ Done: {dst}")

print("✨ All conversions completed.")
