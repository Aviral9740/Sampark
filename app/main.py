from fastapi import FastAPI
from app.schemas import DuplicateRequest, DuplicateResponse
from app.services.duplicate_detector import detect_duplicates

app = FastAPI(title="Duplicate Incident Detector")


@app.post("/detect-duplicate", response_model=DuplicateResponse)
def detect_duplicate(payload: DuplicateRequest):
    return detect_duplicates(
        payload.newIncident,
        payload.existingIncidents
    )
