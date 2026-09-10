def calculate_confidence(anomaly, fan_out=False, fan_in=False,
                         rapid=False, layering=False):

    evidence = sum([
        anomaly == -1,
        fan_out,
        fan_in,
        rapid,
        layering
    ])

    confidence = min(50 + evidence * 10, 100)

    if confidence >= 80:
        reliability = "Very High"
    elif confidence >= 60:
        reliability = "High"
    elif confidence >= 40:
        reliability = "Medium"
    else:
        reliability = "Low"

    return confidence, reliability
