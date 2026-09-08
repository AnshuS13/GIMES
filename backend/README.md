# GIMES Backend

Backend service for the GIMES (Generative-AI based Intelligent Multi-Exit Evacuation System) project.

## Project Scope

GIMES is currently scoped as a seismic-only evacuation prototype.

The backend handles:
- Crowd data
- Vibration sensor data
- Evacuation decisions
- Emergency alerts
- Occupancy and QR check-in/check-out data

The current prototype does NOT use smoke detection.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- python-dotenv
- requests

## Backend Structure

```text
backend/
├── database/
├── routes/
│   └── __init__.py
├── __init__.py
├── config.py
├── database.py
├── main.py
├── models.py
├── README.md
└── requirements.txt