#!/usr/bin/env python3
"""
cc_admin_client.py -- Client for the CrystalCore.OS admin API
(backend/app). Requires the server to be running (see backend/README.md).

Usage:
    CC_ADMIN_USER=admin CC_ADMIN_PASSWORD=... python3 backend/scripts/cc_admin_client.py
"""

import os
import sys

import requests

BASE_URL = os.environ.get("CC_ADMIN_BASE_URL", "http://localhost:8080")
USERNAME = os.environ.get("CC_ADMIN_USER")
PASSWORD = os.environ.get("CC_ADMIN_PASSWORD")
CONTAINER_ID = os.environ.get("CC_CONTAINER_ID", "cc-container-01")


def login(session: requests.Session) -> str:
    if not USERNAME or not PASSWORD:
        sys.exit("Set CC_ADMIN_USER and CC_ADMIN_PASSWORD in the environment.")

    resp = session.post(
        f"{BASE_URL}/api/v1/admin/login",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_diagnostics(session: requests.Session, token: str) -> dict:
    resp = session.get(f"{BASE_URL}/api/v1/admin/diagnostics", headers=_auth_headers(token), timeout=10)
    resp.raise_for_status()
    return resp.json()


def list_containers(session: requests.Session, token: str) -> list:
    resp = session.get(f"{BASE_URL}/api/v1/admin/containers", headers=_auth_headers(token), timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_container_terminal(session: requests.Session, token: str, container_id: str) -> dict:
    resp = session.get(
        f"{BASE_URL}/api/v1/admin/containers/{container_id}/terminal",
        headers=_auth_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    session = requests.Session()
    token = login(session)

    print("Diagnostics:", get_diagnostics(session, token))
    print("Containers:", list_containers(session, token))
    print(f"Terminal ({CONTAINER_ID}):", get_container_terminal(session, token, CONTAINER_ID))


if __name__ == "__main__":
    main()
