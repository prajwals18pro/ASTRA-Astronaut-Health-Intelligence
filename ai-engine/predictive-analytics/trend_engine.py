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
                "status": "INSUFFICIENT DATA",
                "message": "Need at least 3 readings"
            }

        first = mean(values[:2])
        latest = mean(values[-2:])

        change = latest - first

        percentage = (
            (change / first) * 100
            if first != 0 else 0
        )

        if percentage > 10:
            trend = "INCREASING"

        elif percentage < -10:
            trend = "DECREASING"

        else:
            trend = "STABLE"

        return {
            "parameter": parameter,
            "trend": trend,
            "change_percent": round(percentage, 2),
            "latest_value": latest,
            "average": round(mean(values), 2),
            "confidence": "EXPLORATORY"
        }


if __name__ == "__main__":

    predictor = HealthPredictor()

    readings = [
        {"heart_rate": 72},
        {"heart_rate": 76},
        {"heart_rate": 82},
        {"heart_rate": 90},
        {"heart_rate": 98}
    ]

    for reading in readings:
        predictor.add_reading(reading)

    print(
        predictor.analyze_trend("heart_rate")
    )
