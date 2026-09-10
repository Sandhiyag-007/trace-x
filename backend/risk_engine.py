def calculate_risk(anomaly, fan_out=False, fan_in=False, rapid=False, layering=False):
    score = 0
    reasons = []

    if anomaly == -1:
        score += 30
        reasons.append("AI anomaly detected")

    if fan_out:
        score += 20
        reasons.append("Fan-out pattern detected")

    if fan_in:
        score += 20
        reasons.append("Fan-in pattern detected")

    if rapid:
        score += 15
        reasons.append("Rapid fund movement detected")

    if layering:
        score += 15
        reasons.append("Layering pattern detected")

    score = min(score, 100)

    if score >= 80:
        level = "Critical"
    elif score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return score, level, reasons
