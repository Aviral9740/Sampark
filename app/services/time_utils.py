from datetime import datetime


def minutes_difference(t1: datetime, t2: datetime) -> float:
    return abs((t1 - t2).total_seconds()) / 60
