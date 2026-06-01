import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

from fetcher import load_teams_data
from thread_builder import build_threads, filter_threads_by_date
from markdown_generator import generate_daily_markdown
from thread_store import save_daily_report

# Configure logging
logger = logging.getLogger(__name__)


def get_previous_day(current_date: str) -> str:
    """
    Calculate the previous day from a given date using datetime arithmetic.

    Uses datetime subtraction to reliably handle month/year boundaries.
    Does not use string manipulation.

    Args:
        current_date: ISO 8601 date string (e.g., '2026-07-04')

    Returns:
        ISO 8601 date string for the previous day (e.g., '2026-07-03')

    Raises:
        ValueError: If date format is invalid
    """
    try:
        current_dt = datetime.fromisoformat(current_date)
        previous_dt = current_dt - timedelta(days=1)
        return previous_dt.strftime('%Y-%m-%d')
    except ValueError as e:
        logger.error(f"Invalid date format: {current_date}")
        raise ValueError(
            f"Invalid date format '{current_date}'. Expected YYYY-MM-DD format."
        ) from e


def run_daily_ingestion(process_date: str) -> Dict[str, Any]:
    """
    Execute the full pipeline for a specific date.

    Orchestrates the complete data flow:
    1. Load Teams data from response.json
    2. Build canonical thread objects
    3. Filter active threads for the target date
    4. Generate markdown report
    5. Save markdown report to exports/daily/

    Args:
        process_date: ISO 8601 date string to process (e.g., '2026-07-03')

    Returns:
        Dictionary containing:
        - process_date: Date that was processed
        - total_threads: Total threads in dataset
        - active_threads: Threads active on process_date
        - report_path: Path to saved markdown file

    Raises:
        FileNotFoundError: If response.json not found
        IOError: If file operations fail
        ValueError: If date format is invalid
    """
    logger.info(f"Starting daily ingestion for {process_date}")

    try:
        # Step 1: Load Teams data
        logger.debug("Loading Teams data from response.json")
        project_root = Path(__file__).parent.parent
        data_filepath = project_root / "data" / "response.json"
        data = load_teams_data(str(data_filepath))

        # Step 2: Build canonical threads
        logger.debug("Building canonical thread objects")
        threads = build_threads(data)
        logger.debug(f"Built {len(threads)} canonical threads")

        # Step 3: Filter active threads for process_date
        logger.debug(f"Filtering threads for {process_date}")
        active_threads = filter_threads_by_date(threads, process_date)
        logger.debug(f"Found {len(active_threads)} active threads")

        # Step 4: Generate markdown report
        logger.debug("Generating markdown report")
        markdown_content = generate_daily_markdown(active_threads, process_date)

        # Step 5: Save markdown report to disk
        logger.debug("Saving markdown report to disk")
        report_path = save_daily_report(markdown_content, process_date)
        logger.info(f"Report saved to {report_path}")

        # Return summary
        summary = {
            "process_date": process_date,
            "total_threads": len(threads),
            "active_threads": len(active_threads),
            "report_path": str(report_path)
        }

        logger.info(f"Daily ingestion completed successfully for {process_date}")
        return summary

    except Exception as e:
        logger.error(f"Daily ingestion failed for {process_date}: {e}")
        raise


def simulate_cron_run(current_date: str) -> Dict[str, Any]:
    """
    Simulate a cron job execution at the given current date.

    The cron job runs at 00:00 IST and processes the PREVIOUS day's activity.
    This reflects real-world behavior: "What happened yesterday?"

    Example:
    - Cron runs on 2026-07-04 00:00 IST
    - Processes activity from 2026-07-03
    - Generates report for 2026-07-03

    Args:
        current_date: Current date as ISO 8601 string (e.g., '2026-07-04')

    Returns:
        Dictionary containing:
        - current_date: Date the cron would run
        - process_date: Date that was processed
        - total_threads: Total threads in dataset
        - active_threads: Threads active on process_date
        - report_path: Path to saved markdown file

    Raises:
        ValueError: If date format is invalid
        FileNotFoundError: If response.json not found
        IOError: If file operations fail
    """
    logger.info(f"Simulating cron run at {current_date} 00:00 IST")

    # Determine previous day to process
    process_date = get_previous_day(current_date)
    logger.info(f"Processing activity from {process_date}")

    # Run ingestion for previous day
    summary = run_daily_ingestion(process_date)

    # Add current date to summary for reference
    summary["current_date"] = current_date

    return summary
