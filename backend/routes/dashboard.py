from fastapi import APIRouter

from database import get_connection


router = APIRouter()


@router.get("/dashboard/state")
def get_dashboard_state():
    connection = get_connection()
    cursor = connection.cursor()

    # Latest crowd data
    cursor.execute(
        """
        SELECT timestamp, zone_density_json, vibration_flag
        FROM crowd_data
        ORDER BY id DESC
        LIMIT 1
        """
    )
    crowd_row = cursor.fetchone()

    # Latest sensor reading
    cursor.execute(
        """
        SELECT timestamp, sensor_type, value
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
        """
    )
    sensor_row = cursor.fetchone()

    # Latest alert
    cursor.execute(
        """
        SELECT timestamp, action_taken, alert_text, language
        FROM alerts
        ORDER BY id DESC
        LIMIT 1
        """
    )
    alert_row = cursor.fetchone()

    # Current QR occupancy
    cursor.execute(
        """
        SELECT user_id, checkin_time, checkout_time, status
        FROM qr_occupancy
        ORDER BY id DESC
        LIMIT 1
        """
    )
    qr_row = cursor.fetchone()

    connection.close()

    return {
        "crowd": {
            "timestamp": crowd_row[0],
            "zone_density_json": crowd_row[1],
            "vibration_flag": crowd_row[2],
        } if crowd_row else None,

        "sensor": {
            "timestamp": sensor_row[0],
            "sensor_type": sensor_row[1],
            "value": sensor_row[2],
        } if sensor_row else None,

        "alert": {
            "timestamp": alert_row[0],
            "action_taken": alert_row[1],
            "alert_text": alert_row[2],
            "language": alert_row[3],
        } if alert_row else None,

        "qr_occupancy": {
            "user_id": qr_row[0],
            "checkin_time": qr_row[1],
            "checkout_time": qr_row[2],
            "status": qr_row[3],
        } if qr_row else None,
    }