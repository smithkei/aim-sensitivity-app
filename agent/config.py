"""Configuration for the Windows polling agent."""

import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
API_TOKEN = os.getenv("API_TOKEN", "secret123")
POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "2"))
OVERWATCH_EXECUTABLE = os.getenv(
    "OVERWATCH_EXECUTABLE",
    r"C:\Program Files (x86)\Overwatch\_retail_\Overwatch.exe",
)

# Screen coordinates for the replay UI. Update these to match the target PC.
OPEN_REPLAY_BUTTON = (
    int(os.getenv("OPEN_REPLAY_X", "960")),
    int(os.getenv("OPEN_REPLAY_Y", "540")),
)
SELECT_REPLAY_1 = (
    int(os.getenv("SELECT_REPLAY_1_X", "960")),
    int(os.getenv("SELECT_REPLAY_1_Y", "360")),
)
