"""In-memory command state shared by the server routes."""

from __future__ import annotations

from threading import Lock
from typing import Optional

_command_lock = Lock()
_latest_command: Optional[str] = None
_last_completed_command: Optional[str] = None


def set_command(command: str) -> None:
    """Store the latest command, replacing any previously pending command."""
    global _latest_command
    with _command_lock:
        _latest_command = command


def pop_command() -> Optional[str]:
    """Return the latest command and clear it from memory."""
    global _latest_command
    with _command_lock:
        command = _latest_command
        _latest_command = None
        return command


def mark_completed(command: Optional[str]) -> None:
    """Track the most recently completed command for debugging/status."""
    global _last_completed_command
    with _command_lock:
        _last_completed_command = command


def get_last_completed_command() -> Optional[str]:
    """Return the most recently completed command."""
    with _command_lock:
        return _last_completed_command
