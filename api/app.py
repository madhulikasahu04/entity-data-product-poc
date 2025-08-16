
from flask import Flask, jsonify
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
lineage_path = BASE / "data" / "processed" / "lineage.csv"
quality_path = BASE / "data" / "processed" / "quality_metrics.csv"

app = Flask(__name__)

@app.get("/lineage")
def lineage():
    try:
        df = pd.read_csv(lineage_path)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/quality")
def quality():
    try:
        df = pd.read_csv(quality_path)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
