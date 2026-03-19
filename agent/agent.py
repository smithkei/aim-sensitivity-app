"""Windows polling agent for executing Overwatch replay commands."""

from __future__ import annotations

import time

import requests

import config
from actions import COMMAND_HANDLERS


class AgentError(Exception):
    """Raised when a remote API call fails unexpectedly."""


def fetch_command() -> str | None:
    """Poll the API for the next pending command."""
    response = requests.get(
        f"{config.API_BASE_URL}/get-command",
        params={"token": config.API_TOKEN},
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("command")


def notify_complete(command: str) -> None:
    """Notify the API that the command was executed."""
    response = requests.post(
        f"{config.API_BASE_URL}/complete",
        json={"token": config.API_TOKEN, "command": command},
        timeout=10,
    )
    response.raise_for_status()


def execute_command(command: str) -> None:
    """Execute a supported command locally on the Windows PC."""
    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        raise AgentError(f"Unsupported command received: {command}")
    handler()


def main() -> None:
    """Run the command polling loop forever."""
    print("Starting Overwatch replay agent...")
    while True:
        try:
            command = fetch_command()
            if command:
                print(f"Executing command: {command}")
                execute_command(command)
                notify_complete(command)
        except requests.RequestException as exc:
            print(f"Network error while polling API: {exc}")
        except AgentError as exc:
            print(exc)
        except Exception as exc:  # noqa: BLE001 - keep agent alive in production polling loop
            print(f"Unexpected error while executing command: {exc}")

        time.sleep(config.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
