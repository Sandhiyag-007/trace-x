def generate_summary(alert):
    patterns = alert.get("reasons", [])

    if alert["risk"] >= 80:
        action = "Prioritize for immediate investigation"
    elif alert["risk"] >= 60:
        action = "Review transaction and connected entities"
    elif alert["risk"] >= 30:
        action = "Monitor for additional suspicious activity"
    else:
        action = "No immediate action required"

    return {
        "txid": alert["txid"],
        "wallet": alert["wallet"],
        "risk_score": alert["risk"],
        "risk_level": alert["level"],
        "confidence": alert["confidence"],
        "reliability": alert["reliability"],
        "suspicious_patterns": patterns,
        "recommended_action": action
    }
