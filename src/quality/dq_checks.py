from sqlalchemy import text

from src.ingestion.database import get_engine


def run_dq_checks():
    engine = get_engine()

    with engine.connect() as connection:
        results = {}

        # 1. Completeness
        missing_required = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM linkedin_outreach
                WHERE lead_id IS NULL
                   OR last_updated_at IS NULL
                """
            )
        ).scalar_one()

        results["completeness"] = missing_required == 0

        # 2. Uniqueness
        duplicate_leads = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT lead_id
                    FROM linkedin_outreach
                    GROUP BY lead_id
                    HAVING COUNT(*) > 1
                ) duplicates
                """
            )
        ).scalar_one()

        results["uniqueness"] = duplicate_leads == 0

        # 3. Validity
        invalid_network_degree = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM linkedin_outreach
                WHERE network_degree IS NOT NULL
                  AND network_degree NOT IN ('1st', '2nd', '3rd')
                """
            )
        ).scalar_one()

        results["validity"] = invalid_network_degree == 0

        # 4. Timeliness
        stale_records = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM linkedin_outreach
                WHERE source_updated_at IS NOT NULL
                  AND source_updated_at < CURRENT_TIMESTAMP - INTERVAL '7 days'
                """
            )
        ).scalar_one()

        results["timeliness"] = stale_records == 0

        # 5. Referential integrity
        orphan_leads = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM fact_linkedin_activity f
                LEFT JOIN dim_lead d
                    ON f.lead_key = d.lead_key
                WHERE d.lead_key IS NULL
                """
            )
        ).scalar_one()

        results["referential_integrity"] = orphan_leads == 0

    return results