
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[1]
curated_path = BASE / "data" / "processed" / "entities_curated.csv"
quality_path = BASE / "data" / "processed" / "quality_metrics.csv"

def compute_quality():
    df = pd.read_csv(curated_path)

    total = len(df)
    completeness = round(100 * (df["legal_name"] != "").sum() / total, 2) if total else 0.0
    linkage_quality = round(100 * (df["lei"].notna() & (df["lei"] != "")).sum() / total, 2) if total else 0.0

    # Freshness: max age in days based on ingestion_ts
    def age_days(ts):
        try:
            dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
            return (datetime.now(timezone.utc) - dt).days
        except Exception:
            return None
    ages = df["ingestion_ts"].apply(age_days).dropna()
    freshness_max_age_days = int(ages.max()) if len(ages) else None

    metrics = pd.DataFrame([{
        "metric_ts": datetime.now(timezone.utc).isoformat(),
        "records_total": total,
        "completeness_pct": completeness,
        "linkage_quality_pct": linkage_quality,
        "freshness_max_age_days": freshness_max_age_days
    }])
    metrics.to_csv(quality_path, index=False)
    print(f"Wrote quality metrics to {quality_path}")
    print(metrics.to_string(index=False))

if __name__ == "__main__":
    compute_quality()
