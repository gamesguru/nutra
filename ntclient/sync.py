import json

from .utils import NUTRA_DIR, SERVER_HOST

import requests


def sync():
    print("not implemented ;]")


def register(email, password):
    print("not implemented ;]")


def login(email, password):
    import getpass
    import socket
    import sys

    hostname = socket.gethostname()
    username = getpass.getuser()
    oper_sys = sys.platform

    url = f"{SERVER_HOST}/v2/login"
    print(f"POST {url}")
    response = requests.post(
        url,
        json={
            "email": email,
            "password": password,
            "os": oper_sys,
            "hostname": hostname,
            "username": username,
        },
    )
    res = response.json()
    data = res["data"]
    if "error" in data:
        print("error: " + data["error"])
        return

    with open(f"{NUTRA_DIR}/admin.json", "r") as f:
        admin_json = json.load(f)

    with open(f"{NUTRA_DIR}/admin.json", "w+") as f:
        admin_json["email"] = email
        admin_json["token"] = data["token"]
        f.write(json.dumps(admin_json, indent=4))
    print("Logged in.")
