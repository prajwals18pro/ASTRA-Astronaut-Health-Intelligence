"""
ASTRA Communication Resilience Engine
Version 1.0

Offline telemetry storage and synchronization.
"""

import sqlite3
import json
import uuid

from datetime import datetime, timezone


class OfflineTelemetry:

    def __init__(self, database="astra_offline.db"):

        self.connection = sqlite3.connect(database)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                payload TEXT,
                synced INTEGER DEFAULT 0
            )
        """)

        self.connection.commit()

        self.communication_status = "CONNECTED"

    def set_connection(self, connected):

        self.communication_status = (
            "CONNECTED" if connected else "OFFLINE"
        )

    def store_reading(self, reading):

        record_id = str(uuid.uuid4())

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        self.connection.execute(
            """
            INSERT INTO telemetry
            (id, timestamp, payload, synced)
            VALUES (?, ?, ?, 0)
            """,
            (
                record_id,
                timestamp,
                json.dumps(reading)
            )
        )

        self.connection.commit()

        return {
            "record_id": record_id,
            "stored": True,
            "communication": self.communication_status
        }

    def pending_records(self):

        cursor = self.connection.execute(
            """
            SELECT id, timestamp, payload
            FROM telemetry
            WHERE synced = 0
            ORDER BY timestamp
            """
        )

        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "data": json.loads(row[2])
            }
            for row in cursor.fetchall()
        ]

    def synchronize(self):

        if self.communication_status == "OFFLINE":

            return {
                "status": "WAITING_FOR_CONNECTION",
                "pending": len(self.pending_records())
            }

        records = self.pending_records()

        if not records:

            return {
                "status": "NO_PENDING_DATA",
                "synchronized": 0
            }

        # Demonstration acknowledgement.
        # Replace with actual mission-control API later.

        for record in records:

            self.connection.execute(
                """
                UPDATE telemetry
                SET synced = 1
                WHERE id = ?
                """,
                (record["id"],)
            )

        self.connection.commit()

        return {
            "status": "SYNC_COMPLETE",
            "synchronized": len(records)
        }

    def close(self):

        self.connection.close()


if __name__ == "__main__":

    system = OfflineTelemetry()

    system.set_connection(False)

    print("COMMUNICATION LOST")

    print(system.store_reading({
        "astronaut": "AST-001",
        "heart_rate": 85,
        "spo2": 97
    }))

    print(system.store_reading({
        "astronaut": "AST-001",
        "heart_rate": 92,
        "spo2": 96
    }))

    print("PENDING DATA:")
    print(system.pending_records())

    system.set_connection(True)

    print("COMMUNICATION RESTORED")

    print(system.synchronize())

    system.close()
