import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    features = df[["input_amount", "output_amount", "fee"]]

    model = IsolationForest(contamination=0.25, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    df["status"] = df["anomaly"].map({1: "Normal", -1: "Suspicious"})

    return df
