import logging
from cron_job import simulate_cron_run

# Configure logging with a simple format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point demonstrating Milestone 4: pipeline orchestration and cron simulation.

    Simulates a cron job running at 2026-07-04 00:00 IST.
    The cron job processes the PREVIOUS day (2026-07-03).
    """
    logger.info("=" * 80)
    logger.info("TEAMS CHANNEL INGESTION - CRON SIMULATION")
    logger.info("=" * 80)

    try:
        # Simulate cron run: current date is 2026-07-04, process 2026-07-03
        current_date = '2026-07-04'

        logger.info(f"\nSimulating cron job run at {current_date} 00:00 IST\n")

        # Run the simulated cron job
        summary = simulate_cron_run(current_date)

        # Print formatted summary
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


if __name__ == '__main__':
    main()
