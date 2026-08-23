from src.analytics.capacity import recommend_daily_capacity


def test_capacity_never_exceeds_tier_ceiling():
    result = recommend_daily_capacity(
        tier_ceiling=100,
        observed_daily_volume=150,
        risk_score=20,
    )

    assert result <= 100


def test_critical_risk_pauses_outreach():
    result = recommend_daily_capacity(
        tier_ceiling=100,
        observed_daily_volume=80,
        risk_score=95,
    )

    assert result == 0


def test_high_risk_reduces_capacity():
    result = recommend_daily_capacity(
        tier_ceiling=100,
        observed_daily_volume=80,
        risk_score=80,
    )

    assert result == 50


def test_warning_reduces_capacity():
    result = recommend_daily_capacity(
        tier_ceiling=100,
        observed_daily_volume=80,
        risk_score=65,
    )

    assert result == 75