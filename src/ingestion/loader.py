import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import text

from src.ingestion.database import get_engine


def load_records(records: list[dict]) -> str:
    """
    Load LinkedIn records into PostgreSQL.

    Uses lead_id as the unique key so repeated runs do not
    create duplicate records.

    The ingestion watermark advances only to the latest
    successfully loaded record. Failed records remain eligible
    for a future retry.
    """
    records = filter_incremental_records(
        records,
        source_name="linkedin",
    )

    engine = get_engine()
    run_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)

    rows_in = len(records)
    rows_out = 0
    failed_records = 0

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO run_metadata
                    (run_id, started_at, status, rows_in)
                VALUES
                    (:run_id, :started_at, :status, :rows_in)
                """
            ),
            {
                "run_id": run_id,
                "started_at": started_at,
                "status": "RUNNING",
                "rows_in": rows_in,
            },
        )

        successful_timestamps = []

        for record in records:
            try:
                connection.execute(
                    text(
                        """
                        INSERT INTO linkedin_outreach (
                            lead_id,
                            profile_url,
                            first_name,
                            last_name,
                            job_title,
                            company_name,
                            industry,
                            network_degree,
                            pipeline_stage,
                            invited_at,
                            accepted_at,
                            messaged_at,
                            replied_at,
                            last_updated_at,
                            source_updated_at,
                            raw_payload
                        )
                        VALUES (
                            :lead_id,
                            :profile_url,
                            :first_name,
                            :last_name,
                            :job_title,
                            :company_name,
                            :industry,
                            :network_degree,
                            :pipeline_stage,
                            :invited_at,
                            :accepted_at,
                            :messaged_at,
                            :replied_at,
                            :last_updated_at,
                            :source_updated_at,
                            :raw_payload
                        )
                        ON CONFLICT (lead_id)
                        DO UPDATE SET
                            profile_url = EXCLUDED.profile_url,
                            first_name = EXCLUDED.first_name,
                            last_name = EXCLUDED.last_name,
                            job_title = EXCLUDED.job_title,
                            company_name = EXCLUDED.company_name,
                            industry = EXCLUDED.industry,
                            network_degree = EXCLUDED.network_degree,
                            pipeline_stage = EXCLUDED.pipeline_stage,
                            invited_at = EXCLUDED.invited_at,
                            accepted_at = EXCLUDED.accepted_at,
                            messaged_at = EXCLUDED.messaged_at,
                            replied_at = EXCLUDED.replied_at,
                            last_updated_at = EXCLUDED.last_updated_at,
                            source_updated_at = EXCLUDED.source_updated_at,
                            raw_payload = EXCLUDED.raw_payload
                        """
                    ),
                    {
                        "lead_id": record["lead_id"],
                        "profile_url": record.get("profile_url"),
                        "first_name": record.get("first_name"),
                        "last_name": record.get("last_name"),
                        "job_title": record.get("job_title"),
                        "company_name": record.get("company_name"),
                        "industry": record.get("industry"),
                        "network_degree": record.get("network_degree"),
                        "pipeline_stage": record.get("pipeline_stage"),
                        "invited_at": record.get("invited_at"),
                        "accepted_at": record.get("accepted_at"),
                        "messaged_at": record.get("messaged_at"),
                        "replied_at": record.get("replied_at"),
                        "last_updated_at": record["last_updated_at"],
                        "source_updated_at": record.get("source_updated_at"),
                        "raw_payload": json.dumps(record, default=str),
                    },
                )

                rows_out += 1

                source_updated_at = record.get("source_updated_at")

                if source_updated_at is not None:
                    if source_updated_at.tzinfo is None:
                        source_updated_at = source_updated_at.replace(
                            tzinfo=timezone.utc
                        )

                    successful_timestamps.append(source_updated_at)

            except Exception as exc:
                failed_records += 1

                connection.execute(
                    text(
                        """
                        INSERT INTO dead_letter
                            (run_id, record_payload, error_message)
                        VALUES
                            (:run_id, :record_payload, :error_message)
                        """
                    ),
                    {
                        "run_id": run_id,
                        "record_payload": json.dumps(
                            record,
                            default=str,
                        ),
                        "error_message": str(exc),
                    },
                )

        # Only advance the watermark to the latest record that
        # was actually loaded successfully.
        if successful_timestamps:
            connection.execute(
                text(
                    """
                    INSERT INTO ingestion_watermark (
                        source_name,
                        last_updated_at
                    )
                    VALUES (
                        :source_name,
                        :last_updated_at
                    )
                    ON CONFLICT (source_name)
                    DO UPDATE SET
                        last_updated_at = EXCLUDED.last_updated_at
                    """
                ),
                {
                    "source_name": "linkedin",
                    "last_updated_at": max(successful_timestamps),
                },
            )

        if failed_records == 0:
            status = "SUCCESS"
            error_message = None
        elif rows_out > 0:
            status = "PARTIAL"
            error_message = (
                f"{failed_records} record(s) failed and were "
                "written to dead_letter."
            )
        else:
            status = "FAILED"
            error_message = (
                f"All {failed_records} record(s) failed and were "
                "written to dead_letter."
            )

        ended_at = datetime.now(timezone.utc)

        connection.execute(
            text(
                """
                UPDATE run_metadata
                SET
                    ended_at = :ended_at,
                    rows_out = :rows_out,
                    status = :status,
                    error_message = :error_message
                WHERE run_id = :run_id
                """
            ),
            {
                "run_id": run_id,
                "ended_at": ended_at,
                "rows_out": rows_out,
                "status": status,
                "error_message": error_message,
            },
        )

    return run_id
def get_watermark(source_name: str) -> datetime | None:
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT last_updated_at
                FROM ingestion_watermark
                WHERE source_name = :source_name
                """
            ),
            {"source_name": source_name},
        )

        return result.scalar()


def update_watermark(
    source_name: str,
    last_updated_at: datetime,
) -> None:
    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO ingestion_watermark
                    (source_name, last_updated_at)
                VALUES
                    (:source_name, :last_updated_at)
                ON CONFLICT (source_name)
                DO UPDATE SET
                    last_updated_at = EXCLUDED.last_updated_at
                """
            ),
            {
                "source_name": source_name,
                "last_updated_at": last_updated_at,
            },
        )


def filter_incremental_records(
    records: list[dict],
    source_name: str,
) -> list[dict]:
    watermark = get_watermark(source_name)

    if watermark is None:
        return records

    if watermark.tzinfo is None:
        watermark = watermark.replace(tzinfo=timezone.utc)

    filtered = []

    for record in records:
        source_updated_at = record.get("source_updated_at")

        if source_updated_at is None:
            continue

        if source_updated_at.tzinfo is None:
            source_updated_at = source_updated_at.replace(tzinfo=timezone.utc)

        if source_updated_at > watermark:
            filtered.append(record)

    return filtered