def score_setup(
    weekly_trend: str,
    zone_fresh: bool,
    volume_expansion: bool,
    rsi: float,
    risk_reward: float,
    structure_clean: bool
) -> int:

    score = 0

    # 1. Weekly trend
    if weekly_trend == "BULL":
        score += 2

    # 2. Zone freshness
    if zone_fresh:
        score += 2

    # 3. Volume confirmation
    if volume_expansion:
        score += 2

    # 4. RSI sweet spot (swing)
    if 35 <= rsi <= 45:
        score += 1

    # 5. Risk reward
    if risk_reward >= 2:
        score += 1

    # 6. Clean market structure
    if structure_clean:
        score += 1

    return score


def score_to_confidence(score: int) -> str:
    if score >= 7:
        return "HIGH"
    if score >= 5:
        return "MEDIUM"
    return "LOW"
