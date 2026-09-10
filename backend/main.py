from fastapi import FastAPI

from routes.crowd import router as crowd_router
from routes.sensor import router as sensor_router
from routes.decision import router as decision_router
from routes.alert import router as alert_router
from routes.dashboard import router as dashboard_router

app = FastAPI()

app.include_router(crowd_router)
app.include_router(sensor_router)
app.include_router(decision_router)
app.include_router(alert_router)
app.include_router(dashboard_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to GIMES Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "GIMES Backend"
    }