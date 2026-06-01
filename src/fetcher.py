import json
import os
from typing import Dict, Any


def load_teams_data(filepath: str) -> Dict[str, Any]:
    """
    Load and parse Microsoft Teams Graph API response from a JSON file.

    Args:
        filepath: Path to the JSON file containing Teams channel messages

    Returns:
        Parsed dictionary containing the Teams API response

    Raises:
        FileNotFoundError: If the JSON file does not exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    # Check if file exists before attempting to read
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in file {filepath}: {e.msg}",
            e.doc,
            e.pos
        ) from e
