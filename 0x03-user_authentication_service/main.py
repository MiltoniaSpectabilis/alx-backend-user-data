#!/usr/bin/env python3
"""Main test module.
"""

import requests
import json
from typing import Dict, Any

URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user.
    """
    response = requests.post(
        f"{URL}/users", data={"email": email, "password": password})
    response.raise_for_status()


def log_in(email: str, password: str) -> str:
    """Logs in a user and returns the session ID.
    """
    response = requests.post(
        f"{URL}/sessions", data={"email": email, "password": password})
    response.raise_for_status()
    return response.cookies.get("session_id")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with an incorrect password and asserts a 401 status code.
    """
    response = requests.post(
        f"{URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Attempts to access the profile without logging in and asserts a 403 status code.
    """
    response = requests.get(f"{URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Accesses the profile when logged in and asserts the email in the response.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{URL}/profile", cookies=cookies)
    response.raise_for_status()


def log_out(session_id: str) -> None:
    """Logs out a user.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{URL}/sessions", cookies=cookies)
    response.raise_for_status()


def reset_password_token(email: str) -> str:
    """Gets a reset password token.
    """
    response = requests.post(f"{URL}/reset_password", data={"email": email})
    response.raise_for_status()
    data = response.json()
    return data.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the password using the reset token.
    """
    response = requests.put(
        f"{URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password},
    )
    response.raise_for_status()


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
