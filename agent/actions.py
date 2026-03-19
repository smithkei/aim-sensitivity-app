"""Executable actions for the Overwatch replay polling agent."""

from __future__ import annotations

import subprocess
import time
from typing import Callable, Dict

import pyautogui

import config

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2


def start_ow() -> None:
    """Launch Overwatch using the configured Windows executable path."""
    subprocess.Popen([config.OVERWATCH_EXECUTABLE], shell=False)


def open_replay() -> None:
    """Wait for the game window to load and click into the replay menu."""
    time.sleep(15)
    pyautogui.click(*config.OPEN_REPLAY_BUTTON)


def select_replay_1() -> None:
    """Select the first replay entry and confirm with Enter."""
    pyautogui.click(*config.SELECT_REPLAY_1)
    time.sleep(0.5)
    pyautogui.press("enter")


def play_pause() -> None:
    """Toggle replay playback using the in-game keyboard shortcut."""
    pyautogui.hotkey("ctrl", "p")


COMMAND_HANDLERS: Dict[str, Callable[[], None]] = {
    "start_ow": start_ow,
    "open_replay": open_replay,
    "select_replay_1": select_replay_1,
    "play_pause": play_pause,
}
