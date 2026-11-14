"""
ASTRA AI Health Intelligence Engine
Version: 1.0

Experimental decision-support prototype.
Uses simulated astronaut telemetry.
"""

from math import sqrt


PARAMETERS = {
    "heart_rate": {
        "weight": 1.2,
        "demo_low": 45,
        "demo_high": 110
    },
    "spo2": {
        "weight": 1.5,
        "demo_low": 94,
        "demo_high": 100
    },
    "temperature": {
        "weight": 1.0,
        "demo_low": 35.5,
        "demo_high": 37.7
    },
    "respiration_rate": {
        "weight": 1.0,
        "demo_low": 10,
        "demo_high": 20
    }
}


def analyze_health(reading, baseline=None):

    baseline = baseline or {}

    score = 0
    reasons = []
    deviations = {}

    for parameter, config in PARAMETERS.items():

        value = reading.get(parameter)

        if value is None:
            continue

        low = config["demo_low"]
        high = config["demo_high"]

        weight = config["weight"]

        normal = low <= value <= high

        if not normal:

            score += 20 * weight

            reasons.append(
                f"{parameter} outside demo limits: {value}"
            )

        if parameter in baseline:

            reference = baseline[parameter]

            if reference and reference > 0:

                deviation = (
                    (value - reference) / reference
                ) * 100

                deviations[parameter] = round(
                    deviation, 2
                )

                if abs(deviation) >= 15:

                    score += 10 * weight

                    reasons.append(
                        f"{parameter} changed "
                        f"{deviation:.1f}% from baseline"
                    )

    score = min(round(score), 100)

    if score >= 65:
        risk = "CRITICAL"

    elif score >= 30:
        risk = "WARNING"

    else:
        risk = "NORMAL"

    return {
        "engine": "ASTRA AI",
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons,
        "baseline_deviations": deviations,
        "parameters_analyzed": len(
            [p for p in PARAMETERS if p in reading]
        )
    }


if __name__ == "__main__":

    astronaut_data = {
        "heart_rate": 125,
        "spo2": 91,
        "temperature": 38.1,
        "respiration_rate": 24
    }

    astronaut_baseline = {
        "heart_rate": 75,
        "spo2": 98,
        "temperature": 36.8,
        "respiration_rate": 15
    }

    result = analyze_health(
        astronaut_data,
        astronaut_baseline
    )

    print("ASTRA HEALTH INTELLIGENCE")
    print(result)
