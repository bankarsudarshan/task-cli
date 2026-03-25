import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".taskman.json"


def save_token(token: str):
    CONFIG_PATH.write_text(json.dumps({"token": token}))


def get_token():
    if not CONFIG_PATH.exists():
        return None
    try:
        data = json.loads(CONFIG_PATH.read_text())
        return data.get("token")
    except FileNotFoundError:
        return "Please login first"
