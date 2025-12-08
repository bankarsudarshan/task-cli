from pathlib import Path
from datetime import datetime, timedelta

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

CONFIG_DIR = Path.home() / ".config" / "taskman"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"


def get_calendar_service():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"Google API credentials not found at {CREDENTIALS_FILE}.\n"
                    f"Place your credentials.json there (see README for setup)."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with TOKEN_FILE.open("w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def create_event_for_task(task, timezone="Asia/Kolkata"):
    if not task.get("dueAt"):
        raise ValueError("Task has no dueAt field")

    try:
        start = datetime.strptime(task["dueAt"], "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(
            f"Invalid dueAt format for task ID {task['id']}: {task['dueAt']}. "
            "Expected YYYY-MM-DD HH:MM."
        )

    end = start + timedelta(hours=1)

    service = get_calendar_service()

    event = {
        "summary": task["description"],
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": timezone,
        },
    }

    service.events().insert(calendarId="primary", body=event).execute()
