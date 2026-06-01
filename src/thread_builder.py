from typing import List, Dict, Any
from datetime import datetime


def build_threads(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build canonical thread objects from Teams Graph API response.

    Extracts root messages, reconstructs replies with proper sorting,
    and computes aggregate fields (last_updated, reply_count).

    Args:
        data: Parsed Teams Graph API response containing messages and replies

    Returns:
        List of canonical thread objects sorted by creation date
    """
    threads = []
    messages = data.get('value', [])

    for message in messages:
        # Skip messages that are replies themselves (have replyToId)
        if message.get('replyToId') is not None:
            continue

        # Extract root message information
        thread_id = message.get('id', '')
        created_date = message.get('createdDateTime', '')
        author = _extract_author(message)
        content = _extract_content(message)

        # Extract and sort replies by creation time (ascending)
        replies_data = message.get('replies', [])
        replies = []

        for reply in replies_data:
            reply_obj = {
                'reply_id': reply.get('id', ''),
                'created_date': reply.get('createdDateTime', ''),
                'author': _extract_author(reply),
                'content': _extract_content(reply)
            }
            replies.append(reply_obj)

        # Sort replies chronologically to maintain conversation flow
        replies.sort(key=lambda r: _parse_datetime(r['created_date']))

        # Calculate last_updated: latest timestamp from root message or any reply
        all_timestamps = [_parse_datetime(created_date)]
        for reply in replies:
            all_timestamps.append(_parse_datetime(reply['created_date']))

        last_updated_dt = max(all_timestamps) if all_timestamps else _parse_datetime(created_date)
        last_updated = last_updated_dt.isoformat()

        # Build canonical thread object
        thread = {
            'thread_id': thread_id,
            'created_date': created_date,
            'last_updated': last_updated,
            'author': author,
            'content': content,
            'reply_count': len(replies),
            'replies': replies
        }

        threads.append(thread)

    return threads


def filter_threads_by_date(
    threads: List[Dict[str, Any]],
    target_date: str
) -> List[Dict[str, Any]]:
    """
    Filter threads active on a specific date.

    A thread is considered active on a date if:
    - The root message was created on that date, OR
    - At least one reply was created on that date

    Args:
        threads: List of canonical thread objects
        target_date: ISO 8601 date string (e.g., '2026-07-03')

    Returns:
        List of threads active on the target date
    """
    # Parse target date to compare only the date component
    target_date_obj = datetime.fromisoformat(target_date).date()

    active_threads = []

    for thread in threads:
        # Check if root message was created on target date
        root_created = _parse_datetime(thread['created_date'])
        if root_created.date() == target_date_obj:
            active_threads.append(thread)
            continue

        # Check if any reply was created on target date
        for reply in thread.get('replies', []):
            reply_created = _parse_datetime(reply['created_date'])
            if reply_created.date() == target_date_obj:
                active_threads.append(thread)
                break

    return active_threads


def _extract_author(message: Dict[str, Any]) -> str:
    """Safely extract author display name from message object."""
    try:
        return message.get('from', {}).get('user', {}).get('displayName', 'Unknown')
    except (TypeError, AttributeError):
        return 'Unknown'


def _extract_content(message: Dict[str, Any]) -> str:
    """Safely extract message content from body object."""
    try:
        return message.get('body', {}).get('content', '')
    except (TypeError, AttributeError):
        return ''


def _parse_datetime(datetime_str: str) -> datetime:
    """
    Parse ISO 8601 datetime string to Python datetime object.

    Handles 'Z' suffix (UTC indicator) used by Teams API responses.
    """
    if not datetime_str:
        return datetime.min
    try:
        return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return datetime.min
