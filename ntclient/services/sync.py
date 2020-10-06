import json

from ..utils import NUTRA_DIR, SERVER_HOST
from ..utils.sqlfuncs.nt import sql_inserted_or_updated_entities, sql_last_sync

import requests


def sync():
    def get():
        params = {"uid": profile_guid, "last_sync": last_sync}

        print(f"GET {url}")
        response = requests.get(
            url, params=params, headers={"Authorization": f"Bearer {token}"}
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
            url, json=data, headers={"Authorization": f"Bearer {token}"}
        )
        res = response.json()
        data = res["data"]
        if "error" in data:
            print("error: " + data["error"])
            return

        print(data)

    # TODO: use real profile_id
    url = f"{SERVER_HOST}/sync"
    last_sync = sql_last_sync()

    profile_id = 1
    profile_guid = "a0fdac7ab369de43f029a460879c854f"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiYXV0aC1sZXZlbCI6MjAsImV4cGlyZXMiOjE5MTU5ODQyMjl9.L66fkA-9Yq6Y0AhqlEuZh8w1Hh0BJGkNjAJHv71kOHY"
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

    with open(f"{NUTRA_DIR}/admin.json", "r") as f:
        admin_json = json.load(f)

    with open(f"{NUTRA_DIR}/admin.json", "w+") as f:
        admin_json["email"] = email
        admin_json["token"] = data["token"]
        f.write(json.dumps(admin_json, indent=4))
    print("Logged in.")
