from datetime import datetime, timedelta


def days_between(start: datetime, end: datetime) -> int:
    return (end - start).days


def is_trade_expired(
    created_at: datetime,
    max_days: int = 30
) -> bool:
    return datetime.utcnow() >= created_at + timedelta(days=max_days)


def expected_holding_period(score: int) -> str:
    """
    Estimate holding period based on setup quality
    """
    if score >= 8:
        return "4–6 weeks"
    if score >= 6:
        return "2–4 weeks"
    return "1–2 weeks"
