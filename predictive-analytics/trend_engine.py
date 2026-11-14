"""
ASTRA Predictive Health Intelligence
Version 1.0
"""

from statistics import mean


class HealthPredictor:

    def __init__(self):
        self.history = []

    def add_reading(self, reading):
        self.history.append(reading.copy())

    def analyze_trend(self, parameter):

        values = [
            item[parameter]
            for item in self.history
            if parameter in item
        ]

        if len(values) < 3:
            return {
                "status": "INSUFFICIENT DATA"
            }

        baseline = mean(values[:2])
        latest = mean(values[-2:])

        if baseline == 0:
            return {"status": "INVALID BASELINE"}

        change = (
            (latest - baseline) / baseline
        ) * 100

        if change > 10:
            trend = "INCREASING"

        elif change < -10:
            trend = "DECREASING"

        else:
            trend = "STABLE"

        return {
            "parameter": parameter,
            "trend": trend,
            "percentage_change": round(change, 2),
            "latest_value": latest,
            "historical_average": round(
                mean(values), 2
            ),
            "records_analyzed": len(values)
        }


if __name__ == "__main__":

    predictor = HealthPredictor()

    sample_data = [
        {"heart_rate": 72},
        {"heart_rate": 76},
        {"heart_rate": 82},
        {"heart_rate": 90},
        {"heart_rate": 98}
    ]

    for reading in sample_data:
        predictor.add_reading(reading)

    print("ASTRA PREDICTIVE INTELLIGENCE")

    print(
        predictor.analyze_trend("heart_rate")
    )
