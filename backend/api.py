from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os

from anomaly_detection import detect_anomalies
from graph_analysis import (
    build_transaction_graph,
    detect_fan_out,
    detect_fan_in,
    detect_layering
)
from rapid_movement import detect_rapid_movement
from risk_engine import calculate_risk
from confidence import calculate_confidence
from alert_ranking import rank_alerts
from investigation_summary import generate_summary

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_analysis():
    data_file = os.path.join(
        BASE_DIR, "data", "raw", "bitcoin_transactions.csv"
    )

    df = pd.read_csv(data_file)
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

        alert = {
            "txid": row["txid"],
            "wallet": wallet,
            "src_ip": row["src_ip"],
            "dst_ip": row["dst_ip"],
            "amount": row["output_amount"],
            "fee": row["fee"],
            "risk": score,
            "level": level,
            "confidence": confidence,
            "reliability": reliability,
            "reasons": reasons
        }

        alerts.append(alert)

    return rank_alerts(alerts)


@app.route("/")
def home():
    return jsonify({
        "system": "TRACE-X",
        "status": "Operational",
        "mode": "Offline"
    })


@app.route("/dashboard")
def dashboard():
    return send_from_directory(
        os.path.join(BASE_DIR, "frontend"),
        "index.html"
    )


@app.route("/transactions")
def transactions():
    data_file = os.path.join(
        BASE_DIR, "data", "raw", "bitcoin_transactions.csv"
    )

    df = pd.read_csv(data_file)
    return jsonify(df.to_dict(orient="records"))


@app.route("/alerts")
def alerts():
    return jsonify(run_analysis())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

@app.route("/graph")
def graph():
    df = pd.read_csv(
        os.path.join(BASE_DIR, "data", "raw", "bitcoin_transactions.csv")
    )

    nodes = set()
    edges = []

    for _, row in df.iterrows():
        source = row["input_address"]
        target = row["output_address"]

        nodes.add(source)
        nodes.add(target)

        edges.append({
            "source": source,
            "target": target,
            "txid": row["txid"],
            "amount": row["output_amount"]
        })

    return jsonify({
        "nodes": [{"id": node} for node in nodes],
        "edges": edges
    })
