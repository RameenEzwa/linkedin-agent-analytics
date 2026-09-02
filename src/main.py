import json
import logging
import sys
import time
import uuid

from src.quality.dq_runner import run_quality_pipeline


class JsonFormatter(logging.Formatter):
    """Format log records as machine-parseable JSON."""

    def format(self, record):
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "run_id"):
            payload["run_id"] = record.run_id

        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("linkedin_pipeline")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False


def main() -> int:
    """Run the analytics data-quality pipeline with structured logging."""

    run_id = str(uuid.uuid4())
    started = time.monotonic()

    logger.info(
        "pipeline_started",
        extra={"run_id": run_id},
    )

    try:
        result = run_quality_pipeline(run_id=run_id)

        duration_seconds = round(time.monotonic() - started, 2)

        logger.info(
            "dq_pipeline_completed",
            extra={"run_id": run_id},
        )

        logger.info(
            (
                "pipeline_summary "
                "status=%s score=%s duration_seconds=%s"
            ),
            result["status"],
            result["composite_dq_score"],
            duration_seconds,
            extra={"run_id": run_id},
        )

        if result["status"] != "PASS":
            logger.error(
                "dq_threshold_breached",
                extra={"run_id": run_id},
            )
            return 1

        logger.info(
            "pipeline_completed_successfully",
            extra={"run_id": run_id},
        )
        return 0

    except Exception:
        duration_seconds = round(time.monotonic() - started, 2)

        logger.exception(
            "pipeline_failed duration_seconds=%s",
            duration_seconds,
            extra={"run_id": run_id},
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())