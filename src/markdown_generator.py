from typing import List, Dict, Any
from datetime import datetime


def generate_daily_markdown(active_threads: List[Dict[str, Any]], target_date: str) -> str:
    """
    Generate a markdown report for active threads on a specific date.

    Args:
        active_threads: List of canonical thread objects filtered for the target date
        target_date: ISO 8601 date string (e.g., '2026-07-03')

    Returns:
        Formatted markdown string ready for file storage
    """
    lines = []

    # Header section
    lines.append("# Teams Activity Report")
    lines.append(f"Date: {target_date}")
    lines.append("")
    lines.append(f"Total Active Threads: {len(active_threads)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Thread sections
    for thread in active_threads:
        lines.extend(_format_thread(thread))
        lines.append("")

    return "\n".join(lines)


def _format_thread(thread: Dict[str, Any]) -> List[str]:
    """
    Format a single thread object as markdown.

    Includes author and timestamps for both root message and replies.

    Args:
        thread: Canonical thread object

    Returns:
        List of markdown lines for this thread
    """
    lines = []

    # Thread header
    thread_id = thread.get('thread_id', 'Unknown')
    lines.append(f"## Thread: {thread_id}")
    lines.append("")

    # Thread metadata
    author = thread.get('author', 'Unknown')
    lines.append(f"**Author:** {author}")
    lines.append("")

    created_date = _format_datetime(thread.get('created_date', ''))
    lines.append(f"**Created:** {created_date}")
    lines.append("")

    last_updated = _format_datetime(thread.get('last_updated', ''))
    lines.append(f"**Last Updated:** {last_updated}")
    lines.append("")

    reply_count = thread.get('reply_count', 0)
    lines.append(f"**Reply Count:** {reply_count}")
    lines.append("")

    # Root message section with timestamp
    lines.append("### Root Message")
    lines.append("")

    root_author = thread.get('author', 'Unknown')
    root_timestamp = _format_datetime(thread.get('created_date', ''))
    lines.append(f"**{root_author}** — {root_timestamp}")
    lines.append("")

    content = thread.get('content', '')
    if content:
        # Escape any markdown special characters in content
        escaped_content = _escape_markdown(content)
        lines.append(escaped_content)
    else:
        lines.append("*(No content)*")

    lines.append("")

    # Replies section
    replies = thread.get('replies', [])
    if replies:
        lines.append("### Replies")
        lines.append("")

        for reply in replies:
            reply_author = reply.get('author', 'Unknown')
            reply_timestamp = _format_datetime(reply.get('created_date', ''))
            reply_content = reply.get('content', '')

            # Format reply with author and timestamp on one line
            lines.append(f"**{reply_author}** — {reply_timestamp}")
            lines.append("")

            if reply_content:
                escaped_reply_content = _escape_markdown(reply_content)
                lines.append(escaped_reply_content)
            else:
                lines.append("*(No content)*")

            lines.append("")

    # Thread divider
    lines.append("---")

    return lines


def _format_datetime(datetime_str: str) -> str:
    """
    Convert ISO 8601 datetime string to human-readable format.

    Args:
        datetime_str: ISO 8601 datetime string (e.g., '2026-07-03T08:00:00.000Z')

    Returns:
        Formatted datetime string (e.g., '2026-07-03 08:00:00 UTC')
    """
    if not datetime_str:
        return "Unknown"

    try:
        # Parse ISO format, handling 'Z' suffix
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        # Format as readable string
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except (ValueError, TypeError):
        return datetime_str


def _escape_markdown(text: str) -> str:
    """
    Escape markdown special characters in text to prevent formatting issues.

    This preserves the literal text while preventing accidental markdown interpretation.

    Args:
        text: Raw text that may contain markdown special characters

    Returns:
        Text with special characters escaped
    """
    # Escape backslashes first to avoid double-escaping
    text = text.replace('\\', '\\\\')
    # Escape other markdown special characters
    text = text.replace('*', '\\*')
    text = text.replace('_', '\\_')
    text = text.replace('`', '\\`')
    text = text.replace('[', '\\[')
    text = text.replace(']', '\\]')
    text = text.replace('#', '\\#')
    return text
