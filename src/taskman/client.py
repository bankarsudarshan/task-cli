from http import HTTPStatus

import requests

from taskman.auth import login_flow
from taskman.config import get_token, save_token

BASE_URL = "http://localhost:8000/api/v1"


def request(method: str, path: str, **kwargs):
    headers = kwargs.pop("headers", {})

    token = get_token()

    # 🔥 If no token → trigger login
    if not token:
        token = login_flow()
        save_token(token)

    headers["Authorization"] = f"Bearer {token}"
    response = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=headers,
        timeout=10,
        **kwargs,
    )

    # 🔥 If token expired → re-login once
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        print("⚠️ Session expired. Please login again.\n")
        token = login_flow()
        save_token(token)
        headers["Authorization"] = f"Bearer {token}"

        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            headers=headers,
            timeout=10,
            **kwargs,
        )

    if not response.ok:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        raise SystemExit(1)

    return response
