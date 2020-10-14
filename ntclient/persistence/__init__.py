# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:09:07 2019

@author: shane
"""

import os
import json

from .. import NUTRA_DIR

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

# TODO: init, handle when it doesn't exist yet
prefs_file = f"{NUTRA_DIR}/prefs.json"
if os.path.isfile(prefs_file):
    prefs = json.load(open(prefs_file))
else:
    prefs = dict()

REMOTE_HOST = "https://nutra-server.herokuapp.com"
SERVER_HOST = prefs.get("NUTRA_CLI_OVERRIDE_LOCAL_SERVER_HOST", REMOTE_HOST)

TESTING = prefs.get("NUTRA_CLI_NO_ARGS_INJECT_MOCKS", False)
VERBOSITY = prefs.get("VERBOSITY", 1)


profile_id = prefs.get("current_user")  # guid computed by __init__ in .sqlfuncs
email = prefs.get("email")
login_token = prefs.get("token")
