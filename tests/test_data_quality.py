from src.quality.dq_checks import run_dq_checks
from src.quality.dq_score import calculate_dq_score


def test_dq_checks():
    results = run_dq_checks()

    assert set(results.keys()) == {
        "completeness",
        "uniqueness",
        "validity",
        "timeliness",
        "referential_integrity",
    }


def test_dq_score():
    results = {
        "completeness": True,
        "uniqueness": True,
        "validity": True,
        "timeliness": True,
        "referential_integrity": True,
    }

    score = calculate_dq_score(results)

    assert score["composite_dq_score"] == 100.0
    assert score["status"] == "PASS"
    assert score["passed_checks"] == 5
    assert score["failed_checks"] == 0