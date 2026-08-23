from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import mean, stdev


MIN_HISTORY_DAYS = 14

WEIGHTS = {
    "acceptance": 0.30,
    "reply": 0.30,
    "ghosting": 0.25,
    "capacity": 0.15,
}


@dataclass
class RiskResult:
    risk_score: float | None
    status: str
    sufficient_history: bool
    acceptance_component: float
    reply_component: float
    ghosting_component: float
    capacity_component: float


def _z_score(value: float, history: list[float]) -> float:
    if len(history) < 2:
        return 0.0

    deviation = stdev(history)

    if deviation == 0:
        return 0.0

    return (value - mean(history)) / deviation


def _negative_anomaly_score(value: float, history: list[float]) -> float:
    """
    Convert a negative performance z-score into a 0-100 risk component.
    Values at or above the historical mean produce zero risk.
    """
    z = _z_score(value, history)

    if z >= 0:
        return 0.0

    return min(100.0, abs(z) / 3.0 * 100.0)


def _positive_anomaly_score(value: float, history: list[float]) -> float:
    """
    Convert an unusually high risk metric into a 0-100 component.
    """
    z = _z_score(value, history)

    if z <= 0:
        return 0.0

    return min(100.0, z / 3.0 * 100.0)


def calculate_risk_score(
    *,
    acceptance_rate: float,
    acceptance_history: list[float],
    reply_rate: float,
    reply_history: list[float],
    ghosting_rate: float,
    ghosting_history: list[float],
    daily_volume: int,
    capacity_limit: int,
) -> RiskResult:
    """
    Calculate a composite 0-100 operational risk score.

    Statistical anomaly components use historical z-scores.
    A minimum historical baseline of 14 observations is required.
    """

    histories = [
        acceptance_history,
        reply_history,
        ghosting_history,
    ]

    sufficient_history = all(
        len(history) >= MIN_HISTORY_DAYS
        for history in histories
    )

    if not sufficient_history:
        return RiskResult(
            risk_score=None,
            status="INSUFFICIENT_DATA",
            sufficient_history=False,
            acceptance_component=0.0,
            reply_component=0.0,
            ghosting_component=0.0,
            capacity_component=0.0,
        )

    values = [
        acceptance_rate,
        reply_rate,
        ghosting_rate,
    ]

    if not all(isfinite(value) for value in values):
        raise ValueError("Rate values must be finite numbers.")

    if capacity_limit <= 0:
        raise ValueError("capacity_limit must be greater than zero.")

    capacity_utilisation = daily_volume / capacity_limit

    if capacity_utilisation <= 0.80:
        capacity_component = 0.0
    elif capacity_utilisation <= 1.00:
        capacity_component = (
            (capacity_utilisation - 0.80) / 0.20
        ) * 50.0
    else:
        capacity_component = min(
            100.0,
            50.0 + (capacity_utilisation - 1.00) * 100.0,
        )

    acceptance_component = _negative_anomaly_score(
        acceptance_rate,
        acceptance_history,
    )

    reply_component = _negative_anomaly_score(
        reply_rate,
        reply_history,
    )

    ghosting_component = _positive_anomaly_score(
        ghosting_rate,
        ghosting_history,
    )

    risk_score = (
        acceptance_component * WEIGHTS["acceptance"]
        + reply_component * WEIGHTS["reply"]
        + ghosting_component * WEIGHTS["ghosting"]
        + capacity_component * WEIGHTS["capacity"]
    )

    risk_score = round(min(100.0, max(0.0, risk_score)), 2)

    if risk_score >= 90:
        status = "CRITICAL"
    elif risk_score >= 75:
        status = "HIGH_RISK"
    elif risk_score >= 60:
        status = "WARNING"
    else:
        status = "NORMAL"

    return RiskResult(
        risk_score=risk_score,
        status=status,
        sufficient_history=True,
        acceptance_component=round(acceptance_component, 2),
        reply_component=round(reply_component, 2),
        ghosting_component=round(ghosting_component, 2),
        capacity_component=round(capacity_component, 2),
    )