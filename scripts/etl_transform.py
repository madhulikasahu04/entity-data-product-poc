
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]

raw_path = BASE / "data" / "raw" / "entities.csv"
curated_path = BASE / "data" / "processed" / "entities_curated.csv"
lineage_path = BASE / "data" / "processed" / "lineage.csv"

def transform():
    df = pd.read_csv(raw_path)
    # Simple cleanup: standardise names, drop duplicates, trim spaces
    df["legal_name"] = df["legal_name"].fillna("").str.strip()
    df["country"] = df["country"].fillna("").str.upper().str.strip()
    df = df.drop_duplicates(subset=["entity_id"])

    # Business rules (examples):
    # - flag records missing critical fields
    df["critical_missing"] = ((df["entity_id"].isna()) | (df["legal_name"] == "")).astype(int)

    # - derive region
    df["region"] = df["country"].map({"GB":"EMEA", "IE":"EMEA"}).fillna("UNKNOWN")

    # Write curated
    curated = df.copy()
    curated.to_csv(curated_path, index=False)

    # Write lineage (very simplified)
    now = datetime.utcnow().isoformat() + "Z"
    lineage_rows = []
    for _, row in df.iterrows():
        lineage_rows.append({
            "entity_id": row["entity_id"],
            "source": "data/raw/entities.csv",
            "transform": "standardise+derive_region+flag_critical_missing",
            "target": "data/processed/entities_curated.csv",
            "run_ts": now
        })
    lineage_df = pd.DataFrame(lineage_rows)
    lineage_df.to_csv(lineage_path, index=False)

if __name__ == "__main__":
    transform()
    print(f"Wrote curated to {curated_path}")
    print(f"Wrote lineage to {lineage_path}")
