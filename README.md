# Overwatch Replay Remote Control System

This project provides a polling-based remote control workflow for running Overwatch replays on a Windows PC from a smartphone browser.

## Project structure

```text
project-root/
  server/
  agent/
  client/
```

## Components

### 1. Flask API server

The API stores the latest command in memory and exposes three authenticated endpoints:

- `POST /send-command` queues a command.
- `GET /get-command` returns the latest command and immediately clears it.
- `POST /complete` records that the Windows agent finished processing a command.

A `GET /health` endpoint is also included for smoke testing.

### 2. Windows agent

The polling agent uses `requests` and `pyautogui` to fetch commands every 2 seconds and map them to local automation functions.

Supported commands:

- `start_ow`
- `open_replay`
- `select_replay_1`
- `play_pause`

### 3. Mobile web client

The client is a simple static site with a placeholder OBS `<video>` embed and buttons for each command.

## Setup

### Prerequisites

- Python 3.11+
- Windows PC for the agent
- OBS already configured to expose a stream URL

### Install dependencies

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Configuration

All three components use the shared token `secret123` by default. Override settings with environment variables as needed.

### Server environment variables

- `API_TOKEN`
- `SERVER_HOST`
- `SERVER_PORT`
- `FLASK_DEBUG`

### Agent environment variables

- `API_BASE_URL`
- `API_TOKEN`
- `POLL_INTERVAL_SECONDS`
- `OVERWATCH_EXECUTABLE`
- `OPEN_REPLAY_X` / `OPEN_REPLAY_Y`
- `SELECT_REPLAY_1_X` / `SELECT_REPLAY_1_Y`

## Running the server

```bash
cd server
python app.py
```

The Flask server listens on `http://127.0.0.1:5000` by default.

## Running the Windows agent

```bash
cd agent
python agent.py
```

The agent will:

1. Poll `GET /get-command?token=...` every 2 seconds.
2. Execute the mapped automation function when a command is returned.
3. Notify the API with `POST /complete` after each successful execution.

> Update the coordinate values in `agent/config.py` or with environment variables so they match your Overwatch UI layout and display resolution.

## Serving the mobile client

You can host the `client/` directory with any static file server.

Example using Python:

```bash
cd client
python -m http.server 8080
```

Open `http://<server-ip>:8080` on your smartphone browser, and update the following values for your environment:

- `http://YOUR_STREAM_URL` in `client/index.html`
- `API_BASE_URL` and `API_TOKEN` in `client/app.js` if your server is not the default local address/token

## API examples

Queue a command:

```bash
curl -X POST http://127.0.0.1:5000/send-command \
  -H "Content-Type: application/json" \
  -d '{"command":"start_ow","token":"secret123"}'
```

Fetch a command:

```bash
curl "http://127.0.0.1:5000/get-command?token=secret123"
```

Mark a command complete:

```bash
curl -X POST http://127.0.0.1:5000/complete \
  -H "Content-Type: application/json" \
  -d '{"command":"start_ow","token":"secret123"}'
```

## Notes

- Commands are kept in memory only; restarting the server clears pending state.
- The agent keeps running even if polling or command execution encounters a transient error.
- `pyautogui` automation must run in an unlocked Windows desktop session.
