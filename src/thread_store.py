from pathlib import Path
from typing import Union


def save_daily_report(markdown_content: str, target_date: str) -> Path:
    """
    Save markdown report to exports/daily/ directory with date-based filename.

    Creates the directory structure if it doesn't exist. Returns the path
    to the saved file for confirmation and downstream processing.

    Args:
        markdown_content: Markdown-formatted report string
        target_date: ISO 8601 date string (e.g., '2026-07-03')

    Returns:
        Path object pointing to the saved file

    Raises:
        IOError: If file write fails
        ValueError: If target_date format is invalid
    """
    # Get the report filepath
    report_path = _get_report_filepath(target_date)

    # Ensure the exports/daily directory exists
    _ensure_export_directory_exists(report_path.parent)

    # Write markdown content to disk
    try:
        report_path.write_text(markdown_content, encoding='utf-8')
    except IOError as e:
        raise IOError(f"Failed to write report to {report_path}: {e}") from e

    return report_path


def _get_report_filepath(target_date: str) -> Path:
    """
    Generate the filepath for a daily report.

    Args:
        target_date: ISO 8601 date string (e.g., '2026-07-03')

    Returns:
        Path object for the report file

    Raises:
        ValueError: If target_date format is invalid
    """
    try:
        # Validate date format by parsing
        _validate_date_format(target_date)
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got '{target_date}'") from e

    # Construct relative path: exports/daily/YYYY-MM-DD.md
    # Note: This is relative to the project root, not the current script location
    project_root = Path(__file__).parent.parent
    report_filename = f"{target_date}.md"
    return project_root / "exports" / "daily" / report_filename


def _ensure_export_directory_exists(directory: Path) -> None:
    """
    Create the export directory if it doesn't already exist.

    Uses exist_ok=True to prevent errors if directory already exists.

    Args:
        directory: Path object for the directory to create

    Raises:
        IOError: If directory creation fails
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise IOError(f"Failed to create directory {directory}: {e}") from e


def _validate_date_format(date_str: str) -> None:
    """
    Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Raises:
        ValueError: If date string is not in valid YYYY-MM-DD format
    """
    from datetime import datetime

    if not isinstance(date_str, str):
        raise ValueError("Date must be a string")

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")
