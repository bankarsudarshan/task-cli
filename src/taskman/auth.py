import argparse
import getpass
from http import HTTPStatus

import requests

BASE_URL = "http://localhost:8000/api/v1"


def login_flow():
    print("You'll need to login first (:")
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--username", help="Username/email")

    args, _ = parser.parse_known_args()

    # If username not passed → prompt
    username = args.username or input("Username: ")

    # Always use getpass for password
    password = getpass.getpass("Password: ")

    response = requests.post(
        f"{BASE_URL}/login",
        data={"username": username, "password": password},
        timeout=10,
    )

    if response.status_code != HTTPStatus.OK:
        print("❌ Invalid credentials")
        raise SystemExit(1)

    token = response.json()["access_token"]
    print("✅ Logged in")

    return token
