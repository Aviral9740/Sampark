from typing import List
from app.schemas import Incident, MatchedIncident
from app.services.time_utils import minutes_difference
from app.services.geo_utils import haversine_distance

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# CONFIG (TUNED FOR SHORT TEXT)
# =========================
TEXT_WEIGHT = 0.25
TIME_WEIGHT = 0.25
DIST_WEIGHT = 0.5

FINAL_SCORE_THRESHOLD = 0.5

TIME_THRESHOLD_MIN = 15          # minutes
DIST_THRESHOLD_METERS = 200      # meters


# =========================
# TEXT SIMILARITY (CHAR N-GRAM TF-IDF)
# =========================
_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(2, 3),
)


def text_similarity(text1: str, text2: str) -> float:
    tfidf = _vectorizer.fit_transform([text1, text2])
    return float(cosine_similarity(tfidf[0], tfidf[1])[0][0])

def confidence_label(score):
    if score >= 0.70:
        return "HIGH"
    elif score >= 0.5:
        return "MEDIUM"
    else:
        return "LOW"


# =========================
# MAIN DUPLICATE DETECTOR
# =========================
def detect_duplicates(
    new_incident: Incident,
    existing_incidents: List[Incident]
):
    matches = []

    for inc in existing_incidents:

        # ❌ Skip self-comparison
        if inc.id == new_incident.id:
            continue

        # --- TEXT ---
        similarity = text_similarity(
            new_incident.description,
            inc.description
        )

        # --- TIME ---
        time_diff = minutes_difference(
            new_incident.createdAt,
            inc.createdAt
        )
        time_score = max(
            0.0,
            1 - (time_diff / TIME_THRESHOLD_MIN)
        )

        # --- DISTANCE ---
        distance = haversine_distance(
            new_incident.coordinates.lat,
            new_incident.coordinates.lng,
            inc.coordinates.lat,
            inc.coordinates.lng
        )
        distance_score = max(
            0.0,
            1 - (distance / DIST_THRESHOLD_METERS)
        )

        # --- FINAL WEIGHTED SCORE ---
        final_score = (
            TEXT_WEIGHT * similarity +
            TIME_WEIGHT * time_score +
            DIST_WEIGHT * distance_score
        )
        label = confidence_label(final_score)
        print(final_score)
        if final_score >= FINAL_SCORE_THRESHOLD:
            matches.append({
                "incidentId": inc.id,
                "similarityScore": round(similarity, 2),
                "timeDifferenceMinutes": round(time_diff, 1),
                "distanceMeters": round(distance, 1),
                "finalScore": round(final_score, 2),
                "confidenceLabel": label,
                "isVerified": inc.isVerified
            })

    confidence = max(
        [m["finalScore"] for m in matches],
        default=0
    )

    return {
        "possibleDuplicate": len(matches) > 0,
        "confidenceScore": round(final_score, 2),
        "confidenceLabel": confidence_label(final_score),
        "matches": matches
    }

