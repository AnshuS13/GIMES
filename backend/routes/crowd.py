from datetime import datetime, timezone
import json

from fastapi import APIRouter

from models import CrowdUpdate
from database import get_connection


router = APIRouter()


@router.post("/crowd/update")
def update_crowd(data: CrowdUpdate):
    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO crowd_data (
            timestamp,
            zone_density_json,
            vibration_flag
        )
        VALUES (?, ?, ?)
        """,
        (
            timestamp,
            json.dumps(data.zone_density),
            int(data.vibration_detected),
        ),
    )

    new_row_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "status": "received",
        "id": new_row_id
    }