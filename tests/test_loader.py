from datetime import datetime, timezone

from sqlalchemy import text

from src.ingestion.loader import load_records
from src.ingestion.database import get_engine


def test_load_records():
    lead_id = "TEST-001"

    record = {
        "lead_id": lead_id,
        "profile_url": "https://example.com/test",
        "first_name": "Test",
        "last_name": "User",
        "job_title": "Data Analyst",
        "company_name": "Test Company",
        "industry": "Technology",
        "network_degree": "1st",
        "pipeline_stage": "Connected",
        "invited_at": None,
        "accepted_at": None,
        "messaged_at": None,
        "replied_at": None,
        "last_updated_at": datetime.now(timezone.utc),
        "source_updated_at": datetime.now(timezone.utc),
    }

    run_id = load_records([record])

    assert run_id

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT lead_id
                FROM linkedin_outreach
                WHERE lead_id = :lead_id
                """
            ),
            {"lead_id": lead_id},
        )

        assert result.scalar() == lead_id

def test_load_records_is_idempotent():
    record = {
        "lead_id": "TEST-IDEMPOTENT-001",
        "profile_url": "https://example.com/idempotent",
        "first_name": "Test",
        "last_name": "Idempotent",
        "job_title": "Data Analyst",
        "company_name": "Test Company",
        "industry": "Technology",
        "network_degree": "1st",
        "pipeline_stage": "Connected",
        "invited_at": None,
        "accepted_at": None,
        "messaged_at": None,
        "replied_at": None,
        "last_updated_at": "2026-08-23T00:00:00+00:00",
        "source_updated_at": "2026-08-23T00:00:00+00:00",
    }

    load_records([record])
    load_records([record])

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM linkedin_outreach
                WHERE lead_id = :lead_id
                """
            ),
            {"lead_id": record["lead_id"]},
        )

        assert result.scalar() == 1