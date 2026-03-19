"""Flask API server for the Overwatch replay remote control system."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import Flask, jsonify, request

import config
from state import get_last_completed_command, mark_completed, pop_command, set_command

app = Flask(__name__)


def require_token(route_handler: Callable[..., Any]) -> Callable[..., Any]:
    """Reject requests that do not include the expected shared token."""

    @wraps(route_handler)
    def wrapper(*args: Any, **kwargs: Any):
        payload = request.get_json(silent=True) or {}
        token = payload.get("token") or request.args.get("token")
        if token != config.API_TOKEN:
            return jsonify({"error": "Invalid token"}), 401
        return route_handler(*args, **kwargs)

    return wrapper


@app.get("/health")
def healthcheck():
    """Simple liveness endpoint for smoke testing and monitoring."""
    return jsonify({"status": "ok", "last_completed": get_last_completed_command()})


@app.post("/send-command")
@require_token
def send_command():
    """Store the latest command sent by the mobile client."""
    payload = request.get_json(silent=True) or {}
    command = payload.get("command", "").strip()

    if not command:
        return jsonify({"error": "Command is required"}), 400

    set_command(command)
    return jsonify({"status": "queued", "command": command})


@app.get("/get-command")
@require_token
def get_command():
    """Return the current command to the polling agent and clear it."""
    command = pop_command()
    return jsonify({"command": command})


@app.post("/complete")
@require_token
def complete_command():
    """Record completion notifications from the Windows agent."""
    payload = request.get_json(silent=True) or {}
    mark_completed(payload.get("command"))
    return jsonify({"status": "received", "command": payload.get("command")})


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
