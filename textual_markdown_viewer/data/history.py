"""Provides code for saving and loading the history."""

from __future__ import annotations

from pathlib import Path
from json import dumps, loads, JSONEncoder
from typing import Any


from httpx import URL

from xdg import xdg_data_home

from ..utility import is_likely_url


def data_directory() -> Path:
    """Get the location of the data directory.

    Returns:
        The location of the data directory.

    Note:
        As a side effect, if the directory doesn't exist it will be created.
    """
    (target_directory := xdg_data_home() / "textualize" / "markdown-viewer").mkdir(
        parents=True, exist_ok=True
    )
    return target_directory


def history_file() -> Path:
    """Get the location of the history file.

    Returns:
        The location of the history file.
    """
    return data_directory() / "history.json"


class HistoryEncoder(JSONEncoder):
    """JSON encoder for the history data."""

    def default(self, o: object) -> Any:
        """Handle the Path and URL values.

        Args:
            o: The object to handle.

        Return:
            The encoded object.
        """
        return str(o) if isinstance(o, (Path, URL)) else o


def save_history(history: list[Path | URL]) -> None:
    """Save the given history.

    Args:
        history: The history to save.
    """
    history_file().write_text(dumps(history, indent=4, cls=HistoryEncoder))


def load_history() -> list[Path | URL]:
    """Load the history.

    Returns:
        The history.
    """
    return [
        URL(location) if is_likely_url(location) else Path(location)
        for location in loads(history_file().read_text())
    ]
