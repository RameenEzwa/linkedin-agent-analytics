import json
import uuid

from sqlalchemy import text

from src.ingestion.database import get_engine
from src.quality.dq_checks import run_dq_checks
from src.quality.dq_score import calculate_dq_score


def run_quality_pipeline(run_id=None):
    results = run_dq_checks()
    score = calculate_dq_score(results)

    dq_run_id = uuid.uuid4()

    with get_engine().begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO dq_results_history (
                    dq_run_id,
                    run_id,
                    completeness_score,
                    uniqueness_score,
                    validity_score,
                    timeliness_score,
                    referential_integrity_score,
                    composite_dq_score,
                    threshold,
                    status,
                    total_checks,
                    passed_checks,
                    failed_checks,
                    failure_details
                )
                VALUES (
                    :dq_run_id,
                    :run_id,
                    :completeness_score,
                    :uniqueness_score,
                    :validity_score,
                    :timeliness_score,
                    :referential_integrity_score,
                    :composite_dq_score,
                    :threshold,
                    :status,
                    :total_checks,
                    :passed_checks,
                    :failed_checks,
                    :failure_details
                )
                """
            ),
            {
                "dq_run_id": dq_run_id,
                "run_id": run_id,
                "completeness_score": 100 if results["completeness"] else 0,
                "uniqueness_score": 100 if results["uniqueness"] else 0,
                "validity_score": 100 if results["validity"] else 0,
                "timeliness_score": 100 if results["timeliness"] else 0,
                "referential_integrity_score": (
                    100 if results["referential_integrity"] else 0
                ),
                "composite_dq_score": score["composite_dq_score"],
                "threshold": score["threshold"],
                "status": score["status"],
                "total_checks": score["total_checks"],
                "passed_checks": score["passed_checks"],
                "failed_checks": score["failed_checks"],
                "failure_details": json.dumps(results),
            },
        )

    return {
        "dq_run_id": str(dq_run_id),
        **score,
    }
