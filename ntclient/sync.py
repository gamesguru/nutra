import json

from .utils import NUTRA_DIR, SERVER_HOST

import requests


def sync():
    print("not implemented ;]")


def login(email, password):

    url = f"{SERVER_HOST}/login"
    print(f"POST {url}")
    response = requests.post(url, json={"email": email, "password": password})
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
