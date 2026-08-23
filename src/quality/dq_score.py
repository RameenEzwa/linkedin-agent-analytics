WEIGHTS = {
    "completeness": 0.25,
    "uniqueness": 0.20,
    "validity": 0.20,
    "timeliness": 0.15,
    "referential_integrity": 0.20,
}

PASS_THRESHOLD = 90.0


def calculate_dq_score(results: dict) -> dict:
    """
    Calculate the weighted composite Data Quality score.

    Each check is represented as True (100) or False (0).
    """

    score = sum(
        (100.0 if results[check] else 0.0) * weight
        for check, weight in WEIGHTS.items()
    )

    passed_checks = sum(
        1 for check in WEIGHTS if results[check]
    )

    total_checks = len(WEIGHTS)
    failed_checks = total_checks - passed_checks

    status = "PASS" if score >= PASS_THRESHOLD else "FAIL"

    return {
        "composite_dq_score": round(score, 2),
        "threshold": PASS_THRESHOLD,
        "status": status,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
    }