"""Configuration values for the Flask API server."""

import os

API_TOKEN = os.getenv("API_TOKEN", "secret123")
HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
