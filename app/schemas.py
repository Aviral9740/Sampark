from pydantic import BaseModel
from typing import List
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lng: float


class Incident(BaseModel):
    id: str
    type: str
    description: str
    coordinates: Coordinates
    peopleAffected: int | None = 0
    isVerified: bool | None = False
    createdAt: datetime


class MatchedIncident(BaseModel):
    incidentId: str
    similarityScore: float
    timeDifferenceMinutes: float
    distanceMeters: float
    finalScore: float
    confidenceLabel: str
    isVerified: bool


class DuplicateRequest(BaseModel):
    newIncident: Incident
    existingIncidents: List[Incident]


class DuplicateResponse(BaseModel):
    possibleDuplicate: bool
    confidenceScore: float
    confidenceLabel: str
    matches: List[MatchedIncident]
