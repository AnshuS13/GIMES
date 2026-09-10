from pydantic import BaseModel, Field


class CrowdUpdate(BaseModel):
    zone_density: list[float] = Field(..., min_length=9, max_length=9)
    vibration_detected: bool


class SensorUpdate(BaseModel):
    vibration_detected: bool

class DecisionResponse(BaseModel):
    action: int
    description: str
    timestamp: str

class AlertPayload(BaseModel):
    action_taken: int
    alert_text: str
    language: str