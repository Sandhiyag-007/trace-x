from data_loader import load_data
from anomaly_detection import detect_anomalies
from graph_analysis import build_transaction_graph, detect_fan_out, detect_fan_in, detect_layering
from rapid_movement import detect_rapid_movement
from risk_engine import calculate_risk
from confidence import calculate_confidence
from alert_ranking import rank_alerts
from investigation_summary import generate_summary

df = load_data("data/raw/bitcoin_transactions.csv")
df = detect_anomalies(df)

graph = build_transaction_graph(df)

fan_out = detect_fan_out(graph)
fan_in = detect_fan_in(graph)
layering = detect_layering(graph)
rapid = detect_rapid_movement(df)

fanout_wallets = {x["wallet"] for x in fan_out}
fanin_wallets = {x["wallet"] for x in fan_in}
layering_wallets = {x["wallet"] for x in layering}
rapid_wallets = {x["wallet"] for x in rapid}

alerts = []

for _, row in df.iterrows():
    wallet = row["input_address"]

    is_fanout = wallet in fanout_wallets
    is_fanin = wallet in fanin_wallets
    is_layering = wallet in layering_wallets
    is_rapid = wallet in rapid_wallets

    score, level, reasons = calculate_risk(
        row["anomaly"],
        is_fanout,
        is_fanin,
        is_rapid,
        is_layering
    )

    confidence, reliability = calculate_confidence(
        row["anomaly"],
        is_fanout,
        is_fanin,
        is_rapid,
        is_layering
    )

    alerts.append({
        "txid": row["txid"],
        "wallet": wallet,
        "risk": score,
        "level": level,
        "confidence": confidence,
        "reliability": reliability,
        "reasons": reasons
    })

ranked_alerts = rank_alerts(alerts)

print("\n========== TRACE-X INVESTIGATIVE ALERTS ==========")

for alert in ranked_alerts:
    summary = generate_summary(alert)

    print("\nTXID:", summary["txid"])
    print("Wallet:", summary["wallet"])
    print("Risk:", summary["risk_score"], "/ 100")
    print("Level:", summary["risk_level"])
    print("Confidence:", summary["confidence"], "%")
    print("Reliability:", summary["reliability"])
    print("Patterns:", ", ".join(summary["suspicious_patterns"]) if summary["suspicious_patterns"] else "None")
    print("Recommended Action:", summary["recommended_action"])
