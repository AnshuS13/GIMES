from datetime import datetime, timezone

from fastapi import APIRouter

from models import AlertPayload
from database import get_connection


router = APIRouter()

latest_alert = None


@router.post("/alert/send")
def send_alert(data: AlertPayload):
    global latest_alert

    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (
            timestamp,
            action_taken,
            alert_text,
            language
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            timestamp,
            data.action_taken,
            data.alert_text,
            data.language,
        ),
    )

    new_row_id = cursor.lastrowid

    connection.commit()
    connection.close()

    latest_alert = {
        "action_taken": data.action_taken,
        "alert_text": data.alert_text,
        "language": data.language,
        "timestamp": timestamp,
    }

    return {
        "status": "alert_sent",
        "id": new_row_id,
    }