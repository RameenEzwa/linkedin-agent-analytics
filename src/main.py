import logging
import sys

from src.quality.dq_runner import run_quality_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> int:
    """Run the analytics data-quality pipeline."""

    logger.info("Starting LinkedIn analytics pipeline")

    try:
        result = run_quality_pipeline()

        logger.info(
            "Data quality pipeline completed: status=%s score=%s",
            result["status"],
            result["composite_dq_score"],
        )

        if result["status"] != "PASS":
            logger.error("Data quality threshold was not met")
            return 1

        logger.info("LinkedIn analytics pipeline completed successfully")
        return 0

    except Exception:
        logger.exception("LinkedIn analytics pipeline failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
