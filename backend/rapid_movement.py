import pandas as pd

def detect_rapid_movement(df, minutes=5):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    suspicious = []

    for wallet, group in df.groupby("input_address"):
        group = group.sort_values("timestamp")

        for i in range(1, len(group)):
            gap = (group.iloc[i]["timestamp"] - group.iloc[i-1]["timestamp"]).total_seconds() / 60

            if gap <= minutes:
                suspicious.append({
                    "wallet": wallet,
                    "txid": group.iloc[i]["txid"],
                    "time_gap_minutes": gap,
                    "pattern": "Rapid Movement"
                })

    return suspicious

