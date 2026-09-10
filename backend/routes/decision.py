from datetime import datetime, timezone

from fastapi import APIRouter

from models import DecisionResponse
from database import get_connection


router = APIRouter()


@router.get("/decision/get", response_model=DecisionResponse)
def get_decision():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT timestamp
        FROM crowd_data
        ORDER BY id DESC
        LIMIT 1
        """
    )

    latest_row = cursor.fetchone()
    connection.close()

    # Placeholder action until the DRL/PPO model is integrated.
    action = 0

    if latest_row:
        timestamp = latest_row[0]
    else:
        timestamp = datetime.now(timezone.utc).isoformat()

    descriptions = {
        0: "Route all occupants to Exit A",
        1: "Route all occupants to Exit B",
        2: "Route all occupants to Exit C",
        3: "Initiate full evacuation",
    }

    return {
        "action": action,
        "description": descriptions[action],
        "timestamp": timestamp,
    }