"""
ASTRA Emergency Intelligence Engine
Version 1.0

Experimental decision-support prototype.
Uses simulated telemetry.
"""

from datetime import datetime


DEMO_LIMITS = {
    "heart_rate": (45, 110),
    "spo2": (94, 100),
    "temperature": (35.5, 37.7),
    "respiration_rate": (10, 20)
}


class EmergencyEngine:

    def analyze(self, readings):

        alerts = []
        missing = []

        for parameter, limits in DEMO_LIMITS.items():

            value = readings.get(parameter)

            if value is None:
                missing.append(parameter)
                continue

            low, high = limits

            if not isinstance(value, (int, float)):
                alerts.append(
                    f"Invalid reading: {parameter}"
                )
                continue

            if not low <= value <= high:

                alerts.append({
                    "parameter": parameter,
                    "value": value,
                    "message": (
                        f"{parameter} outside "
                        "configured demo limits"
                    )
                })

        if alerts:
            status = "ALERT"

        elif missing:
            status = "DATA_INCOMPLETE"

        else:
            status = "NORMAL"

        return {
            "system": "ASTRA EMERGENCY INTELLIGENCE",
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "alerts": alerts,
            "missing_parameters": missing,
            "recommended_action": self.get_action(status)
        }

    @staticmethod
    def get_action(status):

        actions = {
            "ALERT": (
                "Notify mission medical personnel "
                "and request immediate assessment."
            ),

            "DATA_INCOMPLETE": (
                "Check sensor connectivity and "
                "restore missing telemetry."
            ),

            "NORMAL": (
                "Continue routine monitoring."
            )
        }

        return actions[status]


if __name__ == "__main__":

    engine = EmergencyEngine()

    simulated_readings = {
        "heart_rate": 125,
        "spo2": 91,
        "temperature": 38.1,
        "respiration_rate": 24
    }

    result = engine.analyze(simulated_readings)

    print(result)
