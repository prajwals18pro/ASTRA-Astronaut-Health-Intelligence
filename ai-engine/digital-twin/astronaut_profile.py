from datetime import datetime


class AstronautDigitalTwin:

    def __init__(self, astronaut_id, name):

        self.astronaut_id = astronaut_id
        self.name = name

        self.baseline = {}
        self.history = []

        self.status = "INITIALIZING"

    def establish_baseline(self, readings):

        self.baseline = readings.copy()

        self.status = "BASELINE ESTABLISHED"

    def update_health(self, readings):

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "readings": readings.copy()
        }

        self.history.append(record)

        return self.analyze_changes(readings)

    def analyze_changes(self, readings):

        changes = {}

        for parameter, value in readings.items():

            reference = self.baseline.get(parameter)

            if reference is None or reference == 0:
                continue

            percentage = (
                (value - reference) / reference
            ) * 100

            changes[parameter] = round(
                percentage, 2
            )

        return {
            "astronaut": self.name,
            "astronaut_id": self.astronaut_id,
            "changes": changes,
            "records": len(self.history),
            "status": self.status
        }

    def get_health_history(self):

        return self.history

    def get_profile(self):

        return {
            "astronaut_id": self.astronaut_id,
            "name": self.name,
            "baseline": self.baseline,
            "total_records": len(self.history),
            "status": self.status
        }


if __name__ == "__main__":

    twin = AstronautDigitalTwin(
        "AST-001",
        "Commander Alex Morgan"
    )

    twin.establish_baseline({
        "heart_rate": 75,
        "spo2": 98,
        "temperature": 36.8,
        "respiration_rate": 15
    })

    result = twin.update_health({
        "heart_rate": 95,
        "spo2": 96,
        "temperature": 37.1,
        "respiration_rate": 18
    })

    print("ASTRA DIGITAL TWIN")
    print(result)
