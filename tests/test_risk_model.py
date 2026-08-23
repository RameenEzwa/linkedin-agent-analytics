from src.analytics.risk_model import calculate_risk_score


def test_risk_model_requires_history():
    result = calculate_risk_score(
        acceptance_rate=0.20,
        acceptance_history=[0.30] * 5,
        reply_rate=0.10,
        reply_history=[0.20] * 5,
        ghosting_rate=0.50,
        ghosting_history=[0.20] * 5,
        daily_volume=20,
        capacity_limit=30,
    )

    assert result.status == "INSUFFICIENT_DATA"
    assert result.risk_score is None


def test_normal_risk():
    history = [
        0.30,
        0.31,
        0.29,
        0.30,
        0.32,
        0.28,
        0.30,
        0.31,
        0.29,
        0.30,
        0.31,
        0.29,
        0.30,
        0.31,
    ]

    result = calculate_risk_score(
        acceptance_rate=0.30,
        acceptance_history=history,
        reply_rate=0.20,
        reply_history=history,
        ghosting_rate=0.10,
        ghosting_history=history,
        daily_volume=20,
        capacity_limit=30,
    )

    assert result.sufficient_history is True
    assert result.risk_score is not None
    assert result.status == "NORMAL"


def test_high_risk_acceptance_collapse():
    history = [
        0.30,
        0.31,
        0.29,
        0.30,
        0.32,
        0.28,
        0.30,
        0.31,
        0.29,
        0.30,
        0.31,
        0.29,
        0.30,
        0.31,
    ]

    result = calculate_risk_score(
        acceptance_rate=0.05,
        acceptance_history=history,
        reply_rate=0.20,
        reply_history=history,
        ghosting_rate=0.10,
        ghosting_history=history,
        daily_volume=30,
        capacity_limit=30,
    )

    assert result.risk_score is not None
    assert result.risk_score > 0