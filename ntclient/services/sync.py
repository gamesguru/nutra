import json

import requests

from .. import NUTRA_DIR
from ..persistence.sql import profile_guid
from ..persistence.sql.nt import sql_inserted_or_updated_entities, sql_last_sync
from ..persistence import SERVER_HOST, login_token


def sync():
    def get():
        params = {"uid": profile_guid, "last_sync": last_sync}

        print(f"GET {url}")
        response = requests.get(
            url, params=params, headers={"Authorization": f"Bearer {login_token}"}
        )
        res = response.json()
        data = res["data"]
        if "error" in data:
            print("error: " + data["error"])
            return

        print(data)

    def post():
        profiles, bio_logs = sql_inserted_or_updated_entities(last_sync)
        data = {
            "uid": profile_guid,
            "entities": {"profiles": profiles, "bio_logs": bio_logs},
        }

        print(f"POST {url}")
        response = requests.post(
            url, json=data, headers={"Authorization": f"Bearer {login_token}"}
        )
        res = response.json()
        data = res["data"]
        if "error" in data:
            print("error: " + data["error"])
            return

        print(data)

    # Make GET and POST reqeusts to /sync
    url = f"{SERVER_HOST}/sync"
    last_sync = sql_last_sync()
    get()
    post()


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

    with open(f"{NUTRA_DIR}/prefs.json", "r") as f:
        prefs_json = json.load(f)

    with open(f"{NUTRA_DIR}/prefs.json", "w+") as f:
        prefs_json["email"] = email
        prefs_json["token"] = data["token"]
        f.write(json.dumps(prefs_json, indent=4))
    print("Logged in.")
