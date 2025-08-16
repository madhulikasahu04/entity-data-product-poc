
import streamlit as st
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
lineage_path = BASE / "data" / "processed" / "lineage.csv"
quality_path = BASE / "data" / "processed" / "quality_metrics.csv"
curated_path = BASE / "data" / "processed" / "entities_curated.csv"

st.title("Entity Data Product – Lineage & Quality Dashboard (PoC)")

st.header("Quality Metrics")
if quality_path.exists():
    q = pd.read_csv(quality_path)
    st.dataframe(q)
else:
    st.info("Run scripts/etl_transform.py and scripts/compute_quality.py first.")

st.header("Lineage Records")
if lineage_path.exists():
    l = pd.read_csv(lineage_path)
    st.dataframe(l.head(100))
else:
    st.info("No lineage file found yet.")

st.header("Curated Entities (Sample)")
if curated_path.exists():
    c = pd.read_csv(curated_path)
    st.dataframe(c.head(50))
else:
    st.info("No curated entities found yet.")
