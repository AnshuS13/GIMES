from datetime import datetime, timezone

from fastapi import APIRouter

from models import SensorUpdate
from database import get_connection


router = APIRouter()


@router.post("/sensor/update")
def update_sensor(data: SensorUpdate):
    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (
            timestamp,
            sensor_type,
            value
        )
        VALUES (?, ?, ?)
        """,
        (
            timestamp,
            "vibration",
            int(data.vibration_detected),
        ),
    )

    connection.commit()
    connection.close()

    return {
        "status": "logged"
    }