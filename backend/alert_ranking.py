def rank_alerts(alerts):
    return sorted(
        alerts,
        key=lambda x: (x["risk"], x["confidence"]),
        reverse=True
    )
