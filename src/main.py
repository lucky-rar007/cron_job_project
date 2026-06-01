import logging
import sys
from cron_job import simulate_cron_run

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """
    Entry point for Teams ingestion pipeline.

    Supports:
    1. Default simulation run (hardcoded test date)
    2. Custom date via CLI
    """

    logger.info("=" * 80)
    logger.info("TEAMS CHANNEL INGESTION - CRON SIMULATION")
    logger.info("=" * 80)

    try:
        # -----------------------------
        # Determine input date
        # -----------------------------
        if len(sys.argv) > 1:
            current_date = sys.argv[1]
            logger.info(f"Using CLI provided date: {current_date}")
        else:
            current_date = "2026-07-04"
            logger.info(f"No CLI date provided. Using default: {current_date}")

        logger.info(f"\nSimulating cron job run at {current_date} 00:00 IST\n")

        # -----------------------------
        # Run pipeline
        # -----------------------------
        summary = simulate_cron_run(current_date)

        # -----------------------------
        # Print summary
        # -----------------------------
        logger.info("=" * 80)
        logger.info("CRON EXECUTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Current Date:       {summary['current_date']}")
        logger.info(f"Processing Date:    {summary['process_date']}")
        logger.info(f"Total Threads:      {summary['total_threads']}")
        logger.info(f"Active Threads:     {summary['active_threads']}")
        logger.info(f"Report Saved To:    {summary['report_path']}")
        logger.info("=" * 80)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")

    except ValueError as e:
        logger.error(f"Invalid input: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()