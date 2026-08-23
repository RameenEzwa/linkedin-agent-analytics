from __future__ import annotations


def recommend_daily_capacity(
    *,
    tier_ceiling: int,
    observed_daily_volume: float,
    risk_score: float | None,
) -> int:
    """
    Recommend a daily outreach capacity.

    The recommendation can never exceed the account's tier ceiling.
    """

    if tier_ceiling <= 0:
        raise ValueError("tier_ceiling must be greater than zero.")

    if observed_daily_volume < 0:
        raise ValueError("observed_daily_volume cannot be negative.")

    if risk_score is None:
        # No statistical evidence yet: use a conservative baseline.
        recommended = tier_ceiling * 0.80

    elif risk_score >= 90:
        # Critical risk: pause outreach.
        recommended = 0

    elif risk_score >= 75:
        # High risk: substantial reduction.
        recommended = tier_ceiling * 0.50

    elif risk_score >= 60:
        # Warning: moderate reduction.
        recommended = tier_ceiling * 0.75

    else:
        # Normal: retain observed operating level, capped by tier.
        recommended = min(observed_daily_volume, tier_ceiling)

    return max(0, min(tier_ceiling, int(round(recommended))))