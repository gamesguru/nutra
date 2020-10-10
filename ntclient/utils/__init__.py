# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane
"""

import os
import json
from shutil import copyfile

from ..core import NUTRA_DIR

# TODO: init, handle when it doesn't exist yet
prefs_file = f"{NUTRA_DIR}/prefs.json"
if not os.path.isfile(prefs_file):
    copyfile("resources/prefs.json", prefs_file)
prefs = json.load(open(prefs_file))

REMOTE_HOST = "https://nutra-server.herokuapp.com"
SERVER_HOST = prefs.get("NUTRA_CLI_OVERRIDE_LOCAL_SERVER_HOST", REMOTE_HOST)

TESTING = prefs.get("NUTRA_CLI_NO_ARGS_INJECT_MOCKS", False)
VERBOSITY = prefs.get("VERBOSITY", 1)


profile_id = prefs["current_user"]  # guid computed by __init__ in .sqlfuncs
email = prefs.get("email")
login_token = prefs.get("token")
